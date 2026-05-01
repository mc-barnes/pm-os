# Gap Categories

Taxonomy of gap types used by the gap-analysis module. Each category routes to an accountable owner and defines a remediation path.

## Category Reference

| Category | Owner | Remediation | When It Applies |
|----------|-------|-------------|-----------------|
| Rationale Required | Document owner | Write the rationale for existing behavior | Code behavior documented but "why" is missing |
| Intent Unclear | Clinical SME / product owner | Workshop or interview to reconstruct intent | Code behavior exists but intent can't be determined from code alone |
| Decision Required | Product owner | Make and document the decision | Parameterized or configurable values without a documented production choice |
| Evidence Required | Regulatory affairs | Locate or generate the clinical/regulatory evidence | Clinical or regulatory rationale referenced but source not found |
| Documentation Gap | PM / document owner | Add undocumented behavior to specs | Code works but no PRD, IFU, or spec mentions it |
| Implementation Gap | Product owner / engineering | Decide: build, defer, or descope | PRD/IFU describes behavior with no corresponding code |

## Owner Routing

| Owner | Categories they resolve | Typical artifact |
|-------|------------------------|-----------------|
| Document owner | Rationale Required, Documentation Gap | Design input rationale fields, PRD updates |
| Clinical SME | Intent Unclear | Workshop notes, clinical rationale statements |
| Product owner | Intent Unclear, Decision Required, Implementation Gap | Decision records, PRD updates, backlog items |
| Regulatory affairs | Evidence Required | Literature references, standards citations, clinical evidence summaries |
| Engineering | Implementation Gap (code changes) | Code commits, test evidence |

## Severity in Retrospective Mode

When reviewer agents operate in retrospective mode, gap categories map to finding severities:

| Category | regulatory-reviewer | safety-reviewer | qa-reviewer |
|----------|-------------------|-----------------|-------------|
| Rationale Required | BLOCKER | BLOCKER (if safety-related) | Finding |
| Intent Unclear | BLOCKER | BLOCKER (if safety-related) | Finding |
| Decision Required | BLOCKER | BLOCKER (if safety-related) | Finding |
| Evidence Required | BLOCKER | BLOCKER | Finding |
| Documentation Gap | Major | Minor (unless safety-related) | Finding |
| Implementation Gap | Major | Major (if safety-related) | Finding |

## Skill-Specific Categories

Individual skills may add domain-specific sub-categories:

- **code-to-soup-register:** Evaluation required, Anomaly review required, License review required, Lock file missing, Integration documentation required
- **code-to-design-inputs:** Uses the 6 standard categories above
- **code-to-hazard-candidates:** All items carry `Status: CANDIDATE` — a special status meaning "requires human dispositioning" (accept, modify, or reject with rationale)
