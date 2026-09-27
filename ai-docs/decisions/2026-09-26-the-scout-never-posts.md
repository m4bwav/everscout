---
title: Everscout drafts; the person posts by hand
kind: decision
status: active
date: 2026-09-26
verified: 2026-09-26
tags: [engagement, conduct, reddit, posting, safety]
summary: read before adding any posting, browser automation or API write path to everscout
---

# Decision: the scout never posts

## Context

indie-ai-scout has a browser route that can post a comment through Mark's signed-in Chrome after he approves the text. On 2026-09-19 Mark chose not to use it: the tool drafts, he pastes. The 2026-09-26 research (`../research/2026-09-26-engagement-ethics.md`) found that Reddit defines an app as an account "operating through software or scripts, rather than direct control by a human" and requires a label; asks for human verification on rapid posting; Hacker News bans generated and AI-edited comments; the Zurich r/changemyview study reviewed every comment by hand and was still condemned. A public tool that posts would be used by others in ways its conduct code cannot enforce.

## Decision

Everscout 0.1 has no write path. The engage skill drafts, the person approves the exact text, the skill hands it over as one message to paste, and the ledger records it as `handed` (which counts for pacing exactly like `posted`). No browser automation, no API posting, no scheduling. A person who wires up a platform's personal API (Mastodon token, Bluesky app password) does so outside everscout and records `--route api`.

## Reasons

Reddit's account-control line, platform bans on AI-written comments, the Zurich lesson that review is not enough without the rest of the code, and Mark's own choice. Handing over costs the person seconds per comment at four a day.

## Rejected alternatives

- **Port indie-ai-scout's browser route** into the public engine: it needs a signed-in profile, headed Chrome and block-page handling, and it moves the account toward Reddit's "app" definition.
- **API posting for Mastodon and Bluesky**: technically allowed with a bot label, but a person's own account posting drafted replies through a script reads as automation to the community, and the label would misdescribe a human-reviewed comment.

## Consequences

- indie-ai-scout keeps its browser route privately if Mark ever wants it; it does not come across in the migration.
- Revisiting this needs a new decision record, the conduct code applied to the new path, and tests.
