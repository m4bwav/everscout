# everscout

Name a subject and get a scout for it. Everscout keeps up with any subject by reading the communities where people make and discuss it, and asks the makers themselves when they're happy to talk.

Say "set up a scout for vintage synth restoration" (or container gardening, or Formula 1 aerodynamics). The everscout-beat skill asks you up to three questions: what's in scope, what you want to learn, and whether you want to talk to makers. Then it researches where that subject lives online, fetches every candidate community and feed to check it's real and active, and writes the scout, called a **beat**. You can have as many beats as you like.

A beat covers one subject: AI video, global economics, down-tempo music, whatever you follow. Everscout reads that beat's subreddits, forums, Hacker News, Bluesky, Mastodon, Lemmy, newsletters, YouTube channels, GitHub releases, arXiv and Hugging Face at each platform's polite pace. It writes one short paraphrased note per thread worth keeping and counts the tools, models, artists or indicators those notes name. From that it writes a monthly radar of what is new, rising and fading, and a sourced history-and-guide for the subject. When a maker posts their work, it drafts a question in your voice. You approve it and paste it yourself.

It is a Claude Code plugin: four skills, a standard-library Python CLI and a markdown knowledge base. The skills are evergreen units, so their research refreshes on a schedule instead of going stale.

## The four skills

| skill | does | say |
|---|---|---|
| everscout-beat | defines a subject: scope, research questions, a verified watch list, an entity vocabulary with aliases, a question bank, web searches, a study outline | "set up a scout for AI video", "add r/X to my beat", "check my sources" |
| everscout-scan | fetches, triages, writes notes, collects replies from makers you asked, retallies the signals | "scan", "catch me up on economics", "any replies?" |
| everscout-engage | finds a fresh post where nobody has asked about the process, drafts a question, checks the pace and the community's rules, hands the text to you to paste, records it | "find a post to ask", "thank them for the answer" |
| everscout-report | radar report, weekly digest, or the baseline study, every claim linked to a note and every link checked | "write the radar", "what's rising", "build the study" |

## Starter beats

The starter beats are examples of what a generated beat looks like, and a quick start if one happens to be your subject. `beats/ai-video` (a maker community, open about AI), `beats/global-economics` (analysts and data, strict forums) and `beats/downtempo` (musicians, hostile to AI music) were picked because they differ, and their sources were checked on the day they were added. `beats/_template` is what `beat-new` copies. Copy a starter beat into your private beats folder to make it yours; a private beat shadows a built-in one with the same name.

## Where your data lives

Nothing personal goes in this repository. `python scripts/everscout.py where` prints the paths.

- `~/.everscout/config.json`: your contact for the User-Agent, your Reddit name, paths, pace overrides. Start from `everscout.config.example.json`.
- `~/.everscout/voice.md`: how you write and what is true about you, so drafts sound like you and never invent a persona. Start from `kb/voice-template.md`.
- `~/.everscout/beats/`: your private beats.
- Data folder per beat (`data_root/<slug>` or a path per beat): notes, reports, study, signals, your journal and feedback. It works fine inside an Obsidian vault or a private git repo.
- One engagement ledger for all beats, because pacing belongs to your account and not to a subject.
- A local cache, purged after 48 hours.

## How it reads

Feeds and documented public endpoints only, no keys needed:

| kind | example `source` |
|---|---|
| reddit | `r/aivideo` (logged-out Atom feeds, about one request a minute) |
| hn | `"video generation"` (Algolia search) |
| bluesky | `@someone.bsky.social` or a feed generator `at://.../app.bsky.feed.generator/...` |
| mastodon | `#ambient@mastodon.social` or `@user@instance` |
| lemmy | `c/technology@lemmy.world` |
| discourse | `https://forum.example.org` |
| rss | any feed URL: Substack, Medium, WordPress, podcasts, arXiv category RSS |
| youtube | a channel id `UC...` |
| github | `owner/repo` (releases) |
| arxiv | an API query |
| huggingface | `models?pipeline_tag=text-to-video` |
| news | a Google News search |

Every request names everscout and your contact. Threads (post plus comments) can be read from Reddit, HN, Bluesky, Mastodon, Lemmy and Discourse. X, Threads, Instagram, TikTok, Discord and Telegram aren't read at all, and neither is anything a platform forbids scraping (Bandcamp, for one). `kb/platforms.md` has what each platform allows as of 2026-09-26.

## How it engages

Everscout never posts. It drafts, you edit and approve the exact text, and you paste it. The ledger records every draft so the pace holds: an hour between comments, four a day per platform, one per community a day, never the same person twice. The full conduct code is `kb/conduct.md`. Its main lines:

- You're the author. No personas, no claims about you that your voice file doesn't support.
- Ask how something was made. Never ask "is this AI?"
- Where a community bans AI-written comments (Hacker News does), you get ideas, not a draft.
- Read the work, not the person. No profiling, no DMs, no links, no self-promotion.
- Thank people who answer.

The rules come from research into platform policies, the 2025 r/changemyview AI experiment, internet research ethics and studies of what gets answers. The research notes are in `ai-docs/research/`.

## The CLI

`python scripts/everscout.py <command>`. Python 3.9 or later, standard library only.

| command | does |
|---|---|
| `where [--beat]` | resolved paths |
| `beats`, `beat-new <slug> --title`, `beat-check <slug>` | list, scaffold, validate beats |
| `sources --beat`, `probe --beat [--save]` | list sources; fetch each once and report which fail |
| `fetch --beat [--kinds] [--sources] [--listing new,top] [--max-age-days N] [--json]` | fetch a beat's sources (paced, cached) and list new items |
| `thread <url>` | a thread with comments |
| `search --kind reddit\|hn\|news\|arxiv --q ...` | search one platform |
| `new-note <url> --beat --note-kind` | scaffold a note, prefilled with the vocabulary it finds |
| `vocab-match --beat --text` | canonical entities named in a text |
| `validate`, `tally`, `index`, `lint` (each `--beat`) | check notes; recount signals; rebuild indexes; check report and study links |
| `source-log <url> --beat` | record a web page actually read, so reports may cite it |
| `candidates --beat`, `questions --beat` | rank posts for a question; sample question seeds |
| `engage-check`, `engage-record`, `engage-update`, `ledger`, `followups` | pace rules, the ledger, replies from the people asked |
| `retention`, `state --beat` | purge the cache; fetch state |

## Method

Everscout follows netnography (Kozinets 2020) for the stages and horizon scanning for the trend layer. A signal is one dated observation, and a trend needs three independent signals across two reports. Signals are scored on novelty, velocity, breadth, evidence and relevance. Reports use the ThoughtWorks radar rings: Adopt, Trial, Assess, Hold. Counting follows the LLM-wiki pattern: one note per thread, entities resolved through aliases in code, weight by comment count with time decay. URLs in reports have to come from notes or from pages logged as read; `lint` catches the rest. `kb/method.md` explains each step.

## Install

```
claude plugin marketplace add https://github.com/m4bwav/everscout
claude plugin install everscout@everscout --scope user
```

Then run `python <plugin dir>/scripts/everscout.py where`, write `~/.everscout/config.json` with at least `contact`, and say "set up a scout for <subject>" or "scan the ai-video beat". Other agents (Copilot, Codex, Cursor) can use the four skill folders directly; AGENTS.md has the rules for working in the repository.

## Tests

`python -m unittest discover -s tests` runs offline against synthetic fixtures and also checks every built-in beat. Skill evals live in each skill's `evals/evals.json` and run through the evergreen plugin's `evergreen-test`.

## Prior art

last30days-skill (engagement-ranked briefs across many sources) is the closest cousin; everscout differs in keeping memory across runs, tallying a fixed vocabulary, and engaging under a conduct code. F5Bot and Syften showed that boolean keyword filters are enough for alerts. GummySearch showed what happens to a tool built on Reddit's paid API. `ai-docs/research/2026-09-26-prior-art.md` has the full survey.

## License

MIT.
