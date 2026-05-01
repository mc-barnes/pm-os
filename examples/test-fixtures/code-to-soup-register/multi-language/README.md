# Fixture: multi-language

## Purpose

Tests the script's ability to detect and parse dependency manifests across three different programming languages (Python, JavaScript, Go) in a single project. Verifies that transitive dependencies are resolved from the JavaScript lock file and that all ecosystems are represented in the output.

## Files included

| File | Language | Description |
|------|----------|-------------|
| `requirements.txt` | Python | 2 declared dependencies: numpy==1.26.4, scipy==1.12.0 |
| `package-lock.json` | JavaScript | v3 lock file with express@4.18.2 and transitive deps (accepts@1.3.8, mime-types@2.1.35, mime-db@1.52.0, negotiator@0.6.3) |
| `go.mod` | Go | 1 declared dependency: golang.org/x/crypto v0.19.0 |

## Expected findings

- **SOUP entries:** 8 total
  - Python: 2 declared (numpy, scipy) -- no lock file, so no transitive resolution
  - JavaScript: 6 (1 declared express + 5 transitive: accepts, mime-types, mime-db, negotiator)
  - Go: 1 declared (golang.org/x/crypto)
- **Languages detected:** Python, JavaScript, Go
- **License warnings:** None -- all packages use permissive licenses (BSD, MIT, BSD-3-Clause)
- **Transitive resolution:** Complete for JS (lock file present), incomplete for Python (no Pipfile.lock), N/A for Go (go.sum not provided but go.mod is sufficient for declared deps)
- **GAP:** Missing `Pipfile.lock` for Python transitive dependency resolution
- **GAP fields on every entry:** fitness-for-use rationale, known anomaly list, integration verification -- all marked GAP

## Expected script behavior

1. Detects `requirements.txt`, `package-lock.json`, and `go.mod` in the fixture directory
2. Parses 2 Python declared dependencies from `requirements.txt`
3. Parses 1 JavaScript declared dependency + 5 transitive from `package-lock.json`
4. Parses 1 Go declared dependency from `go.mod`
5. Generates a SOUP register with 8 entries spanning 3 languages
6. No license warnings raised
7. Notes missing Python lock file as a gap in transitive resolution
8. Marks fitness-for-use, anomaly list, and integration verification as GAP on all entries
