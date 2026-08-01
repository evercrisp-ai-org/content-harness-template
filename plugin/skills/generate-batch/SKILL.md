---
name: generate-batch
description: Produce a full week's content batch (whatever pieces are needed for every channel this client has marked active in brand_config.json's channel_config, e.g. blog, podcast, social posts, clips) from the client's editorial/quarterly plan. Loads all brand context, enforces every production rule during drafting, runs the quality gates, writes files with correct naming, exports the Excel summary, and curates every active channel's finished copy into <Week N>/<D-DDMMYYYY-DAY>/<Platform[-N]>/ in Google Drive for the client to review directly. Image generation runs separately via an n8n workflow (see automation/n8n-image-generation-workflow.json), not inline in this skill. Refuses to run until the onboard skill has filled in brand_config.json. Use when the user asks to generate, draft, or produce a content batch / a week of content (e.g. "generate-batch week-21", "draft week 22").
---

# Generate Batch

You are producing one week of [ORG_NAME] content for [PERSON_NAME] — per `brand/voice-profile.md` and `brand/content-recipe.md`. This is the engine skill. Everything you produce must sound like [PERSON_NAME] (or the org's institutional voice) and pass every brand rule. Nothing in this file about specific channels, formats, hashtags, or publish days is a hard default — it is illustrative until `/onboard` and the brand docs say otherwise for this client.

## Input

The user gives you a week (e.g. `week-21`, `21`, or a date) or a range of weeks. Optionally a theme override. If no week is given, ask which week, or infer the next un-produced week from the most recent folder in `outputs/drafts/`.

**A batch may span multiple weeks.** If the user names a range, produce each week in turn while maintaining **ONE running ledger across the whole batch**. The ledger is what makes cross-week rules enforceable; carry it through every drafting and image-brief step — the specific rules it tracks (banned opening templates, rhetorical-device rotation, image-type/color rotation, subject rotation) live in `content-recipe.md` and `.cursor/rules/content-production-batch.mdc`; read those before assuming any specific rotation rule.

## Step 0 — Onboarding preflight (always, before Step 1)

Read `brand/brand_config.json`. Stop and refuse to proceed, telling the user to run the `onboard` skill first, if any of the following is true:
- The file is missing, or `brand_name` / `tagline` still contains a bracketed placeholder token (e.g. `[ORG_NAME]`, `[TAGLINE]`).
- `channel_config.channels` is missing, empty, or every entry has `active: false`.

This is a config-completeness check, not a marker file — there is no separate "onboarded" flag to maintain. Once `brand_config.json` is genuinely filled in with a real channel list, this batch can run.

## Step 1 — Load context (always, before writing anything)

Read these in full. They are the single source of truth:

- `brand/voice-profile.md` — WHO the voice owner is. Study Structural DNA, Rhetorical Toolkit, Anti-Patterns. Apply every hard rule it states (e.g. em-dash bans, banned pivot constructions) exactly as written for this client — do not assume any other client's rules.
- `brand/content-recipe.md` — Content Architecture Templates (§7) for each active channel's format; the image standard (§10); Standard Draft File Format (§12); Quality Checklist (§13).
- The current quarter/editorial plan (whatever `brand/quarterly-plan-*.md` or `brand/editorial-plan.md` this client has) — the authoritative week → topic → channel → date mapping: theme, anchor angle, and any channel-specific hooks for this week. If the plan doesn't cover the requested week, ask the user before drafting rather than inventing a theme.
- `brand/content-calendar.md` — for timing/deadline alignment.
- `brand/brand_config.json` — palette, fonts, `voice_and_tone` (the banned-language list is nested at `voice_and_tone.language_to_avoid`), and `channel_config` (which channels are active and at what frequency).
- Any channel-specific rulebook under `rules/` (e.g. `rules/linkedin-content-creation-guidelines.md`) for every active channel that has one.
- `brand/experience-inventory.md` — read it. **If unpopulated, every client story defaults to `[ILLUSTRATIVE]` with approved framing — no real-client implications.**

Also load the enforcement rules in `.cursor/rules/` so you apply them as you write, not after.

## Step 2 — Resolve the week to dates

Map the week number to its Monday-start date range and publication dates (from the plan). **Week numbers are an internal sequential index, not ISO week numbers**, unless the client's plan says otherwise. Record the resolved range in each file's `Week:` metadata. Confirm no piece will reference an event, deadline, or quarter-close that hasn't occurred by its publish date (date-alignment rule). Publish-day assignments per channel (which weekday each channel's pieces land on) come from `brand/content-recipe.md` / the client's stated cadence, not from any example in this file.

## Step 3 — Produce one batch of pieces per active channel, per week

Read `brand/brand_config.json`'s `channel_config.channels` and produce `posts_per_week` pieces for every channel marked `active: true` — no more, no less. Skip any channel marked `active: false` entirely; do not produce placeholder or "coming soon" content for it. **This repo ships with zero channels active by default** — `/onboard` populates the real list per client, and this step reads whatever that list says. Do not assume any particular channel mix (blog + podcast + LinkedIn + Facebook + clips is one example configuration, not a default).

For each active channel, name files `week-N-{channel}-{slug}.md` (or `week-N-{channel}-1..K.md` for a channel with multiple pieces per week) and produce the format `brand/content-recipe.md`'s Content Architecture Templates (§7) define for that channel. If an active channel has no existing template in §7 (e.g. the client added a channel `/onboard` didn't have a template for yet), the `onboard` skill should already have drafted one — if it hasn't, stop and flag this rather than inventing a format on the spot.

**Non-negotiable: every week gets its full set of pieces across every active channel, regardless of "primary channel."** A "primary channel" designation in the plan sets *emphasis* only — which piece leads the week and gets the most promotion. It NEVER drops an active channel from the batch. Any channel whose count is described as variable in `content-recipe.md` (e.g. "2-5 clips, by natural standalone value") flexes only within that stated range, never below its floor and never forced to its ceiling.

Every file follows the Standard Draft File Format (recipe §12):

1. **Title** (H1)
2. **Post Metadata** — `Type`, `Week` (resolved date range), `Theme`, plan reference (cite the source exactly), `Strategic context`, and `Story classifications used`.
3. **Visual Assets** — image brief(s), delegated to Step 5.
4. **Clip Extraction Map** — for any channel whose format includes clip extraction (e.g. a podcast/video format), per `content-recipe.md`.
5. **Content**.
6. **Quality Checklist** (recipe §13) — and any conditional sections that channel's format requires (e.g. a Short-Form Clips checklist for video, a channel-specific guideline checklist for any channel with a `rules/` file). Write the resolved **Relevance Score (Green/Yellow/Red)** into the Relevance Validation section of every file.

## Step 4 — Enforce these while drafting (not after)

- **Channel-specific rulebooks:** for every active channel with a file under `rules/` (e.g. LinkedIn), every post in that channel obeys every rule in that file — read it fresh each batch, don't rely on memory of a prior client's rules.
- **Opening-line variation:** no rhetorical device repeats on the same channel in the same week; banned opening templates are whatever `content-recipe.md` / the corrections log has flagged for this client, not a fixed list. Track all of this in the running ledger.
- **Image-type rotation:** per `content-recipe.md` §10 and the batch rule in `.cursor/rules/`. Do not hand-write the prompts here — Step 5 delegates them.
- **Integrity:** classify every story `[REAL-ANONYMIZED]` / `[ILLUSTRATIVE]` / `[GENERAL-PRINCIPLE]` and list them in Post Metadata. Inventory unpopulated → all `[ILLUSTRATIVE]`.
- **Voice:** apply every hard rule in `voice-profile.md` and `brand_config.json`'s `voice_and_tone.language_to_avoid` — these are this client's specific rules, not a universal default.

## Step 5 — Run the gates (delegate to the other skills)

Apply these to the produced content before finalizing:
1. **image-brief** — generate the image prompt(s) for every asset, with batch-wide rotation awareness.
2. **linkedin-check** (or the equivalent channel-check skill for whichever channel has a `rules/` file) — run the checklist on each post in that channel; fix any failure before finalizing.
3. **voice-check** — run on **EVERY produced piece across every active channel**. This is the brand-wide voice gate. It must catch every anti-pattern `voice-profile.md` lists for this client. Fix every flagged line before finalizing. **This gate is mandatory and blocking. If voice-check has not actually been run on a piece, that piece is not finished — the batch is incomplete.** Never skip it because a draft "looks clean," because you are short on time, or because you fanned out other work.
4. **validate** — run content-integrity + date-alignment + relevance on every piece; only `Green` (or justified `Yellow`) proceeds. Record the result in each file's Quality Checklist.

**Check the literal text, not your memory.** Before finalizing each file, actually search its body for whatever this client's voice-profile bans (e.g. em dash `—`, en dash `–`, horizontal bar `―`, banned pivot constructions). Any hit is a defect to fix, not to wave through. The Quality Checklist you write must reflect this real re-derivation: never mark a rule "PASS" on a body that still violates it.

If you have the Agent tool available, you may fan these out in parallel (one agent per piece) for speed. Otherwise run them inline.

## Step 6 — Write, export, generate images

0. **Final banned-pattern sweep (BLOCKING, do this before writing anything).** For every file about to be written, literally scan the full text for whatever `voice-profile.md` bans for this client. If any file contains a violation, it is not done: fix it, then re-run `voice-check` on that file. Also confirm `voice-check` actually ran on every piece in Step 5; if it did not run on even one, run it now before proceeding. This sweep is the last line of defense and is not optional.
1. Write all files to `outputs/drafts/content-batch-{YYYY-MM-DD}/`, dated to the **batch's first week's Monday**. All weeks in a multi-week batch go in the SAME folder — do not fragment weeks into separate folders.
2. **Completeness check (before reporting done):** for every week in the batch, confirm on disk that every active channel's mandatory files exist at its configured `posts_per_week` count. If any week is short, produce the missing pieces now. Report the per-week file counts so a shortfall is visible.
3. Regenerate the Excel summary: `python3 src/export_content_batch.py outputs/drafts/content-batch-{YYYY-MM-DD}/`. This produces `content-batch-summary-{YYYYMMDD}.xlsx` in that folder. It is the primary handoff artifact and must always match the markdown — re-run it after ANY later edit to any draft.
4. **Image generation no longer runs here.** Images are produced by a separate n8n workflow (`automation/n8n-image-generation-workflow.json`), triggered when this batch's summary sheet lands in the Drive summary-sheets folder. See Step 7 for how this skill places that sheet itself. Do not call `src/image_gen.py` as part of this step.
5. Print the run summary in chat: week number, theme, file count by channel, any `Yellow` flags that need review, and the folder path.

## Step 7 — Publish to Google Drive

`outputs/drafts/*.md` is the authoritative, git-tracked source and is never altered by this step: full markdown, metadata, and Quality Checklist stay intact locally. This step publishes a **separate, cleaned-up copy** of every finished piece, across every active channel, into a structured Drive tree organized by week, then day, then platform. **This is the pipeline's end state**: there is no downstream approval tool. The client reviews and works directly from this Drive folder. If the Google Drive connector is not connected, skip this step and say so in the run summary; do not treat it as a batch failure.

**Scope: every channel marked active in `channel_config`.** A client with 2 active channels publishes 2 platform folders per applicable day; a client with 5 publishes 5. Nothing here assumes a specific count.

Folder structure (root ID in `automation/drive_config.json`, key `content_root_folder_id`):
```
<Content>/                                    <- the root folder; no additional layer above the week folder
└── <Week N (date range)>/                    <- one folder per batch, e.g. "Week 28 (Aug 31 - Sep 6, 2026)"
    ├── <D-DDMMYYYY-DAY>/                     <- one folder per publish date; D = 1-5 for Mon-Fri
    │   ├── {Channel}/                        <- platform folder; copy Doc + asset(s) sit flat together here
    │   │   ├── {cleaned Google Doc}
    │   │   └── {image file(s)}
    │   └── {Channel}/
    └── {Week N checklist}                    <- a Doc listing every piece with a link to its folder
```

**Week precedes day precedes platform**, and a piece's copy and its own asset are never split into separate subfolders; they sit together, flat, in one folder. The `D-` prefix on each day folder (1 for Monday through 5 for Friday) exists purely so Drive's alphabetical sort shows the week's days in the right order; without it, `DDMMYYYY-DAY` alone sorts wrong (Monday's date string sorts after Tuesday's). The week folder reuses the exact `Week N (date range)` label already in every piece's own metadata, so it stays consistent with what the client already sees on each piece, rather than introducing a separate ISO week number.

A new platform folder is created (with a `-2`, `-3`, ... suffix) only when a later, distinct piece of the SAME platform lands on the same date. Different platforms landing on the same date never collide with each other; each always gets its own folder.

**Publish-day assignment is client-specific**, defined in `brand/content-recipe.md` / the client's stated cadence from onboarding, not hardcoded here. `src/export_content_batch.py`'s `resolve_publish_date_and_order` function currently has example logic for a channel mix like Blog/Podcast/LinkedIn/Facebook/Clips — adjust it for this client's actual active channels and their stated publish days rather than assuming that example applies.

1. Get the publish plan for every piece in the batch, across every active channel, in one call:
   ```
   python3 src/export_content_batch.py --drive-plan outputs/drafts/content-batch-{date}/
   ```
   This returns JSON: one entry per piece with `source_file`, `title`, `platform`, `publish_date`, `drive_week_folder`, `drive_date_folder`, and `drive_platform_folder` (the platform name, or `Platform-2`/`Platform-3` if a later piece of that same platform collides with an earlier one on the same date). There is no local `assets` path to check; images arrive later via the separate n8n workflow (see step 4 below).
2. Ensure the folder chain exists, creating only what's missing (search first, then create only if the search finds nothing): the `drive_week_folder` directly under `content_root_folder_id`; then, for each distinct `drive_date_folder` in the plan, that day folder under the week folder; then, for each piece, its `drive_platform_folder` under that day folder. Do not create any intermediate folders beyond week, day, and platform.
3. For each piece in the plan: get its clean Doc-ready text and create the Doc directly in that piece's platform folder:
   ```
   python3 src/export_content_batch.py --clean-for-drive outputs/drafts/content-batch-{date}/{source_file}
   ```
   This strips markdown syntax but leaves the prose and compliance tags (`[ILLUSTRATIVE]`, etc.) untouched; those are content, not markup. Pass the output as `textContent` to Drive `create_file` (`contentMimeType: text/plain`, `parentId` = that piece's platform folder ID, `title` = the piece's title).
4. **Do not upload an image here.** Image generation and placement happen asynchronously via the separate n8n workflow (`automation/n8n-image-generation-workflow.json`), triggered by the summary sheet this skill places in step 5 below. Do not call `src/image_gen.py` or upload any image file as part of this step.
5. **Place the summary sheet to trigger image generation.** Once every piece's Doc has been created (step 3):
   - Build a `url_map` (a JSON object of `{source_file: doc_url}`) from the Doc URLs step 3 just returned, and write it to a temp file.
   - Get the summary sheet's CSV content:
     ```
     python3 src/export_content_batch.py --drive-summary-csv outputs/drafts/content-batch-{date}/ <url_map.json>
     ```
     This produces one row per image prompt (a piece with multiple images gets one row per image, all sharing that piece's Doc URL). A piece with no image prompt is skipped.
   - Upload this CSV as a native Google Sheet directly into the `summary_sheets_folder_id` folder from `automation/drive_config.json` (a fixed sibling of the content root, not nested under it). Use Drive `create_file` with `contentMimeType: 'text/csv'`, `parentId` = `summary_sheets_folder_id`, `title` = the week folder's name, and leave `disableConversionToGoogleType` unset or false so Drive auto-converts it to a native Sheet (a raw CSV blob will not trigger the n8n workflow). **Pass the CSV as `textContent`, never `base64Content`** — base64 has been unreliable through this pipe.
   - Placing this file is what fires the n8n workflow's Drive Trigger; from here, image generation and placement into each piece's platform folder happen on their own, outside this skill.
6. **Create the week checklist Doc.** Once every piece's Doc exists, create one plain-text Doc directly in the week folder, listing every piece in publish order: day, platform, title, and a link to its folder. This is the single starting point for the client's weekly review; build it last, after every folder and link actually exists.
7. Note in the run summary, per piece: which week, day, and platform folder it landed in, whether the Doc uploaded, whether the summary sheet was placed, and the Drive link. Images are not expected to be present yet at this point in the run; they arrive once the n8n workflow processes the summary sheet.

## Output

End with a concise report: week, theme, files created (by channel), validation results (Green/Yellow/Red counts), any rule conflicts you had to resolve, whether Drive publishing ran (and which pieces are missing an asset), and the next action for the client (open the week folder's checklist Doc in Drive). Do not dump full file contents into chat; they are on disk.
