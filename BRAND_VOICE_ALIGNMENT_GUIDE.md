# Brand & Voice Alignment Guide

> This guide explains how to turn the `onboard` skill's interview answers into a fully configured content production system. It covers voice-profile generation, AI-giveaway detection, channel configuration, compliance setup, example transformations, and multi-voice considerations. Most of Section 1 (populating `brand_config.json`) and part of Section 2 (Stage 1 of the voice profile) happen automatically as part of running `/onboard` — this guide is the deeper reference for what `/onboard` does and how to go further by hand if needed.

**Prerequisite:** Run the `onboard` skill (Stage 1) before working through this guide.

**Companion documents:**
- `plugin/skills/onboard/SKILL.md`: The interactive interview that captures raw context and writes it into the files below
- [docs/CLIENT_ONBOARDING_GUIDE.md](docs/CLIENT_ONBOARDING_GUIDE.md): The end-to-end fork-to-production walkthrough
- [brand/voice-profile.md](brand/voice-profile.md): The voice profile you will generate
- [brand/brand_config.json](brand/brand_config.json): The brand configuration you will populate

---

## 1. Branding Configuration

### 1.1 Populate brand_config.json

Open `brand/brand_config.json` and fill in the values from your onboard interview Section 4:

- **`brand_name`:** Your organization's name.
- **`tagline`:** Your tagline or positioning statement.
- **`colors`:** Replace all placeholder hex codes with your brand colors. Each color entry has a `name`, `hex`, `rgb`, and `usage` field.
- **`typography`:** Replace `[HEADING_FONT]` and `[BODY_FONT]` with your font families. Place font files (TTF/OTF) in `brand/fonts/`.
- **`imagery`:** Update the `audience_context` field with your audience description. Update `people_imagery` and `environment_imagery` with guidance appropriate for your brand.
- **`voice_and_tone`:** Fill in `attributes`, `tone_by_context`, `language_to_use`, and `language_to_avoid` from onboard interview Sections 9 and 6. Set the `final_rule` to your golden rule from onboard interview Question 57.

### 1.2 Visual References

If you have an existing brand book, style guide, or sample graphics:
- Create a `brand/references/` folder.
- Place brand book PDFs, logo files, or example graphics there.
- Reference them in `brand_config.json` `imagery` section so content producers can match the visual standard.

### 1.3 Color Ratio

Define how your colors should be distributed across visual assets:

```json
"color_ratio": {
  "primary": 60,
  "secondary_neutrals": 30,
  "accent": 10,
  "description": "60-30-10 guideline: 60% Primary, 30% Secondary/Neutrals, 10% Accent"
}
```

Adjust the ratio if your brand uses a different distribution.

---

## 2. Voice Profile Generation

This is the most important step. The voice profile is the system's source of truth for how content should sound.

### 2.1 Preparation

Confirm that:
- [ ] 10-30+ sample pieces are in the `samples/` folder.
- [ ] The `onboard` skill's Stage 1 interview is complete (especially Sections 2, 9, and 10).
- [ ] `brand/brand_config.json` has been populated with at least the `voice_and_tone` section.

### 2.2 Run onboard's Stage 2

Ask the `onboard` skill to run its Stage 2 voice-profile completion (or say "the samples are ready, generate the voice profile"). It:

1. Reads all content in `samples/`.
2. Analyzes patterns across the samples to extract:
   - **The person behind the voice** (or brand personality for institutional voices): background, credibility model, the role they play for the reader.
   - **Core philosophy / belief system:** 3-8 foundational beliefs that run through the samples.
   - **Voice characteristics:** Register (casual to formal), tone (warm, direct, cautionary, etc.), vocabulary patterns (frequently used words/phrases, avoided words/phrases), emotional range.
   - **Structural DNA:** Recurring post architecture (how posts open, develop, and close), formatting patterns (paragraph length, use of lists, headers, etc.).
   - **Rhetorical toolkit:** Rhetorical questions, contrarian framing, metaphors, math/data as persuasion, storytelling patterns, named frameworks.
   - **Anti-patterns:** What the voice owner never does (tone, structure, vocabulary, punctuation).
   - **Voice samples:** Direct excerpts from the samples demonstrating key characteristics.
3. Outputs a complete `brand/voice-profile.md`.

### 2.3 Human Review

The voice owner must read the generated profile and answer:
- Does this sound like me?
- Is anything missing?
- Is anything wrong or overstated?
- Are there patterns I use that the analysis missed?

Revise until the voice owner says "yes, this is me."

### 2.4 Mirror to brand_config.json

After the voice profile is finalized, ensure `brand_config.json` `voice_and_tone` reflects the profile:
- `attributes`: 3-5 adjectives describing the voice.
- `tone_by_context`: How tone shifts by content type (educational, advisory, CTA).
- `language_to_use`: Preferred vocabulary and phrases from the profile.
- `language_to_avoid`: Banned vocabulary and phrases from the profile's anti-patterns.
- `final_rule`: The golden rule from the profile.

These two files (voice-profile.md and brand_config.json) must stay in sync. If you update one, update the other.

---

## 3. AI-Giveaway Detection

AI-generated text has recognizable patterns. Every voice will have its own set of "tells" where the AI defaults diverge from the real voice. Detecting and banning these is critical for authenticity.

### 3.1 Default Banned Patterns

The system ships with these defaults. Keep them unless your brand explicitly uses them:

| Pattern | Why it's banned |
|---------|-----------------|
| Em dashes (--) | Common AI default. Many human writers rarely or never use them. |
| "It's not X. It's Y." pivot | Formulaic rhetorical move that AI uses excessively. |
| "Delve," "landscape," "navigate," "crucial," "realm," "foster," "robust" | AI-favored vocabulary that reads as artificial. |
| "It's important to note that..." | Hedging filler that adds no value. |
| "Here are X things you need to know about..." | Template-style list introduction. |
| "In today's [adjective] [noun]..." | Generic AI opening. |
| "Let's dive in" / "Let's unpack this" | Cliche transition phrases. |

### 3.2 Discovering Voice-Specific Giveaways

Run this process after generating the voice profile:

1. **Generate 5-10 test drafts** using the system (e.g., generate a few pieces with `/generate-batch` or by asking Claude directly).
2. **Print them alongside 5-10 real samples** (or view them side by side).
3. **Compare line by line.** Ask:
   - What punctuation choices appear in AI drafts but not in samples?
   - What sentence structures or lengths feel different?
   - What transition words or phrases does the AI use that the real voice doesn't?
   - How do openings differ? Closings?
   - Are there emotional registers the AI hits that the real voice avoids (or vice versa)?
4. **Document each pattern** you find as a "Never Use" rule.
5. **Add each rule** to three places:
   - `brand/voice-profile.md` (anti-patterns section)
   - `brand/content-recipe.md` (language to avoid)
   - `brand/brand_config.json` (`voice_and_tone.language_to_avoid`)
6. **Add a checklist line** in `brand/content-recipe.md` Quality Checklist: "Free of [pattern description]."

### 3.3 Ongoing Detection

Re-run this process:
- Quarterly (voices evolve; AI models change).
- When switching AI models or providers.
- When the voice owner flags content that "doesn't sound right" but passes existing checks.

---

## 4. Channel Configuration

### 4.1 Populate channel_config

Open `brand/brand_config.json` and populate the `channel_config` section from onboard interview Section 5:

```json
"channel_config": {
  "channels": [
    {
      "name": "Blog",
      "active": true,
      "posts_per_week": 1,
      "format": "Long-form article",
      "tone_notes": "Full voice; signs off with [SIGN_OFF_PHRASE]",
      "dimensions": { "width": 1200, "height": 628 }
    },
    {
      "name": "LinkedIn",
      "active": true,
      "posts_per_week": 5,
      "format": "Professional insight posts",
      "tone_notes": "Professional, direct",
      "dimensions": { "width": 1080, "height": 1080 }
    }
  ]
}
```

Add one entry per active channel. Set `active: false` for channels you want to configure but not produce for yet.

### 4.2 Update the Content Recipe

In `brand/content-recipe.md`, the channel-related sections reference `channel_config`. After populating the config:

- Update the weekly volume table in the Content Production Batch Standards.
- Update the Block Assembly table (which building blocks each channel uses).
- Update the Content Architecture section with format specs per channel.

### 4.3 Update the Batch Rule

In `.cursor/rules/content-production-batch.mdc`, update the weekly volume table to match your channel configuration.

### 4.4 Repurposing Flows

If you repurpose content across channels (onboard interview Question 31), document the flow in `brand/content-recipe.md`. Example:

```
Blog post (anchor) → 5 LinkedIn posts (extracted insights) → 5 Facebook posts (warmer tone)
Podcast script → 2-5 short-form clips (YouTube Shorts / Instagram Reels)
```

---

## 5. Compliance and Regulatory Setup

### 5.1 Populate Compliance Rules

From onboard interview Section 7, add your compliance constraints to:

1. **`brand/content-recipe.md`** -- Compliance Guardrails section:
   - Replace `[COMPLIANCE_RULE_1]`, `[COMPLIANCE_RULE_2]`, etc. with your actual rules.
   - Replace `[REQUIRED_DISCLAIMERS]` with any required disclaimer language.

2. **`.cursor/rules/content-integrity.mdc`** -- Compliance section:
   - Add any rules that should trigger automated checks.

3. **`brand/brand_config.json`** -- `compliance` key:
   - List compliance rules and required disclaimers.

### 5.2 Quality Checklist

Add compliance checkboxes to the Quality Checklist in `brand/content-recipe.md`:

```
### Compliance
- [ ] No claims that violate [COMPLIANCE_RULE_1]
- [ ] No claims that violate [COMPLIANCE_RULE_2]
- [ ] Required disclaimers are included where applicable
- [ ] Content has passed internal review (if required)
```

### 5.3 Industry-Specific Examples

| Industry | Common compliance rules |
|----------|----------------------|
| Financial services | No guarantees, no testimonials, forward-looking disclaimers, RIA marketing rules |
| Healthcare | Medical disclaimers, HIPAA considerations, "not medical advice" language |
| Legal | "Not legal advice" disclaimers, jurisdiction caveats, privilege considerations |
| Real estate | Fair housing language, equal opportunity disclosures |
| Technology | Data privacy disclosures, security claim limitations |

Use these as starting points; consult your compliance team for specifics.

---

## 6. Example Transformations

Example transformations show how generic content gets rewritten in your voice. They are teaching tools that calibrate the AI and serve as reference for human reviewers.

### 6.1 Creating Transformations

After the voice profile is finalized, create 2-3 example transformations:

1. **Pick a topic** relevant to your content.
2. **Write a bland, default version** (generic, no voice personality).
3. **Rewrite it in your voice** using the voice profile.
4. **Document what changed** (tone shifts, vocabulary swaps, structural choices, audience-specific adjustments).

### 6.2 Scaffolding Template

Add these to `brand/content-recipe.md` Section 14:

```markdown
### Example [N]: "[Generic angle]" -> "[Voice-aligned angle]"

**Generic version:**
> [A paragraph written in a flat, default voice with no personality]

**Voice-aligned version:**
> [The same content rewritten using the voice profile]

**What changed:** [2-3 sentences explaining the specific voice shifts applied:
tone adjustments, vocabulary choices, structural changes, audience awareness,
rhetorical techniques used]
```

### 6.3 Tips

- The generic version should sound like "anyone could have written this."
- The voice-aligned version should sound like "only [PERSON_NAME] would say it this way."
- Focus the "what changed" explanation on patterns others can repeat.
- Add more transformations over time, especially when voice checks repeatedly flag the same issues.

---

## 7. Multi-Voice Configurations

### 7.1 Single Voice Owner (Default)

The default configuration. All content sounds like one person.

- `[PERSON_NAME]` is used throughout.
- Voice profile documents one individual's characteristics.
- Sign-off uses the person's name.
- No additional configuration needed.

### 7.2 Institutional Voice

Content sounds like the organization, not a specific person.

Configuration changes:
- Replace `[PERSON_NAME]` with `[ORG_NAME]` throughout all files.
- In `brand/voice-profile.md`, Section 1 becomes "The Brand Voice" instead of "The Person Behind the Voice." Describe the brand's personality, values, and communication style as if the brand were a person.
- Sign-off is optional or uses the org name (e.g., "The [ORG_NAME] Team").
- Anti-patterns focus on tone consistency rather than personal quirks.
- The experience inventory and interview guide still apply (the org's experience, not a person's).

### 7.3 Multiple Contributors

Multiple people create content, each with their own style but within a unified brand voice.

Configuration changes:
- Create one primary `brand/voice-profile.md` that defines the unified brand voice (shared tone, shared anti-patterns, shared quality standards).
- Create a `brand/contributor-profiles/` folder with one file per contributor (e.g., `jane.md`, `tom.md`). Each file notes how that contributor's voice differs from the primary profile (e.g., "Jane is more formal and uses longer sentences; Tom uses more humor and shorter paragraphs").
- Content-recipe Block 5 (Voice Validation) checks against the primary profile first, then the contributor's sub-profile.
- The batch rule can optionally note which contributor writes for which channel.

---

## 8. Training the System

### 8.1 The Voice Profile Is the Anchor

Every piece of content is evaluated against `brand/voice-profile.md`. The more accurate and detailed this document is, the better the system performs. Invest time in getting it right.

### 8.2 Samples Are the Ground Truth

The `samples/` folder is the empirical evidence behind the voice profile. When in doubt about "would [PERSON_NAME] say it this way?", check the samples.

### 8.3 Quality Gates Enforce the Rules

The three enforcement layers work together:

1. **Voice profile + content recipe:** The AI reads these before drafting and self-corrects during generation.
2. **Quality Checklist:** Every draft includes a checklist that the AI evaluates against.
3. **Cursor rules:** Automated rules that flag violations in draft files (em dashes, integrity issues, date misalignment).

### 8.4 Recursive Learning Closes the Loop

After content is published and performance data is collected:
1. Log metrics in `outputs/performance-logs/`.
2. Run the `retro` skill (recursive learning cycle).
3. The cycle updates the content recipe, calendar, and voice profile based on what actually worked with the audience.

This is how the system gets better over time. Without performance data, it stays static.

### 8.5 Prompt Snippets for Cursor (optional, non-Claude-Code workflows)

When working in Cursor, always reference the brand documents before drafting:

```
Read @brand/voice-profile.md and @brand/brand_config.json voice_and_tone section
before drafting. Check all output against the Quality Checklist in
@brand/content-recipe.md Section 13 and the language_to_avoid list.
```

This can be added to `.cursor/rules/` as an always-apply rule if desired.

---

## Checklist: Alignment Complete

Before moving to content production, confirm:

- [ ] `brand/brand_config.json` is fully populated (colors, fonts, imagery, voice_and_tone, channel_config, compliance)
- [ ] `brand/voice-profile.md` has been generated from samples and reviewed by the voice owner
- [ ] AI-giveaway detection has been run; banned patterns are documented in voice-profile, content-recipe, and brand_config
- [ ] Channel configuration matches your intended platform mix
- [ ] Compliance rules are documented in content-recipe and content-integrity rule
- [ ] 2-3 example transformations are in content-recipe Section 14
- [ ] Multi-voice configuration is set (if applicable)
- [ ] Validation smoke test passes (generate one test piece and run `validate` + `voice-check` on it)

Once complete, proceed to building your editorial/quarterly plan (see docs/CLIENT_ONBOARDING_GUIDE.md).
