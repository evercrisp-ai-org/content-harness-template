# [ORG_NAME] Content System: Your Guide

> This document explains the entire content system in plain language. It walks you through what each document does, how the pieces fit together, and exactly what you need to do to keep the system running and improving. You do not need to use any software to follow this guide.

**Companion document:** The technical command center for AI-assisted content production lives in `START_HERE.md`. That file is for your content operator (or for use in Cursor). This guide is for you.

---

## Part 1: What This System Is (and Isn't)

The content system is a set of interconnected documents that capture your voice, define your audience, plan your content, enforce accuracy, and learn from performance data over time. Together, they allow content to be produced at scale while sounding like you, staying factually grounded, and improving with every cycle.

### What the system handles automatically

- Matching your voice and tone across every piece of content
- Enforcing accuracy (no fabricated stories, no stale facts, no misleading claims)
- Aligning content timing to deadlines, seasonal cycles, and industry events
- Translating your expertise into language that resonates with [AUDIENCE]
- Producing content in the right formats for each platform
- Learning from performance data to refine what works

### What requires your input

- Reviewing drafts for voice accuracy ("Does this sound like me?")
- Providing real stories and experiences to expand what the system can draw from
- Sharing platform analytics so the system can learn from real engagement data
- Approving plans and adjusting direction when your priorities shift
- Flagging anything that feels wrong, off-brand, or inaccurate

The core promise: every piece of content should sound like you wrote it, be grounded in things you can actually claim, and get better over time because the system learns from what your audience responds to.

---

## Part 2: The Documents and What They Do

### Layer 1: Identity -- Who You Are as a Communicator

**Voice Profile** (`brand/voice-profile.md`)

The most important document in the system. It captures who you are as a writer and communicator, distilled from your sample content. It documents your background, core beliefs, voice characteristics, structural patterns, rhetorical toolkit, and anti-patterns.

**When you should read it:** At least once in full, and any time content feels "off."

---

### Layer 2: Integrity -- What You Can and Cannot Claim

**Experience Inventory** (`brand/experience-inventory.md`)

The source of truth for every claim made in your content. It catalogs your professional facts, practice profile, audience experience, verified client stories, knowledge areas, approved personal anecdotes, aspirational positioning, and off-limits topics.

The system uses three classifications for stories:

| Classification | What it means |
|---------------|---------------|
| **REAL-ANONYMIZED** | A real client story from your practice, with details changed for privacy |
| **ILLUSTRATIVE** | A hypothetical but realistic example to demonstrate a concept |
| **GENERAL-PRINCIPLE** | Teaching a principle without any client narrative |

**When you should update it:** Any time you have a new client story, a new credential, a new topic you have practiced, or a new off-limits item. The more complete this document is, the richer your content becomes.

---

### Layer 3: Strategy -- How Content Gets Made

**Content Recipe** (`brand/content-recipe.md`)

The production playbook. You do not need to read it end-to-end. Key sections:

| Section | What it covers |
|---------|---------------|
| Audience Translation Matrix | How content is adapted for [AUDIENCE] |
| Voice Calibration Guide | What to keep, elevate, retire, and add |
| Content as Building Blocks | The 8-step production workflow |
| Research and Relevance Filter | How content stays current |
| Content Integrity Filter | How stories and claims are validated |
| Quality Checklist | The final gate every piece must pass |
| Recursive Learning Loop | How the system improves from real data |

---

### Layer 4: Timing -- When to Publish What

**Content Calendar** (`brand/content-calendar.md`)

Defines the annual cycles, deadlines, seasonal patterns, and industry events that content timing must align to. Includes a monthly research scan checklist and a signal-driven trigger framework.

---

### Layer 5: Visuals and Tone -- How It Looks and Sounds

**Brand Config** (`brand/brand_config.json`)

The visual and tonal standards: colors, fonts, imagery rules, channel specifications, and voice attributes. This file is read by both humans (for manual design work) and scripts (for automated generation).

---

## Part 3: Your Role in the System

### Weekly: Review Content Drafts

When new content is produced, your job is to read each piece and answer:

1. Does this sound like me?
2. Are the facts correct?
3. Would I be comfortable putting my name on this?
4. Would [AUDIENCE] find this valuable?

If the answer to any of these is no, provide specific feedback. The system will revise.

### Monthly: Share Performance Data

Log in to your platform analytics (LinkedIn, YouTube, website, etc.) and share the numbers. The system cannot access your analytics directly. Without this data, the Recursive Learning Loop cannot function. Use `brand/performance-log-template.md` as the format.

### Quarterly: Review the Plan

Review the editorial plan and quarterly drill-down. Confirm that the topics, timing, and angles still align with your priorities. Flag any changes in your business, audience, or competitive landscape.

### As Needed: Update the Experience Inventory

When you have a new client story, a new credential, or a shift in your practice, update `brand/experience-interview-guide.md` and then `brand/experience-inventory.md`. The richer the inventory, the more authentic the content.

---

## Part 4: How the System Improves Over Time

The Recursive Learning Loop (content-recipe.md Section 11) is the mechanism:

1. **Content is produced** following the voice profile and quality gates.
2. **Content is published** across your channels.
3. **Performance data is collected** (by you, from platform analytics).
4. **The system analyzes** what worked and what didn't.
5. **The system updates** the content recipe, calendar, and voice profile based on real data.
6. **The next batch** is better than the last.

This loop only works if you provide performance data. Without it, the system produces opinions rather than insights.

---

## Part 5: When Something Goes Wrong

| Problem | Solution |
|---------|----------|
| Content doesn't sound like me | Re-read voice-profile.md; provide specific feedback on what feels off |
| Content makes a claim I can't support | Check experience-inventory.md; update it if the claim is now supportable, or flag the content for revision |
| Content references outdated information | Flag it; the system will re-run the Relevance Filter |
| Content is publishing at the wrong time | Check content-calendar.md; update key dates if they've changed |
| The audience isn't responding | Provide performance data; the Recursive Learning Loop will identify the issue |
| I want to change direction | Update the editorial plan; the quarterly plan will adjust |
