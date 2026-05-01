# Test Fixtures: code-to-design-inputs

These fixtures validate the `code-to-design-inputs` skill's ability to scan source files, detect design-input-worthy code boundaries using 6 heuristic scanners, cross-reference against PRDs, and generate IEC 62304 Clause 5.2 compliant design input traceability matrices.

## Directory Structure

```
code-to-design-inputs/
├── README.md                    # This file
├── clear-api-boundaries/        # Flask routes + env vars — API/config detection
│   ├── app.py
│   ├── config.py
│   └── README.md
├── prd-mismatch/                # Code + PRD with gaps in both directions
│   ├── monitor.py
│   ├── prd.md
│   └── README.md
├── clinical-thresholds/         # SpO2/HR thresholds + dosing calculations
│   ├── alarms.py
│   ├── dosing.py
│   └── README.md
└── minimal-repo/                # Hello world — graceful no-results handling
    ├── main.py
    └── README.md
```

## Fixtures

| Fixture | Key Test | Expected DIs | Expected Type |
|---------|----------|-------------|---------------|
| `clear-api-boundaries/` | API/config detection | ~8 | Functional / Performance |
| `prd-mismatch/` | Doc gap + impl gap detection | ~3 DIs, 1 doc gap, 1-2 impl gaps | Mixed |
| `clinical-thresholds/` | Clinical value detection | ~7 | Safety |
| `minimal-repo/` | Graceful no-results handling | 0-1 | — |

## Running

```bash
# Run against a specific fixture
python .claude/skills/code-to-design-inputs/scripts/generate_design_inputs.py \
  --source examples/test-fixtures/code-to-design-inputs/clear-api-boundaries/

# Run with PRD cross-reference
python .claude/skills/code-to-design-inputs/scripts/generate_design_inputs.py \
  --source examples/test-fixtures/code-to-design-inputs/prd-mismatch/ \
  --prd examples/test-fixtures/code-to-design-inputs/prd-mismatch/prd.md
```

## Scoring

A run is considered **passing** if:
- The correct number of DIs is generated (within +/-2 for heuristic tolerance)
- All expected heuristic types fire on the appropriate fixtures
- DI types match expected classifications (Safety for clinical, Functional for CRUD)
- PRD cross-reference correctly identifies documentation and implementation gaps
- The minimal repo case completes without error
- Every DI has Rationale, Rationale Source, and SW Safety Class marked as GAP
- DI IDs are sequential with no gaps

A run is considered **failing** if:
- Clinical thresholds are not classified as Safety type
- PRD gaps are not detected when --prd flag is provided
- The script crashes on the minimal repo fixture
- Rationale or SW Safety Class is auto-populated (not GAP)
