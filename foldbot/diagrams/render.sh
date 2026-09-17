#!/usr/bin/env bash
# Foldbot - render de diagramas Mermaid (.mmd) a SVG.
# Requiere: @mermaid-js/mermaid-cli (mmdc) en el PATH.
# Uso: ./render.sh
set -euo pipefail

cd "$(dirname "$0")"
mkdir -p svg

# Si existe Chrome del sistema, usar el puppeteer-config para no descargar chromium.
PUPPETEER_ARG=()
if [ -f puppeteer-config.json ]; then
  PUPPETEER_ARG=(-p puppeteer-config.json)
fi

for f in *.mmd; do
  out="svg/${f%.mmd}.svg"
  echo "mmdc $f -> $out"
  mmdc -i "$f" -o "$out" -b transparent "${PUPPETEER_ARG[@]}"
done

echo "OK: SVGs en svg/"
