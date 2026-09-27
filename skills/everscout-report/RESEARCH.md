# Research: everscout-report

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin.

Topic: how to turn community monitoring into faithful trend reports and a sourced baseline study: horizon-scanning signal methods, radar formats, citation faithfulness. Tier `medium`. Last refresh 2026-09-26; next due 2026-10-26.

## Current understanding

- Signals and trends are different levels: a trend needs a cluster of three or more independent signals across two consecutive reports (IFTF; GO-Science Futures Toolkit).
- Magnitude times growth (Nesta) is the honest way to say hot, emerging or stabilising; hype-cycle stages are not (Dedehayir and Steinert 2016).
- The ThoughtWorks radar (quadrants, Adopt/Trial/Assess/Hold, new or moved, a rationale per blip) is the report's core table.
- AI citations fail often (Tow Center 2025: over 60 percent wrong; EBU/BBC 2025: 31 percent sourcing issues), so every external link must be held by a note, a snapshot or the source log (everscout.py lint).
- STORM's perspective-seeded outline, approved by the user before writing, is the shape of the baseline study.

The full evidence is in the repository's research notes: `ai-docs/research/2026-09-26-platform-access.md`, `2026-09-26-engagement-ethics.md`, `2026-09-26-prior-art.md`, `2026-09-26-sample-beats.md`.

## Open questions

- Should the radar's rings be proposed by the tally (thresholds) or only judged? 0.1.0 judges them with numbers beside.
- A span check for quotes once raw text is purged

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the period since the last refresh, with the year.

Subject:

- `horizon scanning weak signals method <year>`
- `technology radar format build your own <year>`
- `AI search citation accuracy study <year>`
- `STORM co-storm outline research agent <year>`

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

### R-20260926-1 · 2026-09-26 · Initial research
- Summary: four parallel research passes on 2026-09-26 (platform access with live endpoint checks; engagement ethics and platform rules; prior art in agents, social listening, horizon scanning and knowledge bases; three sample beats). Findings summarised above; full notes under `ai-docs/research/`.
- Track: subject, tooling, practice
- Sources: see the four research notes
- Magnitude: n/a (initial)
- Applied: C-20260926-1
