# The radar report and the digest

Detail for [SKILL.md](../SKILL.md). `ES` = `python "<plugin root>/scripts/everscout.py"`; `DATA` = the folder `ES where --beat <slug>` prints. Method: `kb/method.md` (rubric, rings, faithfulness).

## Inputs

1. `ES tally --beat <slug>`, then `DATA/signals/tallies.json`: per facet and entity, `30d`, `prev30d`, `90d`, `all`, `decayed`, `spread90`, `signal`, `first`, `last`, `example`.
2. The previous report (`DATA/reports/INDEX.md`, newest radar): its period, its blips and rings, its open questions.
3. Notes posted in the period (`DATA/notes/<month>/INDEX.md`). Read in full the ten with the highest interest and every note on a `new` or `rising` entity.
4. `ES ledger --beat <slug> --days 90 --json`: entries with `replies` are practitioner answers.
5. `DATA/journal.md` and `DATA/feedback.md`: the user's own view and steer.
6. The beat's metrics: `ES stats collect --beat <slug>`, then `ES stats review --beat <slug>` (findings: promote, archive, keep, trends, pairs; see `kb/stats.md`), then `ES stats export --beat <slug> --charts` (charts in `DATA/reports/charts/` when chartwright is installed).
7. Optional web check when the user asks for "latest" and the last scan is older than a week: run the scan's due searches first (everscout-scan procedure A8), so the report still cites notes, not memory. A page read only for this report (a policy page, a release note) is logged with `ES source-log <url> --beat <slug> --title ... --supports ...` before it is cited.

## The radar report: `reports/<date>-radar.md`

Frontmatter: `title, kind: report, status: active, date, verified, beat, period: <previous end>..<today>, notes_read: N, summary, tags: [report, radar]`.

Sections:

- `## Direction`: three to six sentences a busy person can act on: the one or two shifts, what stopped moving, and what to try or read. Where the data is thin, "thin: N notes".
- `## Radar`: one table per quadrant (the beat's vocabulary facets; merge small facets). Columns: `entity | ring | change | 30d | prev 30d | spread | why (1 to 3 sentences, with note links)`. Rings Adopt, Trial, Assess, Hold per kb/method.md; change is `new`, `moved from <ring>`, or `no change`. Include every entity whose tally signal is new, rising or fading, every entity in the previous radar (re-examined; one not re-examined for two reports drops off with a line saying so), and steady entities with `decayed` in the facet's top five.
- `## Signals and trends`: the rubric scores (novelty, velocity, breadth, evidence, relevance, each 0 to 3 with a one-line reason) for the three to eight strongest candidates; label each "weak signal", "signal", or "trend" by kb/method.md's thresholds, and say which cluster and which two reports back a trend.
- `## Metrics`: one table `metric | question | last value (date) | trend | review`, headline metric first, candidates marked, archived ones named once with their reason; the review's pairs in one line each; links to the charts (`charts/<slug>-metrics-line.html`, `charts/<slug>-small-multiples.html`) or to `../stats/export.csv` when there are none; then the promotions to ask the user about. "No metrics yet" when the catalog is empty.
- `## Notable threads`: five to ten note links, one clause each (highest interest, an unusual method, a strong reception signal, a surprise).
- `## What makers said`: answers to the user's questions, paraphrased, grouped by question category, each with the note link; "none this period" when empty.
- `## Reception and policy`: community mood and rule changes, dated, each linked.
- `## Your journal`: one to three lines connecting the user's own entries to what the data shows (only when the journal has entries in the period).
- `## Open questions`: what the next scan or engagement should target; carry forward the unresolved ones from the previous report and mark them "(carried)".
- `## Sources`: sources scanned (`ES state --beat <slug>`), searches run, pages read, all dated; the sentence that interest is comments and top-of-week, not score.
- Closing line: `Related: [previous report](<file>) · [signals](../signals/signals.md) · [study](../study/00-overview.md)`.

Budget 120 to 250 lines. Tables carry the numbers; prose carries the judgment.

## The digest: `reports/<date>-digest.md`

For "what happened this week". Frontmatter as above with `tags: [report, digest]`. Five bullets (each one sentence and a note link), then `## Movers` (new and rising entities with counts), then `## Replies` (answers from makers), then `## Next` (one line). Under 40 lines.

## After

`ES lint --beat <slug>` (exit 0), `ES index --beat <slug>`, log line, output per SKILL.md. A gap the report exposed (an entity everyone names but no note explains) goes into Open questions; a gap in the skill itself goes into LEARNINGS.md.
