---
name: prd-writer-samd
version: 1.0.0
description: >
  Generate a structured PRD for a software medical device with regulatory sections.
  Triggers: "write PRD", "product requirements", "SaMD PRD", "medical device PRD".
---

# Skill: PRD Writer — Software Medical Device (SaMD)

## Purpose
Generate a structured Product Requirements Document for a software medical device with EHR integration. Tailored for FDA-regulated products using Rhapsody integration engine, HL7, and FHIR standards.

## When to Use
- Starting a new SaMD feature or product
- Portfolio piece: write a PRD to demonstrate regulatory and clinical product thinking
- Interview prep: walk through a PRD you authored to show depth

## When NOT to Use
- Non-regulated product or feature with no FDA/clinical requirements → use `prd-writer`

## Instructions

When I ask you to write a PRD, use this structure. Ask me clarifying questions for any section I haven't provided enough context on. Do NOT fill in sections with generic content — leave them as `[TBD — need input]` if I haven't given you the info.

## PRD Template

```markdown
# PRD: [Product/Feature Name]
**Author**: [Your Name]
**Date**: [date]
**Status**: Draft / In Review / Approved
**Document Version**: 1.0

---

## 1. Intended Use / Indications for Use
- **Intended use statement**: [One sentence — what the device does and for whom]
- **Indications for use**: [Clinical conditions, patient populations, care settings]
- **Contraindications**: [When this device should NOT be used]
- **Target user**: [Clinician type — e.g., telehealth nurse, cardiologist, primary care]

## 2. Product Overview
- **Problem statement**: [What clinical/workflow problem does this solve?]
- **Proposed solution**: [How the product solves it]
- **User workflow**: [Step-by-step: how does the user interact with this?]
- **Key outcomes**: [What changes for the patient/clinician when this works?]

## 3. Regulatory Context
- **Device classification**: [Class I / II / III]
- **Software classification (IEC 62304)**: [Class A / B / C]
- **Regulatory pathway**: [510(k) / De Novo / PMA / Exempt]
- **Predicate device(s)**: [If 510(k) — predicate device name, 510(k) number, comparison]
- **Applicable standards**: [IEC 62304, ISO 14971, IEC 62366, FDA guidance docs]
- **Quality system**: [Design controls per 21 CFR 820]

## 4. Clinical Requirements
- **Clinical evidence needed**: [What studies/data support this?]
- **Clinical validation plan**: [How will clinical accuracy be validated?]
- **Performance targets**: [Sensitivity, specificity, PPV, NPV — with thresholds]
- **Gold standard comparator**: [What is the reference standard?]
- **Patient population considerations**: [Age, comorbidities, skin tone, gestational age, etc.]

## 5. Design Inputs
- **Functional requirements**: [What the system must do — numbered list]
- **Performance requirements**: [Latency, throughput, accuracy thresholds]
- **User interface requirements**: [Key screens, information hierarchy, clinical workflow fit]
- **Safety requirements**: [Per ISO 14971 risk analysis — what can go wrong?]
- **Cybersecurity requirements**: [Per FDA premarket cybersecurity guidance]

## 6. Design Outputs
- **Architecture overview**: [System diagram — data flow from input to output]
- **Algorithm description**: [What the model/algorithm does, inputs, outputs]
- **Verification plan**: [How design outputs will be verified against design inputs]
- **Validation plan**: [How the product will be validated in the intended use environment]

## 7. EHR Integration
- **Integration engine**: Rhapsody
- **Data standards**: [HL7 v2 / FHIR R4 / CDA — specify which]
- **Message types**: [ADT, ORU, ORM, CCD — specify which]
- **Data elements exchanged**: [What data flows in/out of the EHR?]
- **Authentication**: [OAuth 2.0 / SMART on FHIR / other]
- **Target EHR systems**: [Epic, Cerner, Meditech, etc.]
- **Interoperability testing plan**: [How will integration be validated?]

## 8. Risk Analysis (ISO 14971)
- **Hazard identification**: [Top 5 hazards]
- **Risk estimation**: [Severity x probability for each]
- **Risk control measures**: [How each hazard is mitigated]
- **Residual risk acceptability**: [Per risk management plan]

## 9. Data & Privacy
- **Data classification**: [PHI / PII / de-identified]
- **HIPAA compliance**: [Required controls]
- **Data retention policy**: [How long, where stored, deletion process]
- **Audit trail requirements**: [What actions are logged?]

## 10. Success Metrics
- **Clinical**: [e.g., reduction in missed diagnoses, time to triage]
- **Operational**: [e.g., nurse handoff time, false alarm rate]
- **Business**: [e.g., adoption rate, contract renewals, NPS]

## 11. Out of Scope
- [Explicitly list what this PRD does NOT cover]

## 12. Open Questions
- [Questions that need clinical, regulatory, or engineering input before finalizing]

## 13. Appendix
- [References, related documents, prior art]
```

## Quality Checklist
Before finalizing a PRD, verify:
- [ ] Intended use is specific enough to define regulatory pathway
- [ ] Risk analysis covers the top clinical hazards (not just technical risks)
- [ ] EHR integration section specifies actual message types, not just "HL7"
- [ ] Performance targets have specific numbers, not "high accuracy"
- [ ] Out of scope is explicit — prevents scope creep
- [ ] Patient population considerations address health equity (skin tone, age, comorbidities)
