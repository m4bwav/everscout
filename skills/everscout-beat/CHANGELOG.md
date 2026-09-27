# Changelog: everscout-beat

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`.

### C-20260927-1 · 2026-09-27 · Partial probes merge into the snapshot; GitHub and arXiv guidance; starter beat refreshed
- because: T-20260927-2, L-002, L-003
- files: scripts/everscout.py (probe --save), references/procedure.md (A4), kb/platforms.md (github row), beats/ai-video/sources.md and vocab.md
- The built-in ai-video beat takes the test run's verified refresh (46 sources, all probed ok on 2026-09-27).

### C-20260926-3 · 2026-09-26 · Starter beats are refreshed, not just copied
- because: T-20260926-1 (route shallow)
- files: SKILL.md (Step 1 route table)
- A subject a built-in beat covers is copied, then checked and extended with procedure A's discovery pass for sources the starter lacks.

### C-20260926-2 · 2026-09-26 · Never end the turn with the probe running; probe batches Reddit
- because: T-20260926-1 (finish fail)
- files: SKILL.md (Step 3), scripts/everscout.py (probe)
- The probe runs in the foreground or is waited for. `probe` now checks Reddit ten subreddits per multireddit request and only probes absent ones alone, so a 40-source beat takes minutes, not a quarter hour.

### C-20260926-1 · 2026-09-26 · Created as an evergreen unit
- because: user request (a topic-agnostic version of indie-ai-scout), R-20260926-1
- files: SKILL.md, references/, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json
- Initial version, generalised from indie-ai-scout 0.3.1's scout-scan (procedure D, a new subreddit) skill. Tier `fast`, interval 14 days.
