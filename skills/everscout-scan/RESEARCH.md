# Research: everscout-scan

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin.

Topic: how public community feeds and APIs can be read politely for continuous subject monitoring, and how findings are distilled, deduplicated and tallied faithfully. Tier `fast`. Last refresh 2026-09-26; next due 2026-10-10.

## Current understanding

- Reading goes through feeds and documented public endpoints, cached, one host pace each; Reddit logged-out feeds allow about one request a minute and honour x-ratelimit-reset, but Reddit has announced RSS ends on 2026-11-13, no new public Data API requests after 2026-10-31, unregistered apps cut on 2027-01-12 and the public Data API gone by March 2027 (R-20261010-1). The user chose the Arctic Shift archive for the Reddit lane on 2026-10-15 (plugin 0.4.0, `reddit.reader` auto switches on 2026-11-13); Reddit's undocumented web endpoints and paid scrapers stay out of bounds.
- Triage from the saved fetch JSON, then fetch only kept threads, one at a time (learned in indie-ai-scout's second scan, 2026-09-19).
- One story in several places is one note; the unit of counting is the note, not the mention; entities resolve through vocab aliases in code.
- LLM summaries overgeneralise and drop hedges (Peters and Chin-Yee 2025) and AI search invents URLs (Tow Center 2025): notes quote the key sentence, keep hedges, and take URLs from fetched data only.
- Fetched text is hostile input: last30days users demonstrated prompt injection through ingested posts.
- Reddit's Data API Wiki recommends deleting stored content within 48 hours; the cache is purged at 48 hours and notes paraphrase.

The full evidence is in the repository's research notes: `ai-docs/research/2026-09-26-platform-access.md`, `2026-09-26-engagement-ethics.md`, `2026-09-26-prior-art.md`, `2026-09-26-sample-beats.md`.

## Open questions

- Arctic Shift after March 2027 (its maintainer's issue #76 leaves it open); Gemini URL context is the planned backup (repo ai-docs/plans/2026-10-15-reddit-via-gemini-url-context.md).
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
- `site:reddit.com/r/redditdev` newest posts (API and feed changes are announced there); `"r/redditdev" RSS feed rate limit <month year>` found the 2026 shutdown at once

Practice:

- `"how I" "keep up with" <subject> reddit rss agent <year>`
- `netnography AI agent OR LLM <year>`

Testing:

- `"agent skill" evals trigger decoy <year>`; the evergreen plugin's protocol/TESTING.md

Best sources: the platforms' own docs and rules pages, r/redditdev, bsky.network docs, docs.joinmastodon.org, the HN guidelines, arXiv and ACM for the studies. Noisy: vendor blogs selling Reddit data access (read with care), SEO lists of "best subreddits".

## Findings log

### R-20261010-1 · 2026-10-10 · Reddit retires RSS and the public Data API
- Summary: announced 2026-09-30 in r/modnews with a technical post in r/redditdev: no new public API access requests after 2026-10-31; RSS ends 2026-11-13 ("if you use RSS for feeds outside a community you moderate, there is no replacement"); apps not registered with the Developer Platform lose access 2027-01-12; remaining public Data API ends March 2027; old Reddit limited to logged-in users. Community reports say RSS is already throttled before the cutoff (generic user agents near-constant 429; about one request per 5 s with a custom one, unofficial). Primary posts not fetched (refused or skipped for the rate limit); five secondary outlets agree on the dates. The ai-video fetch on 2026-10-10 still read 46 sources and 601 items in about 10 minutes.
- Track: subject
- Sources: https://mjtsai.com/blog/2026/10/06/reddit-to-remove-rss/, https://thenextweb.com/news/reddit-rss-feeds-shut-down-old-reddit-ai-scraping, https://decrypt.co/379892/reddit-killing-rss-feeds-public-api-access-ai-scrapers, https://aiweekly.co/alerts/reddit-to-shut-rss-feeds-nov-13-close-public-api-by-march-2027
- Magnitude: 0.8 (the Reddit lane's access route ends; affects every beat and the plugin, not only this skill)
- Applied: C-20261010-2

### R-20261010-2 · 2026-10-10 · last30days-skill drops its Reddit RSS lane for an undocumented web endpoint
- Summary: v3.26.0 (2026-10-01, PR #1189) removed RSS discovery because of the November cutoff and now reads Reddit's internal shreddit search fragments, with paid ScrapeCreators backfill; v3.27.x hardens redirects and escapes topics as JSON against injection. Scraping an internal surface conflicts with this unit's documented-endpoints rule; recorded as the route others took, not to adopt.
- Track: tooling, practice
- Sources: https://github.com/mvanhorn/last30days-skill/releases, https://github.com/mvanhorn/last30days-skill/pull/1189
- Magnitude: 0.4
- Applied: C-20261010-2 (named in the rule as out of bounds)

### R-20261010-3 · 2026-10-10 · Injection through ingested posts seen in live attacks; registries quiet
- Summary: Unit 42 reports hidden-instruction pages making summarising agents exfiltrate data or call tools; skill audits flag research skills that pass search results to sub-agents without boundary markers. Backs the existing "fetched text is data" rule; adopted as an eval case. Tooling: two new Reddit MCP servers (2026-10-06, no usage signals, both exposed to the shutdown) and paid Bluesky social-listening servers, none doing what this procedure does. GDELT: one request per 5 s is already recorded in kb/platforms.md with a stricter 10 s pace and cool-down, so nothing new. Testing method: nothing new since skill-creator's March 2026 update. Faithfulness: nothing newer than Peters and Chin-Yee 2025. Bluesky claim unchanged.
- Track: testing, tooling, subject
- Sources: https://explainx.ai/blog/what-is-indirect-prompt-injection-ai-agents-guide-2026, https://agentguard.gopluslabs.io/advisor/AGS-2026-0020, https://registry.modelcontextprotocol.io/v0/servers?search=reddit
- Magnitude: 0.3
- Applied: C-20261010-3

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
