# PRD: Neonatal SpO2 Overnight Triage System
**Author**: [Your Name]
**Date**: 2026-04-28
**Status**: Draft
**Document Version**: 1.0

---

## 1. Intended Use / Indications for Use
- **Intended use statement**: Automated overnight SpO2 monitoring triage system that classifies pulse oximetry traces into clinical urgency tiers for NICU nursing staff.
- **Indications for use**: Neonatal patients (24-44 weeks gestational age) on continuous pulse oximetry monitoring in NICU settings. The system analyzes overnight SpO2 traces and generates clinical handoff summaries with urgency classification.
- **Contraindications**: Not intended for real-time alarm management. Not a replacement for bedside clinical assessment. Should not be used as the sole basis for clinical decision-making.
- **Target user**: NICU nurses (day shift) receiving overnight monitoring handoffs.

## 2. Product Overview
- **Problem statement**: NICU nurses reviewing overnight SpO2 data spend 15-30 minutes per patient manually interpreting desaturation patterns, artifact-affected readings, and baseline shifts. High-acuity events may be buried in hours of data, and inconsistent handoff quality leads to missed or delayed clinical action.
- **Proposed solution**: AI-assisted triage system that: (1) classifies overnight SpO2 traces into 5 urgency tiers (emergency, urgent, monitor, routine, artifact), (2) generates structured nurse handoff summaries with clinical context, and (3) flags safety-critical desaturation events for immediate review.
- **User workflow**:
  1. Overnight SpO2 data is exported from bedside monitor
  2. System ingests trace data and patient demographics (gestational age, baseline SpO2)
  3. Rule engine classifies clear cases (Tier 1: ~58% auto-classified)
  4. Pattern classifier handles ambiguous cases (Tier 2: ~39%)
  5. Remaining cases route to expert queue (Tier 3: ~3%)
  6. Nurse receives triage summary with urgency tier, key findings, and recommended actions
- **Key outcomes**: Reduced handoff preparation time from 15-30 min to <5 min per patient. Zero missed urgent desaturation events. Consistent handoff quality across shifts.

## 3. Regulatory Context
- **Device classification**: Class II (with special controls)
- **Software classification (IEC 62304)**: Class C — software failure could contribute to a hazardous situation resulting in serious injury (missed urgent desaturation)
- **Regulatory pathway**: 510(k) — predicate: existing SpO2 clinical decision support systems
- **Predicate device(s)**: [TBD — need input on specific predicate]
- **Applicable standards**: IEC 62304 (software lifecycle), ISO 14971 (risk management), IEC 62366 (usability engineering), FDA guidance on Clinical Decision Support Software
- **Quality system**: Design controls per 21 CFR 820, ISO 13485 certified QMS

## 4. Clinical Requirements
- **Clinical evidence needed**: Retrospective validation against clinician-labeled SpO2 traces. Prospective usability study with NICU nurses.
- **Clinical validation plan**: 300+ traces labeled by 2+ neonatologists (inter-rater reliability ≥0.8 Cohen's kappa). Compare system triage against clinician consensus.
- **Performance targets**:
  - Urgent/emergency sensitivity: ≥95% (zero missed urgent desaturations is safety target)
  - Overall triage accuracy: ≥85%
  - Artifact detection specificity: ≥90%
  - False urgent rate: <10%
- **Gold standard comparator**: Board-certified neonatologist consensus classification (2 reviewers + adjudication)
- **Patient population considerations**: Gestational age 24-44 weeks. GA-adjusted SpO2 thresholds per published references (Castillo 2008, Hay 2002). Skin tone does not affect pulse oximetry SpO2 values directly but probe placement quality may vary — artifact detection must account for this.

## 5. Design Inputs
- **Functional requirements**:
  1. FR-001: System SHALL classify SpO2 traces into exactly one of 5 tiers: emergency, urgent, monitor, routine, artifact
  2. FR-002: System SHALL apply GA-adjusted SpO2 thresholds for preterm vs. term neonates
  3. FR-003: System SHALL detect SpO2 <80% sustained ≥30s as emergency tier
  4. FR-004: System SHALL generate nurse handoff summary for each classified trace
  5. FR-005: System SHALL flag cases where artifact detection overrides an urgent signal (safety check)
  6. FR-006: System SHALL calculate SatSeconds hypoxemic burden metric for urgent/emergency cases
  7. FR-007: System SHALL route ambiguous cases (Tier 2 confidence <70%) to expert queue
- **Performance requirements**: Classification latency <30s per trace. Dashboard load time <3s.
- **User interface requirements**: Triage summary dashboard showing per-patient urgency tier, key SpO2 statistics, desaturation event count, and recommended actions. Color-coded urgency (red/orange/yellow/green/gray).
- **Safety requirements**: Per ISO 14971 — urgent false negative is the highest-severity hazard. Safety check prevents artifact labeling from ever masking a genuine desaturation event.
- **Cybersecurity requirements**: Per FDA premarket cybersecurity guidance — all patient data encrypted at rest and in transit. No PHI in log files. Role-based access control.

## 6. Design Outputs
- **Architecture overview**: 7-phase pipeline: Synthetic Data → Rule Engine (Tier 1) → Pattern Mining → Pre-Annotation Classifier (Tier 2) → LLM Evaluators → Handoff Generator → Dashboard
- **Algorithm description**: Tier 1 uses threshold-based rules with GA adjustment. Tier 2 uses decision tree + association rules trained on Tier 1 outputs. LLM evaluators assess clinical accuracy, handoff quality, and artifact handling.
- **Verification plan**: 15 unit tests covering safety checks, classification boundaries, GA-adjusted thresholds. LLM-as-judge evaluation on 10+ traces per run.
- **Validation plan**: Prospective usability study with 10 NICU nurses reviewing system-generated handoffs vs. manual handoffs. Measure time savings, accuracy, and nurse confidence.

## 7. EHR Integration
- **Integration engine**: Rhapsody
- **Data standards**: HL7 v2.5.1 (ORU^R01 for SpO2 results), FHIR R4 (Observation, DiagnosticReport)
- **Message types**: ADT^A01 (admit), ORU^R01 (SpO2 observations), ACK (acknowledgment)
- **Data elements exchanged**: Patient ID, gestational age, SpO2 values (mean, min, max), desaturation events, triage classification, handoff summary text
- **Authentication**: OAuth 2.0 / SMART on FHIR for EHR write-back
- **Target EHR systems**: Epic (initial), Cerner (phase 2)
- **Interoperability testing plan**: Validate HL7v2 message parsing with Rhapsody test routes. FHIR bundle validation against US Core profiles. End-to-end test with EHR sandbox environment.

## 8. Risk Analysis (ISO 14971)
- **Hazard identification**:
  1. H-001: Urgent desaturation classified as routine (missed urgent) — Severity: 5, Probability: 2
  2. H-002: Artifact classified as urgent (false alarm fatigue) — Severity: 2, Probability: 3
  3. H-003: GA threshold misconfigured for patient age — Severity: 4, Probability: 2
  4. H-004: System unavailable during critical overnight period — Severity: 3, Probability: 2
  5. H-005: Handoff summary contains inaccurate clinical information — Severity: 4, Probability: 2
- **Risk control measures**:
  1. H-001: Safety check prevents artifact from overriding urgent signal. Raw signal analysis as secondary check.
  2. H-002: Artifact detection uses multiple signal quality indicators. Confidence threshold routing to expert queue.
  3. H-003: GA thresholds from published references, validated against clinical consensus.
  4. H-004: Graceful degradation — manual review workflow available when system is offline.
  5. H-005: LLM evaluator validates handoff content. Template-based generation with structured fields.
- **Residual risk acceptability**: All residual risks acceptable per risk management plan. No unacceptable residual risks after control measures applied.

## 9. Data & Privacy
- **Data classification**: PHI (patient demographics, SpO2 readings linked to patient ID)
- **HIPAA compliance**: Encryption at rest (AES-256) and in transit (TLS 1.3). Access logging. BAA with cloud provider. Minimum necessary access principle.
- **Data retention policy**: SpO2 traces retained for 7 years per medical record requirements. De-identified data may be retained longer for algorithm improvement.
- **Audit trail requirements**: All triage classifications logged with timestamp, input data hash, model version. All user access to patient data logged.

## 10. Success Metrics
- **Clinical**: Zero missed urgent desaturations (sensitivity ≥95%). Handoff quality pass rate ≥90%.
- **Operational**: Handoff preparation time reduced from 15-30 min to <5 min. Nurse satisfaction score ≥4/5.
- **Business**: Adoption by 3+ NICU units within 12 months. Reduction in overnight callback rate by 20%.

## 11. Out of Scope
- Real-time alarm management (this is a retrospective triage system)
- SpO2 probe hardware or signal acquisition
- Treatment recommendations or medication orders
- Adult or pediatric (non-neonatal) populations
- Integration with non-Epic/Cerner EHR systems in v1

## 12. Open Questions
- What is the appropriate predicate device for 510(k) submission?
- Should the system include a "learning mode" where clinician feedback improves classification?
- What is the minimum number of traces needed for clinical validation?
- How should the system handle patients with known chronic desaturation (e.g., cyanotic heart disease)?

## 13. Appendix
- Castillo A, et al. (2008). "Pulse oxygen saturation levels and arterial oxygen tension values in newborns receiving oxygen therapy in the neonatal intensive care unit."
- Hay WW, et al. (2002). "Pulse oximetry in neonatal medicine."
- FDA Guidance: Clinical Decision Support Software (2022)
- IEC 62304:2006+A1:2015 — Medical device software — Software life cycle processes
- ISO 14971:2019 — Medical devices — Application of risk management to medical devices
