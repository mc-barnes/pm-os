---
type: decision
status: approved
owner: "@mc-barnes"
last-reviewed: 2026-04-30
related:
  - .claude/skills/agents/regulatory-reviewer/SKILL.md
  - .claude/skills/agents/clinical-reviewer/SKILL.md
  - .claude/skills/agents/qa-reviewer/SKILL.md
  - .claude/skills/agents/cybersecurity-reviewer/SKILL.md
  - .claude/skills/agents/safety-reviewer/SKILL.md
  - .claude/skills/review-panel/SKILL.md
---
# Decision: DEC-001 — Review Panel Orchestration

## Context

With five agent personas now shipping (clinical-reviewer, regulatory-reviewer, qa-reviewer, safety-reviewer, cybersecurity-reviewer), the natural next layer is a fan-out orchestration skill that runs multiple reviewers against an artifact in parallel and synthesizes findings into a single review package. This was noted as future work in the regulatory-reviewer spec ("Not the review-panel fan-out skill — that will be spec'd separately") and risks being lost without a tracked decision record.

## Options Considered

| Option | Pros | Cons | Regulatory Impact |
|--------|------|------|-------------------|
| A: Single fan-out skill that dispatches to all agents | Simple, one command | May be slow, all-or-nothing | None — orchestration only |
| **B: Configurable panel (select which reviewers to include)** | **Flexible, faster for targeted reviews** | **More complex to implement** | **None** |
| C: Defer — keep manual agent invocation | Zero implementation cost | Loses cross-reviewer synthesis, easy to skip a reviewer | Risk of incomplete reviews |

## Decision

**Option B: Configurable panel.** Auto-route by artifact `type:` frontmatter with user override via explicit agent list.

Key design choices:
- **Routing:** Artifact `type:` frontmatter maps to a default agent set via a routing table covering all 22 document types defined in the project CLAUDE.md. Unknown types dispatch all 5 agents.
- **Execution:** Parallel dispatch via Agent tool — all selected agents run concurrently.
- **Output:** Single merged markdown document with summary table (agent x verdict), per-agent sections (unmodified, not deduplicated), and `CROSS-AGENT CONFLICT` markers when agents flag the same area differently.
- **Panel verdict:** Most conservative wins. Verdict hierarchy: INCOMPLETE > FAIL > CONDITIONAL > PASS.
- **Failure handling:** Partial results shown; panel verdict = INCOMPLETE if any agent fails or times out.

Implemented in `.claude/skills/review-panel/SKILL.md`.

## Consequences

- **Product**: Enables one-command regulatory review across all dimensions
- **Regulatory**: Reduces risk of missing a review dimension when multiple agents exist
- **Engineering**: Uses Agent tool parallel dispatch pattern — no custom infrastructure needed

## Action Items

- [x] Spec the orchestration skill — `.claude/skills/review-panel/SKILL.md`
- [x] Define output format for merged review findings — summary table + per-agent sections
- [x] Decide on conflict resolution when agents disagree on severity — scope-boundary ownership + `CROSS-AGENT CONFLICT` markers

## Participants

- @mc-barnes (PM / decision owner)
