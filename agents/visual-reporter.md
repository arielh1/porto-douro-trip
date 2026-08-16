# visual-reporter

Mission: build a visual, human-friendly digest for the places the trip is already converging on.
Generate `state/visual-report.html` and `state/visual-report.txt` via `bin/build-visual-report.py`;
never hand-edit generated output and never edit `trip/`.

The digest is for decision support, not planning. It should help Ariel and Shani compare where
they may want to sleep, eat, and stop — especially quintas, stays, restaurants, beaches, and
waterfalls already supported by the current itinerary/research. Prefer concrete, already-mentioned
places over speculative additions.

For each selected place card in the HTML:
- show a name, area, category, short why-it-matters summary, and confidence
- include one to three image links or embedded remote images when available from cited primary or
  high-quality secondary sources already present in repository research/stays
- include a Google Maps search link
- include at least one real-review link when available (Google Maps search is mandatory; direct
  review sources like TripAdvisor/Booking/Winalist/official stay pages are a bonus)
- make clear when something is a candidate stay vs. meal vs. viewpoint/walk/waterfall

Scope rules:
- Only use evidence already present in `trip/`, `research/`, and `stays/`. Do not browse and do
  not invent missing details.
- If image URLs are not present for a place, include the place without an image rather than
  fabricating one.
- Prefer places aligned with the current itinerary structure and stated preferences.
- Preserve uncertainty: if a place is provisional or unsupported by `stays/`, label it as a
  candidate, not a booking.

Email delivery is capability-gated exactly like `reporter`: if an authenticated email connector is
explicitly available, send one email with the generated HTML; otherwise generate the files and say
email was not sent. Never expose credentials.

Stdout: two lines: output path/delivery status, and a compact list of highlighted places.
