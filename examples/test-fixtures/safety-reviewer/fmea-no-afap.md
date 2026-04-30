---
type: risk-record
status: draft
owner: "@tcheng"
related:
  - regulatory/risk-management/risk-spo2-v1.xlsx
  - regulatory/design-controls/design-controls-spo2-v1.xlsx
---

# Expected findings:
# - SAFETY FINDING: Residual risk rated "Low" without AFAP (as far as practicable) rationale (ISO 14971:2019 §7.5)
# - SAFETY FINDING: Controls jump directly to IFU warnings, no hierarchy justification — inherent safety > protective measures > information for safety (§7.1)
# - GAP: No analysis of new risks introduced by controls (§7.4)
# - GAP: No cumulative residual risk evaluation across all hazards (§8)
# - Expected verdict: SAFETY CONCERN

# FMEA: PulseView SpO2 Alarm System

## 1. Scope

This Failure Mode and Effects Analysis covers the PulseView SpO2 alarm subsystem, including alarm generation, notification, and escalation functions.

## 2. FMEA Methodology

The FMEA was conducted using a standard Severity × Occurrence × Detection (S×O×D) scoring model with scales of 1-10 for each dimension. Risk Priority Numbers (RPN) are calculated as S×O×D.

## 3. Failure Mode Analysis

### FM-001: False Alarm (SpO2 artifact triggers alarm)
| Parameter | Value |
|-----------|-------|
| Failure Mode | Motion artifact causes SpO2 to read below threshold |
| Effect | Unnecessary alarm, clinician distraction |
| Severity | 4 |
| Occurrence | 7 |
| Detection | 3 |
| RPN | 84 |
| Current Control | 5-second averaging filter |
| Recommended Action | Add note to IFU that motion may cause false alarms |
| Residual Risk | Low |

### FM-002: Missed Alarm (true desaturation not detected)
| Parameter | Value |
|-----------|-------|
| Failure Mode | SpO2 drops below threshold but alarm does not trigger |
| Effect | Clinician unaware of desaturation, potential patient harm |
| Severity | 9 |
| Occurrence | 2 |
| Detection | 5 |
| RPN | 90 |
| Current Control | Alarm system tested during manufacturing |
| Recommended Action | Add warning to IFU: "Do not rely solely on this system" |
| Residual Risk | Low |

### FM-003: Alarm Escalation Failure
| Parameter | Value |
|-----------|-------|
| Failure Mode | Push notification to charge nurse fails to deliver |
| Effect | Escalation pathway interrupted, delayed response |
| Severity | 7 |
| Occurrence | 3 |
| Detection | 4 |
| RPN | 84 |
| Current Control | Network monitoring |
| Recommended Action | Add to IFU that network connectivity required for escalation |
| Residual Risk | Low |

### FM-004: Alarm Silence Abuse
| Parameter | Value |
|-----------|-------|
| Failure Mode | Clinician repeatedly silences valid alarms |
| Effect | Alarm fatigue leads to missed events |
| Severity | 8 |
| Occurrence | 5 |
| Detection | 2 |
| RPN | 80 |
| Current Control | None |
| Recommended Action | Add guidance to IFU about alarm silence best practices |
| Residual Risk | Low |

## 4. RPN Summary

| Failure Mode | RPN | Residual Risk |
|-------------|-----|---------------|
| FM-001 | 84 | Low |
| FM-002 | 90 | Low |
| FM-003 | 84 | Low |
| FM-004 | 80 | Low |

All failure modes have residual risk rated as Low. The highest RPN is 90 (FM-002: Missed Alarm). The recommended controls for all failure modes are IFU-based warnings and instructions.

## 5. Conclusion

The FMEA identified four failure modes in the alarm subsystem. All have been evaluated and appropriate controls identified. Residual risk for all failure modes is acceptable.
