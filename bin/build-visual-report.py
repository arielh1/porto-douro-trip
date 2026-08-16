#!/usr/bin/env python3
"""Build a visual HTML digest for the current trip using repository evidence only."""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parent.parent
FACTS = ROOT / "trip" / "facts.md"
PREFERENCES = ROOT / "trip" / "preferences.md"
ITINERARY = ROOT / "trip" / "itinerary.md"
QUESTIONS = ROOT / "trip" / "open-questions.md"
RESEARCH_DIR = ROOT / "research"
STAYS_DIR = ROOT / "stays"
LOG = ROOT / "state" / "convergence.jsonl"
OUT_HTML = ROOT / "state" / "visual-report.html"
OUT_TXT = ROOT / "state" / "visual-report.txt"


@dataclass
class Place:
    name: str
    area: str
    category: str
    why: str
    confidence: str
    source_label: str
    source_url: str
    review_url: str | None = None
    image_urls: list[str] | None = None


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def latest_cycle_info() -> dict:
    if not LOG.exists():
        return {}
    lines = [l for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    return json.loads(lines[-1]) if lines else {}


def maps_url(query: str) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"


def clean_md(text: str) -> str:
    text = re.sub(r"\[(confirmed|likely|unverified|estimate)(?:[^\]]*)?\]", "", text, flags=re.I)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return " ".join(text.split()).strip()


def extract_table_rows(md: str, heading: str) -> list[list[str]]:
    m = re.search(rf"##\s*{re.escape(heading)}\s*\n((?:\|.*\|\n)+)", md)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and not all(set(c) <= {"-"} for c in cells):
            rows.append(cells)
    if len(rows) >= 2:
        return rows[2:] if rows[1][0].startswith("---") or set(rows[1][0]) <= {"-"} else rows[1:]
    return []


def extract_named_section(md: str, title: str) -> str:
    m = re.search(rf"###\s*{re.escape(title)}\s*\n(.*?)(?=\n### |\n## |\Z)", md, re.S)
    return clean_md(m.group(1)) if m else ""


def first_url(text: str) -> str | None:
    m = re.search(r"https?://[^\s),]+", text)
    return m.group(0) if m else None


def first_review_url(text: str) -> str | None:
    m = re.search(r"https?://[^\s),]*(tripadvisor|booking|winalist|getyourguide|thefork)[^\s),]*", text, re.I)
    return m.group(0) if m else None


def parse_douro(md: str) -> list[Place]:
    places: list[Place] = []
    for row in extract_table_rows(md, "Quintas")[:4]:
        if len(row) < 7:
            continue
        name, area, experience, _booking, _cost, source, confidence = row[:7]
        urls = re.findall(r"https?://[^\s,]+", source)
        places.append(
            Place(
                name=name,
                area=area,
                category="Quinta / winery",
                why=clean_md(experience),
                confidence=confidence,
                source_label="Douro research",
                source_url=urls[0] if urls else maps_url(f"{name} {area} Portugal"),
                review_url=first_review_url(source),
                image_urls=urls[:2],
            )
        )
    for title in ["Provesende (Quinta Manhas Douro) — new candidate this cycle, upgraded from \"day-trip only\"", "Pinhão"]:
        section = extract_named_section(md, title)
        if section:
            name = "Quinta Manhas Douro" if "Quinta Manhas Douro" in title else "Pinhão"
            places.append(
                Place(
                    name=name,
                    area="Douro",
                    category="Stay / base candidate" if "Quinta" in name else "Village base",
                    why=section.split("Source:")[0][:280].strip(),
                    confidence="[likely]",
                    source_label="Douro research",
                    source_url=first_url(section) or maps_url(f"{name} Douro Portugal"),
                    review_url=first_review_url(section),
                    image_urls=re.findall(r"https?://[^\s,]+", section)[:2],
                )
            )
    return places


def parse_porto(md: str) -> list[Place]:
    places: list[Place] = []
    for row in extract_table_rows(md, "Food")[:4]:
        if len(row) < 6:
            continue
        name, category, why, _reservation, source, confidence = row[:6]
        urls = re.findall(r"https?://[^\s)]+", source)
        places.append(
            Place(
                name=name.replace("~~", ""),
                area="Porto",
                category=f"Restaurant / {category}",
                why=clean_md(why),
                confidence=confidence,
                source_label="Porto research",
                source_url=urls[0] if urls else maps_url(f"{name} Porto Portugal"),
                review_url=first_review_url(source),
                image_urls=urls[:1],
            )
        )
    return places


def parse_nature(md: str) -> list[Place]:
    places: list[Place] = []
    waterfall_copy = extract_named_section(md, "Swimming & waterfalls")
    if waterfall_copy:
        for name in ["Poço Azul", "Cascata do Arado", "Cascata do Tahiti"]:
            if name in waterfall_copy:
                places.append(
                    Place(
                        name=name,
                        area="Peneda-Gerês",
                        category="Nature / waterfall",
                        why=waterfall_copy[:320],
                        confidence="[likely]" if name != "Poço Azul" else "[unverified]",
                        source_label="Nature research",
                        source_url=first_url(waterfall_copy) or maps_url(f"{name} Geres Portugal"),
                        review_url=None,
                        image_urls=re.findall(r"https?://[^\s,]+", waterfall_copy)[:2],
                    )
                )
    return places


def parse_coast(md: str) -> list[Place]:
    places: list[Place] = []
    for name, area in [
        ("ASA Peniche", "Peniche/Baleal"),
        ("Bar do Bruno", "Baleal"),
        ("Prainha / Amigos do Baleal", "Baleal"),
        ("Ericeira Camping & Bungalows", "Ericeira"),
        ("Mar D'Areia", "Ericeira"),
        ("Tasca do Joel", "Ericeira"),
    ]:
        match = re.search(rf"{re.escape(name)}.*", md)
        if match:
            line = clean_md(match.group(0))
            urls = re.findall(r"https?://[^\s)]+", line)
            places.append(
                Place(
                    name=name,
                    area=area,
                    category="Camper stop" if "Camping" in name or "ASA" in name else "Restaurant / coast",
                    why=line[:280],
                    confidence="[likely]" if "[unverified]" not in line else "[unverified]",
                    source_label="Coast research",
                    source_url=urls[0] if urls else maps_url(f"{name} {area} Portugal"),
                    review_url=first_review_url(line),
                    image_urls=urls[:1],
                )
            )
    return places


def parse_itinerary_highlights(md: str) -> list[str]:
    rows = extract_table_rows(md, "At a glance")
    return [f"{row[1]} — {row[2]} — {row[3]}" for row in rows[:8] if len(row) >= 4]


def build() -> None:
    facts_md = read(FACTS)
    preferences_md = read(PREFERENCES)
    itinerary_md = read(ITINERARY)
    questions_md = read(QUESTIONS)
    cycle = latest_cycle_info()

    places = (
        parse_douro(read(RESEARCH_DIR / "douro.md"))
        + parse_porto(read(RESEARCH_DIR / "porto.md"))
        + parse_nature(read(RESEARCH_DIR / "nature.md"))
        + parse_coast(read(RESEARCH_DIR / "coast.md"))
    )

    seen: set[tuple[str, str]] = set()
    deduped: list[Place] = []
    for place in places:
        key = (place.name, place.area)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(place)

    highlights = parse_itinerary_highlights(itinerary_md)
    phase = cycle.get("phase", "explore")
    stability = int(cycle.get("similarity", 0) * 100)
    today = datetime.now(timezone.utc).strftime("%d.%m.%Y")
    trip_dates = re.search(r"\*\*Dates:\*\*.*?(\d{1,2}.*?2026.*?27 September 2026)", itinerary_md)
    trip_window = trip_dates.group(1) if trip_dates else "11–27 September 2026"

    cards = []
    for place in deduped:
        imgs = ""
        for url in (place.image_urls or [])[:2]:
            if re.search(r"\.(jpg|jpeg|png|webp|avif)(\?|$)", url, re.I):
                imgs += f'<img src="{html.escape(url)}" alt="{html.escape(place.name)}" loading="lazy">'
        links = [
            f'<a href="{html.escape(maps_url(place.name + " " + place.area + " Portugal"))}">Google Maps</a>',
            f'<a href="{html.escape(place.source_url)}">Source</a>',
        ]
        if place.review_url:
            links.append(f'<a href="{html.escape(place.review_url)}">Reviews</a>')
        cards.append(
            f"""
            <article class="card">
              <div class="meta"><span>{html.escape(place.category)}</span><span>{html.escape(place.area)}</span></div>
              <h3>{html.escape(place.name)}</h3>
              <p class="why">{html.escape(place.why)}</p>
              <p class="confidence">{html.escape(place.confidence)}</p>
              <div class="images">{imgs}</div>
              <div class="links">{' · '.join(links)}</div>
            </article>
            """
        )

    question_items = re.findall(r"-\s*\[ \]\s*\*\*(.+?)\*\*", questions_md)
    question_html = "".join(f"<li>{html.escape(q)}</li>" for q in question_items[:5])
    highlight_html = "".join(f"<li>{html.escape(item)}</li>" for item in highlights)

    html_out = f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Portugal visual digest</title>
  <style>
    body {{ margin:0; background:#f5f1eb; color:#2a241f; font-family:-apple-system,'Segoe UI',Arial,sans-serif; }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:24px 16px 48px; }}
    .hero {{ background:linear-gradient(135deg,#5b2c3b,#8d5c3d); color:#fff; border-radius:18px; padding:24px; }}
    .hero h1 {{ margin:0 0 8px; font-size:28px; }}
    .hero p {{ margin:6px 0; line-height:1.6; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:16px; margin-top:18px; }}
    .card {{ background:#fff; border-radius:16px; padding:16px; box-shadow:0 2px 10px rgba(0,0,0,.06); }}
    .card h3 {{ margin:10px 0 8px; font-size:20px; }}
    .meta, .links, .confidence {{ font-size:13px; color:#7a6758; }}
    .meta {{ display:flex; justify-content:space-between; gap:12px; }}
    .why {{ line-height:1.6; }}
    .images {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:12px 0; }}
    .images img {{ width:100%; height:170px; object-fit:cover; border-radius:12px; background:#eee; }}
    .section {{ margin-top:18px; background:#fff; border-radius:16px; padding:18px; box-shadow:0 2px 10px rgba(0,0,0,.05); }}
    a {{ color:#7b2f42; text-decoration:none; }}
    ul {{ margin:8px 0 0; padding-right:20px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>דוח ויזואלי לטיול בפורטוגל</h1>
      <p><b>חלון הטיול:</b> {html.escape(trip_window)}</p>
      <p><b>שלב:</b> {html.escape(phase)} · <b>יציבות:</b> {stability}%</p>
      <p>המטרה כאן היא לראות בעיניים את המקומות שהטיול כבר מתכנס אליהם: יקבים ולינה פוטנציאלית, מסעדות טובות, ומקומות טבע כמו מפלים — עם קישורים למפות ולביקורות אמיתיות.</p>
    </section>

    <section class="section">
      <h2>מה כבר מסתמן בלוז</h2>
      <ul>{highlight_html}</ul>
    </section>

    <section class="section">
      <h2>מקומות שכדאי להסתכל עליהם עכשיו</h2>
      <div class="grid">
        {''.join(cards)}
      </div>
    </section>

    <section class="section">
      <h2>שאלות פתוחות לפני שסוגרים</h2>
      <ul>{question_html or '<li>כרגע אין שאלות פתוחות בדוח הזה.</li>'}</ul>
    </section>

    <section class="section">
      <h2>הערת אמינות</h2>
      <p>הדוח הזה נבנה רק מהמידע שכבר קיים בריפו: itinerary, research, stays. אם אין תמונה או קישור ביקורות ישיר למקום מסוים, הוא נשאר בלי זה במקום להמציא.</p>
      <p><b>נוצר:</b> {today}</p>
    </section>
  </div>
</body>
</html>"""

    text_out = "\n".join(
        [
            f"דוח ויזואלי לטיול בפורטוגל — {today}",
            f"שלב: {phase} · יציבות: {stability}%",
            "",
            "Highlights:",
            *highlights[:8],
            "",
            "Places:",
            *[f"- {p.name} ({p.area}) — {p.category}" for p in deduped[:12]],
        ]
    )

    OUT_HTML.write_text(html_out, encoding="utf-8")
    OUT_TXT.write_text(text_out, encoding="utf-8")
    top = ", ".join(p.name for p in deduped[:5])
    print(f"wrote {OUT_HTML} ({len(deduped)} places)")
    print(f"highlights: {top}")


if __name__ == "__main__":
    build()
