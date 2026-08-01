# Content Harness Template

A content production system for Claude Code and Claude Cowork. It captures a client's brand voice, generates content across whatever channels they use, gates everything through quality checks before it publishes, and gets better over time by learning from the corrections a client actually makes.

This repo ships with zero clients configured. Fork it, run the `onboard` skill, and you have a working weekly content pipeline for whatever channels that client wants, whether that's one channel or ten.

## What's in here

- **Eight Claude Code skills** (`plugin/skills/`). `onboard` runs the first interview. `generate-batch` is the weekly engine. The rest (`validate`, `linkedin-check`, `image-brief`, `voice-check`, `research-scan`, `retro`) gate quality, check facts, and feed corrections back into the system.
- **Brand docs** (`brand/`), still blank: a voice profile, a content recipe, a content calendar, and `brand_config.json` (colors, fonts, tone, compliance, and `channel_config`, which channels are active and how often). `onboard` fills these in through a conversation.
- **A Python export pipeline** (`src/`): Excel batch summaries, Google Drive publish plans, and PDF/image rendering, all driven by `brand_config.json` instead of hardcoded to any one client.
- **Automation templates** (`automation/`): an n8n image-generation workflow and a Drive folder-ID config, both left as `REPLACE_ME_` placeholders until a client is set up.
- **Quality gates**, folded into `brand/content-recipe.md` (§5.1) and `brand/content-calendar.md`'s Date Alignment Rules. `generate-batch` applies both automatically.

## Getting a new client running

1. Fork or clone this repo into its own folder or repo for that client.
2. Read `docs/CLIENT_ONBOARDING_GUIDE.md`. It covers renaming the plugin, running `/onboard`, setting up Drive and n8n, and going live.
3. In Claude Code or Cowork, run the `onboard` skill. It interviews you and fills in `brand/brand_config.json` and the brand docs.
4. Once `/onboard` reports the config is complete, run `/generate-batch` for the first week.

## Repo layout

```
plugin/                  the installable Cowork plugin (8 skills)
brand/                   placeholder brand docs, filled in by onboard; content-recipe.md and
                         content-calendar.md also hold the quality-gate rules
rules/                   channel-specific rulebooks (LinkedIn, etc.), placeholder until real
                         performance data exists
automation/              n8n workflow template and Drive folder-ID template
src/                     Python export and render pipeline
samples/                 put 10-30 real content samples here for voice-profile generation
outputs/                 generated batches land here
docs/                    the fork-to-production guide, plus the Python pipeline reference
BRAND_VOICE_ALIGNMENT_GUIDE.md   deep reference for voice profiles, AI-giveaway detection, channels, compliance
COWORK_PROJECT_INSTRUCTIONS.md   paste into the Cowork Project's Instructions panel once onboarding is done
```

## What's deliberately not here

No client's brand data, no filled-in voice profile, no real output, nothing client-specific. Every brand doc is a blank template with bracketed placeholders (`[ORG_NAME]`, `[PERSON_NAME]`, and so on) until `/onboard` fills them in for a real client.
