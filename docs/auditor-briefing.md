---
type: onboarding
status: draft
owner: "@mc-barnes"
last-reviewed: 2026-04-30
related:
  - docs/responsible-use.md
  - docs/adoption-guide.md
---
# Auditor Briefing — AI-Assisted Artifact Review

One-page summary for QA leads preparing for audits, or for auditors asking about AI tool usage.

## What It Is

SaMD Team OS includes AI reviewer agents that pre-screen draft regulatory artifacts (PRDs, risk analyses, CAPA records, threat models, etc.) before human expert review. The agents identify structural gaps, missing standards citations, and common deficiencies — similar to a checklist, but able to read and interpret document content.

## What It Is Not

- **Not a quality system.** samd-os is a working environment. The eQMS (Greenlight Guru, MasterControl, Qualio, etc.) remains the system of record for all controlled documents.
- **Not a reviewer of record.** Agent findings are screening output. No document is approved, signed, or released based on agent review alone. Human reviewers (RA, QA, clinical) retain full accountability.
- **Not Part 11 / Annex 11 compliant.** Agent outputs have no electronic signatures, no audit trail in the regulatory sense, and no access controls beyond standard Git permissions.
- **Not a replacement for qualified personnel.** Agents augment — they do not replace — regulatory, quality, safety, and clinical expertise.

## How It Works

1. A team member drafts an artifact (PRD, risk analysis, CAPA record, etc.)
2. They invoke one or more reviewer agents via Claude Code
3. The agent reads the artifact and produces structured findings with standards citations
4. The team member addresses findings and revises the draft
5. A qualified human reviewer conducts the formal review
6. The approved artifact is uploaded to the eQMS as a controlled record

Agent review is an informal pre-screening step. It is not documented as part of the formal design review or approval workflow.

## Scope

| Agent | Domain | Standards Referenced |
|-------|--------|---------------------|
| Regulatory Reviewer | Design controls, submissions, IEC 62304 compliance | IEC 62304:2006+A1:2015, ISO 14971:2019, ISO 13485:2016, IEC 62366-1:2015+A1:2020 |
| QA Reviewer | CAPA, complaints, management review, supplier evaluation | ISO 13485:2016, 21 CFR 820, ISO 19011:2018 |
| Safety Reviewer | Risk analysis, FMEA, usability, AI/ML output safety | ISO 14971:2019, IEC 62366-1:2015+A1:2020 |
| Cybersecurity Reviewer | Threat models, SBOMs, security architecture, Section 524B | FDA Premarket Cybersecurity Guidance (June 2025), AAMI TIR57:2016, IEC 81001-5-1:2021 |
| Clinical Reviewer | Clinical logic, alarm management, handoff quality | Published neonatal literature, AAP guidelines |

## Validation

- **20 test fixtures** with deliberately planted deficiencies (4 per agent) verify that agents detect known gaps
- **Automated eval script** scores blocker detection and verdict accuracy
- **Dry-run validation** confirms all fixtures are well-formed — see [most recent eval results](eval-results-2026-04-30.md) for current status
- **Fixture methodology**: each fixture documents expected findings and expected verdict; scoring compares agent output against these expectations

Validation evidence is maintained in `docs/eval-results-*.md` and `examples/test-fixtures/`. Refer to the most recent `eval-results-*.md` file for current validation status rather than relying on dates quoted in this document.

## Limitations

1. Agent knowledge reflects standards as of the SKILL.md authoring date — not real-time standards updates
2. Agents have no access to prior submission history, predicate device files, or eQMS records
3. AI-generated citations should be verified against source standards
4. Current validation covers deficiency detection only — false-positive rate on compliant artifacts has not been measured
5. Agent performance may vary with underlying model version changes

## Prepared Answers

**Q: "Do you use AI tools in your quality system?"**
> We use AI-assisted pre-screening to identify structural gaps in draft artifacts before formal human review. The tool is a working aid — it does not participate in document approval, does not generate controlled records, and does not replace qualified reviewer judgment. All artifacts in our eQMS have been reviewed and approved by qualified personnel through our standard document control process.

**Q: "How do you know the AI tool gives correct findings?"**
> We maintain a validation suite of 20 test fixtures with known deficiencies. We run these fixtures against the agents periodically and after any agent configuration change. Results are documented. Additionally, our RA/QA team spot-checks agent findings against their own independent assessment of the same artifacts.

**Q: "Is the AI tool itself a validated system?"**
> The tool is a pre-screening aid, not a validated system in the Part 11 / Annex 11 sense. It produces uncontrolled draft output that is always subject to human review before any quality decision is made. Our use of the tool is documented in [reference your applicable SOP or work instruction].

**Q: "What happens if the AI gives a wrong finding?"**
> The same thing that happens with any checklist or screening tool — the human reviewer catches it during formal review. Agent findings are inputs to the review process, not outputs of it. Our process does not permit document approval based on agent review alone.

**Q: "What if the AI flags a real issue and the reviewer dismisses it?"**
> The human reviewer's documented rationale for accepting or dismissing any finding — whether from an agent, a checklist, or a peer reviewer — becomes part of the review record in the eQMS, not in samd-os. If a reviewer dismisses an agent finding, the basis for that decision is captured in the formal review record in the same way any other review comment disposition is recorded per our document control procedures.

**Q: "You built the product before creating design controls. How do we know the documentation reflects the actual device?"**
> We conducted a documented retrospective gap analysis authorized under [reference CAPA/project plan]. The analysis used automated code analysis to identify software requirements, SOUP components, and safety-critical code regions, then produced a gap report identifying where design rationale, clinical evidence, and documented decisions were missing. Each gap was remediated by the responsible owner — rationale was documented through team interviews and clinical literature review, not auto-generated. The resulting design controls, SOUP register, and hazard analysis were then reviewed through our standard design review process, and the reviewer agents issued [X] blockers that were resolved before acceptance. The gap reports themselves are maintained as a series of point-in-time snapshots in our regulatory files, documenting both the initial gap state and the remediation progress.
