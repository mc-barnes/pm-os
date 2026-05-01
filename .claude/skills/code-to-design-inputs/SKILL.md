---
name: code-to-design-inputs
version: 1.0.0
description: >
  Reverse-engineer design inputs from source code in an existing codebase. Walks
  the source tree using 6 inclusion heuristics to identify design-input-worthy
  code boundaries. Produces an IEC 62304 Clause 5.2 compliant traceability matrix
  XLSX with companion gap report.
  Triggers: "design inputs from code", "code-to-design-inputs",
  "reverse-engineer design inputs", "retrospective design controls",
  "design input traceability from code".
---

# code-to-design-inputs

Reverse-engineer design inputs from source code in an existing codebase. Identifies API boundaries, configuration surfaces, integration points, clinical thresholds, data retention policies, and user-facing error messages. Produces an IEC 62304 Clause 5.2 compliant traceability matrix XLSX with a companion gap report documenting where human evaluation is required.

## When to Use

- Existing codebase with no design input traceability — building retrospectively
- Preparing for a first regulatory submission and need to inventory software requirements
- Auditing design input completeness against a PRD or intended use statement
- Running as part of a gap analysis effort (via `/gap-analysis design-inputs`)
- Identifying undocumented code behaviors that should be in the design controls matrix

## When NOT to Use

- Greenfield project — use the prospective design controls skill instead
- Updating an existing, maintained traceability matrix — use change-impact instead
- Pure architecture review without IEC 62304 context — use code-review instead

## Quick Start

```bash
# Generate from your repo
python .claude/skills/code-to-design-inputs/scripts/generate_design_inputs.py \
  --source /path/to/repo

# Generate with PRD cross-reference
python .claude/skills/code-to-design-inputs/scripts/generate_design_inputs.py \
  --source /path/to/repo --prd /path/to/prd.md

# Generate with hazard candidate priority tiers
python .claude/skills/code-to-design-inputs/scripts/generate_design_inputs.py \
  --source /path/to/repo --hazard-candidates output/hazard-candidates-*.xlsx

# Generate example output (no repo needed)
python .claude/skills/code-to-design-inputs/scripts/generate_design_inputs.py --example
```

## Inclusion Heuristics

| # | Heuristic | What It Detects | DI Type |
|---|-----------|----------------|---------|
| 1 | API Boundaries | Routes, exported functions, public interfaces | Functional / Interface |
| 2 | Configuration Surfaces | Env vars, feature flags, threshold constants | Functional / Performance / Safety |
| 3 | Integration Points | External API calls, EHR writes, FHIR endpoints | Interface |
| 4 | Clinical Decision Thresholds | Alarm limits, dosing calculations, scoring cutoffs | Safety |
| 5 | Data Retention/Deletion | Storage duration, purge policies, data lifecycle | Functional |
| 6 | User-Facing Error Messages | Error text shown to clinicians or patients | Safety / Functional |

The inclusion heuristics are documented in `references/traceability-from-code.md` with regex patterns, examples, and DI type classification rules.

## XLSX Structure

### Sheet: Design_Inputs

| Column | Auto-populated? | Notes |
|--------|----------------|-------|
| UN ID | Proposed | Proposed user need — GAP until linked |
| DI ID | Yes | DI-001, DI-002, ... |
| Description | Yes | Design input derived from code analysis |
| Source (code) | Yes | file_path:line_number citation |
| Type | Yes | Functional / Performance / Safety / Interface |
| Priority | Yes (if HC provided) | P1 (safety-critical) / P2 (clinical) / P3 (functional) |
| Rationale | No — GAP | Requires human input — why this behavior exists |
| Rationale Source | No — GAP | Document, paper, meeting minutes, etc. |
| SW Safety Class | No — GAP | A / B / C — requires risk analysis context |
| Gap Status | Formula | COMPLETE / GAP |

### Sheet: Document_Control

Standard document control sheet with device name, date, and approval signatures.

## Priority Tiers

When `--hazard-candidates` is provided, design inputs are prioritized by safety criticality:

| Tier | Criteria | Implication |
|------|----------|-------------|
| P1 (safety-critical) | DI source overlaps hazard candidate code region | Rationale gaps block submission |
| P2 (clinical) | DI type is Safety or heuristic is clinical_thresholds | Rationale gaps need clinical SME |
| P3 (functional) | All other design inputs | Rationale gaps can be addressed in sequence |

Without `--hazard-candidates`, P2/P3 tiers are still assigned based on type and heuristic.

## PRD Cross-Reference

When `--prd` is provided, the skill cross-references discovered DIs against PRD statements using keyword matching:

| Gap Type | Meaning | Owner |
|----------|---------|-------|
| Documentation Gap | Code behavior exists but PRD doesn't mention it | Product / RA |
| Implementation Gap | PRD describes behavior that code doesn't implement | Engineering / Product |

## Gap Report Categories

| Category | Owner | Description |
|----------|-------|-------------|
| Rationale required | Engineering / Product | Design rationale not documented |
| SW Safety Class required | Engineering / RA | Safety classification not assigned |
| Documentation gap | Product / RA | Code behavior not in PRD |
| Implementation gap | Engineering / Product | PRD behavior not in code |

## Reference Files

- `references/traceability-from-code.md` — Heuristic patterns, DI type classification, PRD cross-ref methodology

## Verification Checklist

Before accepting a generated design input traceability matrix:

- [ ] All heuristics ran against the source tree
- [ ] DI IDs are sequential with no gaps (DI-001, DI-002, ...)
- [ ] Every DI has a source file:line citation
- [ ] Rationale, Rationale Source, and SW Safety Class columns are GAP (not auto-filled)
- [ ] Gap Status formula correctly computes COMPLETE / GAP
- [ ] PRD cross-reference results are plausible (if --prd provided)
- [ ] Priority tiers are correct (if --hazard-candidates provided)
- [ ] No network calls were made (all data from local source files)
- [ ] Companion gap report references scope statement if provided
- [ ] File naming follows convention: `design-inputs-{source-name}.xlsx`

## Implementation Notes

- Script uses only `openpyxl` + stdlib — no heavy dependencies
- Python 3.11+ required (match syntax)
- No network calls — all analysis from local source files
- Rationale, Rationale Source, and SW Safety Class are **never** auto-populated — always "GAP"
- Gap Status formula: `=IF(OR(Rationale="GAP",RationaleSource="GAP",SWSafetyClass="GAP"),"GAP","COMPLETE")`
