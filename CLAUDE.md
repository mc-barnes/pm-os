# PM OS — Claude Code Configuration

## Who This Is For
SaMD product managers using Claude Code who want regulatory-aware AI assistance. This file configures Claude Code with domain-specific skills, workflow routing, and safety boundaries for software medical device work.

## Skills Available

### SaMD Regulatory (`skills/samd-regulatory/`)
| Skill | Trigger | Output |
|-------|---------|--------|
| Design Controls | "design controls", "traceability matrix", "IEC 62304", "user needs" | XLSX traceability matrix |
| Risk Management | "risk management", "ISO 14971", "FMEA", "hazard analysis" | XLSX risk analysis |
| FHIR Builder | "FHIR resource", "FHIR bundle", "HL7v2 to FHIR" | JSON FHIR bundle |
| Change Impact | "change impact", "software change", "re-verification scope" | XLSX change impact report |
| Design Review | "design review", "PDR", "CDR", "FDR", "GO/NO-GO gate" | XLSX + narrative |

### SaMD PM (`skills/samd-pm/`)
| Skill | Trigger | Output |
|-------|---------|--------|
| PRD Writer (SaMD) | "write PRD", "product requirements" | Markdown PRD |
| Interview Prep | "interview prep", "STAR stories" | Structured prep doc |
| Networking Outreach | "networking", "outreach message" | Personalized outreach |

### Agent Personas (`skills/agents/`)
| Agent | Use Case |
|-------|----------|
| Clinical Reviewer | Neonatal SpO2 clinical logic review, alarm management, handoff quality |

## Workflow Router

### Triage
Assess task size before diving in:
- **Small** (1-2 files, <50 lines, no new APIs): Just do it → `/review-code` when done
- **Medium** (3-5 files, new logic or UI): `/spec` → `/plan` → `/build` → `/review-code`
- **Large** (new feature, multi-system, API changes): `/spec` → `/plan` → `/review-arch` → `/build` → `/review-code` → `/ship`

### Phase Prompts
After completing each phase, prompt the user with the next step:
- After `/spec` → "Spec is ready. Want me to `/plan` the tasks?"
- After `/plan` → "Tasks are broken down. Run `/review-arch` before building, or go straight to `/build`?"
- After `/build` → "Implementation complete. Running `/review-code`..."
- After `/review-code` → "Code review passed. Is this shipping? If so, run `/ship`?"

### Early-Stage Detection
Route vague requests to ideation:
- Vague idea, no clear direction → suggest `ideate`
- Multiple directions to explore → suggest `/concept-gen`
- Clear direction, needs UI → suggest `/rapid_prototype`
- Clear direction, needs spec → suggest `/spec`

## SaMD Context
Customize this section for your regulatory environment:

```
Device classification: [Class II / Class III]
Predicate device: [predicate or De Novo]
Standards: [IEC 62304, ISO 14971, ISO 13485, IEC 62366]
Clinical domain: [e.g., neonatal monitoring, cardiac, respiratory]
Submission type: [510(k) / De Novo / PMA]
Quality system: [e.g., ISO 13485 certified, FDA QSR]
```

## Boundaries

### Always
- Confirm approach BEFORE implementing — never start coding without explicit approval
- Check if a skill matches the task before starting work — suggest it first
- Check design controls impact for any clinical logic change
- Cite standards (IEC 62304, ISO 14971) when making regulatory claims
- Run `/review-code` after any non-trivial implementation
- Start with the simplest explanation first

### Never
- Skip risk analysis for safety-related changes
- Commit without review
- Push to main without approval
- Make assumptions about regulatory requirements — ask or check the standard
- Add features not explicitly requested

## How to Customize
1. Copy this repo to your machine
2. Copy skills you need to `~/.claude/skills/`
3. Replace `[placeholders]` in this file with your project details
4. Add your own skills to `skills/` as needed

See `skills/README.md` for detailed installation instructions.
