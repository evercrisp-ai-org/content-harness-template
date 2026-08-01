# Content Calendar: [ORG_NAME]

> This document defines WHEN content should publish. It captures the static annual cycles, dynamic research checkpoints, and signal-driven triggers that determine content timing and relevance.

**Companion documents:**
- [voice-profile.md](voice-profile.md): WHO
- [content-recipe.md](content-recipe.md): HOW
- [brand_config.json](brand_config.json): LOOK + TONE

---

## Layer 1: Static Annual Cycles

These are predictable, recurring events that affect [AUDIENCE]. Content should align with these cycles.

### Quarterly Rhythm

| Quarter | Key Events / Deadlines | Content Themes |
|---------|----------------------|----------------|
| Q1 (Jan-Mar) | [KEY_DEADLINE_1], [Events] | [Themes appropriate for this period] |
| Q2 (Apr-Jun) | [KEY_DEADLINE_2], [Events] | [Themes appropriate for this period] |
| Q3 (Jul-Sep) | [Events, mid-year milestones] | [Themes appropriate for this period] |
| Q4 (Oct-Dec) | [Year-end deadlines, planning season] | [Themes appropriate for this period] |

### Key Dates

| Date / Period | What Happens | Content Planning Window |
|---------------|-------------|------------------------|
| [Date 1] | [Event/deadline] | [When to publish content about this] |
| [Date 2] | [Event/deadline] | [When to publish content about this] |
| [Date 3] | [Event/deadline] | [When to publish content about this] |
| [Date 4] | [Event/deadline] | [When to publish content about this] |

### Seasonal Patterns

[Describe seasonal patterns that affect your audience. Examples:]
- [Season 1]: [What happens for AUDIENCE and what content to produce]
- [Season 2]: [What happens]
- [Season 3]: [What happens]

### Date Alignment Rules

Content must be temporally honest: it must never reference an event, deadline, or period as having occurred if the publication week predates it. `validate` and `generate-batch` enforce this on every piece.

**Fiscal quarter boundaries** (replace with this client's actual fiscal year if not calendar-year):
- Q1 closes March 31
- Q2 closes June 30
- Q3 closes September 30
- Q4 closes December 31

Never reference quarterly data as "in," "available," or "complete" before the quarter closes. Use forward-looking framing: "as Q[N] wraps up," "before Q[N] closes."

**Date-sensitive content rules:**
1. Deadline-referenced content should publish 2-4 weeks before the deadline.
2. Post-deadline content (e.g. "the window just opened") must not publish before the deadline date.
3. Quarterly review content (e.g. "your Q[N] numbers are in") must not publish before the quarter has closed.
4. Event-timed content should align with actual event dates.

**When dates shift:** if publication dates are adjusted, audit every content piece in the affected range for titles/body text that reference specific timing, and Quality Checklist entries referencing specific date ranges.

**Validation checklist** (part of every piece's Quality Checklist, per `content-recipe.md` §13):
- [ ] No claims that a period has closed before its actual close date
- [ ] No references to deadlines as "next week" unless publication is actually the week before
- [ ] No post-event framing used before the event has occurred
- [ ] Forward-looking framing used for events that fall after the publication week
- [ ] All "this week" and "next week" references are accurate for the publication date range

---

## Layer 2: Dynamic Research Checkpoints

Monthly research scans to catch changes that affect content relevance.

### Monthly Scan Checklist

Run this checklist at the start of each month, or by invoking the `research-scan` skill:

- [ ] Industry developments affecting [AUDIENCE]
- [ ] Regulatory or legislative changes
- [ ] Economic conditions relevant to [AUDIENCE]
- [ ] Market events or trends
- [ ] Industry news, conferences, or publications
- [ ] Competitor content or thought leadership shifts

### Scan Output Format

```
## Research Scan: [Month Year]

### What Changed
- [Finding 1] (Source: [link or reference])
- [Finding 2] (Source: [link or reference])

### Content Impact
- [Existing content affected]: [Recommended action]
- [New content opportunity]: [Brief description]

### Recommended Actions
- [Action 1]
- [Action 2]
```

---

## Layer 3: Signal-Driven Triggers

Events that cannot be predicted but require immediate content response or adjustment.

### Trigger Types

| Trigger | Response | Timeline |
|---------|----------|----------|
| Major regulatory change | Assess impact; produce explainer content | Within 1 week |
| Market disruption | Check all scheduled content for tone-deafness; produce timely take | Within 48 hours |
| Industry event or announcement | Assess relevance; produce commentary if aligned | Within 1 week |
| Viral conversation in audience community | Assess fit; join conversation if authentic | Same day |

### Event-Triggered Scan

When a significant event occurs, run an immediate scan:

1. What happened?
2. How does it affect [AUDIENCE]?
3. Does it conflict with any scheduled content?
4. Is there an opportunity for timely content?
5. Does any existing content need to be updated or pulled?

---

## Layer 4: Source Library

Trusted sources for research and fact-checking relevant to your audience.

### Primary Sources

| Source | What it provides | URL / Access |
|--------|-----------------|--------------|
| [Source 1] | [Data type] | [URL] |
| [Source 2] | [Data type] | [URL] |
| [Source 3] | [Data type] | [URL] |

### Industry Publications

- [Publication 1]
- [Publication 2]
- [Publication 3]

### Community Signals

- [Forum / community 1]
- [Forum / community 2]
- [Social media trends in audience communities]

---

## Update Log

Append research scan results and event-triggered scans here in reverse chronological order.

```
## [Date]: [Scan Type]

[Scan output per format above]
```
