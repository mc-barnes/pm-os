# FDA Software Changes Guidance

## Decision Flowchart (Simplified)

### Step 1: Is there a change to the device?
- No → No submission needed
- Yes → Continue

### Step 2: Does the change affect safety or effectiveness?
- No → Document in DHF, no submission
- Yes → Continue

### Step 3: Is it a new intended use?
- Yes → New 510(k) required
- No → Continue

### Step 4: Could the change affect biocompatibility, sterility, or performance?
- Performance change → Likely new 510(k) or Letter to File with testing evidence
- No impact on above → Letter to File

## Software-Specific Guidance (FDA 2023 Draft)
- **Major changes**: New algorithm, new risk control, new intended use → New 510(k)
- **Moderate changes**: Algorithm parameter change, UI redesign, new data source → Letter to File (with V&V evidence)
- **Minor changes**: Bug fix, cosmetic UI, documentation update → DHF record only

## Letter to File Requirements
1. Description of the change
2. Risk analysis (updated or rationale for no update)
3. Verification/validation evidence
4. Conclusion: change does not require new submission

## Common Mistakes
- Treating algorithm threshold changes as "minor" — they affect diagnostic output
- Not updating risk analysis when adding new failure modes
- Cumulative minor changes that together constitute a major change
