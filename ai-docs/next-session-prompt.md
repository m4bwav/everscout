# Next session: wire everscout to fetchwright and try it live now

Written 2026-10-15 (night). Run from `D:\m4bwa\Claude\Projects\Ai`. The everscout repository is `Ai\everscout` (public, m4bwav/everscout). Its main clone holds another session's uncommitted edits, so work in a worktree off origin/main (`Ai\everscout-wt-urlctx` exists, parked on origin/main).

Mark's ask (2026-10-15): "integrate it with everscout now. I don't want to wait on Arctic Shift, I want to see if it works now." So build the wiring and run it live on real beats this session. Do not wait for the feeds or Arctic Shift to end.

## Where things stand

- fetchwright 0.1.0 is released (github.com/m4bwav/fetchwright, tag v0.1.0; clone `Ai\fetchwright`; installed as fetchwright@mark-local).
- Its CLI is `skills/fetchwright/scripts/fetchwright.py`: `read URL --thread --json --max-chars 0`. It returns `{read_ok, why_not, title, body, body_removed, comments: [{text, author_is_op}], dropped, retrieval, usage, model, models_tried, style}`, with no usernames. Exit codes: 0 read, 1 not read, 2 usage, 3 rate limited (stop), 4 key problem, 5 every model down.
- `GEMINI_API_KEY` is set at user level and works. On 2026-10-15 `gemini-3.8-flash` 503'd on URL context and `gemini-3.5-flash-lite` read every thread.
- everscout 0.4.0 reads Reddit listings through the feeds (`rss`, until 2026-11-13) or Arctic Shift. Thread reading is `load_thread` in `scripts/everscout.py`; the reader choice is `reddit_reader(cfg)` and `--reddit-reader`. Conduct rule 17 and the `kb/platforms.md` keyed-sources row already allow this route (PR #18).

## Read first

1. `AGENTS.md` (repository rules: synthetic fixtures, the cache, pace, changelogs, versioning).
2. `scripts/everscout.py`: `reddit_reader`, `set_reddit_reader`, `load_thread`, and the `thread` and `scan` commands.
3. `kb/conduct.md` rules 16 and 17, and `kb/platforms.md` keyed sources.
4. `fetchwright/skills/fetchwright/SKILL.md` and `references/route.md`, for what the reader returns and what it does not cover.

## The work

1. **Decision record first** (`ai-docs/decisions/`). It says:
   - Reddit thread reading can go through fetchwright as a subprocess, opt-in.
   - Listings stay on rss or arcticshift.
   - everscout stays keyless by default and never imports fetchwright code.
   - Rejected options, with reasons.
2. **Config and flag:**
   - New config `reddit.thread_reader`: `same` (default, follows `reddit.reader`) or `fetchwright`.
   - New flag `--thread-reader` on `thread` and `scan`, choices `same` and `fetchwright`.
   - Finding the CLI: config `fetchwright.cli` (a path), then `FETCHWRIGHT_CLI`, then the installed plugin under `~/.claude/plugins/`. Not found: a clear message naming the plugin and the setup skill, never a crash.
3. **Adapter in `load_thread`:**
   - Run `[sys.executable, cli, "read", url, "--thread", "--json", "--max-chars", "0"]` with a timeout of about 400 s.
   - Map the JSON onto everscout's thread shape: post with `kind: post`, comments with `kind: comment`, no author handles, `via: fetchwright`.
   - Keep `retrieval`, `model` and `usage` on the thread for the notes' provenance line.
   - Cache the JSON like other thread reads (`thread_ttl_seconds`, purged at 48 h).
   - Exit 3: write a cool-down like the GDELT one (`~/.everscout/local/cooldown.json`), stop that scan's fetchwright reads, and say so.
   - Exit 4: one line pointing at the fetchwright-setup skill.
   - Exits 1 and 5: return None with a note.
   - Pace: a host gap for Gemini of at least 5 s.
4. **Tests** in `tests/test_everscout.py`:
   - A fake CLI script (synthetic JSON, invented text) that covers the mapping, every exit code, the cool-down, the config and flag precedence, and the not-found message.
   - No network and no key.
   - Run `python -m unittest discover -s tests`.
5. **Live, now.**
   - Fetch a real beat's listings with today's reader: `everscout.py fetch --beat ai-video --kinds reddit --peek --json` (feeds or Arctic Shift).
   - Pick 6 to 10 settled threads, a mix of sizes, a media post, and one with deleted comments.
   - Read each through `thread --thread-reader fetchwright --json` and through the current reader.
   - Record per thread: read or not, comments returned against the current reader's count, overlap, any handle or placeholder that got through, model used, page and output tokens, seconds.
   - Then run one real everscout-scan of a beat with `--thread-reader fetchwright` and distil notes from it as usual. Those go in Mark's data folder, never the repository.
6. **Write it down:**
   - Results in `ai-docs/research/` (no fetched text, no usernames, counts only).
   - `kb/platforms.md` row updated with the date.
   - Changelogs and the log.
   - Plan status: Stage 2 step 4 is discovery; note what fetchwright needs from it.
   - README Reddit paragraph: one opt-in line.
   - Version 0.5.0 in `.claude-plugin/plugin.json` and `VERSION` together. This is a CLI addition, so a minor version.
7. **Ship:**
   - One PR, merged once tests pass.
   - The tag and GitHub Release need Mark's go-ahead: ask in the final message, together with anything else that needs his hands.

## Limits

- Opt-in only. The default stays the same for every user, and nothing here may make a key required.
- Never Gemini's Google Search, and nothing that finds Reddit URLs through Gemini.
- Never retry a 429 within the hour.
- Pace: at most about 20 fetchwright reads in this session. The free-tier daily limit is unknown, and a forum claim says 500 a day for flash-lite.
- Notes follow rule 16: paraphrase, one short quote at most, no handles, drop what the author deleted.
- Never commit fetched text, real usernames or a recorded response. Test fixtures are invented.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Document as you go: the ai-docs log, plan status, HANDOFF, decision, research. Kill processes by PID only.
- No README or doc may call the route "legal". State what the terms say and what is untested.
- Merge your own PRs once tests pass. Tagging, releases and publishing need Mark's go-ahead. Batch what needs his hands into one message.

## When to stop and ask

- When the key stops working.
- If Gemini starts returning text from deleted or removed posts (decide with Mark how notes treat it).
- If fetchwright reads start failing with refusals or 429s (record and stop, conduct rule 17).
- If live results are much worse than Stage 1 (fewer than four of six threads readable): stop and report before shipping the wiring.
- Before any release.

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
