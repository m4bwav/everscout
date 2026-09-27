---
title: Questions to a beat are answered by a skill over keyword recall, graded, then researched
kind: decision
status: active
date: 2026-09-26
verified: 2026-09-26
tags: [ask, recall, rag, answers, knowledge-base]
summary: read before changing how everscout answers questions, adding embeddings or a search index, or changing the answers folder
---

# Decision: ask the beat through recall, grading and research

## Context

On 2026-09-26 Mark asked for the framework to "answer any questions using information in its knowledge base combined with whatever else it needs to get the best answer. Like a reporter, you can kind of interrogate them about their beat." Until then a beat's notes were only read by the report skill. Corrective Retrieval Augmented Generation (arXiv 2401.15884) grades retrieved documents and falls back to web search when they are poor; grounded QA evaluation counts "cannot be answered from this material" as a correct result (GroUSE, arXiv 2409.06595).

## Decision

A fifth skill, `everscout-ask`, plus a CLI command `recall`. Recall is word and vocabulary-alias matching over notes, saved answers, reports, study chapters and the journal, with a recency factor on the beat's half-life, and it prints the tally rows for the entities the question names. The agent grades the recall (enough, partial, none), researches only what the grade asks for (the beat's own items with `fetch --peek`, its communities through `search` and `thread`, its data pages, then the web), cites only notes and pages logged with `source-log`, and saves every answer to `DATA/answers/`, which recall searches next time. `lint` checks answers like reports.

## Reasons

Standard library only, like the rest of the CLI; a beat has tens to hundreds of notes, where word and alias matching with rewording is enough and explainable; the vocabulary already carries the aliases people use. Saving answers makes repeated questions cheap and makes the knowledge base grow from questions as well as scans. The split between "what the beat had seen" and "what is new" keeps the scout honest about its own coverage.

## Rejected alternatives

- Embeddings or a vector index: a dependency and a model download for a corpus that small; revisit when a beat passes a few hundred notes (open question in the skill's RESEARCH.md).
- Answering from the web alone: loses the beat's point of view and its history, and repeats work.
- Folding questions into everscout-report: reports are dated, periodic and structured; questions are ad hoc and conversational.
