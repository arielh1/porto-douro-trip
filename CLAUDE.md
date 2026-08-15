# Porto → Douro → Gerês — Trip Planning Agent Fleet

This repository is a self-improving trip planner for **Ariel and Shani**, September 2026.
Every agent in `.claude/agents/` runs headlessly via `claude -p` from `bin/run-cycle.sh`.

## The single source of truth

| File | Owner | Meaning |
|---|---|---|
| `trip/facts.md` | **Human only** | Flights, bookings, hard constraints. Agents READ this, never write it. |
| `trip/preferences.md` | Human, agents may propose | Travel style and taste. |
| `trip/itinerary.md` | `planner` agent only | The deliverable. Day-by-day plan. |
| `trip/critique.md` | `critic` agent only | Open problems with the current itinerary. |
| `trip/open-questions.md` | Any agent may append | Things only a human can decide or book. |
| `research/*.md` | Scout agents | Accumulated findings. Append, don't rewrite history. |
| `state/convergence.jsonl` | `bin/convergence.py` | One line per cycle. Never edit by hand. |

## Rules every agent must follow

1. **Never invent a fact that belongs in `trip/facts.md`.** If a flight time, hotel booking,
   or price is unknown, write it into `trip/open-questions.md` — do not guess it into the itinerary.
2. **Cite sources.** Every non-obvious claim in `research/` gets a URL next to it.
3. **Mark confidence.** Use `[confirmed]`, `[likely]`, `[unverified]` tags on factual claims.
4. **Respect the convergence phase.** `state/phase` tells you how much churn is allowed:
   - `explore` — propose freely, wide options, many alternatives.
   - `refine` — only change something if you can name a concrete improvement.
   - `lock` — structural days are frozen. Only fill gaps, fix errors, add booking detail.
5. **Small diffs win.** In `refine` and `lock`, a cycle that changes nothing is a success,
   not a failure. Do not churn the itinerary to look busy.
6. **Everything in the itinerary must be reachable.** Drive times are checked by `logistics`.
   A day the `critic` calls infeasible must be fixed before the next cycle ends.

## Travel style (why the plan looks the way it does)

Full detail is in `trip/preferences.md` — read it. The short version:

- **Wine and food are the point**, not a necessity. A harvest day, a few excellent
  quintas — not twenty. Less touristy Douro villages that people actually live in.
- **Places with character** over luxury. Stone houses, small quintas, a pool with a view.
- **Almost-nothing days** are a requirement, not a gap in the plan.
- **Ocean and optional morning surf** on the coastal leg — Ariel surfs 06:30–09:00 while
  Shani sleeps, and skips it entirely if the waves are bad. Never plan around waves.
- **Few transfers.** ≥3 nights per Douro base, ≥2 nights everywhere else.

## Shape of the trip

1. Land at **Porto (OPO)** — relaxed city days.
2. **Douro valley — 5-6 days**, exactly **two bases, ~3 nights each**.
   One indulgent quinta in the vineyards (pool, view); one rural and non-touristy.
3. **Nature reserve north of the Douro — short, ~2-3 days** (assumption: Peneda-Gerês).
4. **Campervan down the Atlantic coast — 5-6 days**:
   Porto → Aveiro / Figueira da Foz → Peniche / Baleal → Ericeira → Lisbon.
5. Fly home from **Lisbon (LIS)** — open-jaw ticket.

⚠️ An earlier version of this repo assumed the trip ended in Porto with no coastal leg.
That was wrong, and cycle 1's itinerary was built on it. `trip/facts.md` is authoritative.

## Running a cycle

```bash
bin/run-cycle.sh morning    # research-heavy: scouts run, planner integrates
bin/run-cycle.sh evening    # consolidation: planner + critic + convergence scoring
```
