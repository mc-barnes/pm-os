# SaMD Team OS

A Team OS built for SaMD. One mind across every function. Ship regulated software at startup speed.

One repo your whole team works in — product, regulatory, clinical, engineering, and quality. Claude Code navigates the structure, generates regulatory artifacts (IEC 62304, ISO 14971, FDA guidance), and encodes your QMS workflows so nobody re-explains the device.

## Architecture

```mermaid
graph TD
    ROOT["CLAUDE.md<br/><i>Always loaded — doc index, team, device context</i>"]

    ROOT --> PROD["product/"]
    ROOT --> REG["regulatory/"]
    ROOT --> CLIN["clinical/"]
    ROOT --> ANA["analytics/"]
    ROOT --> ENG["engineering/"]
    ROOT --> QUAL["quality/"]
    ROOT --> TEAM["team/"]
    ROOT --> SKILLS[".claude/skills/"]
    ROOT --> EX["examples/"]

    PROD --> P_NAV["CLAUDE.md<br/><i>PRDs, customers, competitive, strategy</i>"]
    REG --> R_NAV["CLAUDE.md<br/><i>Design controls, risk, submissions, DHF</i>"]
    CLIN --> C_NAV["CLAUDE.md<br/><i>Intended use, usability</i>"]
    ANA --> A_NAV["CLAUDE.md<br/><i>Post-market surveillance, product metrics</i>"]
    ENG --> E_NAV["CLAUDE.md<br/><i>Bugs, RFCs, IEC 62304 SDLC</i>"]
    QUAL --> Q_NAV["CLAUDE.md<br/><i>CAPA, complaints, audits</i>"]
    TEAM --> T_NAV["CLAUDE.md<br/><i>Onboarding, retros</i>"]

    SKILLS --> S1["14 skills"]
    SKILLS --> S2["2 agent personas"]

    style ROOT fill:#1F4E79,color:#fff
    style SKILLS fill:#2E7D32,color:#fff
```

Every folder has a `CLAUDE.md` navigation map. Claude reads the root on every session and only loads deeper context when a query targets that domain — keeping context usage under 5% for most operations.

## What's Included

### Skills (`.claude/skills/`)

| Skill | Trigger | Output |
|-------|---------|--------|
| PRD Writer | "general PRD", "product spec", "feature requirements" | Markdown PRD |
| Metrics Definition | "define metrics", "KPIs", "north star metric" | Markdown metrics framework |
| Decision Doc | "decision doc", "RFC", "ADR" | Markdown decision record |
| Status Update | "status update", "stakeholder update" | Markdown status report |
| Research Synthesis | "synthesize research", "interview findings" | Markdown research summary |
| Competitive Analysis | "competitive analysis", "market analysis" | Markdown competitive report |
| Feature Prioritization | "prioritize features", "RICE scoring" | Markdown ranked backlog |
| Roadmap Planning | "product roadmap", "quarterly plan" | Markdown roadmap |
| PRD Writer (SaMD) | "write PRD", "product requirements" | Markdown PRD with regulatory sections |
| Design Controls | "design controls", "traceability matrix", "IEC 62304" | XLSX traceability matrix |
| Risk Management | "risk management", "ISO 14971", "FMEA" | XLSX risk analysis |
| FHIR Builder | "FHIR resource", "FHIR bundle" | JSON FHIR R4 bundle |
| Change Impact | "change impact", "re-verification scope" | XLSX change impact report |
| Design Review | "design review", "PDR", "CDR", "FDR" | XLSX + markdown narrative |

### Agent Personas (`.claude/skills/agents/`)

| Agent | Domain | Standards & Guidance |
|-------|--------|---------------------|
| Regulatory Reviewer | FDA SaMD submissions (510(k), De Novo, PMA). Reviews PRDs, design controls, risk docs, CAPA, PMS reports, change requests, and SOPs. | IEC 62304, ISO 14971, ISO 13485, IEC 62366-1, IMDRF N41, FDA PCCP guidance, 21 CFR 820. Backed by 28 reference docs. |
| Clinical Reviewer | *Example persona* — ships pre-configured for neonatal pulse oximetry. Replace with your clinical domain. Reviews clinical logic, alarm management, triage accuracy, and handoff quality. | Bonafide et al. (SpO2 accuracy), AAP consensus (cardiorespiratory monitoring), Owlet validation studies, NRP guidelines. |

## Folder Structure

```
pm-os/
├── CLAUDE.md                    # Root nav — always loaded
├── README.md
├── CONTRIBUTING.md              # Routing guide — where does this go?
├── LICENSE
│
├── .claude/skills/              # Claude Code auto-discovers these
│   ├── prd-writer/
│   ├── metrics-definition/
│   ├── decision-doc/
│   ├── status-update/
│   ├── research-synthesis/
│   ├── competitive-analysis/
│   ├── feature-prioritization/
│   ├── roadmap-planning/
│   ├── prd-writer-samd/
│   ├── design-controls/         # IEC 62304 traceability (XLSX)
│   ├── risk-management/         # ISO 14971 FMEA (XLSX)
│   ├── fhir-builder/            # FHIR R4 bundles (JSON)
│   ├── change-impact/           # Change impact analysis (XLSX)
│   ├── design-review/           # PDR/CDR/FDR gate (XLSX + MD)
│   └── agents/
│       ├── regulatory-reviewer/ # FDA SaMD submission reviewer
│       └── clinical-reviewer/   # Domain expert (example: neonatal SpO2)
│
├── product/                     # PRDs, strategy, competitive, customers
├── regulatory/                  # Design controls, risk, submissions, DHF
├── clinical/                    # Intended use, usability, clinical evaluation
├── analytics/                   # Post-market surveillance, product metrics
├── engineering/                 # Bugs, RFCs, IEC 62304 SDLC
├── quality/                     # CAPA, complaints, audit prep
├── team/                        # Onboarding, retros, decisions
├── scripts/                     # status.sh → generates STATUS.md from frontmatter
│
└── examples/                    # Pre-generated artifacts
    ├── design-controls-example.xlsx
    ├── risk-analysis-example.xlsx
    ├── fhir-bundle-example.json
    ├── samd-prd-example.md
    ├── change-impact-example.xlsx
    └── design-review-example.xlsx
```

## Getting Started

### 1. Fork this repo

```bash
git clone https://github.com/mc-barnes/pm-os.git
cd pm-os
```

### 2. Customize the root CLAUDE.md

Open `CLAUDE.md` and replace the `[placeholders]` with your team's details:
- Team roster (names, roles, Slack/GitHub handles)
- Communication channels
- Device context (classification, predicate, standards, clinical domain)

### 3. Start using skills

Skills are auto-discovered by Claude Code from `.claude/skills/`. Just say the trigger phrase:

```
> "Generate design controls for our cardiac monitor, safety class C"
> "Write a PRD for the new alarm management feature"
> "Run a risk analysis for the SpO2 threshold change"
```

### 4. Fill in templates

Each content folder has `_TEMPLATE.md` files with YAML frontmatter pre-configured (`type`, `status: draft`, `owner`). Copy a template, rename it, and fill in the `[brackets]`:

```bash
cp product/prds/_TEMPLATE.md product/prds/alarm-management-v2.md
```

### 5. Check document status

Run the status generator to see what's draft, in-review, approved, or stale:

```bash
./scripts/status.sh    # generates STATUS.md from frontmatter
```

## Example Artifacts

The `examples/` folder contains pre-generated artifacts using a neonatal pulse oximeter as the reference device:

| File | Skill Used | Contents |
|------|-----------|----------|
| `design-controls-example.xlsx` | Design Controls | Full UN → DI → DO → V&V traceability matrix |
| `risk-analysis-example.xlsx` | Risk Management | Hazard analysis + FMEA with RPN calculations |
| `fhir-bundle-example.json` | FHIR Builder | FHIR R4 bundle with Patient + Observation resources |
| `samd-prd-example.md` | PRD Writer (SaMD) | Product requirements with regulatory sections |
| `change-impact-example.xlsx` | Change Impact | Software change impact with re-verification scope |
| `design-review-example.xlsx` | Design Review | CDR gate package with GO/NO-GO recommendation |

> **Regulatory note:** Skill-generated XLSX and JSON files are **uncontrolled drafts** — no audit trail, no electronic signatures, no Part 11 / Annex 11 compliance. Final approved records belong in your eQMS of record (e.g., Greenlight Guru, MasterControl, Qualio). Position these outputs as working drafts that feed your controlled document system.

## Context Management

SaMD Team OS uses tiered context loading to keep Claude Code efficient:

| Tier | What | When Loaded | Example |
|------|------|-------------|---------|
| **Tier 1** | Root `CLAUDE.md` | Every session | Doc index, team roster, device context |
| **Tier 2** | Folder `CLAUDE.md` | When Claude navigates to that folder | `regulatory/CLAUDE.md` loaded on a risk question |
| **Tier 3** | Templates and documents | On demand when referenced | `regulatory/risk-management/_TEMPLATE.md` |

A query about customers loads `product/CLAUDE.md` and relevant customer files — it never touches `analytics/`, `engineering/`, or `regulatory/`. This keeps context usage minimal and responses focused.

## Built with Claude Code

This repo was built entirely with [Claude Code](https://claude.com/claude-code) — from the skill authoring to the folder architecture to this README.

**Companion project**: [spo2-eval-pipeline](https://github.com/mc-barnes/spo2-eval-pipeline) — an end-to-end AI evaluation pipeline for neonatal SpO2 monitoring, also built with Claude Code.

## License

MIT — see [LICENSE](LICENSE).
