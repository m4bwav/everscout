---
title: Reading Reddit through Gemini's Google Search grounding - checked against Google's terms (October 2026)
kind: research
status: active
date: 2026-10-15
verified: 2026-10-15
tags: [reddit, gemini, google-search-grounding, terms, licensing, free-tier, serpapi, perplexity]
---

# Reading Reddit through Gemini's Google Search grounding

Read this before building any route that sends Reddit content to Claude (or into everscout notes) through Gemini, Google AI Studio or another "licensed third party". Companion to `2026-10-11-reddit-after-the-api.md`.

## The idea that was checked

A Gemini chat told Mark on 2026-10-15 that the 2024 Google-Reddit deal (about $60M a year) makes it legal to use the free Gemini API to fetch Reddit content and hand it to Claude, and wrote a script naming `gemini-3.8-flash` and `claude-3-5-sonnet-latest`. Mark asked for a public evergreen plugin built on that route, then a Reddit lane in everscout on top of it.

## Findings

### 1. The deal licenses Google, not Gemini API customers

Announced February 2024. Google got Reddit's Data API ("real-time, structured content") and may "display, train on, and otherwise use" it in Google products; Reddit got Vertex AI. Reported value about $60M a year (Bloomberg, not confirmed by either company). Nothing in the public coverage passes rights through to people who call Google's APIs. What a Gemini API customer may do with search-backed answers is set by the Gemini API terms below, not by the deal.

### 2. The Gemini API terms forbid the pipeline

Gemini API Additional Terms of Service (effective 2026-03-23, page updated 2026-04-28), section on Grounding with Google Search. Answers that use the Google Search tool are "Grounded Results". The terms:

- Use only "in an application that is owned and operated by you", and show results only to "the end user who submitted the prompt".
- You may not let users or third parties "cache, frame, syndicate, resell, analyze, train on, or otherwise learn from Grounded Results or Search Suggestions".
- You may not "modify, or intersperse any other content with" Grounded Results or Search Suggestions without Google's written permission. Search Suggestions (up to five) or the Links must be shown with the result.
- Extracting the Links for other purposes, such as building an index or finding pages to crawl, is a violation.
- Storage: the text of a Grounded Result may be kept up to two years only to evaluate its display in your app, in the end user's own chat history, or briefly to resubmit a refined prompt; results must not be collected programmatically or used to build a database. Anything not shown to the user is deleted once the final result exists.

Handing a Grounded Result to Claude means a third party (Anthropic's model) analyses it, and Claude's answer mixes it with other content. Saving it into everscout notes is programmatic collection into a database. Each step of the planned pipeline hits a named prohibition. A plugin that only prints the Grounded Result, unmodified with its Search Suggestions, to the person who asked, and that Claude never reads, would comply, but it gives Claude no Reddit access.

### 3. The free tier has no search grounding for new users

Pricing page, updated 2026-10-15:

- Gemini 3 and newer (`gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3-flash-preview`): Google Search grounding on the free tier is "Not available" ("can be tested in Google AI Studio", the web UI). Paid tier: 5,000 search queries a month free, shared across Gemini 3+ models, then $14 per 1,000. `gemini-3.8-flash` tokens cost $0.75 in and $3.75 out per million on the paid tier.
- Gemini 2.5 Flash and Flash-Lite: free-tier grounding up to 500 requests a day. But the models page says "we are limiting access to the 2.5 models to users who have actively used them in the past". A new key will not get them.
- Free tier ("Unpaid Services"): prompts and responses are used to improve Google products and human reviewers may read them; do not send sensitive or personal data. Paid tier: not used. Only paid services may serve users in the EEA, Switzerland or the UK. Users must be 18 or older.

So the free tier cannot do this at all for a new user, whatever the terms say.

### 4. Reddit is suing over Reddit content taken from Google

Reddit v. SerpApi, Oxylabs, AWMProxy and Perplexity (S.D.N.Y. 1:25-cv-08736, filed October 2025) alleges the defendants took Reddit content out of Google search results by getting around Google's SearchGuard. On 2026-07-31 Judge Engelmayer let most of the DMCA and civil conspiracy claims go to discovery, including discovery into Reddit's agreement with Google. A Gemini API route is not scraping and does not get around SearchGuard, so the case is not about it directly. It does show that Reddit treats Reddit content taken from Google as unlicensed.

### 5. Model names in the Gemini chat's script

- `gemini-3.8-flash`: real. Stable, released 2026-09-02, the models page's recommendation for new projects (with `gemini-3.5-flash-lite`). Supports the Google Search tool. Newest model: `gemini-4-argon`.
- `claude-3-5-sonnet-latest`: Claude 3.5 Sonnet was retired in October 2025 (not re-checked this session), so the alias no longer works. Not needed anyway: inside Claude Code, Claude is already the reader.
- The current Google Search tool is documented on the Interactions API (`/v1beta/interactions`, `tools: [{"type": "google_search"}]`, response parts `google_search_call`, `google_search_result` with `search_suggestions`, and `url_citation` annotations).

## Routes that stay open

- Arctic Shift (grey footing; see the 2026-10-11 note): unchanged, still waiting on Mark.
- Cross-platform pickup: unchanged, the main lane.
- The user's own reading. Mark may read Gemini's app (gemini.google.com) or Google's AI Mode himself and paste what he wants kept into a beat's captures inbox, like any capture. The Gemini Apps terms for pasting outputs elsewhere were not checked this session; check them before writing it into a skill. A browser-driven or scripted version is out (conduct rule 17, and the consumer app is not an API).
- Asking Google in writing. The terms allow Google to permit modification or mixing "in writing". A long shot for a personal tool.
- Reddit's own routes: register the everscout app before 2027-01-12 (lasts to March 2027 at most), or a commercial Data API licence.

## Sources (fetched 2026-10-15)

- Gemini API Additional Terms of Service: https://ai.google.dev/gemini-api/terms
- Gemini models (2.5 access note, current ids): https://ai.google.dev/gemini-api/docs/models
- Gemini pricing (free-tier grounding per model): https://ai.google.dev/gemini-api/docs/pricing
- Grounding with Google Search: https://ai.google.dev/gemini-api/docs/google-search
- Search Suggestions display rules: https://ai.google.dev/gemini-api/docs/grounding/search-suggestions
- Google-Reddit deal coverage: https://www.tomsguide.com/ai/google-strikes-dollar60m-deal-with-reddit-for-ai-training-data-what-you-need-to-know, https://www.socialmediatoday.com/news/reddit-partners-google-new-data-sharing-deal/708268/
- Reddit v. SerpApi ruling: https://www.mediapost.com/publications/article/416950/reddit-can-proceed-with-scraping-claims-against-pe.html, https://www.loeb.com/en/insights/publications/2026/08/reddit-v-serpapi-llc, https://www.law360.com/articles/2508228/reddit-ai-data-scraping-case-mostly-survives-dismissal
