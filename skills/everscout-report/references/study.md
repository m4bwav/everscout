# The baseline study: a history and guide for a beat

Detail for [SKILL.md](../SKILL.md), study mode. The study is what every later report is read against: what happened, who does what with what, how communities feel about it, and how to do the work, each claim tied to a source and, where one exists, to a community thread. It is written once, STORM style (perspectives, outline, cited chapters), and then refreshed by editing chapters in place, never by regenerating them.

`ES` = `python "<plugin root>/scripts/everscout.py"`; `DATA` = the folder `ES where --beat <slug>` prints. Output: `DATA/study/`.

## 1. Outline first (the user approves it)

Read the beat's `study.md` (the chapter table and the perspectives). For each perspective, write three to five questions that perspective would ask (a newcomer: "where do I start and what does it cost?"; a veteran maker: "what changed in the last year and what still breaks?"; a critic: "what is lost, who objects and why?"; an institution: "what are the rules and the numbers?"). Merge them into the chapter outline: five to twelve chapters, each with its questions. Show the outline to the user and wait. Their edits are the brief. Record the approved outline in `DATA/study/outline.md`.

## 2. Research per chapter (then write it, then move on)

1. Web search, three to eight queries with years: the subject plus the chapter's era or topic; `site:reddit.com/r/<community> "<topic>" <year>` for the beat's main communities; official pages, release notes, papers, statistics; long-form practitioner accounts (postmortems, interviews, talks). Read the two or three best primary pages per query, and log each page you read and will cite: `ES source-log <url> --beat <slug> --title "<title>" --supports "<the claim>"`. Lint accepts only URLs held by a note, a snapshot or this log, so a URL recalled from memory is caught.
2. Community search, paced: `ES search --kind reddit --q "<terms>" --community <sub> --sort top --t all`, `ES search --kind hn --q "<terms>" --t all --sort top`, `ES search --kind arxiv --q "<query>"` for research-heavy beats. Plan 10 to 25 calls per chapter; Reddit calls cost about a minute each, so batch them in one background run and read the cache afterwards (the same command returns the cached copy for an hour).
3. Cross-reference: a claim from the web that a thread confirms or contests gets both links; a claim with no thread says "(no thread found)". A thread worth keeping becomes a note (`ES thread`, `ES new-note`), and the chapter links the note.
4. Write the chapter to disk before starting the next: frontmatter `title, kind: study, status: active, date, verified, beat, tags: [study, <topic>], summary`; 80 to 200 lines; a `## Sources` section with dated links; a `Related:` line to neighbouring chapters. Quote the sentence that carries a key claim before paraphrasing it; keep hedges; "unverified" where it is.
5. Update `DATA/HANDOFF.md`: chapters done, the next chapter, any open searches.

## 3. Finish

Write `00-overview.md` last, from the chapters: what the study is, a one-page summary, an eras or topics table, a reading order, links to every chapter. Then the sources chapter (every source, dated, grouped by chapter). `ES lint --beat <slug>` (exit 0), `ES index --beat <slug>`, `ES tally --beat <slug>` (the ingested threads count), a log line.

## Refresh (study-refresh)

Read the chapter that covers the present and the notes since the study's `verified` date. Edit the affected chapters in place with dated additions ("Added 2026-11-02: ..."), bump `verified` in each touched chapter, add sources. Never rewrite a chapter wholesale: rewrites lose detail that took research to find.

## Parallel writing

A study is a good job for subagents: one chapter each, given the approved outline, the beat files, kb/method.md, kb/SCHEMA.md and this procedure. Each writes its chapter to disk and returns its sources. Then one checker pass per chapter: every external link resolves to a page that says what the chapter claims (spot-check five), `ES lint` passes, the chapter answers its outline questions. The overview is written last, by the main session.
