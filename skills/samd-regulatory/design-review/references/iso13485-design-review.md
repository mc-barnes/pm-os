# ISO 13485 Design Review (Clause 7.3.5)

## Requirements
- Systematic examination of design results
- Evaluate ability to meet requirements
- Identify problems, propose actions
- Participants include representatives of all functions concerned

## Required Inputs
1. Design stage outputs (drawings, specs, analysis results)
2. Risk analysis (current state)
3. Verification/validation results (completed to date)
4. User feedback (if available)
5. Previous review action items (closure status)

## Required Outputs
1. Review minutes/record
2. Action items with owners and due dates
3. GO/CONDITIONAL/NO-GO decision
4. Updated risk assessment (if issues found)

## Participant Roles
| Role | Responsibility | Required? |
|------|---------------|-----------|
| Design Owner / PM | Present design status, answer questions | Yes |
| Clinical/Medical | Validate clinical appropriateness | Yes (for SaMD) |
| Quality/Regulatory | Assess compliance, documentation completeness | Yes |
| Engineering Lead | Technical feasibility, architecture review | Yes |
| Data Scientist/ML | Algorithm performance, validation approach | If AI/ML involved |
| Independent Reviewer | Objective assessment (not part of design team) | Yes (FDA expectation) |

## Design Review Types

### PDR (Preliminary Design Review)
- Gate: Concept -> Detailed Design
- Focus: Is the concept viable? Are requirements clear?
- Key questions: Are user needs captured? Is architecture feasible? Are risks identified?

### CDR (Critical Design Review)
- Gate: Detailed Design -> Implementation/V&V
- Focus: Is the design complete enough to build?
- Key questions: Are all DIs addressed? Is risk analysis complete? Is V&V plan ready?

### FDR (Final Design Review)
- Gate: V&V -> Release/Transfer
- Focus: Is the product ready to ship?
- Key questions: Is V&V complete? Are all risks acceptable? Is regulatory submission ready?
