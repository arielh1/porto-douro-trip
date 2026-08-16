#!/usr/bin/env python3
"""Validate registry, specifications, ownership, phases, and orchestration DAG."""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "agents" / "registry.json"
REQUIRED = {"spec", "mission", "reads", "writes", "phases", "modes", "depends_on"}

def main() -> int:
    errors: list[str] = []
    if not (ROOT / "AGENTS.md").is_file(): errors.append("missing AGENTS.md")
    try: data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: cannot read registry: {exc}"); return 1
    agents = data.get("agents", {})
    phases = set(data.get("phases", []))
    human = set(data.get("human_only", []))
    shared = set(data.get("shared_writes", []))
    owners: dict[str, list[str]] = defaultdict(list)

    for name, cfg in agents.items():
        missing = REQUIRED - cfg.keys()
        if missing: errors.append(f"{name}: missing fields {sorted(missing)}"); continue
        spec = ROOT / cfg["spec"]
        if not spec.is_file(): errors.append(f"{name}: missing spec {cfg['spec']}")
        if set(cfg["phases"]) - phases: errors.append(f"{name}: invalid phases {set(cfg['phases'])-phases}")
        for path in cfg["writes"]:
            if path in human: errors.append(f"{name}: writes human-only path {path}")
            owners[path].append(name)
        for dep in cfg["depends_on"]:
            if dep not in agents: errors.append(f"{name}: unknown dependency {dep}")

    for path, names in owners.items():
        if len(names) > 1 and path not in shared:
            errors.append(f"duplicate authoritative ownership: {path}: {', '.join(names)}")

    registered_specs = {cfg.get("spec") for cfg in agents.values()}
    for spec in (ROOT / "agents").glob("*.md"):
        rel = spec.relative_to(ROOT).as_posix()
        if rel not in registered_specs: errors.append(f"unregistered agent spec: {rel}")

    # Every legacy Claude fleet role must have a same-name Codex port.
    for spec in (ROOT / ".claude" / "agents").glob("*.md"):
        if spec.stem not in agents:
            errors.append(f"Claude agent has no Codex equivalent: {spec.stem}")

    referenced: set[str] = set()
    for mode, stages in data.get("cycles", {}).items():
        positions = {name: i for i, stage in enumerate(stages) for name in stage}
        for stage in stages:
            for name in stage:
                referenced.add(name)
                if name not in agents: errors.append(f"cycle {mode}: unknown agent {name}")
                elif mode not in agents[name]["modes"]: errors.append(f"cycle {mode}: {name} excludes mode")
        for name, pos in positions.items():
            for dep in agents.get(name, {}).get("depends_on", []):
                # A dependency absent from a mode is previous persisted state; if both
                # run in this mode, their ordering must be strictly topological.
                if dep in positions and positions[dep] >= pos:
                    errors.append(f"cycle {mode}: {name} does not follow dependency {dep}")

    visiting: set[str] = set(); visited: set[str] = set()
    def visit(name: str, trail: tuple[str, ...] = ()) -> None:
        if name in visiting: errors.append("dependency cycle: " + " -> ".join(trail + (name,))); return
        if name in visited or name not in agents: return
        visiting.add(name)
        for dep in agents[name].get("depends_on", []): visit(dep, trail + (name,))
        visiting.remove(name); visited.add(name)
    for name in agents: visit(name)

    # Critical invariants are explicit acceptance tests.
    if owners.get("trip/itinerary.md") != ["planner"]: errors.append("planner must be sole itinerary owner")
    if "trip/itinerary.md" in agents.get("critic", {}).get("writes", []): errors.append("critic may not write itinerary")
    if not {"research/logistics.md", "trip/critique.md"}.issubset(agents.get("logistics", {}).get("writes", [])):
        errors.append("logistics veto contract missing")

    if errors:
        for err in errors: print("ERROR:", err)
        print(f"fleet invalid: {len(errors)} error(s)"); return 1
    print(f"fleet valid: {len(agents)} agents, {len(referenced)} orchestrated, {len(owners)} write surfaces")
    return 0

if __name__ == "__main__": sys.exit(main())
