# Tests: everscout-library

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A test passes on evidence (the `everscout.py lit` calls in the trace, the files, exit codes), never on the transcript's claim. The CLI's `lit` commands have offline tests in `tests/test_everscout.py` (LiteratureTests).

## Runs

### T-20261031-1: first end-to-end distillation (manual, real book)

Spelunky (Derek Yu, 2016) into a private game-development beat. `lit ingest` (readwright outline, 12 sections), a reading agent read Parts I to IV, `learnings.md` filled (24 principles, 14 changes), `lit lint` exit 0, the user approved all groups, changes applied (a game-design plugin's kb, the beat's vocab and questions, one study chapter), `lit lint` 14 applied, `lit distill` wrote the `book` note and set the row `distilled`, `tally` and `index` ran. Pass. Notes: `(Part I)` citations were accepted by lint; book text copies the reading agent made in its scratch folder were deleted afterwards.

Trigger cases: not run yet (need a fresh session after install).
