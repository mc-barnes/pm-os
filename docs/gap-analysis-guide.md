---
type: onboarding
status: draft
owner: "@mc-barnes"
last-reviewed: 2026-04-30
related:
  - docs/adoption-guide.md
  - docs/responsible-use.md
  - docs/auditor-briefing.md
  - regulatory/gap-analysis/_SCOPE_TEMPLATE.md
  - regulatory/gap-analysis/_GAP_REPORT_TEMPLATE.md
  - team/specs/gap-analysis-design-v1.md
---
# Gap Analysis Guide

For PM Directors and QA Leads evaluating retrospective regulatory gap analysis — the path from "we built first" to a documented, reviewable artifact set.

## 1. What This Module Is

The gap-analysis module reconstructs draft regulatory artifacts from an existing codebase and produces a gap report documenting exactly where design rationale, clinical evidence, and documented decisions are missing.

It consists of three reverse-engineering skills:

| Skill | What it produces |
|-------|-----------------|
| `code-to-soup-register` | SOUP register XLSX from dependency manifests + gap report |
| `code-to-design-inputs` | Design input traceability matrix XLSX from source analysis + gap report |
| `code-to-hazard-candidates` | Hazard candidate XLSX from safety-critical code regions + gap report |

Each skill produces two outputs: a draft artifact (XLSX) populated from code analysis, and a companion gap report (markdown) categorizing what's missing and who needs to address it.

## 2. What It Accomplishes vs. What It Doesn't

**It accomplishes:**
- Automated extraction of dependency trees, software requirements, and safety-critical code regions
- Point-in-time gap reports that serve as remediation workplans, sorted by accountable owner
- Draft artifact scaffolds that match the existing design-controls and risk-management XLSX schemas
- Honest assessment of what's documented and what isn't

**It does not accomplish:**
- A Design History File (DHF)
- A 510(k)-ready submission package
- Anything that passes the existing reviewer agents without further human work

The reviewer agents issue blockers on raw gap-analysis output by design. That pressure is the feature, not a bug. A gap report that looks clean without human remediation is a gap report that's lying.

## 3. When to Use It

**Target audience:** SaMD teams approaching their first regulatory submission with an existing, undocumented codebase. The software works; the documentation doesn't exist yet.

**Timing signals:**
- You have working software but no design controls, SOUP register, or formal risk analysis
- A regulatory consultant or RA hire has told you "we need to document what you built"
- You're 6-12 months from a planned 510(k) or De Novo submission
- A CAPA or management decision has authorized retrospective documentation work

**When NOT to use it:**
- Greenfield projects — use the prospective skills (design-controls, risk-management) from the start
- Projects with existing design control documentation — use change-impact instead
- Quick prototypes or research code not intended for regulatory submission

## 4. Quick Start

Run `code-to-soup-register` right now, no setup required:

```bash
# Generate a SOUP register from your codebase
python .claude/skills/code-to-soup-register/scripts/generate_soup_register.py \
  --source /path/to/your/repo --example

# Output: SOUP register XLSX + companion gap report
```

This gives you an immediate, concrete artifact — a complete dependency inventory with license flags and gap markers. No scope statement needed to explore; formalize when you're ready to commit to the effort.

When you're ready to formalize:
1. Copy `regulatory/gap-analysis/_SCOPE_TEMPLATE.md` and fill in your device context
2. Get the scope statement authorized (reference a CAPA, project plan, or management decision)
3. Run skills with `--scope` pointing to your scope statement
4. Run `review-panel --retrospective-mode` on the output

## 5. The Honest Auditor Framing

Retrospective compliance is not a scandal — it's a common path, especially for digital health startups. The auditor question isn't "why didn't you do this prospectively?" It's "how do you know the documentation reflects the actual device?"

The honest answer:

> We built the software first. We then conducted a documented retrospective gap analysis, authorized under [CAPA/project plan]. We used automated code analysis to identify what exists, produced gap reports showing what documentation was missing, and remediated each gap with the responsible owner. Rationale was documented through team interviews and clinical literature review, not auto-generated. The resulting artifacts went through our standard design review process.

This framing works because it's true. The gap reports themselves — maintained as a series of point-in-time snapshots — document both the initial gap state and the remediation progress. An auditor can trace the journey from "undocumented" to "documented and reviewed."

See [Auditor Briefing Q6](auditor-briefing.md) for the scripted answer.

## 6. Recommended Sequence

A typical retrospective effort takes 3-6 months, depending on codebase size and team availability.

| Month | Activities | Key outputs |
|-------|-----------|-------------|
| **1** | Create scope statement. Run code-to-soup-register. Review initial gap report with RA. | Authorized scope statement, SOUP register draft, first gap report |
| **2** | Run code-to-design-inputs. Conduct rationale workshops with engineering. Begin SOUP evaluation (fitness, anomaly review). | Design input matrix draft, workshop notes, SOUP evaluations in progress |
| **3** | Run code-to-hazard-candidates. Clinical rationale review with SME. Cross-reference with existing risk analysis if any. | Hazard candidate list, clinical rationale documentation |
| **4-5** | Gap remediation: fill rationale fields, document decisions, locate clinical evidence. Re-run skills to measure progress. | Updated artifacts with gaps filled, delta gap reports showing progress |
| **6** | Formal design reviews on completed artifacts. Submission readiness assessment. | Design review records, review-panel results with blockers resolved |

**Milestones to track:**
- Scope statement authorized (week 1)
- SOUP register at 0 GAP rows (month 2-3)
- Design inputs with rationale filled >80% (month 4)
- All CANDIDATE hazards dispositioned (month 5)
- Review panel passes with no BLOCKERs (month 6)

## 7. Required QMS Prep

Your quality system needs a procedure or work instruction covering retrospective design control activities. Options:

- **Add a section to your Design Control SOP** describing retrospective gap analysis as a documented activity with authorization requirements, accountable owners, and review gates
- **Create a new work instruction:** "Retrospective Design Control Gap Analysis" — scope, authorization requirements (CAPA or management decision), tool usage, human accountability, review process

The scope statement template (`regulatory/gap-analysis/_SCOPE_TEMPLATE.md`) provides the content structure. Your QMS team wraps it in your SOP template.

**The qa-reviewer agent enforces this:** in retrospective mode, it refuses to evaluate gap-analysis output unless a scope statement with procedural authorization is referenced. This gate exists because the use case we're most concerned about — generating fake documentation the night before an audit — requires the absence of process. The gate makes that absence visible.

## 8. What the Team Commits To

The gap-analysis module creates work. It does not eliminate it.

**API cost:** ~$2-5 per full module run (all 3 skills + review panel). Trivial.

**Human time:** 3-6 months of part-time effort across PM, RA, QA, clinical, and engineering. This is the real cost. Retrospective compliance is more expensive in human time than prospective compliance — you're reconstructing intent that should have been documented when decisions were made.

**What each role owns:**

| Role | Responsibility |
|------|---------------|
| **PM / Product** | Fill rationale fields, document product decisions, resolve implementation gaps |
| **Engineering** | Verify code citations are accurate, complete SOUP evaluations, support rationale workshops |
| **Regulatory Affairs** | Locate clinical/regulatory evidence, validate against standards, lead design reviews |
| **Clinical SME** | Provide clinical rationale for thresholds and decision logic, review hazard candidates |
| **QA Lead** | Authorize the effort, integrate into QMS, verify review gates are met |

The gap report is a workplan. The team does the work.

## What This Guide Does Not Cover

- **Multi-repo support:** v1 analyzes one repo at a time. For multi-repo products, run skills separately on each repo and manually cross-reference gap reports.
- **EU MDR / IVDR specifics:** Agent baselines are FDA-focused. EU teams will need to add notified body expectations to agent SKILLs.
- **eQMS integration:** Gap-analysis output is uncontrolled draft material. Upload to your eQMS after human review and approval, same as any other samd-os artifact.
- **C/C++, Swift, Rust support:** v1 supports Python, JavaScript/TypeScript, Go, and Java/Kotlin. Embedded firmware languages are documented as known gaps for v2.
