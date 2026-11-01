# Tests: everscout-library

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A test passes on evidence (the `everscout.py lit` calls in the trace, the files, exit codes), never on the transcript's claim. The CLI's `lit` commands have offline tests in `tests/test_everscout.py` (LiteratureTests).

## Runs

### T-20261031-1: first end-to-end distillation (manual, real book)

Spelunky (Derek Yu, 2016) into a private game-development beat. `lit ingest` (readwright outline, 12 sections), a reading agent read Parts I to IV, `learnings.md` filled (24 principles, 14 changes), `lit lint` exit 0, the user approved all groups, changes applied (a game-design plugin's kb, the beat's vocab and questions, one study chapter), `lit lint` 14 applied, `lit distill` wrote the `book` note and set the row `distilled`, `tally` and `index` ran. Pass. Notes: `(Part I)` citations were accepted by lint; book text copies the reading agent made in its scratch folder were deleted afterwards.

Trigger cases: `evals/library-trigger-1`, `library-trigger-2`, `library-decoy-1` (see T-20261031-2).

### T-20261031-2 · 2026-10-31 · claude plugin eval (default model, 1 run per case) · Windows 11 native · 3/3

- library-trigger-1 (must-read books for a beat): everscout-library fired; scan, ask, report did not. Baseline 0.75.
- library-trigger-2 (distil a game design epub into a beat and its skills): fired, others did not. Baseline 0.75.
- library-decoy-1 (fantasy novel for a holiday): no everscout skill fired.
- The two trigger runs hit max_turns 3 after the skill loaded; the graders only check the Skill call, so this is expected.

### T-20261031-3: second distillation (manual, real book, chapter-split reading)

Press Reset (Jason Schreier, 2021, 98k words) into the same private beat. `lit ingest` (30 sections), one agent read the intro and epilogue and split chapters 1 to 9 over three reading agents, `learnings.md` 24 principles and 12 changes, `lit lint` exit 0, the user approved all four groups, changes applied (game-design plugin 0.1.10, beat vocab and questions, study chapters 01 and 12), `lit distill`, `tally`, `index`. Pass. Notes: the principles for chapters 1 to 9 rest on the readers' summaries, and the learnings file says so; the reading agents' book text copies in the scratch folder were deleted.

### T-20261101-3: seventh distillation (manual, real book, agent pick, two readers, six repositories)

Generative Deep Learning (David Foster, 2nd ed. 2023) into ai-video, picked from the user's downloads folder as the only unread book a beat lists. `lit ingest`, two reader agents (diffusion and multimodal; music and world models), 23 principles, 14 changes, `lit lint` 0, the user approved all. Applied: ai-video vocab, questions and literature row (this PR), comfyui-gen PR #121, cinewright PR #68, artwright 0.7.4 (PR #28), musicwright 0.1.4 (PR #19, `render --check` key_fit with tests), ludowright 0.1.14 (PR #21), edition line in the note. `lit lint` 14 applied, `lit distill`, `tally`, `index`. Pass. Finding: `lit ingest` and `lit distill` write the list row to the beat dir in the user's config (the main clone), so a session working in a worktree must copy the row across by hand.

### T-20261101-2: sixth distillation (manual, real book, three part readers, six repositories)

Game Engine Architecture (Jason Gregory, 2nd ed. 2014) into game-design. Canon row added with two syllabi, `lit ingest`, three reader agents (Parts I-II, III, IV-V), 25 principles, 17 changes, `lit lint` 0, the user approved all 17. Applied: beat vocab, question, literature (indie-ai-scout e36a0d2, a2dd567), ludowright 0.1.13 (PR #20, R-58 to R-61), game-juice 1.3.2 (PR #7), unity-agent 1.2.5 (PR #22), threewright 0.6.8 (PR #17), roblox-agent 0.1.8 (PR #20), polywright 0.5.2 (PR #42), edition line in the note. `lit lint` 17 applied, `lit distill`, `tally`, `index`. Pass. Finding: apply agents wrote statuses like `applied (unity-agent 1.2.5, pr #22)`, which `lit lint` rejects; the status cell must be the bare word, with versions kept in the log.

### T-20261101-1: fifth distillation (manual, real book, agent pick, two repositories)

Play to Learn (Sharon Boller, Karl Kapp, 2017) into game-design. Ingested 2026-10-31 (ch. 4, 5, 9 read to the 25k-character cut); the user approved all 18 changes. Applied: beat vocab, questions, searches and literature row (indie-ai-scout de88bdf), ludowright 0.1.12 (PR #19, released v0.1.12), book_id OL20198942W in book.md, reading caveats in the note. `lit lint` 18 applied, `lit distill`, `tally`, `index`. Pass.

### T-20261031-5: fourth distillation (manual, real book, second edition, three repositories)

The Gamer's Brain (Celia Hodent, 2026 second edition) into game-design. Ingested and linted earlier the same day; the user approved all 20 changes. Applied: beat vocab, questions, searches and literature row (indie-ai-scout e1155de, its first commit of the beat), ludowright 0.1.11 (PR #18), game-juice 1.3.1 (PR #6), edition line in book.md. `lit lint` 20 applied, `lit distill`, edition line added to the note, `tally` and `index`. Pass.

### T-20261031-4: third distillation (manual, real book, technical, changes across five repositories)

AI Engineering (Chip Huyen, 2024) into a token-saving beat. `lit ingest`, sectioned reading, `learnings.md` 25 principles and 18 changes, `lit lint` exit 0, the user approved all 18. Applied: the beat's questions, vocab, searches, study and metrics (beat repository), the book note, and four plugins through their own CHANGELOG and RESEARCH files (two patch releases, two docs-only PRs), each on its own worktree and PR. `lit lint` 18 applied, `lit distill` wrote the note and set the row `distilled`, `tally` and `index` ran. Pass. Notes: the `note` row was applied by editing the note after `lit distill`, since distill writes the note from the principles and does not act on `note` rows; the beat had never been committed, so its first commit carried the whole folder.
