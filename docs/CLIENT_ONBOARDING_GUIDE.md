# Client Onboarding Guide: Fork to Production

This is the end-to-end walkthrough for standing up a new client on the content harness, from forking this template to a working weekly pipeline. It supersedes any per-client onboarding doc (e.g. Capable Wealth's ICCP guide) as the generic version of that process — read this once per new client, then produce a client-specific one-pager from it if the client wants their own copy.

## Phase 0: Pre-setup (before touching this repo)

Done via a client interview, ideally before Step 1 below:

- **Brand identity.** Who is the voice owner (or is this an institutional voice)? What's the organization, tagline, and mission?
- **Digital footprint audit.** What does this client already have — existing content archive, brand book, social accounts, prior analytics? This becomes `samples/` and informs the interview.
- **Channel intent.** Which channels does this client actually want to produce for, and at what frequency? Don't assume any prior client's mix.

This phase can happen in conversation before the repo even exists, or as the first part of the `/onboard` interview itself — the interview covers the same ground (Sections 1-3).

## Phase 1: Fork the repo

1. Create a new repo (or local folder) for this client from this template — `git clone`/fork, then remove the `.git` history and re-init if you want a clean history, or keep this template's history if you'd rather track the divergence.
2. Rename the plugin: edit `plugin/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — change `name` from `content-harness` to something client-specific (e.g. `acme-content`), and rewrite the `description` to name the real client instead of "a generic, client-agnostic content production harness."
3. Rename the top-level `README.md`'s title and intro to name the client.
4. Decide the dual-copy convention now, before it matters: this template ships skills only in `plugin/skills/`. If you'll also want local Claude Code dev-testing (not just a Cowork plugin install), copy `plugin/skills/` to `.claude/skills/` and keep the two in sync — bump the plugin version whenever either changes, or Cowork's plugin cache can serve stale skill content (this bit Capable Wealth once; see `plugin/skills/README.md`).

## Phase 2: Run onboarding

1. Open the project in Claude Code (or Cowork, if the infra from Phase 3 is already set up) and run the `onboard` skill.
2. Work through the interview. It's fine to do this over multiple sessions — Stage 1 (interview + config) doesn't block on anything except the client's answers.
3. If the client has existing content, place 10-30+ representative pieces in `samples/`, then ask `onboard` to run Stage 2 (full voice-profile generation). If no samples exist yet, note who will produce them and by when, and revisit Stage 2 later — `generate-batch` will still run in the meantime with a partial voice profile, just with less precision on tone.
4. Confirm `brand/brand_config.json` has no remaining bracketed placeholders and `channel_config.channels` has at least one active entry. This is exactly what `generate-batch`'s preflight check verifies before it will run.
5. If any active channel needs its own rulebook (e.g. LinkedIn), review `rules/*.md` — it starts as a placeholder structure; real rule content gets confirmed later via `retro` once performance data exists (see Phase 5).

## Phase 3: Infrastructure setup

This is separate from the brand/content configuration in Phase 2 — it's the plumbing that lets the pipeline actually run unattended.

### Claude plan tier

A Team-tier Claude subscription is the practical baseline for most clients: it includes the always-allow connector permissions needed for unattended scheduled runs, and headroom for a second seat (an assistant/VA reviewing output) later, even if only one person uses it on day one. Confirm the actual current Anthropic pricing and feature set before quoting a number to a client — do not reuse any figure from a prior client's guide, since pricing and plan features change.

### Google Drive

1. Create two folders in the client's Drive: a content root (where the client will review weekly batches) and a summary-sheets folder (a sibling, not nested — the n8n image workflow watches this one).
2. Record both folder IDs in `automation/drive_config.json`, replacing the `REPLACE_ME_*` placeholders.
3. Share both folders with whatever account will run the pipeline (a Cowork connector needs write access).

### n8n (image generation)

1. Stand up an n8n instance (self-hosted is cheapest — a small VPS is enough for this workflow's volume).
2. Import `automation/n8n-image-generation-workflow.json` and fill in its `REPLACE_ME_*` values: the summary-sheet folder ID (must match `drive_config.json` exactly), Drive credentials, an OpenAI (or other image-gen) API credential, and a Slack webhook/channel if you want completion notifications.
3. Confirm the workflow's Drive Trigger node watches the same `summary_sheets_folder_id` as `drive_config.json` — if these drift, the workflow silently never fires.

### Cowork project setup

1. Install the plugin (from its local folder path, or add this repo as a plugin marketplace source and install by name).
2. Link the Cowork Project to this client's working folder (must contain `brand/`, `rules/`, `src/`, `outputs/`).
3. Paste `COWORK_PROJECT_INSTRUCTIONS.md` (with its placeholders filled in from Phase 2) into the Project's Instructions panel.
4. Enable web search (needed by `research-scan`) and the Google Drive connector (needed by `generate-batch`'s publish step) in the Project's capabilities.

## Phase 4: First run

1. Run `/research-scan` for the first week, if the client's content touches any time-sensitive facts.
2. Run `/generate-batch week-1` (or whatever the client's first real week is). Confirm it passes its Step 0 preflight, produces the expected file count per active channel, and publishes to Drive correctly.
3. Have the client review the Drive folder — this is the one human-in-the-loop checkpoint in the whole pipeline. There's no separate approval tool; they review and post directly from what's in Drive.
4. Set up the Cowork Scheduled task (see `automation/weekly-pipeline.md` and `automation/crontab.example` for timing reference) once a manual run has been confirmed clean.

## Phase 5: Ongoing operation

- **Weekly:** `research-scan` → `generate-batch` → client reviews Drive → client posts.
- **After each revision the client requests:** log it to `brand/corrections-log.md` before applying the change (see `COWORK_PROJECT_INSTRUCTIONS.md`'s guardrail on this).
- **Weekly, after content work:** run `/retro`. Once a correction pattern recurs 3+ times, it proposes a brand-doc diff — including, eventually, real confirmed rules for any channel-specific rulebook that started as a placeholder (e.g. `rules/linkedin-content-creation-guidelines.md` Section 6).
- **As the voice profile matures:** if `brand/voice-profile.md` still has `PENDING` markers because samples arrived late, re-run `onboard`'s Stage 2 once they're in `samples/`.

## What's illustrative vs. load-bearing in this guide

The phase structure, the preflight/gating mechanism, and the Drive/n8n wiring are load-bearing — they're how the pipeline actually works. Any specific dollar figure, channel mix, or timing estimate mentioned above (or in any per-client guide derived from this one) is illustrative only — verify against current pricing and the actual client's configuration before treating it as fact.
