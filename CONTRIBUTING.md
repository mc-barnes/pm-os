# Contributing to SaMD Team OS

## Where does this go?

| If you're writing... | It lives in... | Filename pattern |
|---------------------|----------------|-----------------|
| Feature spec / PRD | product/prds/ | prd-{feature}-v{n}.md |
| Customer call notes | product/customers/{name}/calls/ | {date}-{topic}.md |
| Competitive analysis | product/competitive/ | {competitor}-v{n}.md |
| Product strategy | product/strategy/ | {topic}-v{n}.md |
| Hazard analysis / FMEA | regulatory/risk-management/ | risk-{device}-v{n}.xlsx |
| Design controls matrix | regulatory/design-controls/ | design-controls-{device}-v{n}.xlsx |
| Submission package | regulatory/submissions/ | {submission-type}-{device}-v{n}.md |
| Change request / impact | regulatory/change-control/ | cr-{nnn}-{slug}.md |
| Design history record | regulatory/design-history/ | dhf-{device}.md |
| Intended use statement | clinical/intended-use/ | intended-use-{device}-v{n}.md |
| Usability study | clinical/usability/ | {study-type}-{device}-v{n}.md |
| Clinical evaluation | clinical/clinical-evaluation/ | cer-{device}-v{n}.md |
| Post-market surveillance | analytics/post-market/ | {metric-or-query}.md |
| Product metrics | analytics/product-metrics/ | {metric-or-query}.md |
| Bug investigation | engineering/bugs/ | bug-{id}-{slug}.md |
| Technical RFC | engineering/rfcs/ | rfc-{nnn}-{slug}.md |
| SDLC phase record | engineering/sdlc/ | {phase}-{device}-v{n}.md |
| SOUP register | engineering/sdlc/ | soup-register.md |
| CAPA record | quality/capa/ | capa-{nnn}-{slug}.md |
| Complaint record | quality/complaints/ | comp-{nnn}-{slug}.md |
| Audit record | quality/audits/ | audit-{type}-{date}.md |
| Cross-functional decision | team/decisions/ | dec-{nnn}-{slug}.md |
| Retro | team/retros/ | retro-{date}.md |

## Ambiguous cases

| Scenario | Where it goes | Why |
|----------|--------------|-----|
| Regulatory impact of a clinical decision | regulatory/change-control/ (regulatory record) + link to clinical/ source | Regulatory folder holds the regulatory record; clinical/ holds the originating decision |
| Threshold change affecting risk + code | engineering/rfcs/ (RFC) → links to regulatory/risk-management/ (updated risk) + regulatory/change-control/ (CR) | RFC is the originating decision; risk and change-control are downstream records |
| Decision spanning product + clinical + reg + eng | team/decisions/ with `related:` links to all affected domains | Cross-functional decisions get their own home |

## File naming rules
- Kebab-case, no spaces, no dates in filenames (dates go in frontmatter)
- Version suffix: `-v{n}` (e.g., `risk-spo2-v3.xlsx`)
- Never reuse IDs even if deprecated
- Templates: `_TEMPLATE.md` in each subfolder

## Cross-reference syntax
- ID references: `(see HAZ-007 in regulatory/risk-management/risk-spo2-v2.xlsx)`
- Document links: `[design-controls-spo2-v2.xlsx](regulatory/design-controls/design-controls-spo2-v2.xlsx)`
- In XLSX: use the ID directly (HAZ-007, RC-003, DI-027) — the XLSX cross-links via formulas
