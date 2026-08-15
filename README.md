# Porto · Douro · Gerês — a self-converging trip planner

An agent fleet that plans Ariel & Shani's September 2026 trip to northern Portugal,
upgrades the plan twice a day, and **stops when the plan is good** instead of
churning forever.

> 📄 The output you actually want is **[`trip/itinerary.md`](trip/itinerary.md)**.
> Everything else is machinery.

---

## The fleet

Six agents. Each is a real headless `claude -p` process with its own spec in
`.claude/agents/`. They never talk to each other directly — they coordinate only
through files in this repo, which is what makes each cycle reproducible and
reviewable as a git diff.

| Agent | Owns | Job |
|---|---|---|
| 🍇 `scout-douro` | `research/douro.md` | Quintas, harvest, villages, valley walks |
| 🌲 `scout-nature` | `research/nature.md` | The short reserve stop north of the Douro |
| 🏙 `scout-porto` | `research/porto.md` | Porto — the opening days, food, port houses |
| 🌊 `scout-coast` | `research/coast.md` | The campervan leg: van rental, where you may sleep, beaches, surf |
| 🛏 `stays` | `stays/` | One folder per place they sleep — the case for it, the catch, and original photos |
| 🚗 `logistics` | `research/logistics.md` | Drive times, car **and van**, **tasting-then-driving** — has veto power |
| 🗺 `planner` | `trip/itinerary.md` | The only agent that writes the itinerary |
| 🔍 `critic` | `trip/critique.md` | Adversarial review — never touches the itinerary |

The planner/critic split is the important one. One agent writes, another attacks,
and the planner must answer every objection in writing before the next cycle.

---

## The convergence loop

The fleet runs in phases, and the phase controls how much any agent is allowed to change.

```
explore  ──▶  refine  ──▶  lock  ──▶  converged
   │            │            │
   │            │            └─ structure frozen; only errors, gaps, booking detail
   │            └─ change only with a stated concrete improvement
   └─ restructure freely, wide options
```

After every cycle, `bin/convergence.py` diffs the itinerary against the previous
snapshot — ignoring timestamps and changelog rows, so cosmetic churn doesn't count
as progress — and promotes the phase only when the plan holds still:

| From | Needs stability | For | And |
|---|---|---|---|
| `explore` → `refine` | 70% | 1 cycle | — |
| `refine` → `lock` | 90% | 2 cycles | zero 🔴 findings |
| `lock` → `converged` | 97% | 2 cycles | zero 🔴 **and** no blocking questions |

A large change drops the fleet back a phase — that means something material was
discovered and the plan deserves rethinking. Once `converged`, cycles become no-ops.

**In `refine` and `lock`, a cycle that changes nothing is a success.** That rule is
written into the planner's spec, and it's the thing that makes the loop terminate.

---

## Running it

```bash
bin/run-cycle.sh morning     # scouts research in parallel → logistics → planner → critic
bin/run-cycle.sh evening     # logistics → planner → critic (no fresh scouting)
bin/run-cycle.sh --dry       # show what would run

python3 bin/convergence.py status    # phase, cycle count, stability history
```

### Codex / OpenAI engine

The repository is dual-engine. Codex uses `AGENTS.md`, platform-neutral specifications
in `agents/`, and the same `trip/`, `research/`, `stays/`, and `state/` as Claude.

```bash
python3 bin/validate-agent-fleet.py
bin/run-agent-codex.sh planner
bin/run-agent-codex.sh --dry critic
bin/run-cycle-codex.sh morning --dry
bin/run-cycle-codex.sh morning
bin/run-cycle-codex.sh evening
```

| Codex agent | Responsibility | Authoritative output |
|---|---|---|
| scout-douro | Douro bases, wine, food, harvest | `research/douro.md` |
| scout-nature | northern reserve and walks | `research/nature.md` |
| scout-porto | short Porto arrival | `research/porto.md` |
| scout-coast | campervan coast and surf | `research/coast.md` |
| festival-scout | exceptional trance/techno events | `research/festivals.md` |
| stays | lodging and legal overnight candidates | `stays/` |
| logistics | feasibility and vetoes | `research/logistics.md` |
| planner | authoritative itinerary | `trip/itinerary.md` |
| critic | independent audit | `trip/critique.md` |
| reporter | human-readable report; optional email | `state/report.*` |
| agent-author | safe fleet extension | fleet infrastructure |

See `docs/OPENAI-AGENT-ARCHITECTURE.md` for ownership, scheduling, manual invocation,
and the agent-creation workflow.

Two scheduled tasks run these automatically — morning and evening, Israel time.
Each one clones this repo, runs a cycle, and pushes the result, so **the git history
is the record of how the plan converged**.

---

## The files that matter

| File | Who writes it |
|---|---|
| `trip/facts.md` | **You.** Flights, bookings, hard constraints. Agents read it and never write it. |
| `trip/preferences.md` | You. The scoring function: wine & food, nature & walking, relaxed pace. |
| `trip/itinerary.md` | `planner` only |
| `trip/critique.md` | `critic` and `logistics` |
| `trip/open-questions.md` | Any agent. **Check this** — it's where the fleet asks you things. |
| `state/convergence.jsonl` | `convergence.py`. One line per cycle. |

### Your job in the loop

1. Fill in `trip/facts.md` when flights are booked. Nothing dates correctly until then.
2. Answer things in `trip/open-questions.md`.
3. Read `trip/itinerary.md` whenever you like and tell the fleet what you don't like.

Everything else runs without you.

---

## Trip shape

**Porto (OPO)** → **Douro, 5-6 days in two bases** → **short reserve stop north of the
Douro, 2-3 days** → **campervan down the coast, 5-6 days** (Aveiro → Peniche/Baleal →
Ericeira) → **fly home from Lisbon (LIS)**. About two weeks.

Style: wine and food as the point rather than a necessity, places with character over
luxury, almost-nothing days on purpose, optional 06:30 surfs that never own the day, and
as few transfers as the map allows.
