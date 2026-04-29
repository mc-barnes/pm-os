---
name: design-review
description: >
  Package design review gate documentation (PDR/CDR/FDR) as XLSX + markdown
  narrative. Generates artifact checklists, requirements status, risk status,
  and sign-off sheets with GO/NO-GO recommendation based on completeness
  formulas. Use when preparing for design reviews, creating review packages,
  or generating GO/NO-GO gate documentation for medical devices under
  ISO 13485, FDA 21 CFR 820.30, and IEC 62304 (software lifecycle).
  Triggers: "design review", "PDR", "CDR", "FDR", "review package",
  "design review gate", "GO NO-GO", "preliminary design review",
  "critical design review", "final design review".
---

# Design Review Packager

Package design review gate documentation (PDR/CDR/FDR) as XLSX + markdown narrative for medical device development under ISO 13485, FDA 21 CFR 820.30, and IEC 62304 (software lifecycle).

## When to Use

- Preparing for a design review gate (PDR, CDR, or FDR)
- Creating a structured review package with checklists and status tracking
- Generating GO/NO-GO gate documentation with completeness formulas
- Assembling sign-off sheets for cross-functional review teams
- Integrating upstream design controls, risk analysis, or change impact outputs
- Documenting software lifecycle gates per IEC 62304 (software safety classification, SOUP assessment, software release)

## When NOT to Use

- For ongoing design work (use design-controls skill instead)
- For risk analysis authoring (use risk-management skill instead)
- For change impact assessment (use change-impact skill instead)
- For informal design discussions that don't require formal gate documentation
- When you need only a single artifact (e.g., just a traceability matrix)

## Quick Start

```bash
# CDR with SpO2 example data
python scripts/package_design_review.py --review-type CDR --example spo2

# PDR with custom device name
python scripts/package_design_review.py --review-type PDR --device-name "Cardiac Monitor v1.0"

# FDR with upstream skill outputs
python scripts/package_design_review.py --review-type FDR --example spo2 \
  --design-controls ../skill-design-controls/output/design-controls-spo2-ai-eval-pipeline.xlsx \
  --risk-analysis ../skill-risk-management/output/risk-analysis-spo2-ai-eval-pipeline.xlsx \
  --change-impact ../skill-change-impact/output/change-impact-spo2-ai-eval-pipeline.xlsx
```

**Outputs:**
- `output/design-review-{TYPE}-{device-name}.xlsx` — 6-sheet XLSX workbook
- `output/design_review_narrative.md` — Executive summary + action items

## XLSX Structure

The workbook contains 6 sheets:

### Sheet 1: Document_Control
| Field | Value |
|-------|-------|
| Document Title | Design Review Package — {review_type} — {device_name} |
| Document Version | 1.0 |
| Device/Software Version | (device/software name) |
| Date Generated | (current date) |
| Review Type | PDR/CDR/FDR |
| Approval Signatures | Role / Name / Date / Signature (Prepared By, QA, Management) |

### Sheet 2: Review_Summary
| Field | Value |
|-------|-------|
| Review Type | CDR -- Critical Design Review |
| Device Name | (from --device-name or --example) |
| Date | (current date) |
| Attendees | (cross-functional team list) |
| Overall Completeness | =Artifact_Checklist completeness formula |
| Recommendation | =IF(completeness>=90%,"GO",IF(>=75%,"CONDITIONAL","NO-GO")) |

### Sheet 3: Artifact_Checklist
| Column | Description |
|--------|-------------|
| Artifact | Checklist item name (PDR: 25, CDR: 56, FDR: 92) |
| Required (Y/N) | Whether the artifact is required for this review |
| Provided (Y/N) | Whether the artifact has been provided |
| Completeness % | `=COUNTIF(Provided,"Y")/COUNTIF(Required,"Y")` |

### Sheet 4: Requirements_Status
| Column | Description |
|--------|-------------|
| Total Requirements | Count of user needs + design inputs |
| % Verified | Percentage with verification evidence |
| % Validated | Percentage with validation evidence |
| Open Items | Count of unresolved requirements |

### Sheet 5: Risk_Status
| Column | Description |
|--------|-------------|
| Total Hazards | Count of identified hazards |
| Unacceptable Remaining | Hazards still above acceptable threshold |
| ALARP | Hazards reduced as low as reasonably practicable |
| Acceptable | Hazards at acceptable risk level |
| Open Risk Controls | Controls not yet implemented/verified |

### Sheet 6: Sign_Off
| Column | Description |
|--------|-------------|
| Role | Functional role (PM, Clinical, QA, etc.) |
| Name | Reviewer name |
| Date | Sign-off date |
| Approval | Approve / Conditional / Reject / Pending |

## Markdown Narrative

Also generates `output/design_review_narrative.md` containing:

1. **Executive Summary** — Device, review type, overall completeness, high-level status
2. **Key Findings** — Requirements status, risk status, traceability, notable gaps
3. **Action Items** — Table with action, owner, due date
4. **Recommendation** — GO / CONDITIONAL GO / NO-GO with rationale

## Review Types

### PDR (Preliminary Design Review)
- **Gate**: Concept -> Detailed Design
- **Focus**: Is the concept viable? Are requirements clear?
- **Checklist**: 25 items (user needs, architecture, initial risk, V&V strategy)
- **Key question**: Can we proceed to detailed design?

### CDR (Critical Design Review)
- **Gate**: Detailed Design -> Implementation/V&V
- **Focus**: Is the design complete enough to build?
- **Checklist**: 56 items (all PDR items + detailed specs, traceability, V&V protocols, 820.30(c) design input quality)
- **Key question**: Are we ready to start verification and validation?

### FDR (Final Design Review)
- **Gate**: V&V -> Release/Transfer
- **Focus**: Is the product ready to ship?
- **Checklist**: 92 items (all CDR items + V&V results, V&V distinction, regulatory package, launch readiness)
- **Key question**: Can we release to market?

## Cross-Skill Integration

The script optionally reads upstream XLSX files from other skills:

| Flag | Source Skill | Populates |
|------|-------------|-----------|
| `--design-controls path.xlsx` | design-controls | Requirements_Status sheet |
| `--risk-analysis path.xlsx` | risk-management | Risk_Status sheet |
| `--change-impact path.xlsx` | change-impact | Action items in narrative |

When upstream files are not provided, the script uses example data (with `--example`) or leaves fields blank for manual entry.

## Reference Files

- `references/iso13485-design-review.md` — ISO 13485 Clause 7.3.5 requirements, participant roles, review type definitions
- `references/review-checklists.md` — Full PDR (25), CDR (56), FDR (92) item checklists
- `references/fda-design-control.md` — FDA 21 CFR 820.30 mapping, common 483 observations

## Verification Checklist

After generating a review package, verify:

- [ ] XLSX has exactly 6 sheets (Document_Control, Review_Summary, Artifact_Checklist, Requirements_Status, Risk_Status, Sign_Off)
- [ ] Artifact_Checklist has correct item count for review type (PDR=25, CDR=56, FDR=92)
- [ ] Completeness formula calculates correctly (COUNTIF-based)
- [ ] GO/NO-GO formula reflects completeness thresholds (>=90% GO, >=75% CONDITIONAL, <75% NO-GO)
- [ ] Conditional formatting applied (green/yellow/red)
- [ ] Narrative markdown has Executive Summary, Key Findings, Action Items, Recommendation
- [ ] Sign-off sheet includes all required roles per ISO 13485
- [ ] If upstream XLSX provided, Requirements_Status and Risk_Status populated from source data
