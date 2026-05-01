# Fixture: empty-repo

## Purpose

Tests the script's behavior when a project directory contains no dependency manifest files at all. The directory has only a Python source file and this README. The script should detect the absence of any recognized manifests and exit with an error.

## Files included

| File | Description |
|------|-------------|
| `main.py` | A trivial Python file with `print("hello")` -- no imports, no dependencies |
| `README.md` | This file |

**Deliberately absent:**
- `requirements.txt`
- `Pipfile.lock`
- `package.json`
- `package-lock.json`
- `go.mod`
- Any other dependency manifest

## Expected findings

- **SOUP entries:** 0
- **No dependency manifests found** -- script should report this explicitly
- **No languages detected**
- **No license warnings**

## Expected script behavior

1. Scans the fixture directory for recognized manifest files (requirements.txt, Pipfile.lock, package.json, package-lock.json, go.mod, etc.)
2. Finds none
3. Exits with error: "No dependency manifests found."
4. Produces zero SOUP entries
5. Non-zero exit code
