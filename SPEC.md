---
type: spec
status: draft
owner: @Sterdb
project: voc-synthesizer
created: 2026-05-02
---

# VoC Synthesizer — Specification

## 1. Objective

Build a **domain-agnostic Voice-of-Customer synthesizer** that turns raw qualitative feedback into a defensible, prioritized insight backlog. The system uses the same multi-agent architecture as samd-os: skills for single-shot generation, agents for specialist review.

### Problem
Product teams drown in qualitative signal — call notes, chat transcripts, NPS verbatims, support tickets, partner feedback. Most teams either ignore most of it or produce vibes-based summaries that don't drive decisions. The synthesizer addresses this by:
1. Extracting themes with verbatim evidence
2. Scoring severity with explicit methodology (Kano + RICE)
3. Auditing for bias before themes influence roadmap decisions
4. Producing a weekly digest artifact that surfaces trends, flags risks, and links to the roadmap

### Target Users
- Product managers synthesizing customer feedback across channels
- Heads of Product who need defensible prioritization inputs
- Customer Success / Support leads tracking theme trends
- Anyone running discovery interviews, NPS programs, or support triage

### What "Done" Looks Like (MVP)
A user drops 20-50 raw input documents (call notes, chat logs, NPS exports, tickets) into `inputs/`, runs the agent panel, and gets:
1. A persistent theme registry with stable IDs and time-series counts
2. Severity scores (Kano classification + RICE prioritization) per theme
3. Bias audit flags on the theme set
4. A weekly digest markdown artifact suitable for stakeholder review

---

## 2. Commands (Skills & Agent Triggers)

### MVP Skills (v1)

| Skill | Trigger | Input | Output |
|-------|---------|-------|--------|
| `transcript-cleaner` | "clean transcript", "clean call notes", "clean social post", "clean blog post" | Raw transcript/post/blog text | Speaker-labeled, redacted markdown with structured frontmatter |
| `voc-weekly-digest` | "weekly voc digest", "voc digest" | `themes/` directory + prior digests | Markdown digest with theme rankings, WoW deltas, bias flags |

### MVP Agents (v1)

| Agent | Trigger | Input | Output |
|-------|---------|-------|--------|
| `theme-extractor` | "extract themes", "run theme extraction" | `inputs/` directory + `themes/_registry.yaml` | Updated registry + new/updated theme docs in `themes/` |
| `severity-scorer` | "score themes", "run severity scoring" | `themes/` directory | Updated theme docs with Kano classification + RICE scores |
| `bias-auditor` | "audit bias", "run bias audit" | `themes/` directory + `inputs/` metadata | Bias audit report with flags and recommendations |

### v2 Skills (out of MVP scope)

| Skill | Trigger | Notes |
|-------|---------|-------|
| `nps-synthesizer` | "synthesize NPS comments" | Promoter/passive/detractor breakdown |
| `interview-synthesizer` | "synthesize discovery interviews" | Per-interview + cross-interview patterns |
| `insight-to-opportunity` | "turn insight into opportunity" | Opportunity solution tree node |
| `quote-bank-builder` | "build quote bank" | May be a query mode on theme data instead |

### v2 Agents (out of MVP scope)

| Agent | Trigger | Notes |
|-------|---------|-------|
| `jtbd-reviewer` | "reframe as JTBD", "run JTBD review" | Christensen/Moesta JTBD framing |
| `roadmap-linker` | "link to roadmap", "run roadmap linkage" | Requires structured roadmap input |

### Orchestration: Full Panel Run

Trigger: "run voc panel", "synthesize feedback"

Execution order (sequential — each depends on the prior):
1. **Theme Extractor** — process all unprocessed inputs, update registry
2. **Severity Scorer** — score/re-score themes with new data
3. **Bias Auditor** — audit the updated theme set
4. **VoC Weekly Digest** — generate the digest artifact

---

## 3. Project Structure

```
voc-synthesizer/
├── CLAUDE.md                       # Always loaded — project context, conventions, domain config
├── SPEC.md                         # This file
├── .claude/
│   └── skills/
│       ├── transcript-cleaner/
│       │   └── SKILL.md
│       ├── voc-weekly-digest/
│       │   └── SKILL.md
│       └── agents/
│           ├── README.md           # Agent index and routing guide
│           ├── theme-extractor/
│           │   ├── SKILL.md
│           │   └── references/
│           │       └── thematic-analysis.md    # Braun & Clarke methodology
│           ├── severity-scorer/
│           │   ├── SKILL.md
│           │   └── references/
│           │       ├── kano-model.md           # Kano classification guide
│           │       └── rice-scoring.md         # RICE prioritization guide
│           └── bias-auditor/
│               ├── SKILL.md
│               └── references/
│                   └── response-bias.md        # Survey methodology, bias types
├── inputs/                         # Raw feedback documents (markdown with frontmatter)
│   ├── _INPUT_TEMPLATE.md          # Template for new input documents
│   └── (user-provided input files)
├── themes/
│   ├── _registry.yaml              # Source of truth: all theme IDs, metadata, time-series
│   ├── _THEME_TEMPLATE.md          # Template for individual theme docs
│   └── (individual theme docs: THM-001.md, THM-002.md, ...)
├── digests/                        # Generated weekly/monthly digests
│   └── (digest-2026-W18.md, ...)
├── audits/                         # Bias audit reports
│   └── (bias-audit-2026-W18.md, ...)
└── examples/
    ├── inputs/                     # 20-30 synthetic example inputs across personas
    ├── themes/                     # Example theme registry + theme docs after extraction
    ├── digests/                    # Example weekly digest
    └── audits/                     # Example bias audit report
```

---

## 4. Schemas

### 4.1 Input Document Schema

Every input document is a markdown file with required YAML frontmatter. This is the "bring your own text" contract — users must provide these fields for the system to work.

```yaml
---
type: input                         # Always "input"
channel: patient-call | physician-call | sales-call | nps | ticket | interview | tiktok | instagram | patient-advocacy-blog
persona: patient | caregiver | physician | advocate | sales-prospect
date: 2026-04-28                    # When the interaction occurred
client: "Client Name"               # Optional: organization name (for B2B contexts or bias auditing)
attribution-level: identified | semi-anonymous | anonymous  # Optional: how identifiable is the source
source-url: ""                      # Optional: URL of the social post, blog, or original source
source-post-id: ""                  # Optional: platform-specific post ID (for tracking amplification)
engagement-views: 0                 # Optional: view count on source post (social channels)
engagement-comments: 0              # Optional: comment count on source post
engagement-shares: 0                # Optional: share/repost count on source post
segment: "Segment Name"             # Optional: population segment, condition, region
severity-hint: low | medium | high | critical  # Optional: submitter's severity estimate
source-id: "ZEN-12345"             # Optional: external system ID (Zendesk, Salesforce, etc.)
processed: false                    # Set to true after Theme Extractor processes it
---

# [Title — brief description of the interaction]

[Raw transcript / feedback text here. Can include speaker labels, timestamps, etc.]
```

**Required fields:** `type`, `channel`, `persona`, `date`
**Optional fields:** `client`, `attribution-level`, `source-url`, `source-post-id`, `engagement-views`, `engagement-comments`, `engagement-shares`, `segment`, `severity-hint`, `source-id`, `processed`

**Channel definitions (organized by tier):**

| Tier | Channel | What it captures |
|------|---------|-----------------|
| **Structured** | `patient-call` | 1:1 patient call transcripts |
| **Structured** | `physician-call` | Provider perspective calls on patient experience |
| **Structured** | `sales-call` | Sales/demo call notes with prospects |
| **Semi-structured** | `nps` | NPS survey verbatim responses |
| **Semi-structured** | `ticket` | Support ticket descriptions and resolutions |
| **Semi-structured** | `interview` | Discovery or usability interview transcripts |
| **Unstructured** | `tiktok` | Short-form video comments, public, high volume |
| **Unstructured** | `instagram` | Captions + comments, public |
| **Unstructured** | `patient-advocacy-blog` | Long-form, curated, partially pre-synthesized |

**Attribution levels:**
- `identified` — Structured channels: patient/physician with name/account (redacted in content)
- `semi-anonymous` — Social media handles, blog authors: real identity unknown
- `anonymous` — Scraped comments with no identity at all

### 4.2 Theme Registry Schema (`themes/_registry.yaml`)

The registry is the persistent backbone. Every theme gets a stable ID that never changes. Themes can be merged or split but IDs are never reused.

```yaml
# Theme Registry — Source of Truth
# Updated by: theme-extractor agent
# Last updated: 2026-05-02

next_id: 8                          # Next available theme ID number

themes:
  THM-001:
    canonical_name: "Urgent care coverage confusion"
    aliases:
      - "UC coverage unclear"
      - "HDHP urgent care questions"
    status: active                   # active | merged | split | retired
    first_seen: 2026-04-01
    kano_class: null                 # basic | performance | delighter | indifferent | null (unscored)
    rice_score: null                 # Composite RICE score (set by severity-scorer)
    rice_components:
      reach: null
      impact: null
      confidence: null
      effort: null
    weekly_counts:                   # Time-series: mentions per ISO week
      "2026-W14": 3
      "2026-W15": 5
      "2026-W16": 7
      "2026-W17": 12
    total_mentions: 27
    linked_quotes:                   # Up to 10 most representative quotes
      - input: "inputs/call-note-2026-04-15-001.md"
        line: 23
        text: "I just want to know if urgent care is covered before I go"
      - input: "inputs/nps-2026-04-20-batch.md"
        line: 47
        text: "Every time I call about UC visits, I get a different answer"
    segment_distribution:            # For bias auditing
      by_client:                     # Optional — populated when client field is present
        "Example Health": 10
        "Regional Med": 5
      by_persona:
        patient: 12
        caregiver: 3
        physician: 5
      by_channel:
        patient-call: 8
        tiktok: 6
        instagram: 3
        physician-call: 3
      by_channel_tier:               # Aggregated from channel assignments
        structured: 11
        semi-structured: 2
        unstructured: 9
      by_source_post:                # For single-source amplification detection
        "tiktok-viral-001": 5
        "ig-post-042": 2
    merged_from: []                  # If this theme absorbed others
    split_from: null                 # If this theme was split from another
    related_themes: ["THM-003"]      # Thematically adjacent (not duplicates)

  THM-002:
    canonical_name: "Surprise billing anxiety"
    # ... same schema ...
```

**Registry rules:**
- IDs are sequential (`THM-001`, `THM-002`, ...) and never reused
- When themes merge: keep the lower ID as `active`, set higher ID to `merged`, update `merged_from`
- When themes split: keep original ID as `split`, create new IDs, set `split_from`
- `weekly_counts` uses ISO 8601 week numbers for unambiguous time-series
- `segment_distribution` is updated on every extraction run (enables bias auditing)
- `linked_quotes` caps at 10 per theme; preference for diversity across clients/personas

### 4.3 Individual Theme Document Schema (`themes/THM-nnn.md`)

Each theme gets a markdown document for narrative detail that doesn't fit in the registry YAML.

```yaml
---
type: theme
theme-id: THM-001
status: active
canonical-name: "Urgent care coverage confusion"
first-seen: 2026-04-01
last-updated: 2026-05-02
kano-class: basic
rice-score: 847
---

# THM-001: Urgent care coverage confusion

## Summary
Patients are confused about medication costs and coverage, leading to delayed refills and treatment gaps. Physicians report patients frequently asking about out-of-pocket costs during appointments, and social media shows widespread frustration with cost transparency.

## Evidence
### Representative Quotes
> "I just want to know what my medication costs before I fill it" — Patient, patient-call, 2026-04-15
> "Every time I call about my prescription, I get a different answer" — Patient, nps, 2026-04-20
> "Patients are delaying refills because they can't predict out-of-pocket costs" — Physician, physician-call, 2026-04-22

### Trend
- W14: 3 → W15: 5 → W16: 7 → W17: 12 (+71% WoW)
- Concentrated in Acme Corp (67% of mentions) — bias flag raised

## Kano Classification
**Basic** — Patients expect to know their costs before filling a prescription. Absence causes dissatisfaction; presence doesn't delight.

## RICE Score
| Component | Score | Rationale |
|-----------|-------|-----------|
| Reach | 3200 | Estimated patients affected based on call volume + silent majority |
| Impact | 3 | High — drives calls, delayed treatment, NPS detractors |
| Confidence | 70% | Strong signal but concentrated in unstructured channels |
| Effort | 2 | Cost lookup integration; generalizable feature is larger |
| **Composite** | **847** | (3200 * 3 * 0.7) / 2 / 8 |

## Signal Quality
**Moderate** — 40% structured (patient calls, physician calls), 60% unstructured (TikTok, Instagram)
- Structured evidence: 4 patient calls, 2 physician calls
- Unstructured evidence: 6 TikTok/Instagram mentions across 3 posts

## Bias Flags
- [PLATFORM BIAS] 60% of mentions from unstructured channels — demographic skew toward younger, digitally active patients
- [RECOMMENDATION] Cross-validate with structured channels (patient calls, physician calls) before roadmap commitment

## Related
- THM-003: "Insurance pre-authorization delays"
- See also: inputs/physician-call-2026-04-22-001.md
```

### 4.4 Agent Output Formats

All agents follow the samd-os pattern: structured verdict + findings + citations.

#### Theme Extractor Output

```markdown
## Theme Extraction Report

**Run date:** 2026-05-02
**Inputs processed:** 47 (23 new, 24 previously processed)
**Themes updated:** 8
**New themes created:** 2
**Merges proposed:** 1

### New Themes
- **THM-008: "Provider directory accuracy complaints"** — 5 mentions across 3 clients
- **THM-009: "Mobile app login friction"** — 3 mentions, all chat channel

### Updated Themes (significant changes)
- **THM-001: "Urgent care coverage confusion"** — +12 mentions (W17), now 27 total. WoW: +71%
- **THM-003: "Plan structure change communication"** — +4 mentions

### Merge Proposal
- **THM-005 → THM-001**: "Coverage lookup failures" appears to be a subset of "Urgent care coverage confusion."
  **Action required:** Human review. Set THM-005 status to `merged` and update THM-001 `merged_from` if confirmed.

### Quotes Captured
[Table of new quotes added to theme docs]

---
*Generated by theme-extractor agent. All theme assignments are proposals — review before committing to registry.*
```

#### Severity Scorer Output

```markdown
## Severity Scoring Report

**Run date:** 2026-05-02
**Themes scored:** 8

### Kano Classification

| Theme | Classification | Rationale |
|-------|---------------|-----------|
| THM-001 | Basic | Knowing medication side effects is table-stakes; absence drives fear and non-adherence |
| THM-002 | Performance | Better scheduling = less friction, linear satisfaction |
| THM-003 | Basic | Pre-auth is a blocker; absence prevents necessary care |
| THM-004 | Performance | More caregiver support = better outcomes, linearly |

### RICE Prioritization

| Rank | Theme | Reach | Impact | Confidence | Effort | Score |
|------|-------|-------|--------|------------|--------|-------|
| 1 | THM-001 | 3200 | 3 | 70% | 2 | 847 |
| 2 | THM-002 | 2800 | 2 | 90% | 2 | 560 |
| 3 | THM-003 | 1500 | 3 | 80% | 3 | 450 |
| ... | ... | ... | ... | ... | ... | ... |

### Scoring Notes
- THM-001 confidence reduced to 70% due to platform bias + single-source amplification (see bias audit)
- THM-002 confidence boosted to 90% (base 80% + 10% cross-channel corroboration)
- THM-003 physician-heavy signal; high impact on clinical outcomes

---
*Generated by severity-scorer agent. RICE scores are inputs to prioritization, not decisions.*
```

#### Bias Auditor Output

```markdown
## Bias Audit Report

**Run date:** 2026-05-02
**Audit scope:** 8 active themes, 143 input documents
**Verdict:** BIAS FLAGS RAISED — review before roadmap commitment

### Flags

- [BA-001] **SINGLE-SOURCE AMPLIFICATION** — THM-001 "Medication side effect anxiety"
  **Finding:** 5 of 6 social media mentions trace to comments on 1 viral TikTok post (850K views).
  **Risk:** Volume reflects one viral moment, not broad patient experience.
  **Recommendation:** Treat the viral post as 1 data point. Require independent mentions from other sources.

- [BA-002] **PLATFORM BIAS** — THM-001 "Medication side effect anxiety"
  **Finding:** 75% of evidence from unstructured channels. TikTok skews 18-34.
  **Risk:** Theme may over-represent younger, digitally active patients.
  **Recommendation:** Cross-validate with structured channels before roadmap commitment.

- [BA-003] **SOURCE CONCENTRATION** — THM-004 "Caregiver burnout / support gap"
  **Finding:** 67% of mentions from one advocacy blog (CaregiverVoices).
  **Risk:** Advocate's editorial lens may amplify certain narratives.
  **Recommendation:** Seek independent patient/caregiver call transcripts.

- [BA-004] **RECENCY BIAS** — THM-005 "Telehealth quality concerns"
  **Finding:** All 4 mentions occurred in W17. No prior-week signal.
  **Risk:** May be a transient spike rather than a durable pattern.
  **Recommendation:** Monitor for 2 more weeks before scoring.

### What Looks Sound
- THM-002 "Appointment scheduling friction" has balanced distribution across 3 channel tiers and 3 personas. High confidence. Cross-channel corroboration boost applies.
- Persona mix across all themes: 56% patient, 12% caregiver, 12% physician, 12% advocate, 8% sales-prospect.

### Sample Composition
| Dimension | Breakdown |
|-----------|-----------|
| Channel Tier | Structured 44%, Semi-structured 8%, Unstructured 48% |
| Personas | Patient 56%, Caregiver 12%, Physician 12%, Advocate 12%, Sales-Prospect 8% |
| Channels | Patient-call 24%, TikTok 20%, Instagram 16%, Physician-call 12%, Blog 12%, Sales-call 8%, NPS 4%, Ticket 4% |
| Weeks | W14: 16%, W15: 20%, W16: 24%, W17: 40% |

---
*Generated by bias-auditor agent. Bias flags are advisory — they inform confidence levels, not veto decisions.*
```

### 4.5 Weekly Digest Format (`digests/digest-2026-W18.md`)

This is the primary demo artifact — the output a Head of Product would review.

```yaml
---
type: digest
period: 2026-W18
generated: 2026-05-02
inputs-processed: 25
themes-active: 7
themes-new: 2
bias-flags: 4
---
```

```markdown
# VoC Weekly Digest — W18 (Apr 28 – May 2, 2026)

**25** inputs processed | **11** structured (6 patient calls, 3 physician calls, 2 sales calls), **2** semi-structured (1 NPS, 1 ticket), **12** unstructured (5 TikTok, 4 Instagram, 3 blogs)
**7** active themes | **2** new this week | **4** bias flags

---

## Top Themes by RICE Score

### 1. THM-001: Medication side effect anxiety — RICE 847 (Kano: Basic)
**Trend:** 1 → 2 → 2 → **3** (+50% WoW) | **8 total mentions**
> "Nobody warned me about these side effects and now I'm terrified to keep taking it" — Patient, TikTok

**Signal quality:** Weak — 75% unstructured (6 TikTok/Instagram), 25% structured (2 patient calls)
- Structured evidence: 2 patient calls (Moderate)
- Unstructured evidence: 6 TikTok/Instagram, 5 from 1 viral post (Weak — single-source amplification)

**Bias flags:** Single-source amplification (5 of 6 social mentions from 1 viral TikTok). Platform bias (75% unstructured).
**Roadmap status:** No current owner.
**Recommended action:** Validate with physician calls and patient calls before committing. The viral TikTok inflated volume — treat as 1 data point.

---

### 2. THM-002: Appointment scheduling friction — RICE 560 (Kano: Performance)
**Trend:** 2 → 2 → 1 → **2** (flat) | **7 total mentions**
> "I spent 45 minutes trying to book a follow-up and ended up just going to urgent care instead" — Patient, patient-call

**Signal quality:** Strong — 57% structured (4 patient/physician calls), 43% unstructured (3 Instagram)
**Bias flag:** None — balanced signal across 3 channel tiers and 3 personas.
**Roadmap status:** Linked to scheduling UX initiative.
**Recommended action:** Strong cross-channel corroboration. Prioritize for next sprint.

---

### 3. THM-003: Insurance pre-authorization delays — RICE 450 (Kano: Basic)
**Trend:** 1 → 1 → 2 → **1** (flat) | **5 total mentions**
> "I've had three patients delay necessary imaging because pre-auth takes two weeks" — Physician, physician-call

**Signal quality:** Strong — 60% structured (3 physician calls), 40% unstructured (2 Instagram)
**Bias flag:** Persona concentration — 60% physician. Seek patient perspective.
**Roadmap status:** Not assessed.
**Recommended action:** Physician-heavy signal suggests clinical impact. Validate with patient calls.

---

[Themes 4-7 with same format, abbreviated for lower-priority items]

---

## Emerging Signals
- **THM-006: Cost transparency before treatment** — 3 mentions, mixed channels. Too early to score. Watching.
- **THM-007: Medication refill confusion** — 3 mentions, patient calls only. Too early to score. Watching.

## Bias Audit Summary
| Flag | Theme | Issue | Action |
|------|-------|-------|--------|
| BA-001 | THM-001 | Single-source amplification (5 of 6 social from 1 TikTok) | Treat viral post as 1 data point |
| BA-002 | THM-001 | Platform bias (75% unstructured) | Cross-validate with structured |
| BA-003 | THM-004 | Source concentration (67% from 1 advocacy blog) | Seek independent sources |
| BA-004 | THM-005 | Recency (all W17) | Monitor 2 weeks |

## Input Gap Analysis
Missing this period: interview transcripts. Unstructured channels over-represented (48% of inputs). Recommend sourcing patient call transcripts and physician feedback for next cycle.

## Week-over-Week Delta
| Metric | W17 | W18 | Delta |
|--------|-----|-----|-------|
| Inputs processed | 20 | 25 | +25% |
| Active themes | 5 | 7 | +2 |
| Avg RICE (top 5) | 520 | 580 | +12% |
| Bias flags | 2 | 4 | +2 |

---

*Generated by voc-weekly-digest skill. All scores and recommendations are inputs to product decisions, not substitutes for product judgment.*
```

---

## 5. Domain Configuration

The system is domain-agnostic. Domain-specific vocabulary, personas, and channel types are configured in `CLAUDE.md`, not hardcoded in skills or agents.

### Domain Config Section in CLAUDE.md

```yaml
## Domain Configuration
domain: patient-experience
personas:
  - patient          # Primary voice — person with the health condition
  - caregiver        # Family member / advocate speaking on behalf of patient
  - physician        # Provider perspective on patient experience, treatment friction
  - advocate         # Patient advocacy blogger, community leader, influencer
  - sales-prospect   # Prospect in sales pipeline
channel-tiers:
  structured:          # Full attribution, rich context, low volume
    - patient-call     # 1:1 patient call transcripts
    - physician-call   # Provider perspective calls
    - sales-call       # Sales/demo call notes
  semi-structured:     # Some attribution, moderate context
    - nps              # NPS survey verbatim responses
    - ticket           # Support ticket descriptions
    - interview        # Discovery or usability interview transcripts
  unstructured:        # Public, anonymous, high volume, weak attribution
    - tiktok           # Short-form video comments, public
    - instagram        # Captions + comments, public
    - patient-advocacy-blog  # Long-form, curated, partially pre-synthesized
severity-levels:
  - low
  - medium
  - high
  - critical
kano-classes:
  - basic           # Absence causes dissatisfaction; presence expected
  - performance     # More is better, linearly
  - delighter       # Unexpected; absence is fine, presence delights
  - indifferent     # No impact either way
```

To adapt for a different domain (e.g., fintech, SaaS), change the personas, channel-tiers, and domain name. Skills and agents read these from CLAUDE.md at runtime.

---

## 6. Conventions

### File Naming
- Inputs: `{channel}-{date}-{nnn}.md` — e.g., `call-notes-2026-04-15-001.md`
- Themes: `THM-{nnn}.md` — e.g., `THM-001.md`
- Digests: `digest-{year}-W{nn}.md` — e.g., `digest-2026-W18.md`
- Audits: `bias-audit-{year}-W{nn}.md` — e.g., `bias-audit-2026-W18.md`
- No spaces, kebab-case, no version suffixes on time-series artifacts (they're snapshots, not versioned docs)

### ID Schemes
- `THM-nnn` — Theme (e.g., THM-001). Sequential, never reused.
- `BA-nnn` — Bias audit finding (e.g., BA-001). Per-audit-report, resets each week.
- `MP-nnn` — Merge proposal (e.g., MP-001). Per-extraction-run.

### Frontmatter
Every document has YAML frontmatter. Required fields vary by type:

| Type | Required Fields |
|------|----------------|
| `input` | type, channel, persona, date |
| `theme` | type, theme-id, status, canonical-name, first-seen |
| `digest` | type, period, generated, inputs-processed |
| `bias-audit` | type, period, generated, themes-audited |

### Cross-References
Use the pattern: `(see THM-001 in themes/THM-001.md)` or `[THM-001](themes/THM-001.md)`.

---

## 7. Testing Strategy

### Example-Driven Validation
Since this is a skills/agents system (not a runtime application), testing means validating that skills and agents produce correct output given known inputs.

#### Test Fixtures (`examples/`)
1. **Synthetic inputs** — 20-30 input documents across all personas, channels, and severity levels. Designed to produce known themes when extracted.
2. **Expected theme registry** — The registry state after running theme extraction on the example inputs. Used to verify the extractor produces stable, correct themes.
3. **Expected digest** — A reference weekly digest generated from the example themes. Used to verify digest format and delta calculations.
4. **Expected bias audit** — A reference audit with known bias flags (pre-seeded concentration and recency bias in the example inputs).

#### Validation Checklist (per skill/agent)

**Theme Extractor:**
- [ ] Processes all unprocessed inputs (sets `processed: true`)
- [ ] Creates new themes with stable IDs
- [ ] Deduplicates against existing themes (doesn't create duplicates)
- [ ] Updates `weekly_counts` with correct ISO week
- [ ] Updates `segment_distribution` accurately
- [ ] Caps `linked_quotes` at 10 per theme
- [ ] Proposes merges (doesn't auto-merge)

**Severity Scorer:**
- [ ] Assigns Kano classification with rationale
- [ ] Calculates RICE components independently
- [ ] Composite score formula is correct: (Reach * Impact * Confidence) / Effort / 8
- [ ] Does not score themes with <3 mentions (flags as "insufficient data")
- [ ] Updates theme docs and registry in sync

**Bias Auditor:**
- [ ] Flags source concentration >50% on a single source (client, platform, or blog)
- [ ] Flags recency bias (>80% of mentions in most recent week)
- [ ] Flags channel skew (>70% from a single channel)
- [ ] Flags platform demographic bias (>70% from unstructured channels per theme)
- [ ] Flags viral amplification (engagement >10x platform median)
- [ ] Flags single-source amplification (>50% social mentions from one post/thread)
- [ ] Reports sample composition table (with channel tier breakdown)
- [ ] Does not veto — flags are advisory

**Transcript Cleaner:**
- [ ] Outputs valid frontmatter with all required fields (type, channel, persona, date)
- [ ] Speaker labels are preserved or inferred (dialogue mode) or single-speaker handled (social/blog mode)
- [ ] No PII/PHI in output (redaction applied); handles redacted to [HANDLE] in social mode
- [ ] Sets `processed: false` (ready for theme extraction)
- [ ] Social mode: sets attribution-level, source-url, engagement fields
- [ ] Blog mode: extracts sub-inputs from multi-story posts

**Weekly Digest:**
- [ ] Covers all active themes, ranked by RICE
- [ ] WoW delta calculations are correct
- [ ] Bias flags are surfaced inline per theme
- [ ] Signal quality indicator (Strong/Moderate/Weak) present per theme
- [ ] Input gap analysis identifies missing channels and channel tiers
- [ ] Format matches the spec exactly

---

## 8. Boundaries

### Always
- Require frontmatter on all input documents — reject inputs without required fields
- Preserve theme ID stability — never reuse or reassign IDs
- Cite evidence (verbatim quotes with source attribution) for every theme
- Surface bias flags before they influence prioritization
- Generate all artifacts as markdown (human-readable, git-diffable)
- Keep the registry as the single source of truth for theme metadata

### Ask First
- Before merging themes (extractor proposes, human confirms)
- Before retiring a theme (may resurface later)
- Before changing a Kano classification (has downstream RICE impact)
- Before acting on a bias-flagged theme (flag is advisory, not a veto)

### Never
- Auto-merge themes without human review
- Use real PHI/PII in example inputs or test fixtures
- Hardcode domain-specific terms in skills/agents (use CLAUDE.md domain config)
- Treat RICE scores as decisions (they're inputs to decisions)
- Delete input documents after processing (mark `processed: true`, keep the source)
- Generate synthetic quotes — all quotes must trace to an actual input document

---

## 9. Build Order

Sequential — each phase depends on the prior:

| Phase | Deliverable | Depends On |
|-------|------------|------------|
| 1 | Repo scaffold + CLAUDE.md + schemas | This spec |
| 2 | Input template + 20-30 synthetic example inputs | Phase 1 (schemas) |
| 3 | Theme Extractor agent | Phase 1 (registry schema) + Phase 2 (inputs to test against) |
| 4 | Transcript Cleaner skill | Phase 1 (input schema) |
| 5 | Severity Scorer agent | Phase 3 (needs themes to score) |
| 6 | Bias Auditor agent | Phase 3 (needs themes + segment data) |
| 7 | VoC Weekly Digest skill | Phases 3+5+6 (needs themes, scores, and bias flags) |
| 8 | End-to-end validation with examples | All phases |

---

## 10. v2 Roadmap (Out of MVP Scope)

Documented here for architectural awareness — v2 items should not constrain MVP design but MVP should not block them either.

| Item | Notes |
|------|-------|
| JTBD Reviewer agent | Reframes themes as JTBD. Needs stable themes (Phase 3) as input. |
| Roadmap Linker agent | Maps themes to roadmap items. Requires structured roadmap input format (not yet defined). |
| NPS Verbatim Synthesizer | Batch processes NPS CSV exports with promoter/passive/detractor segmentation. |
| Interview Synthesizer | Per-interview summary + cross-interview pattern report. |
| Insight-to-Opportunity | Converts a theme into an opportunity solution tree node with hypothesis + experiment design. |
| Audio input adapter | Whisper-based transcription → input document with frontmatter. Out of scope for MVP. |
| Theme embeddings | Vector similarity for smarter deduplication and merge proposals. Requires embedding storage. |
| Dashboard / HTML view | Interactive theme explorer. Low priority — the digest is the primary artifact. |
