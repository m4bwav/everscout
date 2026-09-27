---
title: Engagement ethics and platform rules for a scout that asks makers questions (September 2026)
kind: research
status: active
date: 2026-09-26
verified: 2026-09-26
tags: [ethics, conduct, reddit, hacker-news, bluesky, mastodon, eu-ai-act, ftc, aoir, netnography]
summary: read before changing kb/conduct.md or the engage skill; platform rules on AI-drafted and automated comments, the Zurich r/changemyview lesson, AoIR, what makes makers answer, spam signals, disclosure law, and the 20-rule conduct code everscout adopted
---

# Engagement ethics for everscout (researched 2026-09-26)

## Summary

Human review is necessary and not sufficient: the Zurich researchers reviewed every comment and were still condemned, because they hid the AI, used invented personas, profiled people and broke the community's rules. Reddit's line is account control (an "app" is software operating an account, not a person using AI to write). Hacker News bans generated and AI-edited comments outright since 2026-03-11. r/changemyview and mastodon.social require disclosure. The EU AI Act Article 50(4) (from 2026-08-02) excludes personal activity, and exempts text under substantive human review with editorial responsibility. FTC rules require disclosing material connections. The conduct code in `kb/conduct.md` is built from this note.

V = primary source read on 2026-09-26 (reddit.com pages through Wayback snapshots, dates given). R = secondary.

## 1. Platform rules

- **Reddit Rules** (redditinc.com/policies/reddit-rules, Wayback 2026-09-03, V): rule 2 "Participate authentically in communities where you have a personal interest, and do not spam"; rule 5 no misleading or deceptive impersonation.
- **Responsible Builder Policy** (updated 2026-06-05, support.reddithelp.com article 42728983564564, Wayback 2026-08-28, V): covers "bots, AI agents, or non-human operated accounts"; App label required; explicit consent before private messages; no mixed-use accounts; no "identical or substantially similar content across subreddits"; no inferring sensitive traits or re-identifying users; no training AI on Reddit data; "Any research that uses Reddit data collected outside of the RFR Program is in violation of this policy".
- **Apps on Reddit** (updated 2026-03-25, article 45376380316052, Wayback 2026-07-31, V): an app is an account "operating through software or scripts, rather than direct control by a human". Labels from 2026-03-31; "unusually rapid posting" triggers human verification; Reddit does not plan to label AI-written posts by humans (Help Net Security 2026-03-26, Biometric Update 2026-04-02, R).
- **Data API Wiki** (updated 2026-05-11, V): delete what users deleted; recommend deleting stored content within 48 hours; "NEVER lie about your User-Agent".
- **Hacker News** (news.ycombinator.com/newsguidelines.html, V): "Don't post generated text or AI-edited text. HN is for conversation between humans." Announced 2026-03-11 (item 47340079). dang: "We aren't asking people to not use AI... What we're asking is not to post AI-generated comments."
- **Bluesky** Community Guidelines (effective 2025-09-19, V): no spam, no signal manipulation, no fake identity. Bot guide (bsky-docs bots.mdx, V): self-label, interact only when tagged (opt-in).
- **Mastodon**: bot flag is a visual indication (docs.joinmastodon.org, V); mastodon.social rule 1008 "use of generative AI must be disclosed" (instance rules API, V); `#nobot` in a bio means no automated interaction (convention, R).
- **Lemmy.world**: bots flagged with owner, no ads, only with community permission (R).
- **YouTube** comment spam (support.google.com/youtube/answer/2801973, V): repetitive or similar comments; AI churn.
- **Discord**: self-bots forbidden (R).
- **Trend**: CHI 2025 (arXiv 2410.11698, V): 1.2 percent of subreddits had AI rules in Nov 2024, 17.1 percent of the largest 1 percent; 55 percent of those rules are bans, 18 percent disclosure; art communities lead. CSCW 2025 (Lloyd, Naaman, Reagle, V): moderators see AI content as a threat to quality, human connection and detectability.

## 2. The Zurich r/changemyview experiment (2025)

About 13 accounts, about 1,700 AI comments over four months (R). Wrong on five counts: hidden AI where disclosure is required; invented personas ("a victim of rape", "a trauma counselor", "a black man opposed to Black Lives Matter"); personalised persuasion from inferred traits; no consent from the community; and the researchers "manually reviewed each comment before posting" (Retraction Watch 2025-04-28, V). Reddit's chief legal officer called it "deeply wrong on both a moral and legal level" (R). CMV now: AI use must be disclosed with substantial human content; bot responses banned; accusing others of using AI is also against the rules (wiki, Wayback 2026-08-14, V).

Lines for everscout: no personas, no persuasion, no profiling of individuals, follow community rules whatever the cause, and human review is not a licence.

## 3. Research ethics

AoIR Internet Research Ethics 3.0 (2020, aoir.org/reports/ethics3.pdf, V): people in public forums often expect some privacy (p.8); a verbatim quote re-identifies by string search, so ask why an exact quote is needed and paraphrase (pp.11 to 12); case-by-case judgement. Reddit adds the 48-hour practice and the ban on re-identification.

## 4. What makes makers answer

- Asking questions, especially follow-ups, increases liking (Huang, Yeomans, Brooks et al., JPSP 2017, R).
- Usenet reply rates (Arguello et al., CHI 2006, V): 27 percent of posts got no reply; questions, being on topic and a short personal testimonial each raised reply odds; long, complex wording lowered them.
- Gratitude, reciprocity and prior participation raise success (Althoff et al., ICWSM 2014, R).
- Some communities ask for workflow detail (r/StableDiffusion rules, Wayback 2025-12-10, V).
- Suspected AI use costs trust; being exposed costs more than disclosing (Hohenstein et al. 2023; Jakesch et al. 2019; Schilke and Reimann 2025, R). So make the human authorship real.
- No rigorous study of answer rates by pace; the pace rules are practitioner norms.

## 5. Spam signals

Reported by practitioners (R): new or low-karma accounts, repeated links and domains, promotional words, repeated text, bursts, cross-posting. Official (V): "substantially similar content across subreddits"; rapid posting triggers verification (R); YouTube's similar-comment rule. CMV removes bare agreement ("Great post").

## 6. Disclosure law

- **EU AI Act Art. 50** (artificialintelligenceact.eu/article/50; Commission FAQ 2026-07-24, V): applies from 2026-08-02. 50(4): deployers publishing AI-generated text on matters of public interest disclose it, except where it underwent human review or editorial control and a person holds editorial responsibility; the FAQ says review must be substantive, not "cursory approval". Personal-capacity use is excluded unless it is occupational or regularly economic. A hobbyist is likely out of scope; a professional analyst likely in, and exempt with real review.
- **FTC 16 CFR 255.5** (V): material connections must be disclosed clearly; the 2024 Consumer Reviews and Testimonials Rule bans fake (including AI) testimonials.

## 7. Intelligence ethics

SCIP Code of Ethics (V): comply with law; disclose identity before interviews; respect confidentiality. Berkeley Protocol (OHCHR 2022, V): open-source investigation does not involve soliciting information from users; asking is "closed source"; transparency means no false pretences. Once the scout asks, it is interviewing, so interview ethics apply.

## 8. Domain norms (for the sample beats)

- r/Economics (Wayback 2026-07-26, V): economists' perspective, no memes or self-promotion, comments must engage the article. r/badeconomics (V): explanations required; questions go to r/AskEconomics. EconSky: AEA's 2025-01-02 report backed Bluesky (V).
- Music: r/WeAreTheMusicMakers promotion only in weekly threads (V); KVR no affiliate links, no multiple accounts, its AI forum keeps "the human in the creative workflow" (V); Bandcamp banned music made "wholly or in substantial part" by AI on 2026-01-13 (R). Never ask a musician whether a track is AI.
- AI video: r/aivideo is for serious use of video generation tools with tool-named flair (Wayback 2026-07-19, V); process questions fit.
- Not verified (need a signed-in browser): r/downtempo, r/triphop, r/comfyui, Gearspace rules, reddiquette text.

## The conduct code (adopted as kb/conduct.md, with everscout's additions)

1. The human is the author and presses post. 2. Read the community's AI rule first; where AI-written comments are banned, give ideas, not a draft. 3. Disclose where required; never deny AI help when asked. 4. No personas, no invented experience. 5. Ask and thank; never argue or persuade; stay out of support and crisis threads. 6. Read the work, not the person; no profiling. 7. One true specific observation, then one to three concrete process questions. 8. Never ask "is this AI?", never accuse. 9. Every comment unique to its post. 10. Human pace. 11. Public comments only; respect #nobot and blocks; one unanswered ask per person, ever. 12. No links or self-promotion in engagement comments. 13. Disclose material connections. 14. Answer others only with what the human knows and has checked. 15. Close the loop: thank, share back. 16. Minimal, short-lived notes; paraphrase; purge deleted content; no training. 17. Honest access and User-Agent. 18. One real account; accept moderators. 19. Say who you are when asked; honour off-the-record. 20. Keep a review log.

## Sources

As cited inline, all read or checked 2026-09-26. Wayback snapshot dates are given where the live page blocked fetching.

Related: [prior art](2026-09-26-prior-art.md), [platform access](2026-09-26-platform-access.md)
