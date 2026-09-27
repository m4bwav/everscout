# everscout-ask procedure

Detail for [SKILL.md](../SKILL.md). `ES` = `python "<plugin root>/scripts/everscout.py"`; `DATA` = the data folder `ES where --beat <slug>` prints.

## How recall ranks

`ES recall --beat <slug> --q "..."` reads notes, `answers/`, `reports/`, `study/` and `journal.md`. Each query word (stop words dropped; whole words, a plural counts) scores 3 in a title, 2 in a summary or saved question, 1 in the body (at most 3 a word). Each vocabulary entity the question names adds 4 to any document tagged with it or mentioning one of its aliases. A note's score is scaled by its age on the beat's half-life, never below half, so an old note that fits still shows. It also prints the tally rows (30 days, the 30 before, all, signal) for the entities the question names, and the knowledge base's size and last fetch. `--json` gives the same for scripting.

Recall is keyword and alias matching, not embeddings: reword the question in the beat's vocabulary once or twice (from `vocab.md`) before deciding the knowledge base has nothing. If an alias people use is missing, add it (everscout-beat procedure C).

## Grading, with examples

- "Are companies moving interviews back on-site because of AI cheating?" on a beat with six notes from the last month tagged `onsite` and `interview-cheating`: **enough**; answer from them, check the newest items once.
- The same question with two notes from four months ago: **partial**; the notes are history, the present needs a fresh search.
- "What's the H-1B fee now?" with no notes: **none**; the answer comes from an official page, logged, and the answer file says the scout had not covered it.

## Going outside

- The beat's communities first, because they are the beat's point of view: `ES search --kind reddit --community cscareerquestions --q "onsite interview AI" --t month`. Reddit search runs at Reddit's pace (about one request a minute): two or three searches, not ten.
- `ES thread <url> --beat <slug>` reads a thread with comments; read the two or three with the most comments.
- Official data before commentary for any number: the beat's `searches.md` "Pages worth reading directly" and the `web` rows in `sources.md`.
- Web search last, with the month and year. Prefer primary pages; the beat's "what not to trust" list applies.
- `ES source-log <url> --beat <slug> --title "..." --supports "..."` for every page the answer cites; lint rejects external links that no note or log holds.

## The answer file

Path `DATA/answers/<YYYY-MM-DD>-<slug>.md`, slug from the question (40 characters at most). Frontmatter: `title` (the question, shortened, no colons), `kind: answer`, `status: active`, `date`, `verified`, `beat`, `question` (in full, no colons), `grade: enough|partial|none`, `confidence: high|medium|low`, `notes_used: N`, `fresh_sources: M`, `summary` (the answer in one line), `tags: [answer]`. Body sections: `## Answer`, `## What the beat has seen`, `## What is new`, `## Where sources disagree`, `## Confidence and gaps`, `## Sources` (dated links), then `Related:` with links to the notes used. Follow-ups append `## Follow-up: <question>` with the same parts in short.

## Interrogation sessions

A user may ask ten questions in a row. Keep the recall and the pages read in mind across them; do not re-search what was read three questions ago. Save each substantial question as its own file, and short follow-ups in the file of the question they follow. At the end of a session, if the questions showed a gap in the beat (a community nobody watches, an entity with no alias, a data source missing), fix the beat or note it in `DATA/HANDOFF.md`.
