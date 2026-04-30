---
type: risk-record
status: draft
owner: "@agarcia"
related:
  - regulatory/risk-management/risk-spo2-v1.xlsx
  - engineering/rfcs/rfc-alarm-model-v2.md
---

# Expected findings:
# - SAFETY FINDING: "Clinician decides" is not a risk control — human oversight must be validated as effective (IEC 62366-1, ISO 14971:2019 §7.1)
# - SAFETY FINDING: Confidence scores not validated for user interpretation — 73% confidence is meaningless without calibration data
# - GAP: No automation complacency analysis — clinicians may over-rely on model output over time
# - GAP: No threshold effect analysis for boundary cases — how does system behave at confidence = 50%?
# - Expected verdict: SAFETY CONCERN

# Risk Analysis: PulseView AI/ML Classification Output

## 1. Scope

This risk analysis addresses the AI/ML classification model integrated into PulseView that provides desaturation event predictions to clinicians. The model outputs a confidence score (0.0-1.0) alongside each prediction to help clinicians assess the reliability of the system's output.

## 2. Model Description

The PulseView desaturation classifier is a gradient-boosted decision tree model trained on 12,000 annotated SpO2 traces from the MIMIC-III neonatal dataset. The model outputs:
- **Binary prediction:** Desaturation event (Yes/No)
- **Confidence score:** 0.0 to 1.0 representing model certainty

The confidence score is displayed to clinicians alongside the prediction in the monitoring dashboard.

## 3. Intended Use of Confidence Score

The confidence score is provided to help clinicians gauge how certain the model is about its prediction. Higher scores indicate greater model certainty:
- **0.8-1.0:** High confidence — likely a true event
- **0.5-0.8:** Moderate confidence — clinical judgment recommended
- **0.0-0.5:** Low confidence — prediction uncertain

These ranges are displayed in the user interface with color coding (green/yellow/red).

## 4. Risk Analysis

### HAZ-ML-001: Clinician Acts on False Positive
**Hazard:** Model predicts desaturation with high confidence, but no true event
**Harm:** Unnecessary clinical intervention
**Risk Control:** Clinician decides whether to act on prediction — the model is advisory only
**Residual Risk:** Low — clinician makes the final decision

### HAZ-ML-002: Clinician Ignores True Event Due to Low Confidence
**Hazard:** Model correctly detects desaturation but reports low confidence
**Harm:** Clinician dismisses alert, delayed intervention
**Risk Control:** Clinician decides — they can choose to investigate regardless of confidence level
**Residual Risk:** Low — clinician training covers this scenario

### HAZ-ML-003: Model Drift Over Time
**Hazard:** Model performance degrades as patient population changes
**Harm:** Increased false negatives or false positives
**Risk Control:** Periodic model performance review (annual)
**Residual Risk:** Low — annual review will catch drift

### HAZ-ML-004: Confidence Miscalibration
**Hazard:** Confidence scores do not accurately reflect true probability
**Harm:** Clinician misjudges event likelihood based on misleading confidence
**Risk Control:** Clinician decides — confidence is one input among many clinical factors
**Residual Risk:** Low — clinician uses holistic judgment

## 5. Confidence Score Validation

The confidence score was evaluated on a held-out test set of 2,000 traces. The model achieved an AUC of 0.91, indicating good discriminative ability. Confidence scores were not separately calibrated or validated for clinical interpretation.

No study has been conducted to evaluate how clinicians interpret or act on confidence scores in practice.

## 6. Risk Summary

All identified AI/ML-related hazards have residual risk rated as Low. The primary risk control across all hazards is clinician autonomy — the model is advisory only and clinicians make all final clinical decisions. This human oversight layer ensures that model errors do not directly result in patient harm.

## 7. Conclusion

The AI/ML classification model presents acceptable residual risk. Clinician autonomy serves as the primary risk control, ensuring that model outputs inform but do not determine clinical decisions.
