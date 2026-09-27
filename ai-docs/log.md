# Log

Append only, newest last. `## [YYYY-MM-DD] kind | summary`.

## [2026-09-26] build | everscout 0.1.0 built from indie-ai-scout 0.3.1

Mark asked for a public, topic-agnostic evergreen version of indie-ai-scout (any subject: AI video, global economics, down-tempo music), with indie-ai-scout later becoming a private layer on top. Four research passes ran in parallel (platform access with live endpoint checks; engagement ethics and platform rules; prior art; three sample beats); notes under `research/`. Built: `scripts/everscout.py` and `scripts/es_sources.py` (stdlib), `kb/` (conduct, platforms, method, schema, voice template), `beats/` (`_template` plus three starter beats), four evergreen skills registered with evergreen (lint OK), offline tests with synthetic fixtures, decisions (`decisions/`), the migration plan for indie-ai-scout (kept in indie-ai-scout's private doc set, `plans/2026-09-26-indie-ai-scout-on-everscout.md`).

Live smoke test on 2026-09-26 from Mark's PC with a scratch EVERSCOUT_HOME: every adapter answered (Reddit r/aivideo 25 items, HN, Mastodon tag, Bluesky profile RSS, Lemmy, Discourse, GitHub releases, YouTube, Hugging Face, Google News, Substack RSS); thread readers answered for Reddit, HN, Bluesky, Mastodon, Lemmy and Discourse. arXiv's API returned HTTP 406 after a few calls 4 seconds apart (the research agents were also calling it from this IP); the arXiv host gap is now 15 s and the fetcher retries 406 and 503 with backoff.

Bugs found by tests and the smoke test and fixed the same day: Windows cross-drive `commonpath`; notes not prefilled from the post title; the HN URL changed every call and defeated the cache (now hour-aligned); feed items took their community from a post's own hashtag instead of the watch-list row (broke per-community pacing).

## [2026-09-26] publish | public repo, v0.1.0, installed

Mark clarified mid-session: the core is "name a subject, get a scout"; the starter beats are examples. README and plugin descriptions now lead with that. Added multireddit batching (from the beats research: `r/a+b+c/new/.rss?limit=100` works logged out), seeded by the "about N a day" notes, which cut the ai-video Reddit plan from 15 requests to 8. Vocabulary matching changed: a line with aliases matches only its aliases (ids like `us`, `fed`, `warp` fired on ordinary words). Created github.com/m4bwav/everscout (public), tagged v0.1.0 with a GitHub Release, installed as `everscout@everscout` (user scope). Registered with everlast in mode repo.

## [2026-09-27] test | "set up a scout for ai video generation", two headless runs

Run 1 on 0.1.0: the skill triggered, copied the starter beat, backgrounded the probe and ended, so the probe died with the session (1/3; fixed in 0.1.1). Run 2 on 0.1.1: 3/3, refreshed the starter with a discovery pass, 46 sources all ok, full evidence on disk, 6.3 minutes, $1.55. Its fixes to the starter were backported and `probe --save` now merges (0.1.2). Not yet tested: a subject with no starter beat, which is the from-scratch path Mark cares most about.

## [2026-09-26] build | tech-hiring beat from scratch; everscout-ask skill; 0.2.0

Mark asked, "for a test and use", for a scout for developer and tech hiring, then mid-session for the scout to answer any question from its knowledge base plus whatever else it needs, "like a reporter" interrogated about their beat, and to run and push everything. The tech-hiring beat is the first built with no starter to copy: 33 sources (15 subreddits, 5 HN queries, 3 feeds, 3 Google News queries, 2 Mastodon tags, 5 data pages), probe 32 ok and 1 bad (interviewing.io has no feed, now a web row), 49 entities in 5 facets, 27 question seeds, 11 searches, an 11-chapter study outline; beat-check 0 errors, 0 warnings; data folder at `~/.everscout/data/tech-hiring` (default data_root; Mark's config.json is still absent). Research note `research/2026-09-26-tech-hiring-beat.md`.

The ask feature: skill `everscout-ask` (recall, grade enough/partial/none, research the gaps, answer with seen/new/disagreements/confidence/unknowns, save to `answers/`), CLI `recall`, `answers/` in index and lint; decision `decisions/2026-09-26-ask-the-beat.md`. The build also found that a verification fetch marks items seen and would empty the first scan: `fetch --peek` added, the real state reset (everscout-beat L-004). Rules pages are unreadable through Claude Code's fetch, old.reddit.com included (L-005). The CLI's dates are UTC (L-006). 30 offline tests pass; evergreen lint OK for everscout-ask and everscout-beat (two older lint issues in the beat skill fixed).

## [2026-09-26] index | rebuilt (3 entries)
