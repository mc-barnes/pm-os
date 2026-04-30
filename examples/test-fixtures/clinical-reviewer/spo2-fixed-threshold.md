---
type: prd
status: draft
owner: "@jsmith"
related:
  - regulatory/risk-management/risk-spo2-v1.xlsx
  - clinical/intended-use/intended-use-spo2-v1.md
---

# Expected findings:
# - Critical: No gestational age adjustment — premature infants baseline 92-95%, term 97-100% (Castillo et al., 2008)
# - Critical: No depth×duration analysis — threshold crossing alone generates noise (SatSeconds, Poets et al.)
# - Important: No transient self-resolving hypoxemia handling (brief desats in healthy preterms are normal)
# - Important: No motion artifact / signal quality gating (low SIQ data should suppress alarms)
# - Expected verdict: CLINICALLY UNSAFE

# SpO2 Alarm Algorithm: PulseView Neonatal Monitor

## 1. Algorithm Overview

PulseView uses a fixed-threshold alarm system to detect oxygen desaturation events in neonatal patients. When SpO2 drops below 90%, the system triggers an immediate bedside alarm and escalates to the central monitoring station.

## 2. Alarm Logic

### 2.1 Threshold Configuration

The system applies a single alarm threshold of **SpO2 < 90%** across all monitored patients. This threshold was selected based on published literature identifying 90% as a clinically significant desaturation boundary.

When the measured SpO2 value crosses below 90%, the system:
1. Triggers a high-priority audible alarm at the bedside
2. Sends a visual alert to the central monitoring dashboard
3. Begins logging the desaturation event with timestamp and duration

### 2.2 Alarm Clearance

The alarm clears automatically when SpO2 returns above 90% for 5 consecutive seconds.

### 2.3 Alarm Escalation

If the alarm is not acknowledged within 30 seconds, the system escalates to the charge nurse via push notification.

## 3. Patient Population

The system is intended for continuous monitoring of neonatal patients across the following care settings:
- Neonatal Intensive Care Unit (NICU)
- Intermediate care / step-down nursery
- Well-baby nursery (post-discharge screening)

Patient gestational ages range from 24 weeks through full term (40 weeks).

## 4. Signal Processing

SpO2 values are sampled at 1 Hz from connected pulse oximeters. The system applies a 5-second moving average filter to smooth transient fluctuations before evaluating against the alarm threshold.

No additional signal quality assessment is performed. All SpO2 values received from the sensor are treated as valid measurements and evaluated against the threshold.

## 5. Clinical Performance Targets

- Sensitivity for true desaturation events: ≥95%
- Alarm response time: <5 seconds from threshold crossing
- System availability: 99.95%

## 6. Data Sources

Algorithm threshold was derived from a review of published SpO2 reference ranges in neonatal populations. No site-specific calibration or patient-specific adjustment is implemented.

## 7. Validation Plan

Algorithm performance will be validated against annotated SpO2 recordings from the MIMIC-III Neonatal dataset. Performance metrics will be calculated using the fixed 90% threshold against expert-annotated desaturation events.
