---
type: risk-record
status: draft
owner: "@agarcia"
related:
  - regulatory/design-controls/design-controls-spo2-v1.xlsx
  - clinical/intended-use/intended-use-spo2-v1.md
---

# Expected findings:
# - SAFETY FINDING: No foreseeable misuse analysis (ISO 14971:2019 §5.4)
# - SAFETY FINDING: Incomplete hazard chains — hazard jumps to harm, skipping hazardous situation and sequence of events (§4.4)
# - GAP: "Team brainstorm" is not a systematic hazard identification method (§4.3 requires recognized techniques)
# - GAP: No fault condition analysis — only normal use considered (§4.2)
# - Expected verdict: SAFETY CONCERN

# Risk Analysis: PulseView SpO2 Monitor

## 1. Scope

This risk analysis covers the PulseView SpO2 monitoring software used in the NICU setting. The analysis identifies hazards associated with the intended use of the device and documents risk controls.

## 2. Risk Analysis Methodology

Hazards were identified through a team brainstorm session held on 2026-01-15. Participants included the software lead, product manager, and one clinical advisor. The session lasted 90 minutes and generated the hazard list below.

Risks were estimated using a 3×3 severity/probability matrix. Risk acceptability was determined by the product manager.

## 3. Identified Hazards

### HAZ-001: Incorrect SpO2 Display
**Hazard:** System displays incorrect SpO2 value
**Harm:** Clinician makes incorrect treatment decision
**Severity:** Critical | **Probability:** Low | **Risk Level:** Medium
**Control:** Display updates at 1 Hz with moving average filter
**Residual Risk:** Low

### HAZ-002: Delayed Alarm
**Hazard:** Alarm triggers late
**Harm:** Delayed intervention for desaturation
**Severity:** Critical | **Probability:** Low | **Risk Level:** Medium
**Control:** System processes alarms within 2-second latency requirement
**Residual Risk:** Low

### HAZ-003: System Downtime
**Hazard:** Monitoring system becomes unavailable
**Harm:** Gap in patient monitoring coverage
**Severity:** High | **Probability:** Low | **Risk Level:** Medium
**Control:** 99.95% uptime target with redundant server architecture
**Residual Risk:** Low

### HAZ-004: Data Export Error
**Hazard:** CSV trend export contains incorrect values
**Harm:** Clinician reviews inaccurate historical data
**Severity:** Medium | **Probability:** Low | **Risk Level:** Low
**Control:** Data validation checks before export
**Residual Risk:** Low

## 4. Risk Summary

All identified hazards have been evaluated and controlled. Residual risk for all hazards is Low, which is within our acceptable risk threshold. No further risk reduction measures are required.

## 5. Conclusion

The PulseView SpO2 Monitor risk analysis is complete. Four hazards were identified and all have been reduced to acceptable levels through implementation of design controls. The overall residual risk of the device is acceptable.
