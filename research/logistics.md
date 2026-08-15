# logistics — research
_Last updated: 2026-08-15 · cycle 2 (explore)_

No itinerary exists yet (`trip/itinerary.md` is still the seed skeleton), so there is
nothing to veto this cycle. This file builds the feasibility groundwork — drive times,
car rental, drink-driving, trains/boats, September specifics — for the `planner` to
build the first real itinerary against, and for me to check day-by-day starting next
cycle.

## 1. Drive time matrix

Real driving times (not straight-line), Google/Rome2Rio-style routing. All `[likely]`
or `[estimate]` — none of this is walked/driven personally, treat as planning-grade,
not gospel.

| From | To | Distance | Realistic drive | Road | Notes |
|---|---|---|---|---|---|
| Porto (Campanhã) | Pinhão | ~119–122 km | **~1h25–1h30** | A4/IP4 (fast, tolled→**toll-free since 1 Jan 2025**) | Do not route via the N222 for this leg — it's a Douro-internal road, not the Porto approach. `[likely]` |
| Porto Airport (OPO) | Peso da Régua | ~100 km | **~1h10** | A4 (fast) | Natural route if picking up at the airport instead of in the city. `[likely]` |
| Pinhão | Peso da Régua | ~21–27 km | **~45–60 min** (road alone; add time for viewpoint stops) | N222 — "93 bends," winding two-lane, named World's Best Road 2015 | This is the leg `CLAUDE.md` specifically calls out: 25 km that is not a 20-minute drive. Confirmed slow by design, not a routing error. `[likely]` |
| Peso da Régua | Lamego | ~11–16 km | **~13–19 min** | Short secondary road/bridge crossing, not the N222 | Fast; makes Régua↔Lamego a genuinely easy day-swap. `[likely]` |
| Douro (Régua/Pinhão area) | Vila do Gerês | ~130–140 km | **~1h45–2h30** — sources disagree, see note | Mixed: A-road/highway corridor via Amarante toward Braga, then mountain roads (N304/N308) into the park | Two independent estimates diverge: `research/nature.md` says ~1h45–1h50 (general Douro→park-boundary figure); a separate pass on this leg found ~1h59–2h10 door-to-door to Vila do Gerês specifically, and up to 2h30 if traffic/mountain-road conditions are unfavorable. **Treat as ~2h, not ~90 min** — this breaks the trip's "~90 min travel day" comfort guideline regardless of which estimate is right. `[estimate]` |
| Vila do Gerês | Porto Airport (OPO) | ~92 km | **~1h14–1h15** | Consistent both directions | Clean departure-day drive. `[likely]` |

**Flag to planner:** the Douro→Gerês transfer is the one leg in the whole trip that
cannot be squeezed under ~90 minutes no matter how it's routed. Per `trip/preferences.md`
scoring ("Drive time on a day > 2h: strong negative"), this day should carry **zero
anchor activities** — it's a transfer day, not a transfer-plus-quinta or
transfer-plus-hike day. A stop at a miradouro or café roughly midway is fine; a second
booked activity is not.

## 2. Within-day movement — general rules for the planner

No itinerary exists yet to check activity-by-activity, so these are standing rules
rather than day-specific flags:

- **Quinta tastings run 1.5–2h**, not the 45 min a schedule might assume — confirmed
  by `research/douro.md`'s Quinta do Crasto entry (~90 min guided tour+tasting) and
  general enoturismo practice. Build quinta slots as 2h blocks minimum, door to door.
- **N222-adjacent days**: any day pairing a Pinhão-side anchor with a Régua-side
  anchor (or vice versa) needs the ~45–60 min N222 drive built in on both legs, not
  treated as a quick hop — a quinta at 11:00 and a Régua lunch at 13:00 is workable;
  a quinta at 11:00 and a Régua lunch at 12:00 is not.
  Whichever pattern the planner ships, I'll check it against real place names next
  cycle once an itinerary with actual anchors exists.
- **Gerês trailheads** are themselves a further drive from Vila do Gerês (e.g. Ermida
  for the Arado/Poço Azul trail is ~8 km out) — budget 15–20 min each way from base to
  trailhead on top of the trail time itself, per `research/nature.md`.

## 3. Car rental

- **Automatic transmission**: manual is the overwhelming default in the Portuguese
  rental fleet (~80–90%); automatics are a minority and should be booked well ahead,
  especially for September (still high season). Price premium is inconsistently
  reported across sources — ranges from "slightly more" to roughly double for
  economy/compact classes. Budget for a **noticeably higher** rate than a manual quote
  and lock it in early. `[unverified — wide source disagreement, no single
  authoritative figure]`
  Sources: [drivetheatlas.com](https://drivetheatlas.com/automatic-car-rental-portugal/), [carflexi.com](https://www.carflexi.com/en-us/10h6rm1ztlv4y4/car-rental-automatic-in-portugal)
- **Estimated cost**: budget **€45–75/day** for a mid-size automatic in September;
  blended-average aggregator figures (~€24–35/day) are lower but likely skew toward
  manual/economy cars, not what this trip needs. `[estimate]`
- **Pickup/return location**: `research/porto.md` recommends picking up in the city at
  **Campanha train station** on the way out to the Douro (not at OPO on arrival) to
  avoid airport markup and Porto in-city parking during the walking days, then
  dropping back at the **airport** on departure day. This is already logged as an open
  question pending a chosen rental company — I concur with the routing logic; the
  Porto Airport→Régua leg above (~1h10) is the fallback if airport pickup is preferred
  instead.
- **Via Verde tolls**: Portugal's toll roads are electronic-only (no cash lanes on
  most). Rental companies typically either pre-fit a Via Verde transponder or offer it
  as an add-on that auto-bills tolls to the card on file after return — no separate
  device pickup needed in most cases. `[likely]`
  Source: [Hertz Portugal](https://www.hertz.pt/p/en/hertz-together/mandatory-e-toll-service-via-verde-for-renting-a-car)
- **Good news for this specific route**: the **A4 (Transmontana), including the Marão
  tunnel** — the fast Porto↔Douro highway used on the Porto→Pinhão and OPO→Régua legs
  above — became **toll-free for cars as of 1 January 2025** under Law No. 37/2024.
  This route carries no toll cost. `[confirmed]`
  Sources: [trans.info](https://trans.info/en/portugal-road-tolls-403177), [CiTTi Magazine](https://www.cittimagazine.co.uk/news/road-user-charging-tolling/portugal-ends-toll-charges-on-several-major-highways.html)
- **Fuel**: roughly €1.90/L petrol, €1.98/L diesel as of mid-2026 — noticeably higher
  than 2025 levels; budget at the current rate, not an older figure. `[unverified —
  single-pass search result, worth a spot-check closer to travel date]`
  Standard rental policy is full-to-full; avoid prepaid-tank options.
  Source: [fuel-prices.eu](https://www.fuel-prices.eu/Portugal/)

## 4. Drinking and driving — highest-value check

This is a wine trip built around quinta tastings, so this is the check that matters
most.

- **Legal limit**: 0.5 g/L BAC for regular drivers. **0.2 g/L** for drivers with
  **under 3 years' license experience** (also professional/learner drivers).
  `[confirmed]`
  Sources: [Holafly](https://esim.holafly.com/trip-planning/driving-portugal/), [ETSC fact file](https://etsc.eu/wp-content/uploads/SMART-COUNTRY-ANALYSIS_PORTUGAL_03.pdf)
- **Penalties**: 0.5–0.8 g/L → fine €250–1,250 + driving ban 1 month–1 year. 0.8–1.2
  g/L → fine €500–2,500 + longer ban. ≥1.2 g/L → criminal offence, up to 1 year
  imprisonment or a day-fine, 6 penalty points, possible license revocation.
  `[likely]` Source: [Advocate Abroad](https://advocateabroad.com/portugal/criminal-law/drink-driving-offences/)
- **Rough tasting math** (estimate, not a sourced medical figure — for flagging
  purposes only): a standard quinta tasting pours 3–5 samples of 30–50ml. Using the
  Widmark formula for a ~70–75kg adult, **roughly 3–5 tasting pours can put a person
  at or near 0.5 g/L**, and **1–2 pours can exceed the 0.2 g/L novice-driver limit**.
  Individual variation (body weight, sex, food, time elapsed) is large — treat this as
  "assume you're over the limit after any real tasting," not a precise threshold.
  `[estimate]`
- **Rule for the planner**: any day with **more than one tasting**, or any single
  tasting where the person driving is also the one tasting, needs one of:
  1. A **non-tasting designated driver** for that day (works if Ariel/Shani alternate
     tasting days), or
  2. A **transfer/driver service** for that specific quinta visit (many quintas offer
     or can arrange this, per harvest-season packages in `research/douro.md`), or
  3. **Walking/short-distance only** — a quinta genuinely within safe walking distance
     of the base (Pinhão has a few, per `research/douro.md`).
  **I will flag this explicitly under `## Logistics blockers` in `trip/critique.md`
  for any day the planner ships where two-taster, self-drive, multi-quinta days are
  implied** — this is exactly the kind of day-that-looks-fine-on-paper the itinerary
  needs to avoid.

## 5. Opening days

No real dates exist yet (`trip/facts.md` flights are still `TBD`), so nothing can be
checked against an actual day of the week this cycle. Flagging what's known in
general terms for cycle 2+ once dates land:

- Portuguese museums and many tourist sites commonly close **Mondays** — true broadly
  across Portugal, not confirmed per-site for anything in `research/porto.md`,
  `research/douro.md`, or `research/nature.md` yet. `[unverified — general pattern,
  not site-specific]`
- Quinta enoturismo operations (Crasto, Nova, Pacheca, Bomfim, Seixo, Tedo) are
  commercial wine-tourism operations and plausibly run 7 days/week in harvest season
  given the value of September visitors — but none of the four scout files confirm
  this. **Action for cycle 2**: once `scout-douro` or I confirm specific quinta
  websites, check weekly closure days directly.
- Gerês trailheads themselves have no "closure days" (they're open terrain), but
  visitor-facing infrastructure (park information centres, the Vilarinho das Furnas
  ethnographic museum) may have weekly closures — not checked this cycle.
- **This whole section is a placeholder** until `trip/facts.md` has real dates. Once
  it does, I'll cross-check every planned anchor against its actual weekday.

## 6. Trains and boats

- **Linha do Douro**: Porto (São Bento/Campanhã) → Pocinho, ~160 km / ~3h20
  end-to-end. The **Régua–Pinhão leg (~25 min)** is the scenic highlight — river-hugging
  track, widely called the most beautiful stretch. `[confirmed — operator + multiple
  independent sources agree, per `research/douro.md`]`
  Source: [CP — Linha do Douro](https://www.cp.pt/info/en/w/douro-historical)
- **How this works with a car**: the car stays wherever it's parked (Pinhão or Régua)
  — a car-plus-train day only works as an out-and-back from the same base, or if a
  second person drives the empty leg to pick up the train-riders at the other end.
  Given the ~26–45 min N222 drive is itself scenic, the highest-value pattern is
  **train one direction, drive back (or vice versa)** rather than a same-day round
  trip on the train alone — turns one transfer into two different experiences instead
  of doubling up. `[estimate — reasoning, not sourced]`
- **Rabelo boat trips**: depart from Pinhão, ~2h Pinhão–Tua–Pinhão round trips,
  several daily departures — self-contained, doesn't interact with the car/train
  question. `[likely]` Source: [roteirododouro.com](https://www.roteirododouro.com/en/experience/cruise-regua-pinhao-historic-train)

## 7. September specifics

- **Sunset times**: could not source an exact day-by-day table this cycle (primary
  sun-time sites were unreachable). Directionally: Portugal stays on WEST (UTC+1)
  through September (DST ends late October), and sunset shortens meaningfully across
  the month — roughly from the low-to-mid 20:00s in early September to
  **~19:20–19:40 by month-end**, a decrease on the order of 45–70 minutes over the
  month. **Do not schedule evening activities (sunset miradouro visits, evening
  village walks) against a fixed clock time without checking the actual date first**
  — a plan that works Sept 5 may not work Sept 28. `[unverified — flagging for a
  direct check once real travel dates exist in `trip/facts.md`]`
- **Temperatures**: Douro daytime highs ~25–26°C, overnight lows ~13–14.5°C, ~47mm
  rain for the month. Gerês similar — highs ~26°C, lows ~13°C, ~13% chance of rain on
  a given day. Comfortable for both wine-tasting outdoor time and hiking; still warm
  enough that harvest picking (per `research/douro.md`) happens in the morning to
  avoid midday heat. `[likely]`
  Sources: [climate-data.org Douro](https://en.climate-data.org/europe/portugal/douro-10393/r/september-9/), [Wanderlog Peneda-Gerês](https://wanderlog.com/weather/22531/9/peneda-geres-national-park-weather-in-september)
- **Harvest-season traffic/availability**: not independently checked this cycle
  beyond what `research/douro.md` already covers (booking urgency for vindima
  experiences). No specific road-traffic data found for harvest season in the Douro —
  worth a targeted check in `refine` if the itinerary ends up routing through Pinhão
  on a weekend in peak harvest weeks.

## Cycle 2 (evening) — checking the itinerary day-by-day

`trip/itinerary.md` now exists (13-day skeleton, cycle 1). This cycle checks it against
the matrix above, focused on the item `critic` flagged for me by name: Day 6.

### Day 6 correction — Pinhão→Lamego is NOT the ~45–60 min the itinerary claims

The itinerary's Day 6 gives "~45–60 min" for the whole Pinhão→Lamego leg with a
São Salvador do Mundo stop folded in. This is wrong on two counts:

- **Direct Pinhão→Lamego** (no detour): **~32–36 min / ~36–38 km** on the
  Pinhão↔Régua↔Lamego corridor. `[likely]` — this is actually *faster* than my
  cycle-1 matrix implied (I only had the leg broken into
  Pinhão→Régua + Régua→Lamego, ~58–79 min summed); a more direct routing exists that
  doesn't fully retrace through central Régua. Source:
  [rome2rio](https://www.rome2rio.com/s/Pinhao-Portugal/Lamego).
- **The São Salvador do Mundo miradouro is not en route.** It sits ~5 km outside
  **São João da Pesqueira**, which is on the **south bank of the Douro**, reached by
  crossing at the Barragem da Valeira — geographically off to the side of the
  Pinhão↔Régua↔Lamego corridor, which stays on the north side of the river. Régua↔São
  João da Pesqueira alone is **~43 km** — a proxy for how far off-corridor this stop
  sits. `[likely]` Sources:
  [Mapcarta](https://mapcarta.com/36121244),
  [CM São João da Pesqueira](https://www.sjpesqueira.pt/pages/1404?poi_id=202),
  [itinerarios-mapa.com](https://www.itinerarios-mapa.com/peso-da-regua-sao-joao-da-pesqueira).
- **Net effect:** routing Pinhão→São Salvador do Mundo→Lamego is a genuine
  out-and-back-style detour, not a "stop on the way." Estimating from the leg
  distances above, drive time alone (excluding the stop itself) is more like
  **~70–90 min**, not 45–60 — an added **~40–55 min of driving** versus the honest
  direct route, on top of the viewpoint stop (~10–15 min) and everything else Day 6
  already carries (lunch, sanctuary steps, old-town wander). `[estimate — built from
  the two confirmed-adjacent leg distances, not a single routed door-to-door query]`

**Confirms `critic`'s 🔴 flag.** My recommendation, logged to
`trip/critique.md` under Logistics blockers: **drop the São Salvador do Mundo stop
from Day 6** and use the honest **~32–36 min direct drive**, which then comfortably
clears the ~90-min travel-day guideline with lunch + sanctuary + wander still fitting
a "medium pace" day. If Ariel wants that specific viewpoint, it's a better fit as a
half-day add-on from a Régua/Lamego-based day (still a real detour, but one that
isn't also stacked onto a transfer day) — not something to solve by picking a
different day within Douro without discussing it with `scout-douro`/`planner`.

### Day 4 check — Quinta do Crasto hours

Quinta do Crasto's reception/wine shop runs **10:00–18:00 daily** — no weekly closure
found. `[likely]` Source:
[quintadocrasto.wine](https://www.quintadocrasto.wine/en/wine-tourism/). This
supports the itinerary's Day 4 timing (morning walk, early-afternoon tasting) without
needing a weekday check once real dates land — but I could not confirm Quinta da
Pacheca's (Day 7) hours this cycle; still open per opening-days section below.

### Day 12 — Porto overnight parking (flagged by `critic`, not previously priced)

`critic` correctly noted Day 12 drives the rental car back into Porto for one night
with no parking plan. Rough Porto city-centre parking: **hotel garage ~€15–25/night**,
or a cheaper shopping-centre garage near Cedofeita/Aliados (e.g. Via Catarina, **~€9
for 24h**) if the hotel doesn't offer parking. `[estimate — general Porto rates, not
checked against a specific Cedofeita hotel]` Not a blocker — just a ~€10–25 line item
the planner should note rather than leave silent. Source:
[auto-jardim.com](https://auto-jardim.com/parking-in-porto/).

### Drink-and-driving — Days 4 and 7 checked against my §4 rule

The itinerary's Day 4 and Day 7 text already implements my standing rule from cycle 1
(alternate taster/driver across the two tasting days, or use a quinta transfer) almost
verbatim. **No new blocker** — this is the one place the itinerary is ahead of what I
asked for. It remains a *structural suggestion*, not an assignment of which person
drives which day; that's rightly logged as open in `trip/itinerary.md`'s "Still soft."

### Opening days — still a placeholder

No real calendar dates exist yet (`trip/facts.md` flights still `TBD`), so nothing
else can be checked against an actual weekday this cycle. Carrying forward from
cycle 1.

## Changed this cycle

- First research pass (cycle 1, explore). Built the full drive-time matrix for every
  base-to-base leg implied by the scout recommendations (Porto, Pinhão, Régua/Lamego,
  Vila do Gerês, OPO).
- Flagged the Douro→Gerês leg as running **~2h, not the ~90 min guideline** —
  recommend the planner treat that day as a zero-anchor transfer day.
- Did the drink-and-drive math explicitly: 3–5 tasting pours can reach the 0.5 g/L
  limit, 1–2 pours can exceed the 0.2 g/L novice limit. Set a standing rule for the
  planner (designated driver / transfer / walking-only quinta) rather than a
  day-specific flag, since no itinerary exists yet to check.
- Confirmed the A4/Marão tunnel corridor (the main Porto↔Douro route) is toll-free as
  of Jan 2026 — no Via Verde cost on the core route.
- Opening-days section is a placeholder pending real dates in `trip/facts.md`.
- No entries added to `trip/critique.md` this cycle — there is no itinerary yet to
  veto. Will check day-by-day starting next cycle once `planner` produces one.

## Changed cycle 2

- Checked the cycle-1 itinerary day-by-day for the first time. Confirmed
  `critic`'s Day 6 flag: the itinerary's "~45–60 min" Pinhão→Lamego figure is wrong
  in both directions — the honest **direct** drive is faster (~32–36 min) than my own
  cycle-1 summed estimate suggested, but the **São Salvador do Mundo stop is a real
  detour** (south bank, off-corridor) that adds ~40–55 min of driving on top of that,
  not folded into a quick "on the way" stop as the itinerary implies. Logged to
  `trip/critique.md` under Logistics blockers with a concrete fix.
- Confirmed Quinta do Crasto's hours (10:00–18:00 daily, no closure day found) —
  supports Day 4's timing.
- Priced Day 12's previously-unaddressed Porto overnight parking (~€9–25/night) —
  not a blocker, flagged as a line item.
- Checked Days 4 and 7 against my own drink-and-driving rule from cycle 1: the
  itinerary already implements it correctly. No blocker.
- Opening-days section remains a placeholder — no real dates yet.

## Cycle 2 (morning) — the itinerary is missing its own second half

### 🔴 The itinerary still ends in Porto. It must end in Lisbon.

`trip/itinerary.md` (13 days, cycle 1) has **no campervan leg and no coastal days at
all** — Day 13 is "Gaia, then home," flying out of **OPO**. But `trip/facts.md`
§Route is explicit and `[confirmed]`: step 4 is a **5–6 day campervan leg**
(Porto → Aveiro/Figueira da Foz → Peniche/Baleal → Ericeira → Lisbon) and step 5 is
**"Fly home from Lisbon (LIS) `[confirmed]` — open-jaw ticket."** `CLAUDE.md` itself
carries a standing warning about exactly this mistake: *"An earlier version of this
repo assumed the trip ended in Porto with no coastal leg. That was wrong, and cycle
1's itinerary was built on it."* That warning has not been acted on — cycle 1's
itinerary reproduces the same error it was written to prevent.

This is a logistics problem, not just a content gap: as currently written, the plan
has **no van, no coast, no way home** — the return flight in the itinerary departs
from the wrong airport entirely. I'm raising this under Logistics blockers because it
sits squarely in my domain (item 3 of my brief: work out the car/van handover and the
one-way route) and because a plan that departs from the wrong city isn't a "day that's
full," it's a day that's impossible.

**This error has also contaminated research, not just the itinerary.** `research/nature.md`
(cycle 2, the same cycle `research/coast.md` confirmed the Porto→Lisbon van route is
real) explicitly rejects an alternative Gerês exit route as "too far out of the way
for a trip that ends by flying out of Porto" — still assuming the old, wrong
endpoint. `research/porto.md`'s departure-day car-rental advice ("drop the rental car
at the airport on departure day... since that's a same-day flight-out anyway") also
assumes Porto is the last leg. **Recommend the planner/critic flag `scout-nature` and
`scout-porto` to re-check any recommendation keyed to "the trip ends in Porto"** —
mine is not the only file that needs a pass.

### Car/van handover — proposed plan

Per my brief item 3, working out where the car goes back and where the van is
collected:

- **Car**: picked up at Campanha (Porto) on the way out to the Douro (per
  `research/porto.md`), used through Douro + Gerês, **returned in Porto** — not at
  the airport, since the airport dropoff only made sense under the old
  Porto-departure assumption. Likely the same Campanha depot or another city-centre
  location; an airport detour no longer serves any purpose. `[estimate — depends on
  chosen rental company's Porto depots]`
- **Handover day**: `research/nature.md` confirms the Gerês→Porto exit leg is the
  **short** direction, ~1h15 (vs. ~1h45–1h50 inbound) — so the day the Gerês leg ends
  is a reasonable one to also do the car→van swap **and** reach the first coastal
  stop (Aveiro), *if* the swap itself doesn't eat too much of the day. Budget:
  - Vila do Gerês → Porto: ~1h15
  - Car return + van pickup (inspection, paperwork, walkthrough on an unfamiliar
    vehicle): **~1–2h** `[estimate — not sourced, but campervan pickups routinely
    include a systems walkthrough (water, power, gas) that a car return doesn't]`
  - Porto → Aveiro (first coastal stop): ~1h `[estimate, ~70 km via A1]`
  - **Total ~3.5–4.5h of driving-plus-admin** — doable as a single travel day, but
    only if it carries **no other anchor**, same logic as the Douro→Gerês day.
  - **Alternative worth flagging**: split it — return the car and overnight in
    Porto, collect the van fresh the next morning, then drive to Aveiro. Costs a
    day but removes all admin-under-time-pressure risk. This is a genuine
    day-count-vs-risk trade-off, not something I can decide — flagging to
    `trip/open-questions.md` rather than picking one.
- **Van**: confirmed possible one-way Porto→Lisbon per `research/coast.md` (Indie
  Campers, Yescapa, Roadsurfer, Portugal by Van, Camper Line) — the "critical
  unknown" from my brief item 3 resolves as **feasible**, not a blocker. Still
  open: an actual September 2026 quote and company choice (already in
  `trip/open-questions.md`).
- **Van size**: `research/coast.md` recommends a compact, VW-transporter-class van
  over a boxy Class C motorhome for Portuguese village streets and coastal
  parking. I concur on pure drivability grounds — narrow N222-style roads aren't
  unique to the Douro, and Ericeira's "compact whitewashed centre" (per
  `research/coast.md`) is exactly the kind of street a larger van will struggle to
  park on.

### Coastal-leg drive-time matrix (new — no itinerary days exist yet to check)

`research/coast.md` covers the stops in depth but doesn't give leg-by-leg drive
times, so I'm building the matrix now, ahead of the planner needing it:

| From | To | Distance | Realistic drive | Road | Notes |
|---|---|---|---|---|---|
| Porto | Aveiro | ~70 km | **~1h** | A1 (motorway) | Fast; treat Aveiro as the half-day stop `research/coast.md` recommends, not a base. `[estimate]` |
| Aveiro | Figueira da Foz | ~45 km | **~40–45 min** | A17/N109 coastal corridor | If Figueira is skipped per `research/coast.md`'s recommendation, this leg doesn't happen — flagged for completeness only. `[estimate]` |
| Aveiro (or Figueira da Foz) | Peniche/Baleal | ~135–150 km | **~1h40–2h** | A17→A8 | The longest single coastal-leg drive — comparable to the Porto→Pinhão Douro transfer. Should be the day's only real driving commitment. `[estimate]` |
| Peniche/Baleal | Ericeira | ~35 km | **~35–40 min** | N247 (coast road, curves through small towns, not a straight motorway hop) | Short enough to clear the ≥2-night minimum comfortably. `[estimate]` |
| Ericeira | Lisbon | ~35 km | **~40–50 min** | N247→A21, or coastal N247 if avoiding the motorway | Clean, short final approach — supports `research/coast.md`'s suggestion of a last night *in* Lisbon rather than vanning it to the airport same-day. `[estimate]` |

**All rows `[estimate]`** — built from general road-network knowledge, not a routed
door-to-door query; worth a spot-check once the planner drafts actual coastal days.

### What this means for the planner

- The itinerary needs **new days appended after the current Day 13** (or Day 13
  reworked entirely) covering: the car/van handover day, Aveiro, Peniche/Baleal
  (≥2 nights), Ericeira (≥2 nights), and a Lisbon end — not a Porto flight home.
- This is a **structural fix**, appropriate for `explore` phase, not a small diff —
  logging it as a blocker rather than a "consider" because the current itinerary
  doesn't just have a gap, it actively contradicts `trip/facts.md`.

## Changed this cycle (cycle 2 morning)

- Found and flagged the itinerary's biggest feasibility gap: no coastal/campervan
  leg exists, and the plan as written flies home from the wrong airport (Porto
  instead of the confirmed Lisbon open-jaw). Traced the same wrong assumption into
  `research/nature.md` and `research/porto.md`, both still written as if Porto were
  the last leg.
- Proposed a car/van handover plan (Porto return, ~3.5–4.5h swap-day budget,
  compact van recommended for village streets) and flagged the day-count-vs-risk
  trade-off (same-day swap vs. an overnight buffer) as a human decision.
- Built the first coastal drive-time matrix (Porto→Aveiro→Figueira da
  Foz→Peniche/Baleal→Ericeira→Lisbon) — all `[estimate]`, ahead of any coastal days
  existing in the itinerary to check them against.
- Logged this to `trip/critique.md` under Logistics blockers and added a note to
  `trip/open-questions.md`'s existing car/van handover question.
