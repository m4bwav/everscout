# Metrics: Down-tempo, trip-hop and chill electronic music

The beat's recurring numbers, one row per metric (format: `kb/SCHEMA.md`, section metrics.md; design: `ai-docs/research/2026-09-27-beat-statistics.md`). Values live in the data folder's `stats/series.csv` (`everscout.py stats collect`). Starter rows are candidates: each becomes active after three collected points and the user's yes (`stats review --promote <id>`). Never delete a row: archive it with a reason.

| id | question | definition | unit | kind | source | method | cadence | grade | status | version | created | reviewed | archive_reason | headline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| notes-per-week | Q2 which artists and releases are rising | Notes the scan kept per week, by posted date | count | leading | tally:notes | tally | weekly | C3 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
| wiki-trip-hop | Q4 the trip-hop revival | Weekly English Wikipedia pageviews (users, all access) of Trip hop | count | leading | wikipedia:en.wikipedia/Trip_hop | api | weekly | A2 | candidate | 1 | 2026-09-27 | 2026-09-27 |  | yes |
| wiki-downtempo | Q4 the trip-hop revival | Weekly English Wikipedia pageviews (users, all access) of Downtempo | count | leading | wikipedia:en.wikipedia/Downtempo | api | weekly | A2 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
