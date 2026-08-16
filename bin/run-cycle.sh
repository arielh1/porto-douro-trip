#!/usr/bin/env bash
#
# The orchestrator. Runs one upgrade cycle of the trip-planning agent fleet.
#
#   bin/run-cycle.sh morning   # scouts run in parallel, then planner, then critic
#   bin/run-cycle.sh evening   # logistics + planner + critic, no fresh scouting
#   bin/run-cycle.sh --dry     # print what would run
#
# Each agent is a real headless `claude -p` process reading its own definition
# from .claude/agents/. They share state only through files in the repo.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MODE="${1:-morning}"
DRY=0
[[ "${1:-}" == "--dry" ]] && { DRY=1; MODE="morning"; }

LOGDIR="state/logs"
mkdir -p "$LOGDIR" state/snapshots
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUNLOG="$LOGDIR/cycle-$STAMP-$MODE.log"

PHASE="$(python3 bin/convergence.py phase 2>/dev/null | tr -d '\r' || echo explore)"
CYCLE="$(tr -d '\r' < state/cycle 2>/dev/null || echo 0)"
NEXT=$((CYCLE + 1))

c()  { printf '\033[%sm%s\033[0m\n' "$1" "$2"; }
hr() { printf '─%.0s' $(seq 1 62); echo; }

hr
c '1;36' "  Porto · Douro · Gerês — cycle $NEXT ($MODE)"
c '0;90'  "  phase: $PHASE   $(date -u '+%Y-%m-%d %H:%M UTC')"
hr

if [[ "$PHASE" == "converged" ]]; then
  c '1;32' "  ✓ Itinerary has converged. Nothing to do."
  c '0;90' "    Force a cycle with:  echo lock > state/phase"
  exit 0
fi

# ── the agent runner ──────────────────────────────────────────────────────────
# Runs one agent headlessly. The agent reads its own spec file, so behaviour is
# defined in .claude/agents/ and this script stays dumb.
run_agent() {
  local name="$1" extra="${2:-}"
  local spec=".claude/agents/${name}.md"
  local out="$LOGDIR/${STAMP}-${name}.log"

  if [[ ! -f "$spec" ]]; then
    c '0;31' "  ✗ $name — no spec at $spec"; return 1
  fi

  local prompt="You are the '${name}' agent in this repository's trip-planning fleet.

Read and follow your full specification at ${spec}. It defines your mission, the
file you own, and the rules you plan by. Follow it exactly.

Context for this run:
  - cycle: ${NEXT}
  - time of day: ${MODE}
  - convergence phase: ${PHASE}   (see CLAUDE.md for what this phase permits)

Read CLAUDE.md first for the shared rules, then trip/facts.md for ground truth.
Do the work, write your file, and finish with your short stdout summary.
${extra}"

  if (( DRY )); then
    c '0;90' "  · would run $name"
    return 0
  fi

  c '1;34' "  ▸ $name"
  if timeout 900 claude -p "$prompt" \
        --permission-mode acceptEdits \
        --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Bash" \
        > "$out" 2>&1; then
    tail -4 "$out" | sed 's/^/      /'
    echo "--- $name ---" >> "$RUNLOG"; cat "$out" >> "$RUNLOG"
  else
    c '0;31' "  ✗ $name failed (see $out)"
    tail -6 "$out" | sed 's/^/      /'
  fi
}

# ── phase 1: scouts (morning only, and never in lock) ─────────────────────────
if [[ "$MODE" == "morning" && "$PHASE" != "lock" ]]; then
  c '1;33' "  research"
  for a in scout-douro scout-nature scout-porto scout-coast stays; do
    run_agent "$a" &
  done
  wait
  echo
elif [[ "$MODE" == "morning" ]]; then
  c '0;90' "  research — skipped (phase is lock; research is frozen)"
  echo
fi

# ── phase 2: logistics ────────────────────────────────────────────────────────
c '1;33' "  feasibility"
run_agent logistics
echo

# ── phase 3: planner ──────────────────────────────────────────────────────────
c '1;33' "  planning"
run_agent planner "
Address every point in trip/critique.md from the previous cycle before anything else."
echo

# ── phase 4: critic ───────────────────────────────────────────────────────────
c '1;33' "  review"
run_agent critic
echo

# ── phase 5: score and decide ─────────────────────────────────────────────────
if (( DRY )); then c '0;90' "  · would score convergence"; exit 0; fi

hr
python3 bin/convergence.py score
hr

NEWPHASE="$(tr -d '\r' < state/phase 2>/dev/null || echo explore)"

# ── phase 6: commit ───────────────────────────────────────────────────────────
if git rev-parse --git-dir >/dev/null 2>&1 && [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -q -m "cycle ${NEXT} (${MODE}): ${PHASE} → ${NEWPHASE}

$(python3 -c "
import json,pathlib
p=pathlib.Path('state/convergence.jsonl')
e=json.loads(p.read_text().splitlines()[-1])
f=e['findings']
print(f\"stability {e['similarity']:.1%} · {f['red']} must-fix · {e['blocking_questions']} blocking questions\")
print(e['reason'])
" 2>/dev/null)"
  c '0;32' "  ✓ committed"
  if git remote get-url origin >/dev/null 2>&1; then
    git push -q origin HEAD 2>/dev/null && c '0;32' "  ✓ pushed" || c '0;33' "  ! push failed"
  fi
else
  c '0;90' "  · no changes to commit"
fi

if [[ "$NEWPHASE" == "converged" ]]; then
  echo
  c '1;32' "  ★ The itinerary has converged."
fi
