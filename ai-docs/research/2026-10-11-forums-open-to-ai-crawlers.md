---
title: Which forums let AI crawlers in, and whether Discord or paid API access is an option (October 2026)
kind: research
status: active
date: 2026-10-11
verified: 2026-10-11
tags: [robots-txt, ai-crawlers, terms, reddit-alternatives, bluesky, hacker-news, lemmy, discourse, discord, x-api, reddit]
---

# Forums open to AI crawlers (checked 2026-10-11)

Read this when picking sources for a beat or deciding whether a site may be fetched by an agent.

Method: fetched each site's live `/robots.txt` on 2026-10-11 and parsed it with Python's `urllib.robotparser` for GPTBot, ClaudeBot, CCBot, Google-Extended, PerplexityBot and a generic bot, path `/`. Then read the terms of service for the top candidates. Robots.txt permission is not ToS permission; both are listed.

## Open to all AI crawlers (robots.txt)

| Site | Notes |
|---|---|
| bsky.app (Bluesky) | robots.txt says "may crawl anything", points to the AT Protocol firehose for bulk. ToS (effective 2025-08-14) has no scraping or AI-training clause. Per-user AI-training opt-outs were proposed in March 2025. Best large open source. |
| news.ycombinator.com | Crawl-delay 30. YC ToS bans "data mining, robots, scraping", but the official read-only API (hacker-news.firebaseio.com/v0) is the sanctioned route. |
| lemmy.world | Crawl-delay 60. Fediverse: each instance sets its own rules. |
| boards.4chan.org | Only query-string pages disallowed. |
| slashdot.org | Open. |
| github.com | Names GPTBot, ClaudeBot, PerplexityBot with crawl-delay 1; API preferred. |
| Discourse forums | Default config is open: meta.discourse.org, forum.godotengine.org, forum.cursor.com, community.openai.com. |
| discussions.unity.com | Lists GPTBot, ClaudeBot, CCBot, Google-Extended, PerplexityBot by name with only admin paths blocked: an explicit invitation. |
| dev.to, forums.anandtech.com, discord.com (public pages only) | Open. |

## Partly open

- mastodon.social: blocks GPTBot only.
- tildes.net: blocks GPTBot only.
- resetera.com: blocks GPTBot and Google-Extended.
- forums.somethingawful.com: blocks ClaudeBot only.
- tumblr.com: allows GPTBot, blocks ClaudeBot, CCBot, Google-Extended (Tumblr licensed data to OpenAI).
- medium.com: blocks GPTBot and ClaudeBot.
- quora.com: blocks GPTBot, ClaudeBot, PerplexityBot.

## Closed

- reddit.com: robots.txt itself returns 403; licensed access only (Google, OpenAI). Public RSS still works at a slow pace.
- stackoverflow.com, superuser.com: `Disallow: /` for all plus `Content-signal: search=no, ai-train=no`. Data dumps restricted since July 2024.
- lobste.rs: content-signal blocks AI.
- x.com, threads.net, linkedin.com, facebook.com (CCBot and generic), spiceworks, avsforum, indiehackers: block AI bots.
- metafilter.com, fark.com, bogleheads.org, producthunt.com: Cloudflare challenge on robots.txt itself.

## Discord

The short answer is no: Discord has no free or paid route for an agent to read communities in bulk.

- Terms of Service (effective 2025-09-29), section 9: no "scraping our services without our written consent, including by using any robot, spider, crawler, scraper, or other automatic device". That covers self-bots, meaning automation of a normal user account; Discord bans accounts for these.
- Developer Policy (help-center API, fetched 2026-10-11): "Do not mine or scrape any data, content, or information available on or through Discord services" and "Do not use message content obtained through the APIs to train machine learning or AI models (including large language models) unless express permission is granted by Discord."
- The allowed route is a bot that a server's admin invites. Reading message text needs the privileged Message Content intent. Since 2026-06-10 an app reaching fewer than 10,000 unique users toggles it on in the Developer Portal; above that it must apply within 90 days (docs.discord.com, privileged intent review). So an agent can read and summarise servers the user runs, or servers whose admins invite the bot, for the user's own use. It cannot read arbitrary public servers, and it cannot train on what it reads.
- There is no paid data product for Discord content that we found.
- Answer Overflow (answeroverflow.com) publishes some servers' help channels as public web pages, opt-in per server. Unverified: its site answered with a Vercel bot check on 2026-10-11.

## Paying for access

Mostly true that only large companies can license data, with one exception.

- X: on 2026-02-06 X made pay-per-use the default for new developers. Reported rates: $0.005 per post read, capped at 2 million reads a month, and $0.20 per request for posts containing a URL. Basic ($200/month) and Pro ($5,000/month) are closed to new sign-ups; Enterprise starts at $42,000/month. Secondary sources only (opentermsarchive.org memo, gigazine 2026-02-09); check docs.x.com before relying on the rates.
- Reddit: no new public Data API requests after 2026-10-31, RSS ends 2026-11-13, unregistered apps cut from 2027-01-12, public access closes March 2027. After that the routes are Reddit's own Developer Platform (Devvit, apps that run inside Reddit) or a commercial licence. Secondary sources (techrepublic.com, ppc.land); see skills/everscout-scan/RESEARCH.md R-20261010-1.
- Stack Overflow: licenses data to AI companies through enterprise deals only.
- Discord, Quora, Threads, LinkedIn: no individual data purchase found.

## Sources

- Raw robots.txt files and parser script were in the session scratchpad (not kept); rerun: curl each `https://<host>/robots.txt` and parse with `urllib.robotparser`.
- YC terms: https://www.ycombinator.com/legal/
- Bluesky ToS: https://bsky.social/about/support/tos
- Bluesky AI-intent proposal: https://techcrunch.com/2025/03/15/bluesky-users-debate-plans-around-user-data-and-ai-training/
- Discord terms: https://discord.com/terms
- Discord Developer Policy: https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy
- Discord privileged intents: https://docs.discord.com/developers/gateway/getting-started-with-privileged-intent-review.md
- X pay-per-use: https://opentermsarchive.org/en/memos/x-replaces-its-dollar200-entry-level-api-plan-with-a-pay-per-use-model/
- Reddit API timeline: https://www.techrepublic.com/article/news-reddit-rss-public-api-shutdown/
- Stack Exchange dump restriction: https://devclass.com/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-as-critics-complain-license-permits-reuse-for-any-purpose
