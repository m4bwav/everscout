---
title: What each platform lets a personal scout read and write without paying (September 2026)
kind: research
status: active
date: 2026-09-26
verified: 2026-09-26
tags: [platforms, api, rss, rate-limit, terms, reddit, bluesky, mastodon, lemmy, discourse, hn, youtube]
summary: read before adding or changing a source adapter; endpoint shapes, auth, limits and terms per platform, verified by live calls on 2026-09-26 (V) or from secondary sources (R)
---

# Platform access for everscout (checked 2026-09-26)

## Summary

A no-key tier covers most of what a scout needs: Reddit Atom feeds, Hacker News (Algolia), Mastodon tag and account RSS, Lemmy and PieFed, Discourse, YouTube channel RSS, blogs and newsletters, arXiv, GitHub atom feeds, Hugging Face and Civitai JSON, Bluesky profile RSS and feed generators, and the public economic data APIs. Bluesky post search, OpenAlex, Semantic Scholar, FRED, YouTube Data, Last.fm, Discogs and Podcast Index want a free key or login. X, Threads search, Instagram, TikTok and Discord are closed to a personal scout; Bandcamp and Telegram forbid scraping. Condensed guidance for agents is in `kb/platforms.md`; this note keeps the evidence.

V = a live call from Mark's PC on 2026-09-26 with the UA `everscout-research/0.1 (+https://github.com/m4bwav)`, or the primary doc read that day. R = secondary source.

## Headline changes

- **Reddit.** Logged-out Atom feeds still answer (V: `/r/LocalLLaMA/new/.rss` 200). On 2026-08-05 Reddit said in r/redditdev that the public Data API will be restricted "gradually" and third-party apps must port to Devvit; existing apps register by 2026-09-30, migration programme deadline 2026-12-31, no Data API shutdown date, "won't happen this year" (R: reddit.com/r/redditdev/comments/1vgbm9c, support.reddithelp.com article 47822311698452). RSS is not mentioned. Watch this: it is the most likely break for everscout.
- **OpenAlex.** The mailto polite pool is gone; without a key $0.10 of usage a day (V: `X-RateLimit-Limit-USD: 0.1`), a free key $1 a day (V: help.openalex.org/access/pricing, updated 2026-08-11).
- **Bluesky search.** `public.api.bsky.app/.../searchPosts` returns 403 (V); `api.bsky.app` gives page one only and 403 on any cursor (V). Treat search as needing login.
- **YouTube Data API.** A separate 100 search calls a day, plus 10,000 units a day for the rest (V: developers.google.com/youtube/v3/getting-started, updated 2026-09-14).
- **X.** No free tier for new developers since pay-per-use on 2026-02-06; reads cost $0.005 each (R).

## Per platform

| platform | read without a key | limits | write (personal account) | notes |
|---|---|---|---|---|
| Reddit | `/r/<sub>/new/.rss`, `/top/.rss?t=week`, thread `/comments/<id>/.rss`, search `.rss` (V) | about 1 a minute logged out; honour `x-ratelimit-reset` | browser only; Data API needs approval (Responsible Builder Policy) | 48-hour deletion rule for stored content |
| Hacker News | Algolia `hn.algolia.com/api/v1/search`, `/search_by_date`, `/items/<id>` (V); Firebase `/v0/item/<id>.json` (V) | Algolia 10,000 an hour per IP (V) | none; bots discouraged | read only |
| Bluesky | profile RSS `bsky.app/profile/<handle>/rss` (V); `public.api.bsky.app` `getAuthorFeed`, `getProfile`, `searchActors`, `getPostThread`, `getFeed` for feed generators (V) | AppView "generous" (no numbers); PDS 3,000 per 5 minutes per IP | app password, `createSession`, `createRecord`; self-label as automated (label since app v1.119, 2026-03-19) | `searchPosts` needs login; a topic feed generator is the keyless way to follow a subject |
| Mastodon | `/tags/<tag>.rss`, `/@user.rss` (V); `/api/v1/timelines/tag/<tag>` (V on mastodon.social, fosstodon.org); `/api/v2/search?type=hashtags` with usage history (V) | 300 per 5 minutes per IP (V) | personal token, `POST /api/v1/statuses`; set the bot flag | public timeline 422 logged out; status search needs a token and is opt-in per post; some instances disable logged-out tag feeds; never touch `#nobot` accounts |
| Lemmy | `/api/v3/post/list?community_name=`, `/api/v3/search`, `/feeds/c/<name>.xml` (V) | per instance | JWT login; `bot_account` flag | |
| PieFed | `/api/alpha/post/list`, `/community/<name>/feed` (V) | per instance | | `/c/<name>/feed` is 404 |
| Discourse | `/latest.json`, `/latest.rss`, `/search.json`, `/c/<slug>/<id>.rss`, `/t/<id>.json`, `/t/<slug>/<id>.rss` (V, meta.discourse.org) | default anonymous 50 per 10 s and 200 a minute per IP (V) | user API key | a site may require login |
| YouTube | channel `feeds/videos.xml?channel_id=UC...` and playlist `?playlist_id=PL...` (V), about 15 newest videos | | OAuth | Data API optional, free key |
| Blogs, newsletters | Substack `/feed`, Medium `/feed/@user` and `/feed/tag/<tag>`, Ghost `/rss/`, WordPress `/feed/` (V) | | | store summaries and links, not full texts |
| Podcasts | show RSS | | | Podcast Index API needs a free key and secret (V 401) |
| arXiv | `export.arxiv.org/api/query`, `export.arxiv.org/rss/<cat>` (V) | one request every 3 seconds, one connection (V, info.arxiv.org/help/api/tou.html) | | metadata CC0; do not re-serve PDFs |
| Semantic Scholar | shared pool, 429 when busy (V) | free key 1 a second | | |
| OpenAlex | $0.10 a day without key (V) | free key $1 a day | | |
| GitHub | `/<o>/<r>/releases.atom`, `/tags.atom`, `/commits/<branch>.atom` (V) | REST 60 an hour logged out; search 10 a minute (V) | PAT | atom feeds do not count against REST |
| Hugging Face | `/api/models?sort=trendingScore`, `/api/spaces?sort=trendingScore`, `/api/daily_papers` (V) | 500 calls per 5 minutes per IP (V) | token | |
| Civitai | `/api/v1/models?sort=Newest`, `/api/v1/images` (V) | none published | | anonymous capped at the public browsing level |
| Product Hunt | `producthunt.com/feed` (V) | | GraphQL needs a token | API not for commercial use |
| Google News | `news.google.com/rss/search?q=...&hl=en-US&gl=US&ceid=US:en` (V) | undocumented; be gentle | | terms bar republishing; personal alerts only, keep source links |
| Bing News | RSS only to a browser UA (V) | | | left out: getting it would mean faking a browser UA |
| Economic data | World Bank, IMF SDMX 3.0 and DataMapper, OECD SDMX (60 data queries an hour, R), ECB, BIS, Eurostat and its update RSS (all V) | | | FRED API needs a free key; FRED graph CSV works but is undocumented |
| MusicBrainz | `/ws/2/<entity>?query=&fmt=json` (V) | 1 a second; UA `App/ver ( contact )` required (V) | | |
| ListenBrainz | `/1/stats/sitewide/artists`, `/1/explore/fresh-releases/?days=7` (V) | | token to submit | |
| Discogs | search answered keyless today, 25 a minute (V) | free token 60 a minute | | may re-lock |
| Last.fm | free key required (V) | 100 MB cache cap; non-commercial (V) | | |
| SoundCloud | closed (V 401) | | | oEmbed only |
| Bandcamp | no API; the Acceptable Use Policy forbids scraping and AI ingestion (R) | | | only `daily.bandcamp.com/feed` (V) |
| Resident Advisor | no API; old RSS 404 (V) | | | no |
| X / Twitter | no free reads (R) | | | no |
| Threads | keyword search needs `threads_keyword_search` approval (R) | | own account via API | no for monitoring |
| Instagram, TikTok | no (Business accounts only; research API academic only) (R) | | | no |
| Discord | only servers your bot was added to; self-bots banned (R) | | | no |
| Telegram | `t.me/s/<channel>` answers (V) but the ToS forbids scraping (V, telegram.org/tos) | | Bot API in your own channels | no |

## Design consequences (applied in es_sources.py and kb/platforms.md)

1. Default adapters are keyless: reddit, rss (any feed), youtube, github, hn, news, arxiv, mastodon, bluesky, lemmy, discourse, huggingface.
2. Thread readers (post plus comments) exist for Reddit, HN, Bluesky, Mastodon, Lemmy and Discourse; everything else is read with the agent's web fetch.
3. Per-host gaps: Reddit 45 s plus the reset header, arXiv 3 s, MusicBrainz 1.1 s, Google News 10 s, others 1 to 3 s; back off on 429 and 503 and honour `Retry-After`.
4. The User-Agent names everscout, its repository and the user's contact; never a browser string.
5. Keyed sources are optional and documented, not built in, in 0.1.0.

Related: [prior art](2026-09-26-prior-art.md), [engagement ethics](2026-09-26-engagement-ethics.md)
