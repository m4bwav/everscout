# Continue: beat literature (everscout-library)

Repeating start prompt. State lives in `ai-docs/HANDOFF.md`, never here.

## Load state

1. Read `AGENTS.md`, `ai-docs/HANDOFF.md` (section 0.7.0), the newest entries of `ai-docs/log.md`, `ai-docs/research/2026-10-30-beat-literature.md`.
2. Read `skills/everscout-library/SKILL.md` and `kb/literature.md`; follow them.
3. Mark's private beats are in the indie-ai-scout repo's `beats/`; `python scripts/everscout.py where` prints every path. His book files are in the folder named in the vault user profile; never copy book text into a repo.

## Waits on Mark

- Nothing to pick: if the kickoff names no book, choose one yourself (Mark, 2026-11-01: "auto pick one if one wasn't already selected") and say which and why in the log. Order: a `have` book not yet distilled, then a pick from his book folder (the `file:` lines in earlier books' `book.md` show it): skip any book already in a beat's `DATA/books/` or in `D:/m4bwa/Claude/Projects/Ai/books/plugin-learnings/INDEX.md`, prefer one a beat's literature.md lists as `lead`, and ingest into that beat.
- Approval of the proposed changes from each book's learnings.md before they are applied to a skill in another repo. Once approved, apply them with one agent per target repo in parallel (own worktree, PR, merge when checks pass, tag when bumped), and do the beat files yourself.

## Order of work

1. `python scripts/everscout.py lit due`; research any due tier.
2. Recheck the rows whose `why` starts "Judgment call": find a second kind of evidence (syllabus, award, practitioner list) or drop the row.
3. Distill one book end to end (`lit ingest`, read, `lit lint`, apply approved changes, `lit distill`); record the run in `skills/everscout-library/TESTS.md`.
4. Run the everscout-library trigger evals in a fresh session after install.
5. Improve the tools after every book. Review the run for friction, slips and workarounds: lint refusals, manual steps, agent mistakes, reading limits like the 25k-character cut, big outputs. Fix them where they live:
   - everscout (`scripts/everscout.py` `lit`, `skills/everscout-library/SKILL.md`, `kb/literature.md`, tests), in a worktree PR with a test for each fix.
   - readwright (`D:/m4bwa/Claude/Projects/Ai/readwright`, `rw.py` and its skill) for anything about reading the file, same way.
   - Record each fix in the repo's CHANGELOG or LEARNINGS, merge once checks pass, and tag a release when the version is bumped. Say "no tool changes needed" in the log when there were none.
   - Open items: see HANDOFF.md. In a worktree of the beats repo, set `EVERSCOUT_BEATS=<worktree>/beats` before `lit ingest` or `lit distill` (0.7.1).

## Stop points and hand-over

- Stop before applying any change to another plugin's repository without Mark's yes, and before any registry publish.
- Work in a worktree off origin/main (shared clone). Tests: `python -m unittest discover -s tests`. Merge your own PR once tests pass; tag and release when the version is bumped.
- At the end, update `ai-docs/HANDOFF.md` and `ai-docs/log.md`, and print the same start command: `Execute ai-docs/plans/2026-10-30-beat-literature-continue-prompt.md` (start in `D:\m4bwa\Claude\Projects\Ai\everscout`).
