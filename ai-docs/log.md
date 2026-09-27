# Log

Append only, newest last. `## [YYYY-MM-DD] kind | summary`.

## [2026-09-26] build | everscout 0.1.0 built from indie-ai-scout 0.3.1

Mark asked for a public, topic-agnostic evergreen version of indie-ai-scout (any subject: AI video, global economics, down-tempo music), with indie-ai-scout later becoming a private layer on top. Four research passes ran in parallel (platform access with live endpoint checks; engagement ethics and platform rules; prior art; three sample beats); notes under `research/`. Built: `scripts/everscout.py` and `scripts/es_sources.py` (stdlib), `kb/` (conduct, platforms, method, schema, voice template), `beats/` (`_template` plus three starter beats), four evergreen skills registered with evergreen (lint OK), offline tests with synthetic fixtures, decisions (`decisions/`), the migration plan for indie-ai-scout (kept in indie-ai-scout's private doc set, `plans/2026-09-26-indie-ai-scout-on-everscout.md`).

Live smoke test on 2026-09-26 from Mark's PC with a scratch EVERSCOUT_HOME: every adapter answered (Reddit r/aivideo 25 items, HN, Mastodon tag, Bluesky profile RSS, Lemmy, Discourse, GitHub releases, YouTube, Hugging Face, Google News, Substack RSS); thread readers answered for Reddit, HN, Bluesky, Mastodon, Lemmy and Discourse. arXiv's API returned HTTP 406 after a few calls 4 seconds apart (the research agents were also calling it from this IP); the arXiv host gap is now 15 s and the fetcher retries 406 and 503 with backoff.

Bugs found by tests and the smoke test and fixed the same day: Windows cross-drive `commonpath`; notes not prefilled from the post title; the HN URL changed every call and defeated the cache (now hour-aligned); feed items took their community from a post's own hashtag instead of the watch-list row (broke per-community pacing).

## [2026-09-26] publish | public repo, v0.1.0, installed

Mark clarified mid-session: the core is "name a subject, get a scout"; the starter beats are examples. README and plugin descriptions now lead with that. Added multireddit batching (from the beats research: `r/a+b+c/new/.rss?limit=100` works logged out), seeded by the "about N a day" notes, which cut the ai-video Reddit plan from 15 requests to 8. Vocabulary matching changed: a line with aliases matches only its aliases (ids like `us`, `fed`, `warp` fired on ordinary words). Created github.com/m4bwav/everscout (public), tagged v0.1.0 with a GitHub Release, installed as `everscout@everscout` (user scope). Registered with everlast in mode repo.
