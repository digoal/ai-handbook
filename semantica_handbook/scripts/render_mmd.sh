#!/usr/bin/env bash
# Render every Mermaid ```mermaid``` block inside handbook chapters into
# assets/diagrams/<slug>-<fig>.svg using mermaid-cli (mmdc).
#
# Usage:
#   bash scripts/render_mmd.sh          # render everything
#   bash scripts/render_mmd.sh --check  # only check, don't write SVG
#
# Requirements: npm i -g @mermaid-js/mermaid-cli

set -euo pipefail

HANDBOOK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$HANDBOOK_ROOT/assets/diagrams"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

if ! command -v mmdc >/dev/null 2>&1; then
  if [[ "${CHECK_ONLY:-0}" == "1" ]]; then
    echo "WARN: mmdc (mermaid-cli) not installed; --check skips rendering." >&2
    exit 0
  fi
  echo "WARN: mmdc (mermaid-cli) not installed; install via 'npm i -g @mermaid-js/mermaid-cli'." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

count=0
# Scan all chapters for ```mermaid``` blocks (zsh-safe: -print0 + read -d '')
while IFS= read -r -d '' chapter; do
  slug="$(basename "$chapter" .md)"
  awk -v tmpdir="$TMP_DIR" -v slug="$slug" '
    /^```mermaid$/ {if(inblock) close(file); inblock=1; n++; file=sprintf("%s/%s-fig-%d.mmd", tmpdir, slug, n); next}
    /^```$/ && inblock {inblock=0; next}
    inblock {print > file}
  ' "$chapter"
done < <(find "$HANDBOOK_ROOT/part-"* -name 'ch-*.md' -print0 2>/dev/null)

# Puppeteer config (Chrome path fallback for macOS dev only; CI uses mmdc default)
PUPPETEER_CONFIG=""
if [[ -f "$HANDBOOK_ROOT/assets/puppeteer-config.json" ]] && [[ "$(uname -s)" == "Darwin" ]]; then
  PUPPETEER_CONFIG="$HANDBOOK_ROOT/assets/puppeteer-config.json"
fi

fail=0
for mmd in "$TMP_DIR"/*.mmd; do
  [[ -f "$mmd" ]] || continue
  base="$(basename "$mmd" .mmd)"
  out="$OUT_DIR/$base.svg"
  count=$((count+1))
  mmdc_pup=""
  [[ -n "$PUPPETEER_CONFIG" ]] && mmdc_pup="-p $PUPPETEER_CONFIG"
  if [[ $CHECK_ONLY -eq 1 ]]; then
    if ! mmdc $mmdc_pup -i "$mmd" -o /dev/null 2>&1; then
      echo "✗ $mmd fails to render"
      fail=$((fail+1))
    fi
  else
    if mmdc $mmdc_pup -i "$mmd" -o "$out" -b transparent 2>&1; then
      echo "✓ $out"
    else
      echo "✗ $mmd failed"
      fail=$((fail+1))
    fi
  fi
done

if [[ $fail -gt 0 ]]; then
  echo "✗ $fail mermaid block(s) failed."
  exit 1
fi
echo "✓ Rendered $count mermaid block(s)."