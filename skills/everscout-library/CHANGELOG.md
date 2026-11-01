# Changelog: everscout-library

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`.

### C-20261101-2 · 2026-11-01 · lit pick, empty-file refusal
- because: T-20261101-5 (manual greps to auto-pick a book; a scan without text got a book folder)
- files: SKILL.md Step 3 item 1; kb/literature.md procedure step 0 and 1; scripts/everscout.py (`lit pick`, ingest refusal); 2 tests. Plugin 0.8.0.

### C-20261101-1 · 2026-11-01 · lit fixes from four books
- because: T-20261101-2 (status notes rejected by lint), T-20261031-4 (note rows ignored by distill), T-20261101-3 (`lit` wrote to the main clone, not the worktree)
- files: SKILL.md Step 3 item 4; scripts/everscout.py (`lit_change_status`, `note` rows in distill, `EVERSCOUT_BEATS`); 2 tests. Plugin 0.7.1.

### C-20261030-1 · 2026-10-30 · Created
- because: user request (keep up with a beat's literature: canon, recent, latest; distill a provided book into the knowledge base and attached skills), R-20261030-1 to R-20261030-3
- files: SKILL.md, kb/literature.md, beats/_template/literature.md, scripts/everscout.py (`lit`), scripts/es_sources.py (Open Library). Plugin 0.7.0.
