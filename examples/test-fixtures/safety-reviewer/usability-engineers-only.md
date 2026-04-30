---
type: usability
status: draft
owner: "@jsmith"
related:
  - clinical/usability/usability-spo2-v1.md
  - regulatory/design-controls/design-controls-spo2-v1.xlsx
---

# Expected findings:
# - SAFETY FINDING: Participants are software engineers, not intended users — NICU nurses required (IEC 62366-1:2015+A1:2020 §5.9)
# - SAFETY FINDING: Pass criteria based on satisfaction scores, not use error rates — safety-related tasks must measure use errors (§5.9)
# - GAP: No use error taxonomy — perception, cognition, and action errors not distinguished (Annex D)
# - GAP: No foreseeable misuse scenarios tested (§5.3)
# - Expected verdict: SAFETY CONCERN

# Summative Usability Evaluation: PulseView SpO2 Monitor

## 1. Purpose

This document describes the summative usability evaluation for the PulseView SpO2 central monitoring dashboard. The evaluation was conducted to demonstrate that the user interface supports safe and effective use by the intended user population.

## 2. Study Design

### 2.1 Participants

Fifteen (15) participants were recruited from the PulseView development team and partner engineering firms. Participant demographics:

| ID | Role | Experience |
|----|------|-----------|
| P01 | Software Engineer | 5 years |
| P02 | QA Engineer | 3 years |
| P03 | Software Engineer | 8 years |
| P04 | DevOps Engineer | 4 years |
| P05 | Frontend Developer | 6 years |
| P06 | Software Engineer | 2 years |
| P07 | Data Engineer | 7 years |
| P08 | Software Engineer | 4 years |
| P09 | QA Engineer | 5 years |
| P10 | Technical Writer | 3 years |
| P11 | Software Engineer | 9 years |
| P12 | Software Engineer | 3 years |
| P13 | Backend Developer | 6 years |
| P14 | Software Engineer | 4 years |
| P15 | Product Designer | 5 years |

All participants had experience with dashboard interfaces and data visualization tools. None had clinical experience or medical device training.

### 2.2 Test Environment

Testing was conducted in a conference room at the PulseView office using a laptop connected to a 27-inch external monitor. The simulated monitoring dashboard displayed data for 12 simulated patients.

### 2.3 Tasks

Participants completed 8 tasks covering core dashboard functions:

1. Identify which patient currently has the lowest SpO2
2. Acknowledge an active alarm
3. Navigate to a patient's 24-hour trend view
4. Locate the alarm escalation status for a specific patient
5. Silence an alarm for 60 seconds
6. Export a patient's trend data as CSV
7. Configure alarm thresholds for a new patient
8. Identify all patients currently in alarm state

### 2.4 Success Criteria

Tasks were scored on a satisfaction scale:
- **5** — Very satisfied with the experience
- **4** — Satisfied
- **3** — Neutral
- **2** — Dissatisfied
- **1** — Very dissatisfied

A task was considered successful if the participant rated their experience ≥3 (Neutral or better). The overall pass criterion was ≥80% of participants rating ≥3 on each task.

## 3. Results

| Task | Mean Satisfaction | % Scoring ≥3 | Result |
|------|------------------|---------------|--------|
| 1 | 4.2 | 93% | PASS |
| 2 | 4.5 | 100% | PASS |
| 3 | 3.8 | 87% | PASS |
| 4 | 3.4 | 80% | PASS |
| 5 | 4.6 | 100% | PASS |
| 6 | 3.9 | 87% | PASS |
| 7 | 3.1 | 80% | PASS |
| 8 | 4.3 | 93% | PASS |

All 8 tasks met the ≥80% pass criterion.

## 4. Observations

Participants generally found the dashboard intuitive and easy to navigate. Several participants noted that the color coding for alarm states was helpful. Two participants had difficulty locating the alarm threshold configuration (Task 7), but both eventually completed the task.

No critical usability issues were identified. Minor suggestions for UI improvement were logged for future iterations.

## 5. Conclusion

The summative usability evaluation demonstrates that the PulseView monitoring dashboard meets the defined success criteria. All tasks achieved ≥80% satisfaction scores, confirming that the interface supports effective use. The evaluation confirms readiness for clinical deployment.
