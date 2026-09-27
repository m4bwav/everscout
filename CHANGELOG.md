# Changelog

Plugin versions, newest first. Skill-level changes are in each skill's `CHANGELOG.md`; the session log is `ai-docs/log.md`.

## 0.3.0 · 2026-09-27

Beat statistics, built from the approved design in `ai-docs/research/2026-09-27-beat-statistics.md` (section 5).

- because: Mark wants each beat to gather statistics over time, propose and retire metrics, and feed chartwright; the research note found no skill that does the loop and set the schema, storage and lifecycle.
- Metric catalog `metrics.md` per beat (id, question, definition, unit, kind, source, method, cadence, Admiralty grade, status, version, created, reviewed, archive_reason, headline), validated by `beat-check`. The template and the four starter beats ship candidates (notes per week, GDELT news volume, Wikipedia pageviews), sources checked live on 2026-09-27.
- Append-only `DATA/stats/series.csv` (`date,metric,version,value,unit,source,note_ref`); failed collections are rows with an empty value.
- CLI `stats list|add|collect|review|export`. Adapters: tally (notes or an entity, count or share), GDELT DOC 2.0 TimelineVol and TimelineVolRaw, Wikimedia pageviews, derived, manual. Network reads go through the paced fetcher with a 60 s timeout (GDELT took 45 s for an OR query on 2026-09-27) and no retries; a refusal is never cached.
- Lifecycle in `stats review`: promotion after 3 points at grade C3 or better on the user's yes; archive as stale (3 failed periods, or no value for 3 periods), flat (CV under 5% over 8 points), irrelevant, gamed or superseded; never deletes rows; a definition change bumps the version and export splits the series. Thresholds configurable under `stats` in config.json. Trends and co-movement shown, never acted on.
- `stats export` writes a chartwright-ready long CSV and, when chartwright is found, prints or builds (`--charts`) a line chart, sparklines and small multiples into `DATA/reports/charts/`. Chartwright stays optional.
- Skills: everscout-beat defines metrics, everscout-scan collects, everscout-report reviews and charts, everscout-ask reads the series (procedure in `kb/stats.md`). beat and report descriptions updated with skill-tidy (check OK).
- `kb/SCHEMA.md` and `kb/platforms.md` document the files and the two new sources. 45 offline tests (15 new); root plugin evals 12/12 after the description changes.

## 0.2.2 · 2026-09-26

- The five skill descriptions shortened with skill-tidy so each is under the 1,024-character spec cap (some hosts drop longer ones), under 200 words and at most 12 quoted phrases, with every trigger meaning kept and a boundary sentence naming the siblings. ask 1,415 to 962 chars, beat 1,081 to 926, engage 1,165 to 1,011, report 1,102 to 920, scan 1,096 to 949.
- New `evals/` at the plugin root: 12 trigger and decoy cases for `claude plugin eval . --ablation none --no-publish --trust-plugin` (runs on native Windows); first run 12/12. `evals/results/` is ignored.

## 0.2.1 · 2026-09-26

- `followups` recognises replies imported without a comment id (matched by time), so a migrated ledger does not collect the same answer twice. Found moving indie-ai-scout onto everscout as the private beat `indie-ai-games` (its plan and log are in indie-ai-scout's private doc set).

## 0.2.0 · 2026-09-26

- New skill **everscout-ask**: interrogate a beat like a reporter. It recalls what the beat's knowledge base holds, grades whether that is enough and fresh (corrective retrieval: enough, partial, none), researches the gaps in the beat's communities, data pages and the web, answers with what the scout had seen, what is new, where sources disagree, confidence and unknowns, and saves the answer under `answers/` so the next question starts from it.
- CLI: `recall --beat --q` ranks notes, answers, reports, study and the journal against a question and prints the signals for the entities it names; `index` and `lint` cover `answers/`; `fetch --peek` reads without marking items seen; vocabulary aliases also match their plural.
- Tested headless: "Ask my tech-hiring scout: are companies moving interviews back on-site because of AI cheating?" passed 3 of 3 (everscout-ask TESTS.md, T-20260926-1).
- New built-in beat **tech-hiring** (developer and tech hiring), the first beat built from scratch by everscout-beat: 33 sources (15 subreddits, 5 Hacker News queries, Indeed Hiring Lab, the Pragmatic Engineer, Crunchbase News, Google News, Mastodon, data pages), 49 entities in 5 facets, 27 question seeds, an 11-chapter study outline.

## 0.1.2 · 2026-09-27

From the second headless test of "set up a scout for ai video generation" (everscout-beat TESTS.md, T-20260927-2, 3 of 3 passed).

- `probe --save` merges a partial probe into the day's snapshot instead of overwriting it.
- The built-in ai-video beat takes the test run's verified refresh: 46 sources, all answering on 2026-09-27; three GitHub rows moved to commit feeds (the repositories publish no releases); AI film newsletters, a Bluesky feed generator, arXiv and Lemmy added; PixVerse, KlingAI and SeedVR2 in the vocabulary.
- Procedure and platform guide: check `releases.atom` before adding a GitHub row; prefer arXiv category RSS.

## 0.1.1 · 2026-09-26

Fixes from the first headless test of "set up a scout for ai video generation" (everscout-beat TESTS.md, T-20260926-1).

- `probe` checks Reddit through multireddit requests, ten subreddits each, and probes alone only the ones that do not appear.
- everscout-beat waits for the probe instead of ending with it running, and refreshes a matching starter beat with a discovery pass instead of only copying it.

## 0.1.0 · 2026-09-26

First release. A topic-agnostic scout, generalised from the private indie-ai-scout 0.3.1.

- Beats: a subject is a folder of markdown files (`beat.md`, `sources.md`, `vocab.md`, `questions.md`, `searches.md`, `study.md`). Built-in starter beats `ai-video`, `global-economics`, `downtempo`, and `_template`. Private beats in `~/.everscout/beats` shadow built-in ones.
- Sources, all keyless, checked live on 2026-09-26: Reddit Atom feeds, Hacker News (Algolia), Bluesky (profile RSS, feed generators, threads), Mastodon (tag and account RSS, threads), Lemmy (community RSS, threads), Discourse (latest and category RSS, topics), any RSS or Atom feed, YouTube channel and playlist feeds, GitHub releases, arXiv API, Hugging Face trending models, spaces and daily papers, Google News search. One paced, cached fetcher with a per-host gap, an honest User-Agent, retries on 429, 503 and transient 406.
- Notes with one list field per vocabulary facet, prefilled by alias matching; `validate`, `tally` (counts, 30-day velocity, spread, decayed weight, signal new, rising, steady, fading, dormant), `index`, `lint` (report and study links resolve; external URLs must be held by a note, a snapshot or the source log), `source-log`, `retention`.
- Engagement: `candidates`, `questions`, one ledger across beats with per-platform pace rules (`engage-check`, `engage-record`, `engage-update`, `ledger`, `followups`). Everscout never posts; the person pastes.
- Knowledge base: `kb/conduct.md` (a 20-rule conduct code from the engagement-ethics research), `kb/platforms.md`, `kb/method.md` (netnography stages, signal rubric, radar rings, faithfulness rules), `kb/SCHEMA.md`, `kb/voice-template.md`.
- Four evergreen skills: everscout-beat, everscout-scan, everscout-engage, everscout-report, each with research, changelog, learnings, tests and evals.
- Research notes under `ai-docs/research/`: platform access, engagement ethics, prior art, sample beats.
