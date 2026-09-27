# Handoff

Updated 2026-09-26 (late). Everscout 0.1.0 was built in one session from indie-ai-scout 0.3.1. Read [log.md](log.md) for what happened, `decisions/` for the architecture, and `research/` for the evidence.

## What Mark wants (2026-09-26)

Name any subject and get an AI scout generated for it that keeps up with the subject and engages politely with its community. The three starter beats are examples; generating a beat for any subject (the everscout-beat skill) is the core. Public repository; indie-ai-scout later becomes a private beat, voice and data on top (plan in indie-ai-scout's own doc set: `plans/2026-09-26-indie-ai-scout-on-everscout.md`).

## Current state

- This repository, branch main, public at github.com/m4bwav/everscout (tag v0.1.0).
- CLI `scripts/everscout.py` plus `scripts/es_sources.py`: 26 offline tests pass. Every adapter and every thread reader was checked live on 2026-09-26 in a scratch home.
- Reddit fetches pack quiet subreddits into multireddit requests (rates seeded from "about N a day" notes, learned per scan, busy ones alone, fallback when a window fills). The first live run of the ai-video beat through it was still running at handoff (scratch home only).
- Four skills registered with evergreen; `evergreen.py lint` OK on all four. No eval run yet (TESTS.md: trigger cases need a fresh session after install).
- Built-in beats `ai-video` (42 sources), `global-economics` (52), `downtempo` (48) pass `beat-check`. Their Reddit stances are mostly `~` because subreddit rules pages could not be fetched.

## Next single action

In a fresh session after installing the plugin: say "set up a scout for <a subject Mark cares about>" and watch everscout-beat build a beat from nothing. That run is the real test of the core idea; fix what it gets wrong as a C- entry in the beat skill.

## Standing work

1. Run `evergreen-test` for the four skills (fresh session, scratch EVERSCOUT_HOME).
2. Set up Mark's `~/.everscout/config.json` (contact, reddit_user, data_root in the vault) and `voice.md` (from indie-ai-scout's "Voice (observed)").
3. Verify the `~` stances in the built-in beats with a signed-in browser or the rules pages; record `✓ date`.
4. arXiv API: 406 after bursts on 2026-09-26; gap now 15 s. Re-probe `global-economics` arXiv and BIS rows.
5. Possible 0.2: posting through personal APIs stays out (decision); an MCP server over the notes; a span check for quotes.
6. indie-ai-scout migration, stages 1 to 4, when Mark asks.
