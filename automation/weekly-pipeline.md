# Weekly pipeline instruction (for the scheduled job)

This is the instruction the scheduled job runs unattended. It is written to be fully self-determining: do not ask clarifying questions, resolve every decision from the repo and these rules, and if something is genuinely ambiguous, make the conservative choice and note it in the run summary rather than stopping.

---

You are running the automated weekly content pipeline for [ORG_NAME]. Follow the project's always-on guardrails (see `COWORK_PROJECT_INSTRUCTIONS.md`) for everything you produce.

## Step 1: Determine the target week

- The target is the **next un-produced upcoming week** so that its content is ready to publish the following week.
- Infer it from the most recent `outputs/drafts/content-batch-*` folder: the target week is the next sequential week after the latest produced one.
- If that inference is ambiguous, choose the earliest upcoming week that has no draft folder, and state the week number and date range you chose in the run summary.
- Produce **one week** unless this instruction has been edited to specify a multi-week range.

## Step 2: Refresh the plan

Run `research-scan` for the target week. This researches the live web to confirm the week's already-scheduled items are current, timely, and relevant (tax figures, limits, law changes, current events), updates anything stale, and cites its sources. Carry every "confirm before publish" flag it raises into the final summary so a human verifies rate-sensitive facts before publishing.

## Step 3: Generate the batch

Run `generate-batch` for the target week. This produces the full mandatory set (blog, podcast script, 3 LinkedIn posts, 5 Facebook posts, 2 to 5 clips, plus the optional native video and carousel) and runs the gates (image-brief, linkedin-check, voice-check, validate) during the run. Apply all production rules and the running ledger.

## Step 4: Verify completeness and integrity

- Confirm on disk that every mandatory file exists for the target week with correct naming. If any are missing, produce them now.
- Run the literal scans: zero em-dash characters, zero "not ... but" / "not ... it's" pivot constructions in any file.
- Confirm every story is classified and listed in Post Metadata.

## Step 5: Export and curate to Drive

- Regenerate the Excel summary: `python3 src/export_content_batch.py outputs/drafts/content-batch-{YYYY-MM-DD}/`.
- Publish to Google Drive (generate-batch Step 7): for every piece, across every active channel (per brand_config.json's channel_config), cleaned copy flat in `<Week N>/<D-DDMMYYYY-DAY>/<Platform[-N]>/` under the `capable_wealth_content_root_folder_id` root. Skip and note it if the Drive connector isn't connected; this is not a run failure. Image generation is not part of this step; it runs separately via the n8n workflow described in `automation/README.md`.
- Print the run summary in chat: target week and date range, theme, file count by channel, validation results (Green / Yellow / Red counts), any "verify before publish" figure flags, whether Drive publishing ran, and the week folder path.

## Step 6: Stop. Do not publish.

- Leave all output in `outputs/drafts/`. Do **not** move anything to `outputs/final/`, do not schedule, and do not publish.
- The run ends here. [PERSON_NAME] reviews and approves before anything is scheduled.

## Hard rules for the unattended run

- Never invent or "freshen" a rate, contribution limit, or legal figure. Flag it for human verification instead.
- Never imply a real client relationship; all stories default to `[ILLUSTRATIVE]` with approved framing.
- Never reference a deadline, quarter-close, or event before it has occurred relative to the publish date.
- If you cannot complete a step, write what failed and why in the run summary so a human can pick it up. Do not silently skip it.
