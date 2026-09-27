# Metrics: Personal and professional websites

The beat's recurring numbers, one row per metric (format: `kb/SCHEMA.md`, section metrics.md; design: `ai-docs/research/2026-09-27-beat-statistics.md`). Values live in the data folder's `stats/series.csv` (`everscout.py stats collect`). Starter rows are candidates: each becomes active after three collected points and the user's yes (`stats review --promote <id>`). Never delete a row: archive it with a reason.

| id | question | definition | unit | kind | source | method | cadence | grade | status | version | created | reviewed | archive_reason | headline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| notes-per-week | Q1 what a well-received site looks like | Notes the scan kept per week (all notes, by posted date) | count | leading | tally:notes | tally | weekly | C3 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
| wiki-indieweb | Q6 the small-web revival | Weekly English Wikipedia pageviews (users, all access) of IndieWeb | count | leading | wikipedia:en.wikipedia/IndieWeb | api | weekly | A2 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
