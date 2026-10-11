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
- What replaces `ES thread` for Reddit after logged-out RSS ends on 2026-11-13: a capture the user saves, or a route the scan skill's Reddit lane plan picks (R-20261011-1)?
- Does Bluesky's automated-account label apply to a person using drafting help (no, by the docs; re-checked 2026-10-11: still only service bots in a March 2026 report, no official post)

## Search plan

- Fetch platform rules pages directly (news.ycombinator.com/newsguidelines.html, mastodon.social `/api/v1/instance/rules`, forge.rust-lang.org policies, bsky.social/about/blog); news search is noise for rule changes.

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

### R-20261011-1 · 2026-10-11 · Subject: Reddit's RSS ends 2026-11-13; HN rules cover posts and automation; GitHub projects ban LLM-written comments
- Summary: Reddit announced (2026-09-30, secondary sources) that logged-out RSS ends 2026-11-13, new Data API requests close 2026-10-31, unregistered apps lose access 2027-01-12 and public access ends March 2027; Step 2 reads Reddit threads through RSS, so after 11-13 a Reddit item can be read only from a capture the user saves (the scan skill's R-20261010-1 and the repository's Reddit lane plan cover the reading side). The live Hacker News guidelines ban generated text in posts and automated posting, not only generated or AI-edited comments. rust-lang/rust adopted a policy (2026-08-05) that LLM-created text may not be posted as GitHub comments, issues or PR descriptions even after editing; Bitcoin Core PR #35386 proposes the same. Discourse forums are moving to automatic AI labels (EA Forum, July 2026; NixOS has a disclosure rule). arXiv 2606.12073: pejorative AI-use accusations rose more than tenfold on HN and Reddit 2023 to 2026, which backs rule 8. Tooling: Reddit "growth" MCP servers automate replies and DMs (the anti-pattern); nothing combines drafting with pace checks and a ledger. Testing: no case proved the "ideas only" branch.
- Track: subject, practice, tooling, testing
- Sources: https://decrypt.co/379892/reddit-killing-rss-feeds-public-api-access-ai-scrapers, https://ppc.land/reddit-to-halt-public-data-api-access-in-march-2027-as-14-000-apps-register/, https://news.ycombinator.com/newsguidelines.html, https://forge.rust-lang.org/policies/llm-usage.html, https://blog.rust-lang.org/inside-rust/2026/08/05/rust-langrust-is-adopting-an-llm-policy/, https://forum.effectivealtruism.org/posts/bxA9fsY9Psgarcq6e/ea-forum-llm-use-policy, https://papers.cool/arxiv/2606.12073, https://registry.modelcontextprotocol.io/v0/servers?search=reddit
- Magnitude: 0.4 (Reddit reading changes on a known date; the conduct table gains a GitHub row)
- Applied: C-20261011-1 (SKILL.md Step 2; kb/conduct.md Platform notes; evals/evals.json outcome-1 and new outcome-2)

### R-20260926-1 · 2026-09-26 · Initial research
- Summary: four parallel research passes on 2026-09-26 (platform access with live endpoint checks; engagement ethics and platform rules; prior art in agents, social listening, horizon scanning and knowledge bases; three sample beats). Findings summarised above; full notes under `ai-docs/research/`.
- Track: subject, tooling, practice
- Sources: see the four research notes
- Magnitude: n/a (initial)
- Applied: C-20260926-1
