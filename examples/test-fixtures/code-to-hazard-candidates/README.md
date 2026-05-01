# Test Fixtures: code-to-hazard-candidates

These fixtures validate the `code-to-hazard-candidates` skill's ability to scan source files, detect safety-critical code regions using 6 heuristic scanners, propose candidate hazard scenarios, and cross-reference against existing risk files.

## Directory Structure

```
code-to-hazard-candidates/
├── README.md                    # This file
├── alarm-logic/                 # SpO2 state machine — alarm failure mode detection
│   ├── alarm_manager.py
│   └── README.md
├── existing-risk-file/          # Vitals + risk register — cross-reference test
│   ├── vitals.py
│   ├── risk-register.md
│   └── README.md
├── no-safety-critical/          # Pure CRUD — graceful "no candidates" handling
│   ├── crud_app.py
│   └── README.md
└── non-default-domain/          # Cardiac ECG — domain mismatch test
    ├── rhythm_classifier.py
    └── README.md
```

## Fixtures

| Fixture | Key Test | Expected HCs | Key Heuristic |
|---------|----------|-------------|---------------|
| `alarm-logic/` | Alarm failure mode detection | 4-6 | alarm_logic |
| `existing-risk-file/` | Cross-reference: matched + new + unmapped | ~3 | alarm_logic, threshold_calculations, ehr_writes |
| `no-safety-critical/` | Graceful "no candidates" | 0 | — |
| `non-default-domain/` | Domain mismatch detection | 2-4 | threshold_calculations, decision_support |

## Running

```bash
# Run against a specific fixture
python3 .claude/skills/code-to-hazard-candidates/scripts/generate_hazard_candidates.py \
  --source examples/test-fixtures/code-to-hazard-candidates/alarm-logic/

# Run with risk file cross-reference
python3 .claude/skills/code-to-hazard-candidates/scripts/generate_hazard_candidates.py \
  --source examples/test-fixtures/code-to-hazard-candidates/existing-risk-file/ \
  --risk-file examples/test-fixtures/code-to-hazard-candidates/existing-risk-file/risk-register.md
```

## Scoring

A run is considered **passing** if:
- The correct number of HCs is generated (within +/-2 for heuristic tolerance)
- All expected heuristic types fire on the appropriate fixtures
- Risk file cross-reference correctly identifies matched, new, and unmapped hazards
- The no-safety-critical fixture completes without error
- Every HC has Status = CANDIDATE, Dispositioning = GAP, Clinical Rationale = GAP
- Coverage disclaimer and Hazard Framing Disclaimer are present in every gap report
- HC IDs are sequential with no gaps

A run is considered **failing** if:
- Alarm logic is not detected in the alarm-logic fixture
- Risk file cross-reference produces no results when --risk-file is provided
- The script crashes on the no-safety-critical fixture
- Dispositioning or Clinical Rationale is auto-populated (not GAP)
- Coverage disclaimer is missing from the gap report
