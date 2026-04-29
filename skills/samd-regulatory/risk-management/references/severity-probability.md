# Severity and Probability Scales

## Severity Scale (S1-S5)

| Level | Label | Definition | Examples | Neonatal SpO2 Clinical Threshold |
|-------|-------|-----------|----------|----------------------------------|
| S1 | Negligible | Inconvenience, no injury | Minor display delay | SpO2 display delay <30s, no clinical impact |
| S2 | Minor | Temporary discomfort, no intervention | Brief false alarm | False alarm (SpO2 >90%), brief unnecessary check |
| S3 | Serious | Injury requiring intervention | Missed moderate desat -> delayed O2 | Missed moderate desat (SpO2 85-90%) for >2 min; delayed O2 supplementation |
| S4 | Critical | Life-threatening or permanent damage | Missed severe desat -> brain injury | Missed severe desat (SpO2 <85%) for >2 min; risk of HIE Grade 1-2 |
| S5 | Catastrophic | Death | Missed emergency desat -> death | Undetected SpO2 <70% for >5 min; neonatal death or HIE Grade 3 |

Clinical references: AAP/AHA Neonatal Resuscitation Program (NRP) 8th Edition;
Castillo et al. 2008 (preterm SpO2 reference ranges); BOOST II / COT trials.
HIE = Hypoxic-Ischemic Encephalopathy (Sarnat grading: Grade 1 mild, Grade 2 moderate, Grade 3 severe).

## Probability Scale (P1-P5)

| Level | Label | Definition | Approximate Rate |
|-------|-------|-----------|-----------------|
| P1 | Incredible | Essentially impossible | < 1 in 1,000,000 |
| P2 | Improbable | Unlikely but conceivable | 1 in 100,000 |
| P3 | Remote | Could occur over device lifetime | 1 in 10,000 |
| P4 | Occasional | Expected to occur sometimes | 1 in 1,000 |
| P5 | Frequent | Expected to occur regularly | > 1 in 100 |

## 5x5 Risk Acceptability Matrix

```
         P1    P2    P3    P4    P5
S5       A     U     U     U     U
S4       A     A     U     U     U
S3       AC    A     A     U     U
S2       AC    AC    A     A     U
S1       AC    AC    AC    AC    A
```

AC = Acceptable, A = ALARP (As Low As Reasonably Practicable), U = Unacceptable

## ALARP Criteria
Risk in ALARP zone is acceptable only if:
1. Further risk reduction is impracticable, OR
2. Cost of reduction grossly disproportionate to benefit gained

Document rationale for all ALARP decisions.

## FMEA Scales (for RPN calculation)
- Severity (S): 1-10 (maps from S1-S5 above, doubled)
- Occurrence (O): 1-10 (maps from P1-P5 above, doubled)
- Detection (D): 1-10 (10 = no detection method, 1 = certain detection)
- RPN = S x O x D (range 1-1000, threshold typically 100-150)

### Detection Scale (D) — Medical Device Software Context

| D Score | Label | Definition | Monitoring Example |
|---------|-------|-----------|-------------------|
| 1 | Certain | Automatic detection with validated alert | Automated threshold alarm with tested sensitivity >99% |
| 2 | Very High | Automatic detection, high confidence | Confidence scoring with expert queue routing (>95% catch rate) |
| 3 | High | Automatic detection, moderate confidence | ML classifier flag with 85-95% sensitivity |
| 4 | Moderately High | Semi-automatic detection | Trend analysis requiring clinician interpretation |
| 5 | Moderate | Manual detection likely | Visual review of waveform during routine check |
| 6 | Low-Moderate | Manual detection possible | Clinician review of shift summary reports |
| 7 | Low | Manual detection unlikely in time | Retrospective chart review (hours/days after event) |
| 8 | Very Low | Detectable only by investigation | Post-incident root cause analysis |
| 9 | Remote | Detectable only by field complaint | Patient/family reports adverse outcome |
| 10 | Undetectable | No known detection method | Silent failure with no observable output |
