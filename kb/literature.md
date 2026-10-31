# Literature: the books of a beat

How a beat keeps up with its books, and how a book the user provides becomes knowledge in the beat and in the skills the beat feeds. The everscout-library skill follows this file. Formats are in [SCHEMA.md](SCHEMA.md); the CLI is `everscout.py lit`.

## The three tiers

`literature.md` in the beat folder holds one table per tier. Columns: `title | authors | year | id | why | evidence | status`.

| tier | holds | size | recheck |
|---|---|---|---|
| canon | the most important books of all time for the subject as the beat's scope defines it | 5 to 10 | yearly |
| recent | the most important books of the last five years | 4 to 8 | quarterly |
| latest | new books worth a look, found by `lit new` | up to 10 | monthly |

A young subject (AI video in 2026) has almost no canon of its own. Its canon is then the older craft the practice rests on (editing, cinematography, generative models), and the intro line of the tier says so.

Each tier's date is in the frontmatter (`canon_checked`, `recent_checked`, `latest_checked`). `lit due` lists the tiers past their recheck. `lit check` (also run by `beat-check`) fails a row without a URL as evidence or with a malformed id.

## Picking the canon and the recent books

Importance is a judgment. Make it from more than one kind of evidence, and never from memory alone:

1. **Teaching**: university syllabi and course reading lists (search `syllabus "<subject>"`, `site:edu reading list`).
2. **Awards and best-of lists**: the field's own prizes (FT and McKinsey Business Book of the Year for economics, for example), end-of-year lists in serious outlets.
3. **Practitioners**: books the beat's own communities recommend. `everscout.py recall --beat <slug> --q "book"` finds them in the notes; a community wiki or FAQ often has a reading list.
4. **Citation and endurance**: many editions (Open Library's `edition_count`), still in print, cited by later books on the list.

A book on two or more kinds of evidence goes in. A book on one kind goes in only with a reason in `why`. `evidence` is one URL that was fetched or seen in search results during the research, the strongest one. `id` is the Open Library work key (`OL123W`) from `search.json`, or `isbn:<13 digits>`, or `-`.

Rank inside each tier, most important first. Keep `why` to one plain sentence in your own words.

## Finding the latest books

The `## Searches` table lists Open Library `search.json` queries for the beat (`subject:"labor market"`, `q=generative video`, `author:<name>`). `lit new --beat <slug>` runs them sorted by newest, keeps books from last year on that the file does not list, and ranks those that more searches return. Read each candidate's Open Library page before adding it. Publisher catalogues, award longlists and the beat's own news sources (`fetch`) also surface new books; their URLs may be the evidence.

Expect noise. On 2026-10-30 most of `lit new`'s hits across eight beats were self-published titles, content-farm series (a dozen "Claude Code" books from one imprint in a month), IMF country reports under `subject:"macroeconomics"`, and off-topic matches. Keep a book only when the publisher, author or reviews show it is real work, and write "unvetted" in `why` when unsure. Store queries plain (`subject:"electronic music"`), without year ranges: `lit new` sets the window and undoes URL encoding.

A new book goes in the latest tier as `lead`. After a year or so, either move it to recent (it mattered) or drop it.

Open Library asks API users to identify themselves with a User-Agent and contact, to cache, and not to bulk-harvest (openlibrary.org/developers/api, read 2026-10-30). everscout sends its User-Agent with the user's contact, keeps one request a second, and caches search results for a day. Google Books' keyless API answered 429 on its shared daily quota on 2026-10-30, so it is not used.

## Status

`lead` (listed, not obtained), `have` (the user owns a copy), `reading` (`lit ingest` ran), `read`, `distilled` (`lit distill` ran), `skip` (not worth the time; say why in `why`). Where the user's copy lives is never written in a public beat; `book.md` in the data folder holds it.

## Distilling a provided book

When the user provides a book file (EPUB, PDF, DOCX, text), or names one they own:

1. `lit ingest <file> --beat <slug> [--id OL...W]`. It runs readwright (`info`, `toc`) when installed, writes `DATA/books/<book>/book.md`, `toc.txt` and a `learnings.md` to fill, and sets the list row to `reading`. Without readwright, outline the book with your own reader. readwright never removes DRM, and neither do you.
2. **Plan the read from the outline.** Read the introduction and the conclusion first, then the chapters that bear on the beat's research questions (`beat.md`). Use `rw.py grep` for the beat's vocabulary before reading whole chapters. A long book is read in sections, never dumped into the context.
3. **Write principles**, one numbered line each, in fresh words, each cited `(ch. 3)`, `(p. 41)` or `(sec. 2.4)`. A quote is at most 25 words and rare. Say where the book is wrong or dated.
4. **Compare with the beat.** For each principle run `recall` and note what the beat already has, lacks or contradicts.
5. **Propose changes**, one row each in the Changes table, aimed at a target:
   - `beat/vocab.md`: entities and aliases the book names (tools, methods, schools, people).
   - `beat/questions.md`: better questions to ask makers.
   - `beat/searches.md` and `beat/sources.md`: places the book points to (verify them as the beat skill does).
   - `beat/study.md`: chapters of the baseline study the book changes.
   - `beat/metrics.md`: a number the book says matters.
   - `note`: what goes into the book note only.
   - `feed:<unit>/<path>`: a skill or plugin this beat feeds (beat.md `feeds`), for example `feed:finwright/references/fees.md`.
   - `plugin:<name>/<path>`: any other plugin of the user's the book improves.
6. **Apply** the changes the user wants, through the owning skill's own rules (a skill change goes through its CHANGELOG, a beat source through verification). Mark each row `applied` or `rejected`. Changes to another repository are proposals until made there.
7. `lit lint <book>` must exit 0, then `lit distill <book>`. It writes a `book` note in `DATA/notes/` (so `recall` and everscout-ask find the book), marks the learnings and the list row `distilled`, and refuses while a change is still `proposed` unless `--allow-open` is passed.
8. Write a Verdict: worth it or not, for whom, what to skip. Log the session in `DATA/log.md`.

## Copyright

The user's copy is private. Never commit or paste book text into a repository, a report or a public beat. Learnings are paraphrase with chapter citations; ideas are free to reuse, wording is not. `lit lint` fails a quoted run over 25 words.

## Sources

- Open Library API usage guidelines and rate limits, https://openlibrary.org/developers/api (read 2026-10-30).
- Open Library search API, https://openlibrary.org/dev/docs/api/search (2026-10-30; `sort=new` and `fields` checked live).
- Evidence and probes: `ai-docs/research/2026-10-30-beat-literature.md`.
