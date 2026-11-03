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

## [2026-09-28] scan | first scan of all six beats

Mark asked to run the scout on one r/aigamedev thread (a fishing game's week 9 devlog), draft a question for its maker, and run every beat. The thread became a note in indie-ai-games; the question is drafted and waits for Mark's approval (in that beat's HANDOFF, not in the ledger). All six beats were fetched with `--max-age-days 7` (new listing only; top-of-week skipped to save Reddit time): indie-ai-games 3,600 items in 67 minutes, the five built-in beats 320 to 650 items in 8 to 11 minutes each. Notes written: indie-ai-games 29 (130 in total), ai-video 30, personal-sites 22, tech-hiring 25, global-economics 29, downtempo 24; every beat validates strict with 0 findings, was tallied, indexed and had stats collected (GDELT answered 429 once and cools until 18:38 UTC). Each beat's data folder has the log line and a rewritten HANDOFF with its runners-up under "Not yet distilled"; no beat has a report yet (indie-ai-games' weekly one is due).

How it ran: `ES fetch` for all beats in one background loop; subagents did the web searches and the non-Reddit items in parallel and queued Reddit URLs; one serial script ran `thread` then `new-note` for each queued Reddit URL (62 threads), and subagents filled the notes from the saved thread text. Reason: the pacing file has no cross-process lock (skills/everscout-scan/LEARNINGS.md `pacing-has-no-process-lock`). A Reddit URL with a non-ASCII slug fails in `thread`; percent-encoding it works (`non-ascii-reddit-url-fails`). Both are fix candidates for the CLI. Vocabulary grew in all five built-in beats (uncommitted in this repo) and in indie-ai-games (indie-ai-scout repo, including a new `art-in-code` workflow).

A checker read 18 of the 159 new notes against their sources: 3 ok, 15 fixed (small: dropped hedges, one commenter turned into "several", "about" on exact numbers, mostly in summaries); handle sweep clean. Learning `subagent-notes-drop-hedges`: the unsampled notes likely carry the same slips; sweep every summary line next time.
## [2026-09-28] solution | token-saving processes for thread, ledger, followups and housekeeping; five CLI additions proposed
## [2026-09-28] index | rebuilt (6 entries)
## [2026-09-28] index | rebuilt (6 entries)
## [2026-10-03] update | prepared for the Claude plugin directory: README Privacy section (host classes, request contents, no credentials, no posting), plugin.json homepage, documentationUrl, supportUrl, privacyPolicyUrl; "pass" wording fixed in two skill references; checklist clean (182 files, none over 256 KiB, no binaries); 49 tests OK; no version bump (no code change)
## [2026-10-04] update | the plugin icon (icon.png in .claude-plugin) for the Claude directory, chosen from two Z-Image candidates. Z-Image Turbo bf16, 9 steps, cfg 1, res_multistep/simple, seed 3964253010, prompt "flat vector app icon, bold simple shapes, minimal, centered single motif, thick clean outlines, high contrast, readable at small size, no text, no letters, no numbers, no words, no logos, square composition, a pair of binoculars, brass and black on forest green background"; white corners painted to the background (41, 182, 111)
## [2026-10-04] update | submitted to the Claude plugin directory, https://claude.ai/directory/manage/plugins/7ecd6362-ee1c-4b57-9afa-c3189520a458 (validated main@9f449d6, Scheduled check only, auto-publish on); holds: image reference in ai-docs/log.md, credential (4: research note, EVERSCOUT_* path settings, tests); status after submit: in review
## [2026-10-06] update | 0.3.3 for GitHub Copilot and awesome-copilot: root plugin.json (Agent Plugins 1.0, keywords cut to 10), skills link generated copies in references/kb/ (scripts/sync-skill-refs.py, --check in the test suite) because vally lint rejects `../../kb/` links; Mark chose synced copies over plain copies. vally-cli 0.17.0 lint 5/5
## [2026-10-10] update | ai-video weekly scan (25 notes; data outside the repo) and everscout-scan refresh (m 0.8): Reddit announced RSS ends 2026-11-13, no new public Data API requests after 2026-10-31, unregistered apps cut 2027-01-12, public Data API gone March 2027 (secondary sources, skills/everscout-scan/RESEARCH.md R-20261010-1); SKILL.md rule added (lane goes to the user's decision, never undocumented endpoints or scrapers), followups now run after fetch (L pacing-has-no-process-lock), injection eval case action-2 added, suite not re-run; ai-video vocab gained ~20 entities. Open decision: apply for Reddit Developer Platform access before 2026-10-31 or drop the Reddit lane; affects every beat and the plugin's es_sources Reddit code.

## [2026-10-11] research | Forums open to AI crawlers: live robots.txt of about 40 sites parsed for GPTBot, ClaudeBot, CCBot, Google-Extended, PerplexityBot; HN, Bluesky and Discord terms read; X and Reddit paid routes checked. Bluesky, HN (API), Lemmy, Discourse forums and discussions.unity.com are open; Reddit, Stack Overflow, X, Threads, LinkedIn closed; Discord forbids scraping and AI training on message content, bot reading only where invited. research/2026-10-11-forums-open-to-ai-crawlers.md. No platforms.md or adapter change yet.
## [2026-10-11] index | rebuilt (6 entries)

## [2026-10-11] research | Reddit after the API: Arctic Shift (free archive + API, live, scores settle after ~1.5 days, grey legal footing, future after March 2027 unknown per maintainer issue #76) is the only current reader; Devvit is subreddit-scoped (mods install), Pushshift mods only, Google CSE ends 2027-01-01. Plan for an Arctic Shift adapter, cross-platform pickup and user captures (screenshots or pasted text, at most five per scan) waits for the user: research/2026-10-11-reddit-after-the-api.md, plans/2026-10-11-reddit-lane-after-rss.md.
## [2026-10-11] index | rebuilt (7 entries)

## [2026-10-15] research | Reddit through Gemini's Google Search grounding: does not hold. The Google-Reddit deal licenses Google, not API callers; the Gemini API terms forbid letting third parties analyse, cache, mix or collect Grounded Results (so Gemini to Claude to notes breaks them at each step); the free tier has no search grounding for new users (Gemini 3+ paid only, 2.5 limited to past users); Reddit v. SerpApi/Perplexity survived dismissal 2026-07-31. `gemini-3.8-flash` is real; `claude-3-5-sonnet-latest` is retired. Plugin build paused for Mark's decision. research/2026-10-15-reddit-through-gemini.md.
## [2026-10-15] index | rebuilt (7 entries)

## [2026-10-15] update | 0.4.0: Reddit through the Arctic Shift archive (Mark chose this lane over Gemini, which Google's terms rule out). `reddit.reader` auto/rss/arcticshift (auto switches on 2026-11-13), settled-score window ending 36 h back, paging, points and comments on items, thread via /api/posts/ids and /api/comments/tree, search one subreddit; Fetcher paces x-ratelimit-reset on Reddit only. Live ai-video run: 1,904 posts from 14 subreddits in 48 requests, 2.5 min; a 422 on a deep r/Filmmakers page led to keeping earlier pages. 56 tests. Plan steps 3-4 (cross-platform pickup, capture requests) still open.
## [2026-10-15] update | next-session-prompt.md written (Reddit lane steps 3-4, then the Gemini backup after asking Mark). Mark relayed a Gemini reply saying only training a competing model is forbidden; the terms section "Grounding with Google Search" says otherwise, so the research note stands.
## [2026-10-15] plan | Reddit after 2027: find thread URLs without Gemini search, read them with Gemini URL context, distil in Claude (plans/2026-10-15-reddit-via-gemini-url-context.md); Stage 1 test waits on Mark's GEMINI_API_KEY. next-session-prompt.md rewritten for it.
## [2026-10-15] index | rebuilt (9 entries)

## [2026-10-15] note | Gemini URL context Stage 1 started and blocked: key set, but its Cloud project (268277778089) answered 403 SERVICE_DISABLED or "caller does not have permission" for 15 minutes after Mark found the API Enabled, and calls past the permission check hung at 60 s (plain calls too, so not URL context). Probe script, cases and fixes in notes/2026-10-15-gemini-url-context-probe.md; next-session-prompt.md updated.
## [2026-10-15] index | rebuilt (10 entries)

## [2026-10-15] research | Gemini URL context Stage 1 passed on gemini-3.5-flash-lite: key works now; all six Reddit threads read with the right title and body (fresh and edited posts match the current post, deleted post empty), 47 real comments in the settled thread, no comment shown invented, placeholders instead of removed text; usernames sometimes come back as comment text; Reddit pages come from Google's index (slug URL success, live fetch error). gemini-3.8-flash overloaded (503 or 60 s drop) and untested. research/2026-10-15-gemini-url-context-reddit-test.md; plan status updated; Stage 2 shape waits for Mark.
## [2026-10-15] index | rebuilt (10 entries)

## [2026-10-15] decision | Stage 2 shape: Mark chose the standalone public plugin (reads pages other fetchers cannot; setup skill for key, tiers and privacy; stdlib CLI); everscout stays keyless. Plan, HANDOFF and next-session-prompt.md updated; name to agree with Mark before the repo is created.
## [2026-10-15] update | Stage 2 built as fetchwright (name agreed with Mark; public repo m4bwav/fetchwright): stdlib CLI check/read, two skills (reader, setup advisor), 37 offline tests, live smoke test, size budget. Here: conduct rule 17 and kb/platforms.md keyed-sources row for the route (never Google Search for discovery; public threads only, free-tier privacy line; stop at the first 429); changelogs; plan status. Found: long word-for-word page copies are blocked as recitation (HTTP 400), so pages default to a digest.
## [2026-10-15] update | everscout-scan: the 2026-10-10 refresh (R-20261010-1 to -3, followups after fetch, injection eval action-2, ai-video vocab) was never committed; merged onto 0.4.0 with the Reddit rule rewritten for the Arctic Shift choice (C-20261015-2)
## [2026-10-16] build | everscout 0.5.0 branch: Reddit threads through fetchwright (opt-in), first live run stopped by Gemini's daily quota
Mark asked to wire everscout to fetchwright and test it live now. Built config `reddit.thread_reader` and `--thread-reader` (thread, new-note), a subprocess adapter in `load_thread` (config `fetchwright.cli`, `FETCHWRIGHT_CLI`, the installed plugin), cache, a 5 s Gemini pace, and a cool-down on fetchwright's exit 3 that follows Google's retry time; `followups` keeps the listing's reader. 65 offline tests with a fake CLI. Live on ai-video threads (Arctic Shift listings, bare permalinks read fine): 20 of 22 and 72 of 76 comments, all matching the archive, no handles; a 183-comment thread came back as broken JSON; the fourth read drew a 429, "limit: 20 requests per day on Free Tier" for gemini-3.8-flash. Stopped as the handoff requires; PR left open for Mark. No scan was run and no notes were written (the cool-down blocks fetchwright until 2026-10-17 00:00 UTC). Results: research/2026-10-15-fetchwright-thread-reader-live.md.
## [2026-10-16] decision | Mark's answers: quota fall-through, flash-lite first, merge and release 0.5.0 after the gate
fetchwright PR #2 (merged): a 429 naming one model's quota moves to the next model; exit 3 only when every model is out. Mark's config now runs `gemini-3.5-flash-lite` first through the fetchwright clone. Shortening the 2026-10-17 00:00 UTC cool-down was refused as weakening a safeguard, so the remaining live reads, the gate, the merge of #21, the scan and the 0.5.0 release wait for the next session (next-session-prompt.md).
## [2026-10-16] release | everscout 0.5.0: second live run passed the gate, a real ai-video scan through fetchwright
Mark approved shortening the Gemini cool-down to the one-hour minimum (only gemini-3.8-flash's quota was spent). With flash-lite first: 7 of 7 threads read (9 of 10 across both runs), all comments real, 74% of the archive's comments, the long thread read with `max_comments` 100 (now the default). A real ai-video scan read 7 of 8 kept threads through fetchwright (one was too new for Google's index) and wrote 9 notes to Mark's data folder. Eight tool entries added to the ai-video vocabulary. PR #21 merged, v0.5.0 tagged and released.
## [2026-10-16] update | YouTube outage line, first ai-video radar, Reddit discovery plan
Seven ai-video YouTube feeds 404ed on the 2026-10-16 scan: every YouTube feed did (Google's own channel, playlist and user forms too) while channel pages answered 200, matching forum reports of endpoint-wide 404s since December 2025. `fetch` now prints one line when every YouTube feed fails (1 test, 66 total); kb/platforms.md row. GDELT refuses this address on the first call (third scan running); options for Mark in research/2026-10-16-youtube-feeds-and-gdelt-refusals.md. Wrote the ai-video beat's first monthly radar in Mark's data folder (96 notes, lint 0). Planned Stage 2 step 4 (plans/2026-10-16-reddit-discovery-after-arctic-shift.md). fetchwright 0.2.0 still waits for Mark's go-ahead.
## [2026-10-15] index | rebuilt (12 entries)
## [2026-10-15] index | rebuilt (12 entries)
## [2026-10-16] update | Mark's answers: fetchwright 0.2.0 released and installed (fetchwright.cli dropped from his config; everscout finds the installed copy); ai-video metrics promoted and archived (#23); discovery build is next session's work
## [2026-10-16] build | Reddit discovery without a listing (plan steps 1 to 6), unreleased
Built on `feat/reddit-discovery`: `es_sources.reddit_ids_in` (every permalink form, redd.it, encoded links; skips media hosts, share tokens and ellipsis-cut ids) and `reddit_links` on feed, Mastodon and Bluesky items; pickup during `fetch` into `reddit_seen_elsewhere` (14 days, one mention per linking item, fetch window only); `elsewhere` on listed Reddit items; `discover list|add|mark` with ranking, the 24-hour hold and a coverage line; `captures` and `new-note --capture`; `fetchwright.max_reads_per_scan` (exit 6); notes record via, discovered, mentions. Scan skill Step 2 and procedure G, kb/platforms.md section, SCHEMA fields, conduct and AGENTS lines. 74 tests. Live check in a scratch local root (Mark's state untouched): one week of ai-video's 26 non-Reddit sources linked no Reddit thread; the first try picked up an August thread from an old blog post, which led to the fetch-window filter. Research note `2026-10-16-reddit-pickup-coverage-live.md`. Release as 0.6.0 waits for Mark.
## [2026-10-15] index | rebuilt (12 entries)

## [2026-10-16] scan | five stale beats (tech-hiring, personal-sites, global-economics, downtempo, indie-ai-games), 18 days after the last scan
One serial RSS fetch (17:54-19:06; indie-ai-games 39 minutes), five web-search subagents in parallel, offline triage subagents per beat, one serial script reading the 47 kept Reddit threads (`thread` then `new-note` from the cache, about 45 s each), then offline note-filling subagents from the saved thread text, then a checker sweeping every summary. 113 notes in all (tech-hiring 22, personal-sites 18, global-economics 24, downtempo 21, indie-ai-games 28); validate clean on every beat; logs and HANDOFFs rewritten. r/aigamedev and r/UnrealEngine5 RSS returned HTTP 500 twice an hour apart. New everscout-scan learnings: `subagent-bypassed-fetch-refusal` (a distil subagent sent a browser user-agent to Google News; every distil prompt now forbids that), `arctic-shift-last-resort` (Mark: Arctic Shift is a worst-case fallback, never a speed-up), and an update to `subagent-notes-drop-hedges` (counts in reception lines are now the commonest slip). Parallel subagents collided in the shared scratchpad and working directory: give each its own work folder and absolute paths. Vocab edits to the four built-in beats and LEARNINGS are uncommitted.

## [2026-10-23] refresh | everscout-engage (m 0.3, next due 2026-10-29)
Added the trigger-3 discovery eval case: a natural request that names no skill (Expo eval practice). The conduct.md GitHub row now names Bitcoin Core's quote-and-disclose policy and maintainers who limit issues to collaborators. Reddit dates hold; logged-out .json and old.reddit already need a login. The HN, mastodon.social, Bluesky and Discourse rules are unchanged. The search plan gains official-forum lines. trigger-3 has not been run yet. Detail: skills/everscout-engage/RESEARCH.md R-20261023-1.

## [2026-10-29] feature | beat-new scope flags and leads, for evergreen's beat offer
`beat-new --scope --question --feeds` seeds a beat from a caller; `leads --beat --since` lists notes and reports since a date. Evergreen reads them when it refreshes a unit linked to a beat. Released as 0.6.0 with the Reddit-discovery work that was sitting in Unreleased. A stats test seeded fixed September dates and went red once they aged past the stale rule; it now seeds relative to today. 75 tests pass.

## [2026-10-30] build | 0.7.0: beat literature and the everscout-library skill

Mark asked everscout to keep up with each beat's books (all-time canon, important recent, latest published), with scripts and a procedure to distil a provided book into the beat's knowledge and attached skills, plus the books themselves and books for his other plugins. Built `lit` (list, check, add, new, due, ingest, lint, distill), the Open Library adapter, `kb/literature.md`, the everscout-library skill and a literature.md for every built-in beat; Mark's three private beats got theirs in the indie-ai-scout repo (left uncommitted there: game-design and token-saving are another session's untracked folders). Three research agents did the book tables; quality and gaps in `research/2026-10-30-beat-literature.md`. Live `lit new` showed heavy Open Library noise and found the URL-encoded query bug (fixed: `lit_clean_query`). 79 tests.

## [2026-10-30] research | Rechecked every "Judgment call" book row

`lit due`: all tiers current. Three agents sought a second kind of evidence for the 53 one-source rows across eight beats: 37 kept, 15 dropped, Mark's two `have` books kept as they were (an agent had deleted them; never drop a `have` row). Intro sentences updated. Mark's private beats edited in the indie-ai-scout repo, left uncommitted. Detail and weak keeps: research/2026-10-30-beat-literature.md. First distillation waits for Mark's pick.

## 2026-10-30 (second session): Spelunky picked, file not found

lit due: all 8 beats current; Judgment-call recheck already done. Mark picked Spelunky as the first distill. Searched D:, Downloads and Documents for spelunky epub/pdf/mobi/azw: none. Waiting on the file path. No code changes.

## 2026-10-30 (third session): Spelunky file still missing

lit due: all 8 beats current. Searched C:, E:, F:, G: (depth 7, AppData skipped) for spelunky epub/pdf/mobi/azw/txt: none. Still waiting on the file path from Mark. No code changes.

## [2026-10-31] library | Spelunky distilled end to end

Mark gave the book folder. `lit ingest`, an agent read all four parts, learnings 24 principles and 14 changes, lint 0, Mark approved all: ludowright 0.1.9 (PR #16 merged, released), indie-ai-games vocab and questions committed in indie-ai-scout, study ch. 12 addition, `lit distill`, tally, index. Recorded as TESTS.md T-20261031-1.

## [2026-10-31] eval | everscout-library trigger cases 3/3

Continue prompt step 4. Added `evals/library-trigger-1`, `library-trigger-2`, `library-decoy-1`; `claude plugin eval . --case 'library-*'` passed 3/3 (baseline delta +0.25 on both triggers). TESTS.md T-20261031-2. Only open item: Mark's pick of the next book.

## [2026-10-31] library | AI Engineering ingested, changes proposed

Lit due: all current. Picked AI Engineering (a `have` book in two beats; feeds tokenwright, evergreen-test, fetchwright, local-delegate). `lit ingest` into token-saving; an agent read ch. 3-6, 9-10 sections; learnings 25 principles, 18 proposed changes, lint 0. Waiting for Mark's approval before applying.

## [2026-10-31] check | continue prompt: nothing due

lit due: all 8 beats current. Steps 2-4 already done. Waiting on Mark's next book: remaining `have` rows are Press Reset (Schreier) and AI Engineering (Huyen), both indie-ai-games. No code changes.

## [2026-10-31] library | Press Reset distilled end to end

Mark gave the file (AI Engineering went to another session). Ingested into indie-ai-games, read by an agent with three chapter readers, 24 principles, 12 changes, all approved: ludowright 0.1.10 (PR #17 merged, released), indie-ai-games vocab and questions (indie-ai-scout e791632), study ch. 01 and 12, book note. TESTS.md T-20261031-3. Next: Mark's next book pick.

## [2026-10-31] check | continue prompt: nothing to do

lit due: all 8 beats current. Spelunky and Press Reset distilled, trigger evals passed, AI Engineering is with another session awaiting Mark's approval of its 18 changes. No `have` book left undistilled; waiting on Mark's next book. No code changes.

## [2026-10-31] library | AI Engineering distilled end to end

Mark approved all 18 changes. Beat token-saving committed to indie-ai-scout (74306d9: questions, vocab, searches, study, metrics). tokenwright 0.2.6 (PR #20, habits Edges not middle and Memory by frequency, levers Result caching), fetchwright 0.2.1 (PR #6, result cache guidance in route.md), evergreen-protocol PR #36 (evergreen-test: pin the judge, label graders, agent efficiency evidence; no bump), local-delegate PR #9 (decide.md cascade rule). Note flags ch. 9 cache prices as 2024-dated. `lit lint` 0, `lit distill`, tally, index. TESTS.md T-20261031-4. The private evergreen fork's `git pull upstream master` conflicts in skills/evergreen-refresh/SKILL.md (not from this work); aborted and left for the fork's owner session.

## [2026-10-31] library | The Gamer's Brain ingested, changes proposed

Agent pick from Mark's downloads folder (Mark asked for the most helpful one). The file is the 2026 second edition. Added to the game-design canon tier, ingested; learnings: 25 principles, 20 proposed changes (beat files, ludowright ux-and-the-brain and playtesting, game-juice principles and juice-scan), lint 0. Waiting for Mark's approval, then apply, distill, tally, index.

## [2026-10-31] check | continue prompt: waiting on approval

lit due: all 8 beats current. The Gamer's Brain is ingested with 20 proposed changes awaiting Mark's yes (data folder books/the-gamers-brain learnings.md). No code changes.

## [2026-10-31] library | The Gamer's Brain distilled end to end

Mark approved all 20 changes. game-design beat committed to indie-ai-scout (e1155de, literature 52b3cf0); ludowright 0.1.11 (PR #18, ux-and-the-brain and playtesting), game-juice 1.3.1 (PR #6, P-18, P-19, juice-scan overlay check); edition line in book.md and the note. `lit lint` 20 applied, `lit distill`, tally, index. TESTS.md T-20261031-5. Next: Mark's next book.

## [2026-10-31] check | continue prompt: still waiting on approval

lit due: all 8 beats current. The Gamer's Brain's 20 proposed changes still await Mark's yes. No code changes.

## [2026-10-31] check | Gamer's Brain approval already applied

Mark said yes to all; a parallel session had already applied the 20 changes (#42, ludowright v0.1.11, game-juice v1.3.1, indie-ai-scout 52b3cf0, book note). The entry above saying "still waiting" is out of date. Added the missing data-folder log line. Next: Mark's next book pick.

## [2026-10-31] check | continue prompt: waiting on next book

lit due: all 8 beats current. Steps 2-4 done; all four `have` books distilled. Waiting on Mark's next book pick. No code changes.

## [2026-10-31] library | Play to Learn ingested, changes proposed

Agent pick (Mark: "choose one"): the only game book in his downloads folder not yet read by everscout or plugin-learnings. Ingested into game-design; learnings 25 principles, 18 proposed changes (beat vocab/questions/searches/literature, ludowright playtesting, balance-and-economy, core-loops-and-goals), lint 0. Ch. 4, 5, 9 read only to the 25k-char cut. Waiting for Mark's approval.

## [2026-11-01] library | Play to Learn distilled end to end

Mark approved all 18 changes. game-design beat committed to indie-ai-scout (de88bdf: vocab serious-games, gamification, achievement-design; two questions; three searches; Recent literature row OL20198942W); ludowright 0.1.12 (PR #19, kb playtesting, balance-and-economy, core-loops-and-goals; released v0.1.12). Reading caveats added to the book note. `lit lint` 18 applied, `lit distill`, tally, index. TESTS.md T-20261101-1. Slip: PR #19 was merged before its checks registered; the main run passed afterwards. Wait for `gh pr checks` to list checks before merging. Next: Mark's next book.

## [2026-11-01] check | continue prompt: waiting on next book

lit due: all 8 beats current. Play to Learn already distilled (entry above); no `have` book left. Waiting on Mark's next book pick. No code changes.

## [2026-11-01] library | Game Engine Architecture ingested, changes proposed

Mark picked Gregory (2nd ed., 2014; the 853-page copy is likely the 1st) as the most useful unread book for his plugins. Canon row added to game-design (Chalmers and CTU syllabi), ingested, read by three part readers. Learnings: 25 principles, 17 proposed changes (beat vocab/questions, ludowright R-58 to R-61 and three kb files, game-juice, unity-agent, threewright, roblox-agent, polywright-finish). Waiting for Mark's approval.

## [2026-11-01] library | Game Engine Architecture distilled end to end

Mark approved all 17 changes. Beat vocab, question and literature (indie-ai-scout e36a0d2, a2dd567); ludowright 0.1.13 (PR #20, rubric R-58 to R-61, three kb files; rubric now yellow at about 6,100 tokens), game-juice 1.3.2 (PR #7, P-28 barks, juice-scan input and lag checks), unity-agent 1.2.5 (PR #22, debug time controls and architecture traps; CI Linux leg pinned to ubuntu-24.04), threewright 0.6.8 (PR #17, Timer over Clock note), roblox-agent 0.1.8 (PR #20, streamed-instance references; merged with the failing Python 3.9 job, fixed by roblox-agent PR #21), polywright 0.5.2 (PR #42, clip conventions). Edition line in the note. TESTS.md T-20261101-2. Slip: apply agents annotated status cells, which lit lint rejects; keep the bare word. Next: Mark's next book.

## [2026-11-01] library | Generative Deep Learning ingested, changes proposed

Agent pick from Mark's downloads folder ("choose another"): Foster, 2nd ed. (2023), the only unread book there that a beat lists (ai-video, row `lead`); every game book in the folder was already read by everscout or plugin-learnings. Ingested into ai-video, read by two chapter readers (diffusion and multimodal; music and world models). Learnings: 23 principles, 13 proposed changes (ai-video vocab and questions, note, comfyui-gen, cinewright, artwright-judge, musicwright, ludowright), lint 0. Waiting for Mark's approval. Tool friction: none new (a Bash heredoc with apostrophes failed; Write tool used).

## [2026-11-01] library | Generative Deep Learning distilled end to end

Mark approved all changes. ai-video vocab (flow-matching, dit, video-vae, video-benchmarks, world-model split from physics), two questions, literature row distilled; comfyui-gen PR #121 (no CI), cinewright PR #68 (no bump, local checks), artwright 0.7.4 (PR #28), musicwright 0.1.4 (PR #19; CI 3.9 leg pinned to ubuntu-24.04), ludowright 0.1.14 (PR #21). Continue prompt: rules for an agent pick from Mark's folder and for parallel apply agents. TESTS.md T-20261101-3. Tool friction (open, T-20261101-3): `lit ingest`/`lit distill` edit the literature row in the config's beat dir (main clone), not the worktree; fix by letting `ES` take `--beat-dir` or by honouring an EVERSCOUT_BEATS override.

## [2026-11-01] tools | 0.7.1: three lit frictions fixed

lit due: all 8 beats current; no book waiting on Mark. Judgment-call rows: only Mark's own copies keep the label (Play to Learn, Press Reset, AI Engineering), as the 2026-10-30 recheck intended; nothing to drop. Fixed the open tool items (PR #44, released v0.7.1): `lit_change_status` reads the first word so `applied (v1.2, PR #3)` passes; `lit distill` writes applied `note` rows into the book note; `EVERSCOUT_BEATS` is searched before config beat_dirs so `lit` edits a worktree's literature.md. 81 tests (2 new). No readwright changes needed. Next: Mark's next book.

## [2026-11-01] check | continue prompt: waiting on next book

lit due: all 8 beats current. 0.7.1 left no open tool items; no `have` book undistilled. Waiting on Mark's next book pick (or "choose another"). No code changes.

## [2026-11-01] library | AI for Games ingested, changes proposed

Agent auto-pick (Mark: auto pick when the kickoff names none; continue prompt updated, 130225a): Millington, AI for Games, the only plugin-relevant book in his folder not yet read by everscout or plugin-learnings. Canon row in game-design (SDU DM810 textbook, Wrexham GME706 core reference; indie-ai-scout branch lit/millington), ingested, read by three part readers. Learnings: 25 principles, 12 proposed changes (beat vocab and questions, ludowright game-ai-for-designers, procgen and review, unity-agent and roblox-agent game-design references, note), lint 0. Waiting for Mark's approval. Tool friction (open, readwright): the PDF outline puts 3.4.5 to the end into one 1.85M-char section, and `rw.py grep` prints paragraph numbers, not character offsets, so readers binary-searched `--offset`; wanted: grep offsets or `read --at-para`, and splitting oversized PDF sections by printed headings.

## [2026-11-01] library | AI for Games distilled end to end

Mark approved all 12 changes. Beat vocab (12 terms) and an Enemy and NPC AI question group (indie-ai-scout PR #1); ludowright 0.1.15 (PR #22: game-ai-for-designers principles 22-26, three failure patterns, level-AI checklist; procgen seed streams and capped reject loops; review AI-depth sweep); unity-agent 1.2.6 (PR #23: enemy card awareness and states, AI performance and navigation); roblox-agent 0.1.9 (PR #22: same rows, Heartbeat staggering, PathfindingService costs); book note with the debug-hub rule and caveats. Tool fix: readwright 0.3.0 (PR #6) grep offsets, `read --at-para`, toc giant-section note. No everscout changes needed. TESTS.md T-20261101-4. Next: auto-pick the next book.

## [2026-11-01] library | Beginning Game AI with Unity ingested, changes proposed

lit due: all 8 beats current. Agent auto-pick: every `lead` book in Mark's folder (Hands-On GenAI, Kenworthy, Murch, Katz, DeSantis) was already read by plugin-learnings. First pick, Artists' Master Series: Color & Light, is a scanned PDF with no text layer (0 words in 384 pages), so it was dropped and its book folder removed. Picked Cossu, Beginning Game AI with Unity (Apress 2021): unread anywhere and it feeds unity-agent. Ingested into game-design; ch. 1 and 5 read, ch. 2 to 4 by grep. Learnings: 12 principles, 5 proposed changes (unity-agent game-design.md: NavMeshAgent traps, sight-check order, NavMeshSurface over the old bake; ludowright game-ai-for-designers principle 27, player verbs that feed AI senses; note), lint 0. Waiting for Mark's approval. Tool friction (open): `lit ingest` creates a book folder for a file with no text layer instead of refusing; checking the auto-pick against plugin-learnings took several manual greps (a `lit pick` that lists unread files in the folder would do it).

## [2026-11-01] library | Beginning Game AI with Unity distilled end to end

Mark approved all 5 and pre-approved future book changes unless controversial (continue prompt updated). unity-agent 1.2.7 (PR #24: NavMeshAgent traps, sight-check order, legacy bake), ludowright 0.1.16 (PR #23: principle 27, player verbs that feed AI senses), book note. `lit lint` 5 applied, `lit distill`, tally, index. TESTS.md T-20261101-5. Tool changes still open: `lit ingest` refusing text-less files, and a `lit pick`.

## [2026-11-01] library | 0.8.0 lit pick; Unity 2018 AI Cookbook distilled end to end

lit due: all 8 beats current; no Judgment-call rows to recheck. Built the two open tool items (PR #45, v0.8.0): `lit pick` lists unread book files (config `books_folder`, `books_read_index` set in Mark's config), and `lit ingest` refuses a file with no text. Auto-pick from it: Palacios, Unity 2018 AI Cookbook (unread anywhere, feeds unity-agent). Ingested into game-design, one reader: 14 principles, 5 changes, all applied: indie-ai-scout PR #2 (vocab n-gram, regret-matching), unity-agent 1.2.8 (PR #25, carving vs avoidance, manual NavMeshLink traversal), ludowright 0.1.17 (PR #24, principles 28-29), book note. Tool fix: readwright 0.4.0 (PR #7). T-20261101-6. Next: `lit pick` and the next book.

## [2026-11-01] library | 0.8.1; One-hour Skirmish Wargames distilled end to end

lit due: all 8 beats current; no Judgment-call rows to recheck. Auto-pick: `lit pick` listed Pixel Logic, FilmCraft and Blender Master Class, all already read by plugin-learnings (grep), so picked Lambshead, One-hour Ancient and Medieval Skirmish Wargames (2024): unread anywhere, a fast-play tabletop ruleset that feeds ludowright. Ingested into game-design, read directly (35k tokens): 17 principles, 7 changes, all applied: indie-ai-scout PR #3 (vocab tabletop-wargame, zone-of-control, card-driven-activation; a rules-cutting question), ludowright 0.1.18 (PR #25, ten principles over uncertainty, balance, scope, space; size check yellow from review-rubric.md, unchanged), book note. Tool fix: everscout 0.8.1 (PR #47, v0.8.1): lint accepts toc section names as citations; lit pick catches short titles with an author nearby (87 tests). No readwright changes needed. T-20261101-7. Next: `lit pick` and the next book.

## [2026-11-01] library | 0.8.2; Deep Reinforcement Learning Hands-On distilled end to end

lit due: all 8 beats current; no Judgment-call rows to recheck. Auto-pick: `lit pick` listed 83 unread, none beat-listed; Lapan, Deep RL Hands-On 3rd ed. (2024) is unread anywhere and feeds learned game agents. Recent-tier row, ingested into game-design, two part readers: 22 principles, 5 changes, all applied: indie-ai-scout PR #4 (vocab reward-shaping, self-play, curiosity, preference reward, imitation learning; a learned-agent question), ludowright 0.1.19 (PR #26, when RL is worth it; size check still yellow from review-rubric.md), unity-agent 1.2.9 (PR #26, ML-Agents training checklist), book note. Tool fixes: everscout 0.8.2 (PR #48, missing EVERSCOUT_BEATS fails); readwright toc `--depth` and chapter-number merge (Mark asked mid-session that every run feed readwright tips; continue prompt step 5 updated). T-20261101-8. Next: `lit pick` and the next book.

## [2026-11-01] library | 0.8.3; Foundations of Deep Reinforcement Learning distilled end to end

lit due: all 8 beats current; no Judgment-call rows to recheck. Auto-pick: Graesser & Keng (2019), unread anywhere; Co-Intelligence fit no beat and Brownlee's GAN book had only self-published evidence. Recent-tier row in game-design, one reader: 19 principles, 6 changes, all applied: indie-ai-scout PR #5 (vocab rl-debugging, action-space-design), ludowright 0.1.20 (PR #27, random baseline, reward hacking replay, reward signs), unity-agent 1.2.10 (PR #27, when training fails, action design; also re-encoded its CHANGELOG and log from cp1252 to UTF-8), book note. Tool fixes: everscout 0.8.3 (PR #50, v0.8.3). Slip: a chained `gh pr merge ... | tail` hid a not-yet-mergeable failure and the tag step ran; the wrong release was deleted at once and v0.8.3 re-cut on the merge commit. Never pipe a merge into tail before a tag. Open readwright items in HANDOFF. T-20261101-9. Next: `lit pick` and the next book.

## [2026-11-01] tools | readwright bugs fixed in the same session; continue prompt rule

Mark: fix every readwright bug a run reports in the same session, even at more token cost (continue prompt step 5). Fixed both Graesser items: readwright 0.5.1 (PR #9, v0.5.1): PDF outline sections start at their heading line (numbered headings in capitals or run into a paragraph split it), and a cut-off grep footer names `--section`. 63 tests, CI green. No open readwright items.

## [2026-11-01] library | 0.8.4; Grokking Deep Reinforcement Learning distilled end to end

lit due: all 8 beats current; no Judgment-call rows to recheck. Auto-pick: Morales, Grokking Deep RL (Manning 2020; Mark's copy is the MEAP V11 PDF), unread anywhere; its bandit, horizon and environment-design chapters add to the two RL books already read. Recent-tier row in game-design (Manning page, author teaches Georgia Tech's RL course), one reader: 15 principles, 6 changes, all applied: indie-ai-scout PR #6 (vocab multi-armed-bandit, rl-horizon; two learned-agent questions), ludowright 0.1.21 (PR #28), unity-agent 1.2.11 (PR #28), book note (MEAP edition line). Tool fixes: everscout 0.8.4 (`find_readwright` looks beside the main checkout when run from a `_wt/` worktree; it had printed the stale installed readwright 0.2.0); readwright 0.6.0 (PR #10: outline titles take page spacing, same-page sections split, escaped quotes, repeated `--section` adds, `--strip-boilerplate`, wider grep context in callouts). Mark's installed readwright plugin is still 0.2.0 (plugin cache); everscout now finds the clone. T-20261101-10. Next: `lit pick` and the next book.

## [2026-11-01] library | Video Generation with AI (Enochs) distilled end to end

Mark: "how about a recent book on video generation? anything with comfyui would be nice", and "always update it in plugin manager" (continue prompt step 5 and memory; readwright, ludowright and everscout updated in the plugin manager). Enochs (O'Reilly 2026) ingested into ai-video despite plugin-learnings' earlier pass, because Mark named the topic; the reader skipped what that pass took. 15 principles, 7 changes, all applied: ai-video vocab and questions, comfyui-gen PR #134, cinewright PR #73 (no bumps), book note. readwright 0.7.0 (PR #11) from the run's friction. Open: comfyui-gen's main clone is on another session's branch, so its junctioned skill lacks PR #134 until that clone is back on master and pulled. T-20261101-11. Next: `lit pick` and the next book.

## [2026-11-01] library | 0.8.5; Master Shots Vol. 1 (Kenworthy) distilled end to end

Auto-pick (no book named): Master Shots (series) is a `lead` in ai-video, unread anywhere, and a move off three RL books; Mark's copy is Vol. 1 only. One reader agent read ch. 1-2, 9, 11 (fights, chases, cars, arguments); ch. 3-8, 10, 12 unread. 18 principles, 9 changes, all applied: cinewright PR #74 (new cinewright-shots scene-setups.md, rules in camera-moves via shared/vocab, move-grammar, lens-choice, blocking, cutting-on-action; no bump), ai-video vocab and questions, book note. everscout 0.8.5: `lit` writes local dates (ingest had dated the learnings 2026-11-02 at 19:47 CST). readwright 0.8.0 (PR #12, v0.8.0, installed): `read --drop-repeated` drops recurring credit lines (212 on this book, off by default), and the distilling section now teaches `--section N-M --quiet --max-words`. cinewright's scrub found 9 hits in older ai-docs files (log, wiki note, a research note); the agent did not open the log and wiki-note ones. T-20261101-12. Next: `lit pick` and the next book.

## 2026-11-01: Co-Intelligence and Making Music

- Auto-pick: `lit pick` listed no beat-listed book. DeSantis (downtempo lead) was already in plugin-learnings, so Mollick, Co-Intelligence went to tech-hiring (AI and skilled work, apprenticeship; RL books skipped as over-represented). Added as a recent row (Forbes 2024 list).
- Two reader agents. 17 principles, 4 changes applied (PR #56). One reader's friction list was mostly wrong (toc already shows word counts, `--offset` and `grep --width` exist); the real bug, endnote back-links surviving `--drop-repeated`, was fixed in readwright 0.8.1 (PR #13), with a distilling tip on endnotes. Installed.
- Mark: "don't forget musicwright". Distilled DeSantis into downtempo from the 2026-10-22 read; five strategies never applied went into musicwright 0.1.5 (PR #20, tag v0.1.5). Installed. Tool item: `lit pick` should warn when a read-index book still has a `lead` row.
- No other everscout tool changes needed.

## [2026-11-01] library | 0.8.6; Color & Light (3dtotal) distilled end to end; readwright OCR

lit due: all beats current; no Judgment-call rows. Auto-pick: Artists' Master Series: Color & Light for ai-video (unread per `lit pick`, off the RL run). A previous session's worktree for it stopped at the no-text refusal: the PDF is a 384-page scan. Built readwright 0.9.0 `rw.py ocr` (Windows' built-in OCR via PowerShell 5.1, no install; cache in ~/.readwright/ocr); the book OCR'd in about 3 minutes. Recent row (Judgment call: Mark's copy). One reader: 21 principles, 11 changes, all applied: artwright 0.7.5 (PR #30), comfyui-gen PR #135 and #136, cinewright PR #75, beat vocab (relighting, light-physics) and questions. comfyui-gen had read the book that afternoon (PR #132); one duplicate bullet folded in by #136. Reader friction: a guessed page offset (+1, not -1) and a case-sensitive grep miss, both fixed in readwright 0.9.1 (PR #15). everscout 0.8.6: `lit pick` flags read-elsewhere lead rows; the ingest refusal names `rw.py ocr`. T-20261101-15.

## [2026-11-01] library | 0.8.7; In the Blink of an Eye and Film Directing Shot by Shot distilled

lit due: all beats current; no Judgment-call rows. No book named: `lit pick` listed seven beat rows read elsewhere, so Murch and Katz (ai-video canon) went first, from the 2026-10-22 cinewright read whose cinewright changes were already applied. Both files ingested; 15 and 16 principles; 6 changes, all applied (vocab rule-of-six, jump-cut, cut-on-the-look, coverage, axis-of-action, clearing-the-frame; four questions; notes). Friction: the Murch EPUB's OCR titles a section `€dge`, so lint refused a correct citation; 0.8.7 (PR #59) fixes the match, released and installed. Five C's stays `lead` (no file in the books folder). No readwright changes needed.

## [2026-11-01] library | 0.8.8; The Visual Story (Block) distilled

lit due: all beats current; no Judgment-call rows. No book named: of the five read-elsewhere rows `lit pick` listed, AI Engineering was already distilled (its `have` row only lags), Five C's and Don't Make Me Think have no file, so Block's The Visual Story (ai-video canon) went next, from the 2026-10-22 cinewright full read whose changes were already applied. 15 principles, 3 changes, all applied (vocab: visual-structure, contrast-affinity, story-intensity, space-type; two Visual structure questions; note with the 3rd-edition line). Friction: the PDF's metadata title is `ISO 15930 ... (PDF/X)`, so ingest misnamed the folder and missed the row; 0.8.8 falls back to the file name and finds the row by title in the file name. No readwright changes needed (the read was done earlier; the outline came out clean). T-20261101-17.

## [2026-11-01] library | Hands-On Generative AI with Transformers and Diffusion Models distilled

lit due: all beats current; no Judgment-call rows. No book named: of the four read-elsewhere rows `lit pick` listed, this ai-video recent `lead` was the only one with a file and not yet distilled, so it went next, from the 2026-10-30 comfyui-gen read (Ai/books/plugin-learnings/diffusion-hands-on-genai.md). `git grep` showed P1-P7 already in comfyui-gen (PR #104, LoRA note) and brandwright-train; P8 was half in musicwright, so musicwright PR #25 adds a copy-check row for every released cue (merged; Unreleased, no version bump, so no plugin update). 16 principles, 4 changes, all applied: vocab (guidance-scale, noise-shift, img2img-strength, inpainting, refiner-pass, dreambooth; aliases on lora-training and video-benchmarks), four Diffusion settings questions, note. Tool change: kb/literature.md step 0 tip to grep target repos for an earlier read's proposals. No readwright changes needed (no new reading of the file). T-20261101-18.

## [2026-11-01] library | Talking From 9 to 5 (Tannen) distilled into tech-hiring; everscout 0.8.9, readwright 0.9.2

lit due: all beats current; no Judgment-call rows. No book named and no beat-listed file unread, so auto-picked Tannen (1994): off the RL and ai-video run, and tech-hiring had nothing on how interviewers read candidates' talk. Added a canon row (Evergreen State College programme, in print). Two parallel reader agents; 17 principles; 4 changes applied (vocab Interview judgement section, four question seeds, a study perspective, note) in PR #64. TESTS.md T-20261101-19.

Tool changes: everscout 0.8.9 (cut book slugs no longer end on a stop word; old folders still resolve). readwright 0.9.2 (PR #16): the character-cut footer offers `--max-chars N`, and the skill tells book runs to give reader agents that flag (both readers had sampled long chapters). Both released and updated in the plugin manager. Chapters 5, 6 and 9 were read only in part; a later pass could finish them.

## [2026-11-01] library | The Venture Alchemists (Lalka) distilled into global-economics; readwright 0.9.3

lit due: all beats current; no Judgment-call rows to recheck. No book named and no beat-listed file unread, so auto-picked Lalka (2024): global-economics had no distilled book, and the beat had nothing on market power, venture finance or gig work. Added a recent row (`have`, Judgment call: Mark's copy). Two parallel reader agents; 15 principles; 4 changes applied (five Themes vocab entries, four question seeds, an IO-economist study perspective, note). Verdict: skim ch. 4, 7, 14 and the Epilogue; argued from personalities and press numbers, dated by Uber's and Palantir's profits and the 2024 Google ruling. TESTS.md T-20261101-20.

Tool changes: readwright 0.9.3 (PR #17): EPUB note references print as `[40]` instead of fusing with the sentence; `rw.py outline` aliases `toc`; distilling tip in the skill. No everscout tool changes needed.

## [2026-11-02] library | Inside Palantir rejected (skip); everscout 0.9.0

lit due: all beats current; no Judgment-call rows to recheck. `lit pick`: no beat-listed file unread; auto-picked Elsen, *Inside Palantir* for global-economics (the fewest books read; follows The Venture Alchemists). The book is self-published, 14k words, with no notes and chapter 3 missing; spot checks found the i2 suit (settled Feb 2011) and the Labor Department hiring case (consent decree Apr 2017) misdated, and a Karp Senate hearing on Cambridge Analytica with no record. Row `skip`; learnings and a book note record why. TESTS.md T-20261102-1.

Tool changes (0.9.0): `lit ingest` warns on a short book with no notes, sources or index; kb/literature.md step 1a (reliability check before distilling); `lit distill` keeps a `skip` row. Mark's tip recorded in kb/literature.md "Beyond books": tutorial sites, product and open-source forums and community threads often hold know-how and undocumented options that books and docs miss; they go into a beat's sources.md and searches.md. No readwright changes needed (the short EPUB read cleanly with `--max-chars`).

## [2026-11-02] library | Invisible Women (Criado Perez) distilled into tech-hiring; everscout 0.9.1, readwright 0.10.0

lit due: all beats current; no Judgment-call rows to recheck. No book named and no beat-listed file unread, so auto-picked Criado Perez, *Invisible Women* (2019): off the RL and ai-video run, and tech-hiring had nothing on screening bias, meritocracy or AI-ranker proxies. Canon row (Royal Society Science Book Prize 2019, FT and McKinsey Business Book of the Year 2019; OL20157508W). Reliability check passed (Random House, endnotes, index); of four spot checks, the Google pay-audit testimony and Snyder's review study pass, the blind-audition result is contested, the "70%" speech-recognition figure misreads an effect size. Two parallel reader agents; 14 principles; 4 changes applied (vocab section, four questions, study perspective, note) in PR #70. Verdict: read ch. 4 first, then ch. 3 and the Introduction; follow each figure to its source. TESTS.md T-20261102-2.

Tool changes: everscout 0.9.1 (`lit add` links a book ingested before its row existed; it had stayed `lead` with book_id `-`). readwright 0.10.0 (PR #18): an untocced endnotes file after Endnotes was listed as `Chapter 13`; now `Endnotes: Chapter 13`, and `rw.py note` resolves a marker by chapter. The readers' other reports (`priori-ties`, `cost of€500`, `[39]` in place of 30, typos) are in the EPUB's own XHTML, checked raw; the skill now says to check the source before calling a reader bug. Both released and updated in the plugin manager.

## [2026-11-02] library | Prompt Engineering for LLMs (Berryman, Ziegler) distilled into token-saving; everscout 0.9.2

lit due: all beats current; no Judgment-call rows to recheck. With no book named, the session first auto-picked Phoenix and Taylor, *Prompt Engineering for Generative AI* (O'Reilly 2024) for token-saving (evidence: GOTO Book Club session) and ingested it (row `reading`, a few sections read). Mark then picked Berryman and Ziegler, *Prompt Engineering for LLMs*, already a `lead` row in token-saving recent (its authors built Copilot's context handling), so the session switched: the Phoenix book stays `reading`, next in line. Read 14 sections (ch. 2, 5, 6, 7, 8, 9); 15 principles; 4 changes all applied: vocab Levers prompt-assembly, elastic-snippets, hierarchical-summary, tool-count and Valley of Meh aliases; three question seeds (indie-ai-scout PR #7, #8, which also set both AI Engineering rows `distilled`); tokenwright 0.2.13 (PR #41): Outline first row gains "the biggest part that fits", levers.md gains fewer tools in view and summarize up the tree; book note. Verdict: ch. 6 is the best treatment of fitting context to a token budget the beat has seen; read ch. 4-6 and 8.

Tool changes: everscout 0.9.2 (PR #72): `lit pick` looks in subfolders; it had missed Mark's pick in `Prompt Engineering for LLMs/`. readwright 0.10.1 (PR #19): U+2010 and soft-hyphen splits rejoined (pdftotext had already joined the lines with a space), `N | title` and `title | N` running heads at a page edge dropped by default for PDFs; distilling tip added. All three plugins updated in the plugin manager. Open: running heads without a pipe; paragraphs split at page breaks.

## [2026-11-02] library | Prompt Engineering for Generative AI (Phoenix, Taylor) distilled into token-saving; readwright 0.10.2

lit due: all beats current; Judgment-call rows are all distilled or `have`. Finished the book left `reading` last session (HANDOFF said distil it next). Reliability: O'Reilly, named authors, fine. Two parallel reader agents; 14 principles; 3 changes applied (vocab Levers history-trimming, few-shot-budget, chunk-overlap and progressive-summarization aliases; three question seeds; note on deprecated LangChain memory classes and old tiktoken encodings) in indie-ai-scout PR #9. Verdict: skim p. 40-51, 103-118, 203, 240, 275-276; Berryman and Ziegler covers the same ground better. TESTS.md T-20261102-4.

Tool changes: readwright 0.10.2 (PR #20, installed): running heads without a pipe dropped, sentences split at a page break rejoined, words split with no hyphen rejoined when the joined word appears in the book, lost compound hyphens restored, figure captions start a paragraph. Left open (pdftotext plain output has no layout data): code blocks flattened, tables and two columns read column by column, definition lists and sidebar headings run into the body; a fix needs `pdftotext -bbox-layout`. No everscout tool changes needed.

## [2026-11-02] library | The Five C's of Cinematography (Mascelli) distilled into ai-video; everscout 0.9.3, readwright 0.11.0

lit due: all beats current; no Judgment-call rows to recheck. No book named, so auto-picked. `lit pick`'s first candidates were wrong: Zhu, *Using Stable Diffusion with Python* had been read 2026-10-31 in comfyui-gen's notes (on a branch its shared clone is not on), and Krug, *Don't Make Me Think* showed as read elsewhere only because a reading list named it. Picked Mascelli (ai-video canon `lead`, file in the folder, read 2026-10-22 for cinewright): the EPUB is page images, so it ingested from the DjVu twin. Distilled from the earlier read with `rw.py grep` checks; 14 principles; cinewright already held them, so 3 changes went to the beat (vocab, questions, note). lint 0, distill, tally, index, beat-check 0. Trigger evals (step 4) not run this session.

Tool changes: everscout 0.9.3 (PR #75): reading lists ignored in the read index, `<folder>@<ref>` read-index entries, folder-name matching, ingest passes readwright's note on. readwright 0.11.0 (PR #21, built by a sub-agent that lost its login before reporting; finished and verified here): image-only EPUB OCR, ALL-CAPS heading split for one-section books, PDF code blocks, and a fix so topic heads on facing pages are not chapters. Both installed through the plugin manager.


## [2026-11-02] library | User Friendly (Kuang, Fabricant) distilled into personal-sites; readwright 0.11.1

lit due: all beats current; no Judgment-call rows to recheck. No book named and no beat-listed file unread, so auto-picked Kuang and Fabricant, *User Friendly* (2019) for personal-sites, which had nothing distilled; the plugin-learnings index had not read it (it skipped only consumer AI books such as Reverse Centaur). Canon row (Amazon Best Books of 2019; NYT Book Review). Reliability: FSG, named authors, chapter notes; passed. Two reader agents; 14 principles; 4 changes applied: vocab Usability section (skeuomorphism, dark-patterns, usability-testing, curb-cut), three question seeds (misreads by first visitors, links that open a tab, download or mail, an honest AI feature with a way out), sitewright-audit Step 2 usability pass (sitewright PR #8, merged; version unchanged at 0.1.0, so the installed copy refreshes at its next bump), book note. T-20261102-6.

Tool changes: readwright 0.11.1 (PR #22, v0.11.1, installed): a `--max-chars` cut ends at a paragraph, line, sentence or word break in the piece's last quarter and `--offset` resumes there; distilling tip says to give reader caps a margin. The readers' other wishes (label image captions as captions; a size preview before reading) are noted, not built. No everscout changes needed. Leftover: an undeletable empty folder `Ai/readwright-wt-paracut` (permission denied, like readwright-wt-fivecs; delete by hand).

## [2026-11-02] library | The Reverse Centaur's Guide to Life After AI (Doctorow) distilled into global-economics; readwright 0.12.0

lit due: all beats current; no Judgment-call rows to recheck. No book named and no beat-listed file unread; auto-picked Doctorow's 2026 book for global-economics (AI-investment economics, labour substitution; the beat had one distilled book and none of its canon is in Mark's folder). Reliability check passed 3/3. 18 principles; vocab (5 themes), questions (3), note applied (T-20261102-7). It is polemic, not data: treat its crash forecast and "every lab loses money" as claims to test.

Tool changes: readwright 0.12.0 (PR #23): `read --out-dir DIR` writes one file per selected section. No everscout tool changes needed.

## [2026-11-02] library | Guerrilla Marketing (Levinson, 4th ed.) distilled into indie-ai-games; everscout 0.9.4, readwright 0.13.0, sitewright 0.2.0

lit due: all current. Auto-pick (none beat-listed in the folder): Guerrilla Marketing, for indie-ai-games' reception and marketing questions. 17 principles, 7 changes applied: owned-audience and cross-promotion vocab, three Reception questions (indie-ai-scout PR #10), sitewright-audit one-action-per-landing-page check (sitewright PR #9, released 0.2.0 with its unreleased work, installed), dated-parts note. Verdict: ch. 1-6, 8 and the online sections are worth two hours for a solo dev; Parts II-III are 2007 tactics.

Tool changes: everscout 0.9.4 (PR #79, installed): `lit pick` flags slug file names of books read elsewhere; lint hint for quoted change text. readwright 0.13.0 (PR #24, installed): `read --compact`; distilling tip on briefing reader agents with `--out`. readwright's CI was still pending at merge (watching). Leftover undeletable empty worktree folders: everscout-wt-pickslug, readwright-wt-compact, indie-ai-scout-wt-guerrilla.

## [2026-11-02] library | Essentials of Economics (Mateer, Coppock, O'Roark) distilled into global-economics; everscout 0.9.5, readwright 0.13.1

lit due: all current; no Judgment-call rows to recheck. No book named. `lit pick` first showed `GenerativeDeepLearning.pdf`, but Foster's 2nd ed. was already distilled into ai-video (PR #43, from the EPUB): the PDF's CamelCase name never matched. Fixed in 0.9.5 with a test. No beat-listed file left unread, so auto-picked *Essentials of Economics* (Norton 2016) for global-economics, which had no grounding text on reading data releases. Two reader agents (ch. 10-13 and ch. 14-18). 16 principles; 6 changes applied (vocab, questions, note); lint 0, distill, tally, index, beat-check 0 errors (1 warning: a 2016 book in the recent tier, kept as Mark's copy). Verdict: ch. 11 on measurement is the useful part; its Fed-tools chapter predates the ample-reserves system. T-20261102-9.

Tool changes: everscout 0.9.5 (`lit pick` CamelCase). readwright 0.13.1 (PR #25): escaped line breaks in PDF outline titles, ligatures spelled out, a textbook reading tip. Trigger evals (step 4) not run this session.

## [2026-11-02] library | Epistemic Injustice (Fricker) distilled into tech-hiring; everscout 0.9.6, readwright 0.14.0

lit due: all beats current; no Judgment-call rows to recheck. No book named. `lit pick` led with *FilmCraft Cinematography*, already read on 2026-10-22 (plugin-learnings INDEX): the 0.9.5 CamelCase split hid it, fixed. Auto-picked Fricker's *Epistemic Injustice* for tech-hiring because it theorises credibility bias in judging people, beside the beat's Criado Perez and Tannen sections. Canon row (Guelph and Lorraine syllabi, diversity reading list; Open Library OL9331207W). Reliability passed on provenance (OUP, notes, index; conceptual, no figures). One reader agent; 22 principles; 4 changes applied (T-20261102-10).

Tool changes: everscout 0.9.6 (`lit pick` CamelCase only without separators; `lit ingest` titles release-style file names), tests for both. readwright 0.14.0 (PR #26, v0.14.0, installed): `toc --group`, running heads dropped under `--strip-boilerplate`, reader-brief grep tip. Left open in readwright: footnotes inline at page foot (needs the `-bbox-layout` PDF layout work). Trigger evals (step 4) not run this session.

## 2026-11-02 Blender book question

- Mark asked for the most important Blender book overall, from the last year, and for AI with Blender. His folder has only the 2007-2012 mini-pack, which plugin-learnings already covered (blender-polywright.md). Candidates found: Blain, *The Complete Guide to Blender Graphics* (overall); Lupiani, *Blender Scripting with Python* (Apress, 2025; Blender 4, add-ons, procedural meshes) for the last year and for AI/agent bpy work. No real generative-AI Blender book found; the 2026 Blender 5.x guides are unreviewed self-published titles. No book distilled; waiting for Mark to get Lupiani.
- Update: Blain 6th ed. found at D:/RawStorage/BigDownloads/Unorganized/John M Blain - The Complete Guide to Blender Graphics (6th Ed).epub; already grepped in plugin-learnings (Boids only). The one Blender book there not yet distilled: python-scripting-blender-animations/ (Packt, *Python Scripting in Blender*, Blender 3.x). It is the best next pick for polywright (bpy for agents). Blain 6th ed. full read is the second choice.

## [2026-11-02] library | Python Scripting in Blender (Acampora) distilled into game-design; polywright 0.5.3, readwright 0.15.0

Mark said to go ahead with the selected Blender Python book: Acampora, *Python Scripting in Blender* (Packt 2023, Blender 3.3), from the folder python-scripting-blender-animations. lit due: all current. Reliability passed (Packt, named add-on author, reviewer; 4/4 API spot checks pass in code, prose misnames matrix_parent_inverse and view_layer.objects.active). Two reader agents; 17 principles; 7 changes applied: game-design vocab (blender-python, blender-drivers) and two question seeds (indie-ai-scout PR #11), polywright 0.5.3 (PR #43, tag v0.5.3; new references/bpy-recipes-motion.md because bpy-recipes.md is past its token line), note. Verdict: ch. 2, 4, 8-9 and 12 are the core for bpy work; ch. 3, 5, 6 dated by the 4.2 extension system; read with the 4.4 and 5.0 release notes. T-20261102-11.

Tool changes: readwright 0.15.0 (PR #27, installed): CRLF and no-break-space in code blocks, one-pre-per-line listings joined, `grep --after N`, offset footer says "show the rest", continue hint quieter, multi-section `--section 61,80` documented, code-over-prose distilling tip. The reported lost indent was in the EPUB itself. No everscout tool changes needed. polywright release note: push the tag only; its workflow creates the release. The stuck LEARNINGS edit in the polywright main clone was landed as polywright PR #44; the main clone was pulled and the installed plugin updated 0.3.0 -> 0.5.3.

## [2026-11-02] library | AI Superpowers (Kai-Fu Lee) distilled into global-economics; readwright 0.15.1

Kickoff (Mark's session) ran `lit due` (all current, no Judgment-call rechecks) and auto-picked Lee, *AI Superpowers* (2018): unread in Mark's folder, in no beat's books or the plugin-learnings index, and global-economics lacked a US-China AI and jobs text. Reliability passed. 18 principles; 5 changes applied (vocab us-china-ai-race, chip-export-controls, ai-job-exposure, universal-basic-income, guidance-funds; three Interpretation questions; note). Aged claims: generative AI is missing from the four-waves map; the data-beats-research thesis failed as frontier labs and compute led; chips, a side note in 2018, became the central front; the 40-50% jobs figure is task exposure due about 2033 with no mass unemployment by 2026; US-China cooperation turned into export controls. The China platform chapters (copycats, going heavy, subsidy wars, local-official targets) aged well. T-20261102-12.

Tool changes: readwright 0.15.1 (PR #28, v0.15.1, installed): `read --out --max-chars` cuts at a clean break and prints where to resume. No everscout tool changes needed. Note: global-economics is a built-in beat in this repo, so its book run needs an everscout worktree, not an indie-ai-scout one.

## [2026-11-02] library | FilmCraft Cinematography distilled into ai-video; everscout 0.9.7, readwright 0.16.0

lit due: indie-game-marketing canon and recent due, but that beat was made minutes earlier by another session (untracked in the shared clone, marketwright feed), so it was left alone. No Judgment-call rows to recheck. Auto-picked *FilmCraft: Cinematography* because HANDOFF listed it as read 2026-10-22 and never distilled, and ai-video is the beat it fits. Evidence: NYFA's recommended cinematography books. cinewright already took the 2026-10-22 rules, so this run read the parts that read skipped (Ballhaus, Coutard, Cardiff, Young, glossary): 14 principles, vocab and questions applied (PR #87).

Tool changes: everscout 0.9.7 (`lit lint` accepts interviewee names from `INTERVIEW (in: ...)` toc titles; test). readwright 0.16.0 (PR #29): `terms` view for glossaries; test. Trigger evals (step 4) not run this session.
## [2026-11-02] discord | Discord through the user's own invited bot (0.10.0)

Mark asked for a free, legal way to read Discord, with as much bot code in the plugins as possible and current setup steps; the agent calls the bot (no forwarding to an AI API). Research (Developer Policy read through fetchwright, docs.discord.com gateway, message, reference and rate-limit pages) is in `research/2026-11-02-discord-bot-access.md`. Built `scripts/es_discord.py` (REST only, nothing hosted), source kind `discord`, per-host auth headers in the Fetcher, `kb/discord.md`, and the read-only decision. Tests 109 pass (six new). Untested live: no bot token on this machine yet; guild search for bots is undocumented. fetchwright and readwright got pointers (Discord pages are login-walled; read them with es_discord.py).

## 2026-11-02 (later): Discord continue prompt run

`es_discord.py check` returned `no-token`; stopped at step 2 of the continue prompt. Waiting on Mark for the bot application, settings and DISCORD_BOT_TOKEN (kb/discord.md steps 1-3). No code changed.

## [2026-11-02] discord | first live bot run (0.10.3)

Discord continue prompt run: `es_discord.py check` authenticates; Public Bot on, Message Content Intent off, 0 servers. Stopped for Mark to change both settings.
## [2026-11-02] library | Level Up! (Rogers, 3rd ed.) distilled into game-design (0.10.1)

Auto-pick: `lit pick` listed no beat-listed file; *Level Up!* 3rd ed. (Wiley, Dec 2024) was read 2026-10-22 for plugin-learnings and its proposals landed 2026-10-23 (books track 9: roblox-agent, unity-agent, madnesswright, musicwright; ludowright cites it), but game-design had no row and no level-design vocabulary. Distilled from that read (git grep showed the plugin rows already applied, so this run fed the beat only): canon row, a Level design vocab section (13 terms), five level question seeds (indie-ai-scout PR #12, merged), book note. `lit due`: every tier current. Judgment-call recheck: none open (only `have` rows keep the label).

Tool changes: everscout 0.10.1 (`lit lint` accepts numbered chapter labels such as `(Level 11)`; test). No readwright changes needed: no new reading this run (distilled from the earlier read). Installed everscout was updated to 0.10.0 at the start (main clone back on main).

## [2026-11-02] fix | lit ingest splits (Author) off file-name titles (0.10.2)

`lit_split_stem` in scripts/everscout.py: trailing parenthesized person names become book.md `authors:`, a year or publisher trailer is dropped, other parentheses stay. A colon-less run-together subtitle is not separable and stays. Found ingesting the Mizrahi prompt-engineering PDF; that book folder was left as is (another session owns it). Test: test_lit_split_stem_paren_author.

## [2026-11-02] discord | bot live on Mark's server (0.10.3)

Public Bot off needed Installation > Install Link = None first (kb updated). Bot added to Mark's server; guilds, channels, threads, read, search all work. `read` warned about the intent on a day holding only the bot's join message: `discord_text_missing` now checks user messages only (test added). Released as 0.10.3 (0.10.1 and 0.10.2 were taken by a parallel library session).

## [2026-11-02] discord | continue run: check server count (0.10.4)

Ran the continue prompt: token, check, invite and guilds all work (steps 1-3 done earlier). `check` said servers 0 while `guilds` listed Mark's server: Discord's `approximate_guild_count` is cached. `check` now counts `/users/@me/guilds`. Test: test_check_counts_listed_servers. Step 4 (admin message for a beat's server) waits on Mark.

## [2026-11-02] library | Unlocking the Secrets of Prompt Engineering (Mizrahi) distilled into token-saving; everscout 0.10.2, readwright 0.17.0

Auto-pick: nothing due, no beat-listed file unread; the only unread beat-fitting file. Beginner use-case book with dated models; one new point, spreadsheet LLM formulas re-billing on every open (p. 237-238): recompute-waste vocab, one question (indie-ai-scout PR #13). Verdict skip. Tool changes: everscout 0.10.2 (PR #92) parenthesized author off file-name titles; readwright 0.17.0 (PR #31, installed) printed-contents chapter split. Installed everscout still behind: the main clone holds another session's uncommitted Discord edits. Trigger evals (step 4) not run. T-20261102-15.

## [2026-11-02] library | The Blender Python API (Conlan) distilled into game-design; everscout 0.10.5

Auto-pick: nothing due; the read-elsewhere Blender API book named by the last handoff. Distilled from the 2026-10-22 plugin-learnings read plus greps: recent row (Judgment call: own copy; Springer DOI), mesh-errors vocab, two Levels and generation seeds, edition note (indie-ai-scout PR #14). polywright already held every idea, so no plugin changes. everscout 0.10.5: spaced file names lose a leading publisher. readwright: running-head chapter split and U+FFFD leader collapse handed to an agent in its own worktree.

## [2026-11-02] discord | no-admin routes; everscout 0.10.6

Mark asked how to read servers like r/StableDiffusion with no admin. Tested: invite lookup works without a token (discord.gg/stablediffusion is Stability's official server, 315k; Comfy Org 62k); widgets on but presence only; message text only through a bot or Follow on an announcement channel into Mark's server. Added `es_discord.py peek` and `row --followed`, kb/discord.md section, test. Waits on Mark: create feed channels and click Follow.

## [2026-11-02] library | Show Your Work! (Kleon) distilled into indie-game-marketing; everscout 0.10.7

Auto-pick: nothing due; Mark added indie-game-marketing canon leads to the book folder (Kleon's Show Your Work!, Bacon's The Art of Community; Vogl's Art of Community and a Video Game Marketing textbook are there too, per marketwright's HANDOFF). Took Kleon: canon lead, short, about sharing the build. Essays, no data. Changes: marketwright reach.md devlog step (what to post per stage, capture as you build, time box, stock and flow onto an owned page, opt-in mailing list; PR #3 merged, unreleased: marketwright's own session plans a minor release after its book list), beat vocab build-in-public and mailing-list, three question seeds, a study perspective (indie-ai-scout PR #15). everscout 0.10.7: lint accepts toc titles cited without their final period or number. readwright: `--drop-epigraphs` and a short-book tip handed to an agent. T-20261102-17.

readwright 0.19.0 (PR #33, installed): `read --drop-epigraphs` (40 pairs dropped on Show Your Work!) and a short-book tip in Distilling a book. Trigger evals (step 4) not run.

## [2026-11-02] discord | Follow feeds live

Mark made a fresh server (1567019559620186263) and followed Comfy Org #announcements and #events, Stability #announcements, SwarmUI #announcements. Bot reads all three; only follow notices so far. Rows added to ai-video sources.md. r/StableDiffusion has no announcement channels.

- 2026-11-02: Discord continue run 3: feed channels empty so far (expected); no code change; step 4 waits on Mark.

## [2026-11-02] library | Learn Unity for Android Game Development (Sinicki) distilled into game-design; everscout 0.10.8

Auto-pick: nothing due. `lit pick` led with Bacon (already distilled by the marketwright session) and marketwright plans the Video Game Marketing textbook, so took Sinicki: unread, fits game-design, not RL. Beginner Apress 2017 tutorial; ch. 10 is the lasting part. Changes (indie-ai-scout PR #17): camera-window, first-level-last, functional-fixedness vocab; question seeds on when the first level was built and on device-native input; dated-edition note. Verdict skim. Tool fix: everscout 0.10.8 (PR #99): `lit add --id -` had matched and overwritten another `-` row (The Gamer's Brain), caught in the diff before commit. readwright 0.20.0 (PR #34, installed): `read --headings`. Trigger evals (step 4) not run. T-20261102-18.

## [2026-11-02] library | Conversational Style (Tannen) distilled into tech-hiring; everscout 0.10.9

Auto-pick: nothing due; all indie-game-marketing books already distilled by marketwright. Took Tannen's 1984 study (OUP 2005 ed.): unread, non-RL, the mechanism behind Talking From 9 to 5 (pace, pause and overlap mismatch read as weaker competence). 8 principles, 5 changes applied to the tech-hiring beat (PR #101). Tool fixes: everscout 0.10.9 `lit ingest` unswaps swapped EPUB title/author (the folder had been named deborah-tannen); readwright 0.21.0 (PR #35) `info` notes the swap, plus a distilling tip. Both installed. Trigger evals (step 4) not run. T-20261102-19.

## [2026-11-02] library | LLM Engineer's Handbook (Iusztin, Labonne) distilled into token-saving

Named by the kickoff (book 1 of the 2026-11-02 distill order). Read the retrieval and serving chapters only (~12k of 123k words); the rest is an AWS/ZenML build. 13 principles; applied: beat vocab and two seeds (indie-ai-scout PR #20), tokenwright 0.2.14 (PR #42, installed), local-delegate PR #10 (merged; main clone not pulled, someone else's uncommitted log.md blocks the fast-forward). No everscout tool changes needed. readwright 0.22.0 (PR #36, installed): `--skip-code` drops dangling code lead-ins; Packt tip in Distilling a book. Judgment-call recheck (step 2) and trigger evals (step 4) not run. T-20261102-20.

## [2026-11-02] library | An Introduction to Audio Content Analysis (Lerch) distilled into downtempo

Book 2 of the 2026-11-02 distill order. Read only the onset, tempo, tuning and key sections (~6k of 137k words). 9 principles; applied: a downtempo question seed on sample tuning, musicwright 0.1.6 (PRs #51, #52; released, installed): `pulse --threshold adaptive`, `analyze` key_margin, runner_up_relation and KEY-AMBIGUOUS. Step 2 done by an agent: all 12 Judgment-call rows were distilled user copies, relabelled "User's copy" (everscout PR #103, indie-ai-scout PR #21); no rows dropped, no new evidence fetched. Open everscout item: the cut-title slug spends a word on a leading article (needs a match migration). Leftover undeletable folder Ai/musicwright-wt-lerch. Trigger evals (step 4) not run. T-20261102-21.


## 2026-11-02: book suggestions for the plugins
- Mark asked for new book suggestions instead of a distill run. From `lit pick` (302 unread files), not yet distilled: Doan *Indie Game Marketing Secrets* and *Video Game Marketing: A Student Textbook* (indie-game-marketing, marketwright); Sybex *Bounce Tumble and Splash* and Apress *Foundation Blender Compositing* (polywright-blender, cinewright); Kohler *Tax and Legal Playbook* (lexwright, finwright); Schilit *Financial Shenanigans* and Ittelson *Financial Statements* (marketwright/finwright IPO checks); *Innovation and Marketing in the Video Game Industry* (ludowright/marketing). Skip the generic prompt-engineering titles (Voss-style junk risk) and the 2009-2012 Blender beginner books (dated API). Beat leads still unowned: Dreskin, Marhulets, Hill-Whittall, Manning IR, LLM Engineer's Handbook, Hands-On LLMs. No tool changes.

## 2026-11-02: picked from the new books
- Mark added the token-saving and indie leads plus extras. Distill order: 1) LLM Engineer's Handbook (Iusztin, Labonne; token-saving lead) for tokenwright and local-delegate; 2) Lerch, *An Introduction to Audio Content Analysis* 2nd ed. for musicwright mw.py (measure, transcribe, seam); 3) Manning et al., *Introduction to Information Retrieval* (token-saving canon lead) for readwright grep ranking and everscout triage; 4) Futter, *The GameDev Business Handbook* (indie-game-marketing). Lower: Hands-On LLMs overlaps Huyen; Hill-Whittall is 2015; the Indie Game Magazine issues are history, not technique; generic LLM titles (Hill, Dhanith, Code Et Tu) skipped as junk risk.

- 2026-11-03 08:10: continue run stood down. Another session ingested Manning IR at 07:55 and has readwright PR #38 (BM25 rank, 0.24.0) open; this run re-ran `lit ingest` at 08:07 (rewrote book.md and toc.txt in the data folder, learnings.md untouched), then removed its own worktrees. No other changes.
- 2026-11-03 08:14: second continue run stood down too. The Manning IR session is still live (readwright PR #38 merged 08:09); running alongside it would collide on the same book, HANDOFF.md and TESTS.md. No changes.

## [2026-11-03] library | Introduction to Information Retrieval (Manning, Raghavan, Schutze) distilled into token-saving; everscout 0.10.10, readwright 0.24.0

Book 3 of the 2026-11-02 distill order (token-saving canon lead). Nothing due. A reader agent ran about a dozen greps (25k characters) in ch. 2, 7, 8, 9, 11, 13 and 19. 17 principles. Applied: Levers vocab bm25, near-duplicate, precision-at-k, query-expansion, and three question seeds (indie-ai-scout PR #22); readwright 0.24.0 (PR #38, released, installed): `rw.py rank FILE WORDS` ranks sections or paragraphs by BM25; EPUB equation pictures print `[equation 11.32: image]` or `[formula: image]`; `<sub>` prints `k_1`; grep and rank name swapped arguments. everscout 0.10.10 (PR #105, released, installed): `fetch` marks cross-posts `dup_of` by 4-word shingles and Jaccard 0.8 (31 of 716 cached indie-game-marketing items, all true cross-posts). Rejected: learned triage from keep and drop feedback (no per-item labels yet: a plan, not a book run), a tokenwright habit (habits.md at budget). The first beats worktree vanished between ingest and the beat edits (likely another session's cleanup); re-created and re-ingested. Trigger evals (step 4) not run. Next: book 4, Futter, *The GameDev Business Handbook*, into indie-game-marketing (check marketwright's HANDOFF first).

## 2026-11-03 Futter, The GameDev Business Handbook

- Auto-pick by the 2026-11-02 order (book 4; marketwright had not taken it). `lit due`: nothing due. Step 2 (Judgment-call rows) was done 2026-11-02.
- Read by two parallel reader agents; 17 principles, 16 changes all applied: indie-ai-scout PR #23, marketwright 0.4.1 (PR #18), note via `lit distill`.
- Tools: readwright 0.25.0 (PR #40) `toc --group` from printed contents and page joins that no longer empty pages; everscout 0.10.11 (PR #107) trailing ` - Author` split. Both released and installed. A first tag of readwright v0.25.0 went on main before the PR merged (merge was blocked by a log commit); deleted and re-cut after the merge.
- Trigger evals (step 4) not run.

## 2026-11-03 Hill-Whittall, The Indie Game Developer Handbook

- Auto-pick: first beat lead in `lit pick` (indie-ai-games canon `lead`), not in any beat's books or the plugin-learnings index. `lit due`: nothing due. Step 2 (Judgment-call rows) was done 2026-11-02.
- Read about 9k of 73k words myself (outsourcing, base projects, Early Access, two post-mortems); 2015 tool and portal lists skipped. 10 principles; applied four question seeds and an edition note (indie-ai-scout PR #24, merged), note via `lit distill`.
- Tools: everscout 0.10.12 (PR #109, released, installed): `lit lint` accepts the part of a toc title before a dash. No readwright changes needed: the EPUB outline and `--max-chars` served.
- Trigger evals (step 4) not run.

## 2026-11-03 Alammar and Grootendorst, Hands-On Large Language Models

- Auto-pick: first beat lead in `lit pick` (token-saving recent `lead`). `lit due`: nothing due. Judgment-call rows were rechecked 2026-11-02.
- Three copies in the book folder; read the final 2024 PDF, not the early-access EPUBs. About 14k of 92k words (tokenizers, KV cache, conversation memory, chunking, reranking, query rewriting, RAG evaluation). 17 principles; four vocab levers and four question seeds applied (indie-ai-scout PR #25, merged), edition note via `lit distill`.
- Tools: no everscout changes needed (`lit pick` hides every copy once the row is distilled). readwright 0.26.0 (PR #41, released, installed): `--skip-code` now drops Python listings in PDFs; skill tip on reading the final edition.
- `lit pick` now lists no beat-listed files: the next pick is by topic fit from the unlisted files, or a `lit` research pass to add leads the folder holds.
- Trigger evals (step 4) not run.

## [2026-11-03] library | Advanced Retrieval-Augmented Generation distilled into token-saving

Auto-pick (no beat-listed file left; an unlisted RAG book fits token-saving). 15 principles; 5 changes applied: vocab and questions (indie-ai-scout PR #26), tokenwright 0.2.15 (PR #43, released, installed), book note. readwright 0.27.0 (PR #42, released, installed): `grep --per-section N`, plus a skill tip on formula placeholders and cut sentences in EPUBs. No everscout changes needed. Record: T-20261103-5.

## [2026-11-03] beat | ai-video: ComfyUI tutorials sweep folded in; kb/method.md sweep section (0.11.0)

Two rss rows (Comfy-Org/docs tutorials commits, workflow_templates releases), a monthly `sweep` row for docs.comfy.org/_llms/en/tutorials.txt, keep-list line; everscout-scan follows the method for `sweep` rows. From the comfyui-gen tutorials track (2026-10-30 to 11-03). The tutorials feed showed commits on 11-02 and 11-03, after the last sweep: the next ai-video scan should sweep.

## [2026-11-03] library | Indie Video Game Development Work (Styhre) distilled into indie-game-marketing; readwright 0.28.0

Auto-pick: no beat-listed file left; Doan already read (marketwright), Financial Shenanigans is only an audiobook, so took the last unread indie-games book. Nothing due; Judgment-call rows rechecked 2026-11-02. Two reader agents, ~30k of 94k words (Preface, ch. 1, 4-6, 8). 14 principles, 5 changes applied (indie-ai-scout PR #27: studio-funding and money-norm vocab, launch-day and funding seeds; edition note). readwright 0.28.0 (PR #44, released, installed): the readers disagreed on the page offset because it drifts 10 to 7 across chapters; toc now labels each page `(p. N)` and `read --section pN` reads by printed page. A first v0.28.0 release was cut before the PR merged (merge conflict with the refresh PR #43); deleted and re-tagged on the merge commit. No everscout changes needed. Trigger evals (step 4) not run. T-20261103-6.
