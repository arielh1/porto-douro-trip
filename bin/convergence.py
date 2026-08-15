#!/usr/bin/env python3
"""
Convergence scoring for the trip-planning agent fleet.

Measures how much the itinerary changed since the previous cycle, combines that with
the critic's findings and the state of blocking questions, and decides which phase
the fleet should run in next.

The point: the fleet should stop churning once the plan is good. Phase is the brake.

Usage:
    convergence.py score      # score the current cycle, write state, print report
    convergence.py phase      # print the current phase only
    convergence.py status     # human-readable status
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITINERARY = ROOT / "trip" / "itinerary.md"
CRITIQUE = ROOT / "trip" / "critique.md"
QUESTIONS = ROOT / "trip" / "open-questions.md"
STATE = ROOT / "state"
SNAPSHOTS = STATE / "snapshots"
LOG = STATE / "convergence.jsonl"
PHASE_FILE = STATE / "phase"
CYCLE_FILE = STATE / "cycle"

PHASES = ["explore", "refine", "lock", "converged"]

# How stable the itinerary must be to move up a phase, and for how many cycles.
PROMOTION = {
    "explore": {"similarity": 0.70, "streak": 1, "max_red": 99},
    "refine":  {"similarity": 0.90, "streak": 2, "max_red": 0},
    "lock":    {"similarity": 0.97, "streak": 2, "max_red": 0},
}
# A big change drops the fleet back a phase — something material was discovered.
REGRESSION_SIMILARITY = 0.60


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def normalise(text: str) -> list[str]:
    """Strip the noise that changes every cycle but means nothing.

    Without this, the timestamp and cycle-number lines alone would make every cycle
    look like a change and the fleet would never converge.
    """
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        low = s.lower()
        if low.startswith(("**cycle:**", "**updated:**", "_last updated", "**status:**")):
            continue
        if low.startswith("|") and re.match(r"^\|\s*\d+\s*\|", s):  # changelog rows
            continue
        s = re.sub(r"\d{4}-\d{2}-\d{2}", "<date>", s)
        s = re.sub(r"\s+", " ", s)
        out.append(s)
    return out


def similarity(old: str, new: str) -> float:
    a, b = normalise(old), normalise(new)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def count_findings(critique: str) -> dict[str, int]:
    return {
        "red": critique.count("🔴") + len(re.findall(r"^\s*-\s*\*\*Day", critique, re.M)) * 0,
        "orange": critique.count("🟠"),
        "yellow": critique.count("🟡"),
    }


def blocking_questions(q: str) -> int:
    """Count unchecked items under the 🔴 blocking heading."""
    m = re.search(r"##\s*🔴.*?(?=\n##|\Z)", q, re.S)
    return len(re.findall(r"^\s*-\s*\[ \]", m.group(0), re.M)) if m else 0


def load_log() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def current_phase() -> str:
    p = read(PHASE_FILE).strip()
    return p if p in PHASES else "explore"


def latest_snapshot() -> str:
    snaps = sorted(SNAPSHOTS.glob("itinerary-*.md"))
    return read(snaps[-1]) if snaps else ""


def decide_phase(phase: str, sim: float, red: int, blockers: int, history: list[dict]) -> tuple[str, str]:
    if phase == "converged":
        if sim < REGRESSION_SIMILARITY:
            return "refine", "itinerary changed materially after converging — reopening"
        return "converged", "holding"

    if sim < REGRESSION_SIMILARITY and history:
        back = PHASES[max(0, PHASES.index(phase) - 1)]
        if back != phase:
            return back, f"large change (similarity {sim:.2f}) — stepping back to {back}"

    rule = PROMOTION[phase]
    if red > rule["max_red"]:
        return phase, f"{red} must-fix finding(s) open"
    if blockers and phase in ("lock",):
        return phase, f"{blockers} blocking question(s) unanswered — cannot converge"
    if sim < rule["similarity"]:
        return phase, f"still moving (similarity {sim:.2f} < {rule['similarity']})"

    # count the streak of cycles already at or above this threshold
    streak = 1
    for entry in reversed(history):
        if entry.get("phase") == phase and entry.get("similarity", 0) >= rule["similarity"]:
            streak += 1
        else:
            break
    if streak < rule["streak"]:
        return phase, f"stable {streak}/{rule['streak']} cycles — need one more"

    nxt = PHASES[PHASES.index(phase) + 1]
    return nxt, f"stable for {streak} cycles at similarity {sim:.2f} — promoting to {nxt}"


def cmd_score() -> int:
    new = read(ITINERARY)
    if not new.strip():
        print("convergence: itinerary is empty — nothing to score", file=sys.stderr)
        return 1

    old = latest_snapshot()
    sim = similarity(old, new)
    critique = read(CRITIQUE)
    findings = count_findings(critique)
    blockers = blocking_questions(read(QUESTIONS))
    history = load_log()
    cycle = len(history) + 1
    phase = current_phase()

    new_phase, reason = decide_phase(phase, sim, findings["red"], blockers, history)

    entry = {
        "cycle": cycle,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "phase": phase,
        "next_phase": new_phase,
        "similarity": round(sim, 4),
        "drift": round(1 - sim, 4),
        "findings": findings,
        "blocking_questions": blockers,
        "reason": reason,
        "itinerary_lines": len(normalise(new)),
    }

    STATE.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (SNAPSHOTS / f"itinerary-{stamp}.md").write_text(new, encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    PHASE_FILE.write_text(new_phase + "\n", encoding="utf-8")
    CYCLE_FILE.write_text(str(cycle) + "\n", encoding="utf-8")

    bar = "█" * int(sim * 30) + "░" * (30 - int(sim * 30))
    print(f"""
  cycle {cycle}   {phase} → {new_phase}
  stability  [{bar}] {sim:.1%}
  findings   {findings['red']}🔴  {findings['orange']}🟠  {findings['yellow']}🟡
  blocking   {blockers} unanswered question(s)
  verdict    {reason}
""".rstrip())
    return 0


def cmd_phase() -> int:
    print(current_phase())
    return 0


def cmd_status() -> int:
    history = load_log()
    if not history:
        print("No cycles yet. Phase: explore")
        return 0
    print(f"Phase: {current_phase()}   Cycles: {len(history)}\n")
    print(f"{'cyc':>4} {'phase':<10} {'stability':>9} {'red':>4} {'reason'}")
    for e in history[-12:]:
        print(f"{e['cycle']:>4} {e['phase']:<10} {e['similarity']:>8.1%} "
              f"{e['findings']['red']:>4} {e['reason'][:60]}")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "score"
    sys.exit({"score": cmd_score, "phase": cmd_phase, "status": cmd_status}
             .get(cmd, lambda: (print(__doc__), 2)[1])())
