# Tests: everscout-ask

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research a failure triggered goes in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: the evergreen plugin's protocol/TESTING.md.

A test passes on evidence (the `everscout.py recall` call in the trace, the answer file, the lint exit code, the log line), never on the transcript's claim that something was done. The CLI's `recall` command has offline tests in `tests/test_everscout.py`.

## Runs

### T-20260926-1 · 2026-09-26 · claude -p headless, plugin 0.2.0 · win32, scratch EVERSCOUT_HOME · 3/3
- trigger-1 · trigger · pass · prompt "Ask my tech-hiring scout: are companies moving interviews back on-site because of AI cheating?": first tool call Skill everscout:everscout-ask
- action-1 · action · pass · `everscout.py recall --beat tech-hiring` in the trace (the question plus rewordings); graded none (the beat had never been scanned); searched r/cscareerquestions, read two threads, then the web; 17 pages logged with `source-log`
- outcome-1 · outcome · pass · `answers/2026-09-26-onsite-interviews-ai-cheating.md` with all six sections and grade, confidence, notes_used, fresh_sources; `lint` 0 errors 0 warnings; log line `ask | ...: none, 0 notes, 7 fresh sources, confidence medium`; 19 turns, 3.2 minutes, $0.98
- found: the answer split news coverage ("return to in-person") from what candidates reported on Reddit (remote cheat checks, no on-site calls) and flagged vendor data as vendor data; the grade "none" was stated plainly
- led to: the answer copied into the real tech-hiring data folder as its first entry; vocab matching now accepts plurals (a recall of "in-person interviews" named no entity)

