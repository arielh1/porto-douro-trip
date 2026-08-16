#!/usr/bin/env bash
# Registry-driven Codex cycle runner; manual-only agents remain outside this graph.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MODE="morning"
DRY=0
for arg in "$@"; do
  case "$arg" in
    morning|evening) MODE="$arg" ;;
    --dry) DRY=1 ;;
    *) echo "usage: bin/run-cycle-codex.sh [morning|evening] [--dry]" >&2; exit 2 ;;
  esac
done
PHASE="$(python3 bin/convergence.py phase 2>/dev/null | tr -d '\r' || echo explore)"
CYCLE="$(tr -d '\r' < state/cycle 2>/dev/null || echo 0)"
echo "Codex fleet: cycle $((CYCLE+1)) ($MODE), phase $PHASE"
if [[ "$PHASE" == "converged" ]]; then echo "Itinerary has converged; nothing to do."; exit 0; fi

mapfile -t STAGES < <(python3 - "$MODE" "$PHASE" <<'PY'
import json, sys
r=json.load(open("agents/registry.json", encoding="utf-8")); mode,phase=sys.argv[1:]
for stage in r["cycles"][mode]:
    eligible=[n for n in stage if phase in r["agents"][n]["phases"] and mode in r["agents"][n]["modes"]]
    if eligible: print(" ".join(eligible))
PY
)

failed=0
for stage in "${STAGES[@]}"; do
  read -ra agents <<<"$stage"
  echo "stage: ${agents[*]}"
  pids=()
  for name in "${agents[@]}"; do
    if (( DRY )); then
      bin/run-agent-codex.sh --dry "$name" "$MODE" || failed=1
    else
      bin/run-agent-codex.sh "$name" "$MODE" & pids+=("$!")
    fi
  done
  if (( ! DRY )); then
    for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
  fi
  (( failed )) && { echo "cycle stopped: an agent failed" >&2; exit 1; }
done

if (( DRY )); then echo "would score convergence"; exit 0; fi
python3 bin/convergence.py score

# Match the Claude runner's git-record semantics, but never require a successful push.
if git rev-parse --git-dir >/dev/null 2>&1 && [[ -n "$(git status --porcelain)" ]]; then
  NEWPHASE="$(cat state/phase 2>/dev/null || echo explore)"
  git add -A
  git commit -m "cycle $((CYCLE+1)) ($MODE, codex): $PHASE → $NEWPHASE"
  git remote get-url origin >/dev/null 2>&1 && git push origin HEAD || true
fi
