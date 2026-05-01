---
name: review-panel
version: 1.0.0
description: >
  Orchestration skill that dispatches a SaMD artifact to multiple reviewer
  agents in parallel and merges findings into a single review package.
  Auto-routes by artifact `type:` frontmatter; user can override with an
  explicit agent list. Panel verdict uses most-conservative-wins rule.
  Triggers: "review panel", "panel review", "multi-agent review",
  "run all reviewers", "full review", "cross-functional review".
---

# Review Panel — Multi-Agent Orchestration

Dispatch a SaMD artifact to selected reviewer agents in parallel, then merge findings into a single review package with cross-agent conflict detection.

## When to Use

- Running a cross-functional review before a design review gate (PDR/CDR/FDR)
- Reviewing a submission package across all regulatory dimensions
- Any artifact that touches multiple domains (risk + regulatory + clinical)
- When you want a single merged output instead of running agents one at a time
- Pre-submission readiness checks

## When NOT to Use

- Quick single-dimension review (just invoke the specific agent directly)
- Non-SaMD artifacts with no regulatory relevance
- Exploratory drafts not yet ready for formal review

## Invocation

```
/review-panel <artifact-path> [--agents <agent1,agent2,...>]
```

**Examples:**
```bash
# Auto-route by frontmatter type
/review-panel regulatory/design-controls/traceability-v2.md

# Override with explicit agent list
/review-panel product/prds/alarm-management-v3.md --agents regulatory,safety,clinical

# Full panel (all 5 agents)
/review-panel regulatory/submissions/510k-draft-v1.md --agents all
```

## Routing Table

Artifacts are routed by the `type:` field in YAML frontmatter. If no `type:` is present or the type is not recognized, all 5 agents are dispatched.

| Artifact type | Default agents |
|---------------|---------------|
| `prd` | regulatory, clinical, safety |
| `risk-record` | safety, regulatory, cybersecurity |
| `design-controls` | regulatory, safety |
| `dhf-index` | regulatory, qa |
| `intended-use` | regulatory, clinical, safety |
| `usability` | safety, clinical |
| `cer` | clinical, regulatory |
| `submission` | all 5 |
| `capa` | qa |
| `complaint` | qa, regulatory |
| `change-request` | regulatory, safety, cybersecurity |
| `soup-register` | regulatory, cybersecurity |
| `rfc` | regulatory, cybersecurity |
| `audit` | qa |
| `sdlc-phase` | regulatory |
| `bug-report` | regulatory, safety |
| `decision` | regulatory |
| `retro` | qa |
| `onboarding` | qa |
| `competitive` | regulatory |
| `strategy` | regulatory, clinical |
| `call-notes` | clinical |
| `data-schema` | regulatory, cybersecurity |
| `gap-report` | regulatory, qa, safety |
| `scope-statement` | qa |
| (unknown / missing) | all 5 |

### Agent Reference

| Short name | Skill path | Domain |
|------------|-----------|--------|
| `regulatory` | `.claude/skills/agents/regulatory-reviewer/SKILL.md` | FDA regulatory affairs, submission readiness |
| `clinical` | `.claude/skills/agents/clinical-reviewer/SKILL.md` | Clinical domain expertise, clinical logic |
| `safety` | `.claude/skills/agents/safety-reviewer/SKILL.md` | ISO 14971 risk, IEC 62366-1 usability, human factors |
| `qa` | `.claude/skills/agents/qa-reviewer/SKILL.md` | ISO 13485 QMS, CAPA, complaints, audit |
| `cybersecurity` | `.claude/skills/agents/cybersecurity-reviewer/SKILL.md` | Threat modeling, SBOM, Section 524B |

## Execution Model

### 1. Parse & Route

1. Read the target artifact.
2. Extract `type:` from YAML frontmatter.
3. Look up default agents from the routing table.
4. If `--agents` flag provided, override with the explicit list.
5. If `--agents all`, dispatch to all 5 agents.

### 2. Parallel Dispatch

Launch all selected agents concurrently using the Agent tool. Each agent receives:
- The full artifact content
- Its own SKILL.md persona and instructions
- A prompt: "Review the following artifact. Return your findings in your standard output format."

All agents run in parallel. Do not wait for one agent to complete before launching the next.

### 3. Collect & Merge

Wait for all agents to complete. If any agent fails or times out:
- Include a `[AGENT FAILED]` marker in that agent's section.
- Set panel verdict to `INCOMPLETE`.

### 4. Conflict Detection

After collecting all results, scan for cross-agent conflicts:
- Two agents flag the same section/requirement/hazard ID with different severities.
- Two agents make contradictory recommendations about the same element.

Mark conflicts with a `CROSS-AGENT CONFLICT` block:

```
### CROSS-AGENT CONFLICT
- **Area:** [section or ID both agents reference]
- **safety-reviewer:** [their finding and severity]
- **regulatory-reviewer:** [their finding and severity]
- **Resolution guidance:** [which agent's domain owns this concern]
```

Use scope boundaries to guide resolution: safety-reviewer owns ISO 14971 clinical adequacy judgments; regulatory-reviewer owns submission structure and regulatory pathway; cybersecurity-reviewer owns security risk; qa-reviewer owns QMS process compliance; clinical-reviewer owns clinical domain correctness.

## Output Format

The merged review is a single markdown document with this structure:

```markdown
# Review Panel Report

**Artifact:** [path]
**Type:** [frontmatter type]
**Date:** [YYYY-MM-DD]
**Agents:** [list of agents that ran]
**Panel Verdict:** [PASS | CONDITIONAL | FAIL | INCOMPLETE]

## Summary Table

| Agent | Verdict | Critical | Major | Minor | Info |
|-------|---------|----------|-------|-------|------|
| regulatory-reviewer | PASS | 0 | 1 | 3 | 2 |
| safety-reviewer | CONDITIONAL | 0 | 2 | 1 | 0 |
| clinical-reviewer | PASS | 0 | 0 | 2 | 1 |

## Cross-Agent Conflicts

[Conflict blocks, if any. "None detected." if clean.]

---

## regulatory-reviewer

[Full output from regulatory-reviewer, unmodified]

---

## safety-reviewer

[Full output from safety-reviewer, unmodified]

---

## clinical-reviewer

[Full output from clinical-reviewer, unmodified]
```

### Verdict Rules

The panel verdict is the most conservative individual verdict:

| Priority | Verdict | Meaning |
|----------|---------|---------|
| 1 (highest) | `INCOMPLETE` | At least one agent failed to return results |
| 2 | `FAIL` | At least one agent returned FAIL / REJECT |
| 3 | `CONDITIONAL` | At least one agent returned CONDITIONAL / CONDITIONAL PASS |
| 4 (lowest) | `PASS` | All agents returned PASS / APPROVE |

**Verdict normalization:** Each agent uses its own severity vocabulary. Normalize to the panel scale:

| Agent term | Panel verdict |
|------------|--------------|
| PASS, APPROVE, ADEQUATE | PASS |
| CONDITIONAL, CONDITIONAL PASS, NEEDS WORK | CONDITIONAL |
| FAIL, REJECT, INADEQUATE, NOT READY | FAIL |

### Severity Normalization

Agents use different severity terms. The summary table normalizes to four levels:

| Panel level | regulatory-reviewer | clinical-reviewer | safety-reviewer | qa-reviewer | cybersecurity-reviewer |
|-------------|--------------------|--------------------|-----------------|-------------|----------------------|
| Critical | CRITICAL | SAFETY FINDING (Critical) | SAFETY FINDING | CRITICAL | SECURITY FINDING (Critical) |
| Major | MAJOR | SAFETY FINDING (Major) | FINDING (Major) | MAJOR | SECURITY FINDING (Major) |
| Minor | MINOR | FINDING | FINDING (Minor) | MINOR | FINDING |
| Info | INFO | NOTE | OBSERVATION | OBSERVATION | NOTE |

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Agent times out | Mark section `[AGENT TIMED OUT]`, verdict = INCOMPLETE |
| Agent returns malformed output | Include raw output, mark `[UNEXPECTED FORMAT]`, verdict = INCOMPLETE |
| No frontmatter `type:` found | Dispatch all 5 agents, log warning |
| Artifact file not found | Abort with error message, no partial dispatch |
| User cancels mid-run | Return whatever results are available, verdict = INCOMPLETE |

## Integration with Other Skills

| Skill | Integration |
|-------|------------|
| `design-review` | Run review-panel before a design review gate; feed findings into the review package |
| `change-impact` | Run review-panel on the change request artifact before assessing re-verification scope |
| `design-controls` | Review-panel validates traceability matrix completeness across regulatory + safety |

## Retrospective Mode

When invoked with `--retrospective-mode`, the review panel adjusts its behavior for gap-analysis artifacts.

### Flag Propagation
The `--retrospective-mode` flag propagates to every dispatched agent. Each agent's Retrospective Mode section (documented in its SKILL.md) defines how its evaluation changes.

### Panel Header
The panel summary header includes `**Mode: Retrospective**` when the flag is active. This makes the mode visible in the audit trail.

### Invocation
```bash
/review-panel regulatory/gap-analysis/gap-report-soup-2026-04-30.md --retrospective-mode
/review-panel regulatory/gap-analysis/gap-report-soup-2026-04-30.md --retrospective-mode --agents regulatory,qa,safety
```

### EVALUATION REFUSED Handling
When `--retrospective-mode` is active, the qa-reviewer may return `EVALUATION REFUSED` instead of findings (see qa-reviewer SKILL.md Retrospective Mode section). The review panel handles this as follows:

- `[EVALUATION REFUSED]` is displayed in the qa-reviewer section (distinct from `[AGENT FAILED]`)
- Panel verdict maps to `INCOMPLETE` — same priority as agent failure
- The refusal reason is included verbatim in the section output
- Other agents' results are still included — the panel does not abort

| Marker | Meaning | Panel Verdict |
|--------|---------|--------------|
| `[AGENT FAILED]` | Agent error or timeout | INCOMPLETE |
| `[AGENT TIMED OUT]` | Agent exceeded time limit | INCOMPLETE |
| `[EVALUATION REFUSED]` | Agent gate condition not met | INCOMPLETE |
| `[UNEXPECTED FORMAT]` | Agent output malformed | INCOMPLETE |

## Verification Checklist

After running a review panel, verify:

- [ ] Summary table includes a row for every dispatched agent
- [ ] Each agent section contains the full unmodified agent output
- [ ] Panel verdict matches the most conservative individual verdict
- [ ] Cross-agent conflicts are detected and marked when agents flag the same area
- [ ] Failed agents are marked and panel verdict is INCOMPLETE
- [ ] Severity counts in summary table use normalized panel levels
