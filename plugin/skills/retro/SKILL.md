---
name: retro
description: Weekly recursive-learning pass. Reads the revision requests captured in brand/corrections-log.md, clusters them by rule-candidate, and once a preference has recurred 3 or more times proposes a diff to the relevant brand doc (voice-profile, content-recipe, or a channel-specific rules file) for the client's approval. Improves the source-of-truth the other skills read, so the system needs fewer corrections over time. Use weekly (e.g. "run the retro", "/retro"), after a week of content work, before the next batch.
---

# Retro: Weekly Recursive Learning Pass

This is the only skill that improves the **source-of-truth** itself. The others produce and gate content; `retro` makes the brand docs they read smarter by learning from the corrections the client made during the week.

It does this entirely from `brand/corrections-log.md`. It does **not** read the content drafts, invent preferences, or change any brand doc on its own. It clusters, counts, and proposes. The client approves.

## Input

None required. If given a date range, scope the pass to entries in that range; otherwise cover everything not yet marked `[PROMOTED]`.

## Load

- `brand/corrections-log.md`: the behavioral log (the only required input).
- `brand/voice-profile.md`, `brand/content-recipe.md`, any active channel's rulebook under `rules/`: the brand docs that learnings get proposed into, so a proposal lands in the right place and does not duplicate or contradict an existing rule.

## The pass

1. **Read and group.** Read every log entry not marked `[PROMOTED]`. Group them by **Rule candidate** (the underlying preference), not by verbatim request text.

2. **Drop one-offs.** Ignore entries marked `Scope: one-off` for promotion purposes (they are content requests, not preferences). Keep them in the log for the record.

3. **Count recurrences per candidate.**
   - **1 to 2 occurrences →** mark those entries `[WATCHING]`. Report them as patterns being watched. No proposal yet.
   - **3 or more occurrences →** mark those entries `[CONFIRMED]`. This candidate is eligible for a proposed brand-doc change.
   - **Explicit-rule fast path:** if any single entry's request explicitly states a general rule ("from now on, always X", "make this a rule"), treat that candidate as confirmed immediately, regardless of count, and note it was promoted by explicit instruction.

4. **Locate the right home for each confirmed candidate.** Decide which brand doc the rule belongs in:
   - Voice, tone, phrasing, banned language → `brand/voice-profile.md` (or `brand_config.json` language lists).
   - Content structure, templates, draft format → `brand/content-recipe.md`.
   - Channel-specific structure or hooks (e.g. LinkedIn) → that channel's file under `rules/`. This is also where a placeholder rulebook (e.g. a fresh `rules/linkedin-content-creation-guidelines.md` Section 6 still full of `[Rule N, pending performance data]` markers) gets filled in for real, once enough corrections/performance data exist to confirm a rule.
   - Cross-cutting production rules → `content-recipe.md` or `content-calendar.md`, whichever section they extend.
   Check the target doc first; if the rule already exists, note "reinforces existing rule" instead of proposing a duplicate. If a confirmed candidate **contradicts** an existing rule, flag the conflict for the client rather than silently overriding.

5. **Propose, do not apply.** For each confirmed candidate, produce a concrete **proposed diff**: the exact doc, the exact text to add or change, and a one-line rationale citing how many times and on which pieces it recurred. Present these as proposals. Do **not** edit any brand doc directly. Brand docs change only on the client's explicit approval.

6. **On approval.** When the client approves a proposal, apply that single diff to the named brand doc, then mark the contributing log entries `[PROMOTED]` (do not delete them). If declined, leave the entries `[CONFIRMED]` with a short note that it was declined, so they are not re-proposed identically next week.

## Output

A weekly retro report:

```
RETRO: week of <date range>

CONFIRMED (proposing changes):
1. <rule candidate>  (seen N times: <pieces>)
   → propose adding to <brand doc>:
     <exact proposed text / diff>
   rationale: <one line>

WATCHING (1-2 occurrences, no action yet):
- <rule candidate>  (seen N times)

ONE-OFFS this period (logged, not learned): <count>

CONFLICTS / NEEDS THE CLIENT'S CALL:
- <any confirmed candidate that contradicts an existing rule>
```

End by asking which proposals to apply. Apply only the approved ones, then update the log markers.

## What this skill does NOT do

- It does not read content drafts or judge content quality (that is `validate` / `voice-check`).
- It does not invent preferences that are not in the log.
- It does not change brand docs without the client's approval.
- It does not delete log history.
