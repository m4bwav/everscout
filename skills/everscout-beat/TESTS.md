# Tests: everscout-beat

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research a failure triggered goes in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: the evergreen plugin's protocol/TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done. The CLI underneath has its own offline suite: `python -m unittest discover -s tests` from the repository root.

## Runs

### T-20260926-1 · 2026-09-26 · claude -p headless, plugin 0.1.0 · win32, scratch EVERSCOUT_HOME · 1/3
- trigger-mark · trigger · pass · prompt "set up a scout for ai video generation": first tool call was Skill everscout:everscout-beat
- route · action · shallow · a built-in beat matched, so the skill copied it and stopped there; no discovery or research ran
- finish · action · fail · probe of 42 sources started in the background, the reply said "I'll finish the setup when it reports", the session ended and killed it: no probe snapshot, no data folder, no log line (9 turns, $0.37)
- led to: C-20260926-2, C-20260926-3

### T-20260926-1 · 2026-09-26 · not yet run · skill · 0/0
- Suite written; no run recorded. Trigger cases need a fresh session started after the plugin is installed. Run the baseline without the skill, then with it (`evergreen-test`).
- led to: none
