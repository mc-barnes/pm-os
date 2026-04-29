---
name: design-controls
description: >
  Generate IEC 62304 / ISO 13485 design controls traceability matrices as XLSX.
  Use when building user needs, design inputs/outputs, verification/validation
  records, traceability matrices, or any design control documentation for
  SaMD (Software as a Medical Device). Triggers: "design controls",
  "traceability matrix", "IEC 62304", "user needs to design inputs",
  "V&V traceability", "design input", "design output".
---

# Design Controls Generator

## When to Use

- Building traceability matrices for FDA/notified body submissions
- Converting user needs into formal design inputs/outputs
- Generating V&V record templates with proper linking
- Preparing for design reviews or audits
- Bootstrapping design control documentation for a new SaMD project
- Mapping existing requirements to IEC 62304 / ISO 13485 structure

## When NOT to Use

- Risk management documents (use ISO 14971 risk skill instead)
- Software architecture documentation (use ADR skill)
- Clinical evaluation reports (CER)
- General project planning that isn't design-control-specific

## Quick Start

```bash
# Generate SpO2 example (5 user needs, full traceability)
python scripts/generate_design_controls.py --example spo2

# Custom device with safety class
python scripts/generate_design_controls.py --device-name "Insulin Pump Controller" --safety-class C

# Output: output/design-controls-{device_name}.xlsx
```

## XLSX Structure

The generated workbook contains 6 sheets with full forward/backward traceability.

### Sheet 1: User_Needs

| Column | Content |
|--------|---------|
| ID | UN-001, UN-002, ... |
| Need Statement | What the user/stakeholder actually needs |
| Source | Where the need was identified |
| Priority | High / Medium / Low |
| Acceptance Criteria | How we know the need is satisfied |

### Sheet 2: Design_Inputs

| Column | Content |
|--------|---------|
| ID | DI-001, DI-002, ... |
| Linked UN | Parent user need ID |
| Requirement | Measurable, testable requirement |
| Type | Functional / Performance / Safety / Interface |
| SW Safety Class | A / B / C per IEC 62304 |
| Safety Class Rationale | Justification for the assigned safety class |

### Sheet 3: Design_Outputs

| Column | Content |
|--------|---------|
| ID | DO-001, DO-002, ... |
| Linked DI | Parent design input ID |
| Output Description | What was produced to satisfy the input |
| Verification Method | Inspection / Analysis / Test / Demonstration |

### Sheet 4: Verification

| Column | Content |
|--------|---------|
| ID | VER-001, VER-002, ... |
| Linked DO | Design output being verified |
| Test Protocol | Reference to test procedure |
| Pass Criteria | Quantitative acceptance threshold |
| Status | Pass / Fail / Pending (data-validated dropdown) |
| Test Data Source | Description of test data origin and size |

### Sheet 5: Validation

| Column | Content |
|--------|---------|
| ID | VAL-001, VAL-002, ... |
| Linked UN | User need being validated |
| Validation Method | Usability study / Clinical trial / Simulation |
| Acceptance Criteria | Evidence threshold for user need satisfaction |
| Status | Pass / Fail / Pending (data-validated dropdown) |

### Sheet 6: Traceability_Matrix

Forward and backward trace using VLOOKUP formulas that pull live data from other sheets. Includes summary stats (COUNTIF for pass/fail/pending counts).

## ID Conventions

```
UN-001  → User Need
DI-001  → Design Input (links back to UN)
DO-001  → Design Output (links back to DI)
VER-001 → Verification (links back to DO)
VAL-001 → Validation (links back to UN)
```

Sequential numbering. Never reuse IDs even if deprecated. See `references/id-conventions.md`.

## SW Safety Classes

| Class | When to Apply | Documentation Burden |
|-------|--------------|---------------------|
| A | SW cannot contribute to hazardous situation | Minimal — planning + requirements |
| B | SW can contribute to non-serious injury | Moderate — add detailed design, unit testing |
| C | SW can contribute to death/serious injury | Full — formal V&V, code review, regression, complete trace |

Default to Class C if uncertain. Downgrading requires documented risk analysis justification.

## Reference Files

- `references/iec62304-lifecycle.md` — Activities by safety class and lifecycle phase
- `references/iso13485-design-controls.md` — Clause 7.3 mapping + FDA 820.30 crosswalk
- `references/id-conventions.md` — Numbering rules and linking patterns

## Verification Checklist

Before shipping any design controls document:

- [ ] Every UN has at least one DI linked to it
- [ ] Every DI has exactly one DO
- [ ] Every DO has a VER record with quantitative pass criteria
- [ ] Every UN has a VAL record
- [ ] Traceability matrix has no orphan rows (unlinked items)
- [ ] Safety class is documented and justified
- [ ] Status fields use only allowed values (Pass/Fail/Pending)
- [ ] IDs are sequential with no gaps or reuse
- [ ] All formulas resolve (no #REF! or #N/A in traceability sheet)
- [ ] File naming follows convention: `design-controls-{device-name}.xlsx`

## Implementation Notes

- Script uses only `openpyxl` + stdlib — no heavy dependencies
- VLOOKUP formulas are Excel-native (not Python-computed values)
- Conditional formatting: green=Pass, red=Fail, yellow=Pending
- Headers: bold white text on dark blue (#1F4E79)
- Column widths auto-sized to content
- Data validation dropdowns enforce allowed Status values
