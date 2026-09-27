# Metrics: Global economics and macro

The beat's recurring numbers, one row per metric (format: `kb/SCHEMA.md`, section metrics.md; design: `ai-docs/research/2026-09-27-beat-statistics.md`). Values live in the data folder's `stats/series.csv` (`everscout.py stats collect`). Starter rows are candidates: each becomes active after three collected points and the user's yes (`stats review --promote <id>`). Never delete a row: archive it with a reason.

| id | question | definition | unit | kind | source | method | cadence | grade | status | version | created | reviewed | archive_reason | headline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| notes-per-week | Q4 what economists disagree about | Notes the scan kept per week, by posted date | count | leading | tally:notes | tally | weekly | C3 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
| news-tariffs-share | Q2 tariffs and the energy shock in prices and trade | Mean daily share (%) of GDELT-monitored online news matching tariffs | share % | leading | gdelt:tariffs | api | weekly | B2 | candidate | 1 | 2026-09-27 | 2026-09-27 |  | yes |
| wiki-inflation | Q2 tariffs and the energy shock in prices and trade | Weekly English Wikipedia pageviews (users, all access) of Inflation | count | leading | wikipedia:en.wikipedia/Inflation | api | weekly | A2 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
