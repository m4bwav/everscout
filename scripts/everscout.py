#!/usr/bin/env python3
"""everscout.py - the CLI behind the everscout skills.

A *beat* is one subject the user keeps up with (AI video, global economics,
down-tempo music...). A beat is a folder of five markdown files: beat.md
(scope and settings), sources.md (the watch list), vocab.md (the entities to
tally, with aliases), questions.md (seeds for asking makers about their work)
and searches.md (web searches with cadences), plus study.md (the outline of the
baseline study). Built-in beats ship under <repo>/beats; private beats live in
the folders listed in the user's config (`beat_dirs`) and win on a name clash.

What the CLI does: fetch every source of a beat at a polite per-host pace
through feeds and documented public endpoints (es_sources.py), keep a cache
that is purged after 48 hours, scaffold one distilled note per worthwhile
thread or page, tally the vocabulary into signals (counts, velocity, spread),
regenerate indexes, and keep one engagement ledger with pace rules so that a
person's questions to makers never look automated. It never posts: the
engagement route is draft, approve, paste, record.

Paths (`everscout.py where` prints them):
  HOME   = $EVERSCOUT_HOME or ~/.everscout        config.json, private beats, voice.md
  BEATS  = $EVERSCOUT_BEATS, then beat_dirs, then ./beats   first match of a slug wins
  DATA   = beats.<slug>.data or data_root/<slug>  notes/, reports/, study/, signals/, sources/, log.md, HANDOFF.md
  LEDGER = ledger or data_root/_engage            engagements.jsonl, INDEX.md (all beats: pacing is per account)
  LOCAL  = local_root                             cache/, ratelimit.json, state-<slug>.json, drafts/
Standard library only; runs on Windows, macOS and Linux with Python 3.9+.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import es_sources as S  # noqa: E402

VERSION = "0.8.4"
UTC = dt.timezone.utc

DEFAULT_CONFIG = {
    "contact": "",
    "reddit_user": "",
    "data_root": "~/.everscout/data",
    "local_root": "~/.everscout/local",
    "ledger": "",
    "beat_dirs": ["~/.everscout/beats"],
    "beats": {},
    "voice": "~/.everscout/voice.md",
    "pace": {"hosts": {}, "feed_ttl_seconds": 3600, "thread_ttl_seconds": 1800},
    # reader: rss (Reddit's logged-out feeds, the default), arcticshift (a third-party archive with grey legal footing,
    # so each user opts in; kb/platforms.md) or auto (the feeds until Reddit ends them, then Arctic Shift).
    # settle_hours: Arctic Shift windows end this long ago, so scores and comment counts have settled.
    # thread_reader: same (threads follow `reader`) or fetchwright (a separate plugin that reads a public thread through
    # Gemini's URL context; needs the user's own Gemini key, so it is opt-in; kb/platforms.md, conduct rule 17)
    "reddit": {"reader": "rss", "settle_hours": 36, "max_pages": 10, "thread_reader": "same"},
    # fetchwright's CLI: cli is a path to fetchwright.py (else $FETCHWRIGHT_CLI, else the installed plugin);
    # max_comments > 0 asks for at most that many comments (a 183-comment thread overran the model's answer uncapped
    # and read at 100 on 2026-10-16); 0 lets fetchwright ask for all. max_reads_per_scan caps the fresh reads `thread` and
    # `new-note` make for a beat between two fetches (the free tier allows 20 a day on gemini-3.8-flash); 0 = no cap
    "fetchwright": {"cli": "", "timeout_seconds": 400, "models": "", "max_comments": 100, "max_reads_per_scan": 10},
    "engage": {
        "min_gap_minutes": 60,
        "max_per_day": 4,
        "per_community_hours": 24,
        "max_item_age_days": 3,
        "min_item_age_hours": 1,
        "confirm": True,
        "platforms": {},
    },
    "retention_hours": 48,
}

STANCES = ("native", "open", "mixed", "hostile", "anti", "n/a", "unknown")
KINDS = ("reddit", "rss", "youtube", "github", "hn", "news", "arxiv", "mastodon", "bluesky", "lemmy", "discourse", "huggingface", "web")
NOTE_KINDS = ("showcase", "workflow", "discussion", "release", "question", "postmortem", "analysis", "data", "news", "paper", "web", "book")
DEFAULT_SECTIONS = ["What it is", "How it was made", "Reception and interest", "Why it matters", "Questions this raises"]
ASKED_WORDS = ("how did you make", "how did you do", "what did you use", "what tools", "which tools", "what software",
               "workflow", "what's your process", "whats your process", "your setup", "what setup", "how long did",
               "what model", "which model", "what data", "where is the data", "source for", "what gear", "which daw",
               "what synth", "how was this made", "made with")


# ---------------------------------------------------------------- basics

def note(msg):
    print(msg, file=sys.stderr)


def fail(msg, code=1):
    print("everscout: " + msg, file=sys.stderr)
    sys.exit(code)


def now_utc():
    return dt.datetime.now(UTC)


def today():
    return now_utc().strftime("%Y-%m-%d")


def iso(ts):
    return S.iso(ts)


def slugify(text, n=48, whole=False):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    if whole and len(s) > n and s[n] != "-" and "-" in s[:n]:
        return s[:n].rsplit("-", 1)[0]  # cut at a word, not mid-word
    return s[:n].rstrip("-") or "untitled"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def append(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(text)


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def expand(p):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(p)))


# ---------------------------------------------------------------- config and paths

def home():
    return expand(os.environ.get("EVERSCOUT_HOME") or "~/.everscout")


def config():
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    h = home()
    for k in ("data_root", "local_root", "voice"):
        cfg[k] = cfg[k].replace("~/.everscout", h)
    cfg["beat_dirs"] = [d.replace("~/.everscout", h) for d in cfg["beat_dirs"]]
    user = load_json(os.path.join(h, "config.json"), {})
    for k, v in user.items():
        if isinstance(v, dict) and isinstance(cfg.get(k), dict):
            for kk, vv in v.items():
                if isinstance(vv, dict) and isinstance(cfg[k].get(kk), dict):
                    cfg[k][kk].update(vv)
                else:
                    cfg[k][kk] = vv
        else:
            cfg[k] = v
    for env, key in (("EVERSCOUT_DATA", "data_root"), ("EVERSCOUT_LOCAL", "local_root")):
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    return cfg


def local_root(cfg):
    return expand(cfg["local_root"])


def data_dir(cfg, slug):
    b = (cfg.get("beats") or {}).get(slug) or {}
    return expand(b.get("data") or os.path.join(cfg["data_root"], slug))


def ledger_dir(cfg):
    return expand(cfg.get("ledger") or os.path.join(cfg["data_root"], "_engage"))


def ledger_path(cfg):
    return os.path.join(ledger_dir(cfg), "engagements.jsonl")


def state_path(cfg, slug):
    return os.path.join(local_root(cfg), f"state-{slug}.json")


def items_path(cfg, slug):
    return os.path.join(local_root(cfg), "cache", f"items-{slug}.json")


def user_agent(cfg):
    contact = cfg.get("contact") or "no contact set"
    return f"everscout/{VERSION} (+https://github.com/m4bwav/everscout; {contact})"


def reddit_user_agent(cfg):
    plat = "windows" if sys.platform.startswith("win") else ("macos" if sys.platform == "darwin" else "linux")
    who = cfg.get("reddit_user") or "unknown"
    return f"{plat}:everscout:v{VERSION} (by /u/{who})"


def fetcher(cfg):
    return S.Fetcher(local_root(cfg), user_agent(cfg), reddit_user_agent(cfg),
                     host_gaps=(cfg.get("pace") or {}).get("hosts"), log=note)


REDDIT_RSS_END = dt.date(2026, 11, 13)  # Reddit's logged-out feeds stop answering (kb/platforms.md)


def reddit_reader(cfg):
    """'rss' (Reddit's logged-out feeds) or 'arcticshift' (the third-party archive); auto switches when the feeds end."""
    r = str((cfg.get("reddit") or {}).get("reader") or "rss").lower()
    if r == "auto":
        return "arcticshift" if dt.datetime.now(UTC).date() >= REDDIT_RSS_END else "rss"
    if r not in ("rss", "arcticshift"):
        fail(f"reddit reader {r!r} unknown (auto, rss, arcticshift)")
    return r


def set_reddit_reader(cfg, a):
    if getattr(a, "reddit_reader", None):
        cfg.setdefault("reddit", {})["reader"] = a.reddit_reader
    set_thread_reader(cfg, a)
    return reddit_reader(cfg)


# ---------------------------------------------------------------- Reddit threads through fetchwright (opt-in)
# fetchwright is a separate plugin: everscout runs its CLI as a subprocess and never imports its code, so everscout
# stays keyless and standard-library (ai-docs/decisions/2026-10-15-thread-reader-fetchwright.md).

THREAD_READERS = ("same", "fetchwright")
GEMINI_HOST = "generativelanguage.googleapis.com"  # the pace and cool-down key for fetchwright reads
FETCHWRIGHT_MIN_GAP = 5


class ReaderStop(Exception):
    """A thread reader that must not be called again this run. code: 2 not installed, 3 refused or cooling down, 4 key."""

    def __init__(self, msg, code):
        super().__init__(msg)
        self.code = code


def thread_reader(cfg):
    """'same' (Reddit threads follow reddit.reader) or 'fetchwright'."""
    r = str((cfg.get("reddit") or {}).get("thread_reader") or "same").lower()
    if r not in THREAD_READERS:
        fail(f"reddit thread reader {r!r} unknown (same, fetchwright)")
    return r


def set_thread_reader(cfg, a):
    if getattr(a, "thread_reader", None):
        cfg.setdefault("reddit", {})["thread_reader"] = a.thread_reader
    return thread_reader(cfg)


def claude_plugins_dir():
    return os.path.expanduser("~/.claude/plugins")


def _version_key(path):
    v = re.findall(r"[\\/](\d+(?:\.\d+)+)[\\/]", path)
    return tuple(int(x) for x in v[-1].split(".")) if v else ()


def find_fetchwright(cfg):
    """(path to fetchwright.py, None) or (None, why): config fetchwright.cli, then $FETCHWRIGHT_CLI, then the installed plugin."""
    for where, c in (("config fetchwright.cli", (cfg.get("fetchwright") or {}).get("cli") or ""),
                     ("FETCHWRIGHT_CLI", os.environ.get("FETCHWRIGHT_CLI") or "")):
        if c:
            p = expand(c)
            return (p, None) if os.path.isfile(p) else (None, f"{where} points at {p}, which does not exist")
    tail = os.path.join("skills", "fetchwright", "scripts", "fetchwright.py")
    root = claude_plugins_dir()
    cands = sorted(glob.glob(os.path.join(root, "cache", "*", "fetchwright", "*", tail)), key=_version_key, reverse=True)
    cands += glob.glob(os.path.join(root, "marketplaces", "*", tail)) + glob.glob(os.path.join(root, "marketplaces", "*", "fetchwright", tail))
    for c in cands:
        if os.path.isfile(c):
            return c, None
    return None, ("fetchwright is not installed: the fetchwright thread reader needs the fetchwright plugin "
                  "(github.com/m4bwav/fetchwright) and a Gemini key (its fetchwright-setup skill), or set config "
                  "fetchwright.cli or FETCHWRIGHT_CLI to its fetchwright.py; or read threads with --thread-reader same")


def retry_after_seconds(text):
    """Seconds in a quota message's 'retry in 22h3m56s' (or '41.5s'), else 0."""
    m = re.search(r"retry in (?:(\d+)h)?(?:(\d+)m)?(?:(\d+(?:\.\d+)?)s)?", text or "")
    return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(float(m.group(3) or 0)) if m else 0


def fetchwright_cache_path(cfg, url):
    return os.path.join(local_root(cfg), "cache", "fetchwright", hashlib.sha1(url.encode("utf-8")).hexdigest()[:20] + ".json")


def fetchwright_cached(cfg, url):
    """The cached fetchwright record for a URL while younger than thread_ttl_seconds, else None."""
    cached = load_json(fetchwright_cache_path(cfg, url), None)
    if cached and time.time() - cached.get("_fetched_at", 0) < cfg["pace"]["thread_ttl_seconds"]:
        return cached
    return None


FETCHWRIGHT_RUNS = [0]  # fetchwright subprocesses started by this process (the per-scan budget counts them)


def read_fetchwright(cfg, url, force=False, run=subprocess.run):
    """fetchwright's record for one thread URL, from the cache when younger than thread_ttl_seconds; None when the
    thread was not read (exit 1 or 5, a timeout, output that is not JSON). Raises ReaderStop on exits 2, 3 and 4, and
    while a 429's cool-down lasts (never retried within the hour, conduct rule 17)."""
    cp = fetchwright_cache_path(cfg, url)
    cached = None if force else fetchwright_cached(cfg, url)
    if cached:
        return cached
    f = fetcher(cfg)
    cd = f.cooldown(GEMINI_HOST)
    if cd:
        raise ReaderStop(f"fetchwright was rate limited earlier: no fetchwright reads until "
                         f"{iso(dt.datetime.fromtimestamp(cd[0], UTC))[:16]} UTC ({cd[1]}); use --thread-reader same", 3)
    cli, why = find_fetchwright(cfg)
    if not cli:
        raise ReaderStop(why, 2)
    fw = cfg.get("fetchwright") or {}
    argv = [sys.executable, cli, "read", url, "--thread", "--json", "--max-chars", "0"]
    if fw.get("models"):
        argv += ["--models", str(fw["models"])]
    if int(fw.get("max_comments") or 0) > 0:
        argv += ["--max-comments", str(int(fw["max_comments"]))]
    timeout = float(fw.get("timeout_seconds") or 400)
    gap = max(FETCHWRIGHT_MIN_GAP, f.gap_for(GEMINI_HOST))
    f._wait(GEMINI_HOST)
    t0 = time.time()
    FETCHWRIGHT_RUNS[0] += 1
    try:
        r = run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
                env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    except subprocess.TimeoutExpired:
        note(f"fetchwright: no answer in {timeout:.0f} s, not read: {url}")
        return None
    finally:
        f._mark(GEMINI_HOST, gap)
    secs = round(time.time() - t0, 1)
    last = ((r.stderr or "").strip().splitlines() or [""])[-1][:300]
    if r.returncode == 3:
        # a daily quota says how long ("Please retry in 22h3m56s"): wait that long, never less than an hour
        wait = f.set_cooldown(GEMINI_HOST, "fetchwright exit 3: " + last, base=max(3600, retry_after_seconds(r.stderr)))
        raise ReaderStop(f"fetchwright was rate limited (exit 3): no fetchwright reads for {wait // 60:.0f} min, "
                         f"so stop this scan's fetchwright reads (conduct rule 17). {last}", 3)
    if r.returncode == 4:
        raise ReaderStop(f"fetchwright has no working Gemini key (exit 4): run the fetchwright-setup skill. {last}", 4)
    if r.returncode == 2:
        raise ReaderStop(f"fetchwright refused the arguments (exit 2; an older or newer fetchwright?): {last}", 2)
    try:
        data = json.loads(r.stdout or "")
    except ValueError:
        data = None
    if r.returncode == 5 or not isinstance(data, dict) or not data.get("read_ok"):
        why = "every Gemini model was unavailable" if r.returncode == 5 else ((data or {}).get("why_not") if isinstance(data, dict) else "") or last or f"exit {r.returncode}"
        note(f"fetchwright: not read ({why}): {url}")
        return None
    f.clear_cooldown(GEMINI_HOST)
    data["_fetched_at"], data["_seconds"] = time.time(), secs
    save_json(cp, data)
    return data


def thread_from_fetchwright(url, pid, r):
    """everscout's thread shape from a fetchwright record. fetchwright returns no handles, dates or scores."""
    m = re.search(r"/r/([^/]+)/", url)
    sub = m.group(1) if m else ""
    clean = re.sub(r"^https?://(old\.|new\.|np\.)?reddit\.com", "https://www.reddit.com", url.split("?")[0].split("#")[0])
    post = {"id": f"reddit:{pid}", "platform": "reddit", "kind": "post", "title": r.get("title") or "", "author": "",
            "url": clean, "published": "", "text": r.get("body") or "", "media": [], "community": sub, "via": "fetchwright"}
    comments = [{"id": f"reddit:{pid}:fw{i}", "platform": "reddit", "kind": "comment", "author": "", "published": "",
                 "text": c.get("text") or "", "is_op": bool(c.get("author_is_op")), "via": "fetchwright"}
                for i, c in enumerate(r.get("comments") or []) if (c.get("text") or "").strip()]
    meta = {"model": r.get("model"), "retrieval": r.get("retrieval") or [], "usage": r.get("usage") or {},
            "dropped": r.get("dropped") or {}, "body_removed": bool(r.get("body_removed")), "style": r.get("style"),
            "version": r.get("fetchwright"), "seconds": r.get("_seconds")}
    return post, comments, meta


def arctic_window(f, sub, after_ts, before_ts, max_pages=10, ttl=3600, force=False, query=None):
    """Every post of one subreddit created in [after_ts, before_ts), paging back 100 at a time (newest first).
    Returns (items, pages, missing): missing is None, or why the window's oldest posts are not there (pages ran out,
    or a later page failed; the archive answered 422 to a deep page on 2026-10-15). A failed first page raises."""
    seen, items, before, pages = set(), [], int(before_ts), 0
    while pages < max_pages:
        url = S.arctic_posts_url(sub, after_ts, before, query=query)
        try:
            data, _, status = f.get_json(url, ttl=ttl, force=force)
            if S.arctic_error(data):
                raise S.FetchError(url, status, S.arctic_error(data))
        except S.FetchError as e:
            if not pages:
                raise
            return items, pages, f"page {pages + 1} failed ({e.code})"
        rows = (data or {}).get("data") or []
        pages += 1
        for it in S.parse_arctic_posts(data, url):
            if it["id"] not in seen:
                seen.add(it["id"])
                items.append(it)
        if len(rows) < 100:
            return items, pages, None
        oldest = min(int(p.get("created_utc") or before) for p in rows)
        if oldest + 1 >= before:  # a whole page in one second; give up rather than loop
            return items, pages, "a page of posts in one second"
        before = oldest + 1  # the boundary second again; repeats drop out by id
    return items, pages, f"stopped after {pages} pages of 100 (raise reddit.max_pages)"


# ---------------------------------------------------------------- markdown helpers

def parse_frontmatter(text):
    """Flat YAML-ish frontmatter: `key: value` and `key: [a, b]`. Returns (dict, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm, body = text[3:end], text[end + 4:].lstrip("\n")
    out = {}
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        v = re.sub(r"\s+#.*$", "", v) if not v.startswith(("'", '"')) else v
        if v.startswith("[") and v.endswith("]"):
            out[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
        elif v.lower() in ("true", "false"):
            out[k] = v.lower() == "true"
        elif re.fullmatch(r"-?\d+", v):
            out[k] = int(v)
        else:
            out[k] = v.strip("'\"")
    return out, body


def fm_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(str(x) for x in v) + "]"
    s = str(v).replace("\n", " ")
    return s


def render_frontmatter(d):
    return "---\n" + "".join(f"{k}: {fm_value(v)}\n" for k, v in d.items()) + "---\n"


def parse_table(text):
    """Rows of the first markdown table in text, as dicts keyed by the lower-cased header."""
    rows, header = [], None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            if header and rows:
                break
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower().replace(" ", "_") for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


# ---------------------------------------------------------------- beats

def beat_dirs(cfg):
    # EVERSCOUT_BEATS (os.pathsep-separated) goes first, so a worktree's beats shadow the configured clone's
    dirs = [expand(d) for d in (os.environ.get("EVERSCOUT_BEATS") or "").split(os.pathsep) if d.strip()]
    missing = [d for d in dirs if not os.path.isdir(d)]
    if missing:  # a typo or a worktree not made yet would silently edit the configured clone instead
        fail("EVERSCOUT_BEATS names a missing folder: " + ", ".join(missing))
    dirs += [expand(d) for d in cfg.get("beat_dirs") or []]
    dirs.append(os.path.join(ROOT, "beats"))
    return dirs


def all_beats(cfg):
    found = {}
    for d in beat_dirs(cfg):
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if name.startswith(("_", ".")) or not os.path.isfile(os.path.join(p, "beat.md")):
                continue
            found.setdefault(name, p)  # first dir wins: private beats shadow built-in ones
    return found


class Beat:
    def __init__(self, slug, path):
        self.slug, self.path = slug, path
        self.meta, self.body = parse_frontmatter(read(os.path.join(path, "beat.md")))

    def file(self, name):
        return os.path.join(self.path, name)

    def text(self, name):
        p = self.file(name)
        return read(p) if os.path.exists(p) else ""

    @property
    def title(self):
        return self.meta.get("title") or self.slug

    def sources(self, cfg=None):
        rows = []
        for r in parse_table(self.text("sources.md")):
            src = r.get("source", "").strip().strip("`")
            if not src:
                continue
            r["source"] = src
            r["kind"] = (r.get("kind") or "rss").strip().lower()
            r["stance"] = (r.get("stance") or "unknown").split()[0].lower()
            r["engage_ok"] = (r.get("engage") or "no").lower().startswith("yes")
            r["scan_ok"] = not (r.get("scan") or "yes").lower().startswith("no")
            rows.append(r)
        return rows

    def vocab(self):
        """{facet: {canonical: [aliases]}} from `## facet` headings and `- canonical: alias, alias` lines."""
        out, facet = {}, None
        for line in self.text("vocab.md").splitlines():
            if line.startswith("## "):
                name = line[3:].strip().lower()
                facet = None if name in ("how to use this file", "sources", "notes") else slugify(name).replace("-", "_")
                if facet:
                    out.setdefault(facet, {})
                continue
            m = re.match(r"^- `?([a-z0-9][a-z0-9.+_-]*)`?\s*(?::\s*(.*))?$", line.strip())
            if facet and m:
                aliases = [a.strip() for a in (m.group(2) or "").split(",") if a.strip()]
                out[facet][m.group(1)] = aliases
        return out

    def facets(self):
        return list(self.vocab().keys())

    def questions(self):
        out, cat = [], "general"
        for line in self.text("questions.md").splitlines():
            if line.startswith("## "):
                cat = line[3:].strip().lower()
                continue
            m = re.match(r"^- (?:\[([^\]]*)\]\s*)?(.+)$", line)
            if m and cat not in ("how to use this file", "sources"):
                tags = [t.strip().lower() for t in (m.group(1) or "").split(",") if t.strip()]
                out.append({"category": cat, "tags": tags, "text": m.group(2).strip()})
        return out

    def searches(self):
        return parse_table(self.text("searches.md"))

    def list_meta(self, key, default=()):
        v = self.meta.get(key)
        if isinstance(v, list):
            return v
        if isinstance(v, str) and v:
            return [x.strip() for x in v.split(",") if x.strip()]
        return list(default)

    def sections(self):
        return self.list_meta("note_sections", DEFAULT_SECTIONS)


def get_beat(cfg, slug):
    beats = all_beats(cfg)
    if not slug:
        if len(beats) == 1:
            slug = next(iter(beats))
        else:
            fail("which beat? pass --beat (known: " + ", ".join(beats) + ")")
    if slug not in beats:
        fail(f"no beat named {slug!r} (known: {', '.join(beats) or 'none'}); create one with `beat-new`")
    return Beat(slug, beats[slug])


# ---------------------------------------------------------------- source rows to fetch URLs

def feed_urls(row, listings=("new",), t="week", since_days=3):
    """[(url, listing, parser)] for one watch-list row. parser is 'reddit', 'feed', 'hn' or None (not fetchable)."""
    k, s = row["kind"], row["source"]
    if k == "reddit":
        return [(S.reddit_listing_url(s, l, t), l, "reddit") for l in listings]
    if k == "rss":
        return [(s, "new", "feed")]
    if k == "youtube":
        return [(S.youtube_channel_feed(s), "new", "feed")]
    if k == "github":
        return [(S.github_releases_feed(s), "new", "feed")]
    if k == "news":
        return [(S.google_news_feed(s), "new", "feed")]
    if k == "arxiv":
        return [(S.arxiv_query_feed(s), "new", "feed")]
    if k == "hn":
        since = (int(time.time()) // 3600) * 3600 - since_days * 86400  # hour-aligned so the URL, and the cache, hold for an hour
        return [(S.hn_search_url(s, since_ts=since), "new", "hn")]
    if k == "mastodon":
        m = re.fullmatch(r"#([\w]+)@([\w.-]+)", s) or re.fullmatch(r"@([\w.]+)@([\w.-]+)", s)
        if not m:
            return []
        if s.startswith("#"):
            return [(f"https://{m.group(2)}/tags/{m.group(1)}.rss", "new", "feed")]
        return [(f"https://{m.group(2)}/@{m.group(1)}.rss", "new", "feed")]
    if k == "bluesky":
        if s.startswith("at://") and "/app.bsky.feed.generator/" in s:
            return [(S.bsky_feed_url(s), "new", "bsky")]
        h = s.lstrip("@")
        return [(f"https://bsky.app/profile/{h}/rss", "new", "feed")]
    if k == "huggingface":
        return [(S.huggingface_url(s), "new", "hf")]
    if k == "lemmy":
        m = re.fullmatch(r"(?:c/|!)?([\w]+)@([\w.-]+)", s)
        return [(f"https://{m.group(2)}/feeds/c/{m.group(1)}.xml?sort=New", "new", "feed")] if m else []
    if k == "discourse":
        base = s.rstrip("/")
        return [(base + ("/latest.rss" if "/c/" not in base else ".rss"), "new", "feed")]
    return []


def compile_filter(spec):
    """F5Bot-style filter: `+term` required, `-term` excluded, bare terms any-of; quoted phrases allowed."""
    req, exc, anyof = [], [], []
    for m in re.finditer(r'([+-]?)"([^"]+)"|([+-]?)(\S+)', spec or ""):
        sign = m.group(1) or m.group(3) or ""
        term = (m.group(2) or m.group(4) or "").lower()
        if not term:
            continue
        (req if sign == "+" else exc if sign == "-" else anyof).append(term)
    return req, exc, anyof


def term_in(term, low):
    return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", low) is not None


def passes(item, spec="", mute=()):
    low = (item.get("title", "") + " " + item.get("text", "")).lower()
    if any(term_in(m.lower(), low) for m in mute):
        return False
    req, exc, anyof = compile_filter(spec)
    if any(term_in(t, low) for t in exc):
        return False
    if any(not term_in(t, low) for t in req):
        return False
    return not anyof or any(term_in(t, low) for t in anyof)


def parse_with(parser, text, url, row):
    if parser == "reddit":
        return S.parse_reddit(text, url)
    if parser == "hn":
        return S.parse_hn_hits(json.loads(text) if text.strip() else {}, url)
    if parser == "bsky":
        return S.parse_bsky_feed(json.loads(text) if text.strip() else {}, url)
    if parser == "hf":
        return S.parse_huggingface(json.loads(text) if text.strip() else [], url)
    if parser == "arctic":
        return S.parse_arctic_posts(json.loads(text) if text.strip() else {}, url)
    return S.parse_feed(text, url, platform=row["kind"])


# ---------------------------------------------------------------- commands: setup and inspection

def cmd_where(a):
    cfg = config()
    print(f"everscout {VERSION}")
    print(f"HOME    {home()}  (config.json {'present' if os.path.exists(os.path.join(home(), 'config.json')) else 'absent: defaults'})")
    print(f"LOCAL   {local_root(cfg)}")
    print(f"LEDGER  {ledger_dir(cfg)}")
    print(f"VOICE   {expand(cfg['voice'])} ({'present' if os.path.exists(expand(cfg['voice'])) else 'absent: kb/voice-template.md applies'})")
    for d in beat_dirs(cfg):
        print(f"BEATS   {d}{'' if os.path.isdir(d) else ' (missing)'}")
    if a.beat:
        b = get_beat(cfg, a.beat)
        print(f"BEAT    {b.slug} = {b.path}")
        print(f"DATA    {data_dir(cfg, b.slug)}")


def cmd_beats(a):
    cfg = config()
    beats = all_beats(cfg)
    if a.json:
        print(json.dumps({k: {"path": v, "data": data_dir(cfg, k)} for k, v in beats.items()}, indent=1))
        return
    if not beats:
        print("no beats; create one with `everscout.py beat-new <slug> --title \"...\"`")
    for slug, path in beats.items():
        b = Beat(slug, path)
        rows = b.sources()
        st = load_json(state_path(cfg, slug), {})
        builtin = os.path.normcase(os.path.abspath(path)).startswith(os.path.normcase(os.path.join(ROOT, "beats")))
        print(f"{slug:<22} {b.meta.get('status', 'active'):<8} {len(rows):>3} sources ({sum(r['engage_ok'] for r in rows)} engage) "
              f"{'built-in' if builtin else 'private '} last fetch {st.get('last_fetch', 'never')[:16]}  {b.title}")


def seed_beat_md(text, scope, questions, feeds):
    """Fill a fresh beat.md from a caller's scope (an evergreen unit offering a beat, for one)."""
    if scope:
        text = re.sub(r"^One paragraph: .*$", lambda _: scope.strip(), text, count=1, flags=re.M)
    if questions:
        block = "\n".join(f"{i}. {q.strip()}" for i, q in enumerate(questions, 1))
        text = re.sub(r"^1\. TODO\n2\. TODO\n3\. TODO$", lambda _: block, text, count=1, flags=re.M)
    if feeds:
        text = text.replace("\n---\n", f"\nfeeds: [{feeds}]\n---\n", 1)
    return text


def cmd_beat_new(a):
    cfg = config()
    slug = slugify(a.slug)
    target_root = expand(a.dir) if a.dir else expand((cfg.get("beat_dirs") or [os.path.join(home(), "beats")])[0])
    dest = os.path.join(target_root, slug)
    if os.path.exists(dest):
        fail(f"{dest} exists")
    tpl = os.path.join(ROOT, "beats", "_template")
    shutil.copytree(tpl, dest)
    for name in os.listdir(dest):
        p = os.path.join(dest, name)
        t = read(p).replace("{{SLUG}}", slug).replace("{{TITLE}}", a.title or slug).replace("{{DATE}}", today())
        if name == "beat.md":
            t = seed_beat_md(t, a.scope, a.question or [], a.feeds)
        write(p, t)
    print(dest)
    print("next: fill beat.md (scope), then sources.md, vocab.md, questions.md, searches.md, study.md; "
          "then `everscout.py beat-check " + slug + "` and `probe --beat " + slug + "`")


def cmd_beat_check(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    errs, warns = [], []
    for f in ("beat.md", "sources.md", "vocab.md", "questions.md", "searches.md", "study.md"):
        if not os.path.exists(b.file(f)):
            (errs if f in ("beat.md", "sources.md", "vocab.md") else warns).append(f"missing {f}")
    for k in ("title", "status", "verified"):
        if k not in b.meta:
            errs.append(f"beat.md frontmatter lacks {k}")
    rows = b.sources()
    if not rows:
        errs.append("sources.md has no table rows")
    seen = set()
    for r in rows:
        key = (r["kind"], r["source"].lower())
        if key in seen:
            errs.append(f"duplicate source {r['kind']} {r['source']}")
        seen.add(key)
        if r["kind"] not in KINDS:
            errs.append(f"{r['source']}: unknown kind {r['kind']!r} (one of {', '.join(KINDS)})")
        if r["stance"] not in STANCES:
            errs.append(f"{r['source']}: stance {r['stance']!r} not in {', '.join(STANCES)}")
        if r["kind"] != "web" and r["scan_ok"] and not feed_urls(r):
            errs.append(f"{r['source']}: cannot build a feed URL for kind {r['kind']}")
        if r["engage_ok"] and r["stance"] in ("anti", "n/a"):
            errs.append(f"{r['source']}: engage yes with stance {r['stance']}")
        if not re.search(r"[✓~?]", r.get("notes", "") + r.get("stance", "")):
            warns.append(f"{r['source']}: no verification marker (✓ date, ~ or ?)")
    voc = b.vocab()
    if not voc:
        errs.append("vocab.md has no facets (## headings with - canonical: aliases lines)")
    reserved = {"title", "kind", "status", "date", "verified", "beat", "platform", "community", "url", "posted", "note_kind",
                "interest", "top", "engaged", "tags", "summary"}
    canon_seen = {}
    for facet, ents in voc.items():
        if facet in reserved:
            errs.append(f"vocab facet {facet!r} collides with a note field")
        if not ents:
            warns.append(f"vocab facet {facet} is empty")
        for c in ents:
            if c in canon_seen:
                warns.append(f"{c} is in both {canon_seen[c]} and {facet}")
            canon_seen[c] = facet
    qs = b.questions()
    if len(qs) < 10:
        warns.append(f"questions.md has {len(qs)} seeds (aim for 15 to 40)")
    if len({q['category'] for q in qs}) < 3 and qs:
        warns.append("questions.md has fewer than three categories")
    if not b.searches():
        warns.append("searches.md has no table rows")
    metrics = load_metrics(b) if os.path.exists(b.file("metrics.md")) else []
    if metrics:
        me, mw = metric_problems(b, metrics)
        errs += me
        warns += mw
    if os.path.exists(lit_path(b)) and "{{" not in b.text("literature.md"):
        le, lw = lit_problems(b, *lit_load(b))
        errs += ["literature.md: " + e for e in le]
        warns += ["literature.md: " + w for w in lw]
    for e in errs:
        print("ERROR  " + e)
    for w in warns:
        print("warn   " + w)
    print(f"{b.slug}: {len(rows)} sources, {sum(len(v) for v in voc.values())} entities in {len(voc)} facets, "
          f"{len(qs)} question seeds, {len(b.searches())} searches, {len(metrics)} metrics; {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs or (a.strict and warns) else 0)


def cmd_sources(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    rows = b.sources()
    if a.json:
        print(json.dumps(rows, indent=1, ensure_ascii=False))
        return
    for r in rows:
        urls = [u for u, _, _ in feed_urls(r)]
        print(f"{r['kind']:<9} {r['source'][:44]:<44} {r['stance']:<8} engage {'yes' if r['engage_ok'] else 'no ':<3} "
              f"scan {'yes' if r['scan_ok'] else 'no ':<3} {urls[0] if urls else '(search only)'}")


def cmd_probe(a):
    """Fetch each source once (cache respected unless --force) and report whether it answers with a parseable feed."""
    cfg = config()
    reader = set_reddit_reader(cfg, a)
    b = get_beat(cfg, a.beat)
    f = fetcher(cfg)
    rows = [r for r in b.sources() if (not a.source or a.source.lower() in r["source"].lower())]
    if a.kinds:
        rows = [r for r in rows if r["kind"] in a.kinds.split(",")]
    bad = 0
    results = []
    # Reddit first, ten subreddits per multireddit request: a subreddit that shows up in the shared window is alive;
    # only the ones that do not show up are probed alone (renamed, banned, private, or just quiet)
    done = set()
    reddit_rows = [r for r in rows if r["kind"] == "reddit"] if reader == "rss" else []
    for i in range(0, len(reddit_rows), 10):
        batch = reddit_rows[i:i + 10]
        if len(batch) < 2:
            break
        url = S.reddit_multi_url([r["source"] for r in batch])
        try:
            text, cached, status = f.get(url, ttl=cfg["pace"]["feed_ttl_seconds"], force=a.force)
            items = S.parse_reddit(text, url) if text else []
        except (S.FetchError, ValueError) as e:
            note(f"multireddit probe failed ({e}); probing one by one")
            continue
        for r in batch:
            name = re.sub(r"^r/", "", r["source"]).lower()
            mine = [it for it in items if it["kind"] == "post" and (it.get("community") or "").lower() == name]
            if not mine:
                continue
            newest = max((it["published"] for it in mine if it.get("published")), default="")
            results.append({"source": r["source"], "kind": "reddit", "status": status, "items": len(mine), "newest": newest,
                            "ok": True, "url": url, "via": "multireddit"})
            print(f"ok  {status} {len(mine):>3} items newest {newest[:10] or '-':<10} {'cache ' if cached else 'multi '}reddit    {r['source']}")
            done.add(id(r))
    for r in rows:
        if id(r) in done:
            continue
        urls = feed_urls(r, since_days=30)
        if r["kind"] == "reddit" and reader == "arcticshift":
            end = (int(time.time()) // 3600) * 3600
            urls = [(S.arctic_posts_url(r["source"], end - 30 * 86400, end, limit=5), "new", "arctic")]
        for url, listing, parser in urls[:1]:
            try:
                text, cached, status = f.get(url, ttl=cfg["pace"]["feed_ttl_seconds"], force=a.force)
                items = parse_with(parser, text, url, r) if text else []
                newest = max((i["published"] for i in items if i.get("published")), default="")
                ok = status == 200 and bool(items)
                results.append({"source": r["source"], "kind": r["kind"], "status": status, "items": len(items),
                                "newest": newest, "ok": ok, "url": url})
                print(f"{'ok ' if ok else 'BAD'} {status} {len(items):>3} items newest {newest[:10] or '-':<10} "
                      f"{'cache ' if cached else 'fetch '}{r['kind']:<9} {r['source']}")
                bad += not ok
            except (S.FetchError, ValueError) as e:
                bad += 1
                results.append({"source": r["source"], "kind": r["kind"], "ok": False, "error": str(e), "url": url})
                print(f"BAD {r['kind']:<9} {r['source']}: {e}")
    if a.save:
        dd = data_dir(cfg, b.slug)
        p = os.path.join(dd, "sources", f"probe-{today()}.json")
        merged = {(r.get("kind"), r.get("source")): r for r in load_json(p, [])}  # a partial probe updates its rows only
        merged.update({(r.get("kind"), r.get("source")): r for r in results})
        current = {(r["kind"], r["source"]) for r in b.sources()}
        save_json(p, [r for k, r in merged.items() if k in current])
        print(f"saved {p}")
    print(f"{len(rows)} sources probed, {bad} bad")
    sys.exit(2 if bad else 0)


# ---------------------------------------------------------------- commands: fetch, thread, search

def cmd_fetch(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    f = fetcher(cfg)
    rows = [r for r in b.sources() if r["scan_ok"] and r["kind"] != "web"]
    if a.sources:
        want = [s.strip().lower() for s in a.sources.split(",")]
        rows = [r for r in rows if any(w in r["source"].lower() for w in want)]
    if a.kinds:
        rows = [r for r in rows if r["kind"] in a.kinds.split(",")]
    listings = tuple(a.listing.split(","))
    st = load_json(state_path(cfg, b.slug), {"seen": {}, "fetches": []})
    seen = st.setdefault("seen", {})
    cutoff = now_utc() - dt.timedelta(days=a.max_age_days)
    mute = b.list_meta("mute_words")
    rates = st.setdefault("rates", {})
    new, allitems, errors, muted = [], [], 0, 0
    ttl = cfg["pace"]["feed_ttl_seconds"]

    def get_items(url, parser, row, label):
        nonlocal errors
        try:
            text, _, status = f.get(url, ttl=ttl, force=a.force)
            if not text:
                note(f"{label}: no feed ({status})")
                return None
            return parse_with(parser, text, url, row)
        except (S.FetchError, ValueError) as e:
            errors += 1
            note(f"{label}: {e}")
            return None

    # jobs: (items, {community lower: row} or a single row, listing)
    jobs = []
    reader = set_reddit_reader(cfg, a)
    as_cutoff = cutoff
    if reader == "arcticshift":
        # one window per subreddit that ends settle_hours ago (scores settled), as long as --max-age-days, so weekly
        # scans with --max-age-days 7 tile without gaps; the top listing is not needed (items carry their scores)
        rc = cfg.get("reddit") or {}
        settle = a.settle_hours if a.settle_hours is not None else float(rc.get("settle_hours", 36))
        end = (int(time.time()) // 3600) * 3600 - int(settle * 3600)  # hour-aligned so the URLs, and the cache, hold
        start = end - int(a.max_age_days * 86400)
        as_cutoff = dt.datetime.fromtimestamp(start, UTC)
        note(f"reddit via Arctic Shift: posts from {iso(as_cutoff)[:16]} to {iso(dt.datetime.fromtimestamp(end, UTC))[:16]} UTC "
             f"(scores settle after about {settle:g} h)")
        for r in [r for r in rows if r["kind"] == "reddit"]:
            try:
                items, pages, missing = arctic_window(f, r["source"], start, end, max_pages=int(rc.get("max_pages", 10)),
                                                      ttl=ttl, force=a.force)
            except S.FetchError as e:
                errors += 1
                note(f"reddit {r['source']} (arcticshift): {e}")
                continue
            if missing:
                note(f"reddit {r['source']}: {len(items)} posts kept, but {missing}: the window's oldest posts are missing")
            jobs.append((items, r, "new"))
    reddit_new = [r for r in rows if r["kind"] == "reddit" and "new" in listings and reader == "rss"]
    if reddit_new and dt.datetime.now(UTC).date() >= REDDIT_RSS_END:
        note("Reddit ended its logged-out feeds on 2026-11-13: set reddit.reader to arcticshift or auto in config.json "
             "to read Reddit through the Arctic Shift archive (kb/platforms.md), or rely on captures")
    for batch in plan_reddit_batches(reddit_new, rates, a.max_age_days, cfg):
        if len(batch) == 1:
            r = batch[0]
            url = S.reddit_listing_url(r["source"], "new") + "?limit=100"
            items = get_items(url, "reddit", r, f"reddit {r['source']}")
            if items is not None:
                learn_rate(rates, r["source"], items)
                jobs.append((items, r, "new"))
            continue
        url = S.reddit_multi_url([r["source"] for r in batch])
        items = get_items(url, "reddit", batch[0], "reddit " + "+".join(r["source"] for r in batch))
        if items is None:
            continue
        posts = [i for i in items if i["kind"] == "post"]
        oldest = min((S.parse_time(i.get("published")) for i in posts if S.parse_time(i.get("published"))), default=None)
        if len(posts) >= 95 and oldest and oldest > cutoff:
            # the shared window filled before reaching the cutoff: a busy subreddit crowded the others out
            note(f"multireddit window full ({len(posts)} posts back to {iso(oldest)[:16]}); fetching {len(batch)} subreddits one by one")
            for r in batch:
                rates[r["source"].lower()] = max(rates.get(r["source"].lower(), 0), 100 / max(0.5, a.max_age_days))
                one = get_items(S.reddit_listing_url(r["source"], "new") + "?limit=100", "reddit", r, f"reddit {r['source']}")
                if one is not None:
                    learn_rate(rates, r["source"], one)
                    jobs.append((one, r, "new"))
            continue
        for r in batch:
            learn_rate(rates, r["source"], [i for i in posts if (i.get("community") or "").lower() == re.sub(r"^r/", "", r["source"]).lower()],
                       window_days=max(0.5, (now_utc() - oldest).total_seconds() / 86400) if oldest else a.max_age_days)
        jobs.append((items, {re.sub(r"^r/", "", r["source"]).lower(): r for r in batch}, "new"))
    yt_tried = yt_failed = 0
    for r in rows:
        for url, listing, parser in feed_urls(r, listings if r["kind"] == "reddit" else ("new",), a.t, a.max_age_days):
            if r["kind"] == "reddit" and (listing == "new" or reader != "rss"):
                continue  # planned above
            items = get_items(url, parser, r, f"{r['kind']} {r['source']}")
            if r["kind"] == "youtube":
                yt_tried += 1
                yt_failed += items is None
            if items is not None:
                jobs.append((items, r, listing))
    if yt_tried > 1 and yt_failed == yt_tried:
        # YouTube's feed server has 404ed for every channel at once, on and off, since December 2025 (kb/platforms.md)
        note(f"youtube: all {yt_tried} channel feeds failed at once, so the endpoint is down, not the channel ids; "
             "fetch again later (the 404s are cached for the feed ttl) before changing sources.md")
    for items, target, listing in jobs:
        for it in items:
            if it["kind"] != "post":
                continue
            if isinstance(target, dict) and "source" not in target:
                r = target.get((it.get("community") or "").lower())
                if r is None:
                    continue
            else:
                r = target
            if not passes(it, r.get("filter", ""), mute):
                muted += 1
                continue
            it["source"] = r["source"]
            it["source_kind"] = r["kind"]
            it["stance"] = r["stance"]
            it["engage_ok"] = r["engage_ok"]
            # the watch-list row is the community (a feed's <category> is a post's own tag, not where it lives);
            # only Reddit items carry their subreddit reliably, and search rows may span several
            if r["kind"] != "reddit" or not it.get("community"):
                it["community"] = r["source"]
            it["listing"] = listing
            it["top"] = listing == "top"
            pub = S.parse_time(it.get("published"))
            it["age_hours"] = round((now_utc() - pub).total_seconds() / 3600, 1) if pub else None
            allitems.append(it)
            if it["id"] not in seen:
                if not a.peek:
                    seen[it["id"]] = {"first_seen": iso(now_utc()), "source": r["source"], "title": it["title"][:120]}
                if pub is None or pub >= (as_cutoff if it.get("via") == "arcticshift" else cutoff):
                    new.append(it)
    # pickup: Reddit threads linked from the other platforms' items (discovery without a listing); a listed Reddit item
    # learns how many of them linked it, which counts toward its importance in triage. Only items inside the fetch window:
    # a feed's old posts would bring back threads months old every time their entries are purged
    picked = pickup_reddit_links(st, [i for i in allitems if (S.parse_time(i.get("published")) or now_utc()) >= cutoff])
    disc = st.get("reddit_seen_elsewhere") or {}
    for it in allitems:
        e = disc.get(it["id"].split(":")[-1]) if it.get("platform") == "reddit" else None
        if e and e.get("mentions"):
            it["elsewhere"] = e["mentions"]
    if picked:
        note(f"pickup: {len(picked)} Reddit threads linked from other sources in this fetch, {len(disc)} kept from the last "
             f"{DISCOVERY_KEEP_DAYS} days; `discover list --beat {b.slug}` ranks the ones to read")
    st["fetchwright_reads"] = 0  # a fetch starts a scan: the per-scan fetchwright budget starts again
    st["fetches"] =(st.get("fetches") or [])[-49:] + [{"at": iso(now_utc()), "sources": len(rows), "fetched": f.fetched,
                                                          "cached": f.cached, "new": len(new), "errors": errors}]
    st["last_fetch"] = iso(now_utc())
    if not a.peek:  # a peek (building a beat, answering a question) must not use up the next scan's new items
        save_json(state_path(cfg, b.slug), st)
    merged = {i["id"]: i for i in load_json(items_path(cfg, b.slug), [])}
    for it in allitems:
        old = merged.get(it["id"], {})
        it["top"] = it["top"] or old.get("top", False)
        merged[it["id"]] = it
    save_json(items_path(cfg, b.slug), list(merged.values()))
    out = allitems if a.all else new
    out.sort(key=lambda i: i.get("published") or "", reverse=True)
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return
    print(f"{b.slug}: {len(rows)} sources, {f.fetched} fetched, {f.cached} from cache, {errors} errors, {muted} filtered out, "
          f"{len(new)} new items under {a.max_age_days}d")
    for i in out[: a.limit]:
        age = f"{i['age_hours']:>6}h" if i.get("age_hours") is not None else "     ?"
        score = f"{i['points']}p {i['comments']}c " if i.get("via") == "arcticshift" else ""
        score += f"linked {i['elsewhere']}x elsewhere " if i.get("elsewhere") else ""
        print(f"{(i.get('published') or '')[:16]:<16} {i['source_kind']:<8} {str(i['community'])[:18]:<18} {age} "
              f"{'M' if i['media'] else ' '} {score}{i['title'][:70]}  {i['url']}")


def learn_rate(rates, sub, posts, window_days=None):
    """Remember a subreddit's posts a day, so the next fetch can pack quiet subreddits into one multireddit request."""
    key = re.sub(r"^r/", "", sub).lower()
    times = sorted(t for t in (S.parse_time(p.get("published")) for p in posts if p.get("kind", "post") == "post") if t)
    if window_days is None:
        if len(times) < 2:
            window_days = 7
        else:
            window_days = max(0.5, (now_utc() - times[0]).total_seconds() / 86400)
    rate = round(len(times) / window_days, 2)
    old = rates.get(key)
    rates[key] = rate if old is None else round(0.5 * old + 0.5 * rate, 2)


def plan_reddit_batches(rows, rates, window_days, cfg):
    """Pack subreddits into multireddit requests whose expected posts over the window fit in one 100-post page.
    Unknown subreddits count as 5 a day; a busy one goes alone. Returns a list of row lists."""
    cap = float((cfg.get("pace") or {}).get("reddit_multi_capacity", 70))
    max_batch = int((cfg.get("pace") or {}).get("reddit_multi_max", 10))
    if max_batch <= 1:
        return [[r] for r in rows]
    def hint(r):  # a watch-list note like "about 42 posts a day" seeds the first plan
        m = re.search(r"about ([\d.]+) (?:posts )?a day", r.get("notes", ""))
        return float(m.group(1)) if m else 5.0
    est = lambda r: rates.get(re.sub(r"^r/", "", r["source"]).lower(), hint(r)) * max(0.5, window_days)
    batches, cur, load = [], [], 0.0
    for r in sorted(rows, key=est):
        e = est(r)
        if e >= cap:
            batches.append([r])
            continue
        if cur and (load + e > cap or len(cur) >= max_batch):
            batches.append(cur)
            cur, load = [], 0.0
        cur.append(r)
        load += e
    if cur:
        batches.append(cur)
    return batches


def platform_of(url):
    """Which thread reader fits a URL. Heuristic for the federated platforms (any host)."""
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    if host.endswith("reddit.com") or host == "redd.it":
        return "reddit"
    if host == "news.ycombinator.com" or url.startswith("hn:"):
        return "hn"
    if host == "bsky.app" or url.startswith("at://"):
        return "bluesky"
    if S.mastodon_thread_parts(url)[0]:
        return "mastodon"
    if S.lemmy_thread_parts(url)[0]:
        return "lemmy"
    if S.discourse_thread_parts(url)[0]:
        return "discourse"
    return "web"


def load_thread(cfg, url, force=False, asked_words=ASKED_WORDS, reader=None):
    """A thread with its comments, or None. reader overrides reddit.thread_reader ('same' where authors and dates
    are needed: fetchwright returns neither). Raises ReaderStop when the fetchwright reader must stop."""
    f = fetcher(cfg)
    plat = platform_of(url)
    hidden, fwmeta = 0, None
    if plat == "reddit" and (reader or thread_reader(cfg)) == "fetchwright":
        m = re.search(r"redd\.it/([a-z0-9]+)", url)
        pid = S.reddit_post_id(url) or (m.group(1) if m else None)
        if not pid:
            return None
        r = read_fetchwright(cfg, url, force=force)
        if not r:
            return None
        post, comments, fwmeta = thread_from_fetchwright(url, pid, r)
    elif plat == "reddit" and reddit_reader(cfg) == "arcticshift":
        m = re.search(r"redd\.it/([a-z0-9]+)", url)
        pid = S.reddit_post_id(url) or (m.group(1) if m else None)
        if not pid:
            return None
        ttl = cfg["pace"]["thread_ttl_seconds"]
        data, _, _ = f.get_json(S.arctic_ids_url([pid]), ttl=ttl, force=force)
        posts = S.parse_arctic_posts(data)
        if not posts:
            return None
        tree, _, _ = f.get_json(S.arctic_tree_url(pid), ttl=ttl, force=force)
        t = S.parse_arctic_tree(tree, posts[0])
        post, comments, hidden = t["post"], t["comments"], t["hidden"]
    elif plat == "reddit":
        turl = S.reddit_thread_url(url)
        text, _, status = f.get(turl, ttl=cfg["pace"]["thread_ttl_seconds"], force=force)
        entries = S.parse_reddit(text, turl) if text else []
        if not entries:
            return None
        post, comments = entries[0], entries[1:]
        post["kind"] = "post"
        for c in comments:
            c["kind"] = "comment"
    else:
        ttl = cfg["pace"]["thread_ttl_seconds"]
        if plat == "hn":
            data, _, _ = f.get_json(f"{S.HN_API}/items/{S.hn_item_id(url)}", ttl=ttl, force=force)
            t = S.parse_hn_item(data)
        elif plat == "bluesky":
            who, rkey = S.bsky_thread_parts(url)
            if not who:
                return None
            if not who.startswith("did:"):
                r, _, _ = f.get_json(S.bsky_resolve_url(who), ttl=86400)
                who = (r or {}).get("did") or who
            data, _, _ = f.get_json(S.bsky_thread_url(who, rkey), ttl=ttl, force=force)
            t = S.parse_bsky_thread(data)
        elif plat == "mastodon":
            host, sid = S.mastodon_thread_parts(url)
            st, _, _ = f.get_json(f"https://{host}/api/v1/statuses/{sid}", ttl=ttl, force=force)
            ctx, _, _ = f.get_json(f"https://{host}/api/v1/statuses/{sid}/context", ttl=ttl, force=force)
            t = S.parse_mastodon_thread(st, ctx, host)
        elif plat == "lemmy":
            host, pid = S.lemmy_thread_parts(url)
            pd, _, _ = f.get_json(f"https://{host}/api/v3/post?id={pid}", ttl=ttl, force=force)
            cd, _, _ = f.get_json(f"https://{host}/api/v3/comment/list?post_id={pid}&limit=50&sort=Old&type_=All", ttl=ttl, force=force)
            t = S.parse_lemmy_thread(pd, cd, host)
        elif plat == "discourse":
            base, tid = S.discourse_thread_parts(url)
            data, _, _ = f.get_json(f"{base}/t/{tid}.json", ttl=ttl, force=force)
            t = S.parse_discourse_topic(data, base)
        else:
            return None
        if not t:
            return None
        post, comments = t["post"], t["comments"]
    for c in comments:
        if "is_op" not in c:  # fetchwright marks the poster's replies itself and returns no handles
            c["is_op"] = bool(post.get("author")) and c.get("author") == post.get("author")
    low = " ".join((c.get("text") or "").lower() for c in comments)
    out = {"post": post, "comments": comments, "comment_count": len(comments),
           "process_asked": any(w in low for w in asked_words), "url": post["url"], "id": post["id"],
           "platform": plat, "fetched_at": iso(now_utc())}
    if post.get("via"):
        out["via"] = post["via"]
    if hidden:
        out["collapsed_comments"] = hidden  # Arctic Shift's tree folds long branches; their ids are not fetched
    if fwmeta:
        out["fetchwright"] = fwmeta  # provenance for the note: model, Google's retrieval statuses, tokens
    return out


def thread_cache_path(cfg, tid):
    return os.path.join(local_root(cfg), "cache", "threads", re.sub(r"[^\w.-]", "_", tid) + ".json")


# ---------------------------------------------------------------- Reddit discovery without a listing
# Plan: ai-docs/plans/2026-10-16-reddit-discovery-after-arctic-shift.md. Thread URLs come from links in items already
# fetched from other platforms (pickup, during fetch), the agent's own web search and the user's captures (discover add).
# Never from Gemini's Google Search (conduct rule 17). Entries live in the beat's state under reddit_seen_elsewhere.

DISCOVERY_KEEP_DAYS = 14
DISCOVERY_HOLD_HOURS = 24  # a thread under a day old may not be in Google's index yet, so fetchwright cannot read it
DISCOVERY_VIA = ("pickup", "websearch", "capture")
DISCOVERY_STATUSES = ("new", "read", "dropped", "wanted")  # wanted: a capture was asked of the user


def pickup_reddit_links(st, items, now=None):
    """Record the Reddit threads linked from non-Reddit items in st['reddit_seen_elsewhere'] (id -> entry), one mention
    per linking item, after purging entries first seen over DISCOVERY_KEEP_DAYS ago. Returns the ids linked this time."""
    now = now or now_utc()
    disc = st.setdefault("reddit_seen_elsewhere", {})
    cut = now - dt.timedelta(days=DISCOVERY_KEEP_DAYS)
    for k in [k for k, e in disc.items() if (S.parse_time(e.get("first_seen")) or now) < cut]:
        del disc[k]
    found = set()
    for it in items:
        if it.get("platform") == "reddit":
            continue
        blob = " ".join([it.get("url") or "", it.get("link") or "", it.get("title") or "", it.get("text") or ""]
                        + list(it.get("reddit_links") or []))
        for pid, sub, url in S.reddit_ids_in(blob):
            e = disc.setdefault(pid, {"id": pid, "sub": sub, "url": url, "first_seen": iso(now), "via": "pickup",
                                      "status": "new", "mentions": 0, "from": []})
            if sub and not e.get("sub"):
                e["sub"], e["url"] = sub, url
            if any(x.get("item") == it["id"] for x in e["from"]):
                continue  # the same item fetched again is not a second mention
            pt = S.parse_time(it.get("published"))
            pub = iso(pt) if pt else iso(now)
            e["from"] = (e["from"] + [{"item": it["id"], "platform": it.get("platform") or "", "source": it.get("source") or "",
                                       "title": (it.get("title") or "")[:140], "url": it.get("url") or "", "published": pub}])[-20:]
            e["mentions"] = e.get("mentions", 0) + 1
            # the thread is at least as old as the earliest item linking it, which dates the 24-hour hold
            if not e.get("linked_by") or pub < e["linked_by"]:
                e["linked_by"] = pub
            found.add(pid)
    return found


def discovery_rows(cfg, b, st, now=None):
    """Every discovery entry with what triage ranks it by: mentions across platforms, vocabulary on the linking text,
    the beat's showcase and skip words, and whether the 24-hour hold is over."""
    now = now or now_utc()
    dd = data_dir(cfg, b.slug)
    noted = {S.reddit_post_id(str(fm.get("url") or "")) for _, fm, _ in all_notes(dd)} - {None}
    listed = st.get("seen") or {}
    subs = {re.sub(r"^/?r/", "", r["source"]).lower() for r in b.sources() if r["kind"] == "reddit"}
    showcase = [w.lower() for w in b.list_meta("showcase_words", ("i made", "my first", "we made", "i built", "released"))]
    skip = [w.lower() for w in b.list_meta("skip_words", ("megathread", "weekly thread", "hiring", "[meta]", "daily discussion"))]
    rows = []
    for e in (st.get("reddit_seen_elsewhere") or {}).values():
        pid = e["id"]
        text = " ".join([e.get("title") or ""] + [x.get("title") or "" for x in e.get("from") or []])
        low = text.lower()
        if e.get("via") in ("websearch", "capture"):
            ready_at = S.parse_time(e.get("first_seen")) or now  # a search result is in the index already
        else:
            ready_at = (S.parse_time(e.get("linked_by")) or S.parse_time(e.get("first_seen")) or now) + dt.timedelta(hours=DISCOVERY_HOLD_HOURS)
        vocab = vocab_match(b, text)
        rows.append(dict(e, in_beat=(e.get("sub") or "").lower() in subs, listed=f"reddit:{pid}" in listed, noted=pid in noted,
                         ready=ready_at <= now, ready_at=iso(ready_at), vocab=vocab,
                         showcase=[w for w in showcase if w in low], skip=[w for w in skip if w in low],
                         platforms=sorted({x.get("platform") or "" for x in e.get("from") or []} - {""})))
    # mentions first (a thread linked from two sources beats one found by search; two posts of one blog count less than
    # two sources), then vocabulary, showcase words, home
    rows.sort(key=lambda r: (len({x.get("source") or x.get("item") for x in r.get("from") or []}), r.get("mentions", 0),
                             sum(len(v) for v in r["vocab"].values()), len(r["showcase"]), r["in_beat"]), reverse=True)
    return rows


def discovery_entry(cfg, b, ref):
    """(state, entry or None, id) for an id or a thread URL."""
    st = load_json(state_path(cfg, b.slug), {"seen": {}, "fetches": []})
    ids = S.reddit_ids_in(ref)
    pid = ids[0][0] if ids else ref.strip().lower()
    return st, (st.get("reddit_seen_elsewhere") or {}).get(pid), pid


def cmd_discover(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    if a.action == "add":
        ids = S.reddit_ids_in(a.url)
        if not ids:
            fail("not a Reddit thread URL (r/<sub>/comments/<id>, /comments/<id> or redd.it/<id>)", 2)
        pid, sub, url = ids[0]
        st = load_json(state_path(cfg, b.slug), {"seen": {}, "fetches": []})
        disc = st.setdefault("reddit_seen_elsewhere", {})
        e = disc.get(pid)
        if e is None:
            e = disc[pid] = {"id": pid, "sub": sub, "url": url, "first_seen": iso(now_utc()), "via": a.via, "status": "new",
                             "mentions": 0, "from": []}
        elif e.get("via") == "pickup" and a.via != "pickup":
            e["also_via"] = a.via  # found by pickup and by hand: keep pickup's mentions
        if sub and not e.get("sub"):
            e["sub"], e["url"] = sub, url
        if a.title:
            e["title"] = a.title[:140]
        if a.posted:
            e["linked_by"] = a.posted[:10] + "T00:00:00+00:00"
        save_json(state_path(cfg, b.slug), st)
        print(f"{pid} {e['url']} ({e['via']}{', also ' + e['also_via'] if e.get('also_via') else ''}, {e.get('mentions', 0)} mentions)")
        return
    if a.action == "mark":
        st, e, pid = discovery_entry(cfg, b, a.ref)
        if e is None:
            fail(f"{pid} is not in the beat's discovery list (`discover add` it first)", 2)
        e["status"] = a.status
        if a.why:
            e["why"] = a.why[:200]
        save_json(state_path(cfg, b.slug), st)
        print(f"{pid} {a.status}")
        return
    st = load_json(state_path(cfg, b.slug), {})
    rows = discovery_rows(cfg, b, st)
    wanted = [r for r in rows if r.get("status") == "wanted" and not r["noted"]]
    todo = [r for r in rows if a.all or (r.get("status", "new") == "new" and r["ready"] and not r["noted"] and not r["listed"]
                                          and not r["skip"])]
    if a.json:
        print(json.dumps({"threads": todo[: a.limit], "captures_wanted": wanted}, indent=1, ensure_ascii=False))
        return
    # coverage while a listing still exists: how many of the Reddit threads noted lately did pickup also find
    dd = data_dir(cfg, b.slug)
    cut = (now_utc() - dt.timedelta(days=DISCOVERY_KEEP_DAYS)).date().isoformat()
    recent = {S.reddit_post_id(str(fm.get("url") or "")) for _, fm, _ in all_notes(dd)
              if fm.get("platform") == "reddit" and str(fm.get("posted") or "") >= cut} - {None}
    found = {r["id"] for r in rows}
    held = sum(1 for r in rows if not r["ready"] and r.get("status", "new") == "new")
    print(f"{b.slug}: {len(rows)} Reddit threads found without a listing in the last {DISCOVERY_KEEP_DAYS} days "
          f"({sum(r['in_beat'] for r in rows)} in the beat's subreddits, {sum(r['listed'] for r in rows)} also in the listing, "
          f"{sum(r['noted'] for r in rows)} noted, {held} held under {DISCOVERY_HOLD_HOURS} h); "
          f"pickup found {len(recent & found)} of the {len(recent)} Reddit threads noted in that time")
    if thread_reader(cfg) == "fetchwright":
        cap = int((cfg.get("fetchwright") or {}).get("max_reads_per_scan") or 0)
        print(f"fetchwright reads this scan: {int(st.get('fetchwright_reads') or 0)}" + (f" of {cap}" if cap else ""))
    for r in todo[: a.limit]:
        ents = ", ".join(v for vs in r["vocab"].values() for v in vs)
        print(f"{r.get('mentions', 0):>2}x {r['via']:<9} {('r/' + r['sub']) if r.get('sub') else '?':<22} {r['url']}\n"
              f"      from {', '.join(r['platforms']) or r['via']}: {(r.get('title') or (r.get('from') or [{}])[0].get('title') or '')[:90]}"
              + (f"\n      vocab: {ents}" if ents else "") + (f"; showcase: {', '.join(r['showcase'])}" if r["showcase"] else "")
              + ("" if r["ready"] else f"\n      held until {r['ready_at'][:16]} UTC") + ("" if r["in_beat"] else "; outside the beat's subreddits"))
    if not todo:
        print("nothing ready to read")
    if wanted:
        print("\ncaptures wanted (asked of the user; their files go in " + os.path.join(dd, "captures") + "):")
        for r in wanted:
            print(f"- {r['url']}  {r.get('why') or ''}")


def fetchwright_budget(cfg, b, url, force=False):
    """None, or the run count to compare after the read when it may start fetchwright. Stops (exit 6) once the beat's
    reads since its last fetch reach fetchwright.max_reads_per_scan: the rest become capture requests."""
    if platform_of(url) != "reddit" or thread_reader(cfg) != "fetchwright" or (not force and fetchwright_cached(cfg, url)):
        return None
    cap = int((cfg.get("fetchwright") or {}).get("max_reads_per_scan") or 0)
    used = int(load_json(state_path(cfg, b.slug), {}).get("fetchwright_reads") or 0)
    if cap and used >= cap:
        fail(f"this scan used its {cap} fetchwright reads (fetchwright.max_reads_per_scan): stop reading Reddit threads "
             f"through fetchwright, mark the rest `discover mark <url> --status wanted --why ...` (at most five) and list "
             f"them as captures wanted; `--thread-reader same` still reads through the listing reader", 6)
    return FETCHWRIGHT_RUNS[0]


def count_fetchwright_read(cfg, b, before):
    if before is not None and FETCHWRIGHT_RUNS[0] > before:
        st = load_json(state_path(cfg, b.slug), {"seen": {}, "fetches": []})  # reloaded: a fetch may have saved since
        st["fetchwright_reads"] = int(st.get("fetchwright_reads") or 0) + FETCHWRIGHT_RUNS[0] - before
        save_json(state_path(cfg, b.slug), st)


CAPTURE_TEXT_EXT = (".txt", ".md", ".html", ".htm", ".json", ".eml")


def capture_text(path):
    """The text of a capture file the agent can read itself (pasted text, saved HTML); "" for images and PDFs."""
    if not path.lower().endswith(CAPTURE_TEXT_EXT):
        return ""
    t = read(path)
    return S.strip_html(t) if path.lower().endswith((".html", ".htm")) else t


def cmd_captures(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    inbox = os.path.join(data_dir(cfg, b.slug), "captures")
    os.makedirs(inbox, exist_ok=True)
    files = sorted(f for f in os.listdir(inbox) if os.path.isfile(os.path.join(inbox, f)) and not f.startswith("."))
    out = []
    for f in files:
        p = os.path.join(inbox, f)
        ids = S.reddit_ids_in(read(p)[:200000] if f.lower().endswith(CAPTURE_TEXT_EXT) else "")  # raw: hrefs hold the URL
        out.append({"file": p, "kind": "text" if f.lower().endswith(CAPTURE_TEXT_EXT) else "file",
                    "threads": [u for _, _, u in ids][:5], "bytes": os.path.getsize(p)})
    if a.json:
        print(json.dumps({"inbox": inbox, "captures": out}, indent=1))
        return
    print(f"{b.slug}: {len(out)} captures waiting in {inbox}")
    for c in out:
        print(f"- {os.path.basename(c['file'])} ({c['kind']}, {c['bytes']} bytes)" + (f": {', '.join(c['threads'])}" if c["threads"] else ": no thread URL inside; read it to find one"))


def cmd_thread(a):
    cfg = config()
    set_reddit_reader(cfg, a)
    words, b, before = ASKED_WORDS, None, None
    if a.beat:
        b = get_beat(cfg, a.beat)
        words = tuple(ASKED_WORDS) + tuple(w.lower() for w in b.list_meta("asked_words"))
        before = fetchwright_budget(cfg, b, a.url, force=a.force)
    try:
        t = load_thread(cfg, a.url, force=a.force, asked_words=words)
    except ReaderStop as e:
        fail(str(e), e.code)
    finally:
        if b:
            count_fetchwright_read(cfg, b, before)
    if not t:
        if platform_of(a.url) == "reddit" and thread_reader(cfg) == "fetchwright":
            fail("fetchwright could not read this thread (see the line above); try --thread-reader same", 1)
        fail("no thread reader for this URL (Reddit, HN, Bluesky, Mastodon, Lemmy, Discourse); read other pages with the agent's web fetch", 2)
    save_json(thread_cache_path(cfg, t["id"]), t)
    if a.json:
        print(json.dumps(t, indent=1, ensure_ascii=False))
        return
    p = t["post"]
    print(f"# {p['title']}\n{t['platform']} {p.get('community', '')} · {p.get('author', '')} · {p.get('published', '')} · "
          f"{t['comment_count']} comments{' (+' + str(t['collapsed_comments']) + ' collapsed)' if t.get('collapsed_comments') else ''} · process asked: {t['process_asked']}\n{p['url']}\n")
    if t.get("fetchwright"):
        fm = t["fetchwright"]
        u = fm.get("usage") or {}
        print(f"via fetchwright {fm.get('version') or ''} · {fm.get('model')} · page {u.get('page')} and output {u.get('output')} tokens"
              f" · {sum((fm.get('dropped') or {}).values())} dropped · long threads come back partly; no handles or dates\n")
    print((p.get("text") or "")[:3000])
    print("\n## Comments")
    for c in t["comments"][: a.limit]:
        who = "OP" if c.get("is_op") else c.get("author", "")
        print(f"- [{who}] {(c.get('text') or '')[:600].replace(chr(10), ' ')}")


def cmd_search(a):
    cfg = config()
    f = fetcher(cfg)
    if a.kind == "reddit" and set_reddit_reader(cfg, a) == "arcticshift":
        if not a.community:
            fail("Arctic Shift searches one subreddit at a time: pass --community r/name "
                 "(to find threads across Reddit, use the agent's web search for titles)", 2)
        days = {"day": 1, "week": 7, "month": 31, "year": 366, "all": 3650}.get(a.t, 31)
        end = (int(time.time()) // 3600 + 1) * 3600
        items, _, _ = arctic_window(f, a.community, end - days * 86400, end, max_pages=3,
                                    ttl=cfg["pace"]["feed_ttl_seconds"], force=a.force, query=a.q)
        if a.sort in ("top", "relevance", "comments"):
            items.sort(key=lambda i: (i.get("comments") if a.sort == "comments" else i.get("points")) or 0, reverse=True)
    elif a.kind == "reddit":
        q = urllib.parse.quote(a.q)
        if a.community:
            sub = re.sub(r"^r/", "", a.community)
            url = f"https://www.reddit.com/r/{sub}/search/.rss?q={q}&restrict_sr=1&sort={a.sort}&t={a.t}"
        else:
            url = f"https://www.reddit.com/search/.rss?q={q}&sort={a.sort}&t={a.t}"
        text, _, _ = f.get(url, ttl=cfg["pace"]["feed_ttl_seconds"], force=a.force)
        items = [i for i in S.parse_reddit(text, url) if i["kind"] == "post"]
    elif a.kind == "hn":
        days = {"day": 1, "week": 7, "month": 31, "year": 366, "all": None}.get(a.t, 31)
        url = S.hn_search_url(a.q, since_ts=(time.time() - days * 86400) if days else None, by_date=a.sort == "new")
        data, _, _ = f.get_json(url, ttl=cfg["pace"]["feed_ttl_seconds"], force=a.force)
        items = S.parse_hn_hits(data, url)
    elif a.kind in ("news", "arxiv"):
        url = S.google_news_feed(a.q) if a.kind == "news" else S.arxiv_query_feed(a.q)
        text, _, _ = f.get(url, ttl=cfg["pace"]["feed_ttl_seconds"], force=a.force)
        items = S.parse_feed(text, url, platform=a.kind)
    else:
        fail(f"search kind {a.kind!r} not supported (reddit, hn, news, arxiv); use the agent's web search for the rest")
    if a.json:
        print(json.dumps(items, indent=1, ensure_ascii=False))
        return
    print(f"{len(items)} results for {a.q!r} ({a.kind}{' ' + a.community if a.community else ''})")
    for i in items:
        extra = f" {i['comments']}c {i['points']}p" if i.get("comments") is not None else ""
        print(f"{(i.get('published') or '')[:10]} {str(i.get('community') or '')[:16]:<16}{extra} {i['title'][:70]}  {i['url']}")


# ---------------------------------------------------------------- engagement ledger and pace

def ledger(cfg):
    p = ledger_path(cfg)
    if not os.path.exists(p):
        return []
    out = []
    for line in read(p).splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except ValueError:
                note("ledger: skipped a bad line")
    return out


def save_ledger(cfg, entries):
    p = ledger_path(cfg)
    write(p, "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries))
    build_ledger_index(cfg, entries)


def engage_rules(cfg, platform):
    e = dict(cfg["engage"])
    e.update((cfg["engage"].get("platforms") or {}).get(platform) or {})
    return e


def engage_check(cfg, platform, community=None, author=None, item=None, kind="ask", now=None):
    """(ok, reasons, next_ok_iso). Counts posted and handed entries on the same platform across all beats."""
    now = now or now_utc()
    rules = engage_rules(cfg, platform)
    entries = [e for e in ledger(cfg) if e.get("status") in ("posted", "handed") and e.get("platform") == platform]
    reasons, next_ok = [], now
    times = sorted((S.parse_time(e["ts"]) for e in entries if S.parse_time(e.get("ts"))), reverse=True)
    if times:
        gap = dt.timedelta(minutes=rules["min_gap_minutes"])
        if now - times[0] < gap:
            reasons.append(f"last engagement on {platform} {int((now - times[0]).total_seconds() // 60)} minutes ago "
                           f"(gap {rules['min_gap_minutes']})")
            next_ok = max(next_ok, times[0] + gap)
        day = [t for t in times if now - t < dt.timedelta(hours=24)]
        if len(day) >= rules["max_per_day"]:
            reasons.append(f"{len(day)} engagements on {platform} in 24 hours (cap {rules['max_per_day']})")
            next_ok = max(next_ok, day[rules["max_per_day"] - 1] + dt.timedelta(hours=24))
    if kind == "ask":
        if community:
            win = dt.timedelta(hours=rules["per_community_hours"])
            recent = [e for e in entries if (e.get("community") or "").lower() == community.lower() and e.get("kind", "ask") == "ask"
                      and S.parse_time(e["ts"]) and now - S.parse_time(e["ts"]) < win]
            if recent:
                reasons.append(f"already engaged in {community} within {rules['per_community_hours']} hours")
                next_ok = max(next_ok, S.parse_time(recent[-1]["ts"]) + win)
        if author and any((e.get("author") or "").lower() == author.lower() and e.get("kind", "ask") == "ask" for e in entries):
            reasons.append(f"already asked {author} (never the same person twice)")
        if item and any(e.get("item") == item and e.get("kind", "ask") == "ask" for e in entries):
            reasons.append("already asked on this item")
    return (not reasons), reasons, iso(next_ok)


def cmd_engage_check(a):
    cfg = config()
    ok, reasons, next_ok = engage_check(cfg, a.platform, a.community, a.author, a.item, a.kind)
    if a.json:
        print(json.dumps({"ok": ok, "reasons": reasons, "next_ok": next_ok}))
    else:
        print("ok: an engagement is allowed now" if ok else "blocked: " + "; ".join(reasons) + f" (next allowed {next_ok})")
    sys.exit(0 if ok else 2)


def cmd_engage_record(a):
    cfg = config()
    text = read(a.text_file) if a.text_file else (a.text or "")
    if a.status in ("posted", "handed") and not a.override:
        ok, reasons, _ = engage_check(cfg, a.platform, a.community, a.author, a.item, a.kind)
        if not ok:
            fail("pace rules block this: " + "; ".join(reasons) + " (pass --override only if the user said so)", 2)
    entries = ledger(cfg)
    e = {
        "ts": iso(now_utc()), "beat": a.beat, "platform": a.platform, "community": a.community, "item": a.item,
        "url": a.url, "author": a.author, "title": a.title or "", "kind": a.kind,
        "questions": [q.strip() for q in (a.questions or "").split("|") if q.strip()],
        "route": a.route, "status": a.status, "text": text, "text_sha": hashlib.sha1(text.encode("utf-8")).hexdigest()[:12],
        "comment_url": a.comment_url or "", "override": bool(a.override), "replies": [],
    }
    entries.append(e)
    save_ledger(cfg, entries)
    print(f"recorded {a.kind} {a.status} on {a.platform} {a.community} ({a.url})")


def cmd_engage_update(a):
    cfg = config()
    entries = ledger(cfg)
    hit = [e for e in entries if e.get("item") == a.item and e.get("kind", "ask") == a.kind]
    if not hit:
        fail(f"no {a.kind} entry for item {a.item}")
    e = hit[-1]
    if a.status:
        e["status"] = a.status
        if a.status in ("posted", "handed"):
            e["ts"] = iso(now_utc())
    if a.comment_url:
        e["comment_url"] = a.comment_url
    save_ledger(cfg, entries)
    print(f"updated {a.item}: status {e['status']}")


def cmd_ledger(a):
    cfg = config()
    cut = now_utc() - dt.timedelta(days=a.days)
    es = [e for e in ledger(cfg) if (not a.beat or e.get("beat") == a.beat) and (S.parse_time(e.get("ts")) or cut) >= cut]
    if a.json:
        print(json.dumps(es, indent=1, ensure_ascii=False))
        return
    for e in es:
        print(f"{e['ts'][:16]} {e.get('beat', ''):<16} {e.get('platform', ''):<7} {e.get('kind', 'ask'):<6} {e['status']:<7} "
              f"{str(e.get('community'))[:18]:<18} {len(e.get('replies') or [])} replies  {e.get('title', '')[:50]}  {e.get('url')}")
        if a.text:
            print("    " + (e.get("text") or "").replace("\n", "\n    "))


def build_ledger_index(cfg, entries=None):
    entries = entries if entries is not None else ledger(cfg)
    lines = ["# Engagement ledger", "", "Generated by `everscout.py`; never edit by hand. One line per question, thank-you or answer, "
             "newest first. The source of truth is `engagements.jsonl` next to this file.", "",
             "| when | beat | platform | community | kind | status | replies | item |", "|---|---|---|---|---|---|---|---|"]
    for e in sorted(entries, key=lambda e: e.get("ts", ""), reverse=True):
        title = (e.get("title") or e.get("url") or "").replace("|", "/")[:60]
        lines.append(f"| {e.get('ts', '')[:16]} | {e.get('beat', '')} | {e.get('platform', '')} | {e.get('community', '')} | "
                     f"{e.get('kind', 'ask')} | {e.get('status')} | {len(e.get('replies') or [])} | [{title}]({e.get('url')}) |")
    write(os.path.join(ledger_dir(cfg), "INDEX.md"), "\n".join(lines) + "\n")


def cmd_followups(a):
    cfg = config()
    entries = ledger(cfg)
    cut = now_utc() - dt.timedelta(days=a.days)
    changed, found = False, 0
    me = (cfg.get("reddit_user") or "").lower()
    for e in entries:
        # A drafted ask is checked too when the user's Reddit name is known: people often post
        # the draft by hand and never mark it, and then its replies were never collected.
        if e.get("kind", "ask") != "ask" or e.get("status") not in ("posted", "handed", "drafted"):
            continue
        if e.get("status") == "drafted" and not (me and platform_of(e.get("url", "")) == "reddit"):
            continue
        if a.beat and e.get("beat") != a.beat:
            continue
        ts = S.parse_time(e.get("ts"))
        if not ts or ts < cut or platform_of(e.get("url", "")) == "web":
            continue
        try:
            # replies are matched by author and time, which fetchwright does not return: always the listing's reader
            t = load_thread(cfg, e["url"], force=a.force, reader="same")
        except (S.FetchError, ValueError) as ex:
            note(f"{e['url']}: {ex}")
            continue
        if not t:
            continue
        # The user's own comment dates the ask better than the ledger's ts, which engage-update
        # resets to "now" when the status changes (after the replies may already have arrived).
        mine = sorted((S.parse_time(c.get("published")), c) for c in t["comments"]
                      if me and (c.get("author") or "").lower() == me and S.parse_time(c.get("published")))
        if mine:
            ts = mine[0][0]
            if e.get("status") == "drafted":
                e["status"], e["ts"] = "posted", iso(ts)
                e["comment_url"] = e.get("comment_url") or mine[0][1].get("url", "")
                changed = True
                print(f"found your comment, marked posted: {e['url']}")
        elif e.get("status") == "drafted":
            continue
        # Reddit feeds carry no parent ids, so read only the subtree under the user's comment:
        # otherwise every later comment by the author (thanks to other people) counts as a reply.
        if e.get("comment_url") and platform_of(e["comment_url"]) == "reddit" and e["comment_url"] != e.get("url"):
            try:
                t = load_thread(cfg, e["comment_url"], force=a.force, reader="same") or t
            except (S.FetchError, ValueError) as ex:
                note(f"{e['comment_url']}: {ex}")
        have = {r.get("id") for r in e.get("replies") or []}
        have_when = {str(r.get("when") or "")[:16] for r in e.get("replies") or []}  # replies imported without a comment id
        new = []
        for c in t["comments"]:
            ct = S.parse_time(c.get("published"))
            if c.get("author", "").lower() == (e.get("author") or "").lower() and ct and ct > ts and c.get("id") not in have                     and str(c.get("published") or "")[:16] not in have_when:
                r = {"id": c.get("id"), "when": c.get("published"), "text": (c.get("text") or "")[:3000], "is_op": True}
                e.setdefault("replies", []).append(r)
                new.append(r)
        if new:
            changed = True
            found += len(new)
            print(f"== {e.get('beat')} {e.get('community')}: {e.get('title', '')[:70]}\n{e['url']}")
            for r in new:
                print(f"- {r['when'][:16]}: {r['text'][:800]}")
    if changed:
        save_ledger(cfg, entries)
    print(f"{found} new replies from the people asked")


# ---------------------------------------------------------------- candidates and questions

def score_item(it, b, cfg, entries, now):
    rules = engage_rules(cfg, it.get("platform", "reddit"))
    why, score = [], 0.0
    age = it.get("age_hours")
    if age is None:
        return None
    if age < rules["min_item_age_hours"] or age > rules["max_item_age_days"] * 24:
        return None
    if not it.get("engage_ok"):
        return None
    if any(e.get("item") == it["id"] and e.get("kind", "ask") == "ask" for e in entries):
        return None
    if it.get("author") and any((e.get("author") or "").lower() == it["author"].lower() and e.get("kind", "ask") == "ask"
                                for e in entries):
        return None
    low = (it.get("title", "") + " " + it.get("text", "")).lower()
    words = [w.lower() for w in b.list_meta("showcase_words", ("i made", "my first", "we made", "i built", "released",
                                                                "my new", "just finished", "devlog", "wip", "our "))]
    skip = [w.lower() for w in b.list_meta("skip_words", ("megathread", "weekly thread", "hiring", "[meta]", "daily discussion"))]
    if any(w in low for w in skip):
        return None
    hits = [w for w in words if w in low]
    if hits:
        score += 3
        why.append("maker words: " + ", ".join(hits[:3]))
    if it.get("media"):
        score += 1.5
        why.append("media: " + ",".join(it["media"]))
    if it.get("top"):
        score += 1
        why.append("top of week")
    score += max(0.0, 2 - abs(age - 18) / 24)  # freshest useful window is roughly half a day to a day old
    stance_bonus = {"native": 1.0, "open": 0.8, "mixed": 0.3, "hostile": 0.0}.get(it.get("stance"), 0)
    score += stance_bonus
    if "?" in it.get("title", ""):
        score -= 1.5
        why.append("reads as a question")
    return {"score": round(score, 2), "why": why}


def cmd_candidates(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    entries = ledger(cfg)
    now = now_utc()
    items = load_json(items_path(cfg, b.slug), [])
    out = []
    for it in items:
        pub = S.parse_time(it.get("published"))
        it["age_hours"] = round((now - pub).total_seconds() / 3600, 1) if pub else None
        s = score_item(it, b, cfg, entries, now)
        if s:
            it.update(s)
            out.append(it)
    out.sort(key=lambda i: i["score"], reverse=True)
    out = out[: a.limit]
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return
    if not out:
        print("no candidates in the cache (fetch first, or no engage-yes source has fresh maker posts)")
    for i in out:
        print(f"{i['score']:>5} {i['age_hours']:>5}h {i.get('stance', ''):<7} {str(i.get('community'))[:18]:<18} "
              f"{i['title'][:64]}  {i['url']}\n      {'; '.join(i['why'])}")


def cmd_questions(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    qs = b.questions()
    tags = [t.strip().lower() for t in a.tags.split(",")] if a.tags else []
    recent = set()
    cut = now_utc() - dt.timedelta(days=a.exclude_recent)
    for e in ledger(cfg):
        if (S.parse_time(e.get("ts")) or cut) > cut:
            recent.update(q.lower() for q in e.get("questions") or [])
    pool = [q for q in qs if q["text"].lower() not in recent]
    if a.avoid_ai:
        pool = [q for q in pool if "ai" not in q["tags"]]
    if tags:
        pool = [q for q in pool if q["category"] in tags or set(q["tags"]) & set(tags)] or pool
    # deterministic spread across categories: round robin, rotated by the day so repeats are rare
    bycat = {}
    for q in pool:
        bycat.setdefault(q["category"], []).append(q)
    day = int(now_utc().strftime("%j"))
    for v in bycat.values():
        k = day % len(v)
        v[:] = v[k:] + v[:k]
    picked = []
    while len(picked) < a.n and any(bycat.values()):
        for c in list(bycat):
            if bycat[c] and len(picked) < a.n:
                picked.append(bycat[c].pop(0))
    if a.json:
        print(json.dumps(picked, indent=1, ensure_ascii=False))
    else:
        for q in picked:
            print(f"[{q['category']}; {', '.join(q['tags'])}] {q['text']}")


# ---------------------------------------------------------------- notes

def note_path(dd, posted, nid, title):
    month = (posted or today())[:7]
    return os.path.join(dd, "notes", month, f"{slugify(nid, 24)}-{slugify(title, 40)}.md")


def vocab_match(b, text):
    """{facet: [canonical]} for every alias found in text (word-bounded, case-insensitive, a plural counts). A line with aliases matches
    only its aliases (the id is an id: `us`, `fed` or `warp` must not fire on ordinary words); a line without aliases
    matches its id."""
    low = " " + (text or "").lower() + " "
    out = {}
    for facet, ents in b.vocab().items():
        for canon, aliases in ents.items():
            for term in (aliases or [canon]):
                t = term.lower().strip()
                if not t:
                    continue
                if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?:s|es)?(?![a-z0-9])", low):
                    out.setdefault(facet, []).append(canon)
                    break
    return out


def cmd_vocab_match(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    text = read(a.file) if a.file else (a.text or sys.stdin.read())
    m = vocab_match(b, text)
    if a.json:
        print(json.dumps(m, indent=1))
    else:
        for facet, ents in m.items():
            print(f"{facet}: [{', '.join(ents)}]")
        if not m:
            print("no vocabulary entity found")


def cmd_new_note(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    dd = data_dir(cfg, b.slug)
    fm_extra, capture, moved = {}, None, None
    ids = S.reddit_ids_in(a.url)
    disc = (load_json(state_path(cfg, b.slug), {}).get("reddit_seen_elsewhere") or {}).get(ids[0][0]) if ids else None
    if a.capture:
        # the user's own copy of a page the scan could not read (lane plan step 4): no fetch, the agent writes the body
        capture = os.path.abspath(expand(a.capture))
        if not os.path.isfile(capture):
            fail(f"no capture file at {capture}", 2)
        if not a.title:
            fail("a note from a capture needs --title (the title as the capture shows it) and, when known, --posted", 2)
        title, plat, top, interest = a.title, platform_of(a.url), False, a.interest or 0
        posted = (a.posted or (disc or {}).get("linked_by") or today())[:10]
        if ids:
            nid, community, url = ids[0]
        else:
            nid, community, url = "cap-" + hashlib.sha1(a.url.encode()).hexdigest()[:8], urllib.parse.urlsplit(a.url).hostname or "", a.url
        body_text = title + "\n" + capture_text(capture)
        fm_extra["source"] = "user-capture"
        inbox = os.path.abspath(os.path.join(dd, "captures"))
        if os.path.normcase(os.path.dirname(capture)) == os.path.normcase(inbox):
            moved = os.path.join(inbox, "done", os.path.basename(capture))  # read: out of the inbox, kept for the user
            fm_extra["capture"] = "captures/done/" + os.path.basename(capture)
        else:
            fm_extra["capture"] = os.path.basename(capture)
    elif platform_of(a.url) != "web":
        set_thread_reader(cfg, a)
        before = fetchwright_budget(cfg, b, a.url)
        try:
            t = load_thread(cfg, a.url)
        except ReaderStop as e:
            fail(str(e), e.code)
        finally:
            count_fetchwright_read(cfg, b, before)
        if not t:
            fail("thread not found")
        p = t["post"]
        items = {i["id"]: i for i in load_json(items_path(cfg, b.slug), [])}
        # fetchwright returns no date: the fetched listing has it, else the earliest item that linked the thread
        title, plat = p["title"], t["platform"]
        posted = (p.get("published") or items.get(p["id"], {}).get("published") or (disc or {}).get("linked_by") or today())[:10]
        community, nid, interest = p.get("community") or "", p["id"].split(":")[-1], t["comment_count"]
        url = p["url"]
        body_text = title + "\n" + (p.get("text") or "") + "\n" + "\n".join(c.get("text") or "" for c in t["comments"])
        top = bool(items.get(p["id"], {}).get("top"))
        if t.get("via"):
            fm_extra["via"] = t["via"]  # where interest came from: arcticshift scores, or fetchwright's partial comment count
    else:
        items = {i["url"]: i for i in load_json(items_path(cfg, b.slug), [])}
        it = items.get(a.url, {})
        title = a.title or it.get("title") or a.url
        posted = (a.posted or it.get("published") or today())[:10]
        plat = it.get("platform") or "web"
        community = it.get("community") or urllib.parse.urlsplit(a.url).hostname or ""
        nid, interest, url, top = "web-" + hashlib.sha1(a.url.encode()).hexdigest()[:8], a.interest or 0, a.url, False
        body_text = (title or "") + "\n" + (it.get("text") or "")
    path = note_path(dd, posted, nid, title)
    existing = [os.path.join(r, f) for r, _, fs in os.walk(os.path.join(dd, "notes")) for f in fs
                if f.startswith(slugify(nid, 24) + "-")] if os.path.isdir(os.path.join(dd, "notes")) else []
    if existing and not a.force:
        print(existing[0])
        fail("a note for this item exists (printed above); edit it, or pass --force", 3)
    matched = vocab_match(b, body_text)
    fm = {"title": re.sub(r"[:#]", " ", title).strip()[:140], "kind": "note", "status": "active", "date": today(), "verified": today(),
          "beat": b.slug, "platform": plat, "community": community, "url": url, "posted": posted,
          "note_kind": a.note_kind, "interest": interest, "top": top, "engaged": bool(a.engaged)}
    for facet in b.facets():
        fm[facet] = matched.get(facet, [])
    fm["tags"] = [b.slug, plat]
    fm["summary"] = "TODO one line saying what this teaches"
    if disc:
        fm_extra["discovered"] = disc.get("via") or "pickup"
        fm_extra["mentions"] = disc.get("mentions", 0)
    fm.update(fm_extra)
    body = f"# {fm['title']}\n\n" + "".join(f"## {s}\n\nTODO\n\n" for s in b.sections()) + \
        f"Related: [beat index](../../INDEX.md)\n"
    write(path, render_frontmatter(fm) + "\n" + body)
    if moved:
        os.makedirs(os.path.dirname(moved), exist_ok=True)
        os.replace(capture, moved)
    if disc:
        st = load_json(state_path(cfg, b.slug), {"seen": {}, "fetches": []})
        e = (st.get("reddit_seen_elsewhere") or {}).get(disc["id"])
        if e:
            e["status"] = "read"
            save_json(state_path(cfg, b.slug), st)
    print(path)
    if matched:
        note("vocabulary found (prefilled, check it): " + "; ".join(f"{k}: {', '.join(v)}" for k, v in matched.items()))


def all_notes(dd):
    root = os.path.join(dd, "notes")
    out = []
    if not os.path.isdir(root):
        return out
    for r, _, fs in os.walk(root):
        for f in sorted(fs):
            if f.endswith(".md") and f != "INDEX.md":
                p = os.path.join(r, f)
                fm, body = parse_frontmatter(read(p))
                out.append((p, fm, body))
    return out


def cmd_validate(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    dd = data_dir(cfg, b.slug)
    voc = b.vocab()
    required = ("title", "kind", "status", "date", "verified", "beat", "platform", "url", "posted", "note_kind", "summary")
    errs, warns, n = [], [], 0
    for p, fm, body in all_notes(dd):
        n += 1
        rel = os.path.relpath(p, dd)
        for k in required:
            if k not in fm or fm[k] in ("", None):
                errs.append(f"{rel}: missing {k}")
        if str(fm.get("summary", "")).startswith("TODO") or "\nTODO\n" in body:
            errs.append(f"{rel}: TODO left in the note")
        if fm.get("note_kind") and fm["note_kind"] not in NOTE_KINDS:
            warns.append(f"{rel}: note_kind {fm['note_kind']} not in {', '.join(NOTE_KINDS)}")
        if fm.get("posted") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm["posted"])):
            errs.append(f"{rel}: posted is not YYYY-MM-DD")
        for facet, ents in voc.items():
            vals = fm.get(facet, [])
            if isinstance(vals, str):
                vals = [vals] if vals else []
                errs.append(f"{rel}: {facet} should be a list")
            for v in vals:
                if v not in ents:
                    warns.append(f"{rel}: {facet} value {v!r} is not in vocab.md (add it, or use the canonical spelling)")
        for s in b.sections():
            if f"## {s}" not in body:
                warns.append(f"{rel}: missing section '## {s}'")
    for e in errs:
        print("ERROR  " + e)
    for w in warns:
        print("warn   " + w)
    print(f"{n} notes, {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs or (a.strict and warns) else 0)


# ---------------------------------------------------------------- signals

def tally(b, dd, now=None):
    now = now or now_utc()
    voc = b.vocab()
    facets = list(voc.keys())
    res = {f: {} for f in facets}
    half_life = float(b.meta.get("half_life_days") or 30)
    for p, fm, _ in all_notes(dd):
        posted = S.parse_time(str(fm.get("posted") or fm.get("date") or ""))
        if not posted:
            continue
        age = (now - posted).days
        interest = fm.get("interest") if isinstance(fm.get("interest"), int) else 0
        weight = 1 + math.sqrt(max(0, interest)) / 4
        decayed = weight * 0.5 ** (max(0, age) / half_life)
        where = f"{fm.get('platform', '')}:{fm.get('community', '')}"
        for facet in facets:
            vals = fm.get(facet) or []
            if isinstance(vals, str):
                vals = [vals]
            for v in vals:
                r = res[facet].setdefault(v, {"30d": 0, "prev30d": 0, "90d": 0, "all": 0, "w30": 0.0, "w90": 0.0, "wall": 0.0,
                                              "decayed": 0.0, "first": fm.get("posted"), "last": fm.get("posted"), "where90": [],
                                              "known": v in voc[facet], "example": ""})
                r["all"] += 1
                r["wall"] += weight
                r["decayed"] += decayed
                if age <= 30:
                    r["30d"] += 1
                    r["w30"] += weight
                elif age <= 60:
                    r["prev30d"] += 1
                if age <= 90:
                    r["90d"] += 1
                    r["w90"] += weight
                    if where not in r["where90"]:
                        r["where90"].append(where)
                if str(fm.get("posted")) < str(r["first"]):
                    r["first"] = fm.get("posted")
                if str(fm.get("posted")) >= str(r["last"]):
                    r["last"] = fm.get("posted")
                    r["example"] = os.path.relpath(p, dd).replace(os.sep, "/")
    for facet in facets:
        for v, r in res[facet].items():
            first = S.parse_time(str(r["first"]))
            r["spread90"] = len(r.pop("where90"))
            for k in ("w30", "w90", "wall", "decayed"):
                r[k] = round(r[k], 2)
            if first and (now - first).days <= 30:
                r["signal"] = "new"
            elif r["30d"] >= 2 and r["30d"] >= 1.5 * max(1, r["prev30d"]):
                r["signal"] = "rising"
            elif r["prev30d"] >= 2 and r["30d"] <= 0.5 * r["prev30d"]:
                r["signal"] = "fading"
            elif r["90d"] == 0:
                r["signal"] = "dormant"
            else:
                r["signal"] = "steady"
    return res


def cmd_tally(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    dd = data_dir(cfg, b.slug)
    res = tally(b, dd)
    n = len(all_notes(dd))
    save_json(os.path.join(dd, "signals", "tallies.json"), {"generated": iso(now_utc()), "notes": n, "facets": res})
    lines = [f"# Signals: {b.title}", "", f"Generated {iso(now_utc())} by `everscout.py tally` from {n} notes; never edit by hand. "
             "Weight per mention is 1 + sqrt(interest)/4, where interest is the comment count the source showed; "
             f"decayed halves that weight every {b.meta.get('half_life_days') or 30} days of age. Counts are notes (one per thread), not mentions. "
             "Signal: new (first seen in the last 30 days), rising (30-day count at least 2 and at least 1.5 times the "
             "30 days before), fading (at most half the 30 days before, which had 2 or more), steady, dormant. "
             "Spread is the number of distinct communities in 90 days. Entities marked * are not in vocab.md yet.", ""]
    for facet, ents in res.items():
        lines += [f"## {facet}", "", "| entity | 30d | prev 30d | 90d | all | decayed | spread | signal | last | example |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for v, r in sorted(ents.items(), key=lambda kv: (-kv[1]["decayed"], -kv[1]["all"], kv[0])):
            lines.append(f"| {v}{'' if r['known'] else ' *'} | {r['30d']} | {r['prev30d']} | {r['90d']} | {r['all']} | {r['decayed']} | "
                         f"{r['spread90']} | {r['signal']} | {r['last']} | [note](../{r['example']}) |")
        lines.append("")
    write(os.path.join(dd, "signals", "signals.md"), "\n".join(lines))
    movers = [(f, v, r) for f, ents in res.items() for v, r in ents.items() if r["signal"] in ("new", "rising", "fading")]
    print(f"{n} notes tallied into {sum(len(e) for e in res.values())} entities across {len(res)} facets; "
          f"{sum(1 for m in movers if m[2]['signal'] == 'new')} new, {sum(1 for m in movers if m[2]['signal'] == 'rising')} rising, "
          f"{sum(1 for m in movers if m[2]['signal'] == 'fading')} fading")
    for f, v, r in sorted(movers, key=lambda m: -m[2]["w30"])[:15]:
        print(f"  {r['signal']:<7} {f}: {v} ({r['30d']} in 30d, {r['prev30d']} before, spread {r['spread90']})")


# ---------------------------------------------------------------- recall (the beat as a reporter's memory)

STOPWORDS = set("""a an and are as at be been but by can could did do does for from had has have how i if in into is it its
me my no not of on or our so than that the their them then there these they this to too up us was we were what when where
which who why will with would you your about any anything just more most much should some tell very""".split())


def query_terms(q):
    return [w for w in re.findall(r"[a-z0-9][a-z0-9+.#-]*", (q or "").lower()) if w not in STOPWORDS and len(w) > 1]


def kb_documents(dd):
    """Every file in a beat's knowledge base the reporter can recall: notes, answers, reports, study, the journal."""
    docs = [("note", p, fm, body) for p, fm, body in all_notes(dd)]
    for sub, kind in (("answers", "answer"), ("reports", "report"), ("study", "study")):
        folder = os.path.join(dd, sub)
        if os.path.isdir(folder):
            for f in sorted(os.listdir(folder)):
                if f.endswith(".md") and f != "INDEX.md":
                    fm, body = parse_frontmatter(read(os.path.join(folder, f)))
                    docs.append((kind, os.path.join(folder, f), fm, body))
    j = os.path.join(dd, "journal.md")
    if os.path.exists(j):
        docs.append(("journal", j, {"title": "journal"}, read(j)))
    return docs


def recall(b, dd, q, limit=12, now=None):
    """Rank the knowledge base against a question. Score: each query word (whole word, plural allowed) found in the title (x3), the summary or
    question (x2) and the body (x1, at most 3 a word), plus 4 for each vocabulary entity the question names that the
    document is tagged with or mentions; a note's score is scaled by its age on the beat's half-life (never below half).
    Returns (hits, entities named in the question, tally rows for them)."""
    now = now or now_utc()
    terms = query_terms(q)
    named = vocab_match(b, q)
    ents = [(f, e) for f, es in named.items() for e in es]
    voc = b.vocab()
    half_life = float(b.meta.get("half_life_days") or 30)
    hits = []
    for kind, p, fm, body in kb_documents(dd):
        title = str(fm.get("title") or "").lower()
        summ = (str(fm.get("summary") or "") + " " + str(fm.get("question") or "")).lower()
        low = body.lower()
        s = 0.0
        for t in terms:
            pat = r"(?<![a-z0-9])" + re.escape(t) + r"(?:s|es)?(?![a-z0-9])"
            s += 3 * len(re.findall(pat, title)) + 2 * len(re.findall(pat, summ)) + min(3, len(re.findall(pat, low)))
        for f, e in ents:
            vals = fm.get(f) or []
            vals = [vals] if isinstance(vals, str) else vals
            aliases = voc.get(f, {}).get(e) or [e]
            if e in vals or any(re.search(r"(?<![a-z0-9])" + re.escape(al.lower()) + r"(?![a-z0-9])", low) for al in aliases):
                s += 4
        if s <= 0:
            continue
        when = str(fm.get("posted") or fm.get("date") or "")
        t0 = S.parse_time(when)
        if kind == "note" and t0:
            s *= 0.5 + 0.5 * 0.5 ** (max(0, (now - t0).days) / half_life)
        hits.append({"score": round(s, 2), "kind": kind, "date": when[:10], "path": os.path.relpath(p, dd).replace(os.sep, "/"),
                     "title": fm.get("title") or os.path.basename(p), "summary": fm.get("summary") or "",
                     "url": fm.get("url") or "", "community": fm.get("community") or ""})
    hits.sort(key=lambda h: (-h["score"], h["path"]))
    tallies = load_json(os.path.join(dd, "signals", "tallies.json"), {}).get("facets", {})
    keep = ("30d", "prev30d", "90d", "all", "signal", "last", "spread90")
    trows = [dict({"facet": f, "entity": e}, **{k: v for k, v in (tallies.get(f, {}).get(e) or {}).items() if k in keep})
             for f, e in ents]
    return hits[:limit], named, trows


def kb_status(cfg, b, dd):
    st = load_json(state_path(cfg, b.slug), {})
    dates = sorted(str(fm.get("posted") or fm.get("date") or "")[:10] for _, fm, _ in all_notes(dd))
    ad = os.path.join(dd, "answers")
    return {"beat": b.slug, "title": b.title, "notes": len(dates), "newest_note": dates[-1] if dates else None,
            "oldest_note": dates[0] if dates else None, "last_fetch": st.get("last_fetch"),
            "answers": len([f for f in os.listdir(ad) if f.endswith(".md") and f != "INDEX.md"]) if os.path.isdir(ad) else 0}


def cmd_leads(a):
    """What a beat has seen since a date: notes, then reports, newest first. Leads for a caller to verify, never sources."""
    cfg = config()
    b = get_beat(cfg, a.beat)
    dd = data_dir(cfg, b.slug)
    since = a.since[:10]
    notes = []
    for p, fm, _ in all_notes(dd):
        when = str(fm.get("posted") or fm.get("date") or "")[:10]
        if when >= since:
            notes.append({"date": when, "title": fm.get("title") or os.path.basename(p), "summary": fm.get("summary") or "",
                          "url": fm.get("url") or "", "path": os.path.relpath(p, dd).replace(os.sep, "/")})
    notes.sort(key=lambda n: (n["date"], n["path"]), reverse=True)
    reports = []
    rd = os.path.join(dd, "reports")
    if os.path.isdir(rd):
        for f in sorted(os.listdir(rd), reverse=True):
            if f.endswith(".md") and f != "INDEX.md":
                fm, _ = parse_frontmatter(read(os.path.join(rd, f)))
                when = str(fm.get("date") or f[:10])[:10]
                if when >= since:
                    reports.append({"date": when, "title": fm.get("title") or f, "summary": fm.get("summary") or "",
                                    "path": "reports/" + f})
    st = load_json(state_path(cfg, b.slug), {})
    out = {"beat": b.slug, "since": since, "last_fetch": st.get("last_fetch"), "data": dd,
           "reports": reports, "notes": notes[:a.limit], "notes_total": len(notes)}
    if a.json:
        print(json.dumps(out, indent=1))
        return
    print(f"{b.slug}: {len(notes)} notes and {len(reports)} reports since {since}; last fetch {out['last_fetch'] or 'never'}; data {dd}")
    for r in reports:
        print(f"report {r['date']} {r['path']}: {r['summary'][:160]}")
    for n in notes[:a.limit]:
        print(f"note   {n['date']} {n['path']}: {n['title'][:100]}")


def cmd_recall(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    dd = data_dir(cfg, b.slug)
    hits, named, trows = recall(b, dd, a.q, a.limit)
    status = kb_status(cfg, b, dd)
    if a.json:
        print(json.dumps({"status": status, "entities": named, "tallies": trows, "hits": hits}, indent=1))
        return
    print(f"{b.slug}: {status['notes']} notes (newest {status['newest_note'] or '-'}), {status['answers']} answers, "
          f"last fetch {status['last_fetch'] or 'never'}")
    if named:
        print("entities named: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in named.items()))
    for r in trows:
        if "signal" in r:
            print(f"  signal {r['entity']}: {r['signal']} ({r.get('30d')} in 30d, {r.get('prev30d')} before, "
                  f"{r.get('all')} all, last {r.get('last')})")
        else:
            print(f"  signal {r['entity']}: no notes yet")
    if not hits:
        print("nothing in the knowledge base matches; answer from the beat's sources and the web, then save the answer")
    for h in hits:
        print(f"{h['score']:>6} {h['kind']:<7} {h['date'] or '-':<10} {h['path']}  {h['summary'] or h['title']}")


# ---------------------------------------------------------------- indexes

def index_folder(folder, title, intro, recurse=False):
    if not os.path.isdir(folder):
        return 0
    lines = [f"# {title}", "", intro + " Generated by `everscout.py index`; never edit by hand.", ""]
    count = 0
    subdirs = sorted((d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))), reverse=True)
    if recurse and subdirs:
        for d in subdirs:
            n = index_folder(os.path.join(folder, d), f"{title}: {d}", intro)
            lines.append(f"- [{d}]({d}/INDEX.md) ({n})")
            count += n
    files = []
    for f in os.listdir(folder):
        if f.endswith(".md") and f != "INDEX.md":
            fm, _ = parse_frontmatter(read(os.path.join(folder, f)))
            files.append((str(fm.get("posted") or fm.get("date") or ""), f, fm))
    for d, f, fm in sorted(files, key=lambda x: (x[0], x[1]), reverse=True):
        summ = fm.get("summary") or ""
        lines.append(f"- [{fm.get('title') or f}]({f}) {d} {('· ' + summ) if summ else ''}".rstrip())
        count += 1
    write(os.path.join(folder, "INDEX.md"), "\n".join(lines) + "\n")
    return count


def cmd_index(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    dd = data_dir(cfg, b.slug)
    os.makedirs(dd, exist_ok=True)
    counts = {
        "notes": index_folder(os.path.join(dd, "notes"), "Notes", "One distilled note per thread or page, newest month first.", True),
        "reports": index_folder(os.path.join(dd, "reports"), "Reports", "Dated trend reports, newest first."),
        "study": index_folder(os.path.join(dd, "study"), "Baseline study", "The history and guide for this beat."),
        "answers": index_folder(os.path.join(dd, "answers"), "Answers", "Questions put to the beat and the answers given, newest first."),
        "sources": index_folder(os.path.join(dd, "sources"), "Sources", "Dated snapshots of rules pages, probes and watch lists."),
    }
    build_ledger_index(cfg)
    top = [f"# {b.title}", "", f"The data folder of the everscout beat `{b.slug}`. Generated by `everscout.py index`.", "",
           "- [HANDOFF](HANDOFF.md): read first; what is unfinished and the next action",
           f"- [notes](notes/INDEX.md): {counts['notes']} distilled notes",
           f"- [reports](reports/INDEX.md): {counts['reports']} trend reports",
           f"- [study](study/INDEX.md): {counts['study']} study chapters",
           f"- [answers](answers/INDEX.md): {counts['answers']} questions put to the beat, with the answers given",
           "- [signals](signals/signals.md): tallies of the vocabulary, with velocity",
           f"- [sources](sources/INDEX.md): {counts['sources']} snapshots",
           "- [log](log.md): one line per scan, report and engagement session",
           "- [journal](journal.md): the person's own reflections (the immersion journal); agents read it, never rewrite it",
           "- [feedback](feedback.md): more of this, less of this; triage reads it every scan", ""]
    write(os.path.join(dd, "INDEX.md"), "\n".join(top))
    for f, text in (("log.md", f"# Log: {b.title}\n\nAppend only, newest last. `## [YYYY-MM-DD] scan|report|engage|beat|ask | summary`.\n"),
                    ("journal.md", f"# Journal: {b.title}\n\nYour own reflections on this beat: hunches, what surprised you, what you want to "
                                   "understand next. Dated entries, newest last. Agents read this before a report and never edit it.\n"),
                    ("feedback.md", f"# Feedback: {b.title}\n\nSteer the scan. One line each, dated. Triage reads this every scan.\n\n"
                                    "## More of this\n\n## Less of this\n\n## Never show\n"),
                    ("HANDOFF.md", f"# HANDOFF: {b.title}\n\nUpdated {today()}. Nothing run yet. Next single action: "
                                   f"`everscout.py fetch --beat {b.slug}` then triage (everscout-scan).\n")):
        if not os.path.exists(os.path.join(dd, f)):
            write(os.path.join(dd, f), text)
    print(f"indexed {dd}: " + ", ".join(f"{k} {v}" for k, v in counts.items()))


def cmd_source_log(a):
    """Record a web page the agent actually read (URL, title, date, what it supports), so reports and the study may cite it."""
    cfg = config()
    b = get_beat(cfg, a.beat)
    p = os.path.join(data_dir(cfg, b.slug), "sources", "web-log.md")
    if not os.path.exists(p):
        write(p, render_frontmatter({"title": f"Web pages read for {b.title}", "kind": "log", "date": today(),
                                     "summary": "every web page an agent read and may cite, appended by everscout.py source-log"})
              + "\n# Web pages read\n\n| read | url | title | supports |\n|---|---|---|---|\n")
    for u in re.findall(r"https?://\S+", read(p)):
        if u.rstrip("|").strip() == a.url:
            print(f"already logged: {a.url}")
            return
    row = f"| {today()} | {a.url} | {(a.title or '').replace('|', '/')} | {(a.supports or '').replace('|', '/')} |\n"
    append(p, row)
    print(f"logged {a.url}")


def cmd_lint(a):
    """Reports and study chapters: every relative link resolves; every external URL is one a note or snapshot holds
    (a URL the model wrote from memory is the classic invented citation); TODOs; stale verified dates."""
    cfg = config()
    b = get_beat(cfg, a.beat)
    dd = data_dir(cfg, b.slug)
    known_urls = set()
    for _, fm, body in all_notes(dd):
        if fm.get("url"):
            known_urls.add(str(fm["url"]).rstrip("/"))
        for u in re.findall(r"https?://[^\s)>\]]+", body):
            known_urls.add(u.rstrip("/.,;"))
    for r, _, fs in os.walk(os.path.join(dd, "sources")) if os.path.isdir(os.path.join(dd, "sources")) else []:
        for f in fs:
            known_urls.update(u.rstrip("/.,;\"'") for u in re.findall(r"https?://[^\s)>\]\"']+", read(os.path.join(r, f))))
    for row in b.sources():
        for u, _, _ in feed_urls(row):
            known_urls.add(u.rstrip("/"))
        if row["source"].startswith("http"):
            known_urls.add(row["source"].rstrip("/"))
    errs, warns, files = [], [], 0
    stale_days = a.stale_days
    for sub in ("reports", "study", "answers"):
        folder = os.path.join(dd, sub)
        if not os.path.isdir(folder):
            continue
        for f in sorted(os.listdir(folder)):
            if not f.endswith(".md") or f == "INDEX.md":
                continue
            files += 1
            p = os.path.join(folder, f)
            text = read(p)
            fm, body = parse_frontmatter(text)
            rel = f"{sub}/{f}"
            for k in ("title", "date", "summary"):
                if not fm.get(k):
                    errs.append(f"{rel}: frontmatter lacks {k}")
            if "TODO" in body:
                errs.append(f"{rel}: TODO left")
            ver = S.parse_time(str(fm.get("verified") or ""))
            if ver and (now_utc() - ver).days > stale_days:
                warns.append(f"{rel}: verified {fm.get('verified')} is older than {stale_days} days")
            for target in re.findall(r"\]\(([^)\s]+)\)", body):
                if target.startswith(("http://", "https://")):
                    if target.rstrip("/.,;") not in known_urls and not a.no_url_check:
                        warns.append(f"{rel}: external link not held by any note or snapshot: {target}")
                    continue
                if target.startswith(("#", "mailto:")):
                    continue
                path = os.path.normpath(os.path.join(folder, urllib.parse.unquote(target.split("#")[0])))
                if not os.path.exists(path):
                    errs.append(f"{rel}: broken link {target}")
    for e in errs:
        print("ERROR  " + e)
    for w in warns:
        print("warn   " + w)
    print(f"{files} report, study and answer files, {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs or (a.strict and warns) else 0)


# ---------------------------------------------------------------- retention and state

def cmd_retention(a):
    cfg = config()
    hours = cfg.get("retention_hours", 48)
    cut = time.time() - hours * 3600
    root = os.path.join(local_root(cfg), "cache")
    removed = 0
    for r, _, fs in os.walk(root) if os.path.isdir(root) else []:
        for f in fs:
            p = os.path.join(r, f)
            if os.path.getmtime(p) < cut:
                os.remove(p)
                removed += 1
    # items caches keep only entries younger than the window, so no raw text outlives it
    for f in os.listdir(os.path.join(local_root(cfg), "cache")) if os.path.isdir(os.path.join(local_root(cfg), "cache")) else []:
        if f.startswith("items-") and f.endswith(".json"):
            p = os.path.join(local_root(cfg), "cache", f)
            items = load_json(p, [])
            keep = [i for i in items if (S.parse_time(i.get("published")) or now_utc()).timestamp() > cut - 14 * 86400]
            for i in keep:
                i["text"] = (i.get("text") or "")[:600]
            save_json(p, keep)
    print(f"removed {removed} cached files older than {hours} hours")


def cmd_state(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    st = load_json(state_path(cfg, b.slug), {})
    dd = data_dir(cfg, b.slug)
    print(json.dumps({"beat": b.slug, "last_fetch": st.get("last_fetch"), "fetches": (st.get("fetches") or [])[-5:],
                      "seen": len(st.get("seen") or {}), "notes": len(all_notes(dd)),
                      "reports": sorted(os.listdir(os.path.join(dd, "reports")))[-3:] if os.path.isdir(os.path.join(dd, "reports")) else []},
                     indent=1))


# ---------------------------------------------------------------- stats (beat metrics)
# Design: ai-docs/research/2026-09-27-beat-statistics.md section 5. The catalog is the beat's
# metrics.md; values are one long-form, append-only CSV per beat at DATA/stats/series.csv.

METRIC_FIELDS = ["id", "question", "definition", "unit", "kind", "source", "method", "cadence", "grade", "status",
                 "version", "created", "reviewed", "archive_reason", "headline", "approved"]
METRIC_METHODS = ("tally", "api", "manual", "derived")
METRIC_STATUSES = ("candidate", "active", "archived")
METRIC_KINDS = ("leading", "lagging")
# Days per cadence period, used for staleness. "per scan" collects weekly periods.
METRIC_CADENCES = {"per scan": 7, "weekly": 7, "monthly": 30, "quarterly": 91, "on release": 365}
ARCHIVE_REASONS = ("stale", "flat", "irrelevant", "gamed", "superseded", "source-gone")
DEFINING_FIELDS = ("definition", "unit", "source", "method")
API_PREFIXES = ("gdelt:", "gdelt-raw:", "wikipedia:")
SERIES_FIELDS = ["date", "metric", "version", "value", "unit", "source", "note_ref"]
# Thresholds are judgment (research note 5.3); override any of them under "stats" in config.json.
STATS_DEFAULTS = {"promote_points": 3, "promote_grade": "C3", "stale_periods": 3, "fail_streak": 3,
                  "flat_cv": 0.05, "flat_points": 8, "trend_points": 8, "backfill_periods": 8, "api_timeout": 60}
METRICS_HEAD = ("# Metrics\n\nThe beat's recurring numbers, one row per metric (format: `kb/SCHEMA.md`, section metrics.md). "
                "Values live in the data folder's `stats/series.csv`. Never delete a row: archive it with a reason.\n\n")


def stats_settings(cfg):
    st = dict(STATS_DEFAULTS)
    st.update(cfg.get("stats") or {})
    return st


def series_path(cfg, slug):
    return os.path.join(data_dir(cfg, slug), "stats", "series.csv")


def load_metrics(b):
    rows = []
    for r in parse_table(b.text("metrics.md")):
        m = {k: (r.get(k) or "").strip() for k in METRIC_FIELDS}
        m["id"] = m["id"].strip("`")
        m["source"] = m["source"].strip("`")
        if m["id"]:
            rows.append(m)
    return rows


def render_metrics_table(rows):
    lines = ["| " + " | ".join(METRIC_FIELDS) + " |", "|" + "---|" * len(METRIC_FIELDS)]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(k, "")).replace("|", "/").replace("\n", " ") for k in METRIC_FIELDS) + " |")
    return "\n".join(lines) + "\n"


def save_metrics(b, rows):
    path = b.file("metrics.md")
    text = b.text("metrics.md")
    table = render_metrics_table(rows)
    if not text.strip():
        write(path, METRICS_HEAD + table)
        return
    lines = text.splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if l.lstrip().startswith("|")), None)
    if start is None:
        write(path, text.rstrip("\n") + "\n\n" + table)
        return
    end = start
    while end < len(lines) and lines[end].lstrip().startswith("|"):
        end += 1
    write(path, "".join(lines[:start]) + table + "".join(lines[end:]))


def load_series(cfg, slug):
    p = series_path(cfg, slug)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def append_series(cfg, slug, rows):
    """Append only: rows are never rewritten or deleted."""
    if not rows:
        return
    p = series_path(cfg, slug)
    new = not os.path.exists(p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, SERIES_FIELDS, lineterminator="\n")
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in SERIES_FIELDS})


def grade_ok(grade, floor="C3"):
    """Admiralty grade (source A-F, information 1-6) at least as good as floor."""
    g, f = re.fullmatch(r"([A-F])([1-6])", grade or ""), re.fullmatch(r"([A-F])([1-6])", floor)
    return bool(g and f and g.group(1) <= f.group(1) and int(g.group(2)) <= int(f.group(2)))


def beat_question_numbers(b):
    sec = re.search(r"^## What we want to learn\s*$(.*?)(?=^## |\Z)", b.body, re.M | re.S)
    return {int(n) for n in re.findall(r"^(\d+)\.\s", sec.group(1) if sec else "", re.M)}


def metric_problems(b, rows):
    """(errors, warnings) for a metrics catalog."""
    errs, warns, seen = [], [], set()
    qnums = beat_question_numbers(b)
    for m in rows:
        i = m["id"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", i):
            errs.append(f"metric {i!r}: id must be a lower-case slug")
        if i in seen:
            errs.append(f"metric {i}: duplicate id (ids are never reused)")
        seen.add(i)
        for k in ("question", "definition", "unit", "source", "method", "cadence", "grade", "status", "version", "created"):
            if not m.get(k):
                errs.append(f"metric {i}: {k} is empty")
        if m["method"] and m["method"] not in METRIC_METHODS:
            errs.append(f"metric {i}: method {m['method']!r} not in {', '.join(METRIC_METHODS)}")
        if m["status"] and m["status"] not in METRIC_STATUSES:
            errs.append(f"metric {i}: status {m['status']!r} not in {', '.join(METRIC_STATUSES)}")
        if m["kind"] and m["kind"] not in METRIC_KINDS:
            errs.append(f"metric {i}: kind {m['kind']!r} not in {', '.join(METRIC_KINDS)}")
        if m["cadence"] and m["cadence"] not in METRIC_CADENCES:
            errs.append(f"metric {i}: cadence {m['cadence']!r} not in {', '.join(METRIC_CADENCES)}")
        if m["grade"] and not re.fullmatch(r"[A-F][1-6]", m["grade"]):
            errs.append(f"metric {i}: grade {m['grade']!r} is not Admiralty (A-F then 1-6, like B2)")
        if m["version"] and not m["version"].isdigit():
            errs.append(f"metric {i}: version must be a whole number")
        src, meth = m["source"], m["method"]
        if meth == "tally" and not re.fullmatch(r"tally:(notes|[a-z0-9_]+/[a-z0-9][a-z0-9.+_-]*)", src):
            errs.append(f"metric {i}: a tally source is tally:notes or tally:<facet>/<entity>")
        if meth == "api" and not src.startswith(API_PREFIXES):
            errs.append(f"metric {i}: an api source starts with one of {', '.join(API_PREFIXES)}")
        if meth == "api" and src.startswith("wikipedia:") and "/" not in src:
            errs.append(f"metric {i}: a wikipedia source is wikipedia:<project>/<Article> (en.wikipedia/Layoff)")
        if meth == "derived" and not re.fullmatch(r"derived:\s*[a-z0-9-]+\s*[-+*/]\s*[a-z0-9-]+", src):
            errs.append(f"metric {i}: a derived source is derived:<id> <op> <id> with op one of + - * /")
        if m.get("approved") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m["approved"]):
            errs.append(f"metric {i}: approved must be empty or an ISO date (the day the user pre-approved promotion)")
        if m.get("approved") and m["status"] == "archived":
            warns.append(f"metric {i}: archived but still pre-approved (clear it with `stats approve --withdraw`)")
        if m["status"] == "archived" and not m["archive_reason"]:
            errs.append(f"metric {i}: archived without an archive_reason")
        qm = re.match(r"Q(\d+)\b", m["question"])
        if qm and qnums and int(qm.group(1)) not in qnums:
            warns.append(f"metric {i}: {qm.group(0)} is not a numbered research question in beat.md")
        if not qm and m["question"]:
            warns.append(f"metric {i}: question should start with the research question number (Q2 ...)")
    if sum(1 for m in rows if m["headline"].lower() == "yes") > 1:
        errs.append("more than one metric has headline yes (at most one per beat)")
    for m in rows:
        if m["method"] == "derived":
            for ref in re.findall(r"[a-z0-9-]+", m["source"].split(":", 1)[-1]):
                if ref not in seen:
                    errs.append(f"metric {m['id']}: derived from unknown metric {ref}")
    return errs, warns


# periods ---------------------------------------------------------------------------

def period_start(d, cadence):
    if cadence in ("weekly", "per scan"):
        return d - dt.timedelta(days=d.weekday())
    if cadence == "monthly":
        return d.replace(day=1)
    if cadence == "quarterly":
        return d.replace(month=(d.month - 1) // 3 * 3 + 1, day=1)
    return d


def next_period(d, cadence):
    if cadence in ("weekly", "per scan"):
        return d + dt.timedelta(days=7)
    if cadence in ("monthly", "quarterly"):
        step = 1 if cadence == "monthly" else 3
        y, mth = d.year + (d.month - 1 + step) // 12, (d.month - 1 + step) % 12 + 1
        return d.replace(year=y, month=mth, day=1)
    return d + dt.timedelta(days=1)


def due_periods(m, series, today_d, backfill):
    """Complete periods after the last collected one for this metric version, newest `backfill` at most."""
    cad = m["cadence"]
    done = {r["date"] for r in series if r["metric"] == m["id"] and r["version"] == m["version"] and r["value"] != ""}
    last_done = max(done) if done else None
    end = period_start(today_d, cad)  # the current period is incomplete
    periods, p = [], end
    for _ in range(max(1, int(backfill))):
        prev = period_start(p - dt.timedelta(days=1), cad)
        if last_done and prev.isoformat() <= last_done:
            break
        periods.insert(0, (prev, p))
        p = prev
    return periods


def bucket(points, periods, how):
    """Aggregate dated points [(YYYY-MM-DD, v)] into {period_start_iso: value} (sum or mean); empty periods are left out."""
    out = {}
    for ps, pe in periods:
        vals = [v for d, v in points if ps.isoformat() <= d < pe.isoformat()]
        if vals:
            out[ps.isoformat()] = round(sum(vals) / len(vals), 4) if how == "mean" else round(sum(vals), 4)
    return out


def agg_for(m):
    u = m["unit"].lower()
    return "mean" if ("share" in u or "%" in u or "index" in u or "rank" in u) else "sum"


# adapters ---------------------------------------------------------------------------

def _stats_get_json(fetch, url, ttl):
    """GET JSON; a body that is not JSON (GDELT answers its rate limit in plain text) is dropped from the cache."""
    text, _, status = fetch.get(url, ttl=ttl, accept="application/json")
    if status in (404, 410):
        raise S.FetchError(url, status, "not found (a renamed article or a dead endpoint)")
    try:
        return json.loads(text) if text.strip() else None
    except ValueError:
        for p in (fetch.cache_path(url), fetch.cache_path(url) + ".json"):
            try:
                os.remove(p)
            except OSError:
                pass
        raise S.FetchError(url, status, "not JSON: " + re.sub(r"\s+", " ", text)[:120])


def collect_tally(cfg, b, m, periods, fetch=None):
    spec = m["source"].split(":", 1)[1].strip()
    notes = []
    for _, fm, _ in all_notes(data_dir(cfg, b.slug)):
        t = S.parse_time(str(fm.get("posted") or fm.get("date") or ""))
        if t:
            notes.append((t.date().isoformat(), fm))
    if not notes:
        return {}
    first = min(d for d, _ in notes)
    share = agg_for(m) == "mean"
    out = {}
    for ps, pe in periods:
        if pe.isoformat() <= first:
            continue  # before the beat's first note: no data, not zero
        inside = [fm for d, fm in notes if ps.isoformat() <= d < pe.isoformat()]
        if spec == "notes":
            out[ps.isoformat()] = len(inside)
            continue
        facet, ent = spec.split("/", 1)
        hits = 0
        for fm in inside:
            vals = fm.get(facet) or []
            hits += ent in ([vals] if isinstance(vals, str) else vals)
        if share:
            if inside:
                out[ps.isoformat()] = round(100.0 * hits / len(inside), 2)
        else:
            out[ps.isoformat()] = hits
    return out


GDELT_HOST = "api.gdeltproject.org"


def collect_gdelt(cfg, b, m, periods, fetch):
    prefix, q = m["source"].split(":", 1)
    start, end = periods[0][0], periods[-1][1] - dt.timedelta(days=1)
    start = max(start, periods[-1][1] - dt.timedelta(days=88))  # the DOC API searches the last three months
    periods = [p for p in periods if p[1] > start]
    if not periods:
        return {}
    url = S.gdelt_timeline_url(q.strip(), raw=prefix == "gdelt-raw", start=start, end=end)
    try:
        data = _stats_get_json(fetch, url, ttl=6 * 3600)
    except S.FetchError as e:
        if e.code == 429 or "limit requests" in str(e):  # a refusal: stay away (kb/platforms.md, GDELT row)
            secs = fetch.set_cooldown(GDELT_HOST, str(e))
            raise S.FetchError(url, e.code, f"refused; GDELT skipped for {secs // 60:.0f} min")
        raise
    fetch.clear_cooldown(GDELT_HOST)
    return bucket(S.parse_gdelt_timeline(data), periods, agg_for(m))


def collect_wikipedia(cfg, b, m, periods, fetch):
    project, article = m["source"].split(":", 1)[1].strip().split("/", 1)
    start, end = periods[0][0], periods[-1][1] - dt.timedelta(days=1)
    url = S.wikimedia_pageviews_url(project, article, start, end)
    return bucket(S.parse_wikimedia_pageviews(_stats_get_json(fetch, url, ttl=6 * 3600)), periods, "sum")


def collect_derived(m, series_rows, metrics_by_id):
    a, op, c = re.fullmatch(r"derived:\s*([a-z0-9-]+)\s*([-+*/])\s*([a-z0-9-]+)", m["source"]).groups()

    def values(mid):
        ver = (metrics_by_id.get(mid) or {}).get("version", "1")
        return {r["date"]: float(r["value"]) for r in series_rows if r["metric"] == mid and r["version"] == ver and r["value"] != ""}
    va, vc = values(a), values(c)
    done = {r["date"] for r in series_rows if r["metric"] == m["id"] and r["version"] == m["version"] and r["value"] != ""}
    out = {}
    for d in sorted(set(va) & set(vc) - done):
        x, y = va[d], vc[d]
        if op == "/" and y == 0:
            continue
        out[d] = round({"+": x + y, "-": x - y, "*": x * y, "/": x / y if y else 0}[op], 4)
    return out


def metric_adapter(m):
    if m["method"] == "tally":
        return collect_tally
    if m["method"] == "api":
        return collect_wikipedia if m["source"].startswith("wikipedia:") else collect_gdelt
    return None


def fmt_num(v):
    return str(int(v)) if float(v).is_integer() else str(v)


def stats_collect(cfg, b, metrics, only=None, today_d=None, fetch=None, backfill=None):
    """Collect due values for candidate and active metrics. Returns (rows appended, report lines)."""
    st = stats_settings(cfg)
    today_d = today_d or now_utc().date()
    series = load_series(cfg, b.slug)
    if fetch is None:
        fetch = fetcher(cfg)
    fetch.timeout = float(st["api_timeout"])
    fetch.retry = False  # a refused metric is recorded as a gap and tried at the next collect
    appended, report = [], []
    live = [m for m in metrics if m["status"] in ("candidate", "active") and (not only or m["id"] in only)]
    for m in sorted(live, key=lambda m: m["method"] == "derived"):
        base = {"metric": m["id"], "version": m["version"], "unit": m["unit"], "source": m["source"]}
        if m["method"] == "manual" or m["cadence"] == "on release" and m["method"] != "derived":
            report.append(f"  skip    {m['id']}: {m['method']}, add values with `stats collect --metric {m['id']} --value N`")
            continue
        if m["method"] == "derived":
            vals = collect_derived(m, series + appended, {x["id"]: x for x in metrics})
            rows = [dict(base, date=d, value=fmt_num(v), note_ref="derived") for d, v in sorted(vals.items())]
        else:
            periods = due_periods(m, series + appended, today_d, backfill or st["backfill_periods"])
            if not periods:
                report.append(f"  current {m['id']}")
                continue
            cd = fetch.cooldown(GDELT_HOST) if m["source"].startswith(("gdelt:", "gdelt-raw:")) else None
            if cd:
                until = dt.datetime.fromtimestamp(cd[0], dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
                report.append(f"  cooling {m['id']}: GDELT refused earlier; next try after {until}")
                continue
            try:
                vals = metric_adapter(m)(cfg, b, m, periods, fetch)
                rows = [dict(base, date=d, value=fmt_num(v), note_ref="") for d, v in sorted(vals.items())]
            except Exception as e:  # network, timeout, block page, bad JSON: record the gap, never crash the scan
                reason = re.sub(r"[\r\n,]+", " ", str(e))[:160]
                rows = [dict(base, date=periods[-1][0].isoformat(), value="", note_ref=f"failed: {reason}")]
        appended.extend(rows)
        ok = [r for r in rows if r["value"] != ""]
        if ok:
            report.append(f"  ok      {m['id']}: {len(ok)} value(s), latest {ok[-1]['date']} = {ok[-1]['value']} {m['unit']}")
        elif rows:
            report.append(f"  FAILED  {m['id']}: {rows[0]['note_ref']}")
        else:
            report.append(f"  empty   {m['id']}: no data for the due periods")
    append_series(cfg, b.slug, appended)
    return appended, report


# review ---------------------------------------------------------------------------

def _slope(vals):
    n = len(vals)
    if n < 2:
        return 0.0
    mx, my = (n - 1) / 2, sum(vals) / n
    den = sum((i - mx) ** 2 for i in range(n))
    return sum((i - mx) * (v - my) for i, v in enumerate(vals)) / den if den else 0.0


def _pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if not sx or not sy:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def review_metrics(metrics, series, st, today_d):
    """Findings per live metric: {'id', 'action' (promote|archive|keep), 'reason', 'detail', 'trend'}. Nothing is changed here."""
    out = []
    for m in metrics:
        if m["status"] == "archived":
            continue
        rows = sorted((r for r in series if r["metric"] == m["id"] and r["version"] == m["version"]), key=lambda r: r["date"])
        vals = [float(r["value"]) for r in rows if r["value"] != ""]
        per = METRIC_CADENCES.get(m["cadence"], 30)
        f = {"id": m["id"], "action": "keep", "reason": "", "detail": f"{len(vals)} point(s)", "trend": ""}
        failed_periods = set()  # several failed attempts on one period (a busy API retried the same day) count once
        for r in reversed(rows):
            if r["value"] != "":
                break
            failed_periods.add(r["date"])
        streak = len(failed_periods)
        last_ok = max((r["date"] for r in rows if r["value"] != ""), default=None)
        since = last_ok or m.get("created") or ""
        age = (today_d - dt.date.fromisoformat(since[:10])).days if re.match(r"\d{4}-\d{2}-\d{2}", since) else 0
        # a period's value is dated at its start, so allow one period for it to complete
        stale_after = (int(st["stale_periods"]) + 1) * per
        if streak >= int(st["fail_streak"]):
            f.update(action="archive", reason="stale", detail=f"the source failed for {streak} periods in a row")
        elif m["method"] != "manual" and age > stale_after:
            f.update(action="archive", reason="stale", detail=f"no new value for {age} days ({st['stale_periods']} {m['cadence']} periods)")
        elif m["method"] == "manual" and age > stale_after:
            f.update(action="archive", reason="stale", detail=f"no value entered for {age} days")
        elif len(vals) >= int(st["flat_points"]):
            last = vals[-int(st["flat_points"]):]
            mean = sum(last) / len(last)
            sd = math.sqrt(sum((v - mean) ** 2 for v in last) / len(last))
            cv = sd / abs(mean) if mean else (0.0 if sd == 0 else float("inf"))
            if cv < float(st["flat_cv"]):
                f.update(action="archive", reason="flat", detail=f"coefficient of variation {cv:.3f} over the last {len(last)} points "
                         "(archive unless a research question depends on its level)")
        if f["action"] == "keep" and m["status"] == "candidate":
            if len(vals) >= int(st["promote_points"]) and grade_ok(m["grade"], st["promote_grade"]):
                f.update(action="promote", reason="ready", detail=f"{len(vals)} points, grade {m['grade']}: ask the user before promoting")
            elif not grade_ok(m["grade"], st["promote_grade"]):
                f["detail"] += f"; grade {m['grade']} is below {st['promote_grade']}, cannot be promoted"
            if m.get("approved"):
                f["detail"] += f"; pre-approved {m['approved']}"
        tp = vals[-int(st["trend_points"]):]
        if len(tp) >= 3:
            mean = sum(tp) / len(tp)
            s = _slope(tp)
            rel = s / abs(mean) if mean else 0.0
            f["trend"] = ("rising" if rel > 0.05 else "falling" if rel < -0.05 else "level") + f" (slope {s:+.3g} per period over {len(tp)})"
        out.append(f)
    by_q = {}
    for m in metrics:
        if m["status"] != "archived":
            by_q.setdefault(m["question"].split()[0] if m["question"] else "", []).append(m)
    pairs = []
    for q, ms in by_q.items():
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                a_, c_ = ms[i], ms[j]
                va = {r["date"]: float(r["value"]) for r in series if r["metric"] == a_["id"] and r["version"] == a_["version"] and r["value"] != ""}
                vc = {r["date"]: float(r["value"]) for r in series if r["metric"] == c_["id"] and r["version"] == c_["version"] and r["value"] != ""}
                common = sorted(set(va) & set(vc))
                r = _pearson([va[d] for d in common], [vc[d] for d in common])
                if r is not None:
                    pairs.append((q, a_["id"], c_["id"], round(r, 2), len(common)))
    return out, pairs


def auto_promote(cfg, b, metrics, today_d=None):
    """Promote pre-approved candidates that meet the normal rule. Changes `metrics` in place; returns the change lines."""
    today_d = today_d or now_utc().date()
    by = {m["id"]: m for m in metrics}
    findings, _ = review_metrics(metrics, load_series(cfg, b.slug), stats_settings(cfg), today_d)
    changes = []
    for f in findings:
        m = by[f["id"]]
        if f["action"] == "promote" and m["status"] == "candidate" and m.get("approved"):
            m["status"] = "active"
            m["reviewed"] = today_d.isoformat()
            changes.append(f"promoted {m['id']} (pre-approved {m['approved']})")
    return changes


# commands ---------------------------------------------------------------------------

def _stats_beat(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    return cfg, b


def _stats_log(cfg, b, text):
    append(os.path.join(data_dir(cfg, b.slug), "log.md"), f"\n## [{today()}] stats | {text}\n")


def _builtin_warning(b):
    if os.path.abspath(b.path).startswith(os.path.abspath(os.path.join(ROOT, "beats"))):
        note(f"note: {b.slug} is a built-in beat; its metrics.md is part of the plugin. Copy the beat into your private beat dir "
             "(`everscout.py where`) before editing it for yourself.")


def cmd_stats_list(a):
    cfg, b = _stats_beat(a)
    metrics = load_metrics(b)
    series = load_series(cfg, b.slug)
    out = []
    for m in metrics:
        rows = [r for r in series if r["metric"] == m["id"]]
        ok = sorted((r for r in rows if r["value"] != "" and r["version"] == m["version"]), key=lambda r: r["date"])
        out.append(dict(m, points=len(ok), last_date=ok[-1]["date"] if ok else "", last_value=ok[-1]["value"] if ok else "",
                        rows_all_versions=len(rows)))
    if a.status:
        out = [m for m in out if m["status"] in a.status.split(",")]
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return
    if not out:
        print(f"{b.slug}: no metrics (add one with `stats add`; format in kb/SCHEMA.md)")
        return
    print(f"{b.slug}: {len(out)} metrics; series at {series_path(cfg, b.slug)}")
    for m in out:
        star = " *" if m["headline"].lower() == "yes" else ""
        last = f"{m['last_value']} {m['unit']} ({m['last_date']})" if m["points"] else "no values yet"
        print(f"  {m['status']:<9} {m['id']}{star} v{m['version']}  {m['method']}:{m['cadence']}  {m['grade']}  {m['points']} pts  last {last}"
              + (f"  [{m['archive_reason']}]" if m["status"] == "archived" else ""))


def cmd_stats_add(a):
    cfg, b = _stats_beat(a)
    metrics = load_metrics(b)
    by = {m["id"]: m for m in metrics}
    given = {k: getattr(a, k) for k in ("question", "definition", "unit", "kind", "source", "method", "cadence", "grade", "status")
             if getattr(a, k) is not None}
    if a.headline is not None:
        given["headline"] = "yes" if a.headline == "yes" else ""
    if a.id in by:
        m = by[a.id]
        if m["status"] == "archived" and given.get("status") not in (None, "archived"):
            given.setdefault("archive_reason", "")
        changed = [k for k in DEFINING_FIELDS if k in given and given[k] != m[k]]
        m.update(given)
        if changed:
            m["version"] = str(int(m["version"] or 1) + 1)
        m["reviewed"] = today()
        what = f"updated {a.id}" + (f", {', '.join(changed)} changed: version {m['version']}" if changed else "")
    else:
        m = {k: "" for k in METRIC_FIELDS}
        m.update(id=a.id, status="candidate", version="1", created=today(), reviewed=today(), kind="leading")
        m.update(given)
        metrics.append(m)
        what = f"added candidate {a.id} ({m['method']}, {m['source']})"
    if m.get("headline") == "yes":
        for x in metrics:
            if x is not m and x["headline"] == "yes":
                x["headline"] = ""
                note(f"headline moved from {x['id']} to {m['id']}")
    errs, warns = metric_problems(b, metrics)
    mine = [e for e in errs if e.startswith(f"metric {a.id}") or "headline" in e]
    if mine:
        fail("not saved: " + "; ".join(mine))
    _builtin_warning(b)
    save_metrics(b, metrics)
    _stats_log(cfg, b, what)
    for w in warns:
        if w.startswith(f"metric {a.id}"):
            note("warn: " + w)
    print(what)


def cmd_stats_collect(a):
    cfg, b = _stats_beat(a)
    metrics = load_metrics(b)
    only = set(a.metric.split(",")) if a.metric else None
    if a.value is not None:
        if not only or len(only) != 1:
            fail("--value needs exactly one --metric")
        mid = next(iter(only))
        m = next((x for x in metrics if x["id"] == mid), None)
        if not m:
            fail(f"no metric {mid} in {b.slug}")
        d = a.date or period_start(now_utc().date(), m["cadence"]).isoformat()
        append_series(cfg, b.slug, [{"date": d, "metric": mid, "version": m["version"], "value": a.value, "unit": m["unit"],
                                     "source": m["source"], "note_ref": a.note_ref or "manual"}])
        print(f"{mid}: {d} = {a.value} {m['unit']}")
        return
    today_d = dt.date.fromisoformat(a.date) if a.date else None
    rows, report = stats_collect(cfg, b, metrics, only=only, today_d=today_d, backfill=a.backfill)
    ok = sum(1 for r in rows if r["value"] != "")
    print(f"{b.slug}: {ok} value(s) and {len(rows) - ok} failure(s) appended to {series_path(cfg, b.slug)}")
    for line in report:
        print(line)
    if rows:
        _stats_log(cfg, b, f"collected {ok} value(s), {len(rows) - ok} failed")
    promoted = auto_promote(cfg, b, metrics, today_d)
    if promoted:
        save_metrics(b, metrics)
        for c in promoted:
            print(c)
            _stats_log(cfg, b, c)


def cmd_stats_approve(a):
    cfg, b = _stats_beat(a)
    metrics = load_metrics(b)
    m = next((x for x in metrics if x["id"] == a.metric), None)
    if not m:
        fail(f"no metric {a.metric} in {b.slug}")
    if a.withdraw:
        if not m.get("approved"):
            fail(f"{a.metric} is not pre-approved")
        m["approved"] = ""
        what = f"withdrew pre-approval of {a.metric}"
    else:
        if m["status"] != "candidate":
            fail(f"{a.metric} is {m['status']}, not a candidate")
        m["approved"] = a.date or today()
        what = f"pre-approved {a.metric}: promoted automatically once it meets the promotion rule"
    _builtin_warning(b)
    save_metrics(b, metrics)
    _stats_log(cfg, b, what)
    print(what)
    if not a.withdraw:
        promoted = auto_promote(cfg, b, metrics)
        if promoted:
            save_metrics(b, metrics)
            for c in promoted:
                print(c)
                _stats_log(cfg, b, c)


def cmd_stats_review(a):
    cfg, b = _stats_beat(a)
    st = stats_settings(cfg)
    metrics = load_metrics(b)
    by = {m["id"]: m for m in metrics}
    today_d = dt.date.fromisoformat(a.date) if a.date else now_utc().date()
    changes = []
    for mid in (a.promote.split(",") if a.promote else []):
        if mid not in by:
            fail(f"no metric {mid}")
        findings, _ = review_metrics([by[mid]], load_series(cfg, b.slug), st, today_d)
        if by[mid]["status"] != "candidate":
            fail(f"{mid} is {by[mid]['status']}, not a candidate")
        if not (findings and findings[0]["action"] == "promote") and not a.force:
            fail(f"{mid} does not meet the promotion rule ({st['promote_points']} points at {st['promote_grade']} or better): "
                 f"{findings[0]['detail'] if findings else ''}; --force overrides")
        by[mid]["status"] = "active"
        changes.append(f"promoted {mid} to active (user yes)")
    if a.archive:
        if not a.reason:
            fail("--archive needs --reason (" + ", ".join(ARCHIVE_REASONS) + ", superseded-by:<id>, or free text)")
        for mid in a.archive.split(","):
            if mid not in by:
                fail(f"no metric {mid}")
            by[mid].update(status="archived", archive_reason=a.reason)
            changes.append(f"archived {mid}: {a.reason}")
    for mid in (a.reactivate.split(",") if a.reactivate else []):
        if mid not in by or by[mid]["status"] != "archived":
            fail(f"{mid} is not archived")
        by[mid].update(status="active", archive_reason="")
        changes.append(f"reactivated {mid}")
    changes += auto_promote(cfg, b, metrics, today_d)
    findings, pairs = review_metrics(metrics, load_series(cfg, b.slug), st, today_d)
    if a.apply:
        for f in findings:
            if f["action"] == "archive" and by[f["id"]]["status"] != "archived":
                by[f["id"]].update(status="archived", archive_reason=f"{f['reason']}: {f['detail']}")
                changes.append(f"archived {f['id']}: {f['reason']} ({f['detail']})")
        for m in metrics:
            m["reviewed"] = today_d.isoformat()
    if a.json:
        print(json.dumps({"findings": findings, "pairs": [dict(zip(("question", "a", "b", "r", "n"), p)) for p in pairs],
                          "changes": changes}, indent=1))
    else:
        print(f"{b.slug}: review of {len(findings)} live metric(s) on {today_d.isoformat()}")
        for f in findings:
            print(f"  {f['action']:<8} {f['id']}: {f['reason'] + ', ' if f['reason'] else ''}{f['detail']}"
                  + (f"; trend {f['trend']}" if f["trend"] else ""))
        for q, x, y, r, n in pairs:
            print(f"  pair    {q}: {x} and {y} move {'together' if r > 0.5 else 'apart' if r < -0.5 else 'independently'} (r={r}, {n} common points)")
        for c in changes:
            print("  " + c)
        if not a.apply and any(f["action"] == "archive" for f in findings):
            print("  (proposals only; --apply archives stale and flat metrics and stamps reviewed)")
    if changes or a.apply:
        _builtin_warning(b)
        save_metrics(b, metrics)
        for c in changes:
            _stats_log(cfg, b, c)


def find_chartwright(cfg):
    """Path to chartwright's cw.py, or None. Optional: everscout never needs it."""
    cands = [os.environ.get("EVERSCOUT_CHARTWRIGHT") or "", cfg.get("chartwright") or "",
             os.path.join(os.path.dirname(ROOT), "chartwright", "scripts", "cw.py")]
    for base in (os.path.expanduser("~/.claude/plugins/cache"), os.path.expanduser("~/.claude/plugins/marketplaces")):
        if os.path.isdir(base):
            cands += sorted(glob.glob(os.path.join(base, "*", "chartwright", "*", "scripts", "cw.py")), reverse=True)
            cands += glob.glob(os.path.join(base, "chartwright", "scripts", "cw.py"))
    for c in cands:
        if c and os.path.isfile(expand(c)):
            return expand(c)
    return None


def chart_commands(cw, csv_path, charts_dir, slug, title):
    """(name, argv) for the three chartwright builds: a line chart, terminal sparklines, small multiples."""
    base = [sys.executable, cw, "build", "--data", csv_path, "--x", "date", "--y", "value", "--series", "series", "--agg", "mean"]
    return [
        ("line", base + ["--chart", "line", "--target", "vega-lite", "--html", "--title", title + ": metrics",
                         "--out", os.path.join(charts_dir, slug + "-metrics-line.html")]),
        ("sparkline", base + ["--chart", "sparkline", "--target", "terminal", "--out", os.path.join(charts_dir, slug + "-sparklines.txt")]),
        ("small-multiples", base + ["--chart", "small-multiples", "--target", "vega-lite", "--html", "--title", title + ": by metric",
                                    "--out", os.path.join(charts_dir, slug + "-small-multiples.html")]),
    ]


def show_argv(argv):
    return " ".join('"' + x + '"' if (" " in x or not x) else x for x in ["python"] + argv[1:])


def cmd_stats_export(a):
    cfg, b = _stats_beat(a)
    metrics = {m["id"]: m for m in load_metrics(b)}
    want = set(a.metric.split(",")) if a.metric else None
    rows = []
    for r in load_series(cfg, b.slug):
        m = metrics.get(r["metric"])
        if r["value"] == "" or (want and r["metric"] not in want) or (a.since and r["date"] < a.since):
            continue
        if not want and m and m["status"] == "archived" and not a.include_archived:
            continue
        rows.append(r)
    versions = {}
    for r in rows:
        versions.setdefault(r["metric"], set()).add(r["version"])
    dd = data_dir(cfg, b.slug)
    out = expand(a.out) if a.out else os.path.join(dd, "stats", "export.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "metric", "series", "value", "unit", "version", "status"])
        for r in sorted(rows, key=lambda r: (r["metric"], r["version"], r["date"])):
            # a definition change starts a new series, so a break is never drawn as a trend
            cur = (metrics.get(r["metric"]) or {}).get("version")
            series = r["metric"] if versions[r["metric"]] == {cur} else f"{r['metric']} v{r['version']}"
            w.writerow([r["date"], r["metric"], series, r["value"], r["unit"], r["version"],
                        (metrics.get(r["metric"]) or {}).get("status", "unknown")])
    print(f"{len(rows)} rows from {len(versions)} metric(s) written to {out} (long form: date, series, value)")
    charts_dir = os.path.join(dd, "reports", "charts")
    cw = find_chartwright(cfg)
    if not cw:
        print("chartwright not found (set EVERSCOUT_CHARTWRIGHT or config `chartwright` to its scripts/cw.py); the CSV works in any chart tool")
        return
    cmds = chart_commands(cw, out, charts_dir, b.slug, b.title)
    if not a.charts:
        print(f"chartwright found: {cw}. Build charts into {charts_dir} with --charts, or run:")
        for name, c in cmds:
            print(f"  {name}: {show_argv(c)}")
        return
    if not rows:
        print("no rows: no charts built")
        return
    os.makedirs(charts_dir, exist_ok=True)
    for name, argv in cmds:
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=120)
            print(f"  {name}: {'ok' if r.returncode == 0 else 'failed ' + str(r.returncode)} {(r.stderr or r.stdout).strip()[:200]}")
        except Exception as e:
            print(f"  {name}: failed ({e})")


def cmd_stats(a):
    {"list": cmd_stats_list, "add": cmd_stats_add, "collect": cmd_stats_collect, "review": cmd_stats_review,
     "approve": cmd_stats_approve, "export": cmd_stats_export}[a.action](a)


# ---------------------------------------------------------------- literature (books on the beat)
# literature.md in the beat folder: three tiers of books (canon, recent, latest) and the Open Library searches that find
# new ones. A book provided by the user is read with readwright into DATA/books/<slug>/, distilled into learnings.md
# (principles cited by chapter, changes aimed at the beat's files and the units it feeds), then into a `book` note.

LIT_TIERS = ("canon", "recent", "latest")
LIT_STATUSES = ("lead", "have", "reading", "read", "distilled", "skip")
LIT_COLUMNS = ["title", "authors", "year", "id", "why", "evidence", "status"]
LIT_RECHECK_DAYS = {"canon": 365, "recent": 90, "latest": 30}  # a tier whose checked date is older is due for research
LIT_RECENT_YEARS = 5  # recent: published within this many years of the tier's checked date
LIT_LATEST_MONTHS = 18
LIT_MAX_QUOTE_WORDS = 25  # learnings paraphrase; a quoted run longer than this fails lint (copyright, kb/literature.md)
LIT_CITE = re.compile(r"\((?:[^()]*?)(?:ch\.|chap|chapter|p\.|pp\.|part|sec\.|section|§|loc\.|appendix|intro)[^()]*\)", re.I)
LIT_TARGET_BEAT_FILES = ("beat.md", "sources.md", "vocab.md", "questions.md", "searches.md", "study.md", "metrics.md", "literature.md")


def lit_path(b):
    return b.file("literature.md")


def lit_sections(text):
    """{heading lower: body} for the `## ` sections of a markdown body."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = line[3:].strip().lower(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def lit_load(b):
    """(meta, {tier: [row]}, [search row]) from literature.md; empty when the beat has none."""
    text = b.text("literature.md")
    meta, body = parse_frontmatter(text)
    secs = lit_sections(body)
    tiers = {}
    for t in LIT_TIERS:
        rows = []
        for r in parse_table(secs.get(t, "")):
            r = {k: (r.get(k) or "").strip() for k in LIT_COLUMNS}
            if r["title"]:
                r["status"] = (r["status"] or "lead").split()[0].lower()
                rows.append(r)
        tiers[t] = rows
    searches = [r for r in parse_table(secs.get("searches", "")) if (r.get("query") or "").strip()]
    for r in searches:
        r["query"] = r["query"].strip().strip("`")
    return meta, tiers, searches


def lit_render(b, meta, tiers, searches):
    """literature.md text, keeping the file's prose sections (anything that is not a tier or Searches) in place."""
    old = b.text("literature.md")
    _, body = parse_frontmatter(old)
    head = body.split("\n## ", 1)[0].rstrip() if body else f"# Literature: {b.title}"
    secs = lit_sections(body)
    out = [render_frontmatter(meta) + "\n" + head + "\n"]
    names = {"canon": "Canon", "recent": "Recent", "latest": "Latest"}
    for t in LIT_TIERS:
        intro = re.split(r"\n\s*\|", "\n" + secs.get(t, ""), maxsplit=1)[0].strip()
        out.append(f"## {names[t]}\n\n" + (intro + "\n\n" if intro else "") + "| " + " | ".join(LIT_COLUMNS) + " |\n|"
                   + "---|" * len(LIT_COLUMNS) + "\n"
                   + "".join("| " + " | ".join(r.get(k, "").replace("|", "/") for k in LIT_COLUMNS) + " |\n" for r in tiers[t]))
    intro = re.split(r"\n\s*\|", "\n" + secs.get("searches", ""), maxsplit=1)[0].strip()
    out.append("## Searches\n\n" + (intro + "\n\n" if intro else "") + "| query | notes |\n|---|---|\n"
               + "".join(f"| `{r['query']}` | {r.get('notes', '')} |\n" for r in searches))
    for name, text in secs.items():
        if name not in LIT_TIERS and name != "searches":
            out.append(f"## {name[:1].upper() + name[1:]}\n{text.rstrip()}\n")
    return "\n".join(out)


def lit_norm_title(t):
    t = re.sub(r"[*_`]", "", t or "").lower().split(":")[0]
    t = re.sub(r"\([^)]*\)", " ", t)  # "(3rd ed.)", "(series)" are not in file names
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def lit_find(tiers, ref):
    """(tier, row) whose id or title matches ref, else (None, None)."""
    key = lit_norm_title(ref)
    for t in LIT_TIERS:
        for r in tiers[t]:
            if (ref and r["id"] and r["id"].lower() == ref.lower()) or (key and lit_norm_title(r["title"]) == key):
                return t, r
    return None, None


def lit_problems(b, meta, tiers, searches, today_d=None):
    """(errors, warnings) for literature.md."""
    today_d = today_d or dt.date.today()
    errs, warns = [], []
    seen = {}
    for t in LIT_TIERS:
        checked = str(meta.get(t + "_checked") or meta.get("checked") or "")
        try:
            cd = dt.date.fromisoformat(checked[:10])
        except ValueError:
            cd = None
            if checked == "never":
                warns.append(f"{t} tier never researched (kb/literature.md)")
            else:
                errs.append(f"literature.md frontmatter lacks a date in {t}_checked (or checked)")
        if cd and (today_d - cd).days > LIT_RECHECK_DAYS[t]:
            warns.append(f"{t} tier last checked {cd}, over {LIT_RECHECK_DAYS[t]} days ago: due for research (lit due)")
        for r in tiers[t]:
            name = r["title"][:60]
            k = r["id"].lower() if r["id"] not in ("", "-") else lit_norm_title(r["title"])
            if k in seen:
                errs.append(f"{name}: listed twice ({seen[k]} and {t})")
            seen[k] = t
            if r["status"] not in LIT_STATUSES:
                errs.append(f"{name}: status {r['status']!r} not in {', '.join(LIT_STATUSES)}")
            if not re.match(r"https?://", r["evidence"]):
                errs.append(f"{name}: evidence must be a URL that was fetched or seen in search results")
            if r["id"] and r["id"] != "-" and not re.fullmatch(r"OL\d+W|isbn:\d{9}[\dX]|isbn:\d{13}", r["id"]):
                errs.append(f"{name}: id {r['id']!r} is not an Open Library work key (OL...W) or isbn:<number>")
            if not r["why"]:
                warns.append(f"{name}: no why")
            y = re.match(r"\d{4}", r["year"])
            if not y:
                warns.append(f"{name}: no year")
            elif cd and t == "recent" and int(y.group()) < cd.year - LIT_RECENT_YEARS:
                warns.append(f"{name}: {y.group()} is older than the recent window ({LIT_RECENT_YEARS} years); canon?")
            elif cd and t == "latest" and int(y.group()) < (cd - dt.timedelta(days=LIT_LATEST_MONTHS * 31)).year:
                warns.append(f"{name}: {y.group()} is older than the latest window ({LIT_LATEST_MONTHS} months)")
    if not tiers["canon"]:
        warns.append("no canon books")
    if not searches:
        warns.append("no Open Library searches: `lit new` has nothing to run")
    return errs, warns


def cmd_lit_list(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    if not os.path.exists(lit_path(b)):
        fail(f"{b.slug} has no literature.md yet; copy beats/_template/literature.md and follow kb/literature.md")
    meta, tiers, searches = lit_load(b)
    if a.json:
        print(json.dumps({"beat": b.slug, "meta": meta, "tiers": tiers, "searches": searches}, indent=1))
        return
    for t in LIT_TIERS:
        rows = [r for r in tiers[t] if not a.status or r["status"] == a.status]
        if a.tier and t != a.tier:
            continue
        print(f"{t} ({len(rows)}; checked {meta.get(t + '_checked') or meta.get('checked') or 'never'})")
        for r in rows:
            print(f"  [{r['status']:<9}] {r['title'][:70]} - {r['authors'][:40]} ({r['year']}) {r['id']}")
    print(f"{len(searches)} searches")


def cmd_lit_check(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    if not os.path.exists(lit_path(b)):
        fail(f"{b.slug} has no literature.md")
    errs, warns = lit_problems(b, *lit_load(b))
    for e in errs:
        print("ERROR  " + e)
    for w in warns:
        print("warn   " + w)
    _, tiers, _ = lit_load(b)
    print(f"{b.slug}: " + ", ".join(f"{len(tiers[t])} {t}" for t in LIT_TIERS) + f"; {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs or (a.strict and warns) else 0)


def cmd_lit_add(a):
    """Add a book to a tier, or update one already listed (matched by id, then title): status, tier, fields."""
    cfg = config()
    b = get_beat(cfg, a.beat)
    if not os.path.exists(lit_path(b)):
        shutil.copy(os.path.join(ROOT, "beats", "_template", "literature.md"), lit_path(b))
    meta, tiers, searches = lit_load(b)
    t, r = lit_find(tiers, a.id or a.title)
    if r is None:
        if not (a.title and a.tier):
            fail("a new book needs --title and --tier")
        r = {k: "" for k in LIT_COLUMNS}
        r["status"] = "lead"
        tiers[a.tier].append(r)
        t, verb = a.tier, "added"
    else:
        verb = "updated"
        if a.tier and a.tier != t:
            tiers[t].remove(r)
            tiers[a.tier].append(r)
            t = a.tier
    for k in ("title", "authors", "year", "id", "why", "evidence", "status"):
        v = getattr(a, k, None)
        if v is not None:
            r[k] = str(v)
    if a.status and a.status not in LIT_STATUSES:
        fail(f"status must be one of {', '.join(LIT_STATUSES)}")
    write(lit_path(b), lit_render(b, meta, tiers, searches))
    print(f"{verb} {t}: {r['title']} [{r['status']}]")


def lit_clean_query(query):
    """A query as Open Library takes it: a pasted `q=` and URL encoding undone, fixed year ranges dropped (--since-year sets the window)."""
    q = re.sub(r"^q=\s*", "", query.strip())
    if re.search(r"%[0-9A-Fa-f]{2}", q):
        q = urllib.parse.unquote_plus(q)
    q = re.sub(r"\s*\bfirst_publish_year:\[[^\]]*\]", "", q)
    return q.strip()


def lit_search(cfg, query, fetch=None, limit=40, force=False):
    fetch = fetch or fetcher(cfg)
    query = lit_clean_query(query)
    url = S.openlibrary_search_url(query, sort="new", limit=limit)
    text, _, status = fetch.get(url, ttl=86400, force=force, accept="application/json")
    try:
        return S.parse_openlibrary(json.loads(text) if text.strip() else {}, url)
    except ValueError:
        raise S.FetchError(url, status, "not JSON: " + re.sub(r"\s+", " ", text)[:120])


def cmd_lit_new(a):
    """Recent books from the beat's Open Library searches that literature.md does not list yet: candidates for Latest."""
    cfg = config()
    b = get_beat(cfg, a.beat)
    meta, tiers, searches = lit_load(b)
    if not searches:
        fail(f"{b.slug}: literature.md has no searches (a `## Searches` table with a query column)")
    since = a.since_year or dt.date.today().year - 1
    seen = {}
    for s in searches:
        try:
            books = lit_search(cfg, s["query"], limit=a.per_search, force=a.force)
        except S.FetchError as e:
            note(f"search failed: {s['query']}: {e}")
            continue
        for bk in books:
            if (bk["year"] or 0) < since or (a.language and a.language != "any" and bk["languages"] and a.language not in bk["languages"]):
                continue
            if lit_find(tiers, bk["id"])[1] or lit_find(tiers, bk["title"])[1]:
                continue
            got = seen.setdefault(bk["id"], dict(bk, queries=[]))
            got["queries"].append(s["query"])
    found = sorted(seen.values(), key=lambda x: (len(x["queries"]), x["editions"], x["publish_date"]), reverse=True)[:a.limit]
    if a.json:
        print(json.dumps({"beat": b.slug, "since_year": since, "candidates": found}, indent=1))
        return
    print(f"{b.slug}: {len(found)} books from {since} on, not yet listed ({len(searches)} searches)")
    for bk in found:
        print(f"{bk['id']:<14} {bk['year']} {bk['title'][:70]} - {', '.join(bk['authors'])[:40]}"
              f" ({bk['publisher'][:30]}; {len(bk['queries'])} searches) {bk['url']}")


def lit_due(meta, today_d=None):
    today_d = today_d or dt.date.today()
    out = []
    for t in LIT_TIERS:
        c = str(meta.get(t + "_checked") or meta.get("checked") or "")
        try:
            age = (today_d - dt.date.fromisoformat(c[:10])).days
        except ValueError:
            age = None
        if age is None or age > LIT_RECHECK_DAYS[t]:
            out.append((t, c or "never"))
    return out


def cmd_lit_due(a):
    """Which tiers of which beats are due for literature research (exit 2 when any is)."""
    cfg = config()
    any_due = False
    for slug, path in all_beats(cfg).items():
        if a.beat and slug != a.beat:
            continue
        b = Beat(slug, path)
        if not os.path.exists(lit_path(b)):
            print(f"{slug}: no literature.md")
            any_due = True
            continue
        meta, _, _ = lit_load(b)
        due = lit_due(meta)
        any_due |= bool(due)
        print(f"{slug}: " + ("; ".join(f"{t} due (checked {c})" for t, c in due) if due else "current"))
    sys.exit(2 if any_due else 0)


def main_checkout(root):
    """The main clone of a git worktree at root (a worktree under _wt/ has no sibling clones), else root."""
    try:
        p = subprocess.run(["git", "-C", root, "rev-parse", "--path-format=absolute", "--git-common-dir"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return root
    common = p.stdout.strip()
    return os.path.dirname(os.path.normpath(common)) if p.returncode == 0 and common else root


def find_readwright(cfg):
    """Path to readwright's rw.py, or None: $EVERSCOUT_READWRIGHT, config readwright, a sibling clone, the plugin cache."""
    tail = os.path.join("skills", "readwright", "scripts", "rw.py")
    cands = [os.environ.get("EVERSCOUT_READWRIGHT") or "", cfg.get("readwright") or ""]
    cands += [os.path.join(os.path.dirname(r), "readwright", tail) for r in dict.fromkeys([ROOT, main_checkout(ROOT)])]
    root = claude_plugins_dir()
    cands += sorted(glob.glob(os.path.join(root, "cache", "*", "readwright", "*", tail)), key=_version_key, reverse=True)
    cands += glob.glob(os.path.join(root, "marketplaces", "*", tail)) + glob.glob(os.path.join(root, "marketplaces", "*", "readwright", tail))
    for c in cands:
        if c and os.path.isfile(expand(c)):
            return expand(c)
    return None


def books_dir(cfg, slug):
    return os.path.join(data_dir(cfg, slug), "books")


LEARNINGS_TEMPLATE = """---
title: {title}
kind: learnings
beat: {beat}
book_id: {book_id}
status: reading
date: {date}
---

# Learnings: {title}

How it was read: readwright outline in `toc.txt`; sections read and searched are listed below. Paraphrase in fresh words.
Cite every principle by chapter, section or page in parentheses, like (ch. 3) or (p. 41). Quote at most {quote} words at a time.

## Principles

1. TODO one principle in plain words (ch. N)

## What the beat already has

Run `everscout.py recall --beat {beat} --q "<topic>"` for each principle and note where the beat agrees, lacks it or disagrees.

## Changes

One row per proposed change. target: `beat/<file>` ({beat_files}), `note` (the book note `lit distill` writes),
or `feed:<unit>/<path>` for a skill or plugin this beat feeds (beat.md `feeds`: {feeds}), or `plugin:<name>/<path>` for
another plugin. status: proposed, applied, rejected.

| target | change | principle | status |
|---|---|---|---|
| beat/vocab.md | TODO | 1 | proposed |

## Verdict

One paragraph: worth it or not, for whom, what to skip.
"""


def cmd_lit_ingest(a):
    """Set up a provided book for distilling: outline through readwright, a learnings.md to fill, the list row set to reading."""
    cfg = config()
    b = get_beat(cfg, a.beat)
    path = expand(a.file)
    if not os.path.isfile(path):
        fail(f"no such file: {path}")
    rw = find_readwright(cfg)
    info, toc = "", ""
    if rw:
        for args, name in ((["info", path], "info"), (["toc", path], "toc")):
            p = subprocess.run([sys.executable, rw] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if p.returncode != 0:
                note(f"readwright {name} exited {p.returncode}: {(p.stderr or p.stdout).strip()[:300]}")
            if name == "info":
                info = p.stdout
            else:
                toc = p.stdout
    else:
        note("readwright not found (github.com/m4bwav/readwright, or set EVERSCOUT_READWRIGHT): outline the book with your own reader")
    m = re.search(r"^words:\s*(\d+)\s*$", info, re.M)
    if m and int(m.group(1)) == 0 and not a.force:
        fail("readwright found no text in this file (a scan without a text layer?); OCR it first, or pass --force to set it up anyway")
    title = a.title or (re.search(r"^title:\s*(.+)$", info, re.M | re.I).group(1).strip() if re.search(r"^title:\s*(.+)$", info, re.M | re.I)
                        else os.path.splitext(os.path.basename(path))[0])
    meta, tiers, searches = lit_load(b) if os.path.exists(lit_path(b)) else ({}, {t: [] for t in LIT_TIERS}, [])
    tier, row = lit_find(tiers, a.id or title)
    if row:
        title = row["title"] or title
    slug = slugify(title, 40, whole=True)
    d = os.path.join(books_dir(cfg, b.slug), slug)
    os.makedirs(d, exist_ok=True)
    write(os.path.join(d, "book.md"), render_frontmatter({
        "title": title, "kind": "book", "beat": b.slug, "book_id": (row or {}).get("id") or a.id or "-", "tier": tier or "-",
        "file": path.replace(os.sep, "/"), "reader": "readwright" if rw else "none", "date": today()})
        + f"\n# {title}\n\nThe user's own copy, read for this beat. Never commit or redistribute the text.\n\n## readwright info\n\n```\n{info.strip()}\n```\n")
    if toc:
        write(os.path.join(d, "toc.txt"), toc)
    lp = os.path.join(d, "learnings.md")
    if not os.path.exists(lp) or a.force:
        write(lp, LEARNINGS_TEMPLATE.format(title=title, beat=b.slug, book_id=(row or {}).get("id") or a.id or "-", date=today(),
                                            quote=LIT_MAX_QUOTE_WORDS, beat_files=", ".join(LIT_TARGET_BEAT_FILES),
                                            feeds=", ".join(b.list_meta("feeds")) or "none"))
    if row and row["status"] in ("lead", "have"):
        row["status"] = "reading"
        write(lit_path(b), lit_render(b, meta, tiers, searches))
    print(f"book folder {d}")
    print(f"  learnings.md to fill; toc.txt {'written' if toc else 'not written'}; list row {'set to reading' if row else 'not found (lit add it)'}")
    if rw:
        print(f"  read sections with: python {rw} read \"{path}\" --section N   (search: grep \"{path}\" PATTERN)")


LIT_BOOK_EXTS = (".pdf", ".epub", ".mobi", ".azw3", ".azw", ".djvu", ".txt")


def lit_file_key(path):
    return re.sub(r"[^a-z0-9]+", " ", os.path.splitext(os.path.basename(path.replace("\\", "/")))[0].lower()).strip()


def cmd_lit_pick(a):
    """Book files in a folder that no beat has read yet, the ones a beat's literature lists first."""
    cfg = config()
    folder = expand(a.dir or cfg.get("books_folder") or "")
    if not folder or not os.path.isdir(folder):
        fail("give the folder of book files with --dir, or set books_folder in config.json")
    read_keys, listed = set(), []
    for slug, path in all_beats(cfg).items():
        bd = books_dir(cfg, slug)
        for name in (os.listdir(bd) if os.path.isdir(bd) else []):
            bm = os.path.join(bd, name, "book.md")
            if os.path.isfile(bm):
                f = parse_frontmatter(read(bm))[0].get("file")
                if f:
                    read_keys.add(lit_file_key(f))
        b = Beat(slug, path)
        if os.path.exists(lit_path(b)):
            for tier, rows in lit_load(b)[1].items():
                for r in rows:
                    t = lit_norm_title(r["title"])
                    names = [w for w in re.sub(r"[^a-z ]+", " ", (r.get("authors") or "").lower()).split() if len(w) > 3]
                    if len(t) >= 8:
                        listed.append((t, names, slug, tier, r["status"]))
    # other records of books already read (a notes index, say): a file whose name appears there counts as read
    idx = []
    for p in (a.read_index or []) + list(cfg.get("books_read_index") or []):
        p = expand(p)
        idx += sorted(glob.glob(os.path.join(p, "**", "*.md"), recursive=True)) if os.path.isdir(p) else [p] if os.path.isfile(p) else []
    elsewhere = " ".join(read(p) for p in idx)
    elsewhere_keys = re.sub(r"[^a-z0-9]+", " ", elsewhere.lower())
    out = []
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith(LIT_BOOK_EXTS):
            continue
        key = lit_file_key(name)
        if key in read_keys:
            continue
        if len(key) >= 8 and f" {key} " in f" {elsewhere_keys} ":
            continue
        # a short title (two words or fewer) also needs an author's name in the file name: "Deep Learning" is in many titles
        hits = [l for l in listed if f" {l[0]} " in f" {key} " and (len(l[0].split()) > 2 or any(n in key.split() for n in l[1]))]
        if any(h[4] == "distilled" for h in hits):
            continue
        # a run of four title words found in the other records: probably read there under a different file name
        words = key.split()
        maybe = next((" ".join(words[i:i + 4]) for i in range(len(words) - 3)
                      if f" {' '.join(words[i:i + 4])} " in f" {elsewhere_keys} "), "")
        # or a short title ("Pixel Logic") with another word of the file name, like the author, close by in the record
        maybe = maybe or lit_short_title_hit(words, elsewhere_keys)
        out.append({"file": name, "listed": [{"beat": h[2], "tier": h[3], "status": h[4]} for h in hits], "maybe_read": maybe})
    out.sort(key=lambda r: (bool(r["maybe_read"]), not r["listed"], r["file"].lower()))
    if a.json:
        print(json.dumps(out, indent=1))
        return
    for r in out:
        if r["maybe_read"] and not a.all:
            continue
        tag = "; ".join(f"{l['beat']} {l['tier']} {l['status']}" for l in r["listed"])
        print(r["file"] + (f"   [{tag}]" if tag else "") + (f"   (maybe read: '{r['maybe_read']}' in the read index)" if r["maybe_read"] else ""))
    maybe = sum(1 for r in out if r["maybe_read"])
    print(f"{len(out) - maybe} unread ({sum(1 for r in out if r['listed'] and not r['maybe_read'])} listed by a beat), "
          f"{maybe} maybe read elsewhere{'' if a.all else ' (--all shows them)'}; check the topic fits a beat before ingesting")


def lit_short_title_hit(words, text, near=150):
    """Two long file-name words in a row found in `text` with a third, rare one (an author's name, say) within `near` characters, or ''."""
    padded = f" {text} "
    for i in range(len(words) - 1):
        pair = f" {words[i]} {words[i + 1]} "
        if min(len(words[i]), len(words[i + 1])) < 5:
            continue
        # rare in the records: "python" or "theory" sits near any title, a surname does not
        others = {w for w in words if len(w) >= 4 and padded.count(f" {w} ") <= 8} - {words[i], words[i + 1]}
        for m in re.finditer(re.escape(pair), padded):
            window = padded[max(0, m.start() - near):m.end() + near]
            if any(f" {w} " in window for w in others):
                return pair.strip()
    return ""


def lit_change_status(c):
    """A change row's status word; a note after it, like `applied (x 1.2, PR #3)`, is allowed."""
    m = re.match(r"\s*\**([a-z]+)", (c.get("status") or "").lower())
    return m.group(1) if m else ""


def lit_toc_titles(d):
    """Section titles from a book folder's toc.txt (`  12.   Cards  (344 w)`), lower case, four letters or more."""
    p = os.path.join(d, "toc.txt")
    titles = [m.group(1).strip().lower() for m in re.finditer(r"^\s*\d+\.\s+(.+?)\s+\([\d,]+ w\)\s*$", read(p) if os.path.isfile(p) else "", re.M)]
    return {t for t in titles if len(t) >= 4}


def lit_learnings_problems(b, text, toc_titles=()):
    """(errors, warnings, changes) for a learnings.md. A parenthesis naming a section title from toc.txt counts as a citation."""
    errs, warns = [], []
    _, body = parse_frontmatter(text)
    secs = lit_sections(body)
    principles = [l for l in secs.get("principles", "").splitlines() if re.match(r"\s*\d+\.\s", l)]
    if not principles or any("TODO" in l for l in principles):
        errs.append("Principles: none written yet, or a TODO left")
    for l in principles:
        if not LIT_CITE.search(l) and not re.search(r"\(\s*\d+(\.\d+)+", l) and not any(t in g.lower() for g in re.findall(r"\(([^()]*)\)", l) for t in toc_titles):
            errs.append(f"principle without a citation (ch., p., section): {l.strip()[:80]}")
    for q in re.findall(r"[\"“]([^\"”]+)[\"”]", body):
        if len(q.split()) > LIT_MAX_QUOTE_WORDS:
            errs.append(f"quote of {len(q.split())} words (max {LIT_MAX_QUOTE_WORDS}): paraphrase it: {q[:60]}...")
    changes = parse_table(secs.get("changes", ""))
    feeds = set(b.list_meta("feeds"))
    for c in changes:
        tgt, st = (c.get("target") or "").strip("` "), lit_change_status(c)
        if "TODO" in (c.get("change") or ""):
            errs.append(f"change for {tgt}: TODO left")
        if st not in ("proposed", "applied", "rejected"):
            errs.append(f"change for {tgt}: status {st!r} not proposed, applied or rejected")
        if tgt.startswith("beat/"):
            if tgt[5:] not in LIT_TARGET_BEAT_FILES:
                errs.append(f"target {tgt}: not a beat file ({', '.join(LIT_TARGET_BEAT_FILES)})")
        elif tgt.startswith("feed:"):
            if tgt[5:].split("/")[0] not in {f.split(":", 1)[-1] for f in feeds} | feeds:
                warns.append(f"target {tgt}: the beat does not list this unit in beat.md feeds")
        elif tgt != "note" and not tgt.startswith("plugin:"):
            errs.append(f"target {tgt!r}: use beat/<file>, note, feed:<unit>/<path> or plugin:<name>/<path>")
    if not changes:
        warns.append("Changes: no rows; a book that changes nothing should say why in the Verdict")
    if "TODO" in secs.get("verdict", "") or not secs.get("verdict", "").strip():
        warns.append("Verdict: not written")
    return errs, warns, changes


def lit_book(cfg, b, ref):
    d = os.path.join(books_dir(cfg, b.slug), ref)
    for cut in (True, False):  # folders from before 0.8.3 were cut mid-word
        if not os.path.isdir(d):
            d = os.path.join(books_dir(cfg, b.slug), slugify(ref, 40, whole=cut))
    if not os.path.isfile(os.path.join(d, "learnings.md")):
        have = sorted(os.listdir(books_dir(cfg, b.slug))) if os.path.isdir(books_dir(cfg, b.slug)) else []
        fail(f"no learnings.md for {ref!r} (books: {', '.join(have) or 'none'}); start with `lit ingest`")
    return d


def cmd_lit_lint(a):
    cfg = config()
    b = get_beat(cfg, a.beat)
    d = lit_book(cfg, b, a.book)
    errs, warns, changes = lit_learnings_problems(b, read(os.path.join(d, "learnings.md")), lit_toc_titles(d))
    for e in errs:
        print("ERROR  " + e)
    for w in warns:
        print("warn   " + w)
    by = {}
    for c in changes:
        by[lit_change_status(c)] = by.get(lit_change_status(c), 0) + 1
    print(f"{os.path.basename(d)}: {len(changes)} changes (" + ", ".join(f"{v} {k}" for k, v in sorted(by.items())) + f"); {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


def cmd_lit_distill(a):
    """Finish a book: learnings lint clean and no change left proposed, then a `book` note for recall and the row set to distilled."""
    cfg = config()
    b = get_beat(cfg, a.beat)
    d = lit_book(cfg, b, a.book)
    text = read(os.path.join(d, "learnings.md"))
    errs, _, changes = lit_learnings_problems(b, text, lit_toc_titles(d))
    open_ = [c for c in changes if lit_change_status(c) == "proposed"]
    if errs:
        fail("learnings.md has lint errors; run `lit lint` first")
    if open_ and not a.allow_open:
        fail(f"{len(open_)} changes still proposed: apply or reject each (or pass --allow-open to leave them for later)")
    fm, body = parse_frontmatter(text)
    bm, _ = parse_frontmatter(read(os.path.join(d, "book.md"))) if os.path.exists(os.path.join(d, "book.md")) else ({}, "")
    title = fm.get("title") or bm.get("title") or os.path.basename(d)
    secs = lit_sections(body)
    url = ""
    meta, tiers, searches = lit_load(b) if os.path.exists(lit_path(b)) else ({}, {t: [] for t in LIT_TIERS}, [])
    _, row = lit_find(tiers, fm.get("book_id") if fm.get("book_id") not in (None, "", "-") else title)
    if row:
        url = row["evidence"] if row["id"] in ("", "-") else ("https://openlibrary.org/works/" + row["id"] if row["id"].startswith("OL") else row["evidence"])
    nid = "book-" + os.path.basename(d)
    summary = re.sub(r"\s+", " ", secs.get("verdict", "")).strip()[:240]
    note_fm = {"title": title, "kind": "note", "status": "active", "date": today(), "verified": today(), "beat": b.slug,
               "platform": "book", "community": "-", "url": url or "-", "posted": today(), "note_kind": "book",
               "interest": 3, "engaged": False, "tags": ["book"], "summary": summary or title}
    for facet, ents in vocab_match(b, body).items():
        note_fm[facet] = ents
    applied = [c for c in changes if lit_change_status(c) == "applied"]
    # `note` rows are text for the book note itself (an edition line, reading caveats), not a change elsewhere
    for_note = [c for c in applied if (c.get("target") or "").strip("` ") == "note"]
    applied = [c for c in applied if c not in for_note]
    note_body = (f"# {title}\n\nDistilled from the user's copy on {today()}; full learnings in `books/{os.path.basename(d)}/learnings.md`.\n\n"
                 + "".join(f"{c.get('change')}\n\n" for c in for_note)
                 + f"## Principles\n{secs.get('principles', '').rstrip()}\n\n## What changed\n\n"
                 + "".join(f"- {c.get('target')}: {c.get('change')}\n" for c in applied) + ("- nothing applied\n" if not applied else "")
                 + f"\n## Verdict\n\n{secs.get('verdict', '').strip()}\n")
    p = os.path.join(data_dir(cfg, b.slug), "notes", today()[:7], f"{today()}-{nid}.md")
    write(p, render_frontmatter(note_fm) + "\n" + note_body)
    fm["status"] = "distilled"
    write(os.path.join(d, "learnings.md"), render_frontmatter(fm) + "\n" + body)
    if row:
        row["status"] = "distilled"
        write(lit_path(b), lit_render(b, meta, tiers, searches))
    print(f"note {p}\n{len(applied)} changes applied ({len(for_note)} written into the note), {len(open_)} left proposed; list row {'distilled' if row else 'not found'}")


def cmd_lit(a):
    {"list": cmd_lit_list, "check": cmd_lit_check, "add": cmd_lit_add, "new": cmd_lit_new, "due": cmd_lit_due,
     "ingest": cmd_lit_ingest, "lint": cmd_lit_lint, "distill": cmd_lit_distill, "pick": cmd_lit_pick}[a.action](a)


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(prog="everscout", description="Keep up with any subject: beats, paced feeds, notes, signals, a polite engagement ledger.")
    ap.add_argument("--version", action="version", version=f"everscout {VERSION}")
    sp = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_):
        p = sp.add_parser(name, help=help_)
        p.set_defaults(fn=fn)
        return p

    p = add("where", cmd_where, "resolved paths"); p.add_argument("--beat")
    p = add("beats", cmd_beats, "list beats"); p.add_argument("--json", action="store_true")
    p = add("beat-new", cmd_beat_new, "scaffold a beat from the template"); p.add_argument("slug"); p.add_argument("--title"); p.add_argument("--dir")
    p.add_argument("--scope", help="the beat's opening paragraph, from a caller such as an evergreen unit")
    p.add_argument("--question", action="append", help="a research question (repeat); replaces the template's TODO list")
    p.add_argument("--feeds", help="who reads this beat's findings, e.g. evergreen:<unit>; written to beat.md frontmatter")
    p = add("leads", cmd_leads, "notes and reports since a date, for a caller's refresh (evergreen)"); p.add_argument("--beat", required=True)
    p.add_argument("--since", required=True, help="YYYY-MM-DD"); p.add_argument("--limit", type=int, default=40); p.add_argument("--json", action="store_true")
    p = add("beat-check", cmd_beat_check, "validate a beat's files"); p.add_argument("beat"); p.add_argument("--strict", action="store_true")
    p = add("sources", cmd_sources, "list a beat's sources"); p.add_argument("--beat"); p.add_argument("--json", action="store_true")
    p = add("probe", cmd_probe, "fetch each source once and report"); p.add_argument("--beat"); p.add_argument("--source"); p.add_argument("--kinds")
    p.add_argument("--force", action="store_true"); p.add_argument("--save", action="store_true")
    p.add_argument("--reddit-reader", choices=["auto", "rss", "arcticshift"], help="override config reddit.reader")
    p = add("fetch", cmd_fetch, "fetch a beat's sources (paced, cached) and list new items"); p.add_argument("--beat")
    p.add_argument("--sources"); p.add_argument("--kinds"); p.add_argument("--listing", default="new"); p.add_argument("--t", default="week")
    p.add_argument("--max-age-days", type=float, default=3); p.add_argument("--all", action="store_true"); p.add_argument("--limit", type=int, default=200)
    p.add_argument("--force", action="store_true"); p.add_argument("--json", action="store_true")
    p.add_argument("--peek", action="store_true", help="read without marking items seen or saving fetch state (beat building, questions)")
    p.add_argument("--reddit-reader", choices=["auto", "rss", "arcticshift"], help="override config reddit.reader")
    p.add_argument("--settle-hours", type=float, help="Arctic Shift: end the window this long ago (default reddit.settle_hours, 36)")
    p = add("thread", cmd_thread, "a thread with comments (Reddit, HN, Bluesky, Mastodon, Lemmy, Discourse)"); p.add_argument("url"); p.add_argument("--beat")
    p.add_argument("--force", action="store_true"); p.add_argument("--limit", type=int, default=60); p.add_argument("--json", action="store_true")
    p.add_argument("--reddit-reader", choices=["auto", "rss", "arcticshift"], help="override config reddit.reader")
    p.add_argument("--thread-reader", choices=list(THREAD_READERS), help="override config reddit.thread_reader (fetchwright: opt-in, needs that plugin and a Gemini key)")
    p = add("search", cmd_search, "search reddit, hn, news or arxiv"); p.add_argument("--q", required=True)
    p.add_argument("--kind", default="reddit", choices=["reddit", "hn", "news", "arxiv"]); p.add_argument("--community")
    p.add_argument("--sort", default="new"); p.add_argument("--t", default="month"); p.add_argument("--force", action="store_true"); p.add_argument("--json", action="store_true")
    p.add_argument("--reddit-reader", choices=["auto", "rss", "arcticshift"], help="override config reddit.reader")
    p = add("discover", cmd_discover, "Reddit threads found without a listing: pickup from other sources, web search, captures")
    dsp = p.add_subparsers(dest="action", required=True)
    q = dsp.add_parser("list", help="ranked threads ready to read (24 h after the first link), coverage, captures wanted"); q.add_argument("--beat")
    q.add_argument("--all", action="store_true", help="every entry: held, listed, noted, read, dropped"); q.add_argument("--limit", type=int, default=20)
    q.add_argument("--json", action="store_true")
    q = dsp.add_parser("add", help="record a thread URL found by the agent's web search or a capture"); q.add_argument("url"); q.add_argument("--beat")
    q.add_argument("--via", default="websearch", choices=[v for v in DISCOVERY_VIA if v != "pickup"]); q.add_argument("--title"); q.add_argument("--posted")
    q = dsp.add_parser("mark", help="set an entry's status (wanted: a capture was asked of the user)"); q.add_argument("ref", help="id or thread URL")
    q.add_argument("--beat"); q.add_argument("--status", required=True, choices=DISCOVERY_STATUSES); q.add_argument("--why")
    p = add("captures", cmd_captures, "files the user dropped in the beat's captures/ inbox, with the thread URLs inside"); p.add_argument("--beat")
    p.add_argument("--json", action="store_true")
    p = add("candidates", cmd_candidates, "rank cached items for an engagement"); p.add_argument("--beat"); p.add_argument("--limit", type=int, default=8); p.add_argument("--json", action="store_true")
    p = add("engage-check", cmd_engage_check, "may we engage now? exit 0 yes, 2 no"); p.add_argument("--platform", default="reddit")
    p.add_argument("--community"); p.add_argument("--author"); p.add_argument("--item"); p.add_argument("--kind", default="ask", choices=["ask", "thanks", "answer"]); p.add_argument("--json", action="store_true")
    p = add("engage-record", cmd_engage_record, "record an engagement in the ledger"); p.add_argument("--beat", required=True)
    p.add_argument("--platform", default="reddit"); p.add_argument("--community", required=True); p.add_argument("--item", required=True)
    p.add_argument("--url", required=True); p.add_argument("--author", default=""); p.add_argument("--title")
    p.add_argument("--kind", default="ask", choices=["ask", "thanks", "answer"]); p.add_argument("--questions")
    p.add_argument("--route", default="manual", choices=["manual", "api", "browser"]); p.add_argument("--status", default="handed", choices=["drafted", "handed", "posted", "dropped"])
    p.add_argument("--text-file"); p.add_argument("--text"); p.add_argument("--comment-url"); p.add_argument("--override", action="store_true")
    p = add("engage-update", cmd_engage_update, "change an entry's status or permalink"); p.add_argument("--item", required=True)
    p.add_argument("--kind", default="ask", choices=["ask", "thanks", "answer"]); p.add_argument("--status", choices=["drafted", "handed", "posted", "dropped"]); p.add_argument("--comment-url")
    p = add("ledger", cmd_ledger, "list engagements"); p.add_argument("--beat"); p.add_argument("--days", type=int, default=30)
    p.add_argument("--text", action="store_true"); p.add_argument("--json", action="store_true")
    p = add("followups", cmd_followups, "collect replies from the people asked"); p.add_argument("--beat"); p.add_argument("--days", type=int, default=14); p.add_argument("--force", action="store_true")
    p = add("questions", cmd_questions, "sample question seeds"); p.add_argument("--beat"); p.add_argument("--n", type=int, default=4)
    p.add_argument("--tags"); p.add_argument("--avoid-ai", action="store_true"); p.add_argument("--exclude-recent", type=int, default=30); p.add_argument("--json", action="store_true")
    p = add("vocab-match", cmd_vocab_match, "canonical entities named in a text"); p.add_argument("--beat"); p.add_argument("--file"); p.add_argument("--text"); p.add_argument("--json", action="store_true")
    p = add("new-note", cmd_new_note, "scaffold a note for a thread or page"); p.add_argument("url"); p.add_argument("--beat")
    p.add_argument("--note-kind", default="discussion", choices=NOTE_KINDS); p.add_argument("--title"); p.add_argument("--posted"); p.add_argument("--interest", type=int)
    p.add_argument("--engaged", action="store_true"); p.add_argument("--force", action="store_true")
    p.add_argument("--thread-reader", choices=list(THREAD_READERS), help="override config reddit.thread_reader")
    p.add_argument("--capture", help="write the note from the user's capture file (no fetch; needs --title); source: user-capture")
    p = add("validate", cmd_validate, "check a beat's notes"); p.add_argument("--beat"); p.add_argument("--strict", action="store_true")
    p = add("tally", cmd_tally, "recount signals from the notes"); p.add_argument("--beat")
    p = add("recall", cmd_recall, "what the knowledge base holds on a question: ranked notes, answers, reports, study, signals"); p.add_argument("--beat")
    p.add_argument("--q", required=True); p.add_argument("--limit", type=int, default=12); p.add_argument("--json", action="store_true")
    p = add("index", cmd_index, "regenerate the data folder's indexes"); p.add_argument("--beat")
    p = add("source-log", cmd_source_log, "record a web page actually read, so it may be cited"); p.add_argument("url"); p.add_argument("--beat")
    p.add_argument("--title"); p.add_argument("--supports", help="the claim it supports, in a few words")
    p = add("lint", cmd_lint, "check reports and study: links resolve, external URLs come from notes"); p.add_argument("--beat")
    p.add_argument("--strict", action="store_true"); p.add_argument("--stale-days", type=int, default=120); p.add_argument("--no-url-check", action="store_true")
    p = add("retention", cmd_retention, "purge cached raw content older than retention_hours")
    p = add("state", cmd_state, "fetch state of a beat"); p.add_argument("--beat")
    p = add("stats", cmd_stats, "beat metrics: list, add, collect, review, export (kb/SCHEMA.md, metrics.md)")
    ssp = p.add_subparsers(dest="action", required=True)
    q = ssp.add_parser("list", help="the beat's metrics with point counts and last values"); q.add_argument("--beat"); q.add_argument("--status"); q.add_argument("--json", action="store_true")
    q = ssp.add_parser("add", help="add a candidate metric, or edit one (a definition, unit, source or method change bumps its version)")
    q.add_argument("--beat"); q.add_argument("--id", required=True)
    for f in ("question", "definition", "unit", "source", "grade"):
        q.add_argument("--" + f)
    q.add_argument("--kind", choices=METRIC_KINDS); q.add_argument("--method", choices=METRIC_METHODS)
    q.add_argument("--cadence", choices=list(METRIC_CADENCES)); q.add_argument("--status", choices=METRIC_STATUSES); q.add_argument("--headline", choices=["yes", "no"])
    q = ssp.add_parser("collect", help="collect due values (tally, GDELT, Wikimedia, derived) or record a manual one")
    q.add_argument("--beat"); q.add_argument("--metric"); q.add_argument("--value"); q.add_argument("--date", help="manual: the period; otherwise: collect as if today were this date")
    q.add_argument("--note-ref"); q.add_argument("--backfill", type=int)
    q = ssp.add_parser("review", help="lifecycle review: promotion candidates, stale and flat metrics, trends; --apply to archive")
    q.add_argument("--beat"); q.add_argument("--apply", action="store_true"); q.add_argument("--promote"); q.add_argument("--force", action="store_true")
    q.add_argument("--archive"); q.add_argument("--reason"); q.add_argument("--reactivate"); q.add_argument("--date"); q.add_argument("--json", action="store_true")
    q = ssp.add_parser("approve", help="pre-approve promoting a candidate: collect and review promote it once it meets the rule")
    q.add_argument("metric"); q.add_argument("--beat"); q.add_argument("--withdraw", action="store_true"); q.add_argument("--date", help=argparse.SUPPRESS)
    q = ssp.add_parser("export", help="chartwright-ready long-form CSV, and chart commands when chartwright is found")
    q.add_argument("--beat"); q.add_argument("--metric"); q.add_argument("--since"); q.add_argument("--out"); q.add_argument("--include-archived", action="store_true")
    q.add_argument("--charts", action="store_true", help="build the charts into DATA/reports/charts/ with chartwright")
    p = add("lit", cmd_lit, "books on the beat: canon, recent and latest tiers; Open Library for new ones; a provided book distilled")
    lsp = p.add_subparsers(dest="action", required=True)
    q = lsp.add_parser("list", help="the beat's literature by tier"); q.add_argument("--beat"); q.add_argument("--tier", choices=LIT_TIERS)
    q.add_argument("--status", choices=LIT_STATUSES); q.add_argument("--json", action="store_true")
    q = lsp.add_parser("check", help="validate literature.md"); q.add_argument("--beat"); q.add_argument("--strict", action="store_true")
    q = lsp.add_parser("add", help="add a book to a tier, or update a listed one (matched by --id, then --title)"); q.add_argument("--beat")
    q.add_argument("--tier", choices=LIT_TIERS); q.add_argument("--status", choices=LIT_STATUSES)
    for f in ("title", "authors", "year", "id", "why", "evidence"):
        q.add_argument("--" + f)
    q = lsp.add_parser("new", help="recent books from the beat's Open Library searches that are not listed yet"); q.add_argument("--beat")
    q.add_argument("--since-year", type=int); q.add_argument("--per-search", type=int, default=40); q.add_argument("--limit", type=int, default=30)
    q.add_argument("--language", default="eng", help="keep books in this language code (default eng; `any` keeps all); books with no language are kept"); q.add_argument("--force", action="store_true")
    q.add_argument("--json", action="store_true")
    q = lsp.add_parser("due", help="tiers due for research (canon yearly, recent quarterly, latest monthly); exit 2 when any"); q.add_argument("--beat")
    q = lsp.add_parser("ingest", help="set up a provided book: readwright outline, DATA/books/<slug>/learnings.md, row set to reading")
    q.add_argument("file"); q.add_argument("--beat"); q.add_argument("--title"); q.add_argument("--id")
    q.add_argument("--force", action="store_true", help="rewrite learnings.md; set up a file with no text layer anyway")
    q = lsp.add_parser("pick", help="book files in a folder no beat has read yet, beat-listed ones first")
    q.add_argument("--dir", help="folder of book files (default: config books_folder)")
    q.add_argument("--all", action="store_true", help="also list books that are maybe read elsewhere")
    q.add_argument("--read-index", action="append", help="a file or folder of .md files recording books read elsewhere; a book whose file name appears there counts as read (repeatable; config books_read_index)")
    q.add_argument("--json", action="store_true")
    q = lsp.add_parser("lint", help="check a book's learnings.md: citations, quote length, change targets"); q.add_argument("book"); q.add_argument("--beat")
    q = lsp.add_parser("distill", help="finish a book: a `book` note for recall, the row set to distilled"); q.add_argument("book"); q.add_argument("--beat")
    q.add_argument("--allow-open", action="store_true", help="leave proposed changes for later")
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
