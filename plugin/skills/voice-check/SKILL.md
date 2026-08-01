---
name: voice-check
description: Audit a draft against this client's voice profile (brand/voice-profile.md): the Voice Alignment, Audience Specificity, and Pull Signal Design gates, flagging the exact lines that miss and suggesting rewrites in the client's own voice. Use when the user asks whether something sounds right for this client, to voice-check / tone-check a draft, or to catch voice drift.
---

# Voice Check

Audit a draft for voice fidelity to `brand/voice-profile.md`. Do not assume any prior client's voice (e.g. "conversational-professional, gently contrarian") applies here; read this client's own profile every time. Catch drift at the line level before it becomes a pattern.

## Input

A path to a draft or pasted content. Audit the Content section. Infer the content type from the Post Metadata `Type:` field to apply the correct sign-off rule (from `brand/voice-profile.md` / the interview's Section 2 sign-off answer); if pasted text has no type, ask or state the assumption.

**voice-check does NOT verify whether a client story is real.** A line can be perfectly on-voice and still be a fabricated client interaction. If the draft opens with framing that implies a specific real relationship (e.g. "a client I spoke with," a quoted real person), note **"integrity review required, run `validate`"** even when the voice passes. On-voice is not publish-clear.

## Load first

`brand/voice-profile.md` (Voice Characteristics, Structural DNA, Rhetorical Toolkit, Anti-Patterns, Voice Samples), `brand/content-recipe.md` §13 (the checklists below) and §9 (Language Guide), and `brand_config.json` → `voice_and_tone.language_to_avoid` (nested key, not top-level) for this client's full banned list.

## Three gates

### Voice Alignment
- [ ] Opens per this client's Structural DNA (voice-profile.md §4). Not necessarily a story/scenario opener; check what this client's profile actually specifies.
- [ ] Uses this client's rhetorical toolkit (contrarian reframe, myth-bust, etc.) as documented, woven into the argument rather than delivered as a blunt pivot.
- [ ] Address style (direct "you," third person, institutional "we") matches voice-profile.md.
- [ ] Reads in the register voice-profile.md describes (advisor conversation, brochure, technical brief, whichever this client's profile states).
- [ ] Avoids all banned language (`brand_config.json`'s `voice_and_tone.language_to_avoid`).
- [ ] Ends with the correct sign-off per channel, from voice-profile.md / the interview's Section 2 answer (many channels may have no sign-off at all, check, don't assume).
- [ ] Tone matches the profile's stated attributes.
- [ ] **No em dashes, and no banned pivot construction ("It's not X, it's Y" and its variants), unless voice-profile.md's Anti-Patterns section explicitly says this client allows them.** These are the most common AI tells and are hard fails for any client that hasn't cleared them.

### Audience Specificity
- [ ] Could only have been written for `brand_config.json`'s `imagery.audience_context` / the interview's Section 3 audience (not generic advice for anyone).
- [ ] Includes concrete specifics appropriate to that audience's actual sophistication level (income, seniority, technical depth, per Section 3's answers).
- [ ] References the audience's real context (industry, role, life stage) where appropriate.
- [ ] Respects the reader's intelligence and time per Section 3's "what they already know well" answer. Don't over-explain basics the interview said this audience already knows.

### Pull Signal Design
- [ ] Provides genuine value the reader would forward to a peer.
- [ ] Ties tactical advice back to whatever bigger principle this client's positioning centers on (from onboarding Section 1's mission/goals answers).
- [ ] Includes a natural next step matching this client's stated CTA style, not a hard sell unless the client wants one.
- [ ] Reader finishes feeling the emotional outcome this client's content is meant to produce (informed and in control, inspired, entertained, whichever the interview specified), not the opposite.

## Output

Per-item ✓/✗ across all three gates. For every ✗, **quote the offending line** and give a one-line rewrite in this client's voice.

Scan specifically for:
- **Em dashes (run this scan first, every time), unless voice-profile.md explicitly clears them**: search the literal text for `—` (em dash, U+2014), `–` (en dash, U+2013), and `―` (horizontal bar). Any hit is a hard fail by default.
- **The banned pivot, every surface form** ("It's not X, it's Y"; "Not X, but Y"; "not because X, because Y"; and quoted-question variants), unless voice-profile.md says this client's voice uses this construction.
- Whatever throat-clearing kill-phrases voice-profile.md / the corrections log has flagged for this client.
- Brochure tone (feature-listing with no antagonist or scenario), if voice-profile.md says this client avoids that.
- Academic/textbook phrasing, or anything that contradicts the profile's stated register.

Re-derive every item independently; ignore the draft's own `[x]` self-checklist. End with a 1-line verdict: **On-voice** / **Minor drift (N fixes)** / **Off-voice (rework)**. Report only; offer to apply rewrites if the user wants.
