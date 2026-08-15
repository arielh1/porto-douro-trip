# Porto → Douro → Gerês Agent Fleet (Codex)

This repository is a deterministic, file-mediated travel-planning fleet for Ariel
and Shani's September 2026 Portugal trip. Each invocation starts fresh, reads the
repository, makes a narrowly owned change, and leaves an auditable git diff. Hidden
conversation history is never a source of truth.

## Authority and ownership

Read inputs in this order: `trip/facts.md`, current critique and logistics blockers,
`trip/preferences.md`, cited `research/`, then `state/phase`.

| Path | Authority / writer |
|---|---|
| `trip/facts.md` | Human only. Agents must never modify it. |
| `trip/preferences.md` | Human owned. Agents may suggest changes in open questions, never edit it. |
| `trip/itinerary.md` | `planner` only. It is the authoritative plan. |
| `trip/critique.md` | `critic`; `logistics` may edit only `## Logistics blockers`; planner may append only its response. |
| `trip/open-questions.md` | Shared append surface for questions requiring human facts, choices, or bookings. Never answer on the human's behalf. |
| `research/*.md` | The matching research agent named in `agents/registry.json`. |
| `stays/` | `stays`. |
| `state/phase`, `state/cycle`, `state/convergence.jsonl`, `state/snapshots/` | `bin/convergence.py` only. |
| `state/report.html`, `state/report.txt` | `reporter` via `bin/build-report.py`. |
| `agents/registry.json`, `agents/*.md`, fleet docs/runners/tests | `agent-author` only when explicitly asked to add or revise an agent. |

No agent may invent flights, dates, bookings, prices, opening hours, availability,
or human choices. Put unknown human facts in `trip/open-questions.md`. Every
non-obvious research claim needs a URL and a confidence tag: `[confirmed]` for a
primary source, `[likely]` for corroborated secondary evidence, or `[unverified]`
for a single weak source or inference. Estimates must be labelled `[estimate]` and
show their basis.

## Convergence contract

- `explore`: research agents may widen options; planner may restructure.
- `refine`: make a change only for a named, concrete improvement. Prefer small diffs.
- `lock`: research is frozen except corrections and booking verification. Bases,
  nights, and segment order are frozen. Logistics verification has priority.
- `converged`: do no agent work. Only a deliberate human reopening may resume cycles.

In `refine` and `lock`, no material change is a successful result. Never reword to
appear productive. `bin/convergence.py` is the shared phase engine and must not be
duplicated per platform.

The planner and critic must remain independent. The critic never writes the itinerary.
The planner must address every critique item but may explain a sourced disagreement.
Logistics may veto a physically infeasible day in its reserved critique section; the
planner must resolve that blocker before convergence.

## Runtime and communication

The registry is the orchestration authority. Run one Codex agent with
`bin/run-agent-codex.sh NAME`; run a cycle with `bin/run-cycle-codex.sh morning` or
`evening`. `--dry` prints the graph without invoking Codex. Agents communicate only
through repository files and stdout summaries. Do not depend on a prior chat.

Before editing, read this file, the selected specification, `trip/facts.md`,
`trip/preferences.md`, `state/phase`, and every path listed in that specification's
`reads`. Modify only its `writes`; all other files are forbidden. Preserve human edits.

## Adding agents

Use `agent-author`. It must check for overlapping responsibility and authoritative
write ownership, define dependencies and phase/mode eligibility, add a complete spec
and registry entry, update documentation, and run `python bin/validate-agent-fleet.py`.
It must stop on an ownership conflict rather than granting two agents the same file.
New research files may feed the planner, but new agents never gain itinerary ownership.
