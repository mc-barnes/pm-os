---
type: prd
status: draft
owner: "@tcheng"
related:
  - clinical/usability/usability-spo2-v1.md
  - clinical/intended-use/intended-use-spo2-v1.md
---

# Expected findings:
# - Critical: No urgency level leading the handoff — clinician must parse entire output to determine action priority
# - Critical: Researcher jargon (AUC, percentile, classifier confidence) not actionable for telehealth nurse (IEC 62366-1 §5.1)
# - Important: No patient-specific context (gestational age, baseline SpO2, trend direction)
# - Important: "Monitor closely" is not a specific action — handoff must specify what to do and when to escalate
# - Expected verdict: NEEDS REVISION

# Clinical Handoff Output Specification: PulseView SpO2 Monitor

## 1. Purpose

When the PulseView system identifies a patient requiring clinical attention, it generates a structured handoff summary for the receiving clinician. This document specifies the content and format of the handoff output displayed on the monitoring dashboard and sent via secure notification.

## 2. Handoff Output Format

The system generates the following output when a monitoring event requires clinician review:

```
PATIENT HANDOFF SUMMARY
━━━━━━━━━━━━━━━━━━━━━━
Patient ID: [MRN]
Bed: [Location]
Timestamp: [ISO 8601]

CLASSIFICATION RESULT
Model output: Desaturation event classifier returned positive
  prediction (p=0.73, AUC=0.91 on validation set)
SpO2 percentile rank: 12th percentile relative to age-matched
  cohort distribution (n=4,200, 95% CI: 8th-16th)
Trend regression: -2.1 SpO2 points/hr (R²=0.84, p<0.001)

EVENT CHARACTERIZATION
Mean SpO2 during event window: 87.3%
Nadir: 82.1% at 14:23:07
Duration below 90th percentile threshold: 4 min 12 sec
Signal quality index: 0.76 (adequate for classification)

RISK STRATIFICATION
Composite risk score: 0.68/1.00 (moderate-high)
Contributing factors:
  - SpO2 trajectory (weight: 0.35): declining
  - Heart rate variability (weight: 0.25): reduced
  - Historical event frequency (weight: 0.20): 3 events/8hr
  - Gestational age factor (weight: 0.20): preterm adjustment applied

RECOMMENDATION
Monitor closely. Consider clinical assessment if trending continues.
Review historical pattern for context.
```

## 3. Output Delivery

The handoff summary is displayed on the central monitoring dashboard in a scrollable text panel. The same content is sent as a push notification to the assigned clinician's mobile device.

## 4. Intended Recipients

The handoff output is designed for use by:
- Bedside NICU nurses
- Telehealth monitoring nurses (remote monitoring center)
- Charge nurses during shift transitions

## 5. Output Frequency

A handoff summary is generated each time the classification model identifies a positive event. During periods of frequent desaturation, summaries may be generated as often as every 2-3 minutes.

## 6. Clinical Decision Support

The handoff output is intended to support, not replace, clinical judgment. The composite risk score provides a quantitative summary that clinicians can use alongside their clinical assessment to prioritize patient attention.

## 7. Training Requirements

Clinicians will receive a 30-minute online training module covering interpretation of the handoff output fields, including the classification probability, percentile ranking, and composite risk score methodology.
