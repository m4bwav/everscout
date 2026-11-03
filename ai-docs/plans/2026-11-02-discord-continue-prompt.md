# Continue: Discord through the invited bot

Start in `D:/m4bwa/Claude/Projects/Ai/everscout`.

1. Load state: `ai-docs/HANDOFF.md` (section "0.10.0"), `kb/discord.md`, `ai-docs/research/2026-11-02-discord-bot-access.md`, `ai-docs/decisions/2026-11-02-discord-bot-read-only.md`.
2. Waits on Mark: the Discord application, bot and `DISCORD_BOT_TOKEN` (kb/discord.md steps 1-3). Never ask for the token, never print it, never run the browser login for him. If `python scripts/es_discord.py check` says no token, stop here and tell him the three steps.
3. With a token: run `check` (intent must be on, Public Bot off), `invite`, then once he has added the bot to his own server, `guilds`, `channels`, `read <channel> --guild <id> --days 1`, and `search <guild> <word>`. Record each result (works or the exact error, no message text) in the research note's "Unverified" section, then fix es_discord.py with a test for anything that broke.
4. Then, if Mark wants it: draft the admin message for one server a beat needs, for him to send; add rows with `es_discord.py row` only after the admin adds the bot.
5. Stop points: any write action (post, react, DM) needs a new decision record first; any 401 or 403 stops the run.
6. Hand-over: patch release if code changed (tag and GitHub release; no registry publishing), `claude plugin update everscout@everscout`, update HANDOFF.md, and print the same start command: `Execute D:/m4bwa/Claude/Projects/Ai/everscout/ai-docs/plans/2026-11-02-discord-continue-prompt.md`.
