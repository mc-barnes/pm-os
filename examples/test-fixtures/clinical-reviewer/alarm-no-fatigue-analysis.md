---
type: prd
status: draft
owner: "@agarcia"
related:
  - regulatory/risk-management/risk-spo2-v1.xlsx
  - clinical/intended-use/intended-use-spo2-v1.md
---

# Expected findings:
# - Critical: No alarm fatigue analysis — 6.7 alarms/patient/hr for continuous monitoring is unsustainable (Bonafide et al., 2015)
# - Critical: No SatSeconds or depth×duration approach — simple threshold crossing maximizes false positives (Poets et al.)
# - Important: No false positive rate reported or targeted (ECRI Top 10 hazard: alarm fatigue)
# - Important: No confidence mechanism — system treats all threshold crossings as equally urgent
# - Expected verdict: NEEDS REVISION

# Alarm Management System: PulseView SpO2 Monitor

## 1. Alarm System Overview

The PulseView alarm management system provides real-time notification when monitored SpO2 values indicate potential oxygen desaturation in neonatal patients. The system supports three alarm priority levels and configurable escalation pathways.

## 2. Alarm Priority Levels

### 2.1 High Priority (Red)
- SpO2 < 85% for ≥5 seconds
- Audible alarm at bedside: 80 dB continuous tone
- Visual: flashing red indicator on dashboard

### 2.2 Medium Priority (Yellow)
- SpO2 between 85-89% for ≥10 seconds
- Audible alarm at bedside: 70 dB intermittent tone
- Visual: solid yellow indicator on dashboard

### 2.3 Low Priority (Cyan)
- SpO2 between 90-92% for ≥15 seconds
- Audible alarm at bedside: 60 dB single chime
- Visual: cyan indicator on dashboard

## 3. Alarm Generation Logic

When SpO2 crosses below the configured threshold:
1. Timer starts for the duration requirement
2. If SpO2 remains below threshold for the required duration, alarm triggers
3. Alarm persists until SpO2 returns above threshold or clinician acknowledges

All SpO2 values are evaluated as received from the sensor with a 3-second averaging window. Threshold crossings are detected on every sample (1 Hz).

## 4. Expected Alarm Volume

Based on internal bench testing with simulated patient data, the system generates approximately 6.7 alarms per patient per hour during continuous monitoring. For a 20-bed NICU, this corresponds to approximately 134 alarms per hour at the central station.

The system does not implement alarm reduction strategies beyond the time-delay mechanism described in Section 3. No alarm suppression, intelligent grouping, or trending-based alarm modification is currently planned.

## 5. Escalation Pathway

| Time Since Alarm | Action |
|-----------------|--------|
| 0 seconds | Bedside alarm triggers |
| 30 seconds | Central station alert |
| 60 seconds | Charge nurse notification |
| 120 seconds | Attending physician notification |

## 6. Alarm Silence / Override

Clinicians may silence alarms for 60-second intervals. There is no limit on the number of times an alarm may be silenced. Silenced alarms are logged but do not generate further notifications during the silence period.

## 7. Clinical Performance

The alarm system targets ≥99% sensitivity for true desaturation events. Specificity targets have not been established. The system prioritizes detecting all potential events over minimizing false alarms.

## 8. Regulatory Considerations

The alarm system complies with IEC 60601-1-8 general alarm signal requirements for priority, sound pressure, and visual indicators. Alarm tones follow the melodic alarm patterns specified in Annex F.
