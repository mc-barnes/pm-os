# Test Fixtures: code-to-soup-register

These fixtures validate the `code-to-soup-register` skill's ability to scan project directories, detect dependency manifests across multiple languages, resolve transitive dependencies from lock files, and generate IEC 62304-compliant SOUP registers.

## Directory Structure

```
code-to-soup-register/
├── README.md                 # This file
├── gpl-dependency/           # GPL-licensed dep triggers license WARNING
│   ├── requirements.txt
│   ├── Pipfile.lock
│   └── README.md
├── missing-lock-file/        # No lock files -- transitive deps unresolvable
│   ├── package.json
│   ├── requirements.txt
│   └── README.md
├── multi-language/           # Python + JS + Go in one project
│   ├── requirements.txt
│   ├── package-lock.json
│   ├── go.mod
│   └── README.md
└── empty-repo/               # No manifests at all -- error case
    ├── main.py
    └── README.md
```

## Fixtures

| Fixture | Key Test | Expected SOUP Entries | Expected Warnings |
|---------|----------|----------------------|-------------------|
| `gpl-dependency/` | GPL license detection + transitive resolution | 9 (3 declared + 6 transitive) | WARNING: pylint-django GPL-2.0 |
| `missing-lock-file/` | Missing lock file gap detection | 5 (declared only) | GAP: no lock files for JS or Python |
| `multi-language/` | Multi-ecosystem detection (Python, JS, Go) | 8 (across 3 languages) | None |
| `empty-repo/` | No-manifest error handling | 0 | ERROR: No dependency manifests found |

## Running

Point the `code-to-soup-register` skill at each fixture directory:

```bash
# Run against a specific fixture
claude --skill code-to-soup-register --input ./gpl-dependency/

# Expected: each fixture's README.md documents the expected output
```

## Scoring

A run is considered **passing** if:
- The correct number of SOUP entries is generated (within +/-1 for transitive resolution differences)
- All expected WARNINGs and GAPs are surfaced
- License flags match expected (GPL flagged, MIT/BSD not flagged)
- The error case (`empty-repo/`) exits with the correct error message
- Every SOUP entry has fitness-for-use, anomaly list, and integration verification marked as GAP

A run is considered **failing** if:
- A GPL dependency is not flagged
- Missing lock files are not noted as gaps
- The script silently produces zero entries without an error for `empty-repo/`
- Transitive dependencies are listed as declared (or vice versa)
