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
