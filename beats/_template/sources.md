# Sources: {{TITLE}}

The watch list. `everscout.py` parses the first table; keep the column names. One row per source.

- `source`: `r/<name>` (reddit), a feed URL (rss), a query (hn, news, arxiv), a channel id `UC...` or playlist `PL...` (youtube), `owner/repo` (github releases), `#tag@instance` or `@user@instance` (mastodon), `@handle` or a feed generator `at://.../app.bsky.feed.generator/...` (bluesky), `c/name@instance` (lemmy), a forum base URL or category URL (discourse), `models?pipeline_tag=...`, `spaces` or `daily_papers` (huggingface), or a site name (web: read by hand, never fetched).
- `kind`: reddit, rss, youtube, github, hn, news, arxiv, mastodon, bluesky, lemmy, discourse, huggingface, web.
- `stance`: how the community treats the kind of engagement and content this beat cares about: `native` (the subject is the point), `open`, `mixed` (allowed, expect pushback), `hostile` (banned or reliably downvoted), `anti` (read for sentiment only), `n/a` (a feed with no community).
- `engage`: `yes` only for a community with a showcase culture whose rules allow ordinary comments. Everything else is read only.
- `scan`: `no` keeps the row for reference and drops it from `fetch`.
- `filter`: optional terms, F5Bot style: bare words any-of, `+word` required, `-word` excluded, quotes for phrases. Use it on broad sources (news, hn, a general subreddit).
- `notes`: size, rules, what it yields, and a marker: ✓ YYYY-MM-DD verified from the rules page or the feed on that date · ~ believed, not verified · ? unknown.

| source | kind | group | stance | engage | scan | filter | notes |
|---|---|---|---|---|---|---|---|
| r/example | reddit | core | native | yes | yes | | ? TODO replace with real rows; verify with `everscout.py probe --beat {{SLUG}}` |
| "example query" | hn | news | n/a | no | yes | | ? |
