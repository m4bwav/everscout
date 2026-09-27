# Metrics: Developer and tech hiring

The beat's recurring numbers, one row per metric (format: `kb/SCHEMA.md`, section metrics.md; design: `ai-docs/research/2026-09-27-beat-statistics.md`). Values live in the data folder's `stats/series.csv` (`everscout.py stats collect`). Starter rows are candidates: each becomes active after three collected points and the user's yes (`stats review --promote <id>`). Never delete a row: archive it with a reason.

| id | question | definition | unit | kind | source | method | cadence | grade | status | version | created | reviewed | archive_reason | headline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| notes-per-week | Q1 where demand is rising or falling | Notes the scan kept per week, by posted date | count | leading | tally:notes | tally | weekly | C3 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
| news-tech-layoffs | Q6 layoffs, rehiring and offshoring | Weekly count of GDELT-monitored online news articles matching layoffs with tech, software or startup | count | leading | gdelt-raw:layoffs (tech OR software OR startup) | api | weekly | B2 | candidate | 2 | 2026-09-27 | 2026-09-27 |  | yes |
| wiki-layoff | Q6 layoffs, rehiring and offshoring | Weekly English Wikipedia pageviews (users, all access) of Layoff | count | leading | wikipedia:en.wikipedia/Layoff | api | weekly | A2 | active | 1 | 2026-09-27 | 2026-09-27 |  |  |
