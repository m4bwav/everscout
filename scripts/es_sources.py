"""es_sources.py - source adapters for everscout.

Every network read goes through Fetcher.get: one cache, one pace per host,
an honest User-Agent that names the tool and a contact. Each adapter turns a
platform's public, logged-out surface into the same item shape:

  {id, platform, kind (post|comment), title, author, url, published (ISO),
   text, media [..], community, comments (count or None), points (or None),
   source (the watch-list row), listing}

Standard library only. Nothing here posts, logs in, or scrapes HTML pages:
feeds and documented public JSON endpoints only (see kb/platforms.md).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UTC = dt.timezone.utc
ATOM = "{http://www.w3.org/2005/Atom}"
MEDIA_NS = "{http://search.yahoo.com/mrss/}"
YT_NS = "{http://www.youtube.com/xml/schemas/2015}"
DC_NS = "{http://purl.org/dc/elements/1.1/}"
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}"
RDF_NS = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
RSS1_NS = "{http://purl.org/rss/1.0/}"

# Seconds between requests to one host. Reddit's logged-out feeds allow about one a
# minute (x-ratelimit-reset is honoured on top); documented APIs get a polite gap.
DEFAULT_HOST_GAPS = {
    "www.reddit.com": 45,
    "reddit.com": 45,
    "hn.algolia.com": 1,
    "hacker-news.firebaseio.com": 1,
    "rss.arxiv.org": 5,
    "export.arxiv.org": 15,  # the terms say 3 s; on 2026-09-26 bursts at 4 s drew 406s, so stay well above it
    "public.api.bsky.app": 1,
    "bsky.app": 2,
    "www.youtube.com": 2,
    "github.com": 2,
    "api.github.com": 2,
    "news.google.com": 10,
    "musicbrainz.org": 1.1,
    "api.gdeltproject.org": 6,  # GDELT asks for at most one request every 5 s (its refusal text, 2026-09-27)
    "wikimedia.org": 1,
    "default": 3,
}

MEDIA_HINTS = {
    "video": ("v.redd.it", "youtube.com/watch", "youtu.be", "vimeo.com", "streamable", ".mp4", ".webm", ".gifv", "tiktok.com"),
    "image": ("i.redd.it", "i.imgur", "preview.redd.it", ".png", ".jpg", ".jpeg", ".gif", ".webp"),
    "audio": ("soundcloud.com", "bandcamp.com", "open.spotify.com", "music.apple.com", ".mp3", ".wav", ".flac", "audiomack"),
    "code": ("github.com/", "gitlab.com/", "huggingface.co/", "codeberg.org/"),
    "paper": ("arxiv.org/", "doi.org/", "ssrn.com/", "nber.org/papers", "openreview.net"),
    "data": ("fred.stlouisfed.org", "data.worldbank.org", "data.imf.org", "ourworldindata.org", "data.ecb.europa.eu", ".csv"),
    "store": ("store.steampowered.com", "itch.io", "play.google", "apps.apple", "gumroad.com", "patreon.com"),
}


# ---------------------------------------------------------------- time and text

def now_utc():
    return dt.datetime.now(UTC)


def iso(ts):
    return ts.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_time(s):
    """ISO 8601, RFC 822 (RSS pubDate) or a Unix timestamp, to an aware datetime; None when unparseable."""
    if s is None or s == "":
        return None
    if isinstance(s, (int, float)):
        return dt.datetime.fromtimestamp(s, UTC)
    s = str(s).strip()
    if re.fullmatch(r"\d{9,11}", s):
        return dt.datetime.fromtimestamp(int(s), UTC)
    try:
        t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=UTC)
    except ValueError:
        pass
    try:
        from email.utils import parsedate_to_datetime
        t = parsedate_to_datetime(s)
        return t if t.tzinfo else t.replace(tzinfo=UTC)
    except Exception:
        return None


def strip_html(s):
    s = html.unescape(s or "")
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def media_of(*texts):
    low = " ".join(t or "" for t in texts).lower()
    return [k for k, hints in MEDIA_HINTS.items() if any(h in low for h in hints)]


def short_hash(s, n=12):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:n]


# ---------------------------------------------------------------- fetching

class FetchError(Exception):
    def __init__(self, url, code, msg=""):
        super().__init__(f"{code} {url} {msg}".strip())
        self.url, self.code = url, code


class Fetcher:
    """Paced, cached HTTP GET. State files live in `local` (never in the data folder)."""

    def __init__(self, local, user_agent, reddit_user_agent=None, host_gaps=None, log=None, sleep=time.sleep, opener=None):
        self.local = local
        self.ua = user_agent
        self.reddit_ua = reddit_user_agent or user_agent
        self.gaps = dict(DEFAULT_HOST_GAPS)
        self.gaps.update(host_gaps or {})
        self.log = log or (lambda m: None)
        self.sleep = sleep
        self.opener = opener or urllib.request.urlopen
        self.fetched = 0
        self.cached = 0
        self.timeout = 40
        self.retry = True  # False: fail at once on 429, 503 or 406 (statistics collection must not stall a scan)

    # state
    def _rl_path(self):
        return os.path.join(self.local, "ratelimit.json")

    def _load(self, path, default):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def _save(self, path, obj):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
        os.replace(tmp, path)

    def cache_path(self, url):
        return os.path.join(self.local, "cache", "http", short_hash(url, 20))

    def gap_for(self, host):
        return float(self.gaps.get(host, self.gaps.get("default", 3)))

    def _wait(self, host):
        st = self._load(self._rl_path(), {})
        delay = st.get(host, 0) - time.time()
        if delay > 0:
            self.log(f"pacing: waiting {delay:.0f}s before the next request to {host}")
            self.sleep(delay)

    def _mark(self, host, seconds):
        st = self._load(self._rl_path(), {})
        st[host] = time.time() + seconds
        self._save(self._rl_path(), st)

    def get(self, url, ttl=3600, force=False, accept="*/*"):
        """Body text (str) for url; from the cache when younger than ttl. Returns (text, from_cache, status).
        404 and 410 return ('', False, code) and are cached, so a dead source costs one request per ttl."""
        cp = self.cache_path(url)
        meta = self._load(cp + ".json", {})
        if not force and os.path.exists(cp) and time.time() - meta.get("fetched_at", 0) < ttl:
            self.cached += 1
            with open(cp, encoding="utf-8") as f:
                return f.read(), True, meta.get("status", 200)
        host = urllib.parse.urlsplit(url).hostname or "default"
        gap = self.gap_for(host)
        is_reddit = host.endswith("reddit.com")
        headers = {"User-Agent": self.reddit_ua if is_reddit else self.ua, "Accept": accept}
        tries = 0
        while True:
            tries += 1
            self._wait(host)
            req = urllib.request.Request(url, headers=headers)
            try:
                with self.opener(req, timeout=self.timeout) as r:
                    raw = r.read()
                    charset = r.headers.get_content_charset() or "utf-8"
                    body = raw.decode(charset, "replace")
                    wait = gap
                    reset = r.headers.get("x-ratelimit-reset")
                    if reset:
                        try:
                            wait = max(gap, float(reset) + 3)
                        except ValueError:
                            pass
                    self._mark(host, wait)
                    os.makedirs(os.path.dirname(cp), exist_ok=True)
                    with open(cp, "w", encoding="utf-8") as f:
                        f.write(body)
                    self._save(cp + ".json", {"url": url, "fetched_at": time.time(), "status": r.status})
                    self.fetched += 1
                    return body, False, r.status
            except urllib.error.HTTPError as e:
                self._mark(host, gap)
                if e.code in (503, 406) and tries < 3 and self.retry:  # busy or a transient refusal (arXiv, MusicBrainz): back off
                    wait = 15 * tries
                    self.log(f"{e.code} from {host}; waiting {wait}s (try {tries})")
                    self._mark(host, wait)
                    continue
                if e.code == 429 and tries < 4 and self.retry:
                    retry = e.headers.get("Retry-After") if e.headers else None
                    wait = float(retry) if retry and retry.isdigit() else 60 * tries
                    self.log(f"429 from {host}; waiting {wait:.0f}s (try {tries})")
                    self._mark(host, wait)
                    continue
                if e.code in (404, 410):
                    self._save(cp + ".json", {"url": url, "fetched_at": time.time(), "status": e.code})
                    with open(cp, "w", encoding="utf-8") as f:
                        f.write("")
                    return "", False, e.code
                raise FetchError(url, e.code, str(e.reason))
            except urllib.error.URLError as e:
                self._mark(host, gap)
                raise FetchError(url, "network", str(e.reason))
            except (TimeoutError, OSError) as e:  # a read that times out is not always wrapped in URLError
                self._mark(host, gap)
                raise FetchError(url, "timeout", str(e) or "timed out")

    def get_json(self, url, ttl=3600, force=False):
        text, cached, status = self.get(url, ttl=ttl, force=force, accept="application/json")
        if not text.strip():
            return None, cached, status
        try:
            return json.loads(text), cached, status
        except ValueError:
            raise FetchError(url, status, "not JSON (a login wall or an HTML error page?)")


# ---------------------------------------------------------------- feeds (Atom, RSS 2.0, RSS 1.0)

def _t(el, tag):
    x = el.find(tag)
    return (x.text or "") if x is not None and x.text else ""


def parse_feed(text, feed_url="", platform="rss"):
    """Entries of an Atom, RSS 2.0 or RSS 1.0 (RDF) document, as items. Raises ValueError on non-XML (a block page)."""
    if not text or not text.strip():
        return []
    try:
        root = ET.fromstring(text.lstrip("﻿"))
    except ET.ParseError as e:
        raise ValueError(f"not a feed ({e}); first bytes: {text.strip()[:80]!r}")
    items = []
    if root.tag == ATOM + "feed":
        feed_cat = root.find(ATOM + "category")
        for e in root.findall(ATOM + "entry"):
            link = ""
            for l in e.findall(ATOM + "link"):
                if l.get("rel", "alternate") == "alternate":
                    link = l.get("href", "")
                    break
            if not link and e.find(ATOM + "link") is not None:
                link = e.find(ATOM + "link").get("href", "")
            content = _t(e, ATOM + "content") or _t(e, ATOM + "summary")
            mg = e.find(MEDIA_NS + "group")
            if not content and mg is not None:  # YouTube puts the description here
                content = _t(mg, MEDIA_NS + "description")
            cat = e.find(ATOM + "category")
            if cat is None:
                cat = feed_cat
            items.append({
                "id": _t(e, ATOM + "id") or link,
                "title": html.unescape(_t(e, ATOM + "title")),
                "author": _t(e, ATOM + "author/" + ATOM + "name"),
                "url": link,
                "published": _t(e, ATOM + "published") or _t(e, ATOM + "updated"),
                "html": content,
                "community": (cat.get("term") if cat is not None else "") or "",
            })
    else:
        channel = root.find("channel")
        entries = channel.findall("item") if channel is not None else []
        if not entries:
            entries = root.findall(RSS1_NS + "item") or root.findall("item")
        for e in entries:
            link = _t(e, "link") or _t(e, RSS1_NS + "link") or (e.get(RDF_NS + "about") or "")
            content = _t(e, CONTENT_NS + "encoded") or _t(e, "description") or _t(e, RSS1_NS + "description")
            items.append({
                "id": _t(e, "guid") or link,
                "title": html.unescape(_t(e, "title") or _t(e, RSS1_NS + "title")),
                "author": _t(e, DC_NS + "creator") or _t(e, "author"),
                "url": link.strip(),
                "published": _t(e, "pubDate") or _t(e, DC_NS + "date"),
                "html": content,
                "community": _t(e, "category"),
            })
    out = []
    for it in items:
        pub = parse_time(it["published"])
        text_body = strip_html(it["html"])
        out.append({
            "id": f"{platform}:{short_hash(it['id'] or it['url'])}",
            "platform": platform,
            "kind": "post",
            "title": it["title"].strip(),
            "author": it["author"].strip(),
            "url": it["url"],
            "published": iso(pub) if pub else "",
            "text": text_body[:6000],
            "media": media_of(it["html"], it["url"]),
            "community": it["community"],
            "comments": None,
            "points": None,
            "feed": feed_url,
        })
    return out


# ---------------------------------------------------------------- Reddit (logged-out Atom feeds only)

def reddit_listing_url(sub, listing="new", t="week"):
    sub = re.sub(r"^/?r/", "", sub)
    if listing == "top":
        return f"https://www.reddit.com/r/{sub}/top/.rss?t={t}"
    return f"https://www.reddit.com/r/{sub}/{listing}/.rss"


def reddit_multi_url(subs, listing="new", limit=100):
    """One logged-out feed for several subreddits (`r/a+b+c`); each entry keeps its subreddit in <category>."""
    names = "+".join(re.sub(r"^/?r/", "", s) for s in subs)
    return f"https://www.reddit.com/r/{names}/{listing}/.rss?limit={limit}"


def reddit_thread_url(url_or_id):
    s = url_or_id.strip()
    if s.startswith("http"):
        s = s.split("?")[0].split("#")[0].rstrip("/")
        s = re.sub(r"^https?://(old\.|new\.|np\.)?reddit\.com", "https://www.reddit.com", s)
        return s + "/.rss"
    return f"https://www.reddit.com/comments/{s}/.rss"


def reddit_post_id(link):
    m = re.search(r"/comments/([a-z0-9]+)", link or "")
    return m.group(1) if m else None


def parse_reddit(text, feed_url=""):
    items = parse_feed(text, feed_url, platform="reddit")
    for it in items:
        # reddit ids: t3_ posts, t1_ comments; comment titles read "/u/name on <post title>"
        is_comment = bool(re.match(r"^/u/[^ ]+ on ", it["title"]))
        it["kind"] = "comment" if is_comment else "post"
        it["author"] = it["author"].replace("/u/", "")
        pid = reddit_post_id(it["url"])
        if it["kind"] == "post" and pid:
            it["id"] = f"reddit:{pid}"
        it["post_id"] = pid
        if not it["community"] and "/r/" in it["url"]:
            it["community"] = re.sub(r".*/r/([^/]+)/.*", r"\1", it["url"])
    return items


# ---------------------------------------------------------------- Hacker News (Algolia search API)

HN_API = "https://hn.algolia.com/api/v1"


def hn_search_url(query, since_ts=None, tags="story", by_date=True, hits=50):
    params = {"query": query, "tags": tags, "hitsPerPage": str(hits)}
    if since_ts:
        params["numericFilters"] = f"created_at_i>{int(since_ts)}"
    return f"{HN_API}/{'search_by_date' if by_date else 'search'}?" + urllib.parse.urlencode(params)


def parse_hn_hits(data, feed_url=""):
    out = []
    for h in (data or {}).get("hits", []):
        oid = h.get("objectID")
        title = h.get("title") or h.get("story_title") or ""
        is_comment = "comment" in (h.get("_tags") or []) or (not h.get("title") and h.get("comment_text"))
        text = strip_html(h.get("story_text") or h.get("comment_text") or "")
        link = h.get("url") or h.get("story_url") or ""
        out.append({
            "id": f"hn:{oid}",
            "platform": "hn",
            "kind": "comment" if is_comment else "post",
            "title": title,
            "author": h.get("author") or "",
            "url": f"https://news.ycombinator.com/item?id={(h.get('story_id') or oid) if is_comment else oid}",
            "link": link,
            "published": h.get("created_at") or "",
            "text": text[:6000],
            "media": media_of(link),
            "community": "hn",
            "comments": h.get("num_comments"),
            "points": h.get("points"),
            "feed": feed_url,
        })
    return out


def hn_item_id(url_or_id):
    m = re.search(r"id=(\d+)", url_or_id) or re.fullmatch(r"(?:hn:)?(\d+)", url_or_id.strip())
    return m.group(1) if m else None


def parse_hn_item(data):
    """An Algolia /items/<id> tree to {post, comments} with a flat comment list (depth kept)."""
    if not data:
        return None
    post = {
        "id": f"hn:{data.get('id')}", "platform": "hn", "kind": "post", "title": data.get("title") or "",
        "author": data.get("author") or "", "url": f"https://news.ycombinator.com/item?id={data.get('id')}",
        "link": data.get("url") or "", "published": data.get("created_at") or "",
        "text": strip_html(data.get("text") or "")[:6000], "media": media_of(data.get("url") or ""),
        "community": "hn", "points": data.get("points"), "comments": None,
    }
    comments = []

    def walk(node, depth):
        for ch in node.get("children") or []:
            if ch.get("type") == "comment" and ch.get("text"):
                comments.append({
                    "id": f"hn:{ch.get('id')}", "platform": "hn", "kind": "comment", "author": ch.get("author") or "",
                    "published": ch.get("created_at") or "", "text": strip_html(ch.get("text"))[:4000],
                    "depth": depth, "parent": f"hn:{ch.get('parent_id')}",
                    "url": f"https://news.ycombinator.com/item?id={ch.get('id')}",
                })
            walk(ch, depth + 1)
    walk(data, 0)
    post["comments"] = len(comments)
    return {"post": post, "comments": comments}


# ---------------------------------------------------------------- Bluesky (public AppView, no login)

BSKY_API = "https://public.api.bsky.app/xrpc"


def bsky_web_url(uri, handle):
    rkey = uri.rsplit("/", 1)[-1]
    return f"https://bsky.app/profile/{handle}/post/{rkey}"


def _bsky_item(pv, feed_url=""):
    rec = pv.get("record") or {}
    author = (pv.get("author") or {}).get("handle", "")
    text = rec.get("text") or ""
    embed = json.dumps(pv.get("embed") or {})
    return {
        "id": f"bluesky:{pv.get('uri', '').rsplit('/', 1)[-1]}", "platform": "bluesky", "kind": "post",
        "title": (text.split("\n")[0])[:140], "author": author, "url": bsky_web_url(pv.get("uri", ""), author),
        "at_uri": pv.get("uri"), "published": rec.get("createdAt") or pv.get("indexedAt") or "",
        "text": text[:6000], "media": media_of(embed, text) + (["image"] if "images" in embed else []),
        "community": "bluesky", "comments": pv.get("replyCount"), "points": pv.get("likeCount"), "feed": feed_url,
    }


def bsky_feed_url(feed_at_uri, limit=50):
    return f"{BSKY_API}/app.bsky.feed.getFeed?" + urllib.parse.urlencode({"feed": feed_at_uri, "limit": str(limit)})


def bsky_author_feed_url(actor, limit=50):
    return f"{BSKY_API}/app.bsky.feed.getAuthorFeed?" + urllib.parse.urlencode({"actor": actor, "limit": str(limit), "filter": "posts_no_replies"})


def parse_bsky_feed(data, feed_url=""):
    out = []
    for f in (data or {}).get("feed", []):
        pv = f.get("post") or {}
        if pv:
            out.append(_bsky_item(pv, feed_url))
    return out


def bsky_thread_parts(url):
    """(handle_or_did, rkey) from a bsky.app post URL or an at:// URI."""
    m = re.search(r"bsky\.app/profile/([^/]+)/post/([^/?#]+)", url) or re.match(r"at://([^/]+)/app\.bsky\.feed\.post/([^/?#]+)", url)
    return (m.group(1), m.group(2)) if m else (None, None)


def bsky_resolve_url(handle):
    return f"{BSKY_API}/com.atproto.identity.resolveHandle?handle={urllib.parse.quote(handle)}"


def bsky_thread_url(did, rkey, depth=6):
    uri = f"at://{did}/app.bsky.feed.post/{rkey}"
    return f"{BSKY_API}/app.bsky.feed.getPostThread?" + urllib.parse.urlencode({"uri": uri, "depth": str(depth)})


def parse_bsky_thread(data):
    th = (data or {}).get("thread") or {}
    if not th.get("post"):
        return None
    post = _bsky_item(th["post"])
    comments = []

    def walk(node, depth):
        for r in node.get("replies") or []:
            pv = r.get("post")
            if pv:
                c = _bsky_item(pv)
                c.update({"kind": "comment", "depth": depth})
                comments.append(c)
                walk(r, depth + 1)
    walk(th, 0)
    return {"post": post, "comments": comments}


# ---------------------------------------------------------------- Mastodon (status and context, public on most instances)

def mastodon_thread_parts(url):
    m = re.match(r"https?://([^/]+)/(?:@[^/]+|users/[^/]+/statuses)/(\d+)", url)
    return (m.group(1), m.group(2)) if m else (None, None)


def _masto_item(s, host):
    acct = (s.get("account") or {}).get("acct", "")
    text = strip_html(s.get("content") or "")
    return {
        "id": f"mastodon:{host}:{s.get('id')}", "platform": "mastodon", "kind": "post", "title": text.split("\n")[0][:140],
        "author": acct, "url": s.get("url") or s.get("uri") or "", "published": s.get("created_at") or "", "text": text[:6000],
        "media": media_of(json.dumps(s.get("media_attachments") or []), s.get("content") or ""), "community": host,
        "comments": s.get("replies_count"), "points": s.get("favourites_count"),
    }


def parse_mastodon_thread(status, context, host):
    if not status:
        return None
    post = _masto_item(status, host)
    comments = []
    for s in (context or {}).get("descendants", []):
        c = _masto_item(s, host)
        c["kind"] = "comment"
        comments.append(c)
    return {"post": post, "comments": comments}


# ---------------------------------------------------------------- Lemmy (v3 API, public)

def lemmy_thread_parts(url):
    m = re.match(r"https?://([^/]+)/post/(\d+)", url)
    return (m.group(1), m.group(2)) if m else (None, None)


def parse_lemmy_thread(post_data, comments_data, host):
    pv = (post_data or {}).get("post_view")
    if not pv:
        return None
    p = pv.get("post") or {}
    counts = pv.get("counts") or {}
    body = p.get("body") or ""
    post = {
        "id": f"lemmy:{host}:{p.get('id')}", "platform": "lemmy", "kind": "post", "title": p.get("name") or "",
        "author": (pv.get("creator") or {}).get("name", ""), "url": f"https://{host}/post/{p.get('id')}", "link": p.get("url") or "",
        "published": p.get("published") or "", "text": body[:6000], "media": media_of(p.get("url") or "", body),
        "community": (pv.get("community") or {}).get("name", ""), "comments": counts.get("comments"), "points": counts.get("score"),
    }
    comments = []
    for cv in (comments_data or {}).get("comments", []):
        c = cv.get("comment") or {}
        comments.append({
            "id": f"lemmy:{host}:c{c.get('id')}", "platform": "lemmy", "kind": "comment", "author": (cv.get("creator") or {}).get("name", ""),
            "published": c.get("published") or "", "text": (c.get("content") or "")[:4000], "depth": max(0, (c.get("path") or "0").count(".") - 1),
            "url": c.get("ap_id") or "",
        })
    return {"post": post, "comments": comments}


# ---------------------------------------------------------------- Discourse (topic JSON, public on open forums)

def discourse_thread_parts(url):
    m = re.match(r"(https?://[^/]+(?:/[^/]+)*?)/t/(?:[^/]+/)?(\d+)", url)
    return (m.group(1), m.group(2)) if m else (None, None)


def parse_discourse_topic(data, base):
    if not data or "post_stream" not in data:
        return None
    posts = data["post_stream"].get("posts") or []
    if not posts:
        return None
    first = posts[0]
    host = urllib.parse.urlsplit(base).hostname or base
    post = {
        "id": f"discourse:{host}:{data.get('id')}", "platform": "discourse", "kind": "post", "title": data.get("title") or "",
        "author": first.get("username") or "", "url": f"{base}/t/{data.get('slug', 'topic')}/{data.get('id')}",
        "published": data.get("created_at") or first.get("created_at") or "", "text": strip_html(first.get("cooked"))[:6000],
        "media": media_of(first.get("cooked") or ""), "community": host, "comments": max(0, (data.get("posts_count") or 1) - 1),
        "points": data.get("like_count"),
    }
    comments = [{
        "id": f"discourse:{host}:p{p.get('id')}", "platform": "discourse", "kind": "comment", "author": p.get("username") or "",
        "published": p.get("created_at") or "", "text": strip_html(p.get("cooked"))[:4000], "depth": 0,
        "url": f"{post['url']}/{p.get('post_number')}",
    } for p in posts[1:]]
    return {"post": post, "comments": comments}


# ---------------------------------------------------------------- Hugging Face (trending models, spaces, daily papers)

def huggingface_url(spec, limit=30):
    """spec like 'models?pipeline_tag=text-to-video', 'spaces', 'daily_papers'; trending sort is added when none is given."""
    path, _, q = spec.partition("?")
    params = dict(urllib.parse.parse_qsl(q))
    if path in ("models", "spaces"):
        params.setdefault("sort", "trendingScore")
        params.setdefault("limit", str(limit))
    return f"https://huggingface.co/api/{path}" + ("?" + urllib.parse.urlencode(params) if params else "")


def parse_huggingface(data, feed_url=""):
    out = []
    kind = "spaces" if "/api/spaces" in feed_url else "daily_papers" if "daily_papers" in feed_url else "models"
    for d in data or []:
        if kind == "daily_papers":
            p = d.get("paper") or {}
            pid = p.get("id") or ""
            out.append({"id": f"huggingface:paper:{pid}", "platform": "huggingface", "kind": "post", "title": p.get("title") or d.get("title") or "",
                        "author": "", "url": f"https://huggingface.co/papers/{pid}", "published": p.get("publishedAt") or d.get("publishedAt") or "",
                        "text": (p.get("summary") or "")[:3000], "media": ["paper"], "community": "hf-papers",
                        "comments": d.get("numComments"), "points": p.get("upvotes"), "feed": feed_url})
            continue
        rid = d.get("id") or d.get("modelId") or ""
        url = f"https://huggingface.co/{'spaces/' if kind == 'spaces' else ''}{rid}"
        tags = d.get("tags") or []
        out.append({"id": f"huggingface:{kind}:{rid}", "platform": "huggingface", "kind": "post", "title": rid, "author": rid.split("/")[0],
                    "url": url, "published": d.get("createdAt") or d.get("lastModified") or "",
                    "text": " ".join([d.get("pipeline_tag") or ""] + [t for t in tags if ":" not in t][:20]),
                    "media": ["code"], "community": f"hf-{kind}", "comments": None, "points": d.get("likes"),
                    "trending": d.get("trendingScore"), "downloads": d.get("downloads"), "feed": feed_url})
    return out


# ---------------------------------------------------------------- convenience URL builders for generic feeds

def youtube_channel_feed(channel_id):
    if channel_id.startswith("PL"):
        return f"https://www.youtube.com/feeds/videos.xml?playlist_id={channel_id}"
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def github_releases_feed(repo):
    return f"https://github.com/{repo.strip('/')}/releases.atom"


def google_news_feed(query, hl="en-US", gl="US"):
    q = urllib.parse.quote(query)
    ceid = f"{gl}:{hl.split('-')[0]}"
    return f"https://news.google.com/rss/search?q={q}&hl={hl}&gl={gl}&ceid={ceid}"


def arxiv_query_feed(query, max_results=50):
    params = {"search_query": query, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": str(max_results)}
    return "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)


# ---------------------------------------------------------------- statistics sources (beat metrics)

def gdelt_timeline_url(query, raw=False, start=None, end=None, timespan="3months"):
    """GDELT DOC 2.0 timeline. TimelineVol is the share (%) of all monitored coverage; TimelineVolRaw is the count."""
    params = {"query": query, "mode": "TimelineVolRaw" if raw else "TimelineVol", "format": "json"}
    if start and end:
        params["startdatetime"] = start.strftime("%Y%m%d000000")
        params["enddatetime"] = end.strftime("%Y%m%d235959")
    else:
        params["timespan"] = timespan
    return "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)


def parse_gdelt_timeline(data):
    """[(date 'YYYY-MM-DD', value float)] from a TimelineVol or TimelineVolRaw JSON body (first series)."""
    out = []
    for series in (data or {}).get("timeline") or []:
        for pt in series.get("data") or []:
            d = str(pt.get("date") or "")
            if len(d) >= 8 and d[:8].isdigit():
                try:
                    out.append((f"{d[:4]}-{d[4:6]}-{d[6:8]}", float(pt.get("value") or 0)))
                except (TypeError, ValueError):
                    continue
        break
    return out


def wikimedia_pageviews_url(project, article, start, end, agent="user"):
    art = urllib.parse.quote(article.replace(" ", "_"), safe="")
    return (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/all-access/{agent}/{art}/daily/"
            f"{start.strftime('%Y%m%d')}00/{end.strftime('%Y%m%d')}00")


def parse_wikimedia_pageviews(data):
    out = []
    for it in (data or {}).get("items") or []:
        ts = str(it.get("timestamp") or "")
        if len(ts) >= 8:
            out.append((f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}", float(it.get("views") or 0)))
    return out
