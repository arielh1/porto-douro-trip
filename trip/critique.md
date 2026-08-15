# Critique — cycle 2
_2026-08-15_

## 🔴 Must fix — the plan is wrong or broken

- **Day 11 (Mon 21 Sept): The Yeatman is offered as the evening "serious meal," but
  it doesn't seat on Mondays.** `trip/itinerary.md` Day 11 lists "The Yeatman (2-star
  splurge...) or Cantinho do Avillez... if a more casual, easier-to-book option is
  preferred" — presenting Yeatman as the lead option, deliberately paired with the
  same-day Gaia port-house tour. But `research/porto.md`'s own sourced entry for The
  Yeatman gives **"seatings Tue–Sat 18:30/19:30/20:30"** — no Monday service. Per
  `trip/facts.md`'s calendar, Day 11 is unambiguously **Monday 21 September**. As
  written, the day's headline dinner isn't bookable on the date it's assigned to.
  Evidence: `trip/itinerary.md` Day 11 evening line; `research/porto.md` §Food, The
  Yeatman row ("seatings Tue–Sat"); `trip/facts.md` §Calendar (Day 11 = Monday).
  Suggested fix: drop The Yeatman from Day 11 and default to **Cantinho do Avillez**
  (already offered as the alternative in the same line, and `research/porto.md`
  doesn't record a weekday restriction for it). If Ariel specifically wants the
  Yeatman splurge, it needs a Tue–Sat Porto evening — the only other Porto days are
  Day 1 (Fri, arrival, deliberately zero-plan) and Day 2 (Sat, already booked with
  Lello/Clérigos and a sunset dinner) — neither is a clean fit without displacing
  something else and moving the Gaia visit off "the last Porto day" logic
  `research/porto.md` recommends. Cleanest fix is simply: this trip doesn't get a
  Yeatman night, update Day 11 and `trip/open-questions.md`'s "serious meal" entry
  accordingly.

## 🟠 Should fix — this will hurt the trip

- **Day 12 is labeled "medium pace... one light stop" but is actually one of the
  most demanding days in the trip, stacked directly on Day 11's already-full day.**
  Day 12 bundles: campervan pickup with a full systems walkthrough
  (`research/logistics.md` estimates **~1–2h** for this alone on an unfamiliar
  vehicle), a drive to Aveiro (~1h), **three** sub-stops there — a 45-min canal
  cruise, an Art Nouveau walk, and a drive-plus-stroll at Costa Nova (`research/coast.md`
  itself calls Costa Nova "an hour's stroll") — then the **longest single driving
  leg of the whole coastal side**, Aveiro→Baleal at ~1h40–2h
  (`research/logistics.md` §Coastal-leg drive-time matrix). That's van-admin plus
  what reads like 2–3 real anchors plus the trip's longest coastal drive, immediately
  after Day 11 — itself explicitly called a "full pace (2 anchors)" day with its own
  drive-back-from-Gerês and car-return admin on top. Days 9 (2h drive), 10 (half-day
  hike), 11 (2-anchor day + admin), and 12 (van admin + 3 stops + longest drive) run
  four demanding days back-to-back with no rest day in between — exactly what
  `CLAUDE.md`'s critic brief flags under "three big days in a row with no recovery."
  The next fully empty day isn't until Day 13. Evidence: `trip/itinerary.md` Days
  11–12; `research/coast.md` §Aveiro/Figueira da Foz; `research/logistics.md`
  §Coastal-leg drive-time matrix and the van-pickup admin estimate. Suggested fix:
  trim Aveiro to two stops instead of three (e.g. drop Costa Nova, or drop the canal
  cruise and keep the walk+Costa Nova), or accept Day 12 honestly as a "full pace"
  travel day rather than "medium," and consider whether Day 11's port tour could move
  to a lighter treatment (skip the splurge-dinner pairing given the 🔴 above) to give
  Day 11 more slack before Day 12.
- **The car/van handover "day-count-vs-risk" question was a call `research/logistics.md`
  explicitly flagged as "not something I can decide... a human decision," but the
  itinerary has already silently picked one answer.** `trip/itinerary.md` splits the
  handover across two days (Day 11: return car, overnight in Porto; Day 12: collect
  van) — the "costs a day but removes admin-under-time-pressure risk" option from
  `research/logistics.md`'s two alternatives. That's a defensible choice, but
  `trip/open-questions.md`'s entry on this is still phrased as an open decision for
  Ariel/Shani ("This is a day-count-vs-risk call for Ariel/Shani... not something I
  can resolve"), with no note that the planner has since committed to one answer.
  Evidence: `trip/itinerary.md` Days 11–12 structure; `trip/open-questions.md` §🟠
  "How the car/van handover works." Suggested fix: update the open-questions.md entry
  to say the itinerary now assumes the overnight-split option by default, and ask
  Ariel to confirm or override rather than leaving it as if nothing has been decided.

## 🟡 Consider

- **Day 10's dedicated Minho dinner (rojões à Minhota / papas de sarrabulho) is
  placed on the hiking day, which `research/nature.md` explicitly advises against.**
  Research says: "Suggest to the planner that a sarrabulho-style meal pairs better
  with a rest day than a hiking day." Day 10 is the Arado/Poço Azul half-day hike;
  the trimmed 2-night Gerês stay has no separate rest day to move it to. This
  reinforces — with a fresh, concrete reason — the itinerary's own open item about
  whether Gerês should get a 3rd night back. Evidence: `research/nature.md` §Eating;
  `trip/itinerary.md` Day 10; `trip/itinerary.md` §Still soft (Gerês night count).
  Suggested fix: no action needed unless a 3rd Gerês night gets added — at that
  point, move the sarrabulho dinner to the new rest day.
- **Douro base B silently settled on Lamego/Régua; Provesende never appears in the
  itinerary or "Still soft."** `research/douro.md` calls Provesende/Quinta Manhas
  Douro "the strongest match yet found" for the very-highly-weighted
  `trip/preferences.md` signal "village/quinta is non-touristy and lived-in," and
  flags this cycle as explicitly `explore`-phase (i.e., not yet time to narrow). The
  research file itself notes the trade-off (Provesende wins on character, Lamego
  wins on restaurant variety and logistics) but the itinerary doesn't mention having
  weighed it at all. Evidence: `research/douro.md` §Bases, Provesende entry and
  "Cycle-2 read"; `trip/preferences.md` scoring table. Suggested fix: not a
  structural change needed necessarily — Lamego may still win given facts.md wants
  base B "near a village with a couple of good restaurants" (Provesende's own
  research flags thin eating options beyond the quinta itself) — but the itinerary
  or "Still soft" should say this was considered and why it lost, not stay silent.
- **Gaia port tour is scheduled for Day 11's afternoon, when `research/porto.md`'s
  own sourced advice is "a weekday morning slot is the quietest realistic option...
  the terrace fills with coach/cruise traffic from midday on."** The itinerary
  already flags this itself as "worth revisiting," which is good practice, but it
  isn't tracked as a decision item in `trip/open-questions.md` the way other
  Graham's/Taylor's booking details are. Suggested fix: fold this specific
  morning-vs-afternoon tension into the existing open-questions.md entry so it isn't
  lost once a company/slot gets booked.
- **The BBC "world's six best views" claim (Day 4, Casal de Loivos) is stated as
  settled fact but its own source in `research/douro.md` is tagged `[likely]`,
  sourced via a secondary Komoot page, not a primary BBC citation.** Minor, but
  `CLAUDE.md` asks agents to mark confidence — worth softening the itinerary's
  wording or citing the primary source. Evidence: `research/douro.md` §Walks, Casal
  de Loivos row.
- **Research hygiene, not an itinerary error:** `research/porto.md`'s "Departure day
  plan" section (drop the car at the airport, Gaia visit then straight to the
  airport) still assumes the trip ends in Porto — the same stale assumption
  `research/logistics.md` already flagged in `research/nature.md`. The itinerary
  itself didn't fall into this trap (Day 11 correctly returns the car at Campanha
  with no flight that day), but the stale section in `research/porto.md` is still
  there and could mislead a future cycle. Worth a `scout-porto` cleanup pass.

## Logistics blockers

_`logistics` did not run this cycle — no new content to report. Its most recent
findings (the missing coastal leg, Day 6's drive-time correction) were both
addressed by the planner last cycle; see `trip/critique.md`'s prior "Planner
response" for the record. The car/van handover trade-off it raised is now
addressed above under 🟠, since the itinerary has since acted on it without
closing the loop in `trip/open-questions.md`._

## ✅ What's working

- **The coastal leg exists now and is internally consistent** — every day's date
  and weekday matches `trip/facts.md`'s calendar exactly (spot-checked all 17 days),
  the route never backtracks north of Lisbon, and Peniche/Baleal and Ericeira both
  clear the ≥2-night minimum with room to spare.
- **Day 6's drive-time fix from last cycle held up under a second check** — direct
  Pinhão→Lamego is genuinely ~32–36 min per `research/logistics.md`, and the
  itinerary uses that figure, not the old detoured one.
- **Day 10's Poço Azul/Arado safety distinction is threaded through correctly** —
  the itinerary is precise about swimming at Poço Azul, not at the falls, matching
  `research/nature.md`'s explicit correction, and the Mata de Albergaria toll-window
  note (last staffed day = this exact date) is a nice piece of research synthesis.
- **Drink-and-drive handling on Days 4 and 7** still correctly implements
  `research/logistics.md`'s alternate-taster/driver rule.
- **The genuinely empty days (Day 1, Day 5 partial, Day 8, Day 13, Day 15) are well
  distributed** and Day 8 is still smartly placed right before the hardest drive.
- **The harvest-day gap is being handled honestly** — Day 4 runs a placeholder
  standard tasting rather than inventing a fake harvest booking, and the open
  question is sharp and current (12–20 Sept window, Seixo as the one live
  candidate).

## Verdict

**still churning** — this cycle's big structural fix (the coastal leg) is solid and
holds up under a second pass, but a sourced factual conflict (Yeatman/Monday) and a
real pacing problem (Days 9–12 with no recovery) need fixing before this can be
called converging, and the vindima day is still the trip's biggest unresolved piece.
