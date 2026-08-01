---
name: image-brief
description: Generate production-ready image prompts for this client's content — correct platform dimensions, exclusive brand palette (from brand_config.json), and the mandatory image-type/color/subject rotation rules applied across a week or batch. Use when the user asks for an image brief, image prompt, or visual asset for a piece, or it is invoked inside generate-batch to brief every asset.
---

# Image Brief

Produce self-contained AI image prompts a person can paste into any generator (Midjourney, Ideogram, DALL-E) and get a brand-consistent result. The credibility test governs everything: *"Would [AUDIENCE] take this seriously?"* — read `brand/brand_config.json`'s `imagery.audience_context` for who that actually is; do not assume any prior client's audience.

## Input

A content piece (path or description) + its channel, OR a batch folder (brief every asset with rotation awareness). If briefing for a single piece outside a batch, ask which platform if it's ambiguous.

## Load first

`brand/content-recipe.md` §10 (Visual Asset Guidelines, the image-prompt standard, and any example prompts it contains), `.cursor/rules/content-production-batch.mdc` (Image Type Variety + Image Prompt Variation), and `brand/brand_config.json` (`colors`, `typography`, `imagery`, `social_image_specs`).

## Palette (exclusive — no other colors)

Read the exact hex values from `brand/brand_config.json`'s `colors` block and the `color_ratio` guideline — never use a prior client's palette (e.g. do not default to navy/gold). Fonts: `typography.heading` / `typography.body` from the same file.

## Dimensions

Read `brand/brand_config.json`'s `imagery.social_image_specs` and each active channel's `dimensions` in `channel_config` — every platform's canvas size lives there, not in this file.

## Every prompt must specify these points (adapt count/order to what the format needs)

1. **Canvas** — exact px + orientation. 2. **Background** — treatment with hex. 3. **Layout/composition** — where each element sits (quadrants, thirds, px margins, alignment). 4. **Typography** — exact text in quotes, font family, weight, ~pt size, hex, alignment, vertical position. 5. **Graphic elements** — dividers/accent lines/logo with hex, thickness, position, scale. 6. **Photographic direction** (if a photo) — subject, environment, lighting, angle, depth of field, color grading shifted toward brand palette. 7. **Brand constraints** — full palette + ratio + the exclusion list from `brand_config.json`'s `imagery.disallowed`. 8. **Mood** — 2-3 descriptors matching `imagery.tone`. 9. **Audience context** — from `imagery.audience_context`, stated plainly (e.g. "professional aesthetic for [AUDIENCE]").

A vague prompt ("minimalist card") is a failure. Two people generating from your prompt should get visually similar results.

## Rotation rules (mandatory — track across the whole week/batch)

The specific counts below are Capable Wealth's original tuning, shown as a worked example of the *kind* of rotation rule this section should hold — read `.cursor/rules/content-production-batch.mdc` for this client's actual rotation rules before applying any of these numbers as fact:

- Max N text-on-block cards (stat/quote) per platform per week; the rest are conceptual photo / infographic / data viz.
- Minimum count of conceptual photographs and infographics per platform per week, with no repeated subject in the same week.
- Text-on-block background colors and layouts rotate across the batch rather than repeating.
- Conceptual photos rotate subject and vary person age/gender representation; state "no people" explicitly when none are used.
- Infographics rotate layout — no two the same week.
- Cross-platform dedup: the same stat on multiple platforms gets different visual treatments, never the same card at multiple dimensions.

## Output

For each asset: image type · one-line rationale · the full prompt · text overlay spec (or "None") · platform + dimensions — matching the Visual Assets block of the Standard Draft File Format (recipe §12). When briefing a batch, start with a short rotation ledger (which card colors, photo subjects, and infographic layouts you assigned to each slot) so the set is provably distinct, then list the prompts.
