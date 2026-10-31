# Continue: beat literature (everscout-library)

Repeating start prompt. State lives in `ai-docs/HANDOFF.md`, never here.

## Load state

1. Read `AGENTS.md`, `ai-docs/HANDOFF.md` (section 0.7.0), the newest entries of `ai-docs/log.md`, `ai-docs/research/2026-10-30-beat-literature.md`.
2. Read `skills/everscout-library/SKILL.md` and `kb/literature.md`; follow them.
3. Mark's private beats are in the indie-ai-scout repo's `beats/`; `python scripts/everscout.py where` prints every path. His book files are in the folder named in the vault user profile; never copy book text into a repo.

## Waits on Mark

- Which provided book to distill first (a book with status `have`, or one he names).
- Approval of the proposed changes from each book's learnings.md before they are applied to a skill in another repo.

## Order of work

1. `python scripts/everscout.py lit due`; research any due tier.
2. Recheck the rows whose `why` starts "Judgment call": find a second kind of evidence (syllabus, award, practitioner list) or drop the row.
3. Distill one book end to end (`lit ingest`, read, `lit lint`, apply approved changes, `lit distill`); record the run in `skills/everscout-library/TESTS.md`.
4. Run the everscout-library trigger evals in a fresh session after install.

## Stop points and hand-over

- Stop before applying any change to another plugin's repository without Mark's yes, and before any registry publish.
- Work in a worktree off origin/main (shared clone). Tests: `python -m unittest discover -s tests`. Merge your own PR once tests pass; tag and release when the version is bumped.
- At the end, update `ai-docs/HANDOFF.md` and `ai-docs/log.md`, and print the same start command: `Execute ai-docs/plans/2026-10-30-beat-literature-continue-prompt.md` (start in `D:\m4bwa\Claude\Projects\Ai\everscout`).
