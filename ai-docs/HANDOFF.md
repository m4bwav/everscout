# Handoff

Updated 2026-10-30 (0.7.0: beat literature, see the first section). Before that 2026-10-16 (Reddit discovery built, unreleased; see the first section). Before that 2026-10-15 (0.4.0: Reddit through Arctic Shift). Before that 2026-09-28 (first all-beats scan; 0.3.0: beat statistics built). Everscout 0.1.0 was built in one session from indie-ai-scout 0.3.1; 0.2.0 added the everscout-ask skill (interrogate a beat like a reporter) and the tech-hiring beat, the first built from scratch. Read [log.md](log.md) for what happened, `decisions/` for the architecture, and `research/` for the evidence.


## 0.7.0 (2026-10-30): beat literature

- `everscout.py lit` and the everscout-library skill: each beat's `literature.md` holds canon, recent and latest books with evidence and status; `lit new` finds new books on Open Library; `lit ingest|lint|distill` turns a provided book (read through readwright) into `DATA/books/<book>/learnings.md`, applied changes and a `book` note. Procedure: `kb/literature.md`.
- All five built-in beats and Mark's three private beats have literature.md (2026-10-30). The one-source "Judgment call" rows were rechecked the same day: 37 kept with a second kind of evidence, 15 dropped; only Mark's own books (status `have`) keep the label. Weak keeps are listed in the research note. Rechecks: canon yearly, recent quarterly, latest monthly (`lit due`).
- Spelunky distilled end to end on 2026-10-31 (TESTS.md T-20261031-1): 24 principles; ludowright 0.1.9 (PR #16), indie-ai-games vocab and questions (indie-ai-scout e0ed600), study chapter 12, book note in the data folder. Where Mark's book files live is in the book's `book.md` in the data folder, never here.
- Press Reset (Schreier) distilled 2026-10-31 (T-20261031-3): 24 principles, 12 changes; ludowright 0.1.10 (PR #17), indie-ai-scout e791632, study ch. 01 and 12. AI Engineering distilled too (below).
- Trigger evals passed 3/3 on 2026-10-31 (TESTS.md T-20261031-2). 
- AI Engineering (Chip Huyen) distilled 2026-10-31 (T-20261031-4): 25 principles, 18 changes all applied: token-saving beat committed to indie-ai-scout (74306d9), tokenwright 0.2.6 (PR #20), fetchwright 0.2.1 (PR #6), evergreen-protocol PR #36, local-delegate PR #9, book note. Open: the private evergreen fork needs `git pull upstream master` with a conflict in skills/evergreen-refresh/SKILL.md resolved.
- The Gamer's Brain (Hodent, 2nd ed. 2026) distilled into game-design 2026-10-31 (T-20261031-5): 20 changes all applied: beat files (indie-ai-scout e1155de, 52b3cf0), ludowright 0.1.11 (PR #18), game-juice 1.3.1 (PR #6), book note. No `have` book left undistilled; next is Mark's next pick.
- Play to Learn (Boller, Kapp 2017) distilled into game-design 2026-11-01 (T-20261101-1): 18 changes all applied: indie-ai-scout de88bdf, ludowright 0.1.12 (PR #19, v0.1.12), book note. Next is Mark's next pick (or an agent pick from his downloads folder).
- Game Engine Architecture (Gregory, 2nd ed. 2014) distilled into game-design 2026-11-01 (T-20261101-2): 17 changes all applied across the beat, ludowright 0.1.13, game-juice 1.3.2, unity-agent 1.2.5, threewright 0.6.8, roblox-agent 0.1.8 and polywright 0.5.2. Next is Mark's next pick.
- Generative Deep Learning (Foster, 2nd ed. 2023) ingested into ai-video 2026-11-01: 23 principles, 14 changes all applied 2026-11-01 (T-20261101-3): beat vocab and questions, comfyui-gen #121, cinewright #68, artwright 0.7.4, musicwright 0.1.4, ludowright 0.1.14. Next is Mark's next pick.
- AI for Games (Millington, 3rd ed.) distilled into game-design 2026-11-01 (auto-pick, T-20261101-4): 12 changes all applied: indie-ai-scout PR #1, ludowright 0.1.15, unity-agent 1.2.6, roblox-agent 0.1.9, book note. readwright 0.3.0 fixed the big-section reading friction. Next session auto-picks the next book (continue prompt rule).
- 0.7.1 released 2026-11-01 (PR #44, v0.7.1): the three open lit frictions fixed: a note after a change's status word passes lint; applied `note` rows go into the book note; `EVERSCOUT_BEATS=<worktree>/beats` makes `lit` edit the worktree. No open tool items. The repo has no CI; local tests (81) are the gate.
- Beginning Game AI with Unity (Cossu 2021) ingested into game-design 2026-11-01 (auto-pick): 12 principles, 5 changes all applied the same day (unity-agent 1.2.7 PR #24, ludowright 0.1.16 PR #23, note; T-20261101-5). Since 2026-11-01 Mark pre-approves book changes unless one is controversial. Open tool items: `lit ingest` should refuse a file with no text layer; a `lit pick` to list unread books in Mark's folder.
- 0.8.0 released 2026-11-01 (PR #45): `lit pick` and the no-text refusal; Mark's config has `books_folder` and `books_read_index`. Palacios, Unity 2018 AI Cookbook distilled into game-design the same day (T-20261101-6; unity-agent 1.2.8, ludowright 0.1.17, readwright 0.4.0, indie-ai-scout PR #2). Open tool item: `lit pick` matches by file name only; books read under another name still list (verify each pick). Next: `ES lit pick`, then the next book.

## Reddit discovery built (2026-10-16, night), unreleased

- Branch `feat/reddit-discovery` (PR to main): steps 1 to 6 of `plans/2026-10-16-reddit-discovery-after-arctic-shift.md`. Pickup of Reddit links during `fetch`, `discover list|add|mark`, `captures`, `new-note --capture`, `fetchwright.max_reads_per_scan` (exit 6), scan skill Step 2 and procedure G, kb rows. 74 tests. The plan's Status section lists how the build differs from its shape.
- Live check: a week of ai-video's non-Reddit sources linked no Reddit thread (`research/2026-10-16-reddit-pickup-coverage-live.md`). Pickup stays on (no requests); web search and captures carry discovery for that beat after the archive.
- Open: release as 0.6.0 (tag and GitHub Release need Mark's go-ahead); then the coverage line after about four weekly scans; YouTube descriptions once the feeds answer.

## After 0.5.0 (2026-10-16, later): YouTube outage line, first ai-video radar, discovery plan

- Unreleased on main (PR from `fix/youtube-outage-line`): `fetch` says in one line when every YouTube feed fails, because YouTube's feed server 404s for every channel at once, on and off, since December 2025; the ai-video ids are fine. Evidence and the GDELT findings: `research/2026-10-16-youtube-feeds-and-gdelt-refusals.md`. 66 tests.
- Mark's ai-video data folder: the first monthly radar, `reports/2026-10-16-radar.md` (96 notes, lint clean). His answers the same night: `wiki-text-to-video` promoted, `news-ai-video-share` archived as `source-gone` (PR #23).
- Stage 2 step 4 planned: `plans/2026-10-16-reddit-discovery-after-arctic-shift.md` (pickup from fetched items and captures first, agent web search next, at most 10 fetchwright reads a scan). Built the same night (section above).
- fetchwright 0.2.0 released 2026-10-16 and installed (fetchwright@mark-local); `fetchwright.cli` removed from Mark's config, and `find_fetchwright` picks the installed 0.2.0.

## 0.5.0 state (2026-10-16): Reddit threads through fetchwright, opt-in, released

- Released as v0.5.0 (PR #21 merged). Config `reddit.thread_reader` (`same` default, `fetchwright`), `--thread-reader` on `thread` and `new-note`, `fetchwright.cli|models|max_comments (100)|timeout_seconds`; subprocess adapter in `load_thread`; cache, 5 s pace, cool-down from Google's retry time. Decision: `decisions/2026-10-15-thread-reader-fetchwright.md`.
- Live (`research/2026-10-15-fetchwright-thread-reader-live.md`): 9 of 10 threads read, every comment real, about three quarters of the archive's comments. The free tier gives `gemini-3.8-flash` 20 requests a day; fetchwright now moves to the next model on a per-model quota 429 (fetchwright PR #2, merged, not released). Mark's config runs `gemini-3.5-flash-lite` first and points `fetchwright.cli` at the fetchwright clone until fetchwright 0.2.0 is released and installed.
- First real scan with it (ai-video, 2026-10-16): 7 of 8 threads read; a thread hours old was not yet in Google's index and was read through the feed.
- Open: fetchwright 0.2.0 release (needs Mark), then drop `fetchwright.cli` from Mark's config; flash-lite's daily limit is still unverified (about 20 reads this session, no 429).

## 0.4.0 state (2026-10-15): Reddit after the feeds

- Mark chose the Arctic Shift lane on 2026-10-15. Built: config `reddit.reader` (`rss` default for everyone; `arcticshift`; `auto` = feeds until 2026-11-13, then Arctic Shift; Mark's own `~/.everscout/config.json` is set to `auto`), `--reddit-reader` on fetch, thread, probe and search; settled-score window (`reddit.settle_hours` 36); points and comments on every Reddit item. Live run on ai-video worked (1,904 posts, 2.5 minutes; one note, `1wzxyaa`, in Mark's data folder).
- Not built yet (plan steps 3 and 4): cross-platform pickup of Reddit links found elsewhere, and capture requests (`captures-wanted`, a beat `captures/` inbox).
- Rejected: Reddit through Gemini's Google Search grounding (Google's terms forbid handing grounded results to another model; `research/2026-10-15-reddit-through-gemini.md`). Mark keeps the Gemini API as a backup to learn, outside everscout for now.
- Backup route for after March 2027 (`plans/2026-10-15-reddit-via-gemini-url-context.md`): Reddit thread URLs found without Gemini's search, read with Gemini's URL context tool. Stage 1 passed on 2026-10-15 on `gemini-3.5-flash-lite` (`research/2026-10-15-gemini-url-context-reddit-test.md`); `gemini-3.8-flash` was overloaded and untested. Stage 2: built the same night as the standalone public plugin [fetchwright](https://github.com/m4bwav/fetchwright) (0.1.0, unreleased); conduct rule 17 and a platforms.md row here. Open: discovery after Arctic Shift, and everscout calling fetchwright's CLI. Key: `GEMINI_API_KEY` at user level, works.
- Open: Reddit app registration before 2027-01-12 (Mark's call); Arctic Shift after March 2027 is unknown (maintainer issue #76). `/api/subreddits/rules` on the archive could verify the beats' `~` stances (standing work 3); untried.
- The main clone `Ai/everscout` holds another session's uncommitted vocab and scan-skill edits; work in a worktree off origin/main.

## What Mark wants (2026-09-26)

Name any subject and get an AI scout generated for it that keeps up with the subject and engages politely with its community. The three starter beats are examples; generating a beat for any subject (the everscout-beat skill) is the core. Public repository; indie-ai-scout later becomes a private beat, voice and data on top (plan in indie-ai-scout's own doc set: `plans/2026-09-26-indie-ai-scout-on-everscout.md`).

## Current state

- This repository, branch main, public at github.com/m4bwav/everscout (tag v0.1.0).
- CLI `scripts/everscout.py` plus `scripts/es_sources.py`: 26 offline tests pass. Every adapter and every thread reader was checked live on 2026-09-26 in a scratch home.
- Reddit fetches pack quiet subreddits into multireddit requests (rates seeded from "about N a day" notes, learned per scan, busy ones alone, fallback when a window fills). The first live run of the ai-video beat through it was still running at handoff (scratch home only).
- Four skills registered with evergreen; `evergreen.py lint` OK on all four. No eval run yet (TESTS.md: trigger cases need a fresh session after install).
- Built-in beats `ai-video` (42 sources), `global-economics` (52), `downtempo` (48) pass `beat-check`. Their Reddit stances are mostly `~` because subreddit rules pages could not be fetched.

## 0.2.0 state (2026-09-26 evening)

- Five skills; `everscout-ask` passed its first headless test 3/3 (TESTS.md T-20260926-1). CLI `recall`, `fetch --peek`, `answers/` folder, plural alias matching; 30 offline tests pass.
- Built-in `tech-hiring` beat (33 sources) with Mark's real data folder at `~/.everscout/data/tech-hiring`: never scanned; one saved answer (on-site interviews and AI cheating). Next for it: the first scan (everscout-scan), then more questions.

- Mark's config (`~/.everscout/config.json`) exists since 2026-09-26: private beats from indie-ai-scout's `beats/` (the `indie-ai-games` beat, migrated from indie-ai-scout with 101 notes), `reddit_user`, ledger and voice in the vault and the indie repository. tech-hiring data still uses the default `~/.everscout/data`.

## 0.3.0 state (2026-09-27)

- Beat statistics: `metrics.md` per beat, `DATA/stats/series.csv`, `ES stats list|add|collect|review|export`, procedure in `kb/stats.md`, decision in `decisions/2026-09-27-beat-statistics.md`. 45 offline tests.
- Mark's tech-hiring data folder has the first real series (Wikipedia Layoff pageviews, 8 weeks; GDELT v1 with the narrow query, 8 weeks; GDELT v2 not yet collected because GDELT answered 429 all session). Next collect: `ES stats collect --beat tech-hiring`, then `ES stats review --beat tech-hiring` should propose promoting wiki-layoff (ask Mark).
- indie-ai-games (private beat, in the indie-ai-scout repo) has no `metrics.md` yet: offer candidates from its tallies next time it is scanned.
- Thresholds stay as judgment calls (Mark agreed 2026-09-27); revisit them after about three months of data (around 2026-12-27).

## 0.3.1 state (2026-09-27)

- tech-hiring `wiki-layoff` is active (promoted on Mark's yes). GDELT still refused a single probe at 16:38 UTC after 10 quiet minutes, so a cool-down runs to about 17:39 UTC (`~/.everscout/local/cooldown.json`); the v2 GDELT values are still missing. Next: `ES stats collect --beat tech-hiring` after that time (it skips GDELT while cooling). Details: [solutions/2026-09-27-gdelt-rate-limit.md](solutions/2026-09-27-gdelt-rate-limit.md).
- indie-ai-games: the beat folder and voice live in the indie-ai-scout repo (`beats/indie-ai-games`, commit 4988ecf, 0.4.0 parked), the data in the vault (`projects/indie-ai-scout/ai-docs/scout`); everscout runs it through `beat_dirs` in `~/.everscout/config.json`. Its `metrics.md` therefore belongs in indie-ai-scout; not added this session (that repo was not to be modified). Candidates to offer: notes per week (tally:notes), Wikipedia pageviews of a generative-AI article, GDELT raw volume for "AI-generated" game coverage.

## Next single action

All six beats had their first scan on 2026-09-28 (see log.md). Next: fix the two CLI faults that scan found (a file lock in `es_sources.py` `_wait`/`_mark`, then parallel distillation is safe; percent-encode non-ASCII Reddit slugs in `reddit_thread_url`), commit the vocabulary additions in the five built-in beats, then write the first reports (indie-ai-games weekly is due) and put questions to the beats with everscout-ask.

## Standing work

1. Run `evergreen-test` for the four skills (fresh session, scratch EVERSCOUT_HOME).
2. Set up Mark's `~/.everscout/config.json` (contact, reddit_user, data_root in the vault) and `voice.md` (from indie-ai-scout's "Voice (observed)").
3. Verify the `~` stances in the built-in beats with a signed-in browser or the rules pages; record `✓ date`.
4. arXiv API: 406 after bursts on 2026-09-26; gap now 15 s. Re-probe `global-economics` arXiv and BIS rows.
5. Possible 0.2: posting through personal APIs stays out (decision); an MCP server over the notes; a span check for quotes.
6. indie-ai-scout migration, stages 1 to 4, when Mark asks.

## Pre-approved metrics (0.3.2)

tech-hiring `news-tech-layoffs` and indie-ai-games `news-ai-indie-games` are pre-approved (`approved` in metrics.md) and will promote automatically on the first `stats collect` or `stats review` after GDELT data gives them 3 points.

## personal-sites beat (2026-09-27)

- New built-in beat `beats/personal-sites` (34 sources, probe clean). Mark's data folder `~/.everscout/data/personal-sites` holds the first reading: `answers/2026-09-27-state-of-personal-sites.md` (peek only; no scan yet, nothing marked seen).
- Purpose: refresh Mark's professional site (markdavidrogers repos under Ai/) and seed a new personal-site design skill from the beat. Next: first scan, then agree the study outline and write chapters 03, 04 and 06.
