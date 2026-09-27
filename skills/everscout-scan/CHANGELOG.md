# Changelog: everscout-scan

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`.

### C-20260926-9 · 2026-09-26 · Description shortened (skill-tidy)
- because: skill-tidy lint ST005 (over 1,024 chars)
- files: SKILL.md (front matter only)
- 1096 to 949 chars; same trigger meanings (skill-tidy check OK), boundary sentence kept. Plugin 0.2.2; plugin eval trigger cases 12/12.

### C-20260926-1 · 2026-09-26 · Created as an evergreen unit
- because: user request (a topic-agnostic version of indie-ai-scout), R-20260926-1
- files: SKILL.md, references/, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json
- Initial version, generalised from indie-ai-scout 0.3.1's scout-scan skill. Tier `fast`, interval 14 days.
