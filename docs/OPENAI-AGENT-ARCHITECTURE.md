# Dual-engine agent architecture

The Claude and Codex fleets are two runtimes over one repository state. Neither owns a
private copy of the trip.

```text
Human → trip/facts.md + trip/preferences.md
                         │
      parallel research agents + stays
                         │
                         ▼
                     logistics ── veto → trip/critique.md
                         │
                         ▼
                      planner → trip/itinerary.md
                         │
                         ▼
                       critic → trip/critique.md
                         │
                         ▼
              bin/convergence.py → shared state → repeat/stop
```

## Components

| Concern | Claude | Codex | Shared |
|---|---|---|---|
| Repository contract | `CLAUDE.md` | `AGENTS.md` | human facts/preferences |
| Agent definitions | `.claude/agents/` | `agents/*.md` + registry | output files |
| One agent | internal `run_agent` | `bin/run-agent-codex.sh` | fresh file context |
| Cycle | `bin/run-cycle.sh` | `bin/run-cycle-codex.sh` | convergence engine |
| Phase | reads state | reads state | `state/phase` |

The Claude implementation is intentionally preserved. The Codex registry removes agent
names from its shell runner and declares mission, reads, writes, phases, modes, and
dependencies in inspectable JSON. Agent prompts describe intent and contracts rather
than Claude-specific tool names.

## Ownership and graph

The complete machine-checkable map is `agents/registry.json`; `AGENTS.md` defines its
human meaning. Morning's first stage is the disjoint research set: Douro, nature, Porto,
coast, festivals, and stays. Those authoritative outputs differ, so processes run in
parallel. `trip/open-questions.md` is an explicitly shared append surface: agents must
append non-duplicate questions and preserve existing text. Logistics waits for research;
planner waits for logistics; critic waits for planner; convergence waits for critic.
Evening starts at logistics.

`reporter` is registered but intentionally outside the convergence cycle, matching the
existing repository. It can be invoked manually. Email is connector-dependent; report
generation is portable and delivery failure must be explicit.

## Runtime abstraction

An invocation reads `AGENTS.md`, its spec, and registered inputs from disk. The prompt
contains cycle, mode, phase, and allowed paths. It writes only registered outputs and
ends with a short stdout summary captured under `state/logs/`. No conversation transcript
is carried between processes. Git diffs plus convergence snapshots form the audit trail.

The Codex runner uses the non-interactive `codex exec` entry point. Before production,
run `codex --help` and `codex exec --help` on the target host. This migration host exposed
a desktop-bundled executable but Windows denied shell execution, so live runtime testing
was not possible here; dry-run and registry validation remain deterministic.

## Commands

```bash
python3 bin/validate-agent-fleet.py
bin/run-agent-codex.sh --dry planner
bin/run-agent-codex.sh planner
bin/run-agent-codex.sh reporter
bin/run-cycle-codex.sh morning --dry
bin/run-cycle-codex.sh morning
bin/run-cycle-codex.sh evening
python3 bin/convergence.py status
```

The original Claude commands remain `bin/run-cycle.sh morning|evening|--dry`.

## Creating an agent

Invoke `agent-author` manually with a concrete request. It performs a responsibility and
ownership collision check before writing. A successful registration includes a spec,
registry entry, graph stage and dependencies, phase/mode policy, docs, and validation.
Use a uniquely owned research output whenever possible. A collision on an authoritative
file is a hard stop, not a warning.

The `festival-scout` is the acceptance example: it owns `research/festivals.md`, reads
confirmed dates and the route, runs alongside independent morning researchers in explore
and refine, reports only verified high-value electronic events, and never edits the
itinerary. Planner may consider its evidence after logistics has assessed route impact.

## Scheduling and GitHub Actions

The current disabled workflow installs Claude only and remains untouched. A Codex job
must install an official CLI version appropriate to the runner, supply authentication as
a repository secret, run validation and the Codex cycle, and use a concurrency group so
morning/evening writes cannot overlap. Do not enable or add credentials during migration.
Scheduled desktop tasks should clone/pull a clean branch, run one fresh cycle, and push
the generated commit. Reporter email additionally requires an authenticated Gmail
capability; a headless CLI must not assume the desktop connector exists.

