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

## [2026-09-26] migrate | indie-ai-scout now runs on everscout (private beat indie-ai-games); 0.2.1

Mark asked to park the indie-ai-scout skills that overlap everscout's, while keeping the indie scout and its knowledge base usable, so its migration plan's stages 1 to 3 ran first. The private beat and voice live in the private indie-ai-scout repository; the data and the one ledger for all beats live in the vault (`~/.everscout/config.json` now exists with `reddit_user`, `beat_dirs`, the beat's data path, `ledger` and `voice`). Checks: beat-check, validate --strict and lint all clean; tally counts equal the old ones; engage-check agrees with the old ask-check; recall answers from the 101 notes. The only engine change needed: `followups` matches imported replies by time (0.2.1). The indie-ai-scout plugin is disabled and its skills marked parked.

## [2026-09-26] tidy | five skill descriptions shortened; root plugin evals; 0.2.2

Asked to shorten the five descriptions with skill-tidy without losing triggers. Each rewrite passed `tidy.py check` (OK, no lost trigger, closest similarity equal or lower) and was applied (backups in the user's `~/.skill-tidy/backups/`). The engage/ask boundary set by the indie-ai-scout parking (0.4.0) is unchanged: indie scout-* skills are parked and point to everscout. Two quoted phrases merged into neighbours ('explain what's going on with' into 'what's the latest on'; 'what's new in a subject' into 'anything new this week'); 'is this AI' was a negative example in engage, not a trigger, and was dropped. Added `evals/` (claude plugin eval format, copied from chartwright's): 10 trigger cases each forbidding the other four skills, 2 unrelated decoys; 12/12 (scan cases rerun after a usage limit cut the first run). 30 offline tests pass.

## [2026-09-27] research | beat statistics: metric catalog, series CSV and lifecycle (design only)

Mark wants each beat to gather statistics over time, propose and retire metrics, and feed chartwright. Researched prior art (no skill does the full loop; GDELT DOC 2.0 and Wikimedia pageviews are keyless series sources; pytrends archived April 2025), reporter and CI practice (NICAR data library, KITs/KIQs, Admiralty grading) and metric selection and retirement (GQM, Lean Analytics, Goodhart, KPI sunset guides). Proposed `metrics.md` per beat, long-form `DATA/stats/series.csv` for `cw.py build --series metric`, and candidate/active/archived rules with judgment thresholds. Nothing implemented. Note: [research/2026-09-27-beat-statistics.md](research/2026-09-27-beat-statistics.md).
## [2026-09-27] index | rebuilt (3 entries)

## [2026-09-27] build | beat statistics; 0.3.0

Built the approved design from [research/2026-09-27-beat-statistics.md](research/2026-09-27-beat-statistics.md); decision: [decisions/2026-09-27-beat-statistics.md](decisions/2026-09-27-beat-statistics.md). `metrics.md` per beat (template and four starter beats ship candidates), append-only `DATA/stats/series.csv`, CLI `stats list|add|collect|review|export`, adapters tally, GDELT timelines, Wikimedia pageviews, derived and manual, lifecycle rules in `review`, chartwright-ready export with optional chart builds. Skills route to `kb/stats.md`; beat and report descriptions updated through skill-tidy check then apply. 45 offline tests pass (15 new); `claude plugin eval .` 12/12 after the description changes. Live: Wikimedia answered at once; GDELT answered the first call and then HTTP 429 with a plain-text "one request every 5 seconds" for many minutes (probably shared with the research session's calls), so collection now never retries and never caches a non-JSON body. The tech-hiring GDELT query `"tech layoffs"` was too narrow (0 to 3 articles a day); changed to `layoffs (tech OR software OR startup)`, which made it version 2 (the first real use of the version bump).

## [2026-09-27] index | rebuilt (4 entries)

## [2026-09-27] fix | GDELT cool-down; wiki-layoff promoted; 0.3.1

Promoted tech-hiring `wiki-layoff` to active on Mark's yes (`stats review --promote`). Probed GDELT once (16:38 UTC, 10 minutes after the last call, everscout User-Agent): still HTTP 429 with the plain-text "one every 5 seconds" body, so the block outlasts the published rate. Research: no official rate-limit page; issue reports see 429s at 5 to 30 s spacing and multi-minute blocks. Fetcher gained a per-host cool-down (1 h doubling, cap 24 h) that `stats collect` honours for GDELT; gap 10 s. The collect for GDELT v2 waits for the cool-down. indie-ai-games checked: beat files in the indie-ai-scout repo, data in the vault, run by everscout through config; no metrics.md added. Thresholds stay judgment until about 2026-12-27. Solution: [solutions/2026-09-27-gdelt-rate-limit.md](solutions/2026-09-27-gdelt-rate-limit.md).

## [2026-09-27] feature | pre-approved metric promotion; 0.3.2

`stats approve --beat B METRIC [--withdraw]` records a yes in advance in a new optional `approved` column of `metrics.md`; `stats collect`, `stats review` and `approve` promote approved candidates that meet the rule (3 points at C3 or better) and print and log `promoted X (pre-approved <date>)`. Old catalogs stay valid. Applied: tech-hiring `news-tech-layoffs` and indie-ai-games `news-ai-indie-games` (the latter in the indie-ai-scout repo) approved; the HANDOFF "Pending promotion" section replaced. 49 offline tests pass.

## [2026-09-27] beat | personal-sites created

Mark asked for a beat on how people, especially in tech and design, think about and design personal and professional sites and blogs, as the start of a site refresh and a new skill. Built with everscout-beat without the interview (the request said enough): 36 rows, then the probe found 5 bad. Fixes: IndieNews `en.atom` answers 404, so the row uses the granary Atom URL the page advertises; ooh.directory's feed is `/feeds/recently-added.xml` (the updated feed 404s); Codrops' feed answers 410 Gone, so it became a hand-read web row; the HN queries "personal site" and "indieweb" returned nothing in the window and were dropped. 34 sources ok. A 30-day peek (483 items) plus web research gave the first answer, saved in Mark's data folder: clarity of role over the "Hi, I'm" hero, slash pages and small-web features back, moves off Framer to cheap self-hosting, typography as the main lever, AI-built sites common and mocked when generic. Bash heredocs with apostrophes failed again here; files were written with the Write tool.

## [2026-09-27] beat | personal-sites: AI and visual design

Mark mostly wants a current visual design and asked about AI with personal sites, as a merge or a new beat. Merged: the communities are the same. Added research question 7, an AI and design facet, 9 sources (r/FramerDesign dropped: Reddit answered 429 twice, so it could not be verified) (Figma and Framer blog feeds 404; Sidebar, UX Collective, Awwwards and Creative Bloq feeds answer), and study chapter 04b. The answer in Mark's data folder: the dated look is now the AI default (Inter, purple gradients, glass, centred hero with three cards; wasitvibed.com checks 46 signals, avoid-ai-design 67); current is committed type, colour and texture plus a personal concept (retro OS, game maps, dithering on this month's Show HN); the working method is direction first, tokens and a no-list in DESIGN.md, build with an agent, audit for tells. That method is the planned skill's spine.
