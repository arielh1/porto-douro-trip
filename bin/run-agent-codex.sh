#!/usr/bin/env bash
# Run one registered fleet agent in a fresh, non-interactive Codex process.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DRY=0
if [[ "${1:-}" == "--dry" ]]; then DRY=1; shift; fi
NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  echo "usage: bin/run-agent-codex.sh [--dry] AGENT [mode]" >&2
  exit 2
fi
MODE="${2:-manual}"
REGISTRY="agents/registry.json"

readarray -t META < <(python3 - "$NAME" <<'PY'
import json, sys
r=json.load(open("agents/registry.json", encoding="utf-8"))
a=r["agents"].get(sys.argv[1])
if not a: raise SystemExit(f"unknown agent: {sys.argv[1]}")
print(a["spec"])
print(", ".join(a["reads"]))
print(", ".join(a["writes"]))
PY
)
SPEC="${META[0]}"
PHASE="$(python3 bin/convergence.py phase 2>/dev/null || echo explore)"
CYCLE="$(cat state/cycle 2>/dev/null || echo 0)"
NEXT=$((CYCLE + 1))

PROMPT="You are the '$NAME' agent in this repository's Codex travel fleet.
Start fresh. Read AGENTS.md completely, then $SPEC, then the registered inputs.
Run context: mode=$MODE, cycle=$NEXT, convergence phase=$PHASE.
Allowed reads: ${META[1]}
Allowed writes: ${META[2]}
Follow source authority, citation/confidence rules, phase limits, file ownership,
and stdout contract exactly. Inspect the git diff before finishing and revert none
of the human's pre-existing changes. Do not modify any unlisted path."

if (( DRY )); then
  printf 'would run %-16s phase=%s mode=%s spec=%s\n' "$NAME" "$PHASE" "$MODE" "$SPEC"
  exit 0
fi
if [[ "$PHASE" == "converged" ]]; then
  echo "fleet is converged; no agent invoked"
  exit 0
fi
if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found. Install/configure it, then verify with: codex --help" >&2
  exit 127
fi

mkdir -p state/logs
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="state/logs/${STAMP}-${NAME}-codex.log"
# Verified Codex CLI shape: `codex exec` is the non-interactive entry point. Keep all
# runtime flags here so CLI-version adjustments never alter agent specifications.
if codex exec --full-auto -C "$ROOT" "$PROMPT" >"$OUT" 2>&1; then
  tail -5 "$OUT"
else
  status=$?
  echo "$NAME failed (see $OUT). Run 'codex --help' and 'codex exec --help' on this host." >&2
  tail -10 "$OUT" >&2 || true
  exit "$status"
fi

