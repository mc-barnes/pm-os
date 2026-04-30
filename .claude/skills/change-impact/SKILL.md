---
name: change-impact
version: 1.0.0
description: >
  Analyze software change impact for SaMD regulatory compliance. Generates
  XLSX change impact reports with traceability to design controls and risk
  analysis, re-verification scope, and regulatory pathway assessment.
  Use when evaluating software changes, determining re-verification scope,
  assessing if a new 510(k) is needed, or creating change request documentation.
  Triggers: "change impact", "software change", "re-verification scope",
  "new 510(k) needed", "change request", "change control".
---

# Change Impact Analyzer

Analyze software change impact for SaMD regulatory compliance. Generates XLSX
change impact reports with traceability to design controls and risk analysis,
re-verification scope, and regulatory pathway assessment.

## When to Use

- Evaluating impact of a proposed software change on safety/effectiveness
- Determining re-verification scope after a code change
- Assessing whether a change triggers a new 510(k) submission
- Creating change request documentation for design history file (DHF)
- Preparing Letter to File evidence packages
- Reviewing cumulative changes for regulatory threshold

## When NOT to Use

- Initial product development (use design-controls skill instead)
- Risk analysis from scratch (use risk-management skill instead)
- Routine documentation updates with zero clinical/safety impact
- Changes to non-SaMD software (standard change management suffices)

## Quick Start

```bash
# Standalone example (no input files needed)
python scripts/analyze_change_impact.py --example spo2

# With upstream skill outputs
python scripts/analyze_change_impact.py --example spo2 \
  --design-controls ../design-controls/output/design-controls-spo2-ai-eval-pipeline.xlsx \
  --risk-analysis ../risk-management/output/risk-analysis-spo2-ai-eval-pipeline.xlsx

# Custom device name
python scripts/analyze_change_impact.py --device-name "my-device" --example spo2
```

Output: `output/change-impact-{device_name}.xlsx`

## XLSX Structure (5 Sheets)

### Sheet 1: Document_Control
Document metadata and approval signature block. Includes document title, version, device/software version, date generated, and signature rows for Prepared By, Reviewed By (QA), Approved By (Management), and Approved By (Regulatory).

### Sheet 2: Change_Request
| Column | Description |
|--------|-------------|
| CR ID | Change request identifier (e.g., CR-001) |
| Description | What is being changed and why |
| Files Changed | Comma-separated list of affected source files |
| Rationale | Clinical/business/safety justification for the change |
| Date | Date of change request |
| Requestor | Person or team requesting the change |

### Sheet 3: Impact_Trace
| Column | Description |
|--------|-------------|
| Changed File | Source file being modified |
| Affected DI IDs | Design Input IDs impacted by this file change |
| Affected HAZ IDs | Hazard IDs potentially impacted |
| Affected VER IDs | Verification IDs needing re-execution |
| Notes | Additional context on the trace relationship |

### Sheet 4: Reverification_Scope
| Column | Description |
|--------|-------------|
| VER ID | Verification item identifier |
| Test Name | Human-readable test/verification name |
| Rationale | Why this verification needs re-execution |
| Effort Estimate | Estimated hours to re-execute |
| Priority | Execution priority (P1/P2/P3) |

### Sheet 5: Regulatory_Assessment
| Column | Description |
|--------|-------------|
| Field | Assessment dimension |
| Value | Assessment result |

Fields: Classification, Pathway, Rationale, New 510(k) Required, Risk Analysis Update Required, Cumulative Impact Notes.

Includes a **510(k) Equivalence Assessment** sub-section with: Predicate Device, Predicate Intended Use, Performance Claims Affected, Substantial Equivalence Conclusion, and Evidence Required.

## Cross-Skill Integration

This skill can optionally consume outputs from:

- **design-controls skill** (`--design-controls path.xlsx`): Reads Design_Inputs sheet to auto-populate DI IDs and trace affected requirements.
- **risk-management skill** (`--risk-analysis path.xlsx`): Reads Hazard_Identification sheet to auto-populate HAZ IDs and trace affected hazards.

When input files are not provided, the script uses hardcoded template IDs from the SpO2 example for demonstration purposes.

## FDA Decision Flowchart

```
Is there a change to the device?
├── No → No submission needed (stop)
└── Yes
    Does the change affect safety or effectiveness?
    ├── No → Document in DHF only (stop)
    └── Yes
        Is it a new intended use?
        ├── Yes → NEW 510(k) REQUIRED
        └── No
            Could it affect performance?
            ├── Yes → Likely new 510(k) or Letter to File + testing
            └── No → Letter to File
```

**Software-specific (FDA 2023 Draft):**
- Major: New algorithm, new risk control, new intended use → New 510(k)
- Moderate: Param change, UI redesign, new data source → Letter to File + V&V
- Minor: Bug fix, cosmetic UI, documentation → DHF record only

## Classification Rules

### Minor
- **Definition**: No impact on safety, effectiveness, or intended use
- **Examples**: Typo fixes, cosmetic UI, documentation, logging
- **Regulatory**: DHF record only
- **Re-verification**: None or targeted unit tests
- **Approval**: Developer + Reviewer

### Major
- **Definition**: Affects performance, adds features, or modifies clinical behavior
- **Examples**: Threshold changes, new tier, algorithm params, new data source
- **Regulatory**: Letter to File with V&V evidence
- **Re-verification**: Affected integration/system tests + regression
- **Approval**: PM + Clinical + QA

### Critical
- **Definition**: Affects intended use, safety controls, or creates new hazards
- **Examples**: New indication, new risk control, safety-critical algorithm change
- **Regulatory**: New 510(k) or De Novo likely required
- **Re-verification**: Full system V&V
- **Approval**: PM + Clinical + Regulatory + QA + Executive

## Reference Files

- `references/fda-sw-changes.md` — FDA guidance on software changes and submission decisions
- `references/iec62304-change-mgmt.md` — IEC 62304 Clause 6/8 change management requirements
- `references/impact-classification.md` — Classification levels with decision aids

## Risk Analysis Update Decision Tree

When to update risk analysis after a software change:

1. **New failure mode introduced?** → Yes: Update risk analysis, add new HAZ
2. **Existing failure mode severity changed?** → Yes: Re-estimate risk, update controls
3. **New population at risk?** → Yes: Update intended use, re-analyze all hazards
4. **Risk control modified or added?** → Yes: Update residual risk assessment
5. **None of the above?** → Document: "Risk analysis reviewed [date], no update required. Rationale: [brief explanation]"

Always document the review decision, even when no update is needed.

## Verification Checklist

Before submitting a change impact report:

- [ ] All changed files identified and listed
- [ ] Each file traced to affected DI, HAZ, and VER IDs
- [ ] Classification level justified with rationale
- [ ] Regulatory pathway determined using FDA flowchart
- [ ] Re-verification scope includes effort estimates
- [ ] Risk analysis update need assessed (new hazards? changed severity?)
- [ ] Cumulative impact considered (minor + minor + minor = major?)
- [ ] Letter to File template prepared (if applicable)
- [ ] Approval authorities identified per classification level
- [ ] Output XLSX reviewed by QA before inclusion in DHF
