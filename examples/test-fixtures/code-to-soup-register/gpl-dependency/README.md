# Fixture: gpl-dependency

## Purpose

Tests detection of a GPL-licensed dependency in a Python project with a lock file present. The script should resolve transitive dependencies from the Pipfile.lock and flag `pylint-django` as a license risk due to its GPL-2.0 license.

## Files included

| File | Description |
|------|-------------|
| `requirements.txt` | 3 direct dependencies: flask==3.0.2, numpy==1.26.4, pylint-django==2.5.5 |
| `Pipfile.lock` | Resolved transitive dependencies for all 3 packages (werkzeug, jinja2, click, markupsafe, itsdangerous, blinker) |

## Expected findings

- **SOUP entries:** 9 total (3 declared + 6 transitive from Pipfile.lock)
- **WARNING:** `pylint-django` has GPL-2.0 license -- copyleft license may impose distribution obligations on the medical device software
- **Transitive deps resolved:** Yes -- werkzeug==3.0.1, jinja2==3.1.3, click==8.1.7, markupsafe==2.1.5, itsdangerous==2.1.2, blinker==1.7.0
- **License flags:** All BSD-3-Clause/MIT except pylint-django (GPL-2.0)
- **GAP fields on every entry:** fitness-for-use rationale, known anomaly list, integration verification -- all marked GAP (require manual completion)

## Expected script behavior

1. Detects `requirements.txt` and `Pipfile.lock` in the fixture directory
2. Parses 3 declared dependencies from `requirements.txt`
3. Resolves 6 transitive dependencies from `Pipfile.lock`
4. Generates a SOUP register with 9 entries
5. Flags `pylint-django` with a WARNING for GPL-2.0 license
6. Marks fitness-for-use, anomaly list, and integration verification as GAP on all entries
7. All versions pinned (resolved from lock file)
