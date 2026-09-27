"""Offline tests for everscout. Every fixture is synthetic: no real user names or posts.

Run: python -m unittest discover -s tests
"""
import contextlib
import datetime as dt
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import es_sources as S  # noqa: E402
import everscout as E  # noqa: E402

UTC = dt.timezone.utc


def ago(hours):
    return (dt.datetime.now(UTC) - dt.timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def reddit_atom(sub="exampleSub", entries=()):
    body = "".join(f"""<entry><author><name>/u/{a}</name></author><category term="{sub}" label="r/{sub}"/>
<content type="html">&lt;p&gt;{t}&lt;/p&gt; &lt;a href="https://i.redd.it/x.png"&gt;img&lt;/a&gt;</content>
<id>t3_{pid}</id><link href="https://www.reddit.com/r/{sub}/comments/{pid}/slug/"/><updated>{when}</updated><published>{when}</published>
<title>{title}</title></entry>""" for pid, a, title, t, when in entries)
    return f'<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom"><category term="{sub}"/>{body}</feed>'


def reddit_thread_atom(pid="abc123", op="maker_one", replies=()):
    post = (pid, op, "I made a short film with a new pipeline", "Here is how I did it with Tool X", ago(30))
    base = reddit_atom("exampleSub", [post])
    comments = "".join(f"""<entry><author><name>/u/{a}</name></author><content type="html">{t}</content><id>t1_{cid}</id>
<link href="https://www.reddit.com/r/exampleSub/comments/{pid}/slug/{cid}/"/><updated>{when}</updated>
<title>/u/{a} on I made a short film with a new pipeline</title></entry>""" for cid, a, t, when in replies)
    return base.replace("</feed>", comments + "</feed>")


RSS2 = """<?xml version="1.0"?><rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel><title>Blog</title>
<item><title>Rates held again</title><link>https://example.org/p/rates</link><guid>https://example.org/p/rates</guid>
<pubDate>Wed, 23 Sep 2026 10:00:00 GMT</pubDate><dc:creator>A Writer</dc:creator><description>&lt;p&gt;The central bank held. Chart from fred.stlouisfed.org&lt;/p&gt;</description></item>
</channel></rss>"""

RSS1 = """<?xml version="1.0"?><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<item rdf:about="https://example.org/a"><title>Paper one</title><link>https://example.org/a</link><description>abstract</description><dc:date>2026-09-20T00:00:00Z</dc:date></item>
</rdf:RDF>"""

YT_ATOM = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xmlns:yt="http://www.youtube.com/xml/schemas/2015">
<entry><id>yt:video:VID1</id><title>Making a music video with toolx</title><link rel="alternate" href="https://www.youtube.com/watch?v=VID1"/>
<author><name>Channel</name></author><published>2026-09-24T00:00:00+00:00</published>
<media:group><media:description>Full workflow breakdown</media:description></media:group></entry></feed>"""

HN_HITS = {"hits": [
    {"objectID": "101", "title": "Show HN: A tool for X", "url": "https://github.com/someone/x", "author": "hnuser", "points": 42,
     "num_comments": 7, "created_at": "2026-09-25T12:00:00Z", "_tags": ["story", "show_hn"]},
    {"objectID": "102", "comment_text": "<p>I use it daily</p>", "story_id": 101, "story_title": "Show HN: A tool for X",
     "author": "other", "created_at": "2026-09-25T13:00:00Z", "_tags": ["comment"]},
]}

HN_ITEM = {"id": 101, "title": "Show HN: A tool for X", "author": "hnuser", "url": "https://github.com/someone/x", "points": 42,
           "created_at": "2026-09-25T12:00:00Z", "text": None, "children": [
               {"id": 201, "type": "comment", "author": "a1", "text": "<p>What did you use for the UI?</p>", "created_at": "2026-09-25T12:30:00Z",
                "parent_id": 101, "children": [
                    {"id": 202, "type": "comment", "author": "hnuser", "text": "Plain HTML", "created_at": "2026-09-25T13:00:00Z", "parent_id": 201, "children": []}]}]}

BSKY_FEED = {"feed": [{"post": {"uri": "at://did:plc:abc/app.bsky.feed.post/3kx1", "author": {"handle": "someone.bsky.social"},
                                "record": {"text": "New chart on wages\nmore text", "createdAt": "2026-09-25T10:00:00Z"},
                                "replyCount": 3, "likeCount": 10, "embed": {"$type": "app.bsky.embed.images#view", "images": [{}]}}}]}

BSKY_THREAD = {"thread": {"post": BSKY_FEED["feed"][0]["post"], "replies": [
    {"post": {"uri": "at://did:plc:def/app.bsky.feed.post/3kx2", "author": {"handle": "asker.bsky.social"},
              "record": {"text": "Which deflator did you use?", "createdAt": "2026-09-25T11:00:00Z"}}, "replies": []}]}}

MASTO_STATUS = {"id": "111", "account": {"acct": "maker@example.social"}, "content": "<p>Released my new EP</p>",
                "created_at": "2026-09-24T09:00:00Z", "url": "https://example.social/@maker/111", "replies_count": 1, "favourites_count": 5,
                "media_attachments": []}
MASTO_CONTEXT = {"descendants": [{"id": "112", "account": {"acct": "fan"}, "content": "<p>What synth is that pad?</p>",
                                  "created_at": "2026-09-24T10:00:00Z", "url": "https://example.social/@fan/112"}]}

LEMMY_POST = {"post_view": {"post": {"id": 55, "name": "My workflow", "body": "text", "published": "2026-09-24T00:00:00Z"},
                            "creator": {"name": "maker"}, "community": {"name": "aivideo"}, "counts": {"comments": 1, "score": 9}}}
LEMMY_COMMENTS = {"comments": [{"comment": {"id": 9, "content": "nice", "published": "2026-09-24T01:00:00Z", "path": "0.9"},
                                "creator": {"name": "fan"}}]}

DISCOURSE_TOPIC = {"id": 77, "slug": "my-patch", "title": "My new patch", "created_at": "2026-09-23T00:00:00Z", "posts_count": 2,
                   "post_stream": {"posts": [
                       {"id": 1, "username": "maker", "cooked": "<p>Here is the patch</p>", "created_at": "2026-09-23T00:00:00Z", "post_number": 1},
                       {"id": 2, "username": "fan", "cooked": "<p>How did you route it?</p>", "created_at": "2026-09-23T01:00:00Z", "post_number": 2}]}}

HF_MODELS = [{"id": "org/video-model", "likes": 120, "downloads": 5000, "trendingScore": 80, "createdAt": "2026-09-20T00:00:00Z",
              "pipeline_tag": "text-to-video", "tags": ["diffusers", "license:apache-2.0"]}]


class FakeResponse:
    def __init__(self, body, status=200, headers=None):
        self.body = body.encode("utf-8") if isinstance(body, str) else body
        self.status = status
        self.headers = FakeHeaders(headers or {})

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakeHeaders(dict):
    def get_content_charset(self):
        return "utf-8"

    def get(self, k, d=None):
        return super().get(k.lower(), d)


class ParserTests(unittest.TestCase):
    def test_reddit_listing(self):
        items = S.parse_reddit(reddit_atom("exampleSub", [("p1", "maker_one", "I made a thing", "body", ago(5))]))
        self.assertEqual(items[0]["id"], "reddit:p1")
        self.assertEqual(items[0]["author"], "maker_one")
        self.assertEqual(items[0]["community"], "exampleSub")
        self.assertIn("image", items[0]["media"])
        self.assertEqual(items[0]["kind"], "post")

    def test_reddit_thread_comments(self):
        items = S.parse_reddit(reddit_thread_atom(replies=[("c1", "fan", "what tools?", ago(2))]))
        self.assertEqual([i["kind"] for i in items], ["post", "comment"])

    def test_rss2_and_rss1_and_youtube(self):
        r2 = S.parse_feed(RSS2, platform="rss")
        self.assertEqual(r2[0]["title"], "Rates held again")
        self.assertEqual(r2[0]["published"], "2026-09-23T10:00:00Z")
        self.assertEqual(r2[0]["author"], "A Writer")
        self.assertIn("data", r2[0]["media"])
        r1 = S.parse_feed(RSS1, platform="arxiv")
        self.assertEqual(r1[0]["url"], "https://example.org/a")
        yt = S.parse_feed(YT_ATOM, platform="youtube")
        self.assertEqual(yt[0]["text"], "Full workflow breakdown")
        self.assertIn("video", yt[0]["media"])

    def test_block_page_is_an_error(self):
        with self.assertRaises(ValueError):
            S.parse_feed("<html><body>blocked by network security</body")

    def test_hn(self):
        hits = S.parse_hn_hits(HN_HITS)
        self.assertEqual(hits[0]["id"], "hn:101")
        self.assertEqual(hits[0]["comments"], 7)
        self.assertEqual(hits[1]["kind"], "comment")
        self.assertTrue(hits[1]["url"].endswith("id=101"))
        t = S.parse_hn_item(HN_ITEM)
        self.assertEqual(len(t["comments"]), 2)
        self.assertEqual(t["comments"][1]["depth"], 1)
        self.assertEqual(S.hn_item_id("https://news.ycombinator.com/item?id=101"), "101")

    def test_bluesky(self):
        f = S.parse_bsky_feed(BSKY_FEED)
        self.assertEqual(f[0]["url"], "https://bsky.app/profile/someone.bsky.social/post/3kx1")
        self.assertEqual(f[0]["title"], "New chart on wages")
        self.assertIn("image", f[0]["media"])
        t = S.parse_bsky_thread(BSKY_THREAD)
        self.assertEqual(t["comments"][0]["author"], "asker.bsky.social")
        self.assertEqual(S.bsky_thread_parts("https://bsky.app/profile/x.bsky.social/post/3kx1"), ("x.bsky.social", "3kx1"))

    def test_mastodon_lemmy_discourse(self):
        m = S.parse_mastodon_thread(MASTO_STATUS, MASTO_CONTEXT, "example.social")
        self.assertEqual(m["post"]["text"], "Released my new EP")
        self.assertEqual(m["comments"][0]["author"], "fan")
        self.assertEqual(S.mastodon_thread_parts("https://example.social/@maker/111"), ("example.social", "111"))
        l = S.parse_lemmy_thread(LEMMY_POST, LEMMY_COMMENTS, "lemmy.example")
        self.assertEqual(l["post"]["community"], "aivideo")
        self.assertEqual(len(l["comments"]), 1)
        d = S.parse_discourse_topic(DISCOURSE_TOPIC, "https://forum.example")
        self.assertEqual(d["post"]["url"], "https://forum.example/t/my-patch/77")
        self.assertEqual(d["comments"][0]["text"], "How did you route it?")
        self.assertEqual(S.discourse_thread_parts("https://forum.example/t/my-patch/77"), ("https://forum.example", "77"))

    def test_huggingface(self):
        url = S.huggingface_url("models?pipeline_tag=text-to-video")
        self.assertIn("sort=trendingScore", url)
        items = S.parse_huggingface(HF_MODELS, url)
        self.assertEqual(items[0]["url"], "https://huggingface.co/org/video-model")
        self.assertIn("text-to-video", items[0]["text"])

    def test_platform_of(self):
        self.assertEqual(E.platform_of("https://old.reddit.com/r/x/comments/abc/t/"), "reddit")
        self.assertEqual(E.platform_of("https://news.ycombinator.com/item?id=1"), "hn")
        self.assertEqual(E.platform_of("https://bsky.app/profile/a/post/b"), "bluesky")
        self.assertEqual(E.platform_of("https://example.social/@maker/111"), "mastodon")
        self.assertEqual(E.platform_of("https://lemmy.example/post/55"), "lemmy")
        self.assertEqual(E.platform_of("https://forum.example/t/slug/77"), "discourse")
        self.assertEqual(E.platform_of("https://example.org/article"), "web")

    def test_times(self):
        self.assertEqual(S.iso(S.parse_time("Wed, 23 Sep 2026 10:00:00 GMT")), "2026-09-23T10:00:00Z")
        self.assertEqual(S.iso(S.parse_time("2026-09-23")), "2026-09-23T00:00:00Z")
        self.assertIsNone(S.parse_time("not a date"))

    def test_filter(self):
        it = {"title": "New Kling release for music videos", "text": ""}
        self.assertTrue(E.passes(it, "kling veo"))
        self.assertFalse(E.passes(it, "+sora"))
        self.assertFalse(E.passes(it, "-\"music videos\""))
        self.assertFalse(E.passes(it, "", mute=["release"]))
        self.assertTrue(E.passes(it, ""))
        self.assertFalse(E.passes({"title": "veolia earnings", "text": ""}, "veo"))  # word boundary


class WorkspaceTest(unittest.TestCase):
    """A temporary EVERSCOUT_HOME with one private beat."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="everscout-test-")
        self.home = os.path.join(self.tmp, "home")
        os.makedirs(os.path.join(self.home, "beats"))
        cfg = {"contact": "test@example.org", "data_root": os.path.join(self.tmp, "data"), "local_root": os.path.join(self.tmp, "local"),
               "beat_dirs": [os.path.join(self.home, "beats")], "pace": {"hosts": {"default": 0, "www.reddit.com": 0}}}
        with open(os.path.join(self.home, "config.json"), "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        self.env = mock.patch.dict(os.environ, {"EVERSCOUT_HOME": self.home})
        self.env.start()
        self.run_cli("beat-new", "test-beat", "--title", "Test beat")
        bd = os.path.join(self.home, "beats", "test-beat")
        with open(os.path.join(bd, "sources.md"), "w", encoding="utf-8") as f:
            f.write("# Sources\n\n| source | kind | group | stance | engage | scan | filter | notes |\n|---|---|---|---|---|---|---|---|\n"
                    "| r/exampleSub | reddit | core | native | yes | yes | | ✓ 2026-09-26 |\n"
                    "| https://example.org/feed | rss | blogs | n/a | no | yes | -sponsored | ✓ 2026-09-26 |\n"
                    "| \"tool x\" | hn | news | n/a | no | yes | | ~ |\n")
        with open(os.path.join(bd, "vocab.md"), "w", encoding="utf-8") as f:
            f.write("# Vocab\n\n## Tools\n\n- toolx: Tool X, tool-x\n- tooly: ToolY\n\n## Techniques\n\n- pipeline: pipeline, workflow\n")
        self.bd = bd

    def tearDown(self):
        self.env.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                E.main(list(args))
            except SystemExit as e:
                code = e.code or 0
        return code, out.getvalue(), err.getvalue()

    def cfg(self):
        return E.config()


class BeatTests(WorkspaceTest):
    def test_beats_and_check(self):
        code, out, _ = self.run_cli("beats")
        self.assertIn("test-beat", out)
        self.assertIn("ai-video", out)  # built-in beats are listed too
        code, out, _ = self.run_cli("beat-check", "test-beat")
        self.assertEqual(code, 0, out)
        self.assertIn("3 sources", out)

    def test_beat_check_catches_bad_rows(self):
        with open(os.path.join(self.bd, "sources.md"), "a", encoding="utf-8") as f:
            f.write("| r/exampleSub | reddit | core | native | yes | yes | | dup |\n| x | telepathy | core | weird | no | yes | | ? |\n")
        # the table ended at the blank line in the template, so rewrite it whole
        text = open(os.path.join(self.bd, "sources.md"), encoding="utf-8").read().replace("\n\n| r/exampleSub | reddit | core | native | yes | yes | | dup |", "\n| r/exampleSub | reddit | core | native | yes | yes | | dup |")
        open(os.path.join(self.bd, "sources.md"), "w", encoding="utf-8").write(text)
        code, out, _ = self.run_cli("beat-check", "test-beat")
        self.assertEqual(code, 1)
        self.assertIn("duplicate source", out)
        self.assertIn("unknown kind", out)

    def test_builtin_beats_pass_check(self):
        for slug in ("ai-video", "global-economics", "downtempo", "tech-hiring"):
            code, out, _ = self.run_cli("beat-check", slug)
            self.assertEqual(code, 0, f"{slug}: {out}")

    def test_vocab_and_questions(self):
        b = E.get_beat(self.cfg(), "test-beat")
        self.assertEqual(b.facets(), ["tools", "techniques"])
        m = E.vocab_match(b, "I used Tool X and a custom workflow, not toolyish")
        self.assertEqual(m, {"tools": ["toolx"], "techniques": ["pipeline"]})
        code, out, _ = self.run_cli("questions", "--beat", "test-beat", "--n", "3")
        self.assertEqual(len(out.strip().splitlines()), 3)

    def test_feed_urls(self):
        row = lambda k, s: {"kind": k, "source": s}
        self.assertEqual(E.feed_urls(row("mastodon", "#ambient@example.social"))[0][0], "https://example.social/tags/ambient.rss")
        self.assertEqual(E.feed_urls(row("lemmy", "c/aivideo@lemmy.example"))[0][0], "https://lemmy.example/feeds/c/aivideo.xml?sort=New")
        self.assertEqual(E.feed_urls(row("youtube", "UCabc"))[0][0], "https://www.youtube.com/feeds/videos.xml?channel_id=UCabc")
        self.assertEqual(E.feed_urls(row("github", "comfyanonymous/ComfyUI"))[0][0], "https://github.com/comfyanonymous/ComfyUI/releases.atom")
        self.assertEqual(E.feed_urls(row("bluesky", "at://did:plc:x/app.bsky.feed.generator/econ"))[0][2], "bsky")
        self.assertEqual(E.feed_urls(row("discourse", "https://forum.example"))[0][0], "https://forum.example/latest.rss")
        self.assertEqual(E.feed_urls(row("web", "some site")), [])


class FetchTests(WorkspaceTest):
    def fake_net(self, req, timeout=0):
        url = req.full_url
        self.calls.append((url, dict(req.header_items())))
        if "reddit.com/r/exampleSub/new" in url:
            return FakeResponse(reddit_atom("exampleSub", [("p1", "maker_one", "I made a short film with Tool X", "my workflow", ago(20)),
                                                          ("p2", "someone", "Weekly thread", "megathread", ago(3))]),
                                headers={"x-ratelimit-reset": "0"})
        if "reddit.com/r/exampleSub/comments/p1" in url:
            return FakeResponse(reddit_thread_atom("p1", "maker_one", [("c1", "fan", "love it", ago(10))]))
        if "example.org/feed" in url:
            return FakeResponse(RSS2.replace("Rates held again", "Sponsored post").replace("</channel>",
                                "<item><title>Tool X pipeline notes</title><link>https://example.org/p/x</link>"
                                f"<pubDate>{dt.datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate></item></channel>"))
        if "hn.algolia.com" in url:
            return FakeResponse(json.dumps(HN_HITS))
        raise AssertionError("unexpected URL " + url)

    def setUp(self):
        super().setUp()
        self.calls = []
        self.net = mock.patch("urllib.request.urlopen", self.fake_net)
        self.net.start()

    def tearDown(self):
        self.net.stop()
        super().tearDown()

    def test_fetch_filter_cache_and_user_agents(self):
        code, out, err = self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650")
        self.assertEqual(code, 0, err)
        self.assertIn("1 filtered out", out)  # the sponsored item
        self.assertIn("I made a short film", out)
        self.assertIn("Tool X pipeline notes", out)
        uas = {u.split("/")[2]: h.get("User-agent") for u, h in self.calls}
        self.assertTrue(uas["www.reddit.com"].endswith(":everscout:v" + E.VERSION + " (by /u/unknown)"))
        self.assertIn("test@example.org", uas["example.org"])
        n = len(self.calls)
        self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650")
        self.assertEqual(len(self.calls), n, "second fetch within the hour must come from the cache")

    def test_candidates_note_validate_tally_index_lint(self):
        self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650")
        code, out, _ = self.run_cli("candidates", "--beat", "test-beat")
        self.assertIn("I made a short film", out)
        self.assertNotIn("Weekly thread", out)  # skip words
        code, out, err = self.run_cli("new-note", "https://www.reddit.com/r/exampleSub/comments/p1/slug/", "--beat", "test-beat",
                                      "--note-kind", "showcase")
        self.assertEqual(code, 0, err)
        path = out.strip()
        text = open(path, encoding="utf-8").read()
        self.assertIn("tools: [toolx]", text)
        self.assertIn("techniques: [pipeline]", text)
        code, out, _ = self.run_cli("validate", "--beat", "test-beat")
        self.assertEqual(code, 1)  # TODOs left
        text = text.replace("TODO one line saying what this teaches", "a maker's Tool X pipeline").replace("\nTODO\n", "\nfilled\n")
        open(path, "w", encoding="utf-8").write(text)
        code, out, _ = self.run_cli("validate", "--beat", "test-beat", "--strict")
        self.assertEqual(code, 0, out)
        code, out, _ = self.run_cli("tally", "--beat", "test-beat")
        self.assertIn("1 notes tallied", out)
        dd = E.data_dir(self.cfg(), "test-beat")
        t = json.load(open(os.path.join(dd, "signals", "tallies.json"), encoding="utf-8"))
        self.assertEqual(t["facets"]["tools"]["toolx"]["signal"], "new")
        self.assertEqual(t["facets"]["tools"]["toolx"]["30d"], 1)
        code, out, _ = self.run_cli("index", "--beat", "test-beat")
        self.assertTrue(os.path.exists(os.path.join(dd, "notes", "INDEX.md")))
        self.assertTrue(os.path.exists(os.path.join(dd, "journal.md")))
        os.makedirs(os.path.join(dd, "reports"), exist_ok=True)
        note_rel = os.path.relpath(path, os.path.join(dd, "reports")).replace(os.sep, "/")
        open(os.path.join(dd, "reports", "2026-09-26-trends.md"), "w", encoding="utf-8").write(
            f"---\ntitle: r\ndate: 2026-09-26\nverified: 2026-09-26\nsummary: s\n---\n[ok]({note_rel}) [bad](../notes/nope.md) "
            "[held](https://www.reddit.com/r/exampleSub/comments/p1/slug/) [invented](https://made.up/article)\n")
        code, out, _ = self.run_cli("lint", "--beat", "test-beat")
        self.assertEqual(code, 1)
        self.assertIn("broken link ../notes/nope.md", out)
        self.assertIn("made.up/article", out)
        self.assertNotIn("comments/p1/slug/ ", out.replace("\n", " ").split("made.up")[0].split("warn")[-1] + " x")

    def test_peek_leaves_items_new(self):
        code, out, _ = self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650", "--peek")
        n_peek = int(out.split(" new items")[0].split()[-1])
        self.assertGreater(n_peek, 0)
        self.assertFalse(os.path.exists(E.state_path(self.cfg(), "test-beat")))
        code, out, _ = self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650")
        self.assertEqual(int(out.split(" new items")[0].split()[-1]), n_peek)
        code, out, _ = self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650")
        self.assertIn(" 0 new items", out)

    def test_community_is_the_row_and_source_log_satisfies_lint(self):
        self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650")
        items = json.load(open(E.items_path(self.cfg(), "test-beat"), encoding="utf-8"))
        rss = [i for i in items if i["source_kind"] == "rss"]
        self.assertTrue(rss and all(i["community"] == "https://example.org/feed" for i in rss))
        self.assertTrue(all(i["community"] == "exampleSub" for i in items if i["source_kind"] == "reddit"))
        dd = E.data_dir(self.cfg(), "test-beat")
        os.makedirs(os.path.join(dd, "study"), exist_ok=True)
        open(os.path.join(dd, "study", "01-origins.md"), "w", encoding="utf-8").write(
            "---\ntitle: o\ndate: 2026-09-26\nverified: 2026-09-26\nsummary: s\n---\n[policy](https://policy.example.org/page)\n")
        code, out, _ = self.run_cli("lint", "--beat", "test-beat", "--strict")
        self.assertEqual(code, 1)
        self.run_cli("source-log", "https://policy.example.org/page", "--beat", "test-beat", "--title", "Policy", "--supports", "the rule")
        code, out, _ = self.run_cli("source-log", "https://policy.example.org/page", "--beat", "test-beat")
        self.assertIn("already logged", out)
        code, out, _ = self.run_cli("lint", "--beat", "test-beat", "--strict")
        self.assertEqual(code, 0, out)

    def test_thread_and_followups(self):
        self.run_cli("fetch", "--beat", "test-beat", "--max-age-days", "3650")
        code, out, _ = self.run_cli("thread", "https://www.reddit.com/r/exampleSub/comments/p1/slug/", "--beat", "test-beat")
        self.assertIn("process asked: False", out)
        cfg = self.cfg()
        E.save_ledger(cfg, [{"ts": ago(12), "beat": "test-beat", "platform": "reddit", "community": "exampleSub", "item": "reddit:p1",
                             "url": "https://www.reddit.com/r/exampleSub/comments/p1/slug/", "author": "maker_one", "kind": "ask",
                             "status": "handed", "questions": [], "replies": []}])
        # the OP answers after the ask
        self.calls.clear()
        orig = self.fake_net

        def net(req, timeout=0):
            if "comments/p1" in req.full_url:
                return FakeResponse(reddit_thread_atom("p1", "maker_one", [("c2", "maker_one", "I used Tool X", ago(1)),
                                                                           ("c3", "maker_one", "old reply", ago(20))]))
            return orig(req, timeout)
        with mock.patch("urllib.request.urlopen", net):
            code, out, _ = self.run_cli("followups", "--force")
        self.assertIn("1 new replies", out)
        self.assertIn("I used Tool X", out)


class MultiredditTests(WorkspaceTest):
    def write_sources(self, subs):
        with open(os.path.join(self.bd, "sources.md"), "w", encoding="utf-8") as f:
            f.write("| source | kind | group | stance | engage | scan | filter | notes |\n|---|---|---|---|---|---|---|---|\n")
            for s in subs:
                f.write(f"| r/{s} | reddit | core | native | yes | yes | | ~ |\n")

    def test_plan(self):
        rows = [{"source": f"r/s{i}", "kind": "reddit"} for i in range(5)]
        cfg = {"pace": {}}
        self.assertEqual([len(b) for b in E.plan_reddit_batches(rows, {}, 3, cfg)], [4, 1])  # unknown = 5 a day, 15 each, cap 70
        busy = {"s0": 40}
        plan = E.plan_reddit_batches(rows, busy, 3, cfg)
        self.assertIn([rows[0]], plan, "a busy subreddit goes alone")
        self.assertEqual(E.plan_reddit_batches(rows, {}, 3, {"pace": {"reddit_multi_max": 1}}), [[r] for r in rows])

    def test_multi_fetch_maps_rows_and_falls_back(self):
        self.write_sources(["alpha", "beta"])
        calls = []

        def net(req, timeout=0):
            calls.append(req.full_url)
            if "/r/alpha+beta/new" in req.full_url or "/r/beta+alpha/new" in req.full_url:
                entries = [(f"a{i}", "u", "I made a thing", "x", ago(1 + i * 0.1)) for i in range(3)]
                atom = reddit_atom("alpha", entries).replace("</feed>", reddit_atom("beta", [("b1", "v", "My new track", "y", ago(2))])
                                                            .split('<category term="beta"/>', 1)[1])
                return FakeResponse(atom)
            raise AssertionError(req.full_url)
        with mock.patch("urllib.request.urlopen", net):
            code, out, err = self.run_cli("fetch", "--beat", "test-beat", "--json")
        self.assertEqual(len(calls), 1, calls)
        items = json.loads(out)
        self.assertEqual({i["community"] for i in items}, {"alpha", "beta"})
        self.assertEqual({i["source"] for i in items}, {"r/alpha", "r/beta"})
        st = json.load(open(E.state_path(self.cfg(), "test-beat"), encoding="utf-8"))
        self.assertIn("alpha", st["rates"])

        # a full window that does not reach the cutoff falls back to one request per subreddit
        calls.clear()

        def full(req, timeout=0):
            calls.append(req.full_url)
            if "+" in req.full_url:
                return FakeResponse(reddit_atom("alpha", [(f"x{i}", "u", "post", "t", ago(0.1 + i * 0.01)) for i in range(100)]))
            return FakeResponse(reddit_atom(req.full_url.split("/r/")[1].split("/")[0], [("z1", "w", "I made it", "t", ago(5))]))
        cfg_path = os.path.join(self.home, "config.json")
        c = json.load(open(cfg_path, encoding="utf-8"))
        open(cfg_path, "w", encoding="utf-8").write(json.dumps(c))
        st["rates"] = {}
        json.dump(st, open(E.state_path(self.cfg(), "test-beat"), "w", encoding="utf-8"))
        with mock.patch("urllib.request.urlopen", full):
            code, out, err = self.run_cli("fetch", "--beat", "test-beat", "--force", "--max-age-days", "3")
        self.assertIn("window full", err)
        self.assertEqual(len(calls), 3, calls)


class RecallTests(WorkspaceTest):
    def write(self, rel, text):
        dd = E.data_dir(self.cfg(), "test-beat")
        p = os.path.join(dd, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)
        return p

    def test_recall_ranks_notes_answers_and_names_entities(self):
        today = E.today()
        self.write(f"notes/{today[:7]}/p1-tool-x.md", f"---\ntitle: My Tool X pipeline for short films\nkind: note\ndate: {today}\n"
                   f"posted: {today}\nbeat: test-beat\nurl: https://www.reddit.com/r/exampleSub/comments/p1/x/\ntools: [toolx]\n"
                   "techniques: [pipeline]\nsummary: a maker's end-to-end pipeline\n---\n# t\n\nThe pipeline uses Tool X.\n")
        self.write("notes/2020-01/p2-old.md", "---\ntitle: Old ToolY thread\nkind: note\ndate: 2020-01-02\nposted: 2020-01-02\n"
                   "tools: [tooly]\nsummary: an old discussion of ToolY\n---\nnothing about the other one\n")
        self.write(f"answers/{today}-what-pipeline.md", f"---\ntitle: What pipeline do makers use\nkind: answer\ndate: {today}\n"
                   f"verified: {today}\nquestion: what pipeline do makers use with Tool X\nsummary: mostly Tool X then an editor\n---\n"
                   "## Answer\n\nTool X, then an editor.\n")
        self.run_cli("tally", "--beat", "test-beat")
        code, out, _ = self.run_cli("recall", "--beat", "test-beat", "--q", "Which pipeline do people build around Tool X?", "--json")
        self.assertEqual(code, 0)
        r = json.loads(out)
        self.assertEqual(r["status"]["notes"], 2)
        self.assertEqual(r["status"]["answers"], 1)
        self.assertEqual(r["entities"], {"tools": ["toolx"], "techniques": ["pipeline"]})
        kinds = [h["kind"] for h in r["hits"]]
        self.assertIn("note", kinds)
        self.assertIn("answer", kinds)
        self.assertNotIn("notes/2020-01/p2-old.md", [h["path"] for h in r["hits"]])  # names neither the words nor the entities
        self.assertEqual(r["tallies"][0]["signal"], "new")
        code, out, _ = self.run_cli("recall", "--beat", "test-beat", "--q", "zebra migration")
        self.assertIn("nothing in the knowledge base matches", out)

    def test_answers_are_indexed_and_linted(self):
        today = E.today()
        self.write(f"answers/{today}-q.md", f"---\ntitle: q\nkind: answer\ndate: {today}\nverified: {today}\nsummary: s\n---\n"
                   "[invented](https://made.up/claim)\n")
        code, out, _ = self.run_cli("index", "--beat", "test-beat")
        self.assertIn("answers 1", out)
        code, out, _ = self.run_cli("lint", "--beat", "test-beat", "--strict")
        self.assertEqual(code, 1)
        self.assertIn("answers/", out)
        self.run_cli("source-log", "https://made.up/claim", "--beat", "test-beat")
        code, out, _ = self.run_cli("lint", "--beat", "test-beat", "--strict")
        self.assertEqual(code, 0, out)


class ProbeTests(WorkspaceTest):
    write_sources = MultiredditTests.write_sources

    def test_probe_batches_reddit_and_checks_absent_ones_alone(self):
        self.write_sources(["alpha", "beta", "gone"])
        calls = []

        def net(req, timeout=0):
            calls.append(req.full_url)
            if "+" in req.full_url:
                return FakeResponse(reddit_atom("alpha", [("a1", "u", "t", "x", ago(1))]).replace(
                    "</feed>", reddit_atom("beta", [("b1", "v", "t", "y", ago(2))]).split('<category term="beta"/>', 1)[1]))
            if "/r/gone/" in req.full_url:
                import urllib.error
                raise urllib.error.HTTPError(req.full_url, 404, "nf", {}, None)
            raise AssertionError(req.full_url)
        with mock.patch("urllib.request.urlopen", net):
            code, out, _ = self.run_cli("probe", "--beat", "test-beat")
        self.assertEqual(len(calls), 2, calls)
        self.assertEqual(code, 2)
        self.assertIn("BAD 404", out)
        self.assertEqual(out.count("multi reddit"), 2)


class EngageTests(WorkspaceTest):
    def entry(self, hours, **kw):
        e = {"ts": ago(hours), "beat": "test-beat", "platform": "reddit", "community": "a", "item": "reddit:x", "author": "u1",
             "kind": "ask", "status": "posted", "questions": ["q one"], "replies": []}
        e.update(kw)
        return e

    def test_pace_rules(self):
        cfg = self.cfg()
        E.save_ledger(cfg, [self.entry(0.5)])
        ok, reasons, _ = E.engage_check(cfg, "reddit", "b", "u2", "reddit:y")
        self.assertFalse(ok)
        self.assertIn("minutes ago", reasons[0])
        ok, _, _ = E.engage_check(cfg, "bluesky", "b", "u2", "bluesky:y")
        self.assertTrue(ok, "pacing is per platform")
        E.save_ledger(cfg, [self.entry(2)])
        ok, reasons, _ = E.engage_check(cfg, "reddit", "a", "u1", "reddit:x")
        self.assertFalse(ok)
        self.assertEqual(len(reasons), 3)  # community, author, item
        ok, _, _ = E.engage_check(cfg, "reddit", "a", "u1", "reddit:x", kind="thanks")
        self.assertTrue(ok, "a thank-you only obeys the gap and the daily cap")
        E.save_ledger(cfg, [self.entry(h, community=f"c{h}", author=f"u{h}", item=f"i{h}") for h in (2, 4, 6, 8)])
        ok, reasons, _ = E.engage_check(cfg, "reddit", "z", "uz", "iz")
        self.assertFalse(ok)
        self.assertIn("cap", reasons[0])
        E.save_ledger(cfg, [self.entry(2, status="drafted")])
        ok, _, _ = E.engage_check(cfg, "reddit", "a", "u1", "reddit:x")
        self.assertTrue(ok, "drafts do not count")

    def test_record_blocks_then_overrides(self):
        cfg = self.cfg()
        E.save_ledger(cfg, [self.entry(0.2)])
        args = ["engage-record", "--beat", "test-beat", "--community", "b", "--item", "reddit:z", "--url", "https://x", "--author", "u9",
                "--text", "hello"]
        code, _, err = self.run_cli(*args)
        self.assertEqual(code, 2)
        code, out, _ = self.run_cli(*args, "--override")
        self.assertEqual(code, 0)
        es = E.ledger(cfg)
        self.assertTrue(es[-1]["override"])
        self.assertTrue(os.path.exists(os.path.join(E.ledger_dir(cfg), "INDEX.md")))
        code, out, _ = self.run_cli("engage-update", "--item", "reddit:z", "--status", "posted", "--comment-url", "https://x/c")
        self.assertEqual(E.ledger(cfg)[-1]["comment_url"], "https://x/c")

    def test_questions_skip_recent(self):
        cfg = self.cfg()
        b = E.get_beat(cfg, "test-beat")
        first = b.questions()[0]["text"]
        E.save_ledger(cfg, [self.entry(1, questions=[first])])
        code, out, _ = self.run_cli("questions", "--beat", "test-beat", "--n", "10")
        self.assertNotIn(first, out)


class FetcherTests(unittest.TestCase):
    def test_pacing_and_404(self):
        tmp = tempfile.mkdtemp()
        slept = []
        calls = []

        def opener(req, timeout=0):
            calls.append(req.full_url)
            if req.full_url.endswith("missing"):
                import urllib.error
                raise urllib.error.HTTPError(req.full_url, 404, "nf", {}, None)
            return FakeResponse("<rss><channel></channel></rss>")
        try:
            f = S.Fetcher(tmp, "ua", host_gaps={"default": 100}, sleep=slept.append, opener=opener)
            f.get("https://a.example/one")
            f.get("https://a.example/two")
            self.assertEqual(len(slept), 1)
            self.assertGreater(slept[0], 90)
            text, cached, status = f.get("https://b.example/missing")
            self.assertEqual((text, status), ("", 404))
            f.get("https://b.example/missing")
            self.assertEqual(calls.count("https://b.example/missing"), 1, "a 404 is cached")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- stats (beat metrics)

GDELT_RAW = {"query_details": {"title": "q"}, "timeline": [{"series": "Article Count", "data": [
    {"date": "20260907T000000Z", "value": 10, "norm": 1000}, {"date": "20260908T000000Z", "value": 5, "norm": 1000},
    {"date": "20260914T000000Z", "value": 7, "norm": 1000}, {"date": "20260921T000000Z", "value": 4, "norm": 1000},
    {"date": "20260927T000000Z", "value": 1, "norm": 1000}]}]}
GDELT_VOL = {"timeline": [{"series": "Volume Intensity", "data": [
    {"date": "20260914T000000Z", "value": 0.2}, {"date": "20260915T000000Z", "value": 0.4}]}]}
WIKI_VIEWS = {"items": [{"timestamp": "2026091400", "views": 100}, {"timestamp": "2026091500", "views": 50},
                        {"timestamp": "2026092100", "views": 30}]}
TODAY = "2026-09-28"  # a Monday: complete weeks start 2026-08-03 ... 2026-09-21


class StatsTests(WorkspaceTest):
    def setUp(self):
        super().setUp()
        self.calls = []
        self.responses = {}

    # helpers
    def add(self, mid, **kw):
        args = ["stats", "add", "--beat", "test-beat", "--id", mid]
        base = {"question": "Q1 demand", "definition": "d", "unit": "count", "kind": "leading", "source": "tally:notes",
                "method": "tally", "cadence": "weekly", "grade": "C3"}
        base.update(kw)
        for k, v in base.items():
            args += ["--" + k.replace("_", "-"), v]
        return self.run_cli(*args)

    def note(self, posted, tools=()):
        d = os.path.join(self.tmp, "data", "test-beat", "notes", posted[:7])
        os.makedirs(d, exist_ok=True)
        n = len(os.listdir(d))
        with open(os.path.join(d, f"{posted}-n{n}.md"), "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: t\nposted: {posted}\ntools: [{', '.join(tools)}]\n---\nbody\n")

    def series(self):
        return E.load_series(self.cfg(), "test-beat")

    def seed(self, mid, values, version="1", start="2026-08-03"):
        d = dt.date.fromisoformat(start)
        rows = []
        for v in values:
            rows.append({"date": d.isoformat(), "metric": mid, "version": version, "value": "" if v is None else str(v),
                         "unit": "count", "source": "x", "note_ref": "failed: x" if v is None else ""})
            d += dt.timedelta(days=7)
        E.append_series(self.cfg(), "test-beat", rows)

    def fake_fetcher(self):
        def opener(req, timeout=0):
            self.calls.append((req.full_url, timeout, req.get_header("User-agent")))
            for key, resp in self.responses.items():
                if key in req.full_url:
                    if isinstance(resp, BaseException):
                        raise resp
                    if isinstance(resp, int):
                        import urllib.error
                        raise urllib.error.HTTPError(req.full_url, resp, "x", {}, None)
                    return FakeResponse(resp if isinstance(resp, str) else json.dumps(resp))
            raise AssertionError("unexpected URL " + req.full_url)
        return S.Fetcher(os.path.join(self.tmp, "local"), "everscout/test (+x; test@example.org)",
                         host_gaps={"default": 0, "api.gdeltproject.org": 0, "wikimedia.org": 0}, sleep=lambda s: None, opener=opener)

    def collect(self, *extra):
        f = self.fake_fetcher()
        with mock.patch.object(E, "fetcher", return_value=f):
            return self.run_cli("stats", "collect", "--beat", "test-beat", "--date", TODAY, *extra)

    def review(self, *extra):
        return self.run_cli("stats", "review", "--beat", "test-beat", "--date", TODAY, *extra)

    def status(self):
        return {m["id"]: m for m in E.load_metrics(E.get_beat(self.cfg(), "test-beat"))}

    def log(self):
        with open(os.path.join(self.tmp, "data", "test-beat", "log.md"), encoding="utf-8") as f:
            return f.read()

    # catalog
    def test_template_ships_a_metrics_catalog(self):
        code, out, _ = self.run_cli("stats", "list", "--beat", "test-beat")
        self.assertIn("notes-per-week", out)
        code, out, _ = self.run_cli("beat-check", "test-beat")
        self.assertEqual(code, 0, out)
        self.assertIn("1 metrics", out)

    def test_add_validates_and_versions(self):
        code, out, err = self.add("bad", source="gdelt:x", method="tally")
        self.assertNotEqual(code, 0)
        self.assertIn("tally source", err)
        with open(os.path.join(self.bd, "metrics.md"), encoding="utf-8") as f:
            self.assertNotIn("| bad |", f.read())
        code, out, err = self.add("layoff-news", source='gdelt-raw:"tech layoffs"', method="api", headline="yes")
        self.assertEqual(code, 0, err)
        m = self.status()
        self.assertEqual((m["layoff-news"]["status"], m["layoff-news"]["version"]), ("candidate", "1"))
        self.run_cli("stats", "add", "--beat", "test-beat", "--id", "layoff-news", "--grade", "B2")
        self.assertEqual(self.status()["layoff-news"]["version"], "1", "a grade change is not a definition change")
        self.run_cli("stats", "add", "--beat", "test-beat", "--id", "layoff-news", "--definition", "weekly articles, new query")
        self.assertEqual(self.status()["layoff-news"]["version"], "2")
        self.add("wiki", source="wikipedia:en.wikipedia/Layoff", method="api", headline="yes")
        m = self.status()
        self.assertEqual((m["wiki"]["headline"], m["layoff-news"]["headline"]), ("yes", ""), "at most one headline")
        self.assertIn("version 2", self.log())

    def test_beat_check_catches_bad_metric_rows(self):
        with open(os.path.join(self.bd, "metrics.md"), "a", encoding="utf-8") as f:
            f.write("| notes-per-week | Q1 x | d | count | leading | tally:notes | tally | fortnightly | Z9 | archived | 1 | 2026-09-27 | | | yes |\n"
                    "| ratio | Q1 x | d | ratio | leading | derived: notes-per-week / missing | derived | weekly | C3 | candidate | 1 | 2026-09-27 | | | yes |\n")
        code, out, _ = self.run_cli("beat-check", "test-beat")
        self.assertEqual(code, 1)
        for bit in ("duplicate id", "cadence", "Admiralty", "archive_reason", "unknown metric missing", "headline"):
            self.assertIn(bit, out)

    # collection
    def test_collect_tally_counts_shares_and_skips_before_first_note(self):
        self.note("2026-09-01", ["toolx"])
        self.note("2026-09-02", ["tooly"])
        self.note("2026-09-15", ["toolx"])
        self.add("toolx-share", source="tally:tools/toolx", unit="share %")
        code, out, err = self.collect()
        self.assertEqual(code, 0, err)
        rows = {(r["metric"], r["date"]): r["value"] for r in self.series()}
        self.assertEqual(rows[("notes-per-week", "2026-08-31")], "2")
        self.assertEqual(rows[("notes-per-week", "2026-09-07")], "0")
        self.assertEqual(rows[("notes-per-week", "2026-09-21")], "0")
        self.assertNotIn(("notes-per-week", "2026-08-24"), rows, "no zeros before the first note")
        self.assertEqual(rows[("toolx-share", "2026-08-31")], "50")
        self.assertNotIn(("toolx-share", "2026-09-07"), rows, "a share of zero notes is undefined")
        n = len(self.series())
        code, out, _ = self.collect()
        self.assertIn("current", out)
        self.assertEqual(len(self.series()), n, "a second collect in the same week appends nothing")

    def test_collect_gdelt_and_wikipedia(self):
        self.add("news", source='gdelt-raw:"tech layoffs"', method="api", grade="B2")
        self.add("share", source="gdelt:layoffs", method="api", unit="share %", grade="B2")
        self.add("wiki", source="wikipedia:en.wikipedia/Layoff", method="api", grade="A2")
        self.responses = {"TimelineVolRaw": GDELT_RAW, "TimelineVol&": GDELT_VOL, "wikimedia.org": WIKI_VIEWS}
        code, out, err = self.collect("--metric", "news,share,wiki")
        self.assertEqual(code, 0, err)
        rows = {(r["metric"], r["date"]): r["value"] for r in self.series()}
        self.assertEqual(rows[("news", "2026-09-07")], "15", "raw counts are summed over the week")
        self.assertEqual(rows[("news", "2026-09-21")], "5")
        self.assertEqual(rows[("share", "2026-09-14")], "0.3", "shares are averaged")
        self.assertEqual(rows[("wiki", "2026-09-14")], "150")
        urls = [c[0] for c in self.calls]
        self.assertTrue(any("startdatetime=20260803000000" in u and "enddatetime=20260927235959" in u for u in urls), urls)
        self.assertTrue(any("/per-article/en.wikipedia/all-access/user/Layoff/daily/2026080300/2026092700" in u for u in urls), urls)
        self.assertTrue(all(c[1] == 60 for c in self.calls), "the stats timeout applies")
        self.assertTrue(all("everscout" in (c[2] or "") for c in self.calls), "an honest User-Agent")

    def test_collect_records_failures_and_never_crashes(self):
        self.add("news", source="gdelt-raw:x", method="api")
        self.add("wiki", source="wikipedia:en.wikipedia/Nope", method="api")
        self.add("slow", source="wikipedia:de.wikipedia/Slow", method="api")
        self.add("busy", source="wikipedia:fr.wikipedia/Busy", method="api")
        self.responses = {"gdeltproject": "Please limit requests to one every 5 seconds", "Nope": 404, "Slow": TimeoutError("timed out"),
                          "Busy": 429}
        code, out, err = self.collect("--metric", "news,wiki,slow,busy")
        self.assertEqual(code, 0, err)
        fails = {r["metric"]: r for r in self.series() if r["value"] == ""}
        self.assertEqual(set(fails), {"news", "wiki", "slow", "busy"})
        self.assertEqual(sum(1 for c in self.calls if "Busy" in c[0]), 1, "a 429 is not retried during collection")
        self.assertIn("not JSON", fails["news"]["note_ref"])
        self.assertIn("timed out", fails["slow"]["note_ref"])
        self.assertEqual(fails["news"]["date"], "2026-09-21")
        gurl = [c[0] for c in self.calls if "gdelt" in c[0]][0]
        self.assertFalse(os.path.exists(self.fake_fetcher().cache_path(gurl)), "a refusal is not cached as data")
        self.assertIn("FAILED", out)

    def test_collect_manual_and_derived(self):
        self.add("postings", source="Indeed Hiring Lab release", method="manual", cadence="monthly")
        code, out, err = self.run_cli("stats", "collect", "--beat", "test-beat", "--metric", "postings", "--value", "80.5",
                                      "--date", "2026-08-01", "--note-ref", "https://example.org/release")
        self.assertEqual(code, 0, err)
        self.seed("a", [10, 20])
        self.seed("b", [5, 0])
        self.add("a")
        self.add("b")
        self.add("ratio", source="derived: a / b", method="derived", unit="ratio")
        self.collect("--metric", "ratio")
        rows = [r for r in self.series() if r["metric"] == "ratio"]
        self.assertEqual([(r["date"], r["value"]) for r in rows], [("2026-08-03", "2")], "division by zero is skipped")
        self.assertIn(("postings", "2026-08-01", "80.5"), [(r["metric"], r["date"], r["value"]) for r in self.series()])
        code, out, _ = self.collect("--metric", "postings")
        self.assertIn("skip", out, "manual metrics are never fetched")

    def test_fetcher_turns_a_read_timeout_into_a_fetch_error(self):
        self.responses = {"example.org": TimeoutError("timed out")}
        with self.assertRaises(S.FetchError):
            self.fake_fetcher().get("https://example.org/slow")

    # lifecycle
    def test_promote_needs_three_points_a_good_grade_and_a_yes(self):
        self.add("good", grade="B2")
        self.add("weak", grade="D4")
        self.add("young", grade="A1")
        self.seed("good", [1, 2, 3], start="2026-09-07")
        self.seed("weak", [1, 2, 3], start="2026-09-07")
        self.seed("young", [1, 2], start="2026-09-14")
        code, out, _ = self.review()
        self.assertIn("promote  good", out)
        self.assertIn("below C3", out)
        self.assertEqual(self.status()["good"]["status"], "candidate", "review alone never promotes")
        code, out, err = self.review("--promote", "young")
        self.assertNotEqual(code, 0)
        code, out, err = self.review("--promote", "weak")
        self.assertNotEqual(code, 0)
        code, out, err = self.review("--promote", "good")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.status()["good"]["status"], "active")
        self.assertIn("promoted good", self.log())

    def test_archive_stale_by_failures_and_by_age(self):
        self.add("failing")
        self.add("old")
        self.seed("failing", [5, None, None, None], start="2026-08-31")
        self.seed("old", [5, 6], start="2026-07-06")
        self.add("busy")
        self.seed("busy", [5, 6], start="2026-09-07")
        for _ in range(3):
            self.seed("busy", [None], start="2026-09-21")
        code, out, _ = self.review()
        self.assertNotIn("archive  busy", out, "three failed tries on one period are one failure")
        self.assertIn("archive  failing: stale, the source failed for 3 periods", out)
        self.assertIn("archive  old: stale, no new value", out)
        self.assertEqual(self.status()["old"]["status"], "candidate", "proposals only without --apply")
        before = len(self.series())
        self.review("--apply")
        st = self.status()
        self.assertEqual((st["failing"]["status"], st["old"]["status"]), ("archived", "archived"))
        self.assertTrue(st["old"]["archive_reason"].startswith("stale"))
        self.assertEqual(st["notes-per-week"]["reviewed"], TODAY)
        self.assertEqual(len(self.series()), before, "archiving never deletes rows")

    def test_archive_flat_and_trends_and_pairs(self):
        self.add("flat")
        self.add("up")
        self.add("up2")
        self.seed("flat", [100, 101, 100, 99, 100, 101, 100, 100])
        self.seed("up", [1, 2, 3, 4, 5, 6, 7, 8])
        self.seed("up2", [2, 4, 6, 8, 10, 12, 14, 17])
        code, out, _ = self.review()
        self.assertIn("archive  flat: flat", out)
        self.assertIn("up: ready", out)
        self.assertIn("trend rising", out)
        self.assertIn("up and up2 move together", out)
        code, out, _ = self.review("--json")
        self.assertEqual({f["id"]: f["action"] for f in json.loads(out)["findings"]}["flat"], "archive")

    def test_flat_threshold_is_configurable(self):
        cfgp = os.path.join(self.home, "config.json")
        with open(cfgp, encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["stats"] = {"flat_cv": 0.001}
        with open(cfgp, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        self.add("flat")
        self.seed("flat", [100, 101, 100, 99, 100, 101, 100, 100])
        code, out, _ = self.review()
        self.assertNotIn("archive  flat", out)

    def test_manual_archive_reasons_and_reactivate(self):
        self.add("gamed-one")
        self.add("better")
        code, out, err = self.review("--archive", "gamed-one")
        self.assertNotEqual(code, 0, "a reason is required")
        self.review("--archive", "gamed-one", "--reason", "gamed")
        self.assertEqual(self.status()["gamed-one"]["archive_reason"], "gamed")
        self.review("--archive", "better", "--reason", "superseded-by:gamed-one")
        self.assertEqual(self.status()["better"]["archive_reason"], "superseded-by:gamed-one")
        self.review("--reactivate", "gamed-one")
        self.assertEqual((self.status()["gamed-one"]["status"], self.status()["gamed-one"]["archive_reason"]), ("active", ""))

    # export
    def test_export_splits_versions_hides_archived_and_offers_charts(self):
        self.add("m1")
        self.add("gone")
        self.seed("m1", [1, 2], version="1")
        self.seed("m1", [5], version="2", start="2026-09-07")
        self.seed("gone", [3])
        self.seed("m1", [None], version="2", start="2026-09-14")
        self.review("--archive", "gone", "--reason", "irrelevant")
        with mock.patch.object(E, "find_chartwright", return_value=None):
            code, out, err = self.run_cli("stats", "export", "--beat", "test-beat")
        self.assertEqual(code, 0, err)
        self.assertIn("chartwright not found", out)
        path = os.path.join(self.tmp, "data", "test-beat", "stats", "export.csv")
        import csv as _csv
        with open(path, encoding="utf-8") as f:
            rows = list(_csv.DictReader(f))
        self.assertEqual({r["series"] for r in rows}, {"m1 v1", "m1 v2"}, "archived hidden, versions split, gaps dropped")
        with mock.patch.object(E, "find_chartwright", return_value=None):
            self.run_cli("stats", "export", "--beat", "test-beat", "--include-archived")
        with open(path, encoding="utf-8") as f:
            self.assertIn("gone", f.read())
        cw = os.path.join(self.tmp, "cw.py")
        with open(cw, "w", encoding="utf-8") as f:
            f.write("import sys\nout = sys.argv[sys.argv.index('--out') + 1]\nopen(out, 'w').write(' '.join(sys.argv[1:]))\n")
        with mock.patch.dict(os.environ, {"EVERSCOUT_CHARTWRIGHT": cw}):
            code, out, err = self.run_cli("stats", "export", "--beat", "test-beat")
            self.assertIn("chartwright found", out)
            self.assertIn("--chart small-multiples", out)
            code, out, err = self.run_cli("stats", "export", "--beat", "test-beat", "--charts")
        charts = os.path.join(self.tmp, "data", "test-beat", "reports", "charts")
        self.assertEqual(sorted(os.listdir(charts)), ["test-beat-metrics-line.html", "test-beat-small-multiples.html", "test-beat-sparklines.txt"])
        with open(os.path.join(charts, "test-beat-metrics-line.html"), encoding="utf-8") as f:
            self.assertIn("--series series", f.read())

    def test_list_json(self):
        self.seed("notes-per-week", [4, 5])
        code, out, _ = self.run_cli("stats", "list", "--beat", "test-beat", "--json")
        m = json.loads(out)[0]
        self.assertEqual((m["points"], m["last_value"]), (2, "5"))


if __name__ == "__main__":
    unittest.main()
