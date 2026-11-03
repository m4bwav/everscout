---
title: Discord is read through the user's own invited bot, read-only, driven by the agent
kind: decision
status: active
date: 2026-11-02
verified: 2026-11-02
tags: [discord, bot, access, conduct, read-only]
summary: read before adding any Discord write action (post, react, DM, join) or another way into Discord
Related: builds on [2026-09-26-the-scout-never-posts.md](2026-09-26-the-scout-never-posts.md); see also [../research/2026-11-02-discord-bot-access.md](../research/2026-11-02-discord-bot-access.md)
---

# Decision: Discord through an invited bot, read-only

## Context

Until 0.9.6 everscout did not read Discord at all ("only servers your bot was invited to; self-bots banned"). On 2026-11-02 Mark asked for a way in: a free bot, as much bot code as possible in the plugin, current setup steps, and the bot able to do on Discord whatever is needed to obtain information legally. He ruled out the usual design where the bot forwards messages to an AI API; the agent calls the bot instead.

## Decision

- `scripts/es_discord.py`, standard library only, calls Discord's REST API v10 with the bot token. No gateway, no hosted process: REST reads are all a reader needs, and the Message Content intent applies to REST answers too.
- Commands cover what reading needs: check, invite link, list servers, channels and threads, read history, guild search, a watch-list row, and `leave`. Scans read `discord` rows through the same paced Fetcher; the token header goes to discord.com only.
- **No write actions.** No post, reaction, DM, edit, or join. Reading needs none of them, the scout-never-posts decision stands, and Developer Policy rules 5 and 13 (no unsolicited contact, no automated activity messages) make bot posts the riskiest part. Asking a community a question stays the person's own hand-written message.
- Authors are dropped from items (conduct: no handles; Developer Policy 16: no profiling). The invite asks for View Channels and Read Message History only.
- Self-bots and user tokens are refused outright (Terms of Service; Developer Policy 4).

## Consequences

- Each server must be asked. For communities Mark does not run, the setup guide (`kb/discord.md`) has the message to send the admins.
- Adding any write action later needs a new decision record, the conduct code applied, and a test change (a test fails if es_discord.py gains a POST or PATCH).
