# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-04-30

### Added

- regulatory-reviewer agent persona (`.claude/skills/agents/regulatory-reviewer/`) — FDA SaMD artifact reviewer with two-tier review model, 9 evaluation dimensions (including cybersecurity), and reference index mapping to 28+ docs
- cybersecurity-reviewer agent persona (`.claude/skills/agents/cybersecurity-reviewer/`) — Medical device cybersecurity specialist covering FDA Premarket Cybersecurity Guidance (June 2025), Section 524B, AAMI TIR57, IEC 81001-5-1:2021, with 8 evaluation dimensions
- qa-reviewer agent persona (`.claude/skills/agents/qa-reviewer/`) — ISO 13485 QMS compliance reviewer with 8 evaluation dimensions
- safety-reviewer agent persona (`.claude/skills/agents/safety-reviewer/`) — Patient safety and human factors specialist covering ISO 14971:2019, IEC 62366-1:2015+A1:2020, AI/ML output safety, with 7 evaluation dimensions
- Cybersecurity section in regulatory-reviewer covering FDA Premarket Cybersecurity Guidance (June 2025), SBOM, AAMI TIR57, IEC 81001-5-1:2021
- AI disclaimer on all agent review outputs (regulatory, clinical, QA, safety, cybersecurity)
- Jurisdiction statement (FDA only) on regulatory-reviewer outputs
- 3 cybersecurity reference docs in `references/cybersecurity/` (FDA cybersecurity FAQ, 524B select updates, postmarket guidance)
- Test fixtures in `examples/test-fixtures/` — 4 deliberately broken SaMD artifacts for validating regulatory-reviewer agent detection
- DEC-001 review-panel orchestration decision stub in `team/decisions/`
- `team/specs/` directory for completed specification documents
- CHANGELOG.md (this file)
- Risk acceptability matrix extracted to `regulatory/risk-management/risk-acceptability-matrix-v1.md`

### Changed

- ALARP → AFAP rename in risk-management skill (ISO 14971:2019 alignment)
- Standards editions pinned in root CLAUDE.md (IEC 62304:2006+A1:2015, ISO 14971:2019/EN, etc.)
- FMEA/RPN explicitly scoped as process FMEA with ISO 14971:2019 Annex G citation
- Clinical-reviewer reframed away from named-person impersonation to RPM pattern
- Regulatory-reviewer citation accuracy: "six traceability chains" reframed as industry best practice; software hazard probability softened from universal rule to common approach
- `status.sh` simplified: frontmatter-based filtering replaces hardcoded filename exclusions; test fixtures excluded
- SPEC.md moved from root to `team/specs/regulatory-reviewer-agent-v1.md` with frontmatter

### Fixed

- Mermaid block rendering in README
- Cybersecurity-reviewer FDA guidance date corrected to June 2025 (supersedes September 2023 final guidance)

## [1.0.0] - 2025-04-28

### Added

- Initial repository structure: 7 content folders with CLAUDE.md nav maps and `_TEMPLATE.md` files
- 14 shared skills in `.claude/skills/`
- clinical-reviewer agent persona
- CONTRIBUTING.md routing guide
- Frontmatter schema documented in root CLAUDE.md
- `sources-of-truth.md` and `team/decisions/` structure
- SOUP register template in `engineering/sdlc/`
- CER folder staged in `clinical/`
- 6 example artifacts in `examples/`
- `scripts/status.sh` for frontmatter-based status reporting
