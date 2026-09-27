# Research: everscout-ask

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin.

Topic: answering questions from a personal monitoring knowledge base with retrieval grading, web fallback and faithful citation. Tier `medium`. Last refresh 2026-09-26; next due 2026-10-26.

## Current understanding

- **Grade the retrieval before answering (R-20260926-1).** Corrective Retrieval Augmented Generation (Yan et al., arXiv 2401.15884) scores the retrieved documents and takes one of three actions: correct (use them, refined), incorrect (discard and search the web), ambiguous (both). SKILL.md step 3 is that grading done by the agent: enough, partial, none. https://arxiv.org/abs/2401.15884 (read 2026-09-26)
- **Abstain and say so when the evidence is thin (R-20260926-2).** Grounded QA evaluation treats "cannot be answered from the provided material" as a correct outcome and scores citation accuracy and faithfulness separately (GroUSE, arXiv 2409.06595; 2026 RAG evaluation work). Hence "what the scout does not know" is a required part of every answer. https://arxiv.org/pdf/2409.06595 (read 2026-09-26)
- **AI answers mis-cite often** (Tow Center 2025, EBU/BBC 2025; see everscout-report's RESEARCH.md), so every external link must be held by a note or the source log, checked by `everscout.py lint`, which now covers `answers/`.
- **Saved answers compound.** Answers are recalled like notes, so a question asked twice starts from the first answer and only needs the news since.

## Open questions

- Keyword and alias recall misses paraphrases; an embedding index would help on a beat with thousands of notes. Not needed below a few hundred notes; revisit when a beat grows.
- Should an answer older than the half-life be marked stale automatically in recall output?

## Search plan

Five tracks; every refresh runs at least one query on each, scoped to the period since the last refresh, with the year.

Subject:

- `corrective RAG OR self-RAG retrieval evaluation web fallback <year>`
- `grounded question answering abstention citation accuracy benchmark <year>`
- `AI assistant news answers citation accuracy study <year>`

Tooling (skills, plugins, MCP servers for this job):

- `path:SKILL.md "knowledge base" "ask" notes` on GitHub code search, recently updated; skills.sh search for research assistant, second brain, ask my notes
- `https://registry.modelcontextprotocol.io/v0/servers?search=notes` and `?search=obsidian`
- Supersession sweep: `"<tool>" deprecated OR archived <year>` for every tool named above

Most discussed:

- `hn.algolia.com/api/v1/search_by_date?query=ask%20your%20notes` and `?query=personal%20knowledge%20base%20RAG`

Practice:

- `beat reporter sourcing verification practice <year>`; `personal knowledge base question answering agent notes <year>`

Testing:

- `RAG evaluation faithfulness abstention harness <year>`; the evergreen plugin's protocol/TESTING.md

Best sources: arXiv papers with code, the Tow Center and EBU studies on AI answers, the evergreen protocol. Noisy: vendor "RAG best practices" posts.

## Findings log

### R-20260926-1 · 2026-09-26 · CRAG's three actions fit a beat's knowledge base
- source: https://arxiv.org/abs/2401.15884
- magnitude: new
- led to: C-20260926-1

### R-20260926-2 · 2026-09-26 · Abstention is a correct answer in grounded QA evaluation
- source: https://arxiv.org/pdf/2409.06595
- magnitude: new
- led to: C-20260926-1
