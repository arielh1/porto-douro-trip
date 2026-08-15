#!/usr/bin/env bash
#
# Download the photos listed in a stay's photos.md into that stay's photos/ folder.
#
#   bin/fetch-photos.sh                      # every stay
#   bin/fetch-photos.sh douro-a-quinta       # one stay
#
# The `stays` agent collects and verifies the image URLs; this script does the
# downloading, so the fetching happens on your machine and under your control.

set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

command -v curl >/dev/null || { echo "curl not found"; exit 1; }

fetch_one() {
  local dir="$1"
  local manifest="$dir/photos.md"
  [[ -f "$manifest" ]] || { echo "  · $(basename "$dir"): no photos.md"; return; }

  mkdir -p "$dir/photos"
  local n=0 ok=0

  # pull every http(s) URL that looks like an image out of the manifest table
  while read -r url; do
    n=$((n + 1))
    local ext="${url##*.}"; ext="${ext%%\?*}"
    case "$ext" in jpg|jpeg|png|webp|avif) ;; *) ext="jpg" ;; esac
    local out
    out="$(printf '%s/photos/%02d.%s' "$dir" "$n" "$ext")"

    [[ -s "$out" ]] && { ok=$((ok + 1)); continue; }

    if curl -fsSL --max-time 30 --max-filesize 15000000 \
         -A "Mozilla/5.0 (trip-planner)" -o "$out" "$url" 2>/dev/null \
       && [[ -s "$out" ]]; then
      ok=$((ok + 1))
    else
      rm -f "$out"
      echo "      ✗ $url"
    fi
  done < <(grep -oE 'https?://[^ )|"]+\.(jpg|jpeg|png|webp|avif)[^ )|"]*' "$manifest" | sort -u)

  echo "  ✓ $(basename "$dir"): $ok/$n"
}

if [[ $# -gt 0 ]]; then
  for s in "$@"; do fetch_one "stays/$s"; done
else
  shopt -s nullglob
  for d in stays/*/; do fetch_one "${d%/}"; done
fi

echo
echo "Done. Photos are in stays/<name>/photos/"
