# Changelog: everscout-scan

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`.

### C-20260927-2 · 2026-09-27 · GDELT cool-down
- because: GDELT kept refusing (429) for more than 10 minutes after a burst; ai-docs/solutions/2026-09-27-gdelt-rate-limit.md
- files: kb/stats.md, kb/platforms.md
- `stats collect` skips GDELT metrics during a cool-down after a refusal and reports `cooling`. Description unchanged. Plugin 0.3.1.

### C-20260927-1 · 2026-09-27 · Collect metrics after the tally
- because: user request (approved design), R-20260927-1, ai-docs/research/2026-09-27-beat-statistics.md section 5
- files: SKILL.md (step 3, output), kb/stats.md
- `ES stats collect` runs after `tally`; failures are recorded as gaps, not retried; the summary names values collected or failed. Description unchanged. Plugin 0.3.0.

### C-20260926-9 · 2026-09-26 · Description shortened (skill-tidy)
- because: skill-tidy lint ST005 (over 1,024 chars)
- files: SKILL.md (front matter only)
- 1096 to 949 chars; same trigger meanings (skill-tidy check OK), boundary sentence kept. Plugin 0.2.2; plugin eval trigger cases 12/12.

### C-20260926-1 · 2026-09-26 · Created as an evergreen unit
- because: user request (a topic-agnostic version of indie-ai-scout), R-20260926-1
- files: SKILL.md, references/, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json
- Initial version, generalised from indie-ai-scout 0.3.1's scout-scan skill. Tier `fast`, interval 14 days.
