---
name: validate
description: Gate a content draft (or a whole batch folder) through all three enforcement rules at once (content integrity, date alignment, and relevance) and return a per-piece verdict of Green / Yellow / Red plus the full Quality Checklist. Use when the user asks to validate, check, gate, QA, or review a draft / batch for compliance before publishing.
---

# Validate

Run a draft (or every `.md` draft in a batch folder) through this client's three enforcement rules simultaneously and return a gated verdict. This is the final quality gate before content publishes.

## Input

A path to a draft file, a path to a `content-batch-*` folder (validate every piece), or pasted content. If given a folder, validate each file and produce a summary table at the end.

## Load first

- `brand/content-recipe.md` §5.1 (Content Integrity Filter)
- `brand/content-recipe.md` §5 (Research & Relevance Filter, the Green/Yellow/Red definitions) and §13 (Quality Checklist)
- `brand/content-calendar.md` (deadlines). For the week to date mapping, use the draft's own Post Metadata `Week:` field as the publish window of record. **Week numbers are an internal sequential index, not ISO week numbers; never infer a date from a standard-calendar week number.**
- `brand/experience-inventory.md` (to trace `[REAL-ANONYMIZED]` claims; if unpopulated, any real-client framing is a fail)

**Trust nothing the draft asserts about itself.** Ignore the draft's embedded Quality Checklist `[x]` marks and re-derive every item independently.

## Three checks per piece

### 1. Content Integrity (→ Clean / Flagged / Blocked)
- Is every client story classified `[REAL-ANONYMIZED]`, `[ILLUSTRATIVE]`, or `[GENERAL-PRINCIPLE]`, and listed in Post Metadata?
- Do `[REAL-ANONYMIZED]` stories trace to a specific entry in `experience-inventory.md`? (Unpopulated inventory → must be `[ILLUSTRATIVE]`.)
- **Read the actual body prose against the client's banned-framing list (from `brand_config.json`'s `voice_and_tone` and the onboarding interview's Section 7 compliance answers). A correct `[ILLUSTRATIVE]` tag in metadata does NOT excuse real-relationship language in the text.** Fabricated real-client phrasing, a direct quote attributed to a real client, or a specific temporal reference implying a real interaction are violations regardless of the tag.
- Do `[ILLUSTRATIVE]` examples use this client's approved framing (from `content-recipe.md`)?
- Any fabricated temporal references, relationship-duration claims, experience-pattern claims, implied guarantees, or testimonial framing? Quote the offending line.

**Flagged vs. Blocked:** Mark **Blocked** (→ RED) when the prose fabricates a real client interaction, names/quotes an implied real person, or makes an experience-pattern claim the unpopulated inventory cannot support. Mark **Flagged** (→ YELLOW) when framing merely needs softening but no fabricated relationship is asserted.

### 2. Date Alignment (pass / fail)
- Does any title/body claim a period has closed before its actual close date, per this client's fiscal year / key-date answers in `content-calendar.md`?
- Are deadline references accurate for the publish week? Any post-event framing used before the event?
- Cross-reference the piece's publish date from the client's plan.

### 3. Relevance (→ Green / Yellow / Red)
- Are all facts, figures, rates, and any regulated claims current as of the publish date? **If a rate/limit/legal fact cannot be verified from the repo, mark Relevance=Yellow and flag the specific figure for manual verification before publish. Never mark Green on an unverifiable rate-sensitive figure, even if the draft's own checklist says Green.**
- Is the timing right vs. this client's annual calendar (per `content-calendar.md`'s seasonal cycles and key dates)?
- Any conflicting current event that would make it tone-deaf?

## Output per piece

Lead every status and the verdict with its color emoji: 🟢 = green/clean/pass, 🟡 = yellow/flagged, 🔴 = red/blocked/fail. (Date has no middle state: 🟢 Pass or 🔴 Fail only.) Use these exact emojis every time so a result is scannable at a glance.

```
FILE: week-N-{channel}-1.md
Integrity:  🟢 Clean | 🟡 Flagged | 🔴 Blocked   : <one line; quote any offending text>
Date:       🟢 Pass | 🔴 Fail                    : <one line>
Relevance:  🟢 Green | 🟡 Yellow | 🔴 Red          : <one line>
VERDICT:    🟢 GREEN (publish) | 🟡 YELLOW (revise: <what>) | 🔴 RED (hold: <why>)
```

(Show only the one status that applies on each line, with its emoji, not the full menu.)

Then render the full §13 Quality Checklist (Voice Alignment, Audience Specificity, Relevance Validation, Pull Signal Design, Visual Assets, Content Integrity, plus any conditional sections this piece's channel requires) with each item checked or flagged. For any channel with its own rulebook under `rules/` (e.g. LinkedIn), additionally run that file's production checklist.

A piece is **🟢 GREEN** only if Integrity=Clean, Date=Pass, Relevance=Green. Any Blocked or Fail → **🔴 RED**. Otherwise **🟡 YELLOW** with the specific fix. For a folder, end with a summary table (file | verdict | top issue) with each verdict cell led by its 🟢/🟡/🔴 emoji.

Do not edit the files, report only, unless the user explicitly asks you to fix.
