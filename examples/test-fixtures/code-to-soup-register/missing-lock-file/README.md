# Fixture: missing-lock-file

## Purpose

Tests the script's behavior when dependency manifests exist but their corresponding lock files are missing. Both `package.json` (JavaScript) and `requirements.txt` (Python) are present, but neither `package-lock.json` nor `Pipfile.lock` exists. This is a common real-world gap that prevents transitive dependency resolution.

## Files included

| File | Description |
|------|-------------|
| `package.json` | 3 JS dependencies: react@18.2.0, express@4.18.2, lodash@4.17.21 |
| `requirements.txt` | 2 Python dependencies: flask==3.0.2, requests==2.31.0 |

**Deliberately absent:**
- `package-lock.json` -- no JS lock file
- `Pipfile.lock` -- no Python lock file

## Expected findings

- **SOUP entries:** 5 total (3 JS + 2 Python, declared only)
- **GAP:** Missing `package-lock.json` -- transitive JavaScript dependencies unresolvable
- **GAP:** Missing `Pipfile.lock` -- transitive Python dependencies unresolvable
- **WARNING:** Transitive dependencies unknown for all 5 declared packages -- IEC 62304 Section 8.1.2 requires identification of all SOUP including transitive
- **Version pinned:** Yes for Python (==), Yes for JS (exact version in package.json) -- but no lock file means builds are not reproducible
- **GAP fields on every entry:** fitness-for-use rationale, known anomaly list, integration verification -- all marked GAP

## Expected script behavior

1. Detects `package.json` and `requirements.txt` in the fixture directory
2. Notes the absence of `package-lock.json` and `Pipfile.lock`
3. Emits GAP notes about missing lock files for both ecosystems
4. Generates a SOUP register with only declared (direct) dependencies -- 5 entries
5. Marks transitive dependency resolution as incomplete
6. Marks fitness-for-use, anomaly list, and integration verification as GAP on all entries
