# Research: everscout-engage

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin.

Topic: how to ask creators and practitioners about their work online without reading as automation or spam, and what platforms and communities allow for AI-assisted comments. Tier `fast`. Last refresh 2026-10-30.

## Current understanding

- The user is the author and presses post; everscout drafts, the user approves and pastes; the ledger records it (kb/conduct.md rule 1).
- Human review is necessary and not sufficient: the 2025 Zurich r/changemyview study reviewed every comment and was condemned for hidden AI, invented personas, profiling and rule-breaking (engagement-ethics note).
- Hacker News bans generated and AI-edited comments since 2026-03-11; r/changemyview and mastodon.social require disclosure; the CHI 2025 study found 55 percent of subreddit AI rules are bans.
- Reddit labels accounts run by software (2026-03-31) and asks for human verification on unusually rapid posting; it does not label AI-written text by humans.
- Questions raise liking and reply rates; long, complex messages lower them (Huang et al. 2017; Arguello et al. 2006). Asking 'is this AI' reads as an accusation.
- EU AI Act Art. 50(4), from 2026-08-02: personal use is out of scope; reviewed text with editorial responsibility is exempt. The AI Omnibus (in force 2026-07-27) gave a grace period only to Art. 50(2) marking, not to 50(4) (R-20261023-1).
- GitHub has no platform rule on AI comments; projects set their own (rust-lang/rust bans LLM text; Bitcoin Core allows it only quoted and disclosed) and maintainers can limit issues and comments to collaborators.
- Reddit's logged-out `.json` and old.reddit already need a login (since mid-2026), so neither is a fallback reader after RSS ends.

The full evidence is in the repository's research notes: `ai-docs/research/2026-09-26-platform-access.md`, `2026-09-26-engagement-ethics.md`, `2026-09-26-prior-art.md`, `2026-09-26-sample-beats.md`.

## Open questions

- Answer rates by platform and pace: no study found; collect from the ledger
- What replaces `ES thread` for Reddit after logged-out RSS ends on 2026-11-13: a capture the user saves, or a route the scan skill's Reddit lane plan picks (R-20261011-1)? Narrowed 2026-10-23: Arctic Shift (opt-in) or a capture; last30days-skill v3.29 uses windowed Arctic Shift queries to get real scores, worth borrowing if ours return zero scores.
- Does Bluesky's automated-account label apply to a person using drafting help (no, by the docs; re-checked 2026-10-23: still no official post)

## Search plan

- Fetch platform rules pages directly (news.ycombinator.com/newsguidelines.html, mastodon.social `/api/v1/instance/rules`, forge.rust-lang.org policies, bsky.social/about/blog); news search is noise for rule changes.

Four tracks; every refresh runs at least one query on each, scoped to the period since the last refresh, with the year.

Subject:

- `reddit rules AI generated comments <month year>`
- `hacker news guidelines AI comments <year>`
- `subreddit bans AI written comments <year>`
- `EU AI Act article 50 guidance personal use <year>`
- `how to ask creators questions reply rate study`
- Official forums, announcements first, then known issues, since `last_checked`: r/redditdev and r/modnews (https://www.reddit.com/r/redditdev/new, https://www.reddit.com/r/modnews/new; read through fetchwright or captures, never WebFetch), Reddit Help Center policy pages (https://support.reddithelp.com), Bluesky (https://github.com/bluesky-social/atproto/discussions, https://bsky.social/about/blog), Mastodon (https://github.com/mastodon/mastodon/discussions, https://blog.joinmastodon.org), Hacker News (https://news.ycombinator.com/newsguidelines.html, dang's moderation comments via hn.algolia.com `author_dang`)

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

- `"agent skill" evals trigger decoy <year>`, `"skill discovery" eval trace <year>`; the evergreen plugin's protocol/TESTING.md

Also: github.blog/changelog for maintainer controls; EUR-Lex for the AI Omnibus text. Reddit-dated news is secondary only (digitalapplied.com had the fullest milestone table; techrepublic returns 403).

Best sources: the platforms' own docs and rules pages, r/redditdev, bsky.network docs, docs.joinmastodon.org, the HN guidelines, arXiv and ACM for the studies. Noisy: vendor blogs selling Reddit data access (read with care), SEO lists of "best subreddits".

## Findings log

### R-20261030-1 · 2026-10-30 · Subject: r/opensource bans AI projects from 2026-10-24; Reddit dates hold

- Summary: r/opensource moderators barred projects that use, are made by, or are for AI, effective 2026-10-24 (secondary coverage); one more subreddit where an AI-assisted ask must check the sidebar rules first, which the per-community rules check already covers. Bluesky rules on agent replies and DMs remain unclear (Blotato survey, 2026-10-08). Reddit dates unchanged: new Data API requests close 2026-10-31, RSS ends 2026-11-13. Tooling: nothing new. Testing: nothing new.
- Track: subject
- Sources: https://letsdatascience.com/news/ropensource-moderators-ban-ai-projects-and-draw-backlash-ac4ed72a, https://www.blotato.com/research/social-media-automation-rulebook, https://www.techwyse.com/news/social-media/reddit-rss-feeds-ending-public-api-shutdown-2027
- Magnitude: 0.2
- applied: none (research only)

### R-20261023-1 · 2026-10-23 · Testing: add a discovery case; GitHub row gains Bitcoin Core and maintainer limits; Reddit dates hold
- Summary: Expo's skill-eval post (2026-10-08) grades triggering from prompts that never name the skill, three runs each, and warns that crowded catalogs truncate descriptions; the suite had no such case. Bitcoin Core PR #35386 was merged 2026-07-07 (AI text only in a disclosed quote block; human-written replies); GitHub has no platform AI-comment rule but lets maintainers limit issues and comments to collaborators (2026-06). Reddit timeline unchanged (RSS ends 11-13; new API requests close 10-31; update 11-10; porting-bounty registration 11-30; unregistered apps 2027-01-12; public access ends 2027-03); logged-out .json and old.reddit already require login. Rules pages re-read: HN, mastodon.social rule 1008, Bluesky blog, Discourse unchanged. EU AI Omnibus delays only Art. 50(2). Tooling: last30days-skill v3.26 to v3.30 keep keyless Reddit via Arctic Shift (windowed queries for scores); new MCP-registry Reddit servers are monitors, none drafts with pace checks. Practice: LinkedIn added an "AI slop" report button and classifiers for generic AI comments (supports short, specific questions); no new outreach backlash case. Testing: see above.
- Track: testing, subject, tooling, practice
- Sources: https://expo.dev/blog/your-skills-need-an-evaluation-mechanism.md, https://github.com/bitcoin/bitcoin/pull/35386, https://visualstudiomagazine.com/articles/2026/06/30/github-extends-contribution-controls-from-prs-to-issues.aspx, https://www.digitalapplied.com/blog/reddit-api-rss-shutdown-ai-tools-deadlines, https://news.ycombinator.com/newsguidelines.html, https://mastodon.social/api/v1/instance/rules, https://www.iubenda.com/en/blog/ai-omnibus-adopted-august-2-obligations-july-2026/, https://github.com/mvanhorn/last30days-skill/releases, https://registry.modelcontextprotocol.io/v0/servers?search=reddit, https://www.fastcompany.com/91545007/linkedin-declares-war-on-ai-slop
- Magnitude: 0.3 (a better check that becomes a case); the rest under 0.2
- Applied: C-20261023-1 (evals/evals.json trigger-3; kb/conduct.md GitHub row and synced copies; RESEARCH.md)

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
