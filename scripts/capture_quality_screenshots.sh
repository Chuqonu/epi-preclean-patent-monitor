#!/usr/bin/env bash
# Capture R1 viewport artifacts. Usage: ./scripts/capture_quality_screenshots.sh [OUT_DIR]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/docs/quality-runs/2026-10-20-r1}"
LOCAL_PORT="${LOCAL_PORT:-8765}"
BASE_LOCAL="http://127.0.0.1:${LOCAL_PORT}/"
PAGES_LIVE="https://chuqonu.github.io/epi-preclean-patent-monitor/"
DOT_REF="https://45-32-39-201.sslip.io:8443/patent-alert/report.html"
CHROME="${CHROME:-google-chrome}"
CHROME_PROFILE="${CHROME_PROFILE:-/tmp/chrome-quality-capture}"

mkdir -p "$OUT/viewports" "$OUT/pages-live" "$OUT/dot-reference"

if ! curl -sf -o /dev/null "$BASE_LOCAL"; then
  echo "Start static server: python3 -m http.server $LOCAL_PORT (repo root)" >&2
  exit 1
fi

shot() {
  local w=$1 h=$2 out=$3 url=$4
  timeout 90 "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --user-data-dir="$CHROME_PROFILE" \
    --window-size="$w,$h" --screenshot="$out" "$url" 2>/dev/null || true
  test -s "$out"
}

shot 1440 900 "$OUT/viewports/local-1440.png" "$BASE_LOCAL"
shot 768 1024 "$OUT/viewports/local-768.png" "$BASE_LOCAL"
shot 390 844 "$OUT/viewports/local-390.png" "$BASE_LOCAL"
shot 1440 900 "$OUT/pages-live/github-1440.png" "$PAGES_LIVE"
shot 768 1024 "$OUT/pages-live/github-768.png" "$PAGES_LIVE"
shot 390 844 "$OUT/pages-live/github-390.png" "$PAGES_LIVE"
shot 1440 900 "$OUT/dot-reference/dot-1440.png" "$DOT_REF"

echo "Wrote screenshots under $OUT"
