---
name: onboard
description: Interactive first-run onboarding for a new client on this content harness. Conversationally interviews the voice owner/stakeholder (organization, voice, audience, channels + frequency, visual brand, compliance, key dates, language rules), then writes the answers directly into brand/brand_config.json, brand/content-calendar.md, brand/content-recipe.md, and brand/voice-profile.md, including channel_config, which determines which channels generate-batch produces for. Voice profile completion (the deep structural/rhetorical analysis) is a second stage that runs once sample content exists in samples/; onboarding flags this as pending rather than blocking on it. Use when a new client is being set up on this harness for the first time, when the user says "onboard", "set this up for a new client", or "run onboarding", or when generate-batch has refused to run because brand_config.json is incomplete.
---

# Onboard

You are running the first-touch setup interview for a new client on this content harness. It is a conversational 10-section interview; answers are written straight into the live config files as you go, not copy-pasted into a separate document.

## Scope

This skill covers **brand and channel configuration only**: voice, audience, channels, visual brand, compliance language, key dates, and language rules. It does not touch infrastructure (Google Drive folder setup, n8n instance, Claude plan tier); that stays a separate manual step (see `docs/CLIENT_ONBOARDING_GUIDE.md`).

## How to run it

Work through the sections below in order, conversationally, one section (or a few related questions) at a time. Do not dump all ~60 questions in one message. Accept short answers; "not yet" / "N/A" are valid. If the user already answered something earlier in the conversation (e.g. during a prior productization discussion), don't re-ask it, just confirm and move on.

### Section 1: Organization Context
- Organization name, tagline/positioning statement, what the org does (2-3 sentences), mission beyond revenue.
- Primary goals for content, ranked (lead gen, authority building, retention, community, education, brand awareness, recruiting).
- What does success look like in 12 months?

### Section 2: Voice Owner
- Who is the voice: single voice owner, institutional voice, or multiple contributors?
- Background/credibility (single owner) or brand personality adjectives (institutional) or contributor roster (multiple).
- Sign-off phrase.
- Where the voice owner's authority comes from.

### Section 3: Target Audience
- Primary audience: demographics, role, industry, life stage.
- Income/seniority level, top 3-5 concerns/goals, decision-making style.
- What they already know well (don't over-explain) vs. what they need reframed.
- Time available for content consumption; where they spend time online.
- Secondary audience, if any.

### Section 4: Branding
- Brand colors (hex): primary, secondary, accent, light neutral, dark neutral, mid neutral.
- Fonts: heading, body (request font files for `brand/fonts/` if available).
- Existing brand book/style guide, if any.
- Visual tone (calm/professional, bold/modern, warm/friendly, luxurious/refined, clean/minimal, etc.).
- Appropriate imagery vs. imagery to never use.

### Section 5: Channels (drives `channel_config`)
For each channel the client wants, capture: active?, posts per week, format notes, tone notes. Offer a menu covering at least: Blog, LinkedIn, Facebook, YouTube long-form, YouTube Shorts, Instagram feed, Instagram Reels, Twitter/X, TikTok, Email newsletter, Podcast, Other. **Only channels the client actually wants become `active: true` entries. Never carry over another client's channel list or counts; this repo ships with zero channels configured by default.** Also ask: does tone shift between channels? Is content repurposed across channels (e.g. podcast → clips)? Does any channel need an extra approval step before publishing?

### Section 6: Content Objectives and Criteria
- What "good" content looks like for this org; what "bad" content looks like.
- Target volume.
- On-limits topics (what you want to own) vs. off-limits topics (no authority / never touch).
- Format priorities (e.g. more video, data-heavy, story-driven).
- Existing content library/archive location, if any.

### Section 7: Compliance and Regulatory Constraints
- Industry-specific regulatory requirements (financial services, healthcare, legal, real estate, education, etc.; ask which applies).
- Required disclaimers/disclosures, exact language.
- Internal review/compliance process, if any.
- Claims that can never be made; governing external regulations or professional codes.

### Section 8: Key Dates and Cycles
- Fiscal year.
- Key deadlines/dates/events content should align to, and why each matters.
- Seasonal cycles affecting the audience.
- Recurring industry events/conferences/publications.
- How far in advance content should reference upcoming deadlines.

### Section 9: Language Rules and AI-Giveaway Detection
- Branded/preferred vocabulary vs. banned words/phrases.
- Industry terms the audience expects vs. terms that read as jargon.
- Punctuation stance: em dashes, Oxford comma, exclamation points, emoji, capitalization style.
- Walk through the standard AI-giveaway list (em dashes; "It's not X. It's Y." pivots; delve/landscape/navigate/crucial/realm/foster/robust; excessive hedging; "Here are X things..." openers; "in today's [adjective] [noun]"; "let's dive in/break it down/unpack this"; leverage/utilize/facilitate) and ask which to explicitly ban.
- The "golden rule" sentence: "If it sounds like ___, rewrite it. If it sounds like ___, it's correct."

### Section 10: Sample Content (gates Stage 2, not Stage 1)
- Does the client have 10-30+ existing pieces representing the target voice? Where are they?
- If yes: ask them to place the files in `samples/` now or before the next session.
- If no: who will produce samples, and by when?
- Any "gold standard" samples or deliberately-bad negative examples to flag.

**Do not block Stage 1 completion on this section.** If samples aren't ready, note it as an open item and move on. Stage 2 runs later.

## Writing the outputs (Stage 1)

Once the interview is complete, write directly into the live files in this repo:

1. **`brand/brand_config.json`**: `brand_name`, `tagline`, `colors`, `typography`, `voice_and_tone` (attributes, language to use/avoid, final_rule), `imagery`, `compliance` (rules + required_disclaimers), and **`channel_config.channels`** built from Section 5's answers exactly as the client stated it. Do not carry over any other client's channel list or counts.
2. **`brand/content-calendar.md`**: key dates, deadlines, seasonal cycles, and lead time from Section 8.
3. **`brand/content-recipe.md`**: audience translation notes (Section 3), content objectives/criteria (Section 6), compliance language (Section 7). If the client selected a channel with no existing Content Architecture Template in Section 7 of this doc (e.g. a newsletter or TikTok, not already covered), draft a new template subsection for it following the pattern of the existing ones. Don't leave an active channel without a production template.
4. **`brand/voice-profile.md`**: fill Section 1 (Person/Brand), Section 2 (Core Philosophy, as far as the interview surfaced it), and Section 6 (Anti-Patterns, from Section 9's banned words/punctuation/AI-giveaway answers) now. Mark Sections 3, 4, 5, and 7 (Voice Characteristics, Structural DNA, Rhetorical Toolkit, Voice Samples) explicitly as `**PENDING, requires sample content analysis, see Stage 2 below**` rather than guessing at them from the interview alone.

After writing, run through `brand_config.json` and confirm no bracketed placeholder tokens remain and `channel_config.channels` has at least one `active: true` entry. This is exactly what `generate-batch`'s Step 0 preflight checks, so if this isn't true yet, say so plainly rather than reporting onboarding as done.

## Stage 2: Voice profile completion (runs later, once samples exist)

When the user confirms samples are in `samples/` (immediately, or in a later session), run the voice-profile generation pass:

1. Read every file in `samples/` in full.
2. Produce the full voice profile: Section 3 (Voice Characteristics: register, tone, vocabulary, emotional range), Section 4 (Structural DNA), Section 5 (Rhetorical Toolkit), and Section 7 (Voice Samples: 5-8 labeled excerpts), replacing the `PENDING` markers left by Stage 1.
3. Run the AI-giveaway detection test: generate 3 short test paragraphs in the profiled voice, compare against the real samples, and add any tell you find (that isn't in the real samples) to the Anti-Patterns section as a "Never Use" rule.
4. Report the completed `brand/voice-profile.md` and confirm no `PENDING` markers remain.

## Output

End with a summary: which sections were completed, which channels are now active (with their posts_per_week), any open items (missing samples, unresolved compliance questions), and whether `generate-batch` will now pass its preflight check.
