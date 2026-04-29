# PM OS Skills

Claude Code skills for SaMD product management. Each skill extends Claude with domain-specific knowledge, workflow automation, and artifact generation.

## Categories

### `samd-regulatory/` — Regulatory Document Generators

Generate IEC 62304, ISO 14971, and FDA-compliant artifacts directly from Claude Code.

| Skill | Trigger Phrase | Output |
|-------|---------------|--------|
| `design-controls` | "design controls", "traceability matrix", "IEC 62304", "user needs", "V&V traceability" | XLSX traceability matrix |
| `risk-management` | "risk management", "ISO 14971", "FMEA", "hazard analysis", "risk acceptability" | XLSX risk analysis + FMEA |
| `fhir-builder` | "FHIR resource", "FHIR bundle", "HL7v2 to FHIR mapping", "capability statement" | JSON FHIR R4 bundle |
| `change-impact` | "change impact", "software change", "re-verification scope", "new 510(k) needed" | XLSX change impact report |
| `design-review` | "design review", "PDR", "CDR", "FDR", "review package", "GO/NO-GO gate" | XLSX + markdown narrative |

### `samd-pm/` — PM Workflow Skills

| Skill | Trigger Phrase | Output |
|-------|---------------|--------|
| `prd-writer-samd` | "write PRD", "product requirements document" | Markdown PRD with regulatory sections |
| `interview-prep` | "interview prep", "mock interview", "STAR stories" | Interactive mock interview session |
| `networking-outreach` | "networking message", "LinkedIn outreach", "reach out to" | Personalized outreach text |

### `agents/` — Specialist Personas

| Agent | Use Case |
|-------|----------|
| `clinical-reviewer` | Neonatal SpO2 clinical logic review, alarm management, triage accuracy, handoff quality |

## Installation

### Prerequisites
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- Python 3.9+ (for XLSX/JSON generation scripts)
- `openpyxl` package: `pip install openpyxl`

### Install All Skills

```bash
# Clone the repo
git clone https://github.com/mc-barnes/pm-os.git
cd pm-os

# Copy regulatory skills
cp -r skills/samd-regulatory/* ~/.claude/skills/

# Copy PM skills
cp -r skills/samd-pm/* ~/.claude/skills/

# Copy agent personas
cp -r skills/agents/* ~/.claude/skills/agents/
```

### Install Individual Skills

```bash
# Just design controls
cp -r skills/samd-regulatory/design-controls ~/.claude/skills/

# Just FHIR builder
cp -r skills/samd-regulatory/fhir-builder ~/.claude/skills/

# Just the clinical reviewer agent
mkdir -p ~/.claude/skills/agents
cp -r skills/agents/clinical-reviewer ~/.claude/skills/agents/
```

## Skill Structure

Each skill follows this structure:
```
skill-name/
├── SKILL.md          # Instructions Claude reads when triggered
├── references/       # Standard excerpts, taxonomy files (regulatory skills)
└── scripts/          # Python generators for XLSX/JSON output (regulatory skills)
```

PM skills (`samd-pm/`) contain only `SKILL.md` — they're prompt-based, not script-based.

## Generating Artifacts

The regulatory skills include Python scripts that generate XLSX or JSON output:

```bash
# Design controls traceability matrix
python skills/samd-regulatory/design-controls/scripts/generate_design_controls.py --example spo2

# Risk management FMEA
python skills/samd-regulatory/risk-management/scripts/generate_risk_analysis.py --example spo2

# FHIR R4 bundle
python skills/samd-regulatory/fhir-builder/scripts/generate_fhir_bundle.py --example spo2

# Change impact report
python skills/samd-regulatory/change-impact/scripts/analyze_change_impact.py --example spo2

# Design review package
python skills/samd-regulatory/design-review/scripts/package_design_review.py --review-type CDR --example spo2
```

See `examples/` in the repo root for pre-generated sample outputs.
