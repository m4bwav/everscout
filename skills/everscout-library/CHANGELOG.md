# Changelog: everscout-library

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`.

### C-20261113-1 · 2026-11-13 · Craft of Research rules
- because: Booth, Colomb and Williams, The Craft of Research, 3rd ed. (2008), ch. 3-6, 8-12, 14; book rule, unverified on our tools
- files: kb/literature.md (step 1a)
- Step 1a checks the copy of a secondary work is the latest edition. Plugin 0.14.0.

### C-20261107-6 · 2026-11-07 · lit ingest prints the outline
- because: T-20261107-27 (Step 3.1 says read the outline it prints; ingest printed only paths, so the run opened toc.txt in a second call)
- files: scripts/everscout.py (`cmd_lit_ingest`); 2 test assertions plus 1 test. Plugin 0.12.20.

### C-20261107-5 · 2026-11-07 · lit ingest --tier needs --year
- because: T-20261107-26 (Typography Workbook row came in with no year; `lit check` warned after distill and the row was fixed with `lit add`)
- files: scripts/everscout.py (`cmd_lit_ingest`), SKILL.md Step 3.1; 1 test. Plugin 0.12.19.

### C-20261107-4 · 2026-11-07 · lit ingest refuses a recent row older than the window
- because: T-20261107-25 (EvoMUSART 2019 went into recent; beat-check warned only after the beats PR, and the row had to be moved by hand)
- files: scripts/everscout.py (`cmd_lit_ingest`); 1 test; also resynced the drifted references/kb/literature.md copy. Plugin 0.12.18.

### C-20261107-3 · 2026-11-07 · lit pick skips a lead another beat distilled
- because: T-20261107-22 (The Computer Music Tutorial listed as an ai-sfx lead read elsewhere after ai-music distilled it)
- files: scripts/everscout.py (`cmd_lit_pick`); 1 test. Plugin 0.12.15.

### C-20261107-2 · 2026-11-07 · lit pick stops copying the read index per test
- because: T-20261107-10 (MemoryError on the full listing)
- files: scripts/everscout.py (`cmd_lit_pick`); 1 test. Plugin 0.12.6.

### C-20261107-1 · 2026-11-07 · lit pick hides a read book's side files
- because: T-20261107-6 (Hewitt's appendix and CD log listed after the book was distilled)
- files: scripts/everscout.py (`cmd_lit_pick`); 1 test. Plugin 0.12.5.

### C-20261106-1 · 2026-11-06 · lit pick sees a much-discussed book's author
- because: T-20261106-6 (*Pixel Logic*, read and written up at length, listed as unread: its author's name passed the 8-mention rarity limit)
- files: scripts/everscout.py (`lit_short_title_hit`); 1 test. Plugin 0.12.2. The file name's last word now also counts when it sits beside at least half the title's mentions. Maybe-read went from 41 to 43; a first version on any word went to 52 and hid unread books through phrases like large language models.

### C-20261102-2 · 2026-11-02 · lit pick looks in subfolders
- because: T-20261102-3 (Mark's pick, Prompt Engineering for LLMs, sat in a folder of its own in the books folder; `lit pick` said no beat-listed file was unread)
- files: scripts/everscout.py (`lit_book_files`, two levels deep, relative paths); 1 test. Plugin 0.9.2.

### C-20261102-1 · 2026-11-02 · lit add links an already-ingested book
- because: T-20261102-2 (`lit ingest` found no row, `lit add` then left it `lead` and book.md's book_id `-`; fixed by hand)
- files: scripts/everscout.py (`lit_link_ingested`, ingest message); 1 test. Plugin 0.9.1; `VERSION` in everscout.py had lagged at 0.8.9 and now matches plugin.json.

### C-20261101-2 · 2026-11-01 · lit pick, empty-file refusal
- because: T-20261101-5 (manual greps to auto-pick a book; a scan without text got a book folder)
- files: SKILL.md Step 3 item 1; kb/literature.md procedure step 0 and 1; scripts/everscout.py (`lit pick`, ingest refusal); 2 tests. Plugin 0.8.0.

### C-20261101-1 · 2026-11-01 · lit fixes from four books
- because: T-20261101-2 (status notes rejected by lint), T-20261031-4 (note rows ignored by distill), T-20261101-3 (`lit` wrote to the main clone, not the worktree)
- files: SKILL.md Step 3 item 4; scripts/everscout.py (`lit_change_status`, `note` rows in distill, `EVERSCOUT_BEATS`); 2 tests. Plugin 0.7.1.

### C-20261030-1 · 2026-10-30 · Created
- because: user request (keep up with a beat's literature: canon, recent, latest; distill a provided book into the knowledge base and attached skills), R-20261030-1 to R-20261030-3
- files: SKILL.md, kb/literature.md, beats/_template/literature.md, scripts/everscout.py (`lit`), scripts/es_sources.py (Open Library). Plugin 0.7.0.
