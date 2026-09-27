# Research: everscout-engage

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin.

Topic: how to ask creators and practitioners about their work online without reading as automation or spam, and what platforms and communities allow for AI-assisted comments. Tier `fast`. Last refresh 2026-09-26; next due 2026-10-10.

## Current understanding

- The user is the author and presses post; everscout drafts, the user approves and pastes; the ledger records it (kb/conduct.md rule 1).
- Human review is necessary and not sufficient: the 2025 Zurich r/changemyview study reviewed every comment and was condemned for hidden AI, invented personas, profiling and rule-breaking (engagement-ethics note).
- Hacker News bans generated and AI-edited comments since 2026-03-11; r/changemyview and mastodon.social require disclosure; the CHI 2025 study found 55 percent of subreddit AI rules are bans.
- Reddit labels accounts run by software (2026-03-31) and asks for human verification on unusually rapid posting; it does not label AI-written text by humans.
- Questions raise liking and reply rates; long, complex messages lower them (Huang et al. 2017; Arguello et al. 2006). Asking 'is this AI' reads as an accusation.
- EU AI Act Art. 50(4), from 2026-08-02: personal use is out of scope; reviewed text with editorial responsibility is exempt.

The full evidence is in the repository's research notes: `ai-docs/research/2026-09-26-platform-access.md`, `2026-09-26-engagement-ethics.md`, `2026-09-26-prior-art.md`, `2026-09-26-sample-beats.md`.

## Open questions

- Answer rates by platform and pace: no study found; collect from the ledger
- Does Bluesky's automated-account label apply to a person using drafting help (no, by the docs; re-check)

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the period since the last refresh, with the year.

Subject:

- `reddit rules AI generated comments <month year>`
- `hacker news guidelines AI comments <year>`
- `subreddit bans AI written comments <year>`
- `EU AI Act article 50 guidance personal use <year>`
- `how to ask creators questions reply rate study`

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
