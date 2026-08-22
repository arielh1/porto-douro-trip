#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a single-page Hebrew HTML report from trip/itinerary.md + trip/open-questions.md.
Writes state/report.html and state/report.txt (plain-text fallback for the email body).

Used by the `reporter` agent every run, and safe to run standalone.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITINERARY = ROOT / "trip" / "itinerary.md"
QUESTIONS = ROOT / "trip" / "open-questions.md"
LOG = ROOT / "state" / "convergence.jsonl"
OUT_HTML = ROOT / "state" / "report.html"
OUT_TXT = ROOT / "state" / "report.txt"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def parse_at_a_glance(md: str):
    m = re.search(r"## At a glance\s*\n\|.*\|\n\|[-\s|]+\|\n((?:\|.*\|\n?)+)", md)
    rows = []
    if not m:
        return rows
    for line in m.group(1).strip().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and not cells[0].startswith("-"):
            rows.append(cells)
    return rows


def parse_status(md: str) -> str:
    m = re.search(r"\*\*Status:\*\*\s*(.+)", md)
    return m.group(1).strip() if m else ""


def parse_changelog_latest(md: str) -> str:
    m = re.findall(r"\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*(.+?)\s*\|\s*$", md, re.M)
    return m[-1][1] if m else ""


def parse_open_questions(md: str, max_items=5):
    items = []
    for heading, emoji in [("🔴 Blocking", "🔴"), ("🟠 Important", "🟠"), ("🟡 Nice to resolve", "🟡")]:
        block = re.search(rf"##\s*{re.escape(emoji)}.*?(?=\n##|\Z)", md, re.S)
        if not block:
            continue
        for m in re.finditer(r"-\s*\[ \]\s*\*\*(.+?)\*\*\s*(.*?)(?=\n- \[|\n##|\Z)", block.group(0), re.S):
            title, body = m.group(1).strip(), m.group(2).strip()
            first_line = body.split("\n")[0].strip()
            items.append((emoji, title, first_line))
            if len(items) >= max_items:
                return items
    return items


def latest_cycle_info():
    if not LOG.exists():
        return {}
    lines = [l for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    return json.loads(lines[-1]) if lines else {}


def build():
    it_md = read(ITINERARY)
    q_md = read(QUESTIONS)
    cycle = latest_cycle_info()

    rows = parse_at_a_glance(it_md)
    status = parse_status(it_md)
    latest_change = parse_changelog_latest(it_md)
    questions = parse_open_questions(q_md)

    total_days = len(rows)
    stability = cycle.get("similarity", 0)
    phase = cycle.get("phase", "explore")
    phase_he = {"explore": "בבנייה ראשונית", "refine": "מתחדד",
                "lock": "כמעט סופי", "converged": "סופי ✅"}.get(phase, phase)

    today = datetime.now(timezone.utc).strftime("%d.%m.%Y")

    day_rows_html = "\n".join(
        f"""<tr>
              <td class="d">{r[0]}</td>
              <td class="dt">{r[1]}</td>
              <td class="b">{r[2]}</td>
              <td class="a">{r[3]}</td>
            </tr>""" for r in rows
    )

    q_html = ""
    if questions:
        items = "\n".join(
            f'<li><span class="qflag">{e}</span> <b>{t}</b><br><span class="qbody">{b}</span></li>'
            for e, t, b in questions
        )
        q_html = f"""
        <div class="card">
          <div class="card-title">💬 כמה שאלות קצרות</div>
          <ul class="qlist">{items}</ul>
          <p class="hint">אפשר פשוט לענות על המייל הזה.</p>
        </div>"""

    stay_html = """
  <div class="card stay-card">
    <div class="card-title">🏡 לינה בפורטו — מועמדת, עדיין לא הוזמנה</div>
    <div class="stay-name">Gallery Townhouse &amp; Home · 11–13.9</div>
    <p class="stay-copy">חדר אחרון: <b>Standard Suite</b> · €327.25 לשני לילות / €163.63 ללילה<br>
    כ־₪1,143 לשהות / כ־₪571 ללילה <span class="estimate">(הערכת ECB)</span></p>
    <p class="stay-warning"><b>חשוב לפני הזמנה:</b> הצ׳ק־אין המפורסם מסתיים ב־00:00, והטיסה נוחתת ב־23:25. צריך אישור כתוב לצ׳ק־אין אחרי חצות לפני שמזמינים.</p>
    <p class="stay-note">לא מתאימה ל־21–22.9: במלון יש מינימום שני לילות.</p>
    <a class="stay-link" href="https://www.booking.com/hotel/pt/gallery-townhouse-amp-home.en-gb.html">לפרטי ההזמנה והקישור הישיר ›</a>
  </div>"""

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, 'Segoe UI', Arial, sans-serif; background:#f4f1ec;
         margin:0; padding:0; color:#2b2420; }}
  .wrap {{ max-width:600px; margin:0 auto; padding:20px 16px 40px; }}
  .header {{ background:linear-gradient(135deg,#6b2b3a,#8a3b4a); color:#fff; border-radius:14px;
             padding:22px 20px; margin-bottom:16px; }}
  .header h1 {{ margin:0 0 6px; font-size:20px; }}
  .header .sub {{ font-size:13px; opacity:.9; }}
  .progress {{ margin-top:14px; background:rgba(255,255,255,.25); border-radius:8px; height:8px; overflow:hidden; }}
  .progress-bar {{ height:100%; background:#f2c14e; border-radius:8px; }}
  .progress-label {{ font-size:11px; margin-top:6px; opacity:.85; }}
  .card {{ background:#fff; border-radius:14px; padding:16px 18px; margin-bottom:14px;
           box-shadow:0 1px 3px rgba(0,0,0,.06); }}
  .card-title {{ font-size:15px; font-weight:700; margin-bottom:10px; color:#6b2b3a; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  td {{ padding:6px 4px; border-bottom:1px solid #f0ece4; vertical-align:top; }}
  td.d {{ color:#a9915f; font-weight:700; width:24px; }}
  td.dt {{ color:#888; width:64px; white-space:nowrap; }}
  td.b {{ font-weight:600; width:100px; }}
  td.a {{ color:#444; }}
  ul.qlist {{ list-style:none; padding:0; margin:0; }}
  ul.qlist li {{ padding:10px 0; border-bottom:1px solid #f0ece4; font-size:13.5px; }}
  ul.qlist li:last-child {{ border-bottom:none; }}
  .qflag {{ font-size:14px; }}
  .qbody {{ color:#666; font-size:12.5px; }}
  .hint {{ font-size:11.5px; color:#999; margin:10px 0 0; }}
  .whats-new {{ font-size:13.5px; line-height:1.6; color:#3a332c; }}
  .stay-card {{ border:1px solid #ead9b9; }}
  .stay-name {{ font-weight:700; font-size:14px; color:#40342d; }}
  .stay-copy {{ margin:7px 0; font-size:13px; line-height:1.55; }}
  .estimate {{ color:#777; font-size:12px; }}
  .stay-warning {{ margin:9px 0; padding:9px 10px; background:#fff4e4; border-radius:8px;
                   color:#754b16; font-size:12.5px; line-height:1.55; }}
  .stay-note {{ margin:7px 0; color:#666; font-size:12.5px; }}
  .stay-link {{ display:inline-block; margin-top:3px; color:#6b2b3a; font-size:13px; font-weight:700; }}
  .footer {{ text-align:center; font-size:11px; color:#aaa; margin-top:18px; }}
</style>
</head>
<body>
<div class="wrap">

  <div class="header">
    <h1>הטיול לפורטוגל 🇵🇹</h1>
    <div class="sub">11–27 בספטמבר 2026 · {total_days}/17 ימים בלוז · {phase_he}</div>
    <div class="progress"><div class="progress-bar" style="width:{int(stability*100)}%"></div></div>
    <div class="progress-label">היציבות של הלוז: {int(stability*100)}%</div>
  </div>

  <div class="card">
    <div class="card-title">✨ מה חדש</div>
    <div class="whats-new">{latest_change or status or "עדיין אין עדכון."}</div>
  </div>

  {stay_html}

  <div class="card">
    <div class="card-title">📍 מבט כללי</div>
    <table>
      <tr><td class="d">#</td><td class="dt">תאריך</td><td class="b">בסיס</td><td class="a">מה קורה</td></tr>
      {day_rows_html}
    </table>
  </div>
  {q_html}

  <div class="footer">נשלח אוטומטית על ידי צוות תכנון הטיול · {today}</div>
</div>
</body>
</html>"""

    text = f"""הטיול לפורטוגל — עדכון {today}
{total_days}/17 ימים בלוז · {phase_he} · יציבות {int(stability*100)}%

מה חדש:
{latest_change or status}

לינה בפורטו — מועמדת, עדיין לא הוזמנה:
Gallery Townhouse & Home, 11–13.9. Standard Suite (חדר אחרון): €327.25 לשני לילות / €163.63 ללילה; כ־₪1,143 / ₪571 ללילה (הערכת ECB).
חשוב: הצ׳ק־אין המפורסם מסתיים ב־00:00, והטיסה נוחתת ב־23:25. חייבים אישור כתוב לצ׳ק־אין אחרי חצות לפני הזמנה. לא מתאימה ל־21–22.9, בגלל מינימום שני לילות.
https://www.booking.com/hotel/pt/gallery-townhouse-amp-home.en-gb.html

(הגרסה המלאה עם כל הפירוט מצורפת כ-HTML)
"""

    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_TXT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT_HTML} ({len(rows)} days, {len(questions)} questions)")


if __name__ == "__main__":
    build()
