# Clinical

## Doc index
- intended-use/   — Intended use statements, indications for use, and contraindications.
- usability/      — Usability engineering files per IEC 62366. Use specifications, formative/summative studies.
- clinical-evaluation/ — Clinical Evaluation Reports (CER) per EU MDR Annex XIV and PMCF plans.

## Key context
The intended use statement drives classification, risk analysis, and labeling. Changes to intended use have regulatory consequences — always check with regulatory/ before modifying.

## Intended-use change workflow
When any file in `clinical/intended-use/` is created or modified:
1. Flag the change as potentially reclassification-triggering
2. Generate a regulatory impact assessment using the change-impact skill
3. Notify regulatory/ owner to review classification, risk analysis, and submission impact
4. Do NOT merge intended-use changes without documented regulatory review

Key questions for any intended-use change:
- Does this change the device classification? (21 CFR 860 / EU MDR Annex VIII)
- Does this require a new or amended submission? (510(k), De Novo, PMA supplement)
- Does this invalidate existing clinical evidence?
- Does this change the risk profile? (update risk analysis)
- Does this affect labeling / IFU?

## Not in this folder
- Risk analysis or hazard records (→ regulatory/risk-management/)
- Product feature specs (→ product/prds/)
- Implementation details (→ engineering/)
- Post-market clinical follow-up data (→ analytics/post-market/)
