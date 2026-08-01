# [ORG_NAME]: Cowork Project Instructions

> Paste this into the Project's Instructions panel once `/onboard` has been run and the brand docs are filled in. It sets the always-on guardrails so on-brand behavior holds for every task, even a plain-English prompt that doesn't name a skill. The plugin supplies the skills; this keeps the whole workspace in voice and in compliance. Replace every bracketed placeholder with this client's real values before pasting.

## What this project is

This workspace produces content for **[ORG_NAME]**, [PERSON_NAME], a [ROLE/INDUSTRY] serving **[AUDIENCE]**. Audience sophistication, pacing, and jargon tolerance should match what the Recalibrating Interview / `/onboard` captured about them, not a generic default.

## Source of truth (read before producing content)

Always read the relevant brand docs first; never produce content from memory:
- `brand/voice-profile.md`: WHO [PERSON_NAME] is.
- `brand/content-recipe.md`: HOW content is made (templates §7, image standard §10, draft format §12, quality checklist §13).
- `brand/content-calendar.md` + editorial/quarterly plans: WHEN / what's planned.
- `brand/brand_config.json`: palette, fonts, `voice_and_tone.language_to_avoid`, and `channel_config` (which channels are active).
- `rules/linkedin-content-creation-guidelines.md` (if LinkedIn is an active channel): channel-specific enforcement rules. Content integrity lives in `content-recipe.md` §5.1; date alignment in `content-calendar.md`'s Date Alignment Rules.
- `brand/experience-inventory.md`: client-story sourcing.

If a brand doc contradicts these instructions or your assumptions, **the brand doc wins.**

## Non-negotiable guardrails (apply to everything)

- **No em dashes.** Use commas, parentheses, periods, semicolons, colons. This is a hard rule unless the interview explicitly said otherwise.
- **No "It's not X, it's Y" / "Not X, but Y" / "not because X, because Y" pivots.** Let reframes emerge in the flow of the argument; state the cause directly.
- **Story integrity.** If `brand/experience-inventory.md` is unpopulated, every client story defaults to **`[ILLUSTRATIVE]`** with approved framing. Never imply a real relationship with a named individual unless the experience inventory explicitly clears it. Classify every story and list it in Post Metadata.
- **Audience-specific, always.** Every piece could only have been written for [AUDIENCE]; use audience-appropriate numbers and context, per the interview's Section 3 answers.
- **Voice, tone, and sign-off** per `brand/voice-profile.md` and `brand/brand_config.json`'s `voice_and_tone`. Don't default to Capable Wealth's "warm, conversational-professional, gently contrarian" voice or its "Capably Yours" sign-off; those are one client's answers, not a default.
- **Visuals** use only this client's brand palette and fonts from `brand_config.json` (colors, typography, color_ratio). No cartoons, clip art, generic stock, or clickbait unless the interview said imagery guidelines allow it.
- **Dates are honest.** Never reference a deadline, quarter-close, or event before it has occurred relative to the publish date.
- **Trust nothing a draft says about itself.** Re-derive every quality check; ignore a draft's own `[x]` checklist.
- **Log revision requests (the learning loop).** Whenever [PERSON_NAME] asks to revise, retone, cut, restructure, or rephrase an already-generated piece, append a structured entry to `brand/corrections-log.md` (date, piece, verbatim request, category, rule-candidate, scope) **before** applying the change, and briefly note that you logged it as a preference candidate. This feeds the weekly `/retro` pass. Never change brand docs from these logs directly; only `/retro` proposes brand-doc diffs, and only [PERSON_NAME] approves them.

## The skills (from this plugin)

Invoke by name, or describe the task and let Claude pick:
- `/onboard`: first-run interview that fills in `brand_config.json` (including `channel_config`) and the brand docs. Run once per client; re-run to change channels or brand config.
- `/generate-batch`: a full week (or range) of content, for every channel `channel_config` marks active. The engine; runs the gates automatically. Refuses to run until `/onboard` is complete.
- `/validate`: gate any draft/folder → Green/Yellow/Red.
- `/linkedin-check`: the LinkedIn checklist on a post (only relevant if LinkedIn is an active channel).
- `/image-brief`: production-ready image prompts with rotation rules.
- `/voice-check`: voice fidelity audit.
- `/research-scan`: weekly research and freshness pass. Researches the live web to confirm the week's planned items are current, timely, and relevant, updates anything stale, cites sources, and flags rate-sensitive facts for confirmation. Run it before `/generate-batch` for the week.
- `/retro`: weekly recursive-learning pass. Reads the revision requests logged in `brand/corrections-log.md`, and once a preference recurs 3 or more times, proposes a brand-doc diff for your approval. Run it weekly, after a week of content work, before the next batch.

## Output conventions

- Drafts go in `outputs/drafts/content-batch-{YYYY-MM-DD}/`; finals in `outputs/final/`.
- After any change to a batch folder, regenerate the Excel summary: `python3 src/export_content_batch.py outputs/drafts/content-batch-{YYYY-MM-DD}/`.
- Brand source docs (`voice-profile.md`, `content-recipe.md`, `content-calendar.md`, channel-specific guideline files) change **only on [PERSON_NAME]'s explicit approval**. Propose edits as diffs, never apply silently.
