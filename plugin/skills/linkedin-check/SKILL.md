---
name: linkedin-check
description: Run a LinkedIn post through this client's own performance-tested rulebook (rules/linkedin-content-creation-guidelines.md Section 6) and return pass/fail per item, line-level fixes, word count, and the opening rhetorical-device classification. Use when the user asks to check, score, or QA a LinkedIn post, or it is invoked inside generate-batch for each LinkedIn draft. Only relevant if LinkedIn is an active channel in this client's channel_config.
---

# LinkedIn Check

Gate a single LinkedIn post against this client's rulebook. **Capable Wealth's original version of this checklist was built from a real 50-post, 3-month performance analysis where a small fraction of posts drove most of the impressions — the difference was structural, not topical.** This client's rulebook won't have that kind of evidence yet on day one; `rules/linkedin-content-creation-guidelines.md` ships as a placeholder until `/retro` has enough real performance data to confirm which rules actually hold for this client. Until Section 6 of that file is populated with confirmed rules, report every numbered item as **"unconfirmed — no performance data yet"** rather than pretending a placeholder passes or fails.

## Input

A path to a `week-N-linkedin-*.md` draft, or pasted post text.

**Format branch:** If the file is a non-text LinkedIn format (e.g. a carousel or native-video brief), this is NOT a text post — skip the word-count and text-hook rules, check slide/clip structure instead, and label the output "non-text format — text-post rules N/A."

**Word-count method:** The post body is the prose between the final `---` separator and the hashtag line. Exclude the H1 title, any duplicated title line, metadata, the visual brief, hashtags, and the Quality Checklist. If no body is clearly delimited (e.g. pasted text), state your assumed span before counting.

**Trust nothing the draft asserts about itself.** Ignore the draft's embedded Quality Checklist `[x]` marks and re-derive every item.

## Load first

`rules/linkedin-content-creation-guidelines.md` (Section 6, the production checklist — this is the actual gate) and `brand_config.json` → `voice_and_tone.language_to_avoid`.

## Run every item in Section 6 of the client's rulebook

Read `rules/linkedin-content-creation-guidelines.md` fresh each time — do not rely on memory of any other client's rules. For each numbered item in that file's Section 6, check the post against it. If Section 6 still contains placeholder text (`[Rule N — pending performance data]`), report that item as unconfirmed rather than inventing a check for it.

Illustrative shape of what a confirmed rulebook's items tend to cover, once real data exists (do not apply these specific thresholds unless this client's own rulebook actually states them):
- A hook that establishes stakes in the opening sentence(s)
- A structural device that creates curiosity or a gap the reader wants closed
- A word-count range tuned to what performs for this client (not necessarily any other client's range)
- One idea per post vs. a deliberate multi-point format
- A close style (diagnostic question, soft CTA, hard CTA) matching this client's stated goals
- Voice conformance to `voice-profile.md`
- Hashtags specific to this client's actual niche, not a generic set

## Output

```
WORD COUNT: N words   (target: see rules/linkedin-content-creation-guidelines.md — PASS/OVER/UNDER/UNCONFIRMED)
OPENING DEVICE: <Provocative stat | Direct question | Scenario | Contrarian assertion | Anecdote lead | Simple declarative | If/when conditional>

RULE CHECK
✓ Rule 1  <item text from the client's rulebook>
✗ Rule 3  <item text> — <quote the offending line; explain what's missing>
? Rule N  Unconfirmed — no performance data yet, rulebook item still a placeholder
... (all items)

VERDICT: PASS (ready) | NEEDS FIXES (N) | RULEBOOK INCOMPLETE (cannot fully gate yet)
TOP FIXES (ranked):
1. <specific rewrite suggestion with example>
```

When invoked from generate-batch, also return the opening device so the batch can track within-week variation (no two LinkedIn posts the same week share a device). If pasted standalone, offer to apply the fixes if the user wants.
