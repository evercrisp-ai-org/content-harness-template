# Automation: scheduled weekly content pipeline

This folder holds the configuration for running the content pipeline on a schedule, so a week's drafts are generated automatically and waiting for [PERSON_NAME]'s review.

## What it does

On a schedule, set up through **Cowork's built-in Scheduled feature** (the "Scheduled" item in the Cowork sidebar), Claude runs the **weekly pipeline** end to end:

1. `research-scan` to refresh the upcoming week's plan for timeliness.
2. `generate-batch` to produce the full week of content (which internally runs the image-brief, linkedin-check, voice-check, and validate gates) and curates every channel's finished copy into Google Drive. Image generation happens separately, via the n8n workflow described below.
3. Writes drafts to `outputs/drafts/content-batch-{YYYY-MM-DD}/`, regenerates the Excel summary, and publishes cleaned copy for every piece, across every active channel (per brand_config.json's channel_config), into `<Week N>/<D-DDMMYYYY-DAY>/<Platform[-N]>/` in Google Drive.

The exact instruction the scheduled job runs is in [`weekly-pipeline.md`](weekly-pipeline.md). That file is written to be **fully self-determining**: an unattended run cannot answer clarifying questions, so the prompt resolves the target week, scope, and completeness on its own.

## Google Drive handoff, this is the pipeline's end state

Drive curation is the **entire** downstream pipeline: no approval platform, no Slack-based review, no publish workflow beyond the image-gen automation below. [PERSON_NAME] reviews and works directly from the Drive folder. `generate-batch`'s Step 7 publishes a cleaned (markdown-stripped) copy of every finished piece, across every active channel (per brand_config.json's channel_config), into a week-first folder tree. Folder IDs live in [`drive_config.json`](drive_config.json). Structure (revised 2026-07-27, replacing the LinkedIn-only date-first structure used 2026-07-24 through 2026-07-26):

```
<Content>/                             the root folder; no additional layer above the week folder
└── <Week N (date range)>/             one folder per batch, e.g. "Week 28 (Aug 31 - Sep 6, 2026)"
    ├── <D-DDMMYYYY-DAY>/              one folder per publish date; D = 1-5 for Mon-Fri
    │   ├── Blog/                      copy Doc + asset sit flat together here
    │   ├── Podcast/
    │   ├── Facebook/
    │   └── LinkedIn/
    ├── <D-DDMMYYYY-DAY>/              e.g. Friday
    │   ├── Facebook/
    │   ├── LinkedIn/                  native video
    │   └── LinkedIn-2/                carousel, distinct piece, same date, same platform
    └── {Week N checklist}             a Doc listing every piece with a link to its folder
```

Week precedes day precedes platform, and a piece's own copy and asset are never split into separate subfolders; a new platform folder only appears for a genuinely different piece of the same platform on the same date. The `D-` day-folder prefix exists purely so Drive's alphabetical sort shows the week's days in order (a bare `DDMMYYYY-DAY` string sorts Monday after Tuesday). Local `outputs/drafts/*.md` stays the authoritative, git-tracked source; the Drive copies are a cleaned export, not the source of truth. All 5 channels now publish to Drive (changed 2026-07-27; LinkedIn-only was the prior scope).

## Schedule

**4:00 AM Wednesday, local time.**

Cron expression: `0 4 * * 3`  (minute 0, hour 4, any day-of-month, any month, day-of-week 3 = Wednesday)

See [`crontab.example`](crontab.example).

### Why Wednesday 4 AM

The job generates **the upcoming week's** content. Running it early Wednesday means:

- The drafts are ready by Wednesday morning.
- [PERSON_NAME] has Wednesday through Friday to do his read-through and approve (the pipeline flags any Yellow items needing his eye; a clean run reports "No Yellow flags requiring [PERSON_NAME]'s review. Ready for his read-through before scheduling").
- Everything is approved and ready to publish the **following week**, where LinkedIn posts go out Tuesday / Wednesday / Thursday. That gives a comfortable approval buffer of about five days before the first publish.

> Set the timezone on whatever runs the cron. `0 4 * * 3` fires at 4 AM in the scheduler's local timezone. On macOS launchd or a server, confirm the TZ so it does not fire at 4 AM UTC by accident.

## Human-in-the-loop: this automates generation, not publishing

The scheduled job **generates drafts only.** It does not publish, schedule, or send anything. The two human dependencies stay in place:

- **Approval (R9):** drafts land in `outputs/drafts/`, never `outputs/final/`. [PERSON_NAME] reviews and approves before anything is scheduled.
- **Figure verification (R2):** any rate-sensitive figure the pipeline flags "verify before publish" must be checked by a person before publishing.

Automation removes the manual labor of *generating* the week. It deliberately does not remove the approval gate. See `../tech-pack/06-risk-assessment.md`.

## Runtime

This runs natively inside Cowork. Cowork has a built-in **Scheduled** feature (the "Scheduled" item in the left sidebar) that runs a task on a recurring schedule, so no external cron, headless CLI, or CI is needed. You create one Scheduled task that runs the [`weekly-pipeline.md`](weekly-pipeline.md) instruction inside this project.

The `0 4 * * 3` cron expression in [`crontab.example`](crontab.example) is kept only as a precise, copy-pasteable record of the intended timing (4 AM every Wednesday). The actual schedule is configured in the Cowork Scheduled UI, not in a crontab file.

## Setup

1. In Cowork, open **Scheduled** in the sidebar and create a new scheduled task **inside this project** (the [ORG_NAME] project), so it has access to the brand docs, skills, and `outputs/`.
2. Set the recurrence to **weekly, Wednesday, 4:00 AM** (your local timezone). This matches `0 4 * * 3`.
3. Use the contents of [`weekly-pipeline.md`](weekly-pipeline.md) as the task's instruction / prompt.
4. Before relying on the schedule, run `weekly-pipeline.md` once **manually** and confirm the output (full file set, no Red flags, drafts in the right folder).
5. Enable the schedule, then watch the first couple of automated runs against the outputs (file completeness, Yellow flags, elapsed time).

## n8n workflow status

The earlier Slack/Airtable review-and-publish hybrid workflows (`cw-c1.json`, `cw-c2.json`, `capable-wealth-scheduler.json`) targeted a Drive structure (`batches/Summary`, `batches/Summary Sheets`) that no longer exists; those files were deleted from this folder on 2026-07-26 rather than kept as historical reference.

There is one active n8n workflow today: [`n8n-image-generation-workflow.json`](n8n-image-generation-workflow.json), built 2026-07-26, which handles image generation separately from `generate-batch`. It watches a dedicated "summary sheet" Drive folder, resolves each piece's target folder from its Doc link, generates the image via OpenAI, uploads it into that same folder, and sends a Slack notification. See the file's own `meta._comment` for the node-by-node breakdown, and `generate-batch/SKILL.md` Step 7 for how the two pipelines hand off to each other.

## Monitoring

Because this runs in Cowork (not a metered API), monitor the **outputs**, not tokens: did the batch produce the full file set, did it finish without Red flags, and did it land in the drafts folder with a regenerated Excel summary. See `../tech-pack/05-time-study.md`.
