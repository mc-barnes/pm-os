---
type: strategy
status: approved
owner: @Sterdb
last-reviewed: 2026-05-01
related:
  - team/decisions/dec-001-review-panel-orchestration.md
  - docs/adoption-guide.md
  - docs/auditor-briefing.md
  - docs/responsible-use.md
---

# Messaging Canon

Agreed messaging state across all surfaces. Future copy, assets, and conversations inherit from this document.

## Thesis

A Claude Code workspace for SaMD teams managing change control on shipped product. Specialist reviewers pre-screen change packages before RA review. Outputs are uncontrolled drafts; the eQMS stays the system of record.

## Three pillars

Every surface should reflect these:

1. **Shared context** — one repo where product, regulatory, clinical, quality, and cybersecurity work
2. **Specialist reviewers** — AI agents with citation discipline against pinned standards
3. **Boundary** — uncontrolled drafts feeding controlled records; the eQMS remains system of record

## Audience anchor

SaMD teams managing change control on shipped product. Not 0-to-1 submission teams as the primary frame — change control is the daily work, the budget, the pain. 510(k) submission framing is secondary.

## Mechanism word

| Context | Term | Example |
|---------|------|---------|
| Human-facing copy (LinkedIn, conversation, slides) | "specialist reviewers" | "Specialist reviewers pre-screen change packages" |
| Technical contexts (README, docs, architecture) | "reviewer agents" | "Reviewer agents run in parallel via the review panel" |

Rule: don't mix within a single surface. The README is a technical surface — use "reviewer agents" throughout. LinkedIn and conversation are human-facing — use "specialist reviewers" throughout.

## Speed claim

What compresses, what doesn't:

- **Compresses:** authoring — code search, dependency research, change control lookup, decision log retrieval, standards-pinned language drafting
- **Doesn't compress:** judgment work — rationale, risk acceptability, change scope decisions
- **Net effect:** review goes to substance, not structural cleanup

## Agent count

Do not hardcode agent counts in copy. The current count (five) is an implementation detail that will change. Use:
- "Specialist reviewers" / "reviewer agents" (no number)
- "Each reviewer operates from a defined regulatory or clinical perspective"

When a count is unavoidable (e.g., cost table), state it as fact without making it a selling point.

---

## Surface-by-surface assignments

### LinkedIn image

| Element | Current | Target |
|---------|---------|--------|
| Tagline | *(not yet created)* | "Specialist reviewers. One repo." |
| Standards row | — | IEC 62304:2006+A1:2015 · ISO 14971:2019 · IEC 81001-5-1:2021 — pinned |
| Boundary line (new) | — | "Uncontrolled drafts. Your eQMS stays the system of record." |
| Speed claim | — | None (image at capacity) |
| Wordmark | — | Render as "samd-os" or "SaMD OS" with visual break. Never "SaMDOS". |

Pre-publish checklist:
- [ ] Reverse-image-search the aperture mark before publishing (IP clearance, one-time task)

### README

| Element | Current (line) | Target |
|---------|----------------|--------|
| Hero tagline (L5) | "Ship regulated software at startup speed — whether you're building docs alongside code or catching up after launch." | **Keep.** |
| Sub-tagline | *(none)* | **Add immediately after L5:** *Authoring in minutes, not days. Review goes to substance, not cleanup.* |
| First sentence (L3) | "For teams shipping regulated software without a 30-person QMS organization." | **Replace with:** "For SaMD teams managing change control on shipped product without a 30-person QMS organization." |
| Agent count (L3) | "Five reviewer agents catch findings before auditors do." | **Replace with:** "Reviewer agents catch findings before auditors do." |
| Section heading (L17) | "Five specialist reviewers that operate from a defined regulatory or clinical perspective." | **Replace with:** "Reviewer agents that each operate from a defined regulatory or clinical perspective." |
| Boundary statement (L9) | Present in Scope and Limitations. | **Keep. Verify visible in first screen.** |
| Standards editions | Pinned in L3. | **Keep.** |
| Mermaid diagram (L127) | "5 agent personas" | **Replace with:** "Agent personas" |
| Cost table (L161) | "Full review panel (5 agents)" | **Replace with:** "Full review panel (all agents)" |

Mechanism word: "reviewer agents" throughout (technical surface).

### docs/responsible-use.md

| Element | Current | Target |
|---------|---------|--------|
| Agent count | "SaMD Team OS includes five AI reviewer agents" | Replace count with "SaMD Team OS includes AI reviewer agents" |

### docs/auditor-briefing.md

| Element | Current | Target |
|---------|---------|--------|
| Agent count | "SaMD Team OS includes five AI reviewer agents" | Replace count with "SaMD Team OS includes AI reviewer agents" |

### CLAUDE.md (root)

| Element | Current (L11) | Target |
|---------|----------------|--------|
| Skills count | "14 shared skills + 5 agent personas" | Replace with "shared skills + agent personas" (counts change) |

### Conversation opener

> "It's a Claude Code workspace for SaMD teams managing change control on shipped product. Specialist reviewers pre-screen change packages — impact assessment, re-verification scope, risk re-evaluation — before RA review. Drafts are uncontrolled; the eQMS stays the system of record. What's your initial reaction?"

End with the question — hands the conversation to them, signals advisor frame, not pitch.

### Conversation goals

**Goals:**
- Their honest reaction to the framing
- Specific blockers to adoption in their context
- Signal on whether the project has commercial legs

**Not goals:**
- Closing them
- Getting a pilot commitment
- Convincing them you're right

---

## Objection handlers

Short forms — expand in conversation only if pressed.

| Objection | Response |
|-----------|----------|
| vs. eQMS vendors | Draft layer that feeds them, not a replacement. eQMS owns control; samd-os owns the working environment. |
| vs. AI compliance tools | They position AI as reviewer of record. samd-os explicitly doesn't. Open source, self-hosted, citation-disciplined. |
| Validation | 20/20 dry-run; live eval pending. Ask their input on what additional evidence their org would need. |
| Versioning | Git handles version control automatically. Frontmatter status tracks lifecycle. eQMS owns controlled records. |
| Integrations | Manual handoff today. Export-format integration as credible v2. Bidirectional API deliberately out of scope. |
| Trust | Not "is the AI right" — "does this catch enough that humans do their job better." Pre-screening, not sign-off. |
| Business model | None today. Open source, MIT. If commercial signal emerges, separate conversation. |
| Fit for their company | Turn into discovery question — what's their QMS, team size, regulatory pathway. |

## Closing pattern

| Signal | Response |
|--------|----------|
| Pushed back substantively | "Would you take another look in a couple months?" |
| Curious but no strong reactions | "Anything I should think about that I haven't mentioned?" |
| Offered intros | Accept warmly, don't seek |
| Raised concerns you can't address | "Can I follow up in a few weeks?" |

---

## Places to avoid

- "Side project" framing
- Promising integrations not built
- Defending features when pushed back on
- Marketing register ("transform," "democratize")
- Overclaiming validation (live eval is pending; say so)
- Pitching gap analysis as production-validated (skills and fixtures exist; live agent evaluation is pending)
- Asking for intros or referrals in the first call
- Giving long technical answers when short ones suffice
- Treating both contacts identically (different roles, different feedback value)
- Hardcoding agent counts in durable copy

---

## New artifact: docs/integrations.md

Scope for a new document (~20 min to write):

### Three eQMS patterns

| Pattern | Description | Status |
|---------|-------------|--------|
| Manual | Copy/paste from samd-os markdown/XLSX into eQMS record forms. Team reviews diff in git, then imports approved content. | Available today |
| Export-format | samd-os outputs in eQMS-ingestible format (CSV, XML, specific XLSX templates). Reduces copy/paste but still human-triggered. | Credible v2 scope |
| Bidirectional API | Two-way sync between samd-os and eQMS. Real-time status, lock management, signature integration. | Deliberately out of scope — complexity and compliance risk outweigh benefit. |

### Jira reference convention

How to cross-reference Jira ticket IDs in samd-os frontmatter. Convention: add `jira: PROJ-123` to frontmatter YAML. Reviewer agents surface the Jira ID in findings so RA can trace back to the change request. No Jira API integration — this is a metadata convention, not a sync.

### Knowledge base recommendation

Guidance on where to host the reference library (pinned standards, guidance docs) that reviewer agents cite against. Recommendation: `references/` folder in repo with PDFs of standards the team has licensed. Reviewer agents cite section numbers; the team verifies against their licensed copy. Do not distribute copyrighted standards in a public repo.

---

## Consistency sweep checklist

Run after README and docs updates:

- [ ] Mechanism word: "reviewer agents" in all technical surfaces (README, docs/, CLAUDE.md)
- [ ] Mechanism word: "specialist reviewers" in all human-facing surfaces (LinkedIn, conversation script)
- [ ] No mixed usage within any single surface
- [ ] Audience anchor: "change control on shipped product" appears in README first sentence, adoption guide, and conversation opener
- [ ] No "predicate review" or "submission" as primary frame (secondary mentions OK)
- [ ] Standards editions pinned in every citation (no bare "IEC 62304" without edition)
- [ ] No hardcoded agent counts in README hero, docs/responsible-use.md, docs/auditor-briefing.md
- [ ] Hardcoded counts acceptable only in: cost table (stated as fact), architecture diagram (if needed), decision records (historical)
- [ ] Gap analysis: described as "skills and fixtures exist; live agent evaluation pending" — not "spec only" and not "production-validated"
- [ ] Boundary statement ("uncontrolled drafts; eQMS is system of record") visible in first screen of README

---

## Staleness triggers

Re-review this canon when any of the following occur:

- Agent count changes (new reviewer added or removed)
- Live eval results arrive
- Commercial model is defined
- New surface is created (website, demo video, conference talk)
- Gap analysis completes live agent evaluation
- Major skill is added or removed
- Standards editions are updated (e.g., IEC 62304 Ed 2 published)
