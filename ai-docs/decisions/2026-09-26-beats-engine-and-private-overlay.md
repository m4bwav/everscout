---
title: Everscout is a public engine with beats; each person's voice, beats and data stay private
kind: decision
status: active
date: 2026-09-26
verified: 2026-09-26
tags: [architecture, beats, privacy, overlay, indie-ai-scout]
summary: read before changing where beats, config, voice, notes or the ledger live, or before moving indie-ai-scout onto everscout
---

# Decision: a public engine, private beats and data

## Context

indie-ai-scout (private, 2026-09-18) does one subject well: AI-assisted indie game development. Mark wants the same capability for any subject (AI video, global economics, down-tempo music), in a public repository, with indie-ai-scout later becoming a private, customised layer on top. The scout's data names people and quotes them, and Mark's voice and Reddit account are his, so none of that can be public. package-modernize solved the same split on 2026-09-25 with a public skill plus a private overlay read at run time.

## Decision

1. **A beat is a folder of markdown files** (`beat.md`, `sources.md`, `vocab.md`, `questions.md`, `searches.md`, `study.md`). Everything subject-specific in indie-ai-scout (the watch list, the question bank, the schema's spellings, the web searches, the study outline) became a beat file. The CLI and the skills know no subject.
2. **Built-in beats ship in the repository** (`beats/ai-video`, `beats/global-economics`, `beats/downtempo`, and `beats/_template`). They name only public communities and feeds.
3. **Private beats live in the folders listed in `beat_dirs`** of `~/.everscout/config.json` (default `~/.everscout/beats`). A private beat with the same slug as a built-in one shadows it, so a person can copy a built-in beat and tune it without forking the repository.
4. **Voice is a private file** (`voice` in config, default `~/.everscout/voice.md`; the public template is `kb/voice-template.md`). The engage skill reads it before every draft.
5. **Data folders are chosen per beat** (`beats.<slug>.data` in config, else `data_root/<slug>`), so a beat's notes can live in an everlast vault project, a private repository or a local folder. The engine never assumes everlast.
6. **One engagement ledger for all beats** (`ledger` in config, else `data_root/_engage`). Pacing is a property of the person's account on a platform, not of a subject: two beats must not each allow four Reddit comments a day.
7. **The cache and pacing state are machine-local** (`local_root`), shared across beats, so the per-host pace holds across beats too.

## Reasons

Privacy (people named in data; the user's voice and accounts), reuse (any subject without code changes), and a clean path for indie-ai-scout: its subject knowledge becomes a private beat, its voice becomes the voice file, its data folder stays in the vault, and its code is replaced by everscout's.

## Rejected alternatives

- **A plugin per subject** (fork indie-ai-scout for each): three copies of the CLI to maintain; fixes do not flow.
- **Beats as JSON or YAML**: harder for a person to edit and review; the markdown tables are parseable enough and render everywhere.
- **Per-beat ledgers**: breaks pacing across beats on one account.
- **Requiring everlast**: the public repository must work for people without it; everlast is one choice of data folder.

## Consequences

- `everscout.py where` is the first command on a new machine: it prints HOME, LOCAL, LEDGER, VOICE, the beat folders and a beat's DATA.
- indie-ai-scout migrates in stages; the plan names private paths, so it lives in indie-ai-scout's own doc set (`plans/2026-09-26-indie-ai-scout-on-everscout.md` there).
- Built-in beats are knowledge and are evergreen through the beat skill's refresh; a private beat is its owner's to keep current.
