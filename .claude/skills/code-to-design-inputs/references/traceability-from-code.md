# Traceability from Code — Design Input Extraction Reference

Reference document for the `code-to-design-inputs` skill. Defines the inclusion heuristics used to identify design-input-worthy code boundaries, DI type classification, and PRD cross-reference methodology.

**Standard reference:** IEC 62304:2006+A1:2015 Clause 5.2 — Software requirements analysis.

## Inclusion Heuristics

The skill uses 6 heuristic scanners to identify code regions that imply design inputs. Each heuristic targets a specific category of software behavior that typically requires documentation in a design controls traceability matrix.

### 1. API Boundaries

**What it detects:** Routes, exported functions, public interfaces — the external contract of the software.

**Regex patterns:**
```python
# Flask/FastAPI route decorators
r'@(app|router|blueprint)\.(get|post|put|delete|patch|route)\s*\('

# Express.js route handlers
r'(app|router)\.(get|post|put|delete|patch|use)\s*\('

# Django URL patterns
r'path\s*\(\s*["\']'

# Public function/class exports
r'^(def|class|export\s+(function|class|const|default))\s+'

# REST endpoint annotations (Java/Kotlin)
r'@(Get|Post|Put|Delete|Patch|Request)Mapping'
```

**DI type:** Functional (default), Interface (if integration-facing)

**Example:**
```python
@app.route("/api/v1/patients/<patient_id>/vitals", methods=["GET"])
def get_patient_vitals(patient_id: str):
```
→ DI: "System shall provide API endpoint to retrieve patient vitals by patient ID"

### 2. Configuration Surfaces

**What it detects:** Environment variables, feature flags, threshold constants, configurable parameters.

**Regex patterns:**
```python
# Environment variable reads
r'os\.environ\[|os\.getenv\(|process\.env\.'

# Feature flags / config constants
r'^\s*(FEATURE_|FLAG_|ENABLE_|DISABLE_|MAX_|MIN_|TIMEOUT_|LIMIT_)'

# Settings/config files with uppercased keys
r'^[A-Z][A-Z_]{2,}\s*[:=]'

# Django/Flask config
r'app\.config\[|settings\.'
```

**DI type:** Functional (feature flags), Performance (timeouts/limits), Safety (clinical thresholds)

**Example:**
```python
SPO2_LOW_ALARM_THRESHOLD = int(os.getenv("SPO2_LOW_THRESHOLD", "88"))
```
→ DI: "System shall use configurable SpO2 low alarm threshold (default: 88%)"

### 3. Integration Points

**What it detects:** External API calls, EHR writes, device interfaces, FHIR endpoints, message queues.

**Regex patterns:**
```python
# HTTP client calls
r'requests\.(get|post|put|delete|patch)\(|fetch\(|axios\.|http\.(get|post)'

# FHIR resource operations
r'fhir|hl7|Bundle|Patient|Observation|DiagnosticReport'

# Database write operations
r'\.(save|create|insert|update|delete|execute)\s*\('

# Message queue / event bus
r'\.(publish|send|emit|dispatch)\s*\('

# Device/hardware interface
r'serial\.|usb\.|bluetooth\.|ble\.'
```

**DI type:** Interface

**Example:**
```python
response = requests.post(f"{EHR_BASE}/Observation", json=fhir_bundle)
```
→ DI: "System shall transmit observation data to EHR via FHIR Observation resource"

### 4. Clinical Decision Thresholds

**What it detects:** Alarm limits, dosing calculations, classification boundaries, scoring cutoffs.

**Regex patterns:**
```python
# Numeric comparisons with clinical variable names
r'(spo2|sao2|heart_rate|hr|bp|temperature|temp|dose|weight|bmi|score|risk|severity|alarm|threshold|limit)\s*[<>=!]+'

# Alarm/threshold constants
r'(ALARM|THRESHOLD|CRITICAL|WARNING|ALERT|LIMIT|BOUNDARY|CUTOFF)\s*[=:]'

# Dosing/calculation functions
r'def\s+(calculate|compute|dose|score|classify|evaluate|assess|grade)'

# Clinical scoring
r'(apgar|bishop|apache|sofa|news|mews|glasgow|braden)\s*'
```

**DI type:** Safety

**Example:**
```python
if spo2 < SPO2_CRITICAL_THRESHOLD:
    trigger_alarm(severity="CRITICAL", value=spo2)
```
→ DI: "System shall trigger critical alarm when SpO2 falls below critical threshold"

### 5. Data Retention / Deletion

**What it detects:** Storage duration policies, purge logic, data lifecycle management.

**Regex patterns:**
```python
# Retention/expiration logic
r'(retention|expir|ttl|purge|archive|delete_after|cleanup|prune|evict)'

# Time-based deletion
r'(days_old|max_age|expire_at|retention_days|keep_days)'

# Data lifecycle
r'(gdpr|hipaa|phi|pii).*delete|delete.*(gdpr|hipaa|phi|pii)'

# Scheduled cleanup
r'(cron|schedule|periodic).*delete|delete.*(cron|schedule|periodic)'
```

**DI type:** Functional

**Example:**
```python
VITALS_RETENTION_DAYS = 365 * 7  # 7-year retention per HIPAA
```
→ DI: "System shall retain vitals data for 7 years per HIPAA requirements"

### 6. User-Facing Error Messages

**What it detects:** Error text shown to clinicians or patients — information-for-safety under risk controls.

**Regex patterns:**
```python
# Error/warning message strings
r'(flash|toast|alert|notify|message|error_msg|warning_msg)\s*\(\s*["\']'

# HTTP error responses with messages
r'(abort|HTTPException|HttpResponse|JsonResponse)\s*\(.*message'

# UI error display
r'(setError|showError|displayError|errorMessage|alertText)\s*[=(]'

# Logging that implies user-facing output
r'(user_error|patient_alert|clinician_warning|display_warning)'
```

**DI type:** Safety (clinical context), Functional (general errors)

**Example:**
```python
flash("WARNING: SpO2 sensor disconnected. Verify probe placement.", "error")
```
→ DI: "System shall display sensor disconnection warning to clinician with remediation guidance"

## DI Type Classification

| Type | Criteria | Examples |
|------|----------|---------|
| Functional | General software behavior, CRUD operations, workflow logic | API endpoints, data retention, feature flags |
| Performance | Timing, throughput, resource constraints | Timeouts, rate limits, batch sizes |
| Safety | Clinical decision logic, alarm behavior, patient-facing outputs | Alarm thresholds, dosing calculations, clinical error messages |
| Interface | External system communication, data exchange | FHIR endpoints, EHR writes, device protocols |

**Classification rules:**
1. If the heuristic is `clinical_thresholds` → Safety
2. If the heuristic is `integration_points` → Interface
3. If the heuristic is `error_messages` and context contains clinical terms → Safety
4. If the variable name contains timeout/rate/latency → Performance
5. Default → Functional

## PRD Cross-Reference Methodology

When a `--prd` flag is provided, the skill performs keyword-based cross-referencing between discovered DIs and the PRD document.

### Parsing PRD content

The PRD is parsed for requirement-like statements:
- Lines starting with bullet points (`-`, `*`, `•`)
- Lines starting with numbered items (`1.`, `2.`, etc.)
- Lines containing "shall", "must", "should", "will"
- Lines containing requirement IDs (e.g., `REQ-001`, `FR-`, `NFR-`)

### Matching algorithm

For each DI, extract keywords from the description and source code context. For each PRD statement, extract keywords. Compare keyword overlap using normalized tokens (lowercase, stemmed).

A match is declared when:
- 3+ non-trivial keywords overlap, OR
- A requirement ID from the PRD appears in the code comments, OR
- The code function/class name matches a PRD term

### Gap types

| Gap Type | Meaning | Owner | Urgency |
|----------|---------|-------|---------|
| Documentation Gap | Code behavior exists but PRD doesn't mention it | Product / RA | Medium — document the intent |
| Implementation Gap | PRD describes behavior that code doesn't implement | Engineering / Product | Varies — could be deferred scope, bug, or intentional |

### Limitations

- Keyword matching produces false positives and false negatives
- Semantic equivalence is not detected (e.g., "notify clinician" vs. "send alert")
- PRD structure varies widely — parsing is best-effort
- Cross-reference results should be reviewed by a human familiar with both the code and the PRD

## What This Reference Is Not

This document describes heuristic patterns for identifying candidate design inputs from source code. It does not define what constitutes a design input under IEC 62304 or ISO 13485. The heuristics are tuned for common software patterns in medical device codebases but will miss domain-specific conventions, custom frameworks, or non-standard architectures. Teams should review and calibrate the heuristics for their specific codebase.
