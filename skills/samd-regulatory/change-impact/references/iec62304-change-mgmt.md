# IEC 62304 Change Management

## Clause 6: Software Maintenance
- Establish maintenance plan
- Problem and modification analysis
- Implement modification using same process as original development
- Re-verify affected items (scope based on impact analysis)

## Clause 8: Software Configuration Management
- Configuration identification (baseline items)
- Change control (formal request → analysis → approval → implementation)
- Configuration status accounting (what changed, when, by whom)
- Configuration audit (verify actual matches records)

## Change Control Process
1. **Change Request** — document what and why
2. **Impact Analysis** — trace through design controls and risk analysis
3. **Approval** — appropriate authority based on classification
4. **Implementation** — follow SW development process for affected items
5. **Verification** — re-execute affected test cases
6. **Release** — update baseline, notify stakeholders

## Traceability Requirements
Every change must trace to:
- Affected requirements (DI IDs)
- Affected hazards (HAZ IDs, if risk-related)
- Affected verifications (VER IDs)
- Updated outputs (DO IDs)
