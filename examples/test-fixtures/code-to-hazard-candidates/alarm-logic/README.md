# Fixture: alarm-logic

## Purpose
Tests detection of alarm failure modes in a SpO2 state machine implementation.

## Files
- `alarm_manager.py` — SpO2 alarm state machine with threshold evaluation, escalation, and silence/acknowledge

## Expected Findings

| Heuristic | Expected HCs | Key Detections |
|-----------|-------------|----------------|
| alarm_logic | 4-6 | trigger_alarm calls, alarm state transitions, silence/suppress logic, escalation |
| threshold_calculations | 0-2 | spo2 threshold comparisons |

**Total expected HCs:** 4-6

## Scoring
- PASS: 3-8 HCs detected, alarm_logic heuristic fires, silence/suppress logic flagged
- FAIL: <2 HCs, alarm logic not detected, threshold comparisons missed
