# Content Harness Skills

This folder is the plugin's skill source. Each subfolder is one skill (`SKILL.md`), invokable in Claude Code / Cowork by name.

For local dev-testing outside a Cowork plugin install, symlink or copy this folder to `.claude/skills/` in whatever project you're working in, and keep the two in sync — Capable Wealth's own deployment hit a real bug where a Cowork plugin cache served stale skill content after the two copies drifted out of sync. Bump the plugin version (`plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`) whenever skill content changes, to force Cowork's plugin cache to refresh.

## The eight skills

| Skill | Role | Trigger |
|-------|------|---------|
| `onboard` | **First-run setup.** Interviews the voice owner/stakeholder (org, voice, audience, channels + frequency, visual brand, compliance, key dates, language rules) and writes the answers into `brand_config.json` and the brand docs, including `channel_config` — which channels `generate-batch` produces for. Voice-profile completion runs as a second stage once sample content exists in `samples/`. | Once per client; re-run to change channels/config |
| `generate-batch` | **The engine.** Produces a full week (or multi-week range) of content for every channel `channel_config` marks active, enforces every production rule while drafting, runs the gates, writes files, exports the Excel summary, and publishes every active channel's cleaned copy into Google Drive for review. Refuses to run until `onboard` has filled in `brand_config.json`. | Weekly |
| `validate` | 3-rule gate (integrity + date alignment + relevance) → Green/Yellow/Red per piece + the §13 checklist. | Auto inside generate-batch; or on demand |
| `linkedin-check` | Runs this client's own LinkedIn rulebook (`rules/linkedin-content-creation-guidelines.md` Section 6) against a post; pass/fail, fixes, word count, opening device. Only relevant if LinkedIn is active. | Auto inside generate-batch; or on demand |
| `image-brief` | Production-ready image prompts with dimensions (from `brand_config.json`), palette, and batch rotation rules. | Auto inside generate-batch; or on demand |
| `voice-check` | Voice fidelity audit against `brand/voice-profile.md` (Voice Alignment / Audience Specificity / Pull Signal). | On demand |
| `research-scan` | Weekly research + freshness pass. Researches the live web to verify the week's planned items are current and timely, updates stale items, cites sources, flags rate-sensitive facts. Needs web access enabled. | Before generating a week's batch |
| `retro` | Recursive learning pass: clusters the revision requests logged in `brand/corrections-log.md`; once a preference recurs 3+ times, proposes a brand-doc diff for the client's approval. The only skill that improves the source-of-truth itself. | Weekly, after content work |

## How they connect

```
ONCE, PER CLIENT      EACH WEEK            WEEKLY ENGINE                    ON DEMAND
onboard          →    research-scan   →    generate-batch              →    validate
  sets channel_config,  refreshes that      ├─ image-brief (every asset)   linkedin-check
  voice, brand, etc.    week's planned      ├─ linkedin-check (if active)  image-brief
                        items for           ├─ voice-check (all pieces)    voice-check
                        timeliness          ├─ validate (gates batch)
                                            └─ publish to Drive
                                                    │
                                                    ▼
                                          Client reviews the Drive folder & posts
```

Running alongside this, the recursive learning loop closes over time: every revision the client prompts during a week is logged to `brand/corrections-log.md`, and the weekly `retro` skill turns recurring corrections into proposed brand-doc improvements (3+ recurrences, client approves).

## What each skill reads (source of truth)

The skills are prompt-native: they read the brand docs directly rather than duplicating them, so updating a brand doc updates every skill.

- `brand/voice-profile.md`, `brand/content-recipe.md` (§5.1 Content Integrity, §7 channel templates, §12/§13 production standards), `brand/content-calendar.md` (timing + Date Alignment Rules), the client's editorial/quarterly plans
- `brand/brand_config.json` (palette, fonts, `voice_and_tone.language_to_avoid`, `channel_config`)
- `rules/*.md` (any channel-specific rulebook this client has)
- `brand/experience-inventory.md` (unpopulated → all stories default to `[ILLUSTRATIVE]`)
