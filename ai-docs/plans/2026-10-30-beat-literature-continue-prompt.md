# Continue: beat literature (everscout-library)

Repeating start prompt. State lives in `ai-docs/HANDOFF.md`, never here.

## Load state

1. Read `AGENTS.md`, `ai-docs/HANDOFF.md` (section 0.7.0), the newest entries of `ai-docs/log.md`, `ai-docs/research/2026-10-30-beat-literature.md`.
2. Read `skills/everscout-library/SKILL.md` and `kb/literature.md`; follow them.
3. Mark's private beats are in the indie-ai-scout repo's `beats/`; `python scripts/everscout.py where` prints every path. His book files are in the folder named in the vault user profile; never copy book text into a repo.

## Waits on Mark

- Nothing to pick: if the kickoff names no book, choose one yourself (Mark, 2026-11-01: "auto pick one if one wasn't already selected") and say which and why in the log. Order: a `have` book not yet distilled, then `python scripts/everscout.py lit pick` (unread files in his book folder, beat-listed first; verify against the notes, it matches by file name) (the `file:` lines in earlier books' `book.md` show it): skip any book already in a beat's `DATA/books/` or in `D:/m4bwa/Claude/Projects/Ai/books/plugin-learnings/INDEX.md`, prefer one a beat's literature.md lists as `lead`, and ingest into that beat.
- Nothing to approve: Mark pre-approves each book's proposed changes (2026-11-01: "unless a change is controversial in some way, you can assume that I can authorize it"). Stop only for a controversial row (reverses existing guidance, public API, release workflow, registry publish). Otherwise, apply them with one agent per target repo in parallel (own worktree, PR, merge when checks pass, tag when bumped), and do the beat files yourself.

## Order of work

1. `python scripts/everscout.py lit due`; research any due tier.
2. Recheck the rows whose `why` starts "Judgment call": find a second kind of evidence (syllabus, award, practitioner list) or drop the row.
3. Distill one book end to end (`lit ingest`, read, `lit lint`, apply approved changes, `lit distill`); record the run in `skills/everscout-library/TESTS.md`.
4. Run the everscout-library trigger evals in a fresh session after install.
5. Improve the tools after every book. Review the run for friction, slips and workarounds: lint refusals, manual steps, agent mistakes, reading limits like the 25k-character cut, big outputs. Fix them where they live:
   - everscout (`scripts/everscout.py` `lit`, `skills/everscout-library/SKILL.md`, `kb/literature.md`, tests), in a worktree PR with a test for each fix.
   - readwright (`D:/m4bwa/Claude/Projects/Ai/readwright`, `rw.py` and its skill) for anything about reading the file, same way. Every book run also adds to readwright (Mark, 2026-11-01): put any book-distillation tip the run taught into its skill's distilling section, and build the reader feature the run lacked (a new view, filter or format fix), with a test. Say "no readwright changes needed" in the log only when the run truly taught nothing. Fix every readwright bug the run or a reader agent reports in the same session, before the hand-over, even when it costs more tokens (Mark, 2026-11-01: "I don't want to leave bugs unaddressed if possible"). Start with any readwright item HANDOFF.md lists as open. Leave one open only when it cannot be fixed (say why in HANDOFF.md).
   - Record each fix in the repo's CHANGELOG or LEARNINGS, merge once checks pass, and tag a release when the version is bumped. Say "no tool changes needed" in the log when there were none.
   - After every release, update the installed plugin (Mark, 2026-11-01: "always update it in plugin manager"): `git pull --ff-only` the plugin's main clone (local marketplaces read it), then `claude plugin marketplace update <marketplace>` and `claude plugin update <plugin>@<marketplace>`; check the version it reports.
   - Open items: see HANDOFF.md. In a worktree of the beats repo, set `EVERSCOUT_BEATS=<worktree>/beats` before `lit ingest` or `lit distill` (0.7.1).

## Stop points and hand-over

- Stop before a controversial change and before any registry publish; apply the rest without asking.
- Work in a worktree off origin's default branch (shared clones; everscout is `main`, the beats repo indie-ai-scout is `master`); create the beats worktree before setting `EVERSCOUT_BEATS`. Tests: `python -m unittest discover -s tests`. Merge your own PR once tests pass; tag and release when the version is bumped.
- At the end, update `ai-docs/HANDOFF.md` and `ai-docs/log.md`, and print the same start command: `Execute ai-docs/plans/2026-10-30-beat-literature-continue-prompt.md` (start in `D:\m4bwa\Claude\Projects\Ai\everscout`).
