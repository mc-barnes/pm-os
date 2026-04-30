# Test Fixtures for SaMD Reviewer Agents

These are **deliberately broken** SaMD artifacts used to validate the 5 reviewer agents in `.claude/skills/agents/`. Each file contains realistic but non-compliant content designed to trigger specific findings.

## Purpose

- Verify each agent catches known gaps in its domain
- Regression-test after SKILL.md changes, reference doc updates, or review framework changes
- Provide concrete examples of common deficiencies for onboarding

## Directory Structure

```
examples/test-fixtures/
├── README.md
├── regulatory-reviewer/     # 4 fixtures
├── clinical-reviewer/       # 4 fixtures
├── safety-reviewer/         # 4 fixtures
├── qa-reviewer/             # 4 fixtures
├── cybersecurity-reviewer/  # 4 fixtures
└── .results/                # gitignored eval output
```

## Severity & Verdict Mapping

Each agent uses its own severity terminology. The eval script maps these internally.

| Agent | Blocker-level | Warning-level | Verdicts (worst → best) |
|-------|-------------|---------------|------------------------|
| regulatory-reviewer | BLOCKER | WARNING | NOT SUBMITTABLE > NEEDS REVISION > ACCEPTABLE |
| clinical-reviewer | Critical | Important | CLINICALLY UNSAFE > NEEDS REVISION > ACCEPTABLE |
| safety-reviewer | SAFETY FINDING | GAP | SAFETY CONCERN > NEEDS REVISION > ACCEPTABLE |
| qa-reviewer | FINDING | OBSERVATION | NOT AUDIT-READY > NEEDS REMEDIATION > AUDIT-READY |
| cybersecurity-reviewer | SECURITY FINDING | GAP | SECURITY CONCERN > NEEDS REVISION > ACCEPTABLE |

## Fixtures

### regulatory-reviewer

| File | Artifact Type | Key Deficiencies | Expected Verdict |
|------|--------------|------------------|-----------------|
| `prd-missing-intended-use.md` | PRD | No intended use, no contraindications, no named predicate | NOT SUBMITTABLE |
| `requirements-no-traceability.md` | SRS | No requirement IDs, no traceability, orphan requirement | NOT SUBMITTABLE |
| `soup-list-incomplete.md` | SOUP Register | Missing risk classifications, missing version, no monitoring | NEEDS REVISION |
| `change-request-no-pccp.md` | Change Request | Misclassified severity, no risk impact, no PCCP assessment | NOT SUBMITTABLE |

### clinical-reviewer

| File | Artifact Type | Key Deficiencies | Expected Verdict |
|------|--------------|------------------|-----------------|
| `spo2-fixed-threshold.md` | Algorithm PRD | No GA adjustment, no depth×duration, no signal quality gating | CLINICALLY UNSAFE |
| `alarm-no-fatigue-analysis.md` | Alarm System | No alarm fatigue analysis, no SatSeconds, 6.7 alarms/hr | NEEDS REVISION |
| `nurse-handoff-jargon.md` | Handoff Spec | Researcher jargon, no urgency level, "monitor closely" | NEEDS REVISION |
| `home-monitor-no-validation.md` | Consumer PRD | Implied SIDS benefit, no ABG validation, sensitivity unknown | CLINICALLY UNSAFE |

### safety-reviewer

| File | Artifact Type | Key Deficiencies | Expected Verdict |
|------|--------------|------------------|-----------------|
| `risk-analysis-happy-path.md` | Risk Analysis | No foreseeable misuse, incomplete hazard chains, no systematic method | SAFETY CONCERN |
| `fmea-no-afap.md` | FMEA | No AFAP rationale, controls jump to IFU, no cumulative risk | SAFETY CONCERN |
| `usability-engineers-only.md` | Usability Eval | Non-representative users, satisfaction-based pass criteria | SAFETY CONCERN |
| `aiml-confidence-untested.md` | AI/ML Risk | "Clinician decides" as control, confidence not validated | SAFETY CONCERN |

### qa-reviewer

| File | Artifact Type | Key Deficiencies | Expected Verdict |
|------|--------------|------------------|-----------------|
| `capa-human-error.md` | CAPA | "Human error" root cause, no effectiveness check, weak action | NOT AUDIT-READY |
| `complaint-no-mdr-eval.md` | Complaint | No MDR evaluation, "no further action" without rationale | NOT AUDIT-READY |
| `management-review-rubber-stamp.md` | Mgmt Review | Missing required inputs, no decisions, no action items | NOT AUDIT-READY |
| `supplier-eval-no-soup.md` | Supplier List | SOUP/cloud not evaluated, no monitoring metrics | NEEDS REMEDIATION |

### cybersecurity-reviewer

| File | Artifact Type | Key Deficiencies | Expected Verdict |
|------|--------------|------------------|-----------------|
| `threat-model-generic.md` | Threat Model | No methodology, no patient safety tracing, generic threat list | SECURITY CONCERN |
| `sbom-no-versions.md` | SBOM | No versions, no transitive deps, not machine-readable | SECURITY CONCERN |
| `security-arch-incomplete.md` | Security Arch | Missing 3 of 4 FDA views, no multi-patient harm assessment | SECURITY CONCERN |
| `vuln-plan-no-cvd.md` | Vuln Mgmt Plan | No CVD, no timelines, no ISAO, NVD-only monitoring | SECURITY CONCERN |

## Running Evaluations

### Automated (eval-agents.sh)

```bash
# Validate fixture format only — no API calls, $0 cost
./scripts/eval-agents.sh --dry-run all
./scripts/eval-agents.sh --dry-run safety-reviewer

# Run live evaluation against claude CLI (~$0.05-0.15/fixture)
./scripts/eval-agents.sh regulatory-reviewer
./scripts/eval-agents.sh all
./scripts/eval-agents.sh --yes all          # skip cost confirmation
```

Results are saved to `examples/test-fixtures/.results/{agent}/{fixture}.txt` (gitignored).

### Manual

1. Run an agent against any fixture file using claude CLI
2. Compare the agent's findings against the expected findings listed at the top of the file
3. All blocker-level expected findings should appear in the agent's output
4. Warning-level findings are desirable but not strictly required

## Expected Findings Format

Each fixture includes a comment block after the frontmatter using the agent's native severity terms:

```markdown
# Expected findings:
# - Critical: [description with literature/standard reference]
# - Important: [description]
# - Expected verdict: CLINICALLY UNSAFE
```

## Scoring

A run is considered **passing** if:
- All expected blocker-level findings are detected (may be worded differently but must cover the same gap)
- The verdict matches or is more conservative than expected
- No false blockers are raised on compliant sections
- No fabricated citations to standards or guidance documents

A run is considered **failing** if:
- Any expected blocker-level finding is missed
- The verdict is best-case (e.g., ACCEPTABLE/AUDIT-READY) when blockers exist
- The agent fabricates citations

## Maintenance

Re-run fixtures after any change to:
- `.claude/skills/agents/{agent}/SKILL.md`
- Reference documents in `references/`
- Review framework dimensions or output format

Add new fixtures when:
- A new review dimension is added to an agent
- A real-world gap is discovered that an agent should catch
- Coverage for a specific artifact type is missing
