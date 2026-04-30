---
type: audit
status: approved
owner: [quality lead]
last-reviewed: 2026-04-30
---
# Common FDA 483 Findings — SaMD / Design Controls

Reference library of frequently cited findings under 21 CFR 820.30 and related sections. Use for audit prep and self-assessment.

## Design Controls (21 CFR 820.30)

| Finding Area | Typical 483 Language | Prevention |
|-------------|---------------------|------------|
| 820.30(a) Design planning | "Failed to establish and maintain procedures to control the design of the device" | Maintain current design plan in regulatory/design-history/ |
| 820.30(c) Design inputs | "Design input requirements not documented" or "Incomplete design inputs" | Every UN traces to at least one DI in design-controls XLSX |
| 820.30(d) Design outputs | "Design outputs do not meet design input requirements" | Traceability matrix shows DO → DI with verification |
| 820.30(f) Design verification | "No objective evidence of verification" | VER records with quantitative pass criteria and test data |
| 820.30(g) Design validation | "Validation not performed under actual or simulated use conditions" | VAL records with realistic use conditions documented |
| 820.30(i) Design changes | "Changes not reviewed, verified, or validated before implementation" | Change control record in regulatory/change-control/ for every change |
| 820.30(j) DHF | "DHF does not contain or reference required records" | DHF index in regulatory/design-history/ links to all records |

## Risk Management (ISO 14971 / 820.30(g))
| Finding Area | Typical Language | Prevention |
|-------------|-----------------|------------|
| Risk analysis incomplete | "Hazard analysis does not include all known hazards" | Systematic hazard identification using hazard taxonomy |
| Risk controls not verified | "No evidence risk control measures were verified for effectiveness" | Every RC has verification method in Risk_Controls sheet |
| Residual risk not evaluated | "Residual risk not assessed after implementation of controls" | Residual_Risk sheet completed for every controlled hazard |

## CAPA (21 CFR 820.198 / ISO 13485 8.5.2-8.5.3)
| Finding Area | Typical Language | Prevention |
|-------------|-----------------|------------|
| No root cause | "CAPA does not include investigation of root cause" | Root cause analysis required in CAPA template |
| Effectiveness not verified | "No evidence of verification of effectiveness" | CAPA template includes effectiveness check with timeline |

## Software (IEC 62304)
| Finding Area | Typical Language | Prevention |
|-------------|-----------------|------------|
| SOUP not identified | "Third-party software components not identified or evaluated" | Maintain SOUP register in engineering/sdlc/ |
| Safety class not assigned | "Software safety classification not documented" | Safety class rationale in design-controls XLSX |
