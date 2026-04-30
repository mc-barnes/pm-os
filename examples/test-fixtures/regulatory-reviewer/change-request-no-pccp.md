---
type: change-request
status: draft
owner: "@mlee"
related:
  - engineering/rfcs/rfc-alarm-model-v2.md
  - regulatory/risk-management/risk-spo2-v1.xlsx
---

# Expected findings:
# - BLOCKER: Misclassified as Minor — algorithm retraining with new data is a Major change per FDA software changes guidance (new algorithm behavior, new data source, potential new risk profile)
# - BLOCKER: No risk impact analysis (IEC 62304 Sections 7.4.1–7.4.3 — all changes must be analyzed for safety impact)
# - WARNING: No PCCP assessment — AI/ML model change should reference Predetermined Change Control Plan or justify why a new submission is not required (FDA PCCP guidance Section V.A)
# - WARNING: No verification/validation plan for the retrained model
# - WARNING: No residual risk assessment for the new training data characteristics
# - Expected verdict: NOT SUBMITTABLE

# Change Request: CR-2026-017

## Change Title

Retrain SpO2 Adaptive Alarm Model with Expanded NICU Dataset

## Change Classification

**Classification: Minor**

Rationale: The change updates model weights using a larger training dataset. The underlying algorithm architecture remains unchanged. No new features or user-facing behavior changes are introduced.

## Description of Change

The current SpO2 adaptive alarm model (v1.2) was trained on 12,000 annotated SpO2 traces from the MIMIC-III neonatal subset. This change request proposes retraining the model on an expanded dataset of 45,000 traces, incorporating data from three additional NICUs:

- **New data sources:**
  - Children's Hospital of Philadelphia NICU (18,000 traces, 2019–2024)
  - Boston Children's Hospital NICU (9,000 traces, 2020–2024)
  - Texas Children's Hospital NICU (6,000 traces, 2021–2024)

- **Training changes:**
  - Dataset expanded from 12,000 to 45,000 traces
  - New sites introduce different sensor hardware (Masimo SET, Nellcor N-600) not present in original training data
  - Gestational age range expanded from 28–40 weeks to 24–42 weeks (now includes extremely preterm infants)
  - Annotation protocol unchanged — all traces labeled by board-certified neonatologists using the same rubric

- **Model architecture:**
  - No changes to model architecture (1D-CNN with attention mechanism)
  - Hyperparameters unchanged (learning rate, batch size, epochs)
  - Output format unchanged (binary alarm/no-alarm decision with confidence score)

## Justification

The expanded dataset is expected to improve model generalization across sensor types and gestational age ranges. Internal cross-validation on the combined dataset shows:
- Sensitivity for true desaturation: 96.2% (up from 95.1%)
- Specificity: 78.4% (up from 71.2%)
- False alarm reduction: 58% (up from 52%)

## Implementation Plan

1. Merge new training data into existing data pipeline
2. Run training pipeline with existing hyperparameters
3. Evaluate on held-out test set (20% split)
4. Deploy updated model weights to staging environment
5. Run 7-day shadow mode comparison against production model
6. If shadow mode results are satisfactory, promote to production

## Affected Components

- Model weights file: `models/spo2_alarm_v1.3.weights`
- No code changes required
- No UI changes
- No database schema changes

## Testing

- Unit tests: existing test suite passes (no code changes)
- Integration tests: verify model loading and inference with new weights
- Shadow mode: 7-day parallel comparison in staging

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Software Lead | @tcheng | — | — |
| QA Lead | @jpark | — | — |
| Regulatory | — | — | — |
