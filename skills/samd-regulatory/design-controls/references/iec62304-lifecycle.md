# IEC 62304 Software Lifecycle

## SW Safety Classes

| Class | Risk | Required Activities |
|-------|------|-------------------|
| A | No injury possible | SW dev planning, requirements, architecture (simplified) |
| B | Non-serious injury | All Class A + detailed design, unit/integration testing, risk mgmt |
| C | Death or serious injury | All Class B + formal V&V, code review, regression testing, full traceability |

## Required Activities by Phase

### Planning (Clause 5.1)
- SW development plan (all classes)
- SW maintenance plan (B, C)
- SW risk management plan (B, C)
- SW configuration management plan (B, C)

### Requirements (Clause 5.2)
All classes: functional, performance, interface, safety requirements.
Class C adds: traceability to system requirements, risk controls.

**Critical linkage**: Design inputs for safety functions MUST trace to hazard controls identified in the ISO 14971 risk analysis. IEC 62304 Clause 5.2.3 requires:
- Safety-related requirements traced from system-level hazard analysis
- Risk controls implemented in software become software requirements
- Software anomaly assessment feeds back into risk analysis

### Architecture (Clause 5.3)
All classes: identify SW items, define interfaces.
Class B/C adds: verify architecture supports risk controls, document rationale.

### Detailed Design (Clause 5.4)
Class B/C only: refine to implementable detail, verify against architecture.

### Implementation (Clause 5.5)
All classes: implement per design.
Class C adds: coding standards, code review.

### Integration & Testing (Clause 5.6-5.7)
Class B/C: integration testing, system testing against requirements.
Class C adds: regression testing after changes.

### Release (Clause 5.8)
All classes: verify completeness of deliverables.
Class C: formal release review with sign-off.

## Common Pitfalls
- Treating Class A as "no documentation needed" — planning is still required
- Missing traceability from risk controls to verification activities
- Not updating safety class when risk analysis changes
