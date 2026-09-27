# Changelog

Plugin versions, newest first. Skill-level changes are in each skill's `CHANGELOG.md`; the session log is `ai-docs/log.md`.

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
