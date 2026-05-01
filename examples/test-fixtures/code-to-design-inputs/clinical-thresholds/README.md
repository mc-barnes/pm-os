# Fixture: clinical-thresholds

## Purpose
Tests detection of clinical decision thresholds, alarm logic, dosing calculations, and safety-relevant error messages.

## Files
- `alarms.py` — SpO2 and heart rate alarm thresholds and evaluation functions
- `dosing.py` — Weight-based neonatal dosing calculations with dose cap warning

## Expected Findings

| Heuristic | Expected DIs | Key Detections |
|-----------|-------------|----------------|
| clinical_thresholds | ~5 | ALARM_SPO2_LOW_CRITICAL, ALARM_HR_HIGH_CRITICAL, THRESHOLD_APNEA, calculate_caffeine, calculate_surfactant |
| configuration_surfaces | ~1-2 | CAFFEINE_DOSE_MG_PER_KG, LIMIT_MAX_DOSE_MG |
| error_messages | ~1 | "WARNING: Calculated dose exceeds maximum limit" |

**Total expected DIs:** ~7
**All should be type:** Safety

## Scoring
- PASS: 5-10 DIs detected, all classified as Safety type, alarm thresholds found
- FAIL: <3 DIs, Safety type not assigned, clinical thresholds missed
