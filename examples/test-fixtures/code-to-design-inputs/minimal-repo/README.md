# Fixture: minimal-repo

## Purpose
Tests graceful handling when no design inputs are detected.

## Files
- `main.py` — Simple hello world with no API, config, or clinical logic

## Expected Findings
**Total expected DIs:** 0-1

The script should handle this gracefully — produce an empty or near-empty XLSX and gap report without crashing.

## Scoring
- PASS: Script completes without error, 0-1 DIs detected, gap report generated
- FAIL: Script crashes, exception raised, or spurious DIs detected (>2)
