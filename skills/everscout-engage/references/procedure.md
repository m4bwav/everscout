# everscout-engage procedure

Detail for [SKILL.md](../SKILL.md). `ES` = `python "<plugin root>/scripts/everscout.py"`; `LOCAL` = the local folder `ES where` prints.

## A. Why this skill exists and where its lines come from

People who post their work usually like being asked how they made it; a good question, asked by a real person at a human pace, brings back knowledge no feed carries. The same act done carelessly is spam, and done covertly it is the 2025 Zurich r/changemyview scandal: AI comments, invented personas, profiling, no disclosure, even with every comment reviewed by hand. The conduct code (`kb/conduct.md`) draws the lines; this procedure applies them. Research: `ai-docs/research/2026-09-26-engagement-ethics.md` in the repository.

## B. The candidate checks, in order

1. Pace: `ES engage-check --platform <p>` (no other arguments) before looking at all; exit 2 ends the task.
2. Fresh enough and not too fresh: `candidates` keeps items between `min_item_age_hours` (1) and `max_item_age_days` (3).
3. Community allows it: the source row's `engage` is `yes`; its `stance` and notes say whether AI-written comments are banned (then ideas only) or disclosure is required (then the draft discloses: "(drafted with help, edited by me)" in the user's words).
4. The poster is the maker: first person ("I made", "my new EP", "our paper"), or the thread says so.
5. Nobody asked yet: `process asked: False` and your own read agrees; a question already asked and answered is read, not repeated. Ask something adjacent that is still open, or skip.
6. There is something true and specific to observe: a detail in the work, not a guess about it.
7. Not a support, grief, crisis, political or argument thread.
8. The author's profile is not marked `#nobot` (Mastodon, Bluesky), and the user has not engaged this author before (`engage-check --author`).
9. `ES engage-check --platform <p> --community <c> --author <a> --item <id>` exit 0.

## C. Writing the draft

- Read the voice file first. It says what is true about the user and how they sound. No sentence may imply anything the file does not support.
- Observation: one line. Specific and true ("the grain on the night shots", "the chart's log scale made the 2022 jump readable", "that sidechained pad in the second half"). When the voice file says the user opens with a few words of slang, do that and move the specific observation into the first question.
- Questions: one to three, from at least two categories of the beat's question bank, rephrased for this post, one idea each, answerable in a sentence or two. Prefer questions whose answers teach something the beat's research questions care about.
- Never: "is this AI", "what did you prompt" (unless the maker already said it was generated), a link, the user's own project, "DM me", flattery with no content, a numbered survey, em dashes if the voice file bans them.
- Check against the ledger: `ES ledger --days 60 --text`. If the opening words or the question shapes match any of the last ten, rewrite.
- Length: the voice file's range, else 25 to 90 words.

## D. Hand over and record

- One message to paste: the link on the first line, a blank line, then the text, and nothing else in that message.
- `ES engage-record ... --route manual --status handed --text-file LOCAL/drafts/<item>.md`. The record is the pace: a handed text counts exactly like a posted one, because the user usually posts it within minutes.
- The user may say "hold it": record with `--status drafted` (does not count for pacing), and hand it over later with `ES engage-update --item <id> --status handed`.
- When the user says it is up, `ES engage-update --item <id> --status posted` (with `--comment-url` if they share the permalink).

## E. Posting through an API (not built in)

Everscout 0.1 never posts. Some platforms allow a personal account to post through an API (Mastodon with a personal token, Bluesky with an app password, Lemmy, Discourse with a user API key). A user who wires that up themselves still follows this procedure to the approval, runs the posting command themselves, and records `--route api`. The Reddit and Hacker News rules make a hand paste the only sound route there.

## F. Thank-yous and answers

- Thank-you: two lines. Thanks, then the one specific thing the answer taught ("the tip about locking the seed per shot saved me an evening"). No new questions unless the user wants a follow-up; a follow-up is a new ask with its own pace check.
- Answers to others: only what the user knows first-hand or can cite; a source link when citing (a link to a primary source is fine in an answer, unlike in an ask). If the user does not know, the draft is not written.

## G. Overrides

When the user overrides a pace rule ("post it anyway"), pass `--override`; the ledger marks it. Say once which rule it breaks and why the rule exists. Conduct rules 4 (no personas), 6 (no profiling), 16 (no keeping deleted content) and 17 (honest access) are not overridden by this skill.
