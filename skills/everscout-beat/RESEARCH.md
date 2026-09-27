# Research: everscout-beat

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin.

Topic: how to define a subject for continuous community monitoring, which platforms and communities can be read and engaged with, and how their access rules change. Tier `fast`. Last refresh 2026-09-26; next due 2026-10-10.

## Current understanding

- A beat is five markdown files plus a study outline; the watch list is the part that rots fastest (communities rename, rules change, platforms close routes).
- Keyless routes that work on 2026-09-26: Reddit Atom feeds (about one request a minute), Hacker News Algolia, Mastodon tag and account RSS, Lemmy and PieFed, Discourse, YouTube channel RSS, GitHub atom, arXiv, Hugging Face JSON, Bluesky profile RSS and feed generators, blogs and newsletters (ai-docs/research/2026-09-26-platform-access.md).
- Closed or forbidden: X, Threads search, Instagram, TikTok, Discord, Telegram scraping, Bandcamp scraping, SoundCloud API.
- Bluesky searchPosts needs login since 2025; Reddit plans to restrict the Data API gradually (announced 2026-08-05; feeds not mentioned).
- Two-phase discovery (seed searches find communities, then each is read) is the pattern last30days and GummySearch used (prior-art note).
- Community stances on AI and on questions move monthly: the CHI 2025 study found AI rules doubling in 16 months, 55 percent of them bans.

The full evidence is in the repository's research notes: `ai-docs/research/2026-09-26-platform-access.md`, `2026-09-26-engagement-ethics.md`, `2026-09-26-prior-art.md`, `2026-09-26-sample-beats.md`.

## Open questions

- Does Reddit's Devvit migration (deadline 2026-12-31) touch the logged-out RSS feeds?
- Which Bluesky feed generators are stable enough to rely on per subject?
- Is there a keyless way to discover Mastodon tags across instances beyond per-instance hashtag search?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the period since the last refresh, with the year.

Subject:

- `"<platform>" API OR RSS changes <month year>`
- `reddit RSS feeds logged out <year>`
- `bluesky searchPosts authentication <year>`
- `best communities for <subject> <year> site:reddit.com`

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
