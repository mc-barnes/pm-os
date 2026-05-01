---
type: decision
status: draft
owner: "@mc-barnes"
last-reviewed: 2026-04-30
related:
  - team/specs/regulatory-reviewer-agent-v1.md
  - docs/auditor-briefing.md
  - docs/responsible-use.md
  - .claude/skills/design-controls/SKILL.md
  - .claude/skills/risk-management/SKILL.md
  - .claude/skills/change-impact/SKILL.md
  - .claude/skills/review-panel/SKILL.md
---
# SPEC: Gap Analysis Module

## Objective

Build a reverse-engineering module for samd-os that reconstructs draft regulatory artifacts from an existing codebase and produces a gap report documenting exactly where design rationale, clinical evidence, and documented decisions are missing.

**One-line positioning:** Reconstructs draft regulatory artifacts from an existing codebase and tells you exactly where the design rationale is missing.

### What It Produces

- **Draft artifacts** (XLSX) — the artifact shape, populated from code analysis, with empty fields where human input is required
- **Gap reports** (markdown) — a categorized list of missing information, sorted by who needs to address each gap, functioning as a workplan
- **Scope statement** (markdown) — front-door artifact authorizing and scoping the retrospective effort

### What It Does Not Produce

- A Design History File (DHF)
- A 510(k)-ready submission package
- Anything that passes the existing reviewer agents without further human work — the agents should issue blockers on raw gap-analysis output by design. That pressure is the feature, not a bug.
- Rationale, clinical justification, or evidence — those fields are left explicitly empty with GAP status. The module never auto-populates rationale, even when the code references a clinical paper or standards clause. It proposes candidate rationale and requires human acceptance.

### Target Users

- SaMD startups that built product first and now need regulatory documentation for a submission
- Established teams acquiring a codebase (M&A, open-source adoption) that needs regulatory characterization
- Teams preparing for a first FDA submission (510(k), De Novo) with an existing product
- RA consultants conducting regulatory gap assessments on client codebases

### Success Criteria

1. A team with an undocumented codebase can run the module and receive a concrete workplan for retrospective compliance within one session
2. Every gap report item identifies who needs to act (document owner, product owner, clinical team, RA)
3. The existing reviewer agents (regulatory, qa, safety, clinical, cybersecurity) issue BLOCKER findings on every raw gap-analysis output, forcing human review and completion before acceptance
4. The qa-reviewer refuses to evaluate gap-analysis output that lacks a scope statement with procedural authorization
5. code-to-soup-register output on a known dependency set matches expected SOUP register entries (verifiable, not debatable)
6. No gap report item contains auto-generated rationale

---

## Architecture

### Module Structure

```
.claude/skills/
├── gap-analysis/                    # Orchestrator — dispatches to sub-skills
│   ├── SKILL.md                     # dispatches: [code-to-soup-register, code-to-design-inputs, code-to-hazard-candidates]
│   └── references/
│       ├── retrospective-mode.md    # When and how to use, what it doesn't accomplish
│       └── gap-categories.md        # Taxonomy of gap types with routing rules
│
├── code-to-soup-register/           # Dependency manifest → IEC 62304 SOUP register
│   ├── SKILL.md
│   └── references/
│       └── soup-classification.md   # SOUP criteria, transitive dep handling, license flags
│
├── code-to-design-inputs/           # Source tree → design controls traceability draft
│   ├── SKILL.md
│   └── references/
│       └── traceability-from-code.md  # Inclusion heuristics, code-to-DI mapping rules
│
├── code-to-hazard-candidates/       # Safety-critical path analysis → candidate hazards
│   ├── SKILL.md
│   └── references/
│       └── hazard-from-code.md      # Default heuristics, domain config, coverage disclaimer spec
│
└── agents/
    └── (existing 5 agents, with retrospective-mode sections added)

docs/
└── gap-analysis-guide.md            # When to use, how to use, what it isn't — for PM Directors and QA Leads

regulatory/
└── gap-analysis/                    # Output destination
    ├── _SCOPE_TEMPLATE.md           # Scope statement template (front door)
    ├── _GAP_REPORT_TEMPLATE.md      # Gap report template
    └── (generated gap reports land here, date-stamped)
```

### Design Decisions

**Flat skill layout (not nested):** The three sub-skills are siblings under `.claude/skills/`, consistent with existing skills (design-controls, risk-management, change-impact). The dispatch relationship is documented via a `dispatches:` field in gap-analysis/SKILL.md frontmatter, following the same pattern as review-panel's agent dispatch.

**Output in `regulatory/gap-analysis/`:** Gap reports are regulatory artifacts — they document the state of compliance at a point in time. Placing them under `regulatory/` reinforces that they're regulatory output, not engineering analysis. Same control model as `regulatory/design-controls/` and `regulatory/risk-management/`.

**Immutable gap reports:** Each gap report is a point-in-time snapshot, never edited after generation. Progress is measured by generating new reports periodically and comparing. A document that gets edited over time to look better is a document that lies. A series of snapshots tells the truth about velocity, drift, and remaining work.

**File naming:** `gap-report-{skill}-{date}.md` (e.g., `gap-report-soup-2026-04-30.md`, `gap-report-design-inputs-2026-05-15.md`). The date comes from the `generated-on` frontmatter field, not the filesystem. This departs from the standard `{descriptor}-v{n}.md` convention because gap reports are temporal snapshots, not versioned documents — there is no "v2" of a snapshot.

---

## Scope Statement (Front Door)

Every gap analysis effort begins with a scope statement. This is a one-page artifact that authorizes and bounds the retrospective effort.

### Template: `regulatory/gap-analysis/_SCOPE_TEMPLATE.md`

```yaml
---
type: scope-statement
status: draft
owner: "@github-handle"
authorization: [path to CAPA, project plan, or management decision authorizing this effort]
generated-on: YYYY-MM-DD
---
```

```markdown
# Gap Analysis Scope Statement

## Authorization
- **Authorizing document:** [path to CAPA, project plan, or quality record]
- **Authorized by:** [name and role]
- **Date authorized:** [YYYY-MM-DD]

## Scope
- **Repository/repositories:** [path(s) to source tree(s) under analysis]
- **Languages detected:** [auto-populated by skills]
- **Excluded paths:** [test/, vendor/, docs/, etc. — explicitly listed]

## Device Context
- **Device name:** [product name]
- **Device classification:** [Class I / Class II / Class III]
- **Regulatory pathway:** [510(k) / De Novo / PMA]
- **Predicate device:** [predicate name and 510(k) number, or "De Novo — no predicate"]
- **Clinical domain:** [e.g., neonatal monitoring, cardiac rhythm classification, CGM]
- **IEC 62304 software safety class:** [A / B / C, or "to be determined"]

## Accountable Owners
- **Gap analysis lead:** [name — accountable for driving the effort]
- **Regulatory affairs:** [name — accountable for regulatory judgment calls]
- **Clinical SME:** [name — accountable for clinical rationale review]
- **QA lead:** [name — accountable for QMS integration]
- **Engineering lead:** [name — accountable for code-level accuracy]

## Skills to Run
- [ ] code-to-soup-register
- [ ] code-to-design-inputs
- [ ] code-to-hazard-candidates

## What This Effort Is Not
This gap analysis produces draft artifacts and a gap report identifying where
documentation is missing. It does not constitute a design control activity,
a hazard analysis, a SOUP evaluation, or any other regulated activity.
The outputs are inputs to a human-led retrospective compliance effort,
not substitutes for it.
```

### Gate Behavior

- **Skills:** Each reverse-engineering skill accepts an optional `--scope` parameter pointing to the scope statement. If omitted, the skill runs but logs a WARNING: `"No scope statement provided. Gap report will be flagged by qa-reviewer as lacking procedural authorization."`
- **qa-reviewer (retrospective mode):** Refuses to evaluate gap-analysis output unless a scope statement is referenced in the gap report frontmatter AND the scope statement contains a non-empty `authorization` field. This is a **gate**, not a finding — the agent returns `EVALUATION REFUSED: No procedural authorization` rather than producing findings on an unauthorized effort.
- **Rationale:** For the use case we're worried about (a stressed team generating a fake DHF the night before an audit), the gate is the only thing that actually works. A finding is too easy to ignore.

---

## The Three Reverse-Engineering Skills

### 1. code-to-soup-register

**Priority:** Build first. Most mechanical, cleanest output, easiest to validate.

**Input:**
- Path to repo root (required)
- Path to scope statement (optional, recommended)

**What it does:**

1. Detects dependency manifests across supported languages:
   - Python: `requirements.txt`, `Pipfile`, `Pipfile.lock`, `pyproject.toml`, `setup.py`, `setup.cfg`
   - JavaScript/TypeScript: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - Go: `go.mod`, `go.sum`
   - Java/Kotlin: `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`

2. Resolves the **full transitive dependency tree**, not just declared top-level dependencies. Per IEC 62304 §5.3.3, SOUP means "software of unknown provenance" — the standard does not distinguish between directly imported and transitively included software. A SOUP register that only lists declared dependencies is incomplete from a regulatory standpoint.
   - When a lock file exists (`package-lock.json`, `Pipfile.lock`, `go.sum`, etc.): use it for the resolved tree
   - When only a manifest exists without a lock file: flag as GAP — `"Lock file missing. Dependency versions are not pinned. Resolved tree cannot be determined."`
   - Clearly distinguish `declared` vs. `transitive` dependencies in the output

3. For each dependency, extracts: name, version, license, repository URL, last release date, declared vs. transitive status.

4. **License classification (WARNING tier):** Flags known problematic licenses for proprietary SaMD:
   - GPL (any version) — WARNING: copyleft, may require source disclosure
   - AGPL — WARNING: network copyleft, triggered by SaaS/cloud deployment
   - SSPL — WARNING: Server Side Public License, restrictive for service deployments
   - Unknown/missing license — WARNING: license cannot be determined

   The WARNING tier is visually distinct from the GAP tier in the output. WARNING means "license needs legal review." GAP means "required SOUP evaluation field is missing."

5. Classifies each dependency by IEC 62304 SOUP criteria and flags what's missing:
   - Fitness for intended use evaluation — GAP (always, requires human assessment)
   - Anomaly list reviewed — GAP (always, requires human review of known issues/CVEs)
   - Version controlled — auto-populated (present in lock file or not)
   - Integration requirements documented — GAP (always, requires human documentation)

**Output:** SOUP register XLSX + companion gap report markdown.

#### XLSX Columns (per IEC 62304 §5.3.3 / §8.1.2)

| Column | Auto-populated? | Notes |
|--------|----------------|-------|
| SOUP ID | Yes | SOUP-001, SOUP-002, ... |
| Component Name | Yes | Package name |
| Version | Yes | From lock file or manifest |
| Declared / Transitive | Yes | Relationship to project |
| License | Yes | Extracted from package metadata |
| License Flag | Yes | OK / WARNING (GPL/AGPL/SSPL/Unknown) |
| Repository URL | Yes | Package registry or source repo |
| Last Release Date | Yes | From package registry metadata |
| Fitness for Intended Use | No — GAP | Requires human evaluation |
| Known Anomalies Reviewed | No — GAP | Requires human review of CVE/issue tracker |
| Integration Requirements | No — GAP | Requires human documentation |
| Version Pinned | Yes | Lock file present and version resolved |
| Gap Status | Formula | COMPLETE / GAP / WARNING |

#### Gap Report Categories (SOUP-specific)

- **Evaluation required** — Fitness for intended use not assessed (every dependency)
- **Anomaly review required** — Known issues/CVEs not reviewed (every dependency)
- **License review required** — Problematic or unknown license detected
- **Lock file missing** — Dependency versions not pinned, transitive tree unresolvable
- **Integration documentation required** — SOUP integration requirements not documented

---

### 2. code-to-design-inputs

**Priority:** Build fourth, after SOUP register, documentation, and agent retrospective-mode.

**Input:**
- Path to source tree (required)
- Path to scope statement (optional, recommended)
- Path to existing PRD or intended use statement (optional, for cross-reference)

**What it does:**

1. Walks the source tree and identifies design-input-worthy boundaries using these inclusion heuristics:
   - **API boundaries:** Routes, exported functions, public interfaces
   - **Configuration surfaces:** Environment variables, feature flags, threshold constants
   - **Integration points:** External API calls, EHR writes, device interfaces, FHIR endpoints
   - **Clinical decision thresholds:** Alarm limits, dosing calculations, classification boundaries, scoring cutoffs
   - **Data retention/deletion logic:** Storage duration, purge policies, data lifecycle
   - **User-facing error messages:** Error text shown to clinicians or patients (information-for-safety under risk controls)

   The inclusion heuristic is documented in `references/traceability-from-code.md` so teams can review and calibrate it for their codebase.

2. Proposes design inputs grounded in actual code locations, with `file_path:line_number` citations.

3. Cross-checks against the PRD/intended use if provided, identifying two distinct gap types:
   - **Documentation gap:** Code exists but intent/PRD doesn't mention it — the behavior is implemented but undocumented
   - **Implementation gap:** Intent/PRD describes behavior that code doesn't implement — this is a product gap (deferred feature, scope reduction, or actual bug), not a documentation gap. Different owner, different remediation path, different urgency.

**Output:** XLSX traceability matrix draft + companion gap report markdown.

#### XLSX Columns

| Column | Auto-populated? | Notes |
|--------|----------------|-------|
| UN ID | Proposed | Proposed user need (if PRD provided) |
| DI ID | Yes | DI-001, DI-002, ... |
| Description | Yes | Design input derived from code analysis |
| Source (code) | Yes | file_path:line_number citation |
| Type | Yes | Functional / Performance / Safety / Interface |
| Rationale | No — GAP | Requires human input — why this behavior exists |
| Rationale Source | No — GAP | Document, paper, meeting minutes, etc. |
| SW Safety Class | No — GAP | A / B / C — requires risk analysis context |
| Gap Status | Formula | COMPLETE / GAP |

The Rationale and Rationale Source columns are the design-control-specific fields. They cannot be auto-filled from code. The skill explicitly leaves them empty when no document supports them, marks the row as GAP, and the gap report tallies these.

#### Priority Tiers (v2 — added after code-to-hazard-candidates ships)

Once code-to-hazard-candidates exists, design input gaps can be prioritized by safety criticality:
- **P1 (safety-critical):** Design inputs that touch code regions flagged as hazard candidates — rationale gaps here block submission
- **P2 (clinical):** Design inputs involving clinical decision logic — rationale gaps need clinical SME
- **P3 (functional):** Design inputs for non-safety functionality — rationale gaps can be addressed in sequence

Ship code-to-design-inputs without prioritization in phase 4. Add prioritization in phase 5 when hazard candidate output exists to inform it. Each phase produces a standalone useful artifact.

---

### 3. code-to-hazard-candidates

**Priority:** Build fifth (last). Most sensitive, requires the most caution, benefits from everything before it being battle-tested.

**Input:**
- Path to source tree (required)
- Path to scope statement (optional, recommended)
- Path to existing risk file or hazard list (optional, for cross-reference)
- Path to domain heuristic config (optional, for non-default clinical domains)

**What it does:**

1. Identifies safety-critical code regions using heuristic analysis. Default heuristics (tuned for the neonatal monitoring reference device):
   - Alarm logic (threshold comparison, escalation, suppression)
   - Threshold/dosing calculations (numeric boundaries with clinical significance)
   - Decision support outputs (classification results, triage recommendations, risk scores)
   - EHR write paths (data that enters the clinical record)
   - Physical device control (actuator commands, pump rates, ventilator settings)
   - Fail-safe paths (fallback behavior, degraded mode, safe state transitions)

   **Domain bias disclosure:** The default heuristics are tuned for the repo's neonatal monitoring reference device. Teams adopting this for a cardiac classifier, CGM, or other clinical domain should review the heuristics and provide a domain-specific override via the `--heuristics` parameter. The skill documents this bias in every generated report.

2. For each identified region, proposes candidate hazard scenarios based on common failure modes:
   - Incorrect threshold (value too high, too low, hardcoded vs. parameterized)
   - Missed alarm (condition met but alarm not triggered)
   - Delayed alarm (latency between condition and notification)
   - False alarm (alarm triggered without clinical condition)
   - Calculation overflow/underflow (numeric edge cases)
   - Integration failure (upstream data missing, malformed, or stale)
   - Dosing miscalculation (unit conversion errors, weight-based calculation errors)
   - Model inconsistency (ML output contradicts clinical context)

3. Cross-references against existing risk file if provided, flagging:
   - Hazards in code not covered by the risk file (new candidates)
   - Hazards in the risk file that don't map to identifiable code regions (potential dead controls or infrastructure-level hazards)

**Output:** Hazard candidate XLSX + companion gap report markdown + coverage disclaimer.

#### XLSX Columns

| Column | Auto-populated? | Notes |
|--------|----------------|-------|
| Candidate ID | Yes | HC-001, HC-002, ... |
| Code Region | Yes | file_path:line_range citation |
| Heuristic Matched | Yes | Which detection heuristic triggered |
| Proposed Hazard | Yes | Candidate hazard description |
| Proposed Failure Mode | Yes | How the code region could fail |
| Proposed Harm | Yes | Potential patient harm |
| Existing HAZ ID | Yes (if risk file provided) | Cross-reference to existing hazard analysis |
| Status | Always "CANDIDATE" | **CANDIDATE — requires human evaluation** |
| Dispositioning Decision | No — GAP | Accepted / Modified / Rejected with rationale |
| Clinical Rationale | No — GAP | Clinical judgment on severity and probability |

**Every output row carries `Status: CANDIDATE — requires human evaluation`.** The safety-reviewer agent treats CANDIDATE status as a blocker — it refuses to grade a risk file as ACCEPTABLE if any rows still carry CANDIDATE status.

#### Coverage Disclaimer

Every generated report includes a "Coverage" section:

```markdown
## Coverage

### Code paths analyzed
- [list of directories/files scanned]
- Heuristics applied: [list of active heuristics with version]

### Code paths excluded
- Test files (test/, tests/, __tests__/, *_test.go, *_test.py)
- Vendored dependencies (vendor/, node_modules/, .venv/)
- Build artifacts (dist/, build/, target/)
- Documentation (docs/, *.md)
- Infrastructure/deployment (Dockerfile, terraform/, k8s/, .github/)
- [any additional exclusions]

### What this means
This analysis covers application source code only. Hazards arising from
infrastructure, deployment configuration, network architecture, or
operational procedures are not detected by this skill. A complete hazard
analysis per ISO 14971:2019 requires consideration of all sources of harm,
not just application code.

False negatives are possible — the heuristic approach may miss hazardous
code paths that don't match the configured patterns. This candidate list
is an input to a human-led hazard analysis, not a substitute for one.
```

#### Hazard Framing Disclaimer (in every report)

> These are candidate hazards inferred from code structure. Hazard analysis requires clinical context, use environment understanding, and patient population awareness that this skill cannot provide. Treat output as input to a human-led hazard analysis session, not as a hazard analysis.

---

## Gap Report Format

The gap report is the artifact the module is centered on. Every reverse-engineering skill produces one.

### Template: `regulatory/gap-analysis/_GAP_REPORT_TEMPLATE.md`

```yaml
---
type: gap-report
status: draft
owner: "@github-handle"
generated-on: YYYY-MM-DD
generated-by: [code-to-soup-register | code-to-design-inputs | code-to-hazard-candidates]
scope-statement: regulatory/gap-analysis/scope-{effort-name}.md
source-tree: [path analyzed]
companion-artifact: [path to XLSX output]
authorization: [path from scope statement, or "none provided"]
---
```

```markdown
# Gap Report — [Skill Name] (Retrospective)

## Summary
- Items identified: [n]
- Complete: [n] ([%])
- Gaps: [n] ([%])
- Warnings: [n] (license/coverage issues, distinct from gaps)
- Source-code traceability: [n]/[n] ([%])

## Gaps by Category

### Rationale Required ([n])
Design inputs/controls where the code behavior is documented but the
rationale for that behavior is missing. Owner: document owner.
[List each item ID with code reference and what's needed]

### Intent Unclear ([n])
Items where the code behavior exists but the intent behind the behavior
cannot be reconstructed from code alone. Requires team interview or
product decision. Owner: clinical SME or product owner.
[List each item]

### Decision Required ([n])
Items where the code presents alternatives or parameterized values that
need an explicit documented choice — e.g., the alarm threshold is
configurable but no documented decision exists for the production value.
Owner: product owner.
[List each item]

### Evidence Required ([n])
Items that reference clinical or regulatory rationale but the referenced
source cannot be located in the repo or linked documents.
Owner: regulatory affairs.
[List each item]

### Documentation Gap ([n])
Code behavior that exists but is not mentioned in the PRD, intended use,
or any specification document. The feature works; it's just undocumented.
Owner: document owner / PM.
[List each item]

### Implementation Gap ([n])
Behavior described in the PRD or intended use that has no corresponding
code implementation. May be a deferred feature, scope reduction, or
actual bug. Requires product decision. Owner: product owner / engineering.
[List each item]

## Recommended Sequence
1. [Prioritized remediation steps, sorted by who acts]
2. [Specific workshop/meeting recommendations for "intent unclear" items]
3. [RA coordination needed for "evidence required" items]
4. [Product decisions needed for "implementation gap" items]

## What This Report Is Not
This report identifies gaps in the existing artifact set. It does not
constitute a design control activity, a hazard analysis, or any other
regulated activity. The reconstructed artifacts and this gap report
are inputs to a human-led retrospective compliance effort, not
substitutes for it.
```

### Gap Categories — Design Rationale

The categories sort missing information by **who needs to address it**. This turns the gap report into a workplan, not just a findings list.

| Category | Owner | Remediation |
|----------|-------|-------------|
| Rationale required | Document owner | Write the rationale for existing behavior |
| Intent unclear | Clinical SME / product owner | Workshop or interview to reconstruct intent |
| Decision required | Product owner | Make and document the decision |
| Evidence required | Regulatory affairs | Locate or generate the clinical/regulatory evidence |
| Documentation gap | PM / document owner | Add the undocumented behavior to specs |
| Implementation gap | Product owner / engineering | Decide: build, defer, or descope |

---

## Retrospective Mode on Existing Agents

The five existing reviewer agents receive a `retrospective-mode` flag — passed at invocation, defaults to `false` — that adjusts their evaluation logic.

### Flag Specification

- **Parameter:** `--retrospective-mode` (boolean, default false)
- **Propagation:** When invoked via review-panel, the flag propagates from the panel invocation to each dispatched agent.
- **Logging:** review-panel logs the flag's presence visibly in its summary output: `**Mode: Retrospective**` in the panel header. Silent propagation hides the framing from the audit trail; explicit logging surfaces it.

### Per-Agent Adjustments

#### regulatory-reviewer (retrospective-mode: true)
- Treats empty rationale fields as **BLOCKER** findings even if other fields are populated
- Refuses ACCEPTABLE verdict on any retrospective artifact with unaddressed gaps
- Checks that the companion gap report is referenced and that gap items map to specific artifact rows
- Addition to SKILL.md: ~10 lines under a new "## Retrospective Mode" section

#### qa-reviewer (retrospective-mode: true)
- **GATE (not finding):** Refuses to evaluate gap-analysis output unless:
  1. A scope statement is referenced in the gap report frontmatter
  2. The scope statement contains a non-empty `authorization` field
  3. The authorization references a real document (CAPA, project plan, management decision)
- If gate conditions are not met: returns `EVALUATION REFUSED: No procedural authorization for retrospective compliance effort. Create a scope statement using regulatory/gap-analysis/_SCOPE_TEMPLATE.md and reference an authorizing quality record.`
- When gate passes: checks that the retrospective effort was authorized, scoped, and conducted under a documented procedure
- Addition to SKILL.md: ~15 lines under "## Retrospective Mode"

#### safety-reviewer (retrospective-mode: true)
- Treats `Status: CANDIDATE` hazards as gaps requiring human evaluation
- Issues BLOCKER findings if any candidate hazards lack a documented dispositioning decision (accepted, modified, rejected with rationale)
- Refuses ACCEPTABLE verdict on any risk file that contains unresolved CANDIDATE rows
- Addition to SKILL.md: ~10 lines under "## Retrospective Mode"

#### cybersecurity-reviewer (retrospective-mode: true)
- Checks SBOM/SOUP register for completeness (same as prospective)
- Adds a finding category: **"Components in use without documented security evaluation"** — flags dependencies present in lock file but absent from SOUP register or without security assessment
- Addition to SKILL.md: ~8 lines under "## Retrospective Mode"

#### clinical-reviewer (retrospective-mode: true)
- Every clinical threshold or decision boundary must trace to a named clinical reference (published paper, clinical guideline, clinical advisory board minutes, or equivalent)
- Missing citation is **BLOCKER** in retrospective mode (vs. WARNING in prospective mode, where the team may still be documenting)
- Rationale: prospective work is in motion; retrospective work is supposed to be done. The asymmetry between modes reflects this.
- Addition to SKILL.md: ~10 lines under "## Retrospective Mode"

### review-panel Integration

When `--retrospective-mode` is passed to review-panel:

1. The flag propagates to every dispatched agent
2. The panel summary header includes: `**Mode: Retrospective**`
3. The panel adds a routing entry for gap-report artifact types:

| Artifact type | Default agents |
|---------------|---------------|
| `gap-report` | regulatory, qa, safety |
| `scope-statement` | qa |

---

## Type Registry Additions

Add to the root `CLAUDE.md` type reference table:

| Type | Folder | Scope |
|------|--------|-------|
| gap-report | regulatory/gap-analysis/ | Retrospective gap analysis reports — point-in-time compliance snapshots |
| scope-statement | regulatory/gap-analysis/ | Gap analysis scope and authorization documents |

---

## Documentation Layer

### docs/gap-analysis-guide.md

Written for PM Directors and QA Leads (same audiences as adoption-guide.md and responsible-use.md). Sections:

1. **What this module is** — regulatory gap analysis for teams that built first
2. **What it accomplishes vs. what it doesn't** — drafts + gap report, not compliance
3. **When to use it** — timing of regulatory engagement, type of catch-up, authorization requirements
4. **The honest auditor framing** — how to present retrospective compliance work to an auditor (you did the work out of order; you're doing the documentation now; here's what you found and here's how you're addressing it)
5. **Recommended sequence for a retrospective effort** — 3-6 month plan with milestones:
   - Month 1: Scope statement, SOUP register, initial gap report
   - Month 2: Design input reconstruction, rationale workshops
   - Month 3: Hazard candidate analysis, clinical rationale review
   - Month 4-5: Gap remediation, formal design reviews
   - Month 6: Submission readiness assessment
6. **Required QMS prep** — procedure or work instruction for retrospective design control activities (same integration model as adoption-guide.md §1)
7. **What the team commits to** — this is more expensive in human time than prospective compliance, even if cheaper in API cost. The gap report creates work; it doesn't eliminate it.
8. **Cost and time estimates** — API cost (~$2-5 per full module run) is trivial; human time for gap remediation is 3-6 months for a typical codebase

### Auditor Briefing Addendum

Add Q6 to `docs/auditor-briefing.md`:

**Q: "You built the product before creating design controls. How do we know the documentation reflects the actual device?"**
> We conducted a documented retrospective gap analysis authorized under [reference CAPA/project plan]. The analysis used automated code analysis to identify software requirements, SOUP components, and safety-critical code regions, then produced a gap report identifying where design rationale, clinical evidence, and documented decisions were missing. Each gap was remediated by the responsible owner — rationale was documented through team interviews and clinical literature review, not auto-generated. The resulting design controls, SOUP register, and hazard analysis were then reviewed through our standard design review process, and the reviewer agents issued [X] blockers that were resolved before acceptance. The gap reports themselves are maintained as a series of point-in-time snapshots in our regulatory files, documenting both the initial gap state and the remediation progress.

---

## Language Support

### v1
| Language | Manifest Files | Lock Files | Notes |
|----------|---------------|------------|-------|
| Python | requirements.txt, Pipfile, pyproject.toml, setup.py, setup.cfg | Pipfile.lock | pip freeze output accepted as manifest |
| JavaScript/TypeScript | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml | Monorepo workspace detection (lerna, nx, turborepo) |
| Go | go.mod | go.sum | Module-aware only (no GOPATH) |
| Java/Kotlin | pom.xml, build.gradle, build.gradle.kts | — | Maven Central / Gradle metadata for license extraction |

### v2 (documented as known gaps)
| Language | Why Deferred | Notes |
|----------|-------------|-------|
| C/C++ | Different build system model (CMake, Make, Bazel), vendor-specific tooling for embedded, header-only libraries complicate dependency detection | Common in embedded SaMD firmware |
| Swift/Objective-C | iOS companion apps use CocoaPods/SPM | Less common as primary SaMD |
| Rust | Very small installed base in shipping SaMD products today | Growing but not yet common |

### Multi-Repo Support

**v1:** Single-repo only. Each skill runs against one source tree.

**Documented workaround:** Run each skill separately on each repo, then manually cross-reference the gap reports. Acknowledge this in the guide so teams know the limitation upfront.

**v2:** Multi-repo orchestration — gap-analysis/SKILL.md accepts a list of repo paths and produces a unified gap report with per-repo sections.

---

## Orchestrator (gap-analysis/SKILL.md)

### Invocation

```bash
# Run a specific sub-skill
/gap-analysis soup --source ./src --scope regulatory/gap-analysis/scope-mydevice.md

# Run all three skills in sequence
/gap-analysis all --source ./src --scope regulatory/gap-analysis/scope-mydevice.md

# Summary-only mode (stats and category counts, no full item list)
/gap-analysis soup --source ./src --summary-only
```

### Orchestrator Behavior

1. Validates scope statement if provided (checks frontmatter fields populated)
2. Detects languages in source tree and warns if unsupported languages found
3. Dispatches to requested sub-skill(s)
4. Each sub-skill produces its XLSX + gap report independently
5. If `all` is requested, skills run in sequence: soup → design-inputs → hazard-candidates
6. Orchestrator produces no output of its own — it delegates

### SKILL.md Frontmatter

```yaml
---
name: gap-analysis
version: 1.0.0
description: >
  Retrospective regulatory gap analysis. Reconstructs draft regulatory
  artifacts from an existing codebase and produces gap reports documenting
  where design rationale is missing. Dispatches to sub-skills for specific
  artifact types. Triggers: "gap analysis", "retrospective compliance",
  "regulatory gap", "code to design controls", "SOUP from code",
  "hazard analysis from code", "built first".
dispatches:
  - code-to-soup-register
  - code-to-design-inputs
  - code-to-hazard-candidates
---
```

---

## Integration Points

### With Existing Skills

| Skill | Integration | Version |
|-------|------------|---------|
| design-controls | Gap-analysis XLSX uses compatible column schema so output can be imported into prospective design-controls XLSX after gaps are filled | v1 |
| risk-management | Hazard candidates use compatible ID scheme (HC-xxx maps to HAZ-xxx after human dispositioning) | v1 |
| change-impact | Consumes gap reports to scope re-verification needed as gaps are closed — each filled gap is a change to the design control record | v2 |
| review-panel | Routes gap-report and scope-statement types to appropriate agents; propagates retrospective-mode flag | v1 |

### With Existing Agents

All five agents gain retrospective-mode sections (specified above). The key integration is that **agents should issue blockers on raw gap-analysis output** — this is the design pressure that prevents teams from treating drafts as finished artifacts.

---

## Validation Strategy

### Approach

Follow the existing fixture methodology (20 test fixtures, 4 per agent) adapted for gap-analysis skills.

### Test Fixtures Per Skill

#### code-to-soup-register (4 fixtures)
1. **Repo with known dependencies** — 10 declared, 25 transitive, known licenses including one GPL — verify complete extraction and license flagging
2. **Repo with missing lock file** — only `requirements.txt`, no `Pipfile.lock` — verify GAP flagged for unpinned versions
3. **Multi-language repo** — Python + TypeScript — verify both manifests detected and merged
4. **Empty repo** — no dependency manifests — verify graceful handling with "no dependencies detected" report

#### code-to-design-inputs (4 fixtures)
1. **Repo with clear API boundaries** — REST routes, exported functions, env vars — verify design inputs proposed with code citations
2. **Repo with PRD** — known mismatches between code and PRD — verify both documentation gaps and implementation gaps detected
3. **Repo with clinical thresholds** — hardcoded alarm values — verify clinical decision thresholds flagged as design inputs with GAP on rationale
4. **Minimal repo** — single file, no clear boundaries — verify graceful handling

#### code-to-hazard-candidates (4 fixtures)
1. **Repo with alarm logic** — threshold comparison, escalation — verify candidate hazards proposed for alarm failure modes
2. **Repo with existing risk file** — known hazards already analyzed, plus new unanalyzed code — verify cross-reference and new candidates
3. **Repo with no safety-critical code** — pure CRUD app — verify report states no candidates found (not empty/broken)
4. **Repo with non-default clinical domain** — cardiac rhythm classifier — verify default heuristics acknowledge domain mismatch

### Validation Sequence

1. Create fixtures (small synthetic repos, not real codebases)
2. Run skills against fixtures, compare output to expected results
3. Run reviewer agents in retrospective mode against skill output, verify blockers issued
4. Verify qa-reviewer gate on missing scope statement
5. Document results in `docs/eval-results-gap-analysis-{date}.md`

---

## Build Sequence

### Phase 1: Documentation Layer
- `docs/gap-analysis-guide.md`
- Auditor briefing Q6 addendum
- `regulatory/gap-analysis/_SCOPE_TEMPLATE.md`
- `regulatory/gap-analysis/_GAP_REPORT_TEMPLATE.md`
- `references/gap-categories.md`
- Type registry updates in root `CLAUDE.md`

**Rationale:** Writing the guide before building the skills means the skills implement what the guide commits to. Writing it after means the guide describes what got built. The constraint discipline runs the right direction.

**Exit criteria:** Guide reviewed by target audience (PM Director, QA Lead persona). Templates complete and internally consistent.

### Phase 2: code-to-soup-register
- `code-to-soup-register/SKILL.md`
- `code-to-soup-register/references/soup-classification.md`
- Test fixtures (4)
- Validation run

**Rationale:** Most mechanical, cleanest output, easiest to validate. Gets the module shape right before the harder skills. The output is verifiable — a SOUP register is wrong or it isn't.

**Exit criteria:** Skill produces correct SOUP register on test fixtures. Gap report format matches template. Transitive dependencies resolved from lock files.

### Phase 3: Retrospective-mode Flag on Existing Agents
- Add "## Retrospective Mode" section to all 5 agent SKILL.md files
- Add qa-reviewer gate logic
- Add review-panel retrospective-mode propagation and logging
- Add routing entries for gap-report and scope-statement types
- Test: run agents in retrospective mode on SOUP register output, verify blockers

**Rationale:** Small change, parallel across five agents. Validates that the framing pressure works as designed before building the harder skills.

**Exit criteria:** qa-reviewer refuses evaluation without scope statement. All agents issue appropriate blockers on raw gap-analysis output. review-panel logs retrospective mode visibly.

### Phase 4: code-to-design-inputs
- `code-to-design-inputs/SKILL.md`
- `code-to-design-inputs/references/traceability-from-code.md`
- Test fixtures (4)
- Validation run

**Ships without priority tiers.** Basic gap report with all categories. Prioritization added in Phase 5.

**Exit criteria:** Skill identifies design inputs from code with file:line citations. Documentation gaps and implementation gaps correctly distinguished. Rationale fields left empty with GAP status.

### Phase 5: code-to-hazard-candidates
- `code-to-hazard-candidates/SKILL.md`
- `code-to-hazard-candidates/references/hazard-from-code.md`
- Test fixtures (4)
- Validation run
- **Add priority tiers to code-to-design-inputs** (now that hazard data exists to inform prioritization)

**Exit criteria:** Skill proposes candidate hazards with CANDIDATE status. Coverage disclaimer present. safety-reviewer blocks on unresolved candidates. Domain bias documented. Priority tiers added to design-inputs gap reports.

### Phase 6: Orchestrator + Integration
- `gap-analysis/SKILL.md` (orchestrator)
- `gap-analysis/references/retrospective-mode.md`
- End-to-end test: full module run on a synthetic codebase
- Final documentation review

**Exit criteria:** `/gap-analysis all` runs all three skills in sequence. Scope statement flows through. Gap reports reference each other where appropriate.

### Timeline Estimate

6-12 weeks for all six phases. The retrospective use case is real and the audience is large, but rushing it means shipping the version of this tool that helps startups game compliance. Slower and more deliberate produces the version that helps them catch up honestly.

---

## Boundaries

### Always
- Leave rationale fields empty when no document supports them — never auto-populate
- Include the "What This Report Is Not" disclaimer in every generated report
- Cite file_path:line_number for every code-derived finding
- Mark hazard candidates as CANDIDATE requiring human evaluation
- Include coverage disclaimer listing analyzed and excluded code paths
- Reference the scope statement in every gap report frontmatter
- Log warnings when scope statement is missing (don't silently proceed)
- Cite standards with edition when making regulatory claims (IEC 62304:2006+A1:2015, not just "IEC 62304")

### Ask First
- Whether to use domain-specific hazard heuristics vs. defaults
- Whether to include transitive dependencies or top-level only (recommend: always transitive)
- Whether to run summary-only or full gap report
- Which sub-skills to run (or all three)

### Never
- Auto-generate rationale, clinical justification, or dispositioning decisions
- Present gap-analysis output as a completed regulatory artifact
- Allow CANDIDATE-status hazards to pass safety review
- Evaluate retrospective artifacts without procedural authorization (qa-reviewer gate)
- Claim the gap report constitutes a design control activity, hazard analysis, or SOUP evaluation
- Mix code quality findings with regulatory gap findings — these are different concerns with different owners
- Use gap-analysis skills for ongoing prospective work — once caught up, teams adopt prospective design controls and use the existing skills

---

## What This Module Is Explicitly Not

1. **Not a code-quality reviewer.** The skills extract regulatory-relevant structure; they don't comment on code quality, test coverage, or architectural soundness. Those are engineering reviews (use review-code), not regulatory ones.

2. **Not a verification activity.** Reading code to identify what it does is not verifying that it does what it should. V&V requires test execution, not code reading.

3. **Not a substitute for prospective skills.** Teams shouldn't use gap-analysis going forward. Once caught up, adopt prospective design controls and use the existing skills. The gap-analysis module is for the catch-up period only.

4. **Not a clinical evaluation tool.** It can extract clinical decision points from code but cannot evaluate whether those decisions are clinically appropriate. That's the clinical-reviewer agent's job, with proper clinical context.

5. **Not a validated system.** Same framing as the existing agents (see responsible-use.md): the module is a pre-screening aid, not a validated system in the Part 11 / Annex 11 sense.

---

## Open Questions Resolved

| Question | Decision | Rationale |
|----------|----------|-----------|
| Should the module require a stated trigger? | Optional scope statement, WARNING when absent, qa-reviewer gate on evaluation | Separates "let me see what we're dealing with" from "we're using this for our DHF" |
| What languages in v1? | Python, JS/TS, Go, Java/Kotlin | Covers most modern SaMD. C/C++ deferred (different build model). Rust deferred (small installed base). |
| Monorepo handling? | v1 = single-repo, v2 = multi-repo | Document the per-repo workaround |
| Output size at scale? | Priority tiers (v2), summary-only mode, gap categories as workplan | Categories sort by owner; tiers sort by urgency |
| Who validates the module? | Fixture approach, 4 per skill, separate from agent fixtures | Validation surface specified upfront |
| Auto-populate rationale? | No. Never. Even candidate rationale requires human acceptance. | The empty field with GAP status is the feature. |
| Gap report mutable or immutable? | Immutable snapshots, date-stamped, series for progress tracking | A document that gets edited to look better is a document that lies. |
| Retrospective-mode authorization: finding or gate? | Gate. qa-reviewer refuses evaluation, not just issues finding. | A finding is too easy to ignore. The gate prevents unauthorized retro efforts. |
| Priority tiers build order? | Ship design-inputs without tiers (phase 4), add tiers after hazard skill (phase 5) | Each phase produces a standalone useful artifact. |

---

## Dependencies

- Existing skill infrastructure (SKILL.md pattern, references/ convention)
- Existing 5 reviewer agents (for retrospective-mode additions)
- review-panel orchestration (for flag propagation)
- openpyxl (Python, for XLSX generation — same dependency as existing skills)
- No new external dependencies beyond what existing skills use

---

## Future Considerations (Not in Scope)

- **change-impact integration (v2):** Each filled gap is a change to the design control record. change-impact should consume gap reports to scope re-verification.
- **Community-contributable heuristic library (v3):** Domain-specific hazard detection patterns shared across teams and clinical domains.
- **Multi-repo orchestration (v2):** Unified gap report across mobile app + backend + firmware repos.
- **EU MDR support:** Extend agent retrospective-mode sections with MDR-specific requirements.
- **CI integration:** Automated gap report generation on PR merge to track compliance drift.
- **Compliant (green-path) fixtures:** Measure false-positive rate on well-documented codebases.
