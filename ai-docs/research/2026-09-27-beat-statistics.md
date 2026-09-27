---
title: Beat statistics (how scouts, reporters and analysts keep numbers on a subject, and a metric design for everscout)
kind: research
status: active
date: 2026-09-27
verified: 2026-09-27
tags: [metrics, statistics, time-series, lifecycle, chartwright, gqm, intelligence]
summary: read before adding metrics, statistics or charts to everscout beats; prior art, selection and retirement practice, and the proposed metric schema, storage and lifecycle (design only, not built)
---

# Beat statistics (researched 2026-09-27)

Mark wants each beat to gather statistics: define metrics, collect them over time, propose new ones, update old ones and archive the ones that stop mattering, so a growing data pool can feed charts through chartwright. This note is research and a design. Nothing is implemented yet. All sources were read or searched on 2026-09-27 unless a date says otherwise; claims taken only from search snippets are marked "(snippet)".

## Summary

- No agent skill found does the whole loop (define, collect, review, retire) for a topic. Skills that mention metrics are frameworks for product managers with no storage, or agent-performance monitors. Everscout has to build the loop; it can reuse free keyless sources for the numbers.
- Reporters and intelligence analysts agree on the method: start from the questions, keep a short list of recurring sources, grade each source, and write the definition down so the number means the same thing next month.
- Metric frameworks (GQM, Lean Analytics, Goodhart) give the selection test: every metric answers a named question and would change what you think or do. Data teams retire metrics by marking them, recording why, and keeping history, never by deleting.
- Proposed design: `metrics.md` per beat (the catalog, in the beat folder), `DATA/stats/series.csv` (one long-form CSV for all values, which chartwright's `cw.py build --series` reads directly), and a review step in everscout-scan with explicit thresholds.

## 1. Prior art: tools that track topic metrics over time

- **Agent skills.** A GitHub search surfaced `insight68/Skills` `metrics-tracking/SKILL.md` ([github.com/insight68/Skills](https://github.com/insight68/Skills/blob/main/skills/metrics-tracking/SKILL.md)). It is a framework guide: a North Star plus L1 and L2 metrics, reviewed weekly, monthly and quarterly. It stores nothing and never retires a metric. Other hits were agent-performance monitors (`ArieGoldkin/ai-agent-hub` observability-monitoring, agent-skills.md performance-tracking), which are not about subjects. `rate-source-admiralty` on skills.rest ([skills.rest](https://skills.rest/skill/rate-source-admiralty-radarist)) grades sources on the Admiralty axes and is the closest intelligence-style skill (snippet only). The last30days skill from the 2026-09-26 prior-art note ([2026-09-26-prior-art.md](2026-09-26-prior-art.md)) ranks by engagement and has an optional SQLite store, but keeps no defined metric series.
- **Google Trends.** pytrends was archived in April 2025. Google's official Trends API is an alpha you have to apply for, announced July 2025, with no release date ([trendsmcp.ai, 2026](https://www.trendsmcp.ai/blog/best-pytrends-alternatives-python-2026); [meetglimpse.com](https://meetglimpse.com/software-guides/pytrends-alternatives/)). The MCP servers and Apify actors that replace it scrape through rotating residential proxies ([apify.com](https://apify.com/surefetch/google-trends/api/mcp)). Everscout's conduct rules (documented endpoints, honest User-Agent) rule out scraping, so Trends stays out until the official API opens.
- **GDELT DOC 2.0 API.** Keyless. `mode=TimelineVol` returns matching coverage as a percentage of all monitored articles per time step, and `TimelineVolRaw` returns raw counts ([blog.gdeltproject.org](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/); [raw counts](https://blog.gdeltproject.org/gdelt-2-0-api-now-supports-raw-result-counts/)). A good source for a "news attention" metric per beat. Its normalisation is a lesson worth copying: store a share as well as a count when the denominator moves.
- **Wikimedia pageviews API.** Keyless, documented, daily per-article views ([Simon Willison TIL](https://til.simonwillison.net/wikipedia/page-stats-api)); endpoint `wikimedia.org/api/rest_v1/metrics/pageviews/per-article/...`. A good public-attention proxy for entities in a beat's vocabulary.
- **Open-source social listening.** ListeningKit ([github.com/valekar/listeningkit](https://github.com/valekar/listeningkit)) watches Reddit, HN and RSS. `MartinezWendy/social-listening-pipeline` ([github](https://github.com/MartinezWendy/social-listening-pipeline)) computes yearly share of voice with a slope per term (snippet). Share of voice and a fitted slope map onto everscout's existing entity tallies.
- **Metric stores.** The dbt Semantic Layer (MetricFlow) centralises metric definitions as code and exposes them through APIs ([docs.getdbt.com](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl)). Its own history is a lifecycle lesson: the original `dbt_metrics` package was deprecated in favour of MetricFlow ([getdbt.com](https://www.getdbt.com/blog/dbt-semantic-layer-whats-next)). Guidance around it treats metrics as products with an owner, a review cadence and a deprecation policy ([atlan.com](https://atlan.com/dbt-semantic-layer/), snippet).

| tool | what it measures | time-series storage | retires metrics? | everscout: reuse or build |
|---|---|---|---|---|
| insight68 metrics-tracking skill | product KPIs (framework only) | none | no | reuse the review cadence idea |
| last30days skill | engagement per item | optional SQLite | no | nothing new |
| rate-source-admiralty skill | source reliability grade | none known | n/a | reuse the A to F / 1 to 6 grading |
| Google Trends (pytrends, MCP scrapers) | search interest 0 to 100 | caller's job | no | skip: archived or scraped |
| GDELT DOC 2.0 | news volume, share and raw | API returns series | no | reuse as a source adapter |
| Wikimedia pageviews | daily article views | API returns series | no | reuse as a source adapter |
| ListeningKit, social-listening-pipeline | mentions, share of voice, slope | own database | no | build: tallies already exist |
| dbt Semantic Layer | business metrics as code | warehouse | by policy, not tooling | reuse definition-as-file and status |

## 2. How reporters keep statistics on a beat

- IRE's NICAR has trained reporters in computer-assisted reporting since 1989 and keeps a data library of recurring datasets ([GIJN guide](https://gijn.org/resource/data-journalism-gijns-global-guide-to-resources/)). The pattern is a small set of datasets a beat reporter refreshes on their release schedule, not an ad hoc search each time.
- DataJournalism.com's guide to bringing data to deadline stories asks beat reporters "What topics keep coming up over and over on your beat?" and "What are people talking about that you'd like to prove is true or not true?" ([datajournalism.com](https://datajournalism.com/read/longreads/how-to-bring-the-power-of-data)). Those two questions are good prompts for proposing a candidate metric.
- The Data Journalism Handbook 2 ([datajournalism.com](https://datajournalism.com/read/handbook/two)) treats data as made, not found: every number carries the choices of whoever counted it. For everscout that means a metric records its definition and method with the value, and a definition change starts a new version.
- A beat book, as NBCU Academy describes beat building ([nbcuacademy.com](https://nbcuacademy.com/journalism-beat/)), holds the sources, the recurring documents and their release calendar. Everscout's `sources.md` is already the source half; `metrics.md` would be the recurring-numbers half.
- Not found: a primary source for a "number every week" newsroom rule. Treat it as a practice, not a cited standard.

## 3. How competitive-intelligence analysts do it

- **KITs and KIQs.** Jan Herring's Key Intelligence Topics process (1999) starts from what the decision-maker needs, in three kinds: strategic decisions, early warnings and key players ([Wiley, Herring 1999](https://onlinelibrary.wiley.com/doi/abs/10.1002/(SICI)1520-6386(199932)10:2%3C4::AID-CIR3%3E3.0.CO;2-C)). KIQs refine each topic into answerable questions ([Klue](https://klue.com/blog/get-your-kits-together)). A beat's research questions in `beat.md` already play the KIT role; each metric should name the question it answers.
- **Intelligence cycle.** SCIP defines CI as the legal and ethical collection and analysis of information for planning and decisions (quoted in [McGonagle, Salus Journal 2016](https://salusjournal.com/wp-content/uploads/2016/02/McGonagle_Salus_Journal_Volume_4_Number_1_2016_pp_13-24.pdf)). The cycle (requirements, collection, analysis, dissemination, feedback) has a feedback step, which is where a metric gets reviewed and retired.
- **Source grading.** The Admiralty (NATO) code grades the source A to F on its track record and the information 1 to 6 on corroboration, separately. F6 means no basis to judge, not distrust ([Wikipedia](https://en.wikipedia.org/wiki/Admiralty_code); [SANS](https://www.sans.org/blog/enhance-your-cyber-threat-intelligence-with-the-admiralty-system)). Source reliability is cumulative over reports, which fits a metric that is collected repeatedly.
- **Leading and lagging.** Early-warning KITs need leading indicators (attention and chatter that move before outcomes); outcome questions need lagging ones (releases, prices, hires). Classifying each metric as leading or lagging is judgment borrowed from KPI practice; no single primary source was found for it today.

## 4. Choosing metrics and retiring them

- **GQM.** Basili's Goal, Question, Metric method works top down: goal, then the questions that characterise it, then the metrics that answer each question. It exists because teams collected data with no link to a goal ([Basili et al., UMD](https://www.cs.umd.edu/users/mvz/handouts/gqm.pdf)). Everscout maps it directly: beat scope (goal), research question (question), metric.
- **Actionable against vanity.** Lean Analytics (Croll and Yoskovitz): a good metric is comparative, understandable and usually a ratio or rate, and if you do not know what you would do differently when it moves, it is a vanity metric ([holistics.io](https://www.holistics.io/blog/lean-analytics-part-1-an-introduction-to-analytical-thinking/)). "One metric that matters" per stage suggests each beat flags one headline metric.
- **Goodhart and Campbell.** A measure that becomes a target stops being a good measure; the more a social indicator is used for decisions, the more it is corrupted ([Wikipedia](https://en.wikipedia.org/wiki/Goodhart's_law)). For a scout, the risk is counts that communities or vendors inflate (stars, upvotes, press volume). Prefer ratios and cross-source metrics, and record the known distortions.
- **Retirement practice.** Organisations add metrics faster than they retire them. KPI pruning guides say to flag a candidate for retirement, record what it was for and why that no longer applies, check where it is used, and archive rather than delete ([kpitree.co](https://kpitree.co/guides/how-to/how-to-sunset-a-metric); [Sigma](https://www.sigmacomputing.com/blog/kpi-graveyard-useless-metrics); snippets). Dashboard certification is usually reviewed quarterly ([Basedash](https://www.basedash.com/blog/dashboard-sprawl-how-to-audit-certify-and-retire-dashboards), snippet). Julie Zhuo argues for a weekly team metrics review ([Medium](https://joulee.medium.com/why-your-team-needs-a-weekly-metrics-review-dcc9cce7ac3c)).
- **Platform-forced retirement.** Sources remove metrics too, as Facebook did in March 2024 ([Emplifi](https://docs.emplifi.io/platform/latest/home/facebook-metrics-deprecation-march-2024)). A source that stops answering is an archive reason of its own.

## 5. Recommended design for everscout (not built)

### 5.1 Metric catalog: `metrics.md` in the beat folder

One table row per metric, flat so `beat-check` can parse it. The fields:

| field | meaning |
|---|---|
| id | slug, unique in the beat, never reused (`hn-mentions-sora`) |
| question | the research question from `beat.md` it answers (GQM link) |
| definition | one sentence a stranger could recompute from |
| unit | count, share %, index, currency, rank |
| kind | leading or lagging |
| source | a `sources.md` row, or an external endpoint (GDELT, Wikimedia, a statistics office release) |
| method | `tally` (from notes), `api` (an adapter), `manual` (read from a release), `derived` (from other metrics) |
| cadence | per scan, weekly, monthly, on release |
| grade | Admiralty source grade A to F plus credibility 1 to 6 (`B2`) |
| status | candidate, active or archived |
| version | starts at 1; a definition change bumps it |
| created, reviewed | ISO dates |
| archive_reason | stale, flat, irrelevant, source-gone, superseded-by:<id>, or free text |
| headline | yes on at most one metric per beat |

Built-in beats could ship two or three candidate metrics each; private beats hold their own.

### 5.2 Time series: `DATA/stats/series.csv`

Long form, one row per observation, append only:

`date,metric,version,value,unit,source,note_ref`

- `date` is the period the value describes (ISO), not the collection time; a second column `collected` is optional.
- One file for the whole beat, because chartwright's `cw.py build --data FILE.csv --x date --y value --series metric` draws many metrics from long-form CSV, and `cw.py data FILE.csv` profiles it without reading it into the model. A per-chart filtered CSV can be written with a CLI filter (`ES stats export --metric a,b`).
- Archived metrics keep their rows. History is never deleted.
- JSONL was considered; CSV wins because chartwright reads CSV and it opens in any spreadsheet.

### 5.3 Lifecycle rules

Thresholds below are judgment unless a source is named; revisit them after three months of real data.

1. **Propose.** During a scan, report, or ask, the skill may add a `candidate` row when a research question has no metric, a vocabulary entity keeps rising in tallies, or the user asks a quantitative question twice (the DataJournalism.com "keeps coming up" prompt). A candidate must fill every field and pass the actionability test (Lean Analytics): write what you would conclude if it rose or fell.
2. **Promote** to active after at least three collected points from a source graded C3 or better, and the user's yes in the session (judgment). Promotion is logged.
3. **Collect** on its cadence during everscout-scan. A failed collection is recorded as a row with an empty value and a note, so gaps are visible.
4. **Review** monthly with the radar report (matches the report cadence; weekly for metrics with weekly cadence is optional), and quarterly for the whole catalog (dashboard practice, Basedash). Each review stamps `reviewed`.
5. **Archive** when any of these holds, with the reason recorded:
   - stale: no new value for three cadence periods, or the source failed three times in a row (judgment);
   - flat: coefficient of variation under 5% across the last eight points and no research question depends on its level (judgment);
   - irrelevant: its research question was dropped or answered, or the user says it no longer changes what they think (GQM, Lean Analytics);
   - gamed: evidence the number is being inflated (Goodhart); superseded: a better metric answers the same question.
   Archiving never deletes rows; an archived metric can be reactivated with a log line.
6. **Update.** A definition or source change bumps `version`; charts split series by version so a break is not drawn as a trend.

Also check each active metric at review: a trend test (slope over the last eight points) and, where there are two metrics on one question, whether they move together. These are shown to the user, not used to auto-archive.

### 5.4 Where it lives in the skills

- everscout-beat: create `metrics.md` with the beat (two to five candidates from the research questions), and a new route "add, review or retire a metric". `beat-check` validates the table.
- everscout-scan: collect due metrics after the tally, append to `series.csv`, list proposals.
- everscout-report: the radar gets a metrics section and runs the monthly review.
- everscout-ask: may answer from `series.csv` and propose a candidate.
- A separate everscout-stats skill is not recommended yet; five skills already compete for triggers (see the 2026-09-26 tidy in [../log.md](../log.md)). Revisit if the metric routes crowd the beat skill.
- CLI (later): `ES stats list|add|collect|review|export`, standard library only, tested with synthetic fixtures. New keyless adapters: GDELT timeline and Wikimedia pageviews, each with a `kb/platforms.md` row.

### 5.5 Chart hooks

- The radar calls chartwright with `series.csv`: a line chart per question (`--series metric`), a sparkline row for the headline and active metrics in Markdown, and a small-multiples view at the quarterly review.
- Charts go to `DATA/reports/charts/`, linked from the report. Archived metrics are drawn greyed or left out, never silently removed from history.

## Open questions

- Whether Google's official Trends API becomes available to individuals (alpha since July 2025); recheck at the next everscout-beat refresh.
- Whether tallies should be normalised by notes per scan (a share) as GDELT normalises by all coverage. Probably yes; decide when building.
