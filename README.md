# Content Harness Template

A client-agnostic content production system for Claude Code / Claude Cowork: brand-voice capture, quality-gated multi-channel content generation, Google Drive publishing, and a recursive-learning loop that improves the system from real corrections over time.

This repo ships with **zero clients configured**. Fork it per client, run the `onboard` skill, and you have a working weekly content pipeline for whatever channels that client actually wants — one channel or ten.

## What this is

- **Eight Claude Code skills** (`plugin/skills/`): `onboard` (first-run interview), `generate-batch` (the weekly engine), `validate`, `linkedin-check`, `image-brief`, `voice-check`, `research-scan`, `retro` (recursive learning).
- **Brand docs** (`brand/`): placeholder voice profile, content recipe, content calendar, `brand_config.json` (colors, fonts, voice/tone, compliance, and `channel_config` — which channels are active and how often). `onboard` fills these in from a conversational interview.
- **A Python rendering/export pipeline** (`src/`): Excel batch summaries, Google Drive publish-plan generation, PDF/image lead-magnet rendering — all driven by `brand_config.json`, not hardcoded to any client.
- **Automation templates** (`automation/`): an n8n image-generation workflow and a Drive folder-ID config, both `REPLACE_ME_`-templated per client.
- **Quality gates** (`brand/content-recipe.md` §5.1 and `brand/content-calendar.md`'s Date Alignment Rules): content integrity, date alignment, and batch production rules, enforced automatically inside `generate-batch`.

## Quick start (for a new client)

1. Fork or clone this repo into a new folder/repo for the client.
2. Read `docs/CLIENT_ONBOARDING_GUIDE.md` — it walks through renaming the plugin, running `/onboard`, infra setup (Drive, n8n, Claude plan tier), and going live.
3. In Claude Code (or Cowork), run the `onboard` skill. It interviews you and fills in `brand/brand_config.json` and the brand docs.
4. Once `/onboard` reports the config is complete, run `/generate-batch` for the first week.

## Repo layout

```
plugin/                  the installable Cowork plugin (8 skills)
brand/                   placeholder brand docs — onboard fills these in; content-recipe.md and content-calendar.md also hold the quality-gate rules (content integrity, date alignment, production standards)
rules/                   channel-specific rulebooks (e.g. LinkedIn) — placeholder until performance data exists
automation/              n8n workflow template + Drive folder-ID template
src/                     Python export/render pipeline
samples/                 put 10-30+ real content samples here for voice-profile generation (Stage 2 of onboard)
outputs/                 generated batches land here
docs/                    the fork-to-production guide, plus the Python rendering pipeline reference
BRAND_VOICE_ALIGNMENT_GUIDE.md   deep reference for voice-profile generation, AI-giveaway detection, channel/compliance setup
COWORK_PROJECT_INSTRUCTIONS.md   paste into the Cowork Project's Instructions panel once onboarding is done
```

## What's deliberately not here

No client's brand data, no filled-in voice profile, no real outputs, no client-specific business documents. Every brand doc in this repo is a blank template with bracketed placeholders (`[ORG_NAME]`, `[PERSON_NAME]`, etc.) until `/onboard` fills them in for a real client.
