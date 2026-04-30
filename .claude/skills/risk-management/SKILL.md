---
name: risk-management
version: 1.0.0
description: >
  Generate ISO 14971 risk management documentation as XLSX — hazard analysis,
  risk estimation/evaluation, FMEA with RPN calculations, and residual risk
  assessment. Use when building risk management files, FMEA worksheets,
  hazard analyses, or risk acceptability matrices for medical devices.
  Triggers: "risk management", "ISO 14971", "FMEA", "hazard analysis",
  "risk acceptability matrix", "risk controls", "residual risk".
---

# Risk Management Skill

## When to Use
- Building or updating a risk management file for a medical device (SaMD or hardware)
- Creating hazard analysis, risk estimation, risk evaluation, or FMEA worksheets
- Generating risk acceptability matrices (5x5 severity x probability)
- Documenting risk controls and residual risk assessment
- Preparing ISO 14971-compliant documentation for regulatory submissions
- Populating risk records for design reviews or audits

## When NOT to Use
- General project risk management (schedule, budget) -- this is for *patient safety* risk
- Cybersecurity-only risk assessment (for cybersecurity risk, use IEC 80001-1 series (network security) or AAMI TIR57; for industrial controls, reference IEC 62443)
- When you need a full Risk Management Plan (this generates the *analysis*, not the plan)
- Non-medical-device software where ISO 14971 does not apply

## Quick Start

```bash
# Generate SpO2 AI example with all 8 sheets
python scripts/generate_risk_analysis.py --example spo2

# Generate blank template for a custom device
python scripts/generate_risk_analysis.py --device-name "Cardiac Monitor v2"
```

Output lands in `output/risk-analysis-{device_name}.xlsx`.

## XLSX Structure -- 8 Sheets

### 1. Document_Control
| Row | Content |
|-----|---------|
| 1 | "Document Control" (merged header) |
| 3-6 | Document Title, Version, Device/SW Version, Date Generated |
| 8 | "Approval Signatures" (merged) |
| 9-12 | Role / Name / Date / Signature (Prepared By, Reviewed By QA, Approved By Management) |

### 2. Hazard_Identification
| Column | Description |
|--------|-------------|
| Hazard ID | HAZ-001, HAZ-002, ... |
| Hazard | Source of potential harm |
| Hazardous Situation | Circumstance of exposure |
| Harm | Resulting injury or damage to health |
| Sequence of Events | Chain from hazard to harm |

### 3. Risk_Estimation
| Column | Description |
|--------|-------------|
| Hazard ID | Links to Hazard_Identification |
| Severity (S) | S1-S5 scale |
| Probability (P) | P1-P5 scale |
| Risk Level | Formula: lookup from 5x5 matrix (Acceptable / AFAP / Unacceptable) |

### 4. Risk_Evaluation
| Column | Description |
|--------|-------------|
| Hazard ID | Links to Risk_Estimation |
| Risk Level | Pulled from Risk_Estimation |
| Acceptability | Formula-driven from matrix lookup |
| Rationale | Risk reduction rationale if AFAP zone |

### 5. Risk_Controls
| Column | Description |
|--------|-------------|
| Control ID | RC-001, RC-002, ... |
| Hazard ID | Links to Hazard_Identification |
| Control Measure | Description of the risk control |
| Type | inherent safety / protective measure / information for safety |
| Verification Method | How effectiveness is verified |

### 6. Residual_Risk
| Column | Description |
|--------|-------------|
| Control ID | Links to Risk_Controls |
| Hazard ID | Links to Hazard_Identification |
| Post-Control Severity | S1-S5 |
| Post-Control Probability | P1-P5 |
| Residual Risk Level | Formula: lookup from 5x5 matrix |
| Rationale | Risk reduction rationale per ISO 14971:2019 (red-highlighted if AFAP zone and empty) |

### 7. Overall_Residual_Risk (ISO 14971 Clause 7)
| Column | Description |
|--------|-------------|
| Category | Assessment area (Individual Risks, Interactions, Clusters, Benefit-Risk, Post-Market) |
| Description | What is being assessed |
| Status | Acceptable / Reviewed / Documented / Defined (or formula-driven) |
| Notes | Detailed rationale and analysis |

Includes a summary formula row: "ACCEPTABLE -- Proceed to release" or "REVIEW REQUIRED -- Resolve open items"

> **Note:** This is a process FMEA for identifying failure modes and prioritizing design improvements.
> RPN (Risk Priority Number) is not a valid patient risk acceptability metric per ISO 14971:2019 Annex G
> — ordinal scale multiplication does not yield meaningful risk levels. Patient risk acceptability is
> determined solely by the 5×5 severity × probability matrix on sheets 3-6. Do not use RPN values
> for regulatory risk acceptability decisions.

### 8. FMEA
| Column | Description |
|--------|-------------|
| Hazard ID | Links to Hazard_Identification |
| Failure Mode | How the function fails |
| Effect | Consequence of failure |
| Cause | Root cause |
| Severity (S) | 1-10 scale |
| Occurrence (O) | 1-10 scale |
| Detection (D) | 1-10 scale |
| RPN | Formula: =S*O*D |

## Severity / Probability Quick Reference

| Level | Severity | Probability |
|-------|----------|-------------|
| 1 | S1 Negligible | P1 Incredible (<1 in 1M) |
| 2 | S2 Minor | P2 Improbable (1 in 100K) |
| 3 | S3 Serious | P3 Remote (1 in 10K) |
| 4 | S4 Critical | P4 Occasional (1 in 1K) |
| 5 | S5 Catastrophic | P5 Frequent (>1 in 100) |

## Risk Acceptability Matrix (5×5)

Defined in `regulatory/risk-management/risk-acceptability-matrix.md` (document-controlled).
Read that file for the current matrix. Do not hard-code criteria here — the matrix is owned by the Risk Management Plan.

## Reference Files
- `references/iso14971-structure.md` -- ISO 14971 process phases, required documents, key definitions
- `references/hazard-taxonomy.md` -- Hazard categories per ISO 14971 Annex C, software-specific hazards
- `references/severity-probability.md` -- Full scale definitions, matrix, FMEA mapping, AFAP criteria

## Verification Checklist

Before submitting a risk management file, verify:

- [ ] Every hazard has a unique ID (HAZ-nnn)
- [ ] Every hazard traces through all 6 sheets (identification -> estimation -> evaluation -> control -> residual)
- [ ] Severity and probability values use the defined scales (S1-S5, P1-P5)
- [ ] Risk Level is calculated via formula, not hardcoded
- [ ] Every Unacceptable risk has at least one risk control
- [ ] Every risk control has a verification method
- [ ] Residual risk is re-evaluated after controls
- [ ] No residual risk remains Unacceptable
- [ ] AFAP decisions include documented rationale (risk reduced as far as possible per ISO 14971:2019)
- [ ] Process FMEA: RPN is calculated via formula (=S*O*D), not hardcoded (process prioritization only — not for patient risk acceptability)
- [ ] Process FMEA: RPNs above threshold (typically 100-150) have action items for design improvement
- [ ] Overall residual risk benefit-risk conclusion is documented
