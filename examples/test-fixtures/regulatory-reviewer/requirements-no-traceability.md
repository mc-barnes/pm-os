---
type: design-controls
status: draft
owner: "@agarcia"
related:
  - product/prds/pulseview-prd-v1.md
---

# Expected findings:
# - BLOCKER: No unique requirement IDs (IEC 62304 Section 5.2, ISO 13485 Section 7.3.3)
# - BLOCKER: No traceability to user needs or risk controls (IEC 62304 Section 5.2.6, 21 CFR 820.30)
# - BLOCKER: Orphan requirement — CSV export has no parent user need or risk control linkage
# - WARNING: Missing acceptance criteria on requirements 2 and 5
# - WARNING: No indication of requirements review completion (IEC 62304 Section 5.2.6)
# - Expected verdict: NOT SUBMITTABLE

# Software Requirements Specification: PulseView SpO2 Monitor

## 1. Purpose

This document defines the software requirements for the PulseView SpO2 monitoring system. Requirements are derived from clinical workflow analysis and stakeholder interviews.

## 2. Software Requirements

### Real-Time SpO2 Display

The software shall acquire SpO2 values from connected pulse oximetry sensors and display the current value on the monitoring dashboard with a refresh rate of no less than 1 Hz. The displayed value shall reflect the most recent valid measurement from the sensor. Invalid or artifact-corrupted readings shall be indicated with a visual marker rather than displaying a potentially incorrect value.

### Adaptive Alarm Threshold

The software shall calculate a patient-specific alarm threshold using a rolling baseline derived from the prior 30 seconds of artifact-free SpO2 signal. The alarm shall trigger when the current SpO2 value falls below the adaptive threshold by a configurable margin.

### Multi-Patient View

The software shall support simultaneous display of SpO2 values for up to 24 patients on a single screen. Each patient tile shall show the current SpO2 value, waveform trace, alarm status, and patient identifier. Patients in active alarm state shall be visually distinguished from patients in normal range.

### Alert Escalation

The software shall escalate unacknowledged alarms according to the following schedule: first-level notification to the assigned nurse's mobile device at 60 seconds, second-level notification to the charge nurse at 90 seconds, and third-level notification to the attending physician at 120 seconds. Each escalation event shall be logged with timestamp, recipient, and acknowledgment status.

### CSV Export

The software shall export trend data in CSV format. The export shall include patient identifier, timestamp, SpO2 value, alarm events, and sensor status for the selected time range.

### Sensor Connectivity

The software shall maintain persistent connections to GE, Philips, and Masimo pulse oximetry sensors via HL7v2 ADT/ORU messaging. Connection loss shall be detected within 5 seconds and indicated on the dashboard. The system shall attempt automatic reconnection at 10-second intervals for up to 5 minutes before requiring manual intervention.

## 3. Performance Requirements

- End-to-end latency from sensor measurement to dashboard display: ≤2 seconds
- Dashboard page load time: ≤3 seconds for up to 24 patients
- System availability: ≥99.95% uptime measured monthly
- Data retention: 90 days minimum for all trend data

## 4. Interface Requirements

- HL7v2 ADT (patient admission/discharge/transfer) message support
- HL7v2 ORU (observation result) message support for SpO2 data ingestion
- RESTful API for mobile alert delivery
- Browser-based UI compatible with Chrome 120+ and Edge 120+
