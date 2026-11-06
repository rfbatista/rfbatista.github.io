#!/bin/sh
# Seam B: builds the site, serves it locally, and runs a browser pass over the
# in-scope pages (screenshots, axe WCAG 2.2 AA, layout shift). Run through
# `make browser-check`. Usage: browser-check.sh [label] [outdir]
# Tools install into a cache outside the repo (no node_modules or lockfile here).
set -eu

here=$(cd "$(dirname "$0")" && pwd)
root=${BROWSER_CHECK_ROOT:-$(dirname "$here")}
label=${1:-run}
shots=${2:-${TMPDIR:-/tmp}/blog-browser-check/$label}
tools=${BROWSER_CHECK_TOOLS:-$HOME/.cache/blog-browser-check}

mkdir -p "$tools" "$shots"
if [ ! -d "$tools/node_modules/playwright" ] || [ ! -d "$tools/node_modules/axe-core" ]; then
  (cd "$tools" && npm init -y >/dev/null && npm install --no-audit --no-fund playwright axe-core >/dev/null)
  (cd "$tools" && npx playwright install chromium >/dev/null)
fi

port=${PORT:-1399}
out=$(mktemp -d)
trap 'rm -rf "$out"; [ -z "${srv:-}" ] || kill "$srv" 2>/dev/null || true' EXIT
# No --gc: it deletes the tracked resources/_gen images.
# Local baseURL: the pages must load their own CSS and fonts, not the live site's.
(cd "$root" && hugo --minify --baseURL "http://127.0.0.1:$port/" -d "$out" >/dev/null 2>&1)

python3 -m http.server "$port" --bind 127.0.0.1 --directory "$out" >/dev/null 2>&1 &
srv=$!
until python3 -c "import urllib.request,sys;urllib.request.urlopen('http://127.0.0.1:$port/')" 2>/dev/null; do sleep 0.2; done

export BROWSER_CHECK_BASE="http://127.0.0.1:$port" BROWSER_CHECK_OUT="$shots" NODE_PATH="$tools/node_modules"
status=0
node "$here/browser-check.mjs" || status=1
node "$here/browser-check-post.mjs" || status=1
exit $status
