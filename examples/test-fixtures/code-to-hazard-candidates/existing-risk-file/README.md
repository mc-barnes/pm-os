# Fixture: existing-risk-file

## Purpose
Tests risk file cross-reference — matching HCs to existing HAZ IDs, identifying new candidates, and detecting unmapped hazards.

## Files
- `vitals.py` — Heart rate/temperature checks + EHR write
- `risk-register.md` — 4 existing hazards (2 with code refs, 2 without)

## Expected Findings

**Hazard Candidates:** ~3 HCs from vitals.py
- Heart rate alarm logic → should match HAZ-001
- Temperature threshold → should match HAZ-002
- EHR write path → new candidate (not in risk register)

**Cross-Reference:**
- 2 matched to existing hazards (HAZ-001, HAZ-002)
- 1 new candidate (EHR write — not in risk register)
- 2 unmapped existing hazards (HAZ-003, HAZ-004 — infrastructure/hardware)

## Scoring
- PASS: 3+ HCs, at least 1 matched to existing HAZ ID, at least 1 unmapped hazard identified
- FAIL: No cross-reference results, matched count wrong, unmapped hazards not detected
