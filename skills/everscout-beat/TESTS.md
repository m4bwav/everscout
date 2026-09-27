# Tests: everscout-beat

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research a failure triggered goes in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: the evergreen plugin's protocol/TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done. The CLI underneath has its own offline suite: `python -m unittest discover -s tests` from the repository root.

## Runs

### T-20260927-2 · 2026-09-27 · claude -p headless, plugin 0.1.1 · win32, scratch EVERSCOUT_HOME · 3/3
- trigger-mark · pass · first tool call Skill everscout:everscout-beat
- route · pass · copied the starter, then a discovery pass (Reddit, Bluesky, Lemmy, newsletters, arXiv): added two AI film newsletters, a Bluesky feed generator, arXiv RSS, Lemmy; switched three GitHub rows to commit feeds; dropped a dead HN query; added PixVerse, KlingAI and SeedVR2 to the vocabulary after testing aliases on real posts
- finish · pass · evidence on disk: `sources/probe-2026-09-27.json` (46 ok, 0 bad), data folder with INDEX, log, HANDOFF; beat-check 0 errors, 0 warnings; 42 turns, 6.3 minutes, $1.55
- found: `probe --save` overwrote the snapshot on partial probes (L-002, fixed C-20260927-1); GitHub repos without releases (L-003)
- led to: C-20260927-1, the built-in ai-video beat updated with the verified changes

### T-20260926-1 · 2026-09-26 · claude -p headless, plugin 0.1.0 · win32, scratch EVERSCOUT_HOME · 1/3
- trigger-mark · trigger · pass · prompt "set up a scout for ai video generation": first tool call was Skill everscout:everscout-beat
- route · action · shallow · a built-in beat matched, so the skill copied it and stopped there; no discovery or research ran
- finish · action · fail · probe of 42 sources started in the background, the reply said "I'll finish the setup when it reports", the session ended and killed it: no probe snapshot, no data folder, no log line (9 turns, $0.37)
- led to: C-20260926-2, C-20260926-3
