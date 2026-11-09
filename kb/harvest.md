# Technique harvest: from a beat's best posts to changes in your own tools

A scan keeps you informed. A harvest goes one step further: it takes the month's most useful technique, tutorial and
tool posts in a beat, tests the promising ones, and folds the winners into the tools, skills or plugins the person
maintains. It runs on demand ("harvest the month", "what techniques should my plugins pick up") or once a month
after a scan. It was first run on an AI game-art beat: one Reddit post's GIF kit became a new animation command in a
pixel-art plugin, after the kit was reproduced and the new command measured at parity with it.

## 1. Window and feeds

- The window is the last 30 days, or the dates the harvest's HANDOFF names. One shortlist per window; a rerun in
  the same window reuses it.
- Feeds: each core community's top-of-month listing. Reddit through the beat's reader (Arctic Shift carries points
  and comment counts, so rank by them; the top-of-month RSS feed `r/<sub>/top/.rss?t=month&limit=100` gives the
  order without scores while it lasts), Hacker News and Lemmy by points, forums by replies. Pace as
  `kb/platforms.md` says. Save the raw listings beside the harvest so a rerun needs no new fetch.
- Read a thread's comments too: they often hold the best lead (an alternative tool, the author's own correction).
  When a method is shown only on video, take frames with ffmpeg and read them as a contact sheet.

## 2. Shortlist (top 20)

Keep posts that teach a method or link a repo, workflow, node, model or tool. Drop showcases, questions, news, drama
and paid product pitches. Score each:

| score | meaning |
|---|---|
| 3 | a reproducible method with code, a workflow file, a repo or measured numbers, in an area one of the tools covers |
| 2 | a clear method without code, or a new model or component a tool should know about |
| 1 | a tip or a comparison without a method |
| 0 | showcase, question, news, drama, pitch |

Keep 2 and 3 only. Several posts on one technique count once; keep the best. Break ties toward the tool with the
most use. Write `candidates.md`: link, score, the tools it could improve, one line on why. Before mapping, read each
tool's AGENTS.md and skill files; a gap is judged against what the tool does, not against its name.

## 3. Evaluate, one candidate per subagent

Several at once. Give each the post link and the saved listing, the tools named for it with their paths, this file
and the stop rules. Each one:

1. Reads the post, its comments and every linked source. Clones repos into an empty scratch folder of their own and
   reads code before running any (downloaded code runs only with the person's go-ahead per kit).
2. States the technique's claims and what each rests on.
3. Finds what the named tools already do for the same job.
4. Tests if cheap: reproduce the post's own example, then run the tool's current route on the same input and compare
   with numbers (sizes, colours, timings, a gate, a score) and a side-by-side picture when the output is visual.
5. Writes `posts/<id>.md`: link, claims, commands and numbers, verdict, proposed change (file and section), the
   licence of anything to be copied, and an optional friendly draft comment for the author (never posted; the
   conduct code binds it, and posting is the person's call, as with everscout-engage).
6. Returns at most 10 lines. The session keeps only these reports.

Verdicts: **adopt** (a measured improvement; build it), **adopt-partly** (one part wins: a prompt rule, a
parameter), **note** (worth knowing, no change now; record it in the tool's research file or backlog), **skip** (no
gain or not reproducible; say why with the numbers).

## 4. Build and ship

For each adopt, change the tool in its own repository on a branch, by that repository's rules, tests and changelog.
Re-implement in the tool's own style and dependencies rather than vendoring a kit, and credit the source (MIT,
Apache and similar can be adapted with credit; anything else only as an idea). Measure against the tool's current
behaviour, never on the post's say-so; a change that loses its comparison is logged as a skip. Ship by the person's
standing release rules.

## 5. Stop points and record

Stop and ask before: publishing to a package registry, changing someone else's repository, posting, commenting or
voting anywhere, paying for an API, running downloaded code without a grant, and a large download. Carry on with
other candidates while a question waits. Keep a harvest folder with `HANDOFF.md` (window, next step, candidates
left, grants, open questions), `log.md`, `candidates.md`, `posts/` and the saved listings, so any session can resume
from disk. Note each adopted post in the beat as a `web` or thread note with what it became.
