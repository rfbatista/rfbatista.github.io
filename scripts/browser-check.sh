#!/bin/sh
# Seam B: builds the site, serves it locally, and runs a browser pass over the
# in-scope pages (screenshots, axe WCAG 2.2 AA, layout shift). Run through
# `make browser-check`. Usage: browser-check.sh [label] [outdir]
# Tools install into a cache outside the repo (no node_modules or lockfile here).
set -eu

here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")
label=${1:-run}
shots=${2:-${TMPDIR:-/tmp}/blog-browser-check/$label}
tools=${BROWSER_CHECK_TOOLS:-$HOME/.cache/blog-browser-check}

mkdir -p "$tools" "$shots"
if [ ! -d "$tools/node_modules/playwright" ] || [ ! -d "$tools/node_modules/axe-core" ]; then
  (cd "$tools" && npm init -y >/dev/null && npm install --no-audit --no-fund playwright axe-core >/dev/null)
  (cd "$tools" && npx playwright install chromium >/dev/null)
fi

out=$(mktemp -d)
trap 'rm -rf "$out"; [ -z "${srv:-}" ] || kill "$srv" 2>/dev/null || true' EXIT
# No --gc: it deletes the tracked resources/_gen images.
(cd "$root" && hugo --minify -d "$out" >/dev/null 2>&1)

port=${PORT:-1399}
(cd "$out" && python3 -I -m http.server "$port" --bind 127.0.0.1 >/dev/null 2>&1) &
srv=$!
sleep 1

BROWSER_CHECK_BASE="http://127.0.0.1:$port" BROWSER_CHECK_OUT="$shots" \
  NODE_PATH="$tools/node_modules" node "$here/browser-check.mjs"
