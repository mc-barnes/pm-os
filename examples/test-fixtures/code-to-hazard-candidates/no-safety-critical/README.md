# Fixture: no-safety-critical

## Purpose
Tests graceful handling when no safety-critical code patterns are detected.

## Files
- `crud_app.py` — Simple todo list CRUD application with no clinical or safety logic

## Expected Findings
**Total expected HCs:** 0

The script should handle this gracefully — produce an empty or near-empty XLSX and gap report without crashing. The report should clearly state no candidates were found.

## Scoring
- PASS: Script completes without error, 0 HCs detected, gap report generated with coverage section
- FAIL: Script crashes, spurious HCs detected (>0), or coverage disclaimer missing
