# Handoff

Updated 2026-09-27 (0.3.0: beat statistics built; see the section below). Everscout 0.1.0 was built in one session from indie-ai-scout 0.3.1; 0.2.0 added the everscout-ask skill (interrogate a beat like a reporter) and the tech-hiring beat, the first built from scratch. Read [log.md](log.md) for what happened, `decisions/` for the architecture, and `research/` for the evidence.

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

Run the first scan of the tech-hiring beat ("scan the tech-hiring beat"), then interrogate it with a few questions to see recall grade `enough` from real notes. The from-scratch beat build and the ask skill are both proven (2026-09-26).

## Standing work

1. Run `evergreen-test` for the four skills (fresh session, scratch EVERSCOUT_HOME).
2. Set up Mark's `~/.everscout/config.json` (contact, reddit_user, data_root in the vault) and `voice.md` (from indie-ai-scout's "Voice (observed)").
3. Verify the `~` stances in the built-in beats with a signed-in browser or the rules pages; record `✓ date`.
4. arXiv API: 406 after bursts on 2026-09-26; gap now 15 s. Re-probe `global-economics` arXiv and BIS rows.
5. Possible 0.2: posting through personal APIs stays out (decision); an MCP server over the notes; a span check for quotes.
6. indie-ai-scout migration, stages 1 to 4, when Mark asks.

## Pre-approved metrics (0.3.2)

tech-hiring `news-tech-layoffs` and indie-ai-games `news-ai-indie-games` are pre-approved (`approved` in metrics.md) and will promote automatically on the first `stats collect` or `stats review` after GDELT data gives them 3 points.
