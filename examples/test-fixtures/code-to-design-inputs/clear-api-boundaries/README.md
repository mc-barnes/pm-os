# Fixture: clear-api-boundaries

## Purpose
Tests detection of API routes and configuration surfaces in a straightforward Flask app.

## Files
- `app.py` — Flask app with 4 route endpoints
- `config.py` — Configuration constants and environment variables

## Expected Findings

| Heuristic | Expected DIs | Key Detections |
|-----------|-------------|----------------|
| api_boundaries | 4 | GET /patients, GET /patients/<id>/vitals, POST /alerts, POST /export |
| configuration_surfaces | ~8-12 | DATABASE_URL, API_KEY, FEATURE_FHIR_EXPORT, TIMEOUT_EHR_SECONDS, SERVER_HOST, etc. |

**Total expected DIs:** ~14-18 (FHIR bare-keyword false positives removed in Phase 6)

## Scoring
- PASS: 12-20 DIs detected, all 4 routes found, at least 3 config params found, no bare FHIR keyword matches
- FAIL: <8 DIs, any route missed, no configuration detection, bare "patient" or "FHIR" keyword matches
