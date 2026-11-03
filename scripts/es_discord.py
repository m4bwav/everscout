#!/usr/bin/env python3
"""es_discord: read Discord servers that invited your bot, through Discord's REST API.

The agent drives the bot; the bot never drives the agent. Nothing runs in the
background and nothing is hosted: each command is one or a few REST calls made
with the bot token, then the process exits. Setup and the rules are in
kb/discord.md (Developer Portal steps, the invite, the Message Content intent).

  python es_discord.py check                      token, bot identity, intent flag
  python es_discord.py invite [--guild ID]        the read-only invite link for a server admin
  python es_discord.py guilds                     servers the bot is in
  python es_discord.py channels GUILD             text, announcement and forum channels it can see
  python es_discord.py threads GUILD [--archived CHANNEL]
  python es_discord.py read CHANNEL [--guild ID] [--days 3 | --after ID | --before ID] [--max 300] [--json]
  python es_discord.py search GUILD QUERY [--json]
  python es_discord.py row GUILD CHANNEL          a watch-list row for beat sources.md
  python es_discord.py leave GUILD --yes          remove the bot from a server

Read-only by design: no command posts, reacts, joins, DMs or changes anything
except `leave` (ai-docs/decisions/2026-11-02-discord-bot-read-only.md). The token
comes from DISCORD_BOT_TOKEN (or the Windows user environment) and is never printed.
Standard library only, Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import es_sources as S  # noqa: E402

API = S.DISCORD_API
HOST = "discord.com"
UA = "DiscordBot (https://github.com/m4bwav/everscout, 1)"  # the format Discord requires
# VIEW_CHANNEL (1 << 10) + READ_MESSAGE_HISTORY (1 << 16): all a reader needs
READ_PERMISSIONS = (1 << 10) | (1 << 16)
# application flags: the Message Content intent is on (verified apps) or on with the limit (unverified)
FLAG_MESSAGE_CONTENT = 1 << 18
FLAG_MESSAGE_CONTENT_LIMITED = 1 << 19
READABLE_TYPES = {0: "text", 5: "announcement", 15: "forum", 16: "media", 11: "public thread", 10: "announcement thread"}


class DiscordError(Exception):
    def __init__(self, code, msg):
        super().__init__(f"{code} {msg}")
        self.code = code


def token():
    t = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    if not t and sys.platform.startswith("win"):
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                t = str(winreg.QueryValueEx(k, "DISCORD_BOT_TOKEN")[0]).strip()
        except OSError:
            t = ""
    return t


def host_headers():
    """{host: headers} for es_sources.Fetcher; empty when no token is set."""
    t = token()
    return {HOST: {"Authorization": f"Bot {t}", "User-Agent": UA}} if t else {}


def call(path, query=None, method="GET", opener=urllib.request.urlopen, sleep=time.sleep):
    """One REST call. Waits out one 429 (retry_after), then stops; 401 and 403 stop at once
    (they count toward Discord's invalid-request ban)."""
    t = token()
    if not t:
        raise DiscordError("no-token", "set DISCORD_BOT_TOKEN (kb/discord.md, step 3)")
    url = API + path + ("?" + urllib.parse.urlencode(query) if query else "")
    for attempt in (1, 2):
        req = urllib.request.Request(url, method=method, headers={"Authorization": f"Bot {t}", "User-Agent": UA,
                                                                 "Accept": "application/json"})
        try:
            with opener(req, timeout=40) as r:
                body = r.read().decode("utf-8", "replace")
                left = r.headers.get("X-RateLimit-Remaining")
                if left == "0":
                    sleep(float(r.headers.get("X-RateLimit-Reset-After") or 1))
                sleep(S.DEFAULT_HOST_GAPS["discord.com"])
                return json.loads(body) if body.strip() else None
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace") if hasattr(e, "read") else ""
            try:
                info = json.loads(text)
            except ValueError:
                info = {}
            if e.code == 429 and attempt == 1:
                sleep(float(info.get("retry_after") or 5) + 0.5)
                continue
            raise DiscordError(e.code, info.get("message") or str(e.reason)) from None
        except urllib.error.URLError as e:
            raise DiscordError("network", str(e.reason)) from None
    raise DiscordError(429, "rate limited twice; stopped")


def invite_url(app_id, guild=None):
    q = {"client_id": app_id, "scope": "bot", "permissions": str(READ_PERMISSIONS)}
    if guild:
        q.update(guild_id=str(guild), disable_guild_select="true")
    return "https://discord.com/oauth2/authorize?" + urllib.parse.urlencode(q)


def intent_state(flags):
    if flags & FLAG_MESSAGE_CONTENT:
        return "on"
    if flags & FLAG_MESSAGE_CONTENT_LIMITED:
        return "on (unverified app)"
    return "OFF: message text will come back empty (Developer Portal > Bot > Message Content Intent)"


def read_channel(channel, after=None, before=None, most=300, **kw):
    """Up to `most` messages, oldest first. With `after`, pages forward; otherwise pages back from `before` (or now)."""
    got = []
    while len(got) < most:
        q = {"limit": str(min(100, most - len(got)))}
        if after:
            q["after"] = after
        elif before:
            q["before"] = before
        page = call(f"/channels/{channel}/messages", q, **kw) or []
        if not page:
            break
        got += page
        ids = sorted(int(m["id"]) for m in page)
        if after:
            after = str(ids[-1])
        else:
            before = str(ids[0])
        if len(page) < int(q["limit"]):
            break
    return sorted(got, key=lambda m: int(m["id"]))


def show_items(items, as_json):
    if as_json:
        print(json.dumps(items, ensure_ascii=False, indent=1))
        return
    for it in items:
        print(f"{it['published'][:16]}  {it['url']}")
        print("  " + it["text"].replace("\n", "\n  ")[:1500])


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    p = argparse.ArgumentParser(prog="es_discord", description="Read Discord servers that invited your bot (read-only).")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    s = sub.add_parser("invite"); s.add_argument("--guild")
    sub.add_parser("guilds")
    s = sub.add_parser("channels"); s.add_argument("guild")
    s = sub.add_parser("threads"); s.add_argument("guild"); s.add_argument("--archived", metavar="CHANNEL")
    s = sub.add_parser("read"); s.add_argument("channel"); s.add_argument("--guild", default="")
    s.add_argument("--days", type=float, default=3); s.add_argument("--after"); s.add_argument("--before")
    s.add_argument("--max", type=int, default=300); s.add_argument("--json", action="store_true")
    s = sub.add_parser("search"); s.add_argument("guild"); s.add_argument("query"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("row"); s.add_argument("guild"); s.add_argument("channel")
    s = sub.add_parser("leave"); s.add_argument("guild"); s.add_argument("--yes", action="store_true")
    a = p.parse_args(argv)
    try:
        return run(a)
    except DiscordError as e:
        hint = {401: "the token is wrong or was reset: copy a new one (kb/discord.md, step 3)",
                403: "the bot lacks View Channel or Read Message History there, or is not in that server",
                404: "no such server or channel, or the bot cannot see it"}.get(e.code, "")
        print(f"error: {e}" + (f" ({hint})" if hint else ""), file=sys.stderr)
        return 2


def run(a):
    if a.cmd == "check":
        me = call("/users/@me")
        app = call("/applications/@me")
        print(f"bot      {me.get('username')} (id {me.get('id')})")
        print(f"public   {'yes: anyone can add it; turn Public Bot off' if app.get('bot_public') else 'no'}")
        print(f"intent   message content {intent_state(int(app.get('flags') or 0))}")
        # approximate_guild_count is cached by Discord and lagged at 0 with the bot in a server
        print(f"servers  {len(call('/users/@me/guilds') or [])}")
        return 0
    if a.cmd == "invite":
        app = call("/applications/@me")
        print(invite_url(app["id"], a.guild))
        print("Send this to a server admin with the reason (kb/discord.md, step 4). Only someone with Manage Server can add the bot.")
        return 0
    if a.cmd == "guilds":
        for g in call("/users/@me/guilds") or []:
            print(f"{g['id']}  {g.get('name', '')}")
        return 0
    if a.cmd == "channels":
        for c in sorted(call(f"/guilds/{a.guild}/channels") or [], key=lambda c: (c.get("parent_id") or "", c.get("position", 0))):
            kind = READABLE_TYPES.get(c.get("type"))
            if kind:
                print(f"{c['id']}  {kind:<12} #{c.get('name', '')}")
        return 0
    if a.cmd == "threads":
        data = call(f"/channels/{a.archived}/threads/archived/public") if a.archived else call(f"/guilds/{a.guild}/threads/active")
        for t in (data or {}).get("threads", []):
            print(f"{t['id']}  in {t.get('parent_id')}  {t.get('message_count', '?')} msgs  {t.get('name', '')}")
        return 0
    if a.cmd == "read":
        after = a.after or (None if a.before else S.discord_snowflake(time.time() - a.days * 86400))
        msgs = read_channel(a.channel, after=after, before=a.before, most=a.max)
        items = S.parse_discord_messages(msgs, guild_id=a.guild)
        if S.discord_text_missing(msgs):
            print("note: messages came back with no text; is the Message Content intent on? (es_discord.py check)", file=sys.stderr)
        show_items(items, a.json)
        return 0
    if a.cmd == "search":
        data = call(f"/guilds/{a.guild}/messages/search", {"content": a.query})
        msgs = [m for group in (data or {}).get("messages", []) for m in (group if isinstance(group, list) else [group])]
        show_items(S.parse_discord_messages(msgs, guild_id=a.guild), a.json)
        return 0
    if a.cmd == "row":
        names = {c["id"]: c.get("name", "") for c in call(f"/guilds/{a.guild}/channels") or []}
        # engage stays "no": the bot never posts, and the conduct code keeps drafted replies off Discord
        print(f"| {a.guild}/{a.channel} | discord | core | native | no | yes | | ✓ {time.strftime('%Y-%m-%d')} "
              f"#{names.get(a.channel, '?')}; bot invited by the server admin |")
        return 0
    if a.cmd == "leave":
        if not a.yes:
            print("leave removes the bot from that server; run again with --yes", file=sys.stderr)
            return 1
        call(f"/users/@me/guilds/{a.guild}", method="DELETE")
        print(f"left {a.guild}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
