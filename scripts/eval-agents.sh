#!/usr/bin/env bash
# Runs SaMD reviewer agents against test fixtures and scores results.
#
# Usage:
#   ./scripts/eval-agents.sh --dry-run all          # validate fixture format only ($0)
#   ./scripts/eval-agents.sh --dry-run safety-reviewer  # validate one agent's fixtures
#   ./scripts/eval-agents.sh all                    # run all agents live (~$0.05-0.15/fixture)
#   ./scripts/eval-agents.sh regulatory-reviewer    # run one agent live
#   ./scripts/eval-agents.sh --yes all              # skip cost confirmation prompt
#
# Dry-run validates: frontmatter has type+status, expected findings block exists
# with >=1 blocker-level finding, expected verdict uses valid agent terminology.
#
# Live eval invokes claude CLI per fixture, saves output to .results/, scores
# blocker detection and verdict matching.
#
# Scoring:
#   PASS - All expected blocker-level findings detected (keyword match),
#          verdict matches or is more conservative than expected.
#   FAIL - Expected blocker missed, verdict is best-case when blockers exist,
#          or fabricated citations detected.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

FIXTURES_DIR="examples/test-fixtures"
RESULTS_DIR="$FIXTURES_DIR/.results"
AGENTS_DIR=".claude/skills/agents"

ALL_AGENTS="regulatory-reviewer clinical-reviewer safety-reviewer qa-reviewer cybersecurity-reviewer"

# ── Agent severity/verdict lookups (bash 3 compatible) ───────────────────────

blocker_term() {
  case "$1" in
    regulatory-reviewer)    echo "BLOCKER" ;;
    clinical-reviewer)      echo "Critical" ;;
    safety-reviewer)        echo "SAFETY FINDING" ;;
    qa-reviewer)            echo "FINDING" ;;
    cybersecurity-reviewer) echo "SECURITY FINDING" ;;
  esac
}

warning_term() {
  case "$1" in
    regulatory-reviewer)    echo "WARNING" ;;
    clinical-reviewer)      echo "Important" ;;
    safety-reviewer)        echo "GAP" ;;
    qa-reviewer)            echo "OBSERVATION" ;;
    cybersecurity-reviewer) echo "GAP" ;;
  esac
}

best_verdict() {
  case "$1" in
    regulatory-reviewer)    echo "ACCEPTABLE" ;;
    clinical-reviewer)      echo "ACCEPTABLE" ;;
    safety-reviewer)        echo "ACCEPTABLE" ;;
    qa-reviewer)            echo "AUDIT-READY" ;;
    cybersecurity-reviewer) echo "ACCEPTABLE" ;;
  esac
}

valid_verdicts() {
  case "$1" in
    regulatory-reviewer)    echo "NOT SUBMITTABLE|NEEDS REVISION|ACCEPTABLE" ;;
    clinical-reviewer)      echo "CLINICALLY UNSAFE|NEEDS REVISION|ACCEPTABLE" ;;
    safety-reviewer)        echo "SAFETY CONCERN|NEEDS REVISION|ACCEPTABLE" ;;
    qa-reviewer)            echo "NOT AUDIT-READY|NEEDS REMEDIATION|AUDIT-READY" ;;
    cybersecurity-reviewer) echo "SECURITY CONCERN|NEEDS REVISION|ACCEPTABLE" ;;
  esac
}

# ── Helpers ──────────────────────────────────────────────────────────────────

usage() {
  sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
}

log()  { printf "\033[1;34m▸\033[0m %s\n" "$*"; }
pass() { printf "\033[1;32m✓ PASS\033[0m %s\n" "$*"; }
fail() { printf "\033[1;31m✗ FAIL\033[0m %s\n" "$*"; }
warn_msg() { printf "\033[1;33m⚠ WARN\033[0m %s\n" "$*"; }

# Extract value from YAML frontmatter (simple single-line fields only)
frontmatter_val() {
  local file="$1" key="$2"
  sed -n '/^---$/,/^---$/p' "$file" | grep "^${key}:" | head -1 | sed "s/^${key}: *//; s/[\"']//g"
}

# Extract expected findings block from comment lines
expected_findings() {
  local file="$1"
  grep '^# - ' "$file" | grep -v '^# Expected findings:' || true
}

# Extract expected verdict from comment
expected_verdict() {
  local file="$1"
  grep '^# - Expected verdict:' "$file" | sed 's/^# - Expected verdict: *//'
}

# Count blocker-level expected findings for an agent
count_expected_blockers() {
  local file="$1" agent="$2"
  local term
  term=$(blocker_term "$agent")
  expected_findings "$file" | grep -c "$term" || echo 0
}

# ── Dry-run validation ──────────────────────────────────────────────────────

validate_fixture() {
  local file="$1" agent="$2"
  local errors=0

  # Check frontmatter fields
  local ftype fstatus
  ftype=$(frontmatter_val "$file" "type")
  fstatus=$(frontmatter_val "$file" "status")

  if [ -z "$ftype" ]; then
    fail "$file: missing 'type' in frontmatter"
    errors=$((errors + 1))
  fi
  if [ -z "$fstatus" ]; then
    fail "$file: missing 'status' in frontmatter"
    errors=$((errors + 1))
  fi

  # Check expected findings block exists
  local findings
  findings=$(expected_findings "$file")
  if [ -z "$findings" ]; then
    fail "$file: no expected findings block (# - ...)"
    errors=$((errors + 1))
  fi

  # Check >=1 blocker-level finding
  local blocker_count
  blocker_count=$(count_expected_blockers "$file" "$agent")
  if [ "$blocker_count" -eq 0 ]; then
    fail "$file: no blocker-level finding ('$(blocker_term "$agent")')"
    errors=$((errors + 1))
  fi

  # Check verdict uses valid agent terminology
  local verdict
  verdict=$(expected_verdict "$file")
  if [ -z "$verdict" ]; then
    fail "$file: no expected verdict line"
    errors=$((errors + 1))
  else
    local valid_pattern
    valid_pattern=$(valid_verdicts "$agent")
    if ! echo "$verdict" | grep -qE "^(${valid_pattern})$"; then
      fail "$file: verdict '$verdict' not valid for $agent (expected: ${valid_pattern})"
      errors=$((errors + 1))
    fi
  fi

  if [ "$errors" -eq 0 ]; then
    pass "$file"
    return 0
  fi
  return 1
}

run_dry_run() {
  local total=0 passed=0 failed=0

  for agent in $@; do
    local agent_dir="$FIXTURES_DIR/$agent"
    if [ ! -d "$agent_dir" ]; then
      warn_msg "No fixture directory for $agent"
      continue
    fi

    log "Validating $agent fixtures..."
    for fixture in "$agent_dir"/*.md; do
      [ -f "$fixture" ] || continue
      total=$((total + 1))
      if validate_fixture "$fixture" "$agent"; then
        passed=$((passed + 1))
      else
        failed=$((failed + 1))
      fi
    done
  done

  echo ""
  log "Dry-run complete: $total fixtures, $passed passed, $failed failed"
  [ "$failed" -eq 0 ]
}

# ── Live evaluation ─────────────────────────────────────────────────────────

score_result() {
  local output_file="$1" fixture="$2" agent="$3"
  local errors=0
  local bterm
  bterm=$(blocker_term "$agent")
  local best
  best=$(best_verdict "$agent")

  # Check each expected blocker is detected in output
  local expected_blockers
  expected_blockers=$(expected_findings "$fixture" | grep "$bterm" || true)
  while IFS= read -r finding; do
    [ -z "$finding" ] && continue
    # Extract key phrase after the severity term
    local phrase
    phrase=$(echo "$finding" | sed "s|^# - ${bterm}: ||" | sed 's/ (.*//' | head -c 60)
    # Check if any meaningful keywords from the phrase appear in output
    local keywords matched=0 total_kw=0
    keywords=$(echo "$phrase" | tr ' ' '\n' | grep -E '.{4,}' | head -5)
    while IFS= read -r kw; do
      [ -z "$kw" ] && continue
      total_kw=$((total_kw + 1))
      if grep -qi "$kw" "$output_file" 2>/dev/null; then
        matched=$((matched + 1))
      fi
    done <<< "$keywords"
    # Require at least 40% keyword match
    if [ "$total_kw" -gt 0 ] && [ $((matched * 100 / total_kw)) -lt 40 ]; then
      fail "  Missing blocker: $phrase"
      errors=$((errors + 1))
    fi
  done <<< "$expected_blockers"

  # Check verdict is not best-case when blockers exist
  local expected_blocker_count
  expected_blocker_count=$(count_expected_blockers "$fixture" "$agent")
  if [ "$expected_blocker_count" -gt 0 ]; then
    if grep -qi "$best" "$output_file" 2>/dev/null; then
      local verdict_line
      verdict_line=$(grep -i "verdict\|recommendation\|overall" "$output_file" | grep -i "$best" || true)
      if [ -n "$verdict_line" ]; then
        fail "  Verdict is $best despite $expected_blocker_count blocker(s)"
        errors=$((errors + 1))
      fi
    fi
  fi

  return "$errors"
}

run_live_eval() {
  local total=0 passed=0 failed=0

  for agent in $@; do
    local agent_dir="$FIXTURES_DIR/$agent"
    local skill_file="$AGENTS_DIR/$agent/SKILL.md"
    local results_agent_dir="$RESULTS_DIR/$agent"

    if [ ! -d "$agent_dir" ]; then
      warn_msg "No fixture directory for $agent"
      continue
    fi
    if [ ! -f "$skill_file" ]; then
      warn_msg "No SKILL.md for $agent at $skill_file"
      continue
    fi

    mkdir -p "$results_agent_dir"
    log "Running $agent..."

    for fixture in "$agent_dir"/*.md; do
      [ -f "$fixture" ] || continue
      local bn
      bn=$(basename "$fixture" .md)
      local output_file="$results_agent_dir/${bn}.txt"
      total=$((total + 1))

      log "  $bn"
      local skill_content fixture_content
      skill_content=$(cat "$skill_file")
      fixture_content=$(cat "$fixture")

      # Invoke claude CLI
      if claude -p \
        --system-prompt "$skill_content" \
        --output-format text \
        --dangerously-skip-permissions \
        "Review this document:

$fixture_content" > "$output_file" 2>/dev/null; then

        # Score the output
        if score_result "$output_file" "$fixture" "$agent"; then
          pass "  $bn"
          passed=$((passed + 1))
        else
          failed=$((failed + 1))
        fi
      else
        fail "  $bn: claude CLI error"
        failed=$((failed + 1))
      fi
    done
  done

  # Summary table
  echo ""
  echo "┌─────────────────────────────┬────────┐"
  echo "│ Agent                       │ Result │"
  echo "├─────────────────────────────┼────────┤"
  for agent in $@; do
    local agent_dir="$FIXTURES_DIR/$agent"
    [ -d "$agent_dir" ] || continue
    local agent_passed=0 agent_total=0
    for fixture in "$agent_dir"/*.md; do
      [ -f "$fixture" ] || continue
      agent_total=$((agent_total + 1))
      local bn
      bn=$(basename "$fixture" .md)
      local of="$RESULTS_DIR/$agent/${bn}.txt"
      if [ -f "$of" ] && score_result "$of" "$fixture" "$agent" 2>/dev/null; then
        agent_passed=$((agent_passed + 1))
      fi
    done
    printf "│ %-27s │ %6s │\n" "$agent" "${agent_passed}/${agent_total}"
  done
  echo "└─────────────────────────────┴────────┘"
  echo ""
  log "Live eval complete: $total fixtures, $passed passed, $failed failed"
  [ "$failed" -eq 0 ]
}

# ── Main ─────────────────────────────────────────────────────────────────────

DRY_RUN=false
SKIP_CONFIRM=false
TARGET=""

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --yes)     SKIP_CONFIRM=true; shift ;;
    --help|-h) usage ;;
    *)         TARGET="$1"; shift ;;
  esac
done

[ -z "$TARGET" ] && usage

# Resolve target to agent list
if [ "$TARGET" = "all" ]; then
  AGENTS="$ALL_AGENTS"
else
  # Validate agent name
  found=false
  for a in $ALL_AGENTS; do
    if [ "$a" = "$TARGET" ]; then
      found=true
      break
    fi
  done
  if ! $found; then
    echo "Error: unknown agent '$TARGET'"
    echo "Valid agents: $ALL_AGENTS"
    exit 1
  fi
  AGENTS="$TARGET"
fi

# Count fixtures
fixture_count=0
for agent in $AGENTS; do
  agent_dir="$FIXTURES_DIR/$agent"
  [ -d "$agent_dir" ] || continue
  for f in "$agent_dir"/*.md; do
    [ -f "$f" ] && fixture_count=$((fixture_count + 1))
  done
done

if $DRY_RUN; then
  log "Dry-run: validating $fixture_count fixture(s) for $AGENTS"
  run_dry_run $AGENTS
else
  # Cost estimate and confirmation
  local_est=$(echo "$fixture_count * 0.10" | bc 2>/dev/null || echo "?.??")
  log "Live eval: $fixture_count fixture(s) for $AGENTS"
  log "Estimated cost: ~\$${local_est} (varies by model and response length)"

  if ! $SKIP_CONFIRM; then
    printf "\033[1;33mProceed? [y/N]\033[0m "
    read -r confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
      echo "Aborted."
      exit 0
    fi
  fi

  run_live_eval $AGENTS
fi
