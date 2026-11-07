#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${OUT_DIR:-$ROOT/dist}"
CHROME_BIN="${CHROME_BIN:-google-chrome}"

mkdir -p "$OUT_DIR"

PAGES=(
  index.html
  checklist-12hr-medsurg.html
  checklist-float-agency.html
  checklist-ed-wipes.html
  weather-addons.html
  energy-snacks.html
  locker-inventory.html
  fatigue-prep.html
)

for page in "${PAGES[@]}"; do
  pdf_name="${page%.html}.pdf"
  echo "Rendering $page -> dist/$pdf_name"
  "$CHROME_BIN" \
    --headless=new \
    --disable-gpu \
    --no-sandbox \
    --disable-extensions \
    --virtual-time-budget=2000 \
    --print-to-pdf="$OUT_DIR/$pdf_name" \
    --no-pdf-header-footer \
    "file://$ROOT/$page" 2>/dev/null
done

ls -1 "$OUT_DIR"/*.pdf 2>/dev/null
