# Fixture: non-default-domain

## Purpose
Tests detection in a non-neonatal clinical domain (cardiac ECG classification). The default heuristics are tuned for neonatal monitoring — this fixture validates that cardiac-specific patterns are still partially detected but may benefit from a domain-specific heuristic override.

## Files
- `rhythm_classifier.py` — ECG rhythm classification with cardiac thresholds, heart rate calculation, and ML probability scoring

## Expected Findings — Default Heuristics

| Heuristic | Expected HCs | Key Detections |
|-----------|-------------|----------------|
| threshold_calculations | 1 | heart_rate comparisons against brady/tachy thresholds |
| decision_support | 3 | classify_rhythm, compute_vtach_probability, detect_rpeak functions |

**Total expected HCs (default):** 4

**Domain mismatch note:** Cardiac-specific patterns (QRS duration, PR interval, QT interval, ST segment, AFib/AFlutter, VTach/VFib, asystole) are NOT detected by neonatal-tuned default heuristics. Use `--heuristics` with a cardiac config to close these gaps.

## Expected Findings — Cardiac Heuristics (`--heuristics heuristics-cardiac.json`)

| Heuristic | Expected HCs | Key Detections |
|-----------|-------------|----------------|
| alarm_logic | 2 | AFib/AFlutter detection, VTach/VFib classification |
| threshold_calculations | 1 | heart_rate comparisons against brady/tachy thresholds |
| decision_support | 3 | classify_rhythm, compute_vtach_probability, detect_rpeak functions |

**Total expected HCs (cardiac):** 6

**What cardiac heuristics add:** alarm_logic scanner picks up `afib_detected` and `vtach` pattern matches that default neonatal heuristics miss entirely.

## Scoring
- PASS (default): 3-5 HCs detected, at least 1 threshold and 1 decision_support, no crash
- PASS (cardiac): 5-7 HCs detected, at least 1 alarm_logic match, no crash
- FAIL: 0 HCs (heuristics too narrow), or >10 HCs (too noisy)
