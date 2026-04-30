---
type: prd
status: draft
owner: "@jsmith"
related:
  - regulatory/risk-management/risk-spo2-v1.xlsx
  - regulatory/design-controls/design-controls-spo2-v1.xlsx
---

# Expected findings:
# - BLOCKER: Missing intended use statement (no target condition, population, setting, or user specified)
# - BLOCKER: Missing contraindications (21 CFR 807.92(a)(5))
# - BLOCKER: No predicate device named (510(k) pathway unvalidated)
# - WARNING: Device classification stated but not justified (no rationale per IEC 62304 Section 4.3)
# - WARNING: No IMDRF SaMD risk categorization (significance × healthcare situation)
# - Expected verdict: NOT SUBMITTABLE

# Product Requirements Document: PulseView SpO2 Monitor

## 1. Overview

PulseView is a software-as-a-medical-device (SaMD) application that provides continuous SpO2 monitoring for hospitalized patients. The system processes pulse oximetry waveform data from bedside sensors and presents real-time oxygen saturation values to clinical staff via a central monitoring dashboard.

## 2. Device Classification

This product is a Class II medical device software.

Software safety classification: Class C per IEC 62304.

## 3. Problem Statement

Current SpO2 monitoring systems in neonatal intensive care units generate excessive false alarms, leading to alarm fatigue among nursing staff. Studies report that up to 85-99% of clinical alarms are non-actionable, resulting in delayed response to genuine desaturation events. PulseView addresses this by applying signal processing algorithms to reduce false alarm rates while maintaining sensitivity to clinically significant desaturation events.

## 4. Target Users

- NICU nursing staff
- Attending neonatologists
- Respiratory therapists

## 5. Key Features

### 5.1 Real-Time SpO2 Display
The system shall display continuous SpO2 values updated at a minimum rate of 1 Hz. Values shall be displayed numerically and as a waveform trace on the central dashboard.

### 5.2 Smart Alarm Management
The system shall apply adaptive thresholding to SpO2 values to reduce non-actionable alarms. The algorithm uses a rolling baseline calculated from the prior 30 seconds of artifact-free signal. Alarm thresholds adjust based on patient-specific trending data.

### 5.3 Trend Analysis
The system shall provide 1-hour, 4-hour, 12-hour, and 24-hour trend views for each monitored patient. Trend data shall be exportable in CSV format for clinical review.

### 5.4 Multi-Patient Dashboard
The system shall support simultaneous monitoring of up to 24 patients on a single display. Patients in alarm state shall be visually highlighted with color-coded severity indicators.

### 5.5 Alert Escalation
If an alarm is not acknowledged within 60 seconds, the system shall escalate the alert to the charge nurse's mobile device. Second-level escalation to the attending physician occurs at 120 seconds.

## 6. Technical Requirements

- Integration with GE, Philips, and Masimo pulse oximetry sensors via HL7v2 ADT/ORU messaging
- Minimum latency from sensor to display: <2 seconds
- System uptime: 99.95% availability
- Data retention: 90 days of trend data per patient
- Browser-based dashboard (Chrome, Edge) with responsive layout

## 7. Regulatory Pathway

This product will be submitted via the 510(k) pathway. Existing SpO2 clinical decision support systems serve as the basis for substantial equivalence.

## 8. Clinical Evidence Plan

Clinical validation will be performed through a retrospective study using annotated SpO2 data from the MIMIC-III database. The study will evaluate alarm reduction rate versus a standard threshold-based system, with a target of ≥50% reduction in non-actionable alarms while maintaining ≥95% sensitivity for true desaturation events (SpO2 <85% sustained >10 seconds).

## 9. Timeline

- Q1 2026: Software architecture and design controls
- Q2 2026: Core algorithm development and unit testing
- Q3 2026: Integration testing and clinical validation
- Q4 2026: 510(k) submission

## 10. Success Metrics

- False alarm reduction ≥50% compared to standard threshold monitoring
- Sensitivity for true desaturation ≥95%
- Mean time to alarm acknowledgment reduced by ≥30%
- System uptime ≥99.95%
