---
type: gap-report
status: draft
owner: "@[github-handle]"
generated-on: "[YYYY-MM-DD]"
generated-by: "[code-to-soup-register | code-to-design-inputs | code-to-hazard-candidates]"
scope-statement: "[regulatory/gap-analysis/scope-{effort-name}.md]"
source-tree: "[path analyzed]"
companion-artifact: "[path to XLSX output]"
authorization: "[path from scope statement, or 'none provided']"
related:
  - regulatory/gap-analysis/_SCOPE_TEMPLATE.md
---
# Gap Report — [Skill Name] (Retrospective)

## Summary
- Items identified: [n]
- Complete: [n] ([%])
- Gaps: [n] ([%])
- Warnings: [n] (license/coverage issues, distinct from gaps)
- Source-code traceability: [n]/[n] ([%])

## Gaps by Category

### Rationale Required ([n])
Design inputs/controls where the code behavior is documented but the
rationale for that behavior is missing. Owner: document owner.

| Item ID | Code Reference | What's Needed |
|---------|---------------|---------------|
| [ID] | [file:line] | [description of missing rationale] |

### Intent Unclear ([n])
Items where the code behavior exists but the intent behind the behavior
cannot be reconstructed from code alone. Requires team interview or
product decision. Owner: clinical SME or product owner.

| Item ID | Code Reference | What's Needed |
|---------|---------------|---------------|
| [ID] | [file:line] | [description of unclear intent] |

### Decision Required ([n])
Items where the code presents alternatives or parameterized values that
need an explicit documented choice — e.g., the alarm threshold is
configurable but no documented decision exists for the production value.
Owner: product owner.

| Item ID | Code Reference | What's Needed |
|---------|---------------|---------------|
| [ID] | [file:line] | [decision to be documented] |

### Evidence Required ([n])
Items that reference clinical or regulatory rationale but the referenced
source cannot be located in the repo or linked documents.
Owner: regulatory affairs.

| Item ID | Code Reference | What's Needed |
|---------|---------------|---------------|
| [ID] | [file:line] | [evidence to be located or generated] |

### Documentation Gap ([n])
Code behavior that exists but is not mentioned in the PRD, intended use,
or any specification document. The feature works; it's just undocumented.
Owner: document owner / PM.

| Item ID | Code Reference | What's Needed |
|---------|---------------|---------------|
| [ID] | [file:line] | [behavior to be documented in specs] |

### Implementation Gap ([n])
Behavior described in the PRD or intended use that has no corresponding
code implementation. May be a deferred feature, scope reduction, or
actual bug. Requires product decision. Owner: product owner / engineering.

| Item ID | Spec Reference | What's Needed |
|---------|---------------|---------------|
| [ID] | [document:section] | [build, defer, or descope decision] |

## Recommended Sequence
1. Resolve **Evidence Required** items first — RA can work these independently
2. Schedule rationale workshops for **Intent Unclear** items — requires team availability
3. Fill **Rationale Required** fields — document owner can work through these systematically
4. Make and record **Decision Required** choices — product owner drives
5. Update specs for **Documentation Gap** items — PM adds undocumented behavior to PRD/IFU
6. Triage **Implementation Gap** items — product decision: build, defer, or descope

## What This Report Is Not
This report identifies gaps in the existing artifact set. It does not
constitute a design control activity, a hazard analysis, or any other
regulated activity. The reconstructed artifacts and this gap report
are inputs to a human-led retrospective compliance effort, not
substitutes for it.
