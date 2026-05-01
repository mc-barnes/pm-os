# Hazard from Code — Hazard Candidate Extraction Reference

Reference document for the `code-to-hazard-candidates` skill. Defines the 6 heuristic categories for identifying safety-critical code regions, failure mode templates, domain bias disclosure, and coverage limitations.

**Standard references:**
- ISO 14971:2019 — Risk management for medical devices
- IEC 62304:2006+A1:2015 — Medical device software lifecycle

## Heuristic Categories

The skill uses 6 heuristic scanners to identify code regions that may introduce hazards. Each heuristic maps to a category of safety-critical software behavior with associated failure mode templates.

### 1. Alarm Logic

**What it detects:** Threshold comparisons, alarm state machines, escalation logic, suppression/silencing behavior.

**Regex patterns:**
```python
# Alarm state evaluation
r'(alarm|alert)\s*[=<>!]|trigger_alarm|fire_alarm|raise_alarm'

# Alarm state machine transitions
r'(alarm_state|alert_state|alarm_level|severity)\s*[=:]'

# Alarm suppression/silencing
r'(suppress|silence|mute|inhibit|snooze|acknowledge).*alarm'

# Alarm escalation
r'(escalat|de-escalat|upgrade|downgrade).*(?:alarm|alert|severity)'
```

**Failure mode templates:**
| Failure Mode | Description |
|-------------|-------------|
| Missed alarm | Clinical condition met but alarm not triggered |
| Delayed alarm | Latency between condition onset and alarm notification |
| False alarm | Alarm triggered without underlying clinical condition |
| Alarm suppression failure | Suppression logic prevents valid alarm from firing |

### 2. Threshold/Dosing Calculations

**What it detects:** Numeric comparisons with clinical significance, dosing calculations, unit conversions, boundary values.

**Regex patterns:**
```python
# Clinical threshold comparisons
r'(spo2|heart_rate|hr|bp|temperature|dose|weight)\s*[<>=!]+\s*\d+'

# Dosing calculations
r'(dose|dosage|mg_per_kg|ml_per_kg|units_per_kg|infusion_rate)\s*[=*]'

# Unit conversion functions
r'(convert|to_mg|to_ml|kg_to_lb|celsius_to|fahrenheit_to)'

# Boundary/limit checks
r'(min_dose|max_dose|min_rate|max_rate|lower_limit|upper_limit)\s*[=<>]'
```

**Failure mode templates:**
| Failure Mode | Description |
|-------------|-------------|
| Incorrect threshold | Value too high, too low, or hardcoded when should be parameterized |
| Calculation overflow/underflow | Numeric edge cases producing invalid results |
| Dosing miscalculation | Unit conversion error, weight-based calculation error |
| Boundary violation | Value exceeds safe limits without detection |

### 3. Decision Support Outputs

**What it detects:** Classification results, triage recommendations, risk scores, clinical decision support logic.

**Regex patterns:**
```python
# Classification/scoring functions
r'def\s+(classify|triage|score|predict|recommend|assess|grade|stratify|diagnose)'

# Risk score computation
r'(risk_score|severity_score|acuity|priority_level|triage_level)\s*[=:]'

# Clinical decision output
r'(recommendation|diagnosis|classification|prediction|assessment)\s*[=:]'

# Model inference
r'(model\.predict|classifier\.predict|inference|forward_pass)'
```

**Failure mode templates:**
| Failure Mode | Description |
|-------------|-------------|
| Model inconsistency | ML/algorithm output contradicts clinical context |
| Incorrect classification | Patient misclassified to wrong risk category |
| Stale model | Model not updated with current clinical evidence |

### 4. EHR Write Paths

**What it detects:** Data written to the electronic health record — observations, orders, results, notes.

**Regex patterns:**
```python
# FHIR resource creation/update
r'(fhir|hl7|Bundle|Observation|DiagnosticReport|MedicationRequest)\s*\('

# EHR/EMR write operations
r'(ehr|emr|chart|record)\.(write|create|update|post|submit|save)'

# Order placement
r'(place_order|submit_order|create_order|order_entry)'

# Clinical note writing
r'(progress_note|clinical_note|discharge_summary|report)\.(create|write|save)'
```

**Failure mode templates:**
| Failure Mode | Description |
|-------------|-------------|
| Incorrect data written | Wrong patient, wrong value, wrong units in clinical record |
| Data loss | Observation not persisted, write silently fails |
| Stale data | Cached/outdated values written to active record |

### 5. Physical Device Control

**What it detects:** Actuator commands, pump rates, ventilator settings, motor control.

**Regex patterns:**
```python
# Actuator/pump/motor commands
r'(set_rate|set_flow|set_pressure|set_speed|set_power|actuate|activate_pump)'

# Ventilator/respiratory settings
r'(tidal_volume|peep|fio2|respiratory_rate|inspiratory_pressure|pip|map_pressure)'

# Infusion pump control
r'(infusion_rate|bolus|prime_line|pump_speed|flow_rate)'

# Device state commands
r'(start_therapy|stop_therapy|pause_therapy|resume_therapy|emergency_stop)'
```

**Failure mode templates:**
| Failure Mode | Description |
|-------------|-------------|
| Incorrect setting | Wrong rate, volume, or pressure applied to patient |
| Command not executed | Device fails to respond to software command |
| Runaway output | Control loop failure resulting in unchecked delivery |

### 6. Fail-Safe Paths

**What it detects:** Fallback behavior, degraded mode transitions, safe state logic, error recovery.

**Regex patterns:**
```python
# Safe state transitions
r'(safe_state|safe_mode|degraded_mode|fallback|fail_safe|emergency_mode)'

# Error recovery / watchdog
r'(watchdog|heartbeat|keepalive|timeout_handler|recovery|restart)'

# Graceful degradation
r'(degrade|fallback_to|switch_to_manual|disable_auto|revert_to_default)'

# Exception handlers in safety-critical paths
r'except.*(?:alarm|dose|threshold|patient|vital|clinical)'
```

**Failure mode templates:**
| Failure Mode | Description |
|-------------|-------------|
| Failed transition to safe state | Software fails to enter degraded mode on error |
| Incomplete fallback | Partial state transition leaves system in undefined state |
| Silent failure | Error swallowed without notification or safe state entry |

## Domain Bias Disclosure

The default heuristics are tuned for the **neonatal monitoring** reference device used in this repository. Specific biases:

1. **Alarm thresholds** — Patterns prioritize SpO2, heart rate, and apnea detection (neonatal-specific)
2. **Dosing logic** — Patterns include weight-based neonatal medication calculations (caffeine citrate, surfactant)
3. **Clinical terminology** — Keyword sets reflect NICU vocabulary (gestational age, corrected age, etc.)

### Adapting for Other Domains

Teams using this skill for a different clinical domain should provide a `--heuristics` configuration file that adjusts:
- Clinical keyword sets (cardiac vs. neonatal vs. respiratory)
- Threshold variable names
- Domain-specific device control patterns
- Failure mode templates

Without domain adaptation, the skill may produce:
- **False negatives** — Missing hazards expressed in domain-specific patterns
- **False positives** — Flagging non-clinical code that matches neonatal terminology

## Coverage Limitations

This skill analyzes **application source code only**. The following hazard sources are NOT detected:

| Source | Example | Why Not Detected |
|--------|---------|-----------------|
| Infrastructure | Network partition, cloud outage | Not in source code |
| Deployment | Misconfigured environment, wrong version deployed | Not in source code |
| Operational | Nurse training gaps, workflow violations | Not in source code |
| Data quality | Corrupt sensor input, EMR data integrity | Requires runtime analysis |
| Physical | Device hardware failure, power loss | Not in source code |
| Supply chain | Compromised dependency, SOUP vulnerability | Use code-to-soup-register instead |
| Use environment | Lighting, noise, interruptions | Requires usability study |

A complete hazard analysis per ISO 14971:2019 requires consideration of all sources of harm, not just application code. This skill produces hazard **candidates** as input to a human-led analysis.

## Hazard Framing Disclaimer

> These are candidate hazards inferred from code structure. Hazard analysis requires clinical context, use environment understanding, and patient population awareness that this skill cannot provide. Treat output as input to a human-led hazard analysis session, not as a hazard analysis.

## What This Reference Is Not

This document describes heuristic patterns for identifying candidate hazards from source code. It does not constitute a hazard analysis, a risk assessment, or any other ISO 14971 activity. The heuristics will miss hazards that don't match configured patterns and may flag code regions that are not actually hazardous. Teams should treat all output as candidate input requiring clinical evaluation.
