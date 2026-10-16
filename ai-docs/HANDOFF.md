# Handoff

Updated 2026-10-15 (0.4.0: Reddit through Arctic Shift; see the first section). Before that 2026-09-28 (first all-beats scan; 0.3.0: beat statistics built). Everscout 0.1.0 was built in one session from indie-ai-scout 0.3.1; 0.2.0 added the everscout-ask skill (interrogate a beat like a reporter) and the tech-hiring beat, the first built from scratch. Read [log.md](log.md) for what happened, `decisions/` for the architecture, and `research/` for the evidence.

## 0.4.0 state (2026-10-15): Reddit after the feeds

- Mark chose the Arctic Shift lane on 2026-10-15. Built: config `reddit.reader` (`rss` default for everyone; `arcticshift`; `auto` = feeds until 2026-11-13, then Arctic Shift; Mark's own `~/.everscout/config.json` is set to `auto`), `--reddit-reader` on fetch, thread, probe and search; settled-score window (`reddit.settle_hours` 36); points and comments on every Reddit item. Live run on ai-video worked (1,904 posts, 2.5 minutes; one note, `1wzxyaa`, in Mark's data folder).
- Not built yet (plan steps 3 and 4): cross-platform pickup of Reddit links found elsewhere, and capture requests (`captures-wanted`, a beat `captures/` inbox).
- Rejected: Reddit through Gemini's Google Search grounding (Google's terms forbid handing grounded results to another model; `research/2026-10-15-reddit-through-gemini.md`). Mark keeps the Gemini API as a backup to learn, outside everscout for now.
- Backup route for after March 2027 (`plans/2026-10-15-reddit-via-gemini-url-context.md`): Reddit thread URLs found without Gemini's search, read with Gemini's URL context tool. Stage 1 passed on 2026-10-15 on `gemini-3.5-flash-lite` (`research/2026-10-15-gemini-url-context-reddit-test.md`); `gemini-3.8-flash` was overloaded and untested. Stage 2 (standalone public plugin, everscout reader, or both) waits for Mark's choice; no code yet. Key: `GEMINI_API_KEY` at user level, works.
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
