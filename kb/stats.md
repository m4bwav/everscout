# Beat statistics: how the skills use metrics

Each beat can keep a few numbers over time: a catalog in the beat folder (`metrics.md`) and one long-form, append-only CSV of values in the data folder (`DATA/stats/series.csv`). File formats are in [SCHEMA.md](SCHEMA.md); the research and the reasons behind every rule are in `ai-docs/research/2026-09-27-beat-statistics.md` in the repository. `ES` is `python "<plugin root>/scripts/everscout.py"`.

Read this file when a skill step says "metrics". Each section says which skill uses it.

## Choosing a metric (everscout-beat, everscout-ask)

Start from the beat's research questions (Goal, Question, Metric). A metric earns a row when:

- it answers a numbered research question in `beat.md` (the `question` column starts with `Q<n>`);
- a stranger could recompute it from the one-sentence `definition`;
- you can say what you would conclude if it rose or fell (the actionability test; say it to the user when proposing). If you cannot, it is a vanity metric: do not add it;
- it prefers a share or ratio when the denominator moves (GDELT's `gdelt:` share over `gdelt-raw:` counts, a tally share over a raw count);
- its known distortions are named (vendor press releases inflate news volume; upvotes and stars are gamed).

Grade the source on the Admiralty code: a letter for the source's track record (A reliable to E unreliable, F cannot judge) and a digit for the information (1 confirmed to 5 improbable, 6 cannot judge). Wikimedia pageviews are A2, GDELT volume B2, the beat's own tallies C3, a forum poll E5.

Two to five candidates per beat is enough. At most one `headline: yes`.

## Sources (the `source` and `method` columns)

| method | source | value per period |
|---|---|---|
| `tally` | `tally:notes` | notes the scan kept, by posted date |
| `tally` | `tally:<facet>/<entity>` | notes naming the entity; a `share %` unit divides by the period's notes |
| `api` | `gdelt:<query>` | GDELT DOC 2.0 TimelineVol: mean daily share (%) of monitored online news (last three months only) |
| `api` | `gdelt-raw:<query>` | GDELT TimelineVolRaw: articles per period (summed) |
| `api` | `wikipedia:<project>/<Article>` | Wikimedia pageviews, users, all access, summed (`wikipedia:en.wikipedia/Layoff`) |
| `derived` | `derived:<id> <op> <id>` | `+ - * /` of two metrics on the same dates |
| `manual` | the release or page, in words | entered with `ES stats collect --metric <id> --value N --date <period> --note-ref <url>` |

Periods follow `cadence`: `weekly` and `per scan` are ISO weeks (dated by their Monday), `monthly` by the first of the month, `quarterly` by the quarter's first day. Only complete periods are collected. The first collect backfills up to eight periods (`backfill_periods`), so a candidate often has three points at once. GDELT asks for one request every five seconds and the fetcher keeps ten; Wikimedia gets one a second. A refusal, timeout or missing article is recorded as a row with an empty value and `failed: <reason>`, never retried in the same run. A GDELT refusal also starts a cool-down (1 h, doubling per refusal in a row, at most 24 h); until it passes, collect reports `cooling` for GDELT metrics, sends nothing and writes no row (`kb/platforms.md`, GDELT row).

## Commands

- `ES stats list --beat <slug> [--status candidate,active] [--json]`: the catalog with point counts and last values.
- `ES stats add --beat <slug> --id <id> --question "Q2 ..." --definition "..." --unit count --kind leading --source ... --method ... --cadence weekly --grade B2 [--headline yes]`: adds a candidate. On an existing id it edits; a change to `definition`, `unit`, `source` or `method` bumps `version`, and export splits the series so the break is never drawn as a trend.
- `ES stats collect --beat <slug> [--metric a,b]`: collects every due candidate and active metric.
- `ES stats review --beat <slug>`: lifecycle findings. `--apply` archives the stale and flat ones and stamps `reviewed`; `--promote <id>` after the user says yes; `--archive <id> --reason <reason>`; `--reactivate <id>`.
- `ES stats export --beat <slug> [--metric a,b] [--since date] [--include-archived] [--charts]`: writes `DATA/stats/export.csv` (columns `date, metric, series, value, unit, version, status`) and, when chartwright is installed, prints or (`--charts`) runs its builds into `DATA/reports/charts/`.

## Lifecycle (thresholds are defaults; override under `stats` in config.json)

1. **Propose** (beat, scan, report, ask): add a candidate when a research question has no metric, an entity keeps rising in the tallies, or the user asks the same quantitative question twice. Fill every field.
2. **Promote**: `review` lists a candidate as `promote` after `promote_points` (3) values from a source graded `promote_grade` (C3) or better. Ask the user; only on a yes run `--promote <id>`. Never promote without the yes.
3. **Collect** on cadence during every scan.
4. **Review** with each radar report (monthly) and the whole catalog quarterly.
5. **Archive**, never delete: `stale` (collection failed for the last `fail_streak` (3) periods, however many tries each, or no value for `stale_periods` (3) periods plus the one being completed), `flat` (coefficient of variation under `flat_cv` (0.05) over the last `flat_points` (8) values; keep it instead if a research question depends on its level), and by hand `irrelevant`, `gamed`, `superseded-by:<id>` or `source-gone`. Rows in `series.csv` stay. An archived metric can be reactivated.
6. **Update**: a definition change bumps the version (above).

`review` also shows a trend per metric (least-squares slope over the last eight values: rising, falling or level) and, for two metrics on one question, whether they move together. Show these to the user; they never archive anything.

## In each skill

- **everscout-beat**: a new beat gets two to five candidates in `metrics.md` (the template has one); `beat-check` validates the table. Route "add, promote, archive or change a metric" here.
- **everscout-scan**: after `tally`, run `ES stats collect --beat <slug>`; mention failures and new values in the scan summary; propose a candidate if an entity has been rising for two scans.
- **everscout-report**: before writing the radar, `ES stats collect` then `ES stats review --beat <slug>`; put a "Metrics" section in the report (each active metric's last value, its trend and the review's findings, archived ones named as archived); ask the user about promotions; run `--apply` only after telling them what it will archive. Then `ES stats export --beat <slug> --charts` and link the charts from the report (`../reports/charts/...`). No chartwright: link the CSV and say so. Quarterly: review the whole catalog with the user.
- **everscout-ask**: a quantitative question is answered from `ES stats list --json` and `DATA/stats/series.csv` first (values with their dates, units and versions); if no metric answers it and it would pass the tests above, offer a candidate with `stats add`.
