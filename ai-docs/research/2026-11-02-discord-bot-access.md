---
title: Reading Discord with a free bot (November 2026)
kind: research
status: active
date: 2026-11-02
verified: 2026-11-02
tags: [discord, bot, message-content-intent, developer-policy, rate-limits]
summary: the evidence behind kb/discord.md and es_discord.py; read before changing either
Related: see also [../decisions/2026-11-02-discord-bot-read-only.md](../decisions/2026-11-02-discord-bot-read-only.md)
---

# Reading Discord with a free bot

Read this before changing `kb/discord.md` or `scripts/es_discord.py`. All checked 2026-11-02.

## Sources and what they say

- **Developer Policy** (support-dev.discord.com, article 8563934450327; effective 2024-07-08, last updated 2024-06-06; read through fetchwright because the help centre answers 403 to plain fetchers). Rules that bind a reader: 2 (no processes on a user's or server's behalf without permission), 3 (respect removal and opt-out), 4 (never ask for credentials or tokens), 5 (no unsolicited contact), 13 (no automated activity messages), 15 (use API data only for the stated function), 16 (no profiling), 18 (no selling), 20 ("Do not mine or scrape any data, content, or information available on or through Discord services"), 21 ("Do not use message content obtained through the APIs to train machine learning or AI models (including large language models) unless express permission is granted by Discord").
- **Gateway docs, Message Content intent** (docs.discord.com/developers/events/gateway; discord.com/developers/docs now redirects there): the intent "permits your app to receive message content data across the APIs", so REST message reads return empty `content`, `embeds`, `attachments`, `components` and `poll` without it. Exceptions: the app's own messages, DMs with the app, messages that mention it. Apps in 100 or more servers must verify; apps under 10,000 unique users can switch privileged intents on in the portal, above that a review applies.
- **Message resource** (docs.discord.com/developers/resources/message): `GET /channels/{id}/messages`, `limit` 1 to 100 (default 50), one of `around`/`before`/`after`; needs View Channel, and without Read Message History it returns no messages. `GET /guilds/{id}/messages/search` exists, needs Read Message History and the Message Content intent; the page does not say whether a bot token may call it. Untested.
- **Reference** (docs.discord.com/developers/reference): base `https://discord.com/api`, v10 current; `Authorization: Bot <token>`; User-Agent must be `DiscordBot ($url, $versionNumber)`; snowflake time = `(id >> 22) + 1420070400000` ms.
- **Rate limits** (docs.discord.com/developers/topics/rate-limits): 50 requests a second per bot globally plus per-route buckets; 429 body has `retry_after` (seconds) and `global`; headers `X-RateLimit-Limit`, `-Remaining`, `-Reset`, `-Reset-After`, `-Bucket`, `-Global`, `-Scope`. 10,000 invalid requests (401, 403, 429) in 10 minutes block the IP for a while.

## Unverified

- 2026-11-02 live `check`: token works (bot m4bwav-scout-reader, id 1566996995728482334); Public Bot is still ON and the Message Content Intent is OFF; 0 servers. After Mark set Install Link to None (needed before Public Bot can go off) and flipped both: `check` public no, intent on; `invite` link worked; bot added to his own server (1 guild, 2 text channels); `guilds`, `channels`, `threads`, `read --days 3650` (text present), `search` all work. `read --days 1` wrongly warned the intent was off: the only message was the bot's join system message (fixed in 0.10.1).
- The current Developer Terms of Service text: the help centre article could not be read on 2026-11-02 (fetchwright got an access error). The 2020 terms required a privacy policy describing collected data; a private bot that keeps no message data beyond paraphrased notes should say so to admins anyway (the invite message in kb/discord.md does).
- Secondary sources (2026) report the privileged-intent review moved from a server count to a user-reach threshold in June 2026 with yearly reapplication. The gateway docs read today give 10,000 unique users; no primary announcement was found.
- Whether bots must connect to the gateway once before REST calls work: an old requirement for sending messages; reading via REST is not affected in the docs read. The bot never sends.

## Not taken

- **Self-bots or user tokens:** banned by the Terms of Service.
- **Scraping actors and automation platforms** (Apify, n8n, Zapier): cost money or a third party, and scraping is against rule 20.
- **Off-the-shelf Discord MCP servers:** would work with the same token, but add a dependency and a running server for what a few REST calls do; many expose send-message tools that the decision rules out.
- **A bot that forwards messages to an AI API:** Mark ruled it out; the agent calls the bot.
