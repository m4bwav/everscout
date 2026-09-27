# Tests: everscout-engage

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research a failure triggered goes in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: the evergreen plugin's protocol/TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done. The CLI underneath has its own offline suite: `python -m unittest discover -s tests` from the repository root.

## Runs

### T-20260926-1 · 2026-09-26 · not yet run · skill · 0/0
- Suite written; no run recorded. Trigger cases need a fresh session started after the plugin is installed. Run the baseline without the skill, then with it (`evergreen-test`).
- led to: none
