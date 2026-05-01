---
name: code-to-hazard-candidates
version: 1.0.0
description: >
  Reverse-engineer hazard candidates from source code in an existing codebase.
  Identifies safety-critical code regions using 6 heuristic scanners and proposes
  candidate hazard scenarios with failure modes. Produces XLSX hazard candidate
  list with companion gap report including mandatory coverage disclaimer.
  Triggers: "hazard candidates from code", "code-to-hazard-candidates",
  "safety analysis from code", "reverse-engineer hazards", "retrospective hazard analysis".
---

# code-to-hazard-candidates

Reverse-engineer hazard candidates from source code in an existing codebase. Identifies alarm logic, threshold calculations, decision support outputs, EHR write paths, physical device control, and fail-safe paths. Produces a hazard candidate XLSX with companion gap report including mandatory coverage and hazard framing disclaimers.

## When to Use

- Existing codebase with no hazard analysis — building one retrospectively
- Preparing for a first regulatory submission and need to identify safety-critical code
- Auditing hazard coverage against an existing risk file
- Running as part of a gap analysis effort (via `/gap-analysis hazards`)
- Supplementing an existing hazard analysis with code-level coverage

## When NOT to Use

- Greenfield project — use the prospective risk-management skill instead
- Updating an existing, maintained hazard analysis — use change-impact instead
- Non-software hazards (use environment, operational, infrastructure) — this skill only analyzes code
- As a substitute for human-led hazard analysis — this produces **candidates** only

## Quick Start

```bash
# Generate from your repo
python .claude/skills/code-to-hazard-candidates/scripts/generate_hazard_candidates.py \
  --source /path/to/repo

# Generate with risk file cross-reference
python .claude/skills/code-to-hazard-candidates/scripts/generate_hazard_candidates.py \
  --source /path/to/repo --risk-file regulatory/risk-management/risk-register.md

# Generate example output (no repo needed)
python .claude/skills/code-to-hazard-candidates/scripts/generate_hazard_candidates.py --example
```

## Heuristic Categories

| # | Heuristic | What It Detects | Failure Mode Templates |
|---|-----------|----------------|----------------------|
| 1 | Alarm Logic | Threshold comparison, escalation, suppression | Missed alarm, delayed alarm, false alarm, suppression failure |
| 2 | Threshold/Dosing Calculations | Numeric boundaries, dosing calcs, unit conversion | Incorrect threshold, overflow/underflow, dosing miscalc |
| 3 | Decision Support Outputs | Classification, triage, scoring, predictions | Model inconsistency, incorrect classification, stale model |
| 4 | EHR Write Paths | FHIR resources, clinical record writes, orders | Incorrect data, data loss, stale data |
| 5 | Physical Device Control | Actuator commands, pump rates, ventilator settings | Incorrect setting, command failure, runaway output |
| 6 | Fail-Safe Paths | Fallback behavior, degraded mode, safe state | Failed transition, incomplete fallback, silent failure |

## Domain Bias

The default heuristics are tuned for the **neonatal monitoring** reference device. Specific biases:
- Alarm patterns prioritize SpO2, heart rate, and apnea detection
- Dosing patterns include neonatal medication calculations
- Clinical terminology reflects NICU vocabulary

Teams using this skill for a different clinical domain should provide a `--heuristics` configuration file that adjusts keyword sets, threshold variable names, and device control patterns. Without adaptation, false negatives and false positives are likely.

## XLSX Structure

### Sheet: Hazard_Candidates

| Column | Auto-populated? | Notes |
|--------|----------------|-------|
| Candidate ID | Yes | HC-001, HC-002, ... |
| Code Region | Yes | file_path:line_start-line_end |
| Heuristic Matched | Yes | Which detection heuristic triggered |
| Proposed Hazard | Yes | Candidate hazard description |
| Proposed Failure Mode | Yes | How the code region could fail |
| Proposed Harm | Yes | Potential patient harm |
| Existing HAZ ID | Yes (if risk file) | Cross-reference to existing hazard analysis |
| Status | Always "CANDIDATE" | **CANDIDATE — requires human evaluation** |
| Dispositioning Decision | No — GAP | Accepted / Modified / Rejected with rationale |
| Clinical Rationale | No — GAP | Clinical judgment on severity and probability |

**Every output row carries `Status: CANDIDATE` and `Dispositioning: GAP`.** These fields are never auto-populated.

### Sheet: Document_Control

Standard document control sheet with device name, date, and approval signatures.

## Risk File Cross-Reference

When `--risk-file` is provided, the skill cross-references hazard candidates against existing HAZ-xxx IDs:

| Result | Meaning |
|--------|---------|
| Matched | Code region maps to an existing hazard — confirms coverage |
| New candidate | Code region has no matching existing hazard — potential gap |
| Unmapped hazard | Existing hazard has no matching code region — may be infrastructure/operational |

## Coverage Disclaimer

Every generated report includes a "Coverage" section documenting:
- Code paths analyzed (files scanned)
- Code paths excluded (test/, docs/, terraform/, k8s/, etc.)
- What this means (limitations of code-only analysis)

## Hazard Framing Disclaimer

Every generated report includes this disclaimer:

> These are candidate hazards inferred from code structure. Hazard analysis requires clinical context, use environment understanding, and patient population awareness that this skill cannot provide. Treat output as input to a human-led hazard analysis session, not as a hazard analysis.

## Gap Report Categories

| Category | Owner | Description |
|----------|-------|-------------|
| Dispositioning required | Engineering / Clinical | All candidates need human accept/modify/reject |
| Clinical rationale required | Clinical SME | Severity and probability assessment needed |
| New candidates (not in risk file) | Engineering / RA | Code-level hazards not in existing risk analysis |
| Unmapped existing hazards | Engineering / RA | Risk file hazards with no code mapping |

## Reference Files

- `references/hazard-from-code.md` — Heuristic patterns, failure mode templates, domain bias disclosure, coverage limitations

## Verification Checklist

Before accepting a generated hazard candidate list:

- [ ] All 6 heuristics ran against the source tree
- [ ] HC IDs are sequential with no gaps (HC-001, HC-002, ...)
- [ ] Every HC has a code region citation (file:line_start-line_end)
- [ ] Status is CANDIDATE for all rows (not auto-resolved)
- [ ] Dispositioning and Clinical Rationale are GAP for all rows
- [ ] Coverage section lists all analyzed and excluded paths
- [ ] Hazard Framing Disclaimer is present in gap report
- [ ] Risk file cross-reference results are plausible (if --risk-file provided)
- [ ] No network calls were made (all data from local source files)
- [ ] File naming follows convention: `hazard-candidates-{source-name}.xlsx`

## Implementation Notes

- Script uses only `openpyxl` + stdlib — no heavy dependencies
- Python 3.11+ required (match syntax)
- No network calls — all analysis from local source files
- Status, Dispositioning, and Clinical Rationale are **never** auto-populated — always CANDIDATE/GAP/GAP
- HAZARD_SKIP_DIRS is broader than SKIP_DIRS in design-inputs — adds test/, terraform/, k8s/
- Code regions expand trigger lines to enclosing function boundaries
