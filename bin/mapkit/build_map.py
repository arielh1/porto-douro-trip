#!/usr/bin/env python3
"""
build_map.py — turn a structured list of trip places into:
  1. map.html          — a self-contained interactive Google Maps page (sidebar + layers)
  2. trip-map.kml       — for desktop Google My Maps import (folders = layers, styled pins)
  3. trip-map-<cat>.csv — one CSV per category, for MOBILE Google My Maps import
                           (KML file pickers on iOS/Android often grey out .kml files;
                           CSV is universally accepted, so this is the reliable mobile path)
  4. trip-map-all.csv   — every place in one CSV (flat fallback / quick single import)

Input: a JSON file — a list of place objects:
  {
    "name": "Cais da Foz",
    "category": "food",        # short slug, used for grouping/coloring
    "category_label": "🍽️ מסעדות",   # human label shown as KML folder / CSV filename hint
    "day": "יום 3 · 13.9",      # optional, used to group the HTML sidebar
    "desc": "ארוחת ערב ראשונה בדורו",
    "lat": 41.1878,
    "lng": -7.5455,
    "emoji": "🍽️"               # optional, defaults derived from category
  }

Usage:
  python3 build_map.py --input places.json --output-dir out --title "הטיול שלי" --rtl
"""
import argparse
import csv
import json
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

DEFAULT_PALETTE = [
    ("ff3a2b6b", "http://maps.google.com/mapfiles/kml/paddle/homegardenbusiness.png"),
    ("ff2b3ab5", "http://maps.google.com/mapfiles/kml/shapes/wine.png"),
    ("ff2b7a3a", "http://maps.google.com/mapfiles/kml/shapes/hiker.png"),
    ("ff2b5ed6", "http://maps.google.com/mapfiles/kml/shapes/dining.png"),
    ("ffd68c2b", "http://maps.google.com/mapfiles/kml/shapes/water.png"),
    ("ff8c2bd6", "http://maps.google.com/mapfiles/kml/shapes/camera.png"),
    ("ff2ba0a0", "http://maps.google.com/mapfiles/kml/shapes/flag.png"),
    ("ff999999", "http://maps.google.com/mapfiles/kml/shapes/info-i.png"),
]


def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s or "layer"


def load_places(path):
    with open(path, encoding="utf-8") as f:
        places = json.load(f)
    for i, p in enumerate(places):
        for req in ("name", "category", "lat", "lng"):
            if req not in p:
                raise ValueError(f"place #{i} ({p.get('name','?')}) missing required field '{req}'")
    return places


def assign_colors(categories):
    colors = {}
    for i, cat in enumerate(categories):
        colors[cat] = DEFAULT_PALETTE[i % len(DEFAULT_PALETTE)]
    return colors


def build_kml(places, categories, colors, title, out_path):
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(kml, "Document")
    ET.SubElement(doc, "name").text = title
    ET.SubElement(doc, "description").text = "Import: mymaps.google.com → New map → Import"

    for cat in categories:
        color, icon = colors[cat]
        style = ET.SubElement(doc, "Style", id=cat)
        icon_style = ET.SubElement(style, "IconStyle")
        ET.SubElement(icon_style, "color").text = color
        ET.SubElement(icon_style, "scale").text = "1.1"
        icon_el = ET.SubElement(icon_style, "Icon")
        ET.SubElement(icon_el, "href").text = icon

    by_cat = {}
    for p in places:
        by_cat.setdefault(p["category"], []).append(p)

    for cat in categories:
        label = next((p.get("category_label", cat) for p in places if p["category"] == cat), cat)
        folder = ET.SubElement(doc, "Folder")
        ET.SubElement(folder, "name").text = label
        for p in by_cat.get(cat, []):
            pm = ET.SubElement(folder, "Placemark")
            name = p["name"]
            if p.get("day"):
                name = f"{name} ({p['day']})"
            ET.SubElement(pm, "name").text = name
            ET.SubElement(pm, "description").text = p.get("desc", "")
            ET.SubElement(pm, "styleUrl").text = f"#{cat}"
            point = ET.SubElement(pm, "Point")
            ET.SubElement(point, "coordinates").text = f"{p['lng']},{p['lat']},0"

    rough = ET.tostring(kml, encoding="utf-8")
    pretty = minidom.parseString(rough).toprettyxml(indent="  ")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pretty)
    # validate
    ET.parse(out_path)


def build_csvs(places, categories, out_dir, base_name):
    written = []
    by_cat = {}
    for p in places:
        by_cat.setdefault(p["category"], []).append(p)

    for cat in categories:
        label = next((p.get("category_label", cat) for p in places if p["category"] == cat), cat)
        path = os.path.join(out_dir, f"{base_name}-{slugify(cat)}.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["Name", "Description", "Category", "Latitude", "Longitude"])
            for p in by_cat[cat]:
                name = p["name"]
                if p.get("day"):
                    name = f"{name} ({p['day']})"
                w.writerow([name, p.get("desc", ""), label, p["lat"], p["lng"]])
        written.append((path, label, len(by_cat[cat])))

    # The all-in-one CSV carries a Category column so that after import, My Maps'
    # own "Style by data column" feature (layer menu → Style) can auto-color and
    # auto-icon every pin by category in one step — this is what makes a single
    # mobile-friendly CSV import produce a result close to the KML's pre-colored
    # folders, without needing N separate imports.
    all_path = os.path.join(out_dir, f"{base_name}-all.csv")
    with open(all_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Name", "Description", "Category", "Latitude", "Longitude"])
        for p in places:
            label = p.get("category_label", p["category"])
            name = p["name"]
            if p.get("day"):
                name = f"{name} ({p['day']})"
            w.writerow([name, p.get("desc", ""), label, p["lat"], p["lng"]])
    written.append((all_path, "הכל יחד / all-in-one", len(places)))
    return written


HTML_TEMPLATE = """<!DOCTYPE html>
<html dir="{dir}" lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  html, body {{ margin:0; padding:0; height:100%; font-family:-apple-system,'Segoe UI',Arial,sans-serif; }}
  #app {{ display:flex; height:100vh; flex-direction:{flex_dir}; }}
  #sidebar {{ width:360px; min-width:300px; background:#faf8f4; border-{border_side}:1px solid #e5e0d5;
             overflow-y:auto; padding:12px; box-sizing:border-box; }}
  #map {{ flex:1; }}
  .day-group {{ margin-bottom:14px; }}
  .day-title {{ font-size:12px; font-weight:700; color:#6b2b3a; text-transform:uppercase;
               letter-spacing:.03em; margin:14px 0 6px; padding-bottom:4px; border-bottom:1px solid #e5e0d5; }}
  .row {{ display:flex; align-items:flex-start; gap:8px; padding:8px 6px; border-radius:8px;
         cursor:pointer; font-size:13.5px; line-height:1.4; }}
  .row:hover {{ background:#f0ece0; }}
  .emoji {{ font-size:16px; flex-shrink:0; width:22px; text-align:center; }}
  .row .name {{ font-weight:600; color:#2b2420; }}
  .row .desc {{ color:#777; font-size:12px; margin-top:1px; }}
  .legend {{ position:absolute; top:12px; {legend_side}:12px; background:#fff; border-radius:10px;
            padding:10px 14px; box-shadow:0 2px 8px rgba(0,0,0,.15); font-size:13px; z-index:5; }}
  .legend label {{ display:flex; align-items:center; gap:6px; margin:4px 0; cursor:pointer; }}
  .banner {{ position:absolute; top:0; left:0; right:0; background:#6b2b3a; color:#fff;
            padding:10px 16px; font-size:13px; text-align:center; z-index:10; }}
  .banner code {{ background:rgba(255,255,255,.2); padding:1px 6px; border-radius:4px; }}
  .header {{ padding:14px 12px 4px; }}
  .header h1 {{ font-size:16px; margin:0 0 2px; color:#6b2b3a; }}
  .header .sub {{ font-size:11.5px; color:#999; }}
</style>
</head>
<body>
<div id="app">
  <div id="sidebar">
    <div class="header">
      <h1>{title}</h1>
      <div class="sub">{subtitle}</div>
    </div>
    <div id="list"></div>
  </div>
  <div style="position:relative; flex:1;">
    <div class="banner" id="keyBanner" style="display:none;">
      {key_banner_text}
    </div>
    <div id="legend" class="legend">
      <div style="font-weight:700; margin-bottom:6px;">{layers_label}</div>
      {legend_html}
      <label><input type="checkbox" data-layer="route"> {route_label}</label>
    </div>
    <div id="map" style="width:100%; height:100%;"></div>
  </div>
</div>

<script>
const PLACES = {places_json};
const ROUTE = {route_json};

const listEl = document.getElementById('list');
let currentDay = null;
PLACES.forEach((p, i) => {{
  if (p.day && p.day !== currentDay) {{
    currentDay = p.day;
    const h = document.createElement('div');
    h.className = 'day-title';
    h.textContent = currentDay;
    listEl.appendChild(h);
  }}
  const row = document.createElement('div');
  row.className = 'row';
  row.dataset.index = i;
  row.innerHTML = `<span class="emoji">${{p.emoji || '📍'}}</span><div><div class="name">${{p.name}}</div><div class="desc">${{p.desc || ''}}</div></div>`;
  row.onclick = () => focusMarker(i);
  listEl.appendChild(row);
}});

let map, markers = [], routeLine;
window.initMap = function() {{
  map = new google.maps.Map(document.getElementById('map'), {{
    zoom: 7,
    center: {{lat: {center_lat}, lng: {center_lng}}},
    mapTypeId: 'roadmap',
  }});
  const bounds = new google.maps.LatLngBounds();
  const info = new google.maps.InfoWindow();

  PLACES.forEach((p, i) => {{
    const marker = new google.maps.Marker({{
      position: {{lat: p.lat, lng: p.lng}},
      map,
      label: p.emoji || undefined,
      title: p.name,
    }});
    marker.addListener('click', () => {{
      info.setContent(`<div style="font-family:sans-serif;direction:{dir};max-width:220px;">
        <b>${{p.emoji || ''}} ${{p.name}}</b><br><span style="color:#666;font-size:12px;">${{p.day || ''}}</span>
        <p style="margin:6px 0 0;font-size:13px;">${{p.desc || ''}}</p></div>`);
      info.open(map, marker);
    }});
    markers.push({{marker, layer: p.category}});
    bounds.extend(marker.getPosition());
  }});

  routeLine = new google.maps.Polyline({{
    path: ROUTE, geodesic: true, strokeColor: '#6b2b3a', strokeOpacity: 0.7, strokeWeight: 3,
  }});
  routeLine.setMap(null);

  if (PLACES.length) map.fitBounds(bounds);

  document.querySelectorAll('#legend input').forEach(cb => {{
    cb.addEventListener('change', () => {{
      const layer = cb.dataset.layer;
      if (layer === 'route') {{ routeLine.setMap(cb.checked ? map : null); return; }}
      markers.filter(m => m.layer === layer).forEach(m => m.marker.setMap(cb.checked ? map : null));
    }});
  }});

  window._mapFocus = function(i) {{
    const p = PLACES[i];
    map.panTo({{lat: p.lat, lng: p.lng}});
    map.setZoom(13);
    google.maps.event.trigger(markers[i].marker, 'click');
  }};
}};

function focusMarker(i) {{
  if (window._mapFocus) window._mapFocus(i);
}}

const API_KEY = "{api_key}";
if (API_KEY === "GOOGLE_MAPS_API_KEY_PLACEHOLDER" || !API_KEY) {{
  document.getElementById('keyBanner').style.display = 'block';
}} else {{
  const s = document.createElement('script');
  s.src = `https://maps.googleapis.com/maps/api/js?key=${{API_KEY}}&callback=initMap`;
  s.async = true;
  document.head.appendChild(s);
}}
</script>
</body>
</html>
"""


def build_html(places, categories, title, subtitle, out_path, api_key, rtl):
    legend_rows = []
    for cat in categories:
        label = next((p.get("category_label", cat) for p in places if p["category"] == cat), cat)
        legend_rows.append(f'<label><input type="checkbox" checked data-layer="{cat}"> {label}</label>')
    route = [{"lat": p["lat"], "lng": p["lng"]} for p in places if p.get("is_route_point")]
    if not route:
        route = [{"lat": p["lat"], "lng": p["lng"]} for p in places[:1]]
    lats = [p["lat"] for p in places] or [0]
    lngs = [p["lng"] for p in places] or [0]
    html = HTML_TEMPLATE.format(
        dir="rtl" if rtl else "ltr",
        lang="he" if rtl else "en",
        flex_dir="row-reverse" if rtl else "row",
        border_side="left" if rtl else "right",
        legend_side="left" if rtl else "right",
        title=title,
        subtitle=subtitle,
        key_banner_text=(
            "כדי להפעיל את המפה, הדבק Google Maps API key בקובץ google-maps-api-key.txt והרץ שוב."
            if rtl else
            "Paste a Google Maps API key into google-maps-api-key.txt and rebuild to activate the map."
        ),
        layers_label="שכבות" if rtl else "Layers",
        route_label="✈️ המסלול" if rtl else "✈️ Route",
        legend_html="\n      ".join(legend_rows),
        places_json=json.dumps(places, ensure_ascii=False),
        route_json=json.dumps(route, ensure_ascii=False),
        center_lat=sum(lats) / len(lats),
        center_lng=sum(lngs) / len(lngs),
        api_key=api_key,
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="JSON file with the place list")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--title", default="Trip Map")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--api-key-file", default=None, help="path to a text file containing a Google Maps JS API key")
    ap.add_argument("--rtl", action="store_true", help="Hebrew/RTL layout")
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    places = load_places(args.input)
    categories = list(dict.fromkeys(p["category"] for p in places))  # preserves order, dedups
    colors = assign_colors(categories)

    api_key = "GOOGLE_MAPS_API_KEY_PLACEHOLDER"
    if args.api_key_file and os.path.exists(args.api_key_file):
        api_key = open(args.api_key_file, encoding="utf-8").read().strip()

    kml_path = os.path.join(args.output_dir, "trip-map.kml")
    build_kml(places, categories, colors, args.title, kml_path)

    csvs = build_csvs(places, categories, args.output_dir, "trip-map")

    html_path = os.path.join(args.output_dir, "map.html")
    build_html(places, categories, args.title, args.subtitle, html_path, api_key, args.rtl)

    print(f"Wrote {html_path}")
    print(f"Wrote {kml_path} ({len(categories)} layers, {len(places)} places)")
    for path, label, n in csvs:
        print(f"Wrote {path} — {label} ({n})")


if __name__ == "__main__":
    main()

