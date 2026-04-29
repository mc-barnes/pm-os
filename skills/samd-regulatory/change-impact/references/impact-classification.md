# Change Impact Classification

## Classification Levels

### Minor
- Definition: No impact on safety, effectiveness, or intended use
- Examples: Typo fixes, cosmetic UI changes, documentation updates, logging improvements
- Regulatory: DHF record only
- Re-verification: None or targeted unit tests
- Approval: Developer + reviewer

### Major
- Definition: Affects performance, adds features, or modifies clinical behavior
- Examples: Threshold changes, new triage tier, algorithm parameter updates, new data source
- Regulatory: Letter to File with V&V evidence
- Re-verification: Affected integration/system tests + regression
- Approval: PM + Clinical + QA

### Critical
- Definition: Affects intended use, safety controls, or creates new hazards
- Examples: New clinical indication, new risk control implementation, safety-critical algorithm change
- Regulatory: New 510(k) or De Novo likely required
- Re-verification: Full system V&V
- Approval: PM + Clinical + Regulatory + QA + Executive

## Classification Decision Aids

### Algorithm Changes
| Change Type | Classification |
|------------|---------------|
| Fix bug in existing logic | Minor (if no clinical impact) or Major |
| Change threshold value | Major |
| Add new classification tier | Major or Critical |
| New algorithm approach | Critical |
| New ML model architecture | Critical |

### UI Changes
| Change Type | Classification |
|------------|---------------|
| Color/font change | Minor |
| Add informational field | Minor |
| Reorganize clinical display | Major |
| Change alarm presentation | Critical |

### Data Changes
| Change Type | Classification |
|------------|---------------|
| Add logging field | Minor |
| New data source integration | Major |
| Change clinical data format | Major |
| New patient population | Critical |

## Cumulative Impact Assessment

Multiple minor changes can collectively constitute a major or critical change. Evaluate cumulative impact when:

### Escalation Triggers
- **3+ minor changes to the same module** within a release cycle → Reassess as Major
- **5+ minor changes across the system** within 6 months → Reassess overall impact
- **Any minor change that touches a previously-changed file** from a recent minor CR → Reassess interaction effects
- **Cumulative test coverage gap**: if minor changes collectively bypass >20% of system test cases → Major

### Assessment Process
1. List all changes since last formal release (or last major/critical change)
2. Map affected requirements (DI IDs) — look for overlapping DI coverage
3. Map affected hazards (HAZ IDs) — look for compound risk pathways
4. If any two changes affect the same hazard's risk control → escalate to Major minimum
5. Document cumulative assessment conclusion in Change Impact report

### Time Window
- Default: since last formal release baseline
- If continuous deployment: rolling 6-month window
- For adaptive AI/ML: since last predetermined change control plan review
