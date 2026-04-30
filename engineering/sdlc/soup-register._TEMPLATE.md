---
type: soup-register
status: draft
owner: [engineering lead]
last-reviewed: YYYY-MM-DD
---
# SOUP Register

> Per IEC 62304:2006+A1:2015 Clauses 5.3.3 (SOUP identification) and 8.1.2 (SOUP configuration).

## Device
- **Device/Software**: [name and version]
- **SW Safety Class**: [A / B / C]

## SOUP Items

| ID | SOUP Name | Version | Manufacturer / Source | Purpose | Known Anomalies Evaluated? | Risk Class Impact | Verification Method | Notes |
|----|-----------|---------|----------------------|---------|---------------------------|-------------------|--------------------|----|
| SOUP-001 | [e.g., NumPy] | [e.g., 1.26.4] | [e.g., numpy.org] | [e.g., Numerical computation for SpO2 signal processing] | [Yes/No — cite anomaly list review] | [Does this SOUP contribute to a hazardous situation? Y/N] | [e.g., Unit tests, integration tests] | [e.g., Pinned in requirements.txt] |

## SOUP Evaluation Criteria (IEC 62304 Clause 8.1.2)
For each SOUP item, evaluate:
1. **Published anomaly lists** — reviewed for impact on device safety?
2. **Adequate documentation** — sufficient to integrate and maintain?
3. **Change control** — version pinned? Update process defined?
4. **Safety class impact** — could a SOUP failure contribute to a hazardous situation?

## Open Items
- [ ] [Outstanding evaluations or missing anomaly reviews]
