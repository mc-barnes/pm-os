---
name: code-to-soup-register
version: 1.0.0
description: >
  Reverse-engineer a SOUP register from an existing codebase. Parses dependency
  manifests across Python, JavaScript/TypeScript, Go, and Java/Kotlin to produce
  an IEC 62304 §5.3.3 compliant SOUP register XLSX with companion gap report.
  Triggers: "SOUP from code", "dependency register", "code-to-soup-register",
  "SOUP register from repo", "reverse-engineer SOUP", "retrospective SOUP".
---

# code-to-soup-register

Reverse-engineer a SOUP register from dependency manifests in an existing codebase. Produces an IEC 62304 §5.3.3 / §8.1.2 compliant XLSX with a companion gap report documenting where human evaluation is required.

## When to Use

- Existing codebase with no SOUP register — building one retrospectively
- Preparing for a first regulatory submission and need to inventory all dependencies
- Auditing dependency completeness against an existing SOUP register
- Running as part of a gap analysis effort (via `/gap-analysis soup`)

## When NOT to Use

- Greenfield project — use the prospective SOUP register template instead
- Updating an existing, maintained SOUP register — use change-impact instead
- License-only audit without IEC 62304 context — use a standard license scanner

## Quick Start

```bash
# Generate from your repo (Python/JS/Go/Java auto-detected)
python .claude/skills/code-to-soup-register/scripts/generate_soup_register.py \
  --source /path/to/repo

# Generate with scope statement reference
python .claude/skills/code-to-soup-register/scripts/generate_soup_register.py \
  --source /path/to/repo --scope regulatory/gap-analysis/scope-mydevice.md

# Generate example output (no repo needed)
python .claude/skills/code-to-soup-register/scripts/generate_soup_register.py --example
```

## Language Support

| Language | Manifest Files | Lock Files | Notes |
|----------|---------------|------------|-------|
| Python | requirements.txt, Pipfile, pyproject.toml | Pipfile.lock | tomllib (Python 3.11+) for pyproject.toml |
| JavaScript/TypeScript | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml | Monorepo detection not in v1 |
| Go | go.mod | go.sum | Module-aware only |
| Java/Kotlin | pom.xml | — | Maven XML parsing via xml.etree |

## XLSX Structure

### Sheet: SOUP_Register

| Column | Auto-populated? | Notes |
|--------|----------------|-------|
| SOUP ID | Yes | SOUP-001, SOUP-002, ... |
| Component Name | Yes | Package name from manifest |
| Version | Yes | From lock file or manifest |
| Declared / Transitive | Yes | `declared` or `transitive` |
| License | Yes | From manifest metadata; GAP if unavailable |
| License Flag | Yes | OK or WARNING (GPL/AGPL/SSPL/Unknown) |
| Repository URL | Yes | From manifest metadata; GAP if unavailable |
| Last Release Date | Yes | From manifest metadata; GAP if unavailable |
| Fitness for Intended Use | No — GAP | Requires human evaluation |
| Known Anomalies Reviewed | No — GAP | Requires human review of CVE/issue tracker |
| Integration Requirements | No — GAP | Requires human documentation |
| Version Pinned | Yes | Lock file present and version resolved |
| Gap Status | Formula | COMPLETE / GAP / WARNING |

### Sheet: Document_Control

Standard document control sheet with device name, date, and approval signatures.

## ID Conventions

```
SOUP-001 → First SOUP component (alphabetical by name)
SOUP-002 → Second SOUP component
...
```

Sequential numbering. Declared dependencies first, then transitive. Never reuse IDs.

## Gap Report Categories

The companion gap report uses these SOUP-specific categories:

| Category | Owner | Description |
|----------|-------|-------------|
| Evaluation required | Engineering | Fitness for intended use not assessed |
| Anomaly review required | Engineering | Known issues/CVEs not reviewed |
| License review required | Legal / RA | Problematic or unknown license detected |
| Lock file missing | Engineering | Dependency versions not pinned |
| Integration documentation required | Engineering | SOUP integration requirements not documented |

## Reference Files

- `references/soup-classification.md` — IEC 62304 §5.3.3 SOUP criteria, license tiers

## Verification Checklist

Before accepting a generated SOUP register:

- [ ] All detected manifest files are listed in the gap report header
- [ ] Lock file presence/absence is documented per language
- [ ] Transitive dependencies are distinguished from declared dependencies
- [ ] GPL/AGPL/SSPL/Unknown licenses flagged as WARNING
- [ ] Fitness, Anomalies, and Integration columns are GAP (not auto-filled)
- [ ] Gap Status formula correctly computes COMPLETE / GAP / WARNING
- [ ] SOUP IDs are sequential with no gaps
- [ ] No network calls were made (all data from local manifests)
- [ ] Companion gap report references scope statement if provided
- [ ] File naming follows convention: `soup-register-{source-name}.xlsx`

## Implementation Notes

- Script uses only `openpyxl` + stdlib — no heavy dependencies
- Python 3.11+ required for `tomllib` (pyproject.toml parsing)
- No network calls — license and release date from manifest data only, marked GAP when unavailable
- Gradle dependencies parsed from `gradle dependencies` text output, not Gradle DSL
- Gap Status formula: `=IF(OR(I{row}="GAP",J{row}="GAP",K{row}="GAP"),"GAP",IF(F{row}="WARNING","WARNING","COMPLETE"))`
