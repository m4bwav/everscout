# Metrics: AI video generation

The beat's recurring numbers, one row per metric (format: `kb/SCHEMA.md`, section metrics.md; design: `ai-docs/research/2026-09-27-beat-statistics.md`). Values live in the data folder's `stats/series.csv` (`everscout.py stats collect`). Starter rows are candidates: each becomes active after three collected points and the user's yes (`stats review --promote <id>`). Never delete a row: archive it with a reason.

| id | question | definition | unit | kind | source | method | cadence | grade | status | version | created | reviewed | archive_reason | headline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| notes-per-week | Q6 which techniques are rising | Notes the scan kept per week, by posted date | count | leading | tally:notes | tally | weekly | C3 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
| wiki-text-to-video | Q5 how audiences receive AI video | Weekly English Wikipedia pageviews (users, all access) of Text-to-video model | count | leading | wikipedia:en.wikipedia/Text-to-video_model | api | weekly | A2 | candidate | 1 | 2026-09-27 | 2026-09-27 |  | yes |
| news-ai-video-share | Q5 how audiences receive AI video | Mean daily share (%) of GDELT-monitored online news matching "AI video" | share % | leading | gdelt:"AI video" | api | weekly | B2 | candidate | 1 | 2026-09-27 | 2026-09-27 |  |  |
