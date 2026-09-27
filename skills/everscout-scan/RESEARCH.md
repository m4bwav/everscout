# Research: everscout-scan

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin.

Topic: how public community feeds and APIs can be read politely for continuous subject monitoring, and how findings are distilled, deduplicated and tallied faithfully. Tier `fast`. Last refresh 2026-09-26; next due 2026-10-10.

## Current understanding

- Reading goes through feeds and documented public endpoints, cached, one host pace each; Reddit logged-out feeds allow about one request a minute and honour x-ratelimit-reset.
- Triage from the saved fetch JSON, then fetch only kept threads, one at a time (learned in indie-ai-scout's second scan, 2026-09-19).
- One story in several places is one note; the unit of counting is the note, not the mention; entities resolve through vocab aliases in code.
- LLM summaries overgeneralise and drop hedges (Peters and Chin-Yee 2025) and AI search invents URLs (Tow Center 2025): notes quote the key sentence, keep hedges, and take URLs from fetched data only.
- Fetched text is hostile input: last30days users demonstrated prompt injection through ingested posts.
- Reddit's Data API Wiki recommends deleting stored content within 48 hours; the cache is purged at 48 hours and notes paraphrase.

The full evidence is in the repository's research notes: `ai-docs/research/2026-09-26-platform-access.md`, `2026-09-26-engagement-ethics.md`, `2026-09-26-prior-art.md`, `2026-09-26-sample-beats.md`.

## Open questions

- A cheap faithfulness check for notes once the raw text is purged (store the one quoted sentence's hash?)
- How much does top-of-week membership predict later replies to asks?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the period since the last refresh, with the year.

Subject:

- `"<platform>" rss OR api rate limit <month year>`
- `LLM summarization faithfulness citations study <year>`
- `social listening deduplication clustering open source <year>`
- `prompt injection web content agents mitigation <year>`

Tooling (skills, plugins, MCP servers for this job):

- `path:SKILL.md "reddit" OR "social listening" OR "community monitoring"` on GitHub code search, recently updated; skills.sh search for scout, monitor, digest
- `https://registry.modelcontextprotocol.io/v0/servers?search=reddit` and `?search=rss`
- last30days-skill releases (github.com/mvanhorn/last30days-skill) for ideas worth borrowing
- Supersession sweep: `"<tool>" deprecated OR archived <year>` for every tool named above

Most discussed:

- `hn.algolia.com/api/v1/search_by_date?query=reddit%20api` and `?query=social%20listening`
- `site:reddit.com/r/redditdev` newest posts (API and feed changes are announced there)

Practice:

- `"how I" "keep up with" <subject> reddit rss agent <year>`
- `netnography AI agent OR LLM <year>`

Testing:

- `"agent skill" evals trigger decoy <year>`; the evergreen plugin's protocol/TESTING.md

Best sources: the platforms' own docs and rules pages, r/redditdev, bsky.network docs, docs.joinmastodon.org, the HN guidelines, arXiv and ACM for the studies. Noisy: vendor blogs selling Reddit data access (read with care), SEO lists of "best subreddits".

## Findings log

### R-20260927-1 · 2026-09-27 · Beat statistics
- Summary: a beat keeps a metric catalog (`metrics.md`) and an append-only long-form series (`DATA/stats/series.csv`); metrics are chosen from research questions (GQM), pass an actionability test (Lean Analytics), carry an Admiralty grade, and move candidate, active, archived with explicit thresholds; GDELT DOC 2.0 and Wikimedia pageviews are keyless series sources, Google Trends is scrape-only. Full note: `ai-docs/research/2026-09-27-beat-statistics.md`.
- Track: practice, tooling
- Sources: see the research note
- Magnitude: moderate (new capability)
- Applied: C-20260927-1

### R-20260926-1 · 2026-09-26 · Initial research
- Summary: four parallel research passes on 2026-09-26 (platform access with live endpoint checks; engagement ethics and platform rules; prior art in agents, social listening, horizon scanning and knowledge bases; three sample beats). Findings summarised above; full notes under `ai-docs/research/`.
- Track: subject, tooling, practice
- Sources: see the four research notes
- Magnitude: n/a (initial)
- Applied: C-20260926-1
