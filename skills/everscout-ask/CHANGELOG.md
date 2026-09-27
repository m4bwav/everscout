# Changelog: everscout-ask

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`.

### C-20260927-1 · 2026-09-27 · Number questions read the metrics first
- because: user request (approved design), R-20260927-1, ai-docs/research/2026-09-27-beat-statistics.md section 5
- files: SKILL.md (step 2), kb/stats.md
- A question about a number or trend reads `stats list` and `series.csv` first and may propose a candidate metric. Description unchanged. Plugin 0.3.0.

### C-20260926-9 · 2026-09-26 · Description shortened (skill-tidy)
- because: skill-tidy lint ST005 (over 1,024 chars) and ST007/ST013
- files: SKILL.md (front matter only)
- 1415 to 962 chars; same trigger meanings (skill-tidy check OK), boundary sentence kept. Plugin 0.2.2; plugin eval trigger cases 12/12.

### C-20260926-1 · 2026-09-26 · Created as an evergreen unit
- because: user request ("I want the framework to be able to answer any questions using information in its knowledge base combined with whatever else it needs to get the best answer. Like a reporter, you can interrogate them about their beat"), R-20260926-1, R-20260926-2
- files: SKILL.md, references/ask.md, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json; CLI `recall` command and the `answers/` folder (everscout 0.2.0)
- Tier `medium`, interval 30 days.
