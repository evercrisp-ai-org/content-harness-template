# Content Recipe: [ORG_NAME]

> This document is the actionable guide for producing content that sounds like [PERSON_NAME] while serving [AUDIENCE]. It defines HOW content gets made: the workflow, the building blocks, the quality gates, and the validation filters.

**Companion documents:**
- [voice-profile.md](voice-profile.md): WHO: [PERSON_NAME]'s voice, philosophy, and style
- [content-calendar.md](content-calendar.md): WHEN: Timing, relevance cycles, and research checkpoints
- [brand_config.json](brand_config.json): LOOK + TONE: Visual standards, colors, fonts, imagery, and calibrated brand voice attributes

---

## Autonomy Levels

This document uses autonomy levels (L1-L4) to clarify the human-AI division of labor at each step:

- **L1 (Human-led):** Human does the work; AI assists minimally or not at all.
- **L2 (Human-led, AI assists):** Human drives; AI provides research, suggestions, or drafts that the human heavily edits.
- **L3 (AI does, human reviews):** AI produces the output; human reviews, approves, or revises before it goes further.
- **L4 (AI handles, human approves):** AI executes end-to-end; human gives a final yes/no.

---

## 1. The Content Value Flow

Every piece of content follows a value chain. Understanding the chain (and where value can leak) is the foundation for producing content that matters.

```
Audience Need -> Discovery -> Content Creation -> Delivered Content -> Engagement -> Loyal Advocates
      |                                                                              |
      +---------------------------[ Reputation Flywheel ]----------------------------+
```

**Node 1, Audience Need:** What is [AUDIENCE] struggling with, thinking about, or facing right now? Content that doesn't start with a real need leaks value at the first node.

**Node 2, Discovery / Pull Signals:** Content is designed to generate organic discovery. Satisfied readers become advocates who share content with peers. Every piece should contain genuine value that a member of [AUDIENCE] would forward to a colleague.

**Node 3, Content Creation System:** The composable production workflow defined in this document.

**Node 4, Delivered Content:** The finished piece, quality-gated and relevance-validated.

**Node 5, Engagement / Retention:** Does the reader take a next step? Subscribe, share, schedule a conversation, read another piece?

**Node 6, Loyal Advocates:** Readers who generate pull signals for new readers. The flywheel spins.

**Leakage diagnostic:** At each node, ask: What information is being lost? What context vanishes between steps? Where does accountability blur? Fix leaks first; amplify second.

---

## 2. Audience Translation Matrix

### The Core Audience

| Dimension | Value |
|-----------|-------|
| Who | [AUDIENCE] |
| Income / Seniority | [Income or seniority range] |
| Knowledge level | [Beginner / Intermediate / Advanced] |
| Primary concern | [Top concerns] |
| Time availability | [Time-scarce / Variable / Deep-dive oriented] |
| Decision style | [Data-driven / Peer-influenced / Authority-trusting] |
| Life stage | [Building / Optimizing / Transitioning / Preserving] |
| Communication preference | [Casual / Direct / Formal / Respectful of expertise] |

### Key Shifts in Content Approach

[Fill in 4-6 bullet points describing how content should be adapted for this audience. Examples:]

- **[Shift 1]:** [e.g., "Higher sophistication. Do not over-explain basics."]
- **[Shift 2]:** [e.g., "Time-scarce readers. Get to the point."]
- **[Shift 3]:** [e.g., "Complexity-tolerant. Do not oversimplify."]
- **[Shift 4]:** [e.g., "Evidence-driven. Include data and specifics."]

---

## 3. Voice Calibration Guide

How the voice adapts for [AUDIENCE] without losing its essence.

### Keep (Non-Negotiable)

These elements are the DNA of the voice. Without them, it is no longer [PERSON_NAME]:

- [Element 1: e.g., "The warmth. Content must feel like a conversation."]
- [Element 2: e.g., "The storytelling. Every piece opens with a human moment."]
- [Element 3: e.g., "The contrarian framing. Challenge what the audience thinks they know."]
- [Element 4: e.g., "The sign-off. [SIGN_OFF_PHRASE] on all long-form content."]

### Elevate

These elements get dialed up for [AUDIENCE]:

- [Element 1: e.g., "Technical depth. Move beyond basics."]
- [Element 2: e.g., "Specificity of examples. Use audience-relevant numbers."]
- [Element 3: e.g., "Structured decision frameworks. Present decisions as trade-off analyses."]

### Retire

These elements are appropriate for other audiences but not for [AUDIENCE]:

- [Element 1: e.g., "Entry-level explanations."]
- [Element 2: e.g., "Overly casual markers that undermine credibility."]

### Add

New elements introduced specifically for [AUDIENCE]:

- [Element 1: e.g., "Industry-specific context and terminology."]
- [Element 2: e.g., "Audience-specific bridge metaphors: [AUDIENCE_METAPHORS]"]
- [Element 3: e.g., "Time-constraint awareness."]
- [Element 4: e.g., "Peer-level credibility signals."]

---

## 4. Content as Building Blocks

The content pipeline is decomposed into discrete, composable jobs. Each block has defined inputs, processing, and outputs. Blocks are swappable and recombinable.

### The Eight Content Building Blocks

**Block 1: Research**
- Inputs: Topic + content calendar context + current date
- Processing: Gather relevant facts, data, industry context. Verify timeliness. Identify the angle.
- Outputs: Research brief with sources, current data, and relevance assessment
- Autonomy: L3 (AI researches, human reviews)

**Block 2: Brief**
- Inputs: Research brief + voice profile + audience matrix
- Processing: Define the content angle, structure, key points, target length, and target channel
- Outputs: Content brief
- Autonomy: L2 (human-led with AI assist)

**Block 3: Draft**
- Inputs: Content brief + voice profile + content recipe + experience inventory
- Processing: Write the first draft following the voice owner's structural DNA and voice characteristics. Classify all stories and examples per the Content Integrity Filter (Section 5.1).
- Outputs: First draft with story classifications in Post Metadata
- Autonomy: L3 (AI drafts, human reviews)

**Block 4: Relevance Validation**
- Inputs: Draft + content calendar + current date + experience inventory
- Processing: Fact-check all references. Confirm timeliness. Check for conflicting current events. Apply the Relevance Filter (Section 5). Validate story classifications.
- Outputs: Validated draft with relevance score (Green / Yellow / Red)
- Autonomy: L3 (AI validates, human confirms)

**Block 5: Voice Validation**
- Inputs: Draft + voice profile
- Processing: Evaluate the draft against voice characteristics. Flag deviations. Check anti-patterns.
- Outputs: Voice-aligned draft with deviation notes
- Autonomy: L3 (AI checks, human judges)

**Block 6: Edit / Polish**
- Inputs: Validated draft
- Processing: Final editing for clarity, flow, grammar, and brand alignment
- Outputs: Final content
- Autonomy: L1 (human-led)

**Block 7: Distribution**
- Inputs: Final content + channel specifications
- Processing: Format for target platform. Schedule.
- Outputs: Formatted and scheduled content
- Autonomy: L4 (AI handles, human approves)

**Block 8: Performance**
- Inputs: Published content + real engagement data from platform analytics
- Processing: Human logs metrics into the performance data log. AI synthesizes the log into a performance brief and feeds it into the Recursive Learning Loop (Section 11).
- Outputs: Populated performance log + performance brief
- Autonomy: L1 for data capture (human pulls data), L3 for synthesis (AI summarizes)
- Cadence: Log data after each piece has been live for at least 7 days.

**Important:** Block 8 is the only block where the human is the primary data source. The AI cannot access platform analytics. If this block is skipped, the Recursive Learning Loop has no empirical foundation.

### Block Assembly by Content Type

| Content Type | Blocks Used | Notes |
|-------------|------------|-------|
| Blog post / article | All 8 | Full sequence |
| Social post (LinkedIn, Facebook, etc.) | 1, 3, 4, 5, 7, 8 | Lighter brief, shorter draft |
| Podcast / video script | All 8 | Script format; includes clip extraction |
| Short-form clips (Shorts / Reels) | 7, 8 | Derived from validated podcast/video |
| Email sequence | 1, 2, 3, 5, 6, 7, 8 | Brief is critical for sequence arc |
| Lead magnet / report | All 8 + Design block | Adds layout/design step |

---

## 5. The Research and Relevance Filter

A mandatory validation gate applied to every piece of content before publication.

### A. Static Calendar Alignment

Is this content timed correctly relative to known annual cycles? Reference [content-calendar.md](content-calendar.md).

- Content referencing deadlines should precede them by a planning window (typically 4-6 weeks)
- Seasonal content should begin before the season peaks
- [Add audience-specific timing rules from content-calendar.md]

### B. Dynamic Fact Validation

Are all referenced facts, figures, and references current as of publication date?

**Mandatory checks (customize for your industry):**
- [Check 1: e.g., Current regulatory environment]
- [Check 2: e.g., Industry statistics and benchmarks]
- [Check 3: e.g., Market conditions]
- [Check 4: e.g., Pending or recent legislation]
- [Check 5: e.g., Audience-specific economic data]

**Process:** Every draft passes through a fact-check against current data. Stale information gets updated. If a major assumption has changed since the content was briefed, the brief is revised.

### C. Signal-Driven Relevance

Is there something happening right now that this content should acknowledge, incorporate, or be delayed for?

- Has relevant legislation been introduced or passed?
- Is there a market event that would make this content tone-deaf or urgently timely?
- Is the industry experiencing a shift?
- Is there mainstream media coverage that primes the audience?

### Relevance Score

- **Green:** Timely, factually current, no conflicting signals. Proceed.
- **Yellow:** Mostly current but needs specific updates or timing adjustment. Revise.
- **Red:** Contains stale information, conflicts with current events, or is poorly timed. Hold.

Only Green content publishes. Yellow content is revised. Red content is shelved.

---

## 5.1. The Content Integrity Filter

A mandatory validation gate that ensures all claims about experience, client work, and outcomes are honest and verifiable.

**Mandatory reference:** [experience-inventory.md](experience-inventory.md)

### Story Classification

Every client story, case study, or example must be classified:

**[REAL-ANONYMIZED]:** A story based on a verified entry in `experience-inventory.md`. Details changed for privacy.
- Must trace to a specific entry in the inventory
- May use phrases like "a client I work with" or "someone I advise"

**[ILLUSTRATIVE]:** A constructed example using realistic but hypothetical numbers.
- Must be framed with language that signals the example is hypothetical
- Approved framing: "Consider a [AUDIENCE member] earning..." / "Here's how this might look..." / "Let's walk through a scenario..."
- Must NOT use language implying a real advisory relationship
- Must NOT use specific temporal references implying recent real work

**[GENERAL-PRINCIPLE]:** A statement of principle or industry observation without a specific narrative.
- Frame as expertise-based authority
- Does not require an experience inventory reference

### Compliance Guardrails

These apply to all content regardless of story classification:

1. **[COMPLIANCE_RULE_1]:** [Description. e.g., "No implied guarantees of specific outcomes."]
2. **[COMPLIANCE_RULE_2]:** [Description. e.g., "No testimonial-style framing of results."]
3. **[REQUIRED_DISCLAIMERS]:** [Description. e.g., "Forward-looking projections must include qualifying language."]

[Add industry-specific rules from Recalibrating Interview Section 7.]

---

## 6. Human Checkpoints

These are the moments where human judgment is required:

| Checkpoint | What the human does | When |
|-----------|---------------------|------|
| Brief approval | Confirms content angle and structure | After Block 2 |
| Draft review | Reads for voice accuracy and factual correctness | After Block 3 |
| Relevance confirmation | Confirms relevance score and any needed updates | After Block 4 |
| Voice judgment | Determines if voice deviations are acceptable | After Block 5 |
| Final approval | Signs off on finished content | After Block 6 |
| Performance data | Pulls metrics from platform analytics | After Block 7 (7+ days) |

---

## 7. Content Architecture by Channel

Format specifications for each channel. Update based on your `brand_config.json` `channel_config`.

### Blog Post

- **Length:** 800-1,200 words
- **Structure:** Follow voice-profile.md structural DNA
- **Visual assets:** Hero image + 1-3 in-body images
- **Sign-off:** [SIGN_OFF_PHRASE]

### Social Post (LinkedIn, Facebook, etc.)

- **Length:** 100-300 words (adjust per platform norms)
- **Structure:** Hook line (earn the click/tap), core insight, takeaway or question
- **Visual assets:** One primary image
- **Sign-off:** Omit or use abbreviated version

### Podcast / Video Script

- **Length:** Max 25 minutes
- **Structure:** Cold open (30-60s), context, key points (3-5), close
- **Visual assets:** Thumbnail / cover art
- **Derivative:** 2-5 short-form clips extracted from the recording
- **Sign-off:** Verbal close

### Short-Form Clips (YouTube Shorts / Instagram Reels / TikTok)

- **Duration:** 45-90 seconds
- **Format:** Vertical (9:16), 1080x1920px
- **Requirements:** Captions required; keep critical content in center 4:5 safe zone
- **Source:** Extracted from podcast/video; not net-new creation

### Email

- **Length:** 300-600 words
- **Structure:** Personal opening, one core insight, clear next step
- **Sign-off:** [SIGN_OFF_PHRASE]

[Add or remove channels based on your configuration.]

---

## 8. Topic Mapping

Map core themes to audience-relevant angles. Fill in after the editorial plan is created.

| Core Theme | Audience Angle | Example Topics |
|-----------|---------------|----------------|
| [Theme 1] | [How this applies to AUDIENCE] | [2-3 specific topic ideas] |
| [Theme 2] | [How this applies to AUDIENCE] | [2-3 specific topic ideas] |
| [Theme 3] | [How this applies to AUDIENCE] | [2-3 specific topic ideas] |
| [Theme 4] | [How this applies to AUDIENCE] | [2-3 specific topic ideas] |

---

## 9. Language and Terminology Guide

### Use These Words and Phrases

[Fill in from voice-profile.md vocabulary patterns and brand_config.json language_to_use]

- [Word/phrase 1]
- [Word/phrase 2]
- [Word/phrase 3]

### Avoid These Words and Phrases

[Fill in from voice-profile.md anti-patterns and brand_config.json language_to_avoid]

- Em dashes (the long dash). Use commas, periods, parentheses, or colons instead. This is a hard rule.
- The "It's not X. It's Y." pivot construction. Contrarian reframes should be integrated naturally.
- "Delve," "landscape," "navigate," "crucial," "realm," "foster," "robust" (common AI defaults)
- [Add org-specific banned words/phrases]

### Bridge Metaphors

Metaphors that connect [AUDIENCE]'s world to your subject matter:

- [Metaphor 1: "[AUDIENCE_METAPHORS]"]
- [Metaphor 2]
- [Metaphor 3]

### The Golden Rule

From brand_config.json: *"[final_rule from voice_and_tone]"*

---

## 10. Visual Asset Guidelines

Every piece of content gets a corresponding visual asset. The image reinforces the core message, not decorates it.

### Platform Specifications

Reference `brand_config.json` `imagery.social_image_specs` for exact dimensions per platform.

### Visual Types

- **Stat highlight card:** Pull a striking number and display it prominently.
- **Simple infographic:** Clean chart, comparison, or process flow.
- **Conceptual photograph:** Professional, editorial-quality photo evoking the theme.
- **Quote/insight card:** Short pull quote typeset on brand.
- **Data visualization:** Branded chart or graph for math-heavy content.

### Weekly Image Type Distribution

Each week's images must feel visually distinct when viewed as a set:

| Slot | Required Image Type |
|------|-------------------|
| 1 of 5 | Stat highlight card or quote card |
| 2 of 5 | Conceptual photograph (photorealistic) |
| 3 of 5 | Simple infographic or data visualization |
| 4 of 5 | Conceptual photograph (different subject) |
| 5 of 5 | Any type not already used this week |

### The 9-Point AI Image Prompt Standard

Every AI image prompt must specify ALL of the following:

1. **Canvas:** Exact pixel dimensions and orientation
2. **Background:** Exact treatment with hex codes
3. **Layout/composition:** Where every element sits on the canvas
4. **Typography (if text appears):** Exact text, font, weight, size, color hex, position
5. **Graphic elements (if any):** Dividers, logos, icons with color, thickness, position
6. **Photographic direction (if applicable):** Subject, environment, lighting, camera angle, color grading
7. **Brand constraints:** Full palette with hex codes, ratio, exclusion list
8. **Mood:** 2-3 descriptors
9. **Audience context:** "[AUDIENCE] description"

---

## 11. The Recursive Learning Loop

Every piece of content feeds a five-stage loop that makes the next piece better. This loop only works if fed real data from real audience behavior.

### Prerequisite: Performance Data

Before running this cycle, populate the performance data log with actual metrics. Use [performance-log-template.md](performance-log-template.md).

### Stage 1: Observe
Review the performance data log. Extract quantitative signals (engagement rates, top performers, retention), qualitative signals (comments, shares, feedback), and audience signals (who is engaging).

### Stage 2: Detect
Identify patterns: which topics, formats, channels, and timing produce the strongest results.

### Stage 3: Interpret
Synthesize root causes: why did certain pieces outperform or underperform?

### Stage 4: Refactor
Translate understanding into system improvements: update the content calendar, refine content architecture, adjust voice calibration, revise channel strategy.

### Stage 5: Reflect
Publish a "What We Learned" brief. Feed insights back into the content recipe and calendar. Identify experiments for the next cycle.

### Cadence

| Review Type | Frequency | Scope | Output |
|------------|-----------|-------|--------|
| Lightweight | Monthly | Top 3 learnings, quick metrics check | Brief update note |
| Deep review | Quarterly | Full five-stage cycle | Updated master documents |
| Strategic | Annually | Topic priorities, audience evolution, voice refinement | Revised editorial strategy |

---

## 12. Standard Draft File Format

Every draft content file follows a standardized four-part structure:

```
---
## Post Metadata
- **Type:** [Blog Post / Social Post / Podcast Script / etc.]
- **Week:** [Week N (date range)]
- **Theme:** [e.g., Topic Theme]
- **Quarterly plan reference:** [e.g., quarterly-plan-Q1.md, Week 1, Anchor]
- **Strategic context:** [1-2 sentences on how this piece fits the broader strategy]
- **Story classifications used:** [List each classification used]

---
## Visual Assets

### Primary Image
- **Image type:** [stat highlight / infographic / conceptual photo / quote card / data viz]
- **Rationale:** [One sentence on why this type suits this piece]
- **AI image prompt:** [Full production-ready prompt per 9-point standard]
- **Text overlay:** [Exact text, font, weight, size, color hex, position. "None" if no text.]
- **Platform and dimensions:** [e.g., LinkedIn, 1080x1080]

---
## Clip Extraction Map (podcast/video scripts only)

### Clip 1
- **Source segment:** [Segment name]
- **Hook line:** [First sentence the viewer hears]
- **Core insight:** [What the clip teaches]
- **Platform tags:** [YT-SHORT] / [IG-REEL] / [BOTH]
- **Estimated duration:** [e.g., ~55 seconds]

---
## Content

[The full content goes here]

---
## Quality Checklist

[Quality checklist results per Section 13]
```

---

## 13. Quality Checklist

The final gate before any content publishes. Every item must pass.

### Voice Alignment
- [ ] Opens with a story, conversation, or specific scenario (not a definition or statistic)
- [ ] Contains at least one contrarian reframe or fresh angle
- [ ] Uses direct "you" address throughout
- [ ] Reads like a conversation with a trusted advisor, not a brochure or sales piece
- [ ] Avoids all banned language (Section 9)
- [ ] Ends with a clear takeaway and appropriate sign-off
- [ ] Tone matches the voice profile
- [ ] Free of em dashes and formulaic "not X / it's Y" pivot constructions
- [ ] Free of AI-giveaway patterns (see voice-profile.md anti-patterns)

### Audience Specificity
- [ ] Could only have been written for [AUDIENCE] (not generic advice)
- [ ] Includes a concrete example relevant to [AUDIENCE]
- [ ] References audience-specific context where appropriate
- [ ] Respects the reader's intelligence and time

### Relevance Validation
- [ ] All facts, figures, and references are current as of publication date
- [ ] Content is appropriately timed relative to the annual calendar
- [ ] No conflicting current events that would undermine the message
- [ ] Relevance Score is Green

### Pull Signal Design
- [ ] Content provides genuine value that [AUDIENCE] would share with a peer
- [ ] Ties tactical advice back to a bigger principle
- [ ] Includes a natural next step (not a hard sell)
- [ ] The reader finishes feeling more informed, not more anxious

### Visual Assets
- [ ] Every content piece includes a Visual Asset Brief
- [ ] AI image prompt follows the 9-point standard (Section 10)
- [ ] AI image prompt is self-contained and production-ready
- [ ] Image uses only the brand color palette with correct hex codes
- [ ] Would [AUDIENCE] take this seriously?

### Content Integrity
- [ ] Every client story is classified: [REAL-ANONYMIZED], [ILLUSTRATIVE], or [GENERAL-PRINCIPLE]
- [ ] Story classifications listed in Post Metadata
- [ ] All [REAL-ANONYMIZED] stories trace to experience-inventory.md
- [ ] All [ILLUSTRATIVE] examples use approved framing language
- [ ] No fabricated claims or implied guarantees
- [ ] Forward-looking projections include qualifying language

### Compliance
- [ ] [COMPLIANCE_RULE_1] is satisfied
- [ ] [COMPLIANCE_RULE_2] is satisfied
- [ ] Required disclaimers included where applicable

### Short-Form Clips (podcast/video scripts only)
- [ ] Clip Extraction Map included with 2-5 candidates
- [ ] Each clip stands alone without context from the full episode
- [ ] Hook lands in the first 3 seconds
- [ ] Duration within platform target
- [ ] Content stays within safe zone
- [ ] Clip ends with a clear takeaway (not mid-sentence)

---

## 14. Example Transformations

Use these to calibrate the AI and train human reviewers. Create 2-3 following the process in BRAND_VOICE_ALIGNMENT_GUIDE.md Section 6.

### Example 1: "[Generic angle]" -> "[Voice-aligned angle]"

**Generic version:**
> [A paragraph in a flat, default voice with no personality]

**Voice-aligned version:**
> [The same content rewritten using the voice profile]

**What changed:** [2-3 sentences explaining the voice shifts applied]

### Example 2: "[Generic angle]" -> "[Voice-aligned angle]"

**Generic version:**
> [A paragraph in a flat, default voice]

**Voice-aligned version:**
> [The same content rewritten using the voice profile]

**What changed:** [2-3 sentences explaining the voice shifts]

[Add more examples as voice checks reveal common calibration issues.]
