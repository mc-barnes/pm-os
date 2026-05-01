# Fixture: prd-mismatch

## Purpose
Tests PRD cross-reference detection — documentation gaps (code not in PRD) and implementation gaps (PRD not in code).

## Files
- `monitor.py` — 3 functions implementing monitoring, alerting, and CSV export
- `prd.md` — 4 requirements, one of which (FHIR transmission) is not implemented

## Expected Findings

**Design Inputs:** ~3 DIs from code analysis (check_vitals threshold, send_alert, export_vitals_csv, config)

**PRD Cross-Reference:**
- **Documentation gap (1):** `export_vitals_csv` — code exists but PRD doesn't mention CSV export
- **Implementation gaps (1-2):** PRD requirement 4 (FHIR transmission) has no corresponding code

## Scoring
- PASS: 3+ DIs detected, at least 1 documentation gap, at least 1 implementation gap
- FAIL: 0 DIs, no PRD cross-reference gaps identified
