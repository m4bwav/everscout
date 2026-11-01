---
name: everscout-library
description: "Keep up with the books of a subject the user has an everscout beat for: the most important books of all time (canon), the most important recent ones, and the latest published, each listed with evidence in the beat's literature.md; find new books through Open Library; and when the user provides a book file or names one they own, read it with readwright and distill it into the beat's files, its notes and the skills or plugins the beat feeds. Use whenever the user asks 'what are the key books on my beat', 'best books on X', 'what's new in books on Y', 'any new books on my economics beat', 'build the reading list for this beat', 'read this book into my scout', 'distill this book', 'what did we learn from that book', or 'which books would help my plugins'. Also for 'refresh everscout-library' and 'is everscout-library stale'. Setup is everscout-beat, scans everscout-scan, questions about the subject everscout-ask."
---

# everscout-library

Outcome: the beat's `literature.md` has a canon, a recent and a latest tier, every row backed by a URL seen during the research, and `ES lit check --beat <slug>` exits 0; or, for a provided book, `DATA/books/<book>/learnings.md` passes `ES lit lint`, the changes the user approved are applied, and `ES lit distill` wrote the `book` note. Evidence: the `ES lit` calls in the trace, the files, the exit codes, a log line in `DATA/log.md`.

Plugin root: two levels above this file. `ES` = `python "<plugin root>/scripts/everscout.py"`. `DATA` = the path `ES where --beat <slug>` prints. Procedure and the rules for picking books: [references/kb/literature.md](references/kb/literature.md). Formats: [references/kb/SCHEMA.md](references/kb/SCHEMA.md). Why: [RESEARCH.md](RESEARCH.md).

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task, then run `evergreen-refresh` in the same session. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: which beat, which job

`ES beats` lists the beats. Pick the one the user named or whose scope fits. Then the job:

- **List or refresh the literature** ("key books", "reading list", "anything new"): Step 2.
- **A provided book** (a file path, or "I have X"): Step 3.
- **Books for the user's plugins** (not a beat): research as in Step 2, but each row names the plugin file it would feed; write it where the user keeps reading lists, not in a beat.

## Step 2: the three tiers

1. `ES lit due --beat <slug>` says which tiers are due. A beat with no `literature.md` gets the template: `ES lit add` creates it.
2. For each due tier, research as [references/kb/literature.md](references/kb/literature.md) says: syllabi, awards, practitioner lists, the beat's own notes (`ES recall --q "book"`), endurance. Two kinds of evidence per book, or a reason. Look up the Open Library work key.
3. Write rows with `ES lit add --beat <slug> --tier canon|recent|latest --title --authors --year --id --why --evidence`. Rank by importance. Set the tier's `*_checked` date in the frontmatter to today.
4. Latest: `ES lit new --beat <slug>` runs the beat's Open Library searches. Read the candidates' pages, add the real ones as `lead`, and add a search to `## Searches` when the results show a better query.
5. `ES lit check --beat <slug>` must exit 0. Tell the user the top of each tier with one line each, and which ones the user already has (mark them `have` when the user says so).

## Step 3: distill a provided book

Follow the procedure section of [references/kb/literature.md](references/kb/literature.md):

1. `ES lit ingest <file> --beat <slug> [--id OL...W]`, then read the outline it prints.
2. Read the parts that bear on the beat's research questions through readwright (`rw.py read --section`, `rw.py grep`), never the whole text into the context.
3. Fill `learnings.md`: cited principles in fresh words, what the beat already has (`ES recall`), the Changes table with targets, the Verdict.
4. `ES lit lint <book> --beat <slug>` until it exits 0. Show the user the proposed changes grouped by target and ask which to apply. Apply them through each target's own rules; mark rows `applied` or `rejected` (a note after the word is fine: `applied (v1.2, PR #3)`). A `note` row's change text (an edition line, reading caveats) is written into the book note by `lit distill`. Working in a worktree of the beats repo: set `EVERSCOUT_BEATS=<worktree>/beats` so `lit` edits the worktree's literature.md, not the main clone's.
5. `ES lit distill <book> --beat <slug>`, then `ES tally --beat <slug>` and `ES index --beat <slug>`. Append `library | <book>: N principles, M changes applied` to `DATA/log.md`.

## Rules

- Never paste book text into a repository, report or public beat; quotes are 25 words at most (`lit lint` checks). The user's file path stays in the data folder.
- Never strip DRM or fetch a pirated copy. If the user does not have a book, it stays `lead`.
- Evidence URLs come from this session's research, never from memory.
- Open Library is called through `ES lit new` only (paced, cached, identified).
