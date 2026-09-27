# Platforms: what everscout can read, and how

What each platform lets a personal scout read without paying, and how to name it in a beat's `sources.md`. Checked 2026-09-26 by live calls; the evidence and the terms clauses are in `ai-docs/research/2026-09-26-platform-access.md`. Platforms change their access every few months: when a source fails `everscout.py probe`, re-check here first, then refresh this file (the everscout-beat skill's research plan covers it).

## Source kinds the CLI fetches

| kind | `source` column | what the CLI calls | pace (per host) | thread reader | notes |
|---|---|---|---|---|---|
| reddit | `r/name` | `/r/<name>/new/.rss` (and `/top/.rss?t=week` with `--listing new,top`) | 45 s plus `x-ratelimit-reset` | yes, `/comments/<id>/.rss` | logged-out Atom feeds are the only keyless route; JSON and old.reddit need login; the Data API needs approval (Responsible Builder Policy). Reddit said on 2026-08-05 the Data API will be restricted gradually; feeds were not mentioned. Watch this. |
| hn | a search query | Algolia `search_by_date`, stories since the fetch window | 1 s | yes, Algolia `/items/<id>` | no write API; generated comments are banned |
| rss | a feed URL | the URL | 3 s default | no | Atom, RSS 2.0 and RSS 1.0; Substack `/feed`, Medium `/feed/@user` or `/feed/tag/<tag>`, Ghost `/rss/`, WordPress `/feed/`, podcasts, Eurostat updates, Bandcamp Daily, arXiv category RSS (`export.arxiv.org/rss/<cat>`), Product Hunt `/feed`, PieFed `/community/<name>/feed` |
| youtube | channel id `UC...` or playlist id `PL...` | `youtube.com/feeds/videos.xml` | 2 s | no | about 15 newest videos with descriptions; the Data API needs a key |
| github | `owner/repo` | `/<owner>/<repo>/releases.atom` | 2 s | no | many model repositories publish no releases (Wan2.2, ComfyUI-LTXVideo and MiniMax-H3 had none on 2026-09-27); then use an `rss` row on `commits/<branch>.atom` or `tags.atom` |
| news | a search query | Google News RSS search | 10 s | no | undocumented; personal alerts only; store the source link, never republish |
| arxiv | an arXiv API query (`all:"video diffusion"`, `cat:econ.GN AND abs:inflation`) | `export.arxiv.org/api/query`, newest first | 15 s (the terms say 3 s; on 2026-09-26 repeated calls 4 s apart drew HTTP 406 for several minutes) | no | for a whole category prefer an `rss` row with `https://rss.arxiv.org/rss/<cat>`; metadata is CC0; never re-serve PDFs |
| mastodon | `#tag@instance` or `@user@instance` | `/tags/<tag>.rss` or `/@user.rss` | 3 s | yes, `/api/v1/statuses/<id>` and `/context` | some instances turn off logged-out tag feeds (then the row fails `probe`: try another instance); status search needs a token |
| bluesky | `@handle` or a feed generator `at://<did>/app.bsky.feed.generator/<rkey>` | profile RSS, or `app.bsky.feed.getFeed` on `public.api.bsky.app` | 1 to 2 s | yes, `getPostThread` | `searchPosts` needs login since 2025; a topic feed generator is the keyless way to follow a subject; find one with the web search or bsky.app's feed directory |
| lemmy | `c/name@instance` | `/feeds/c/<name>.xml?sort=New` | 3 s | yes, `/api/v3/post` and `/api/v3/comment/list` | |
| discourse | a forum base URL, or a category URL `https://forum/c/<slug>/<id>` | `/latest.rss`, or the category `.rss` | 3 s | yes, `/t/<id>.json` (first 20 posts) | a forum may require login; the default anonymous limit is 200 a minute |
| huggingface | `models?pipeline_tag=<tag>`, `spaces`, or `daily_papers` | `huggingface.co/api/...`, trending first | 3 s | no | good for "which models are rising"; the item is the model, not a discussion |
| web | a site name | nothing | | no | a reminder row: read by hand with the agent's web fetch |

Every request sends `everscout/<version> (+https://github.com/m4bwav/everscout; <contact>)`, and Reddit gets its required `<platform>:everscout:v<version> (by /u/<user>)`. Set `contact` and `reddit_user` in `config.json`. Never swap in a browser User-Agent: a source that only answers a browser string is left out (Bing News was left out for this reason).

## Statistics sources (beat metrics, `stats collect`)

Checked 2026-09-27 by live calls; evidence in `ai-docs/research/2026-09-27-beat-statistics.md`.

| `source` | what the CLI calls | pace | notes |
|---|---|---|---|
| `gdelt:<query>`, `gdelt-raw:<query>` | `api.gdeltproject.org/api/v2/doc/doc?mode=TimelineVol` (share %) or `TimelineVolRaw` (counts), `format=json`, start and end dates | 6 s | keyless; searches the last three months only; over its pace it answered HTTP 429 with a plain-text "Please limit requests to one every 5 seconds" (recorded as a failed value, not retried in the run; a non-JSON body is never cached); query syntax: quoted phrases, `OR` inside parentheses |
| `wikipedia:<project>/<Article>` | `wikimedia.org/api/rest_v1/metrics/pageviews/per-article/<project>/all-access/user/<Article>/daily/<start>/<end>` | 1 s | keyless and documented; an article that does not exist answers 404 (recorded as failed); the title is the URL form (`Trip_hop`) |

Google Trends stays out: pytrends is archived, the official API is a closed alpha, and the replacements scrape through proxies (research note section 1).

## Keyed sources (not built in; the agent may use them when the user has a key)

Bluesky post search (app password), OpenAlex (free key; the keyless allowance is $0.10 a day since 2026), Semantic Scholar (free key, 1 a second), FRED API (free key), YouTube Data API (free key; 100 searches a day), Last.fm (free key), Discogs (free token, 60 a minute), Podcast Index (free key and secret), GitHub REST (PAT, 5,000 an hour), Product Hunt GraphQL (token).

## Data APIs worth knowing (no key; the agent fetches them directly)

World Bank `api.worldbank.org/v2/...?format=json`, IMF SDMX 3.0 `api.imf.org/external/sdmx/3.0/...` and DataMapper `imf.org/external/datamapper/api/v1/...`, OECD SDMX `sdmx.oecd.org/public/rest/...` (60 data queries an hour), ECB `data-api.ecb.europa.eu/service/data/...`, BIS `stats.bis.org/api/v2/...`, Eurostat `ec.europa.eu/eurostat/api/dissemination/...`, MusicBrainz `/ws/2/...` (1 a second, contact in the User-Agent), ListenBrainz `/1/stats/sitewide/artists` and `/1/explore/fresh-releases`, Civitai `/api/v1/models`. These are data, not discussion: a report cites them, a scan pairs them with the commentary.

## Closed, or forbidden to scrape

X/Twitter (no free reads), Threads keyword search (needs Meta approval), Instagram and TikTok (business or academic only), Discord (only servers your bot was invited to; self-bots banned), Telegram (the `t.me/s/` preview answers, but the terms forbid scraping), Bandcamp (no API; the Acceptable Use Policy forbids scraping and AI ingestion; only `daily.bandcamp.com/feed` is fine), SoundCloud (API closed), Resident Advisor (no API). Everscout does not read these. A beat that needs one says so in `beat.md` and relies on the user's own reading plus the web search.

## When a source fails

`everscout.py probe --beat <slug>` prints one line per source. `BAD 404` means the community or feed is gone (remove the row or fix the name). `BAD 403` or "not a feed" means a login wall or a block page: stop, do not retry within the hour, record it in the row's notes, and look for the platform's current rule here and in the research note. `429` is handled by the fetcher (it waits and retries up to three times).
