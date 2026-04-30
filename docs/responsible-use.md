---
type: onboarding
status: draft
owner: "@mc-barnes"
last-reviewed: 2026-04-30
related:
  - docs/adoption-guide.md
  - docs/auditor-briefing.md
  - examples/test-fixtures/README.md
---
# Responsible Use & Validation Approach

## What the Agents Are

SaMD Team OS includes five AI reviewer agents that pre-screen regulated artifacts against standards requirements. Each agent operates from a defined regulatory or clinical persona and produces structured findings with standards citations.

**They are a draft-layer review tool.** Agents read an artifact, compare it against internalized standards knowledge, and produce findings. Findings are uncontrolled output — not regulatory sign-off, not audit evidence, not a substitute for qualified human review.

## What the Agents Are Not

| The agents do NOT | Why this matters |
|-------------------|-----------------|
| Replace Regulatory Affairs review | Agents lack institutional context, submission history, and predicate-specific knowledge that RA professionals bring |
| Constitute design review records | Agent output has no electronic signatures, no approval workflow, no Part 11 / Annex 11 compliance |
| Provide legal or regulatory advice | Standards interpretation in edge cases requires professional judgment; agents apply general rules |
| Guarantee audit readiness | An agent PASS verdict means the artifact appears structurally complete — not that it is substantively correct |
| Access your eQMS | Agents operate on local files only; they have no connection to Greenlight Guru, MasterControl, Qualio, or any controlled system |

## Intended Use Within a QMS

Agents fit into an existing quality system as a **pre-review screening layer**:

```
Draft artifact → Agent review (screening) → Human expert review → eQMS (controlled record)
```

- **Before human review**: Run the relevant agent(s) to catch structural gaps, missing citations, and standards misalignment before consuming reviewer time
- **After revision**: Re-run to verify that flagged findings have been addressed
- **Not during**: Agents do not participate in formal design reviews, CAPA investigations, or management reviews as a reviewer of record

## Known Limitations

1. **Standards knowledge is frozen at authoring time.** Agents internalize standards content from their SKILL.md files. When standards update (e.g., IEC 62304 Edition 2), the agent SKILL.md must be manually updated and re-validated.

2. **No institutional memory.** Agents don't know your submission history, your predicate device, your notified body preferences, or your prior audit findings. They apply general requirements, not organization-specific interpretations.

3. **Citation accuracy is bounded by training data.** Agents are instructed to cite specific clauses and to flag uncertainty rather than fabricate references. However, AI-generated citations should always be verified against the source standard.

4. **Keyword-based eval scoring has limits.** The eval harness uses keyword matching to score blocker detection. Agents may detect a deficiency using different terminology than the fixture expects, producing false fails in scoring. Conversely, a keyword match doesn't guarantee the agent understood the deficiency correctly.

5. **No false-positive baseline.** Current test fixtures contain only deliberately broken artifacts. There are no compliant (green-path) fixtures to measure false-positive rate. An agent that flags everything would score perfectly on current fixtures.

6. **Single-model dependency.** Agent performance may vary across model versions. A model update could change detection sensitivity, citation accuracy, or verdict calibration without any SKILL.md change.

## Human Accountability

- **Every agent output includes a disclaimer** stating findings must be validated by qualified professionals
- **The regulatory-reviewer includes a jurisdiction statement** (FDA scope only)
- **Panel verdicts use most-conservative-wins logic** — an INCOMPLETE or FAIL from any agent blocks a panel PASS
- **Agents (reviewer personas) never generate artifacts** — they only review artifacts produced by skills, by humans, or any combination. Skills generate; agents review.
- **Final accountability for artifact quality rests with the document owner**, not the agent

## Validation Approach

### What Exists Today

| Layer | What it validates | Status |
|-------|-------------------|--------|
| **Fixture format validation** (dry-run) | YAML frontmatter, expected findings structure, verdict terminology | 20/20 PASS ([eval results](eval-results-2026-04-30.md)) |
| **20 deliberately broken fixtures** | Known deficiencies across 5 agents (4 per agent) | Authored and format-validated |
| **Eval script** (`scripts/eval-agents.sh`) | Automated blocker detection scoring with keyword matching | Implemented, dry-run validated |

### What Should Exist Before Broader Adoption

| Layer | Purpose | Status |
|-------|---------|--------|
| **Live eval results** | Scored agent detection against fixtures — do agents actually catch planted defects? | Not yet committed |
| **Compliant fixtures** | Green-path artifacts to measure false-positive rate | Not yet created |
| **Credentialed spot-check** | RA/QA professional reviews a sample of agent findings for accuracy and calibration | Not yet performed |
| **Re-eval cadence** | Documented process for re-running fixtures after SKILL.md changes or model updates | Defined in fixtures README, not yet formalized as SOP |

### Recommended Validation Steps for Adopting Teams

1. **Run the dry-run** (`./scripts/eval-agents.sh --dry-run all`) to confirm fixture integrity in your fork
2. **Run a live eval** on 2-3 fixtures per agent to establish baseline detection in your environment
3. **Have your RA/QA lead review** 3-5 agent outputs against her own assessment of the same artifact — document agreement/disagreement
4. **Decide on re-eval triggers**: at minimum, re-run after any SKILL.md edit or model version change
5. **Document your decision** to use the tool in a quality record (see [Adoption Guide](adoption-guide.md) for QMS integration steps)

## When to Stop Trusting Agent Output

Agent findings should be treated with increased skepticism when:

- The agent produces findings that cite standards clauses you cannot locate in the source document
- The agent gives a PASS verdict on an artifact you know to be deficient
- A model version change has occurred since the last eval run
- The artifact type is not in the agent's documented scope (e.g., asking the QA reviewer to assess a threat model)
- Findings are generic ("consider adding more detail") rather than specific with standards references
