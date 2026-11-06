#!/bin/sh
# Builds the site with the Hugo version CI uses, fails on any new Hugo warning
# or error, then checks the generated HTML. Run through `make check`.
set -eu

HUGO_VERSION=0.166.0 # keep in sync with .github/workflows/hugo.yaml
here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")

if ! hugo version | grep -q "hugo v$HUGO_VERSION[+ ]"; then
  echo "check: needs Hugo $HUGO_VERSION, found: $(hugo version 2>&1 | head -1)" >&2
  exit 1
fi

out=$(mktemp -d)
log=$(mktemp)
trap 'rm -rf "$out" "$log"' EXIT

# No --gc: it deletes the tracked resources/_gen images.
(cd "$root" && hugo --minify -d "$out" >"$log" 2>&1) || { cat "$log" >&2; echo "check: hugo build failed" >&2; exit 1; }

# Warnings the site already had before the Projects page (see the baseline file).
# Anything else that says WARN or ERROR fails the check.
new=$(grep -E '^(WARN|ERROR)' "$log" | grep -v -x -F -f "$here/hugo-warnings-baseline.txt" || true)
if [ -n "$new" ]; then
  echo "check: new Hugo warnings or errors:" >&2
  echo "$new" >&2
  exit 1
fi

python3 -I "$here/check_site.py" "$out"
