---
type: scope-statement
status: draft
owner: "@[github-handle]"
authorization: "[path to CAPA, project plan, or management decision authorizing this effort]"
generated-on: "[YYYY-MM-DD]"
related:
  - regulatory/gap-analysis/_GAP_REPORT_TEMPLATE.md
---
# Gap Analysis Scope Statement

## Authorization
- **Authorizing document:** [path to CAPA, project plan, or quality record]
- **Authorized by:** [name and role]
- **Date authorized:** [YYYY-MM-DD]

## Scope
- **Repository/repositories:** [path(s) to source tree(s) under analysis]
- **Languages detected:** [auto-populated by skills]
- **Excluded paths:** [test/, vendor/, docs/, etc. — explicitly listed]

## Device Context
- **Device name:** [product name]
- **Device classification:** [Class I / Class II / Class III]
- **Regulatory pathway:** [510(k) / De Novo / PMA]
- **Predicate device:** [predicate name and 510(k) number, or "De Novo — no predicate"]
- **Clinical domain:** [e.g., neonatal monitoring, cardiac rhythm classification, CGM]
- **IEC 62304 software safety class:** [A / B / C, or "to be determined"]

## Accountable Owners
- **Gap analysis lead:** [name — accountable for driving the effort]
- **Regulatory affairs:** [name — accountable for regulatory judgment calls]
- **Clinical SME:** [name — accountable for clinical rationale review]
- **QA lead:** [name — accountable for QMS integration]
- **Engineering lead:** [name — accountable for code-level accuracy]

## Skills to Run
- [ ] code-to-soup-register
- [ ] code-to-design-inputs
- [ ] code-to-hazard-candidates

## What This Effort Is Not
This gap analysis produces draft artifacts and a gap report identifying where
documentation is missing. It does not constitute a design control activity,
a hazard analysis, a SOUP evaluation, or any other regulated activity.
The outputs are inputs to a human-led retrospective compliance effort,
not substitutes for it.
