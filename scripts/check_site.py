"""Checks the HTML Hugo generated. Usage: check_site.py <public dir>"""
import sys
from pathlib import Path

PUBLIC = Path(sys.argv[1])
failures = []


def page(url):
    f = PUBLIC / url.strip("/") / "index.html"
    if not f.is_file():
        failures.append(f"{url}: page was not generated")
        return ""
    return f.read_text(encoding="utf-8")


def check(ok, message):
    if not ok:
        failures.append(message)


def test_existing_pages_still_render():
    for url in ["/", "/en/", "/posts/", "/jardim/", "/about/", "/en/about/"]:
        check("<h" in page(url) or url == "/", f"{url}: renders no content")


TESTS = [test_existing_pages_still_render]

for t in TESTS:
    t()

if failures:
    print("check: FAILED", file=sys.stderr)
    for f in failures:
        print(f"  - {f}", file=sys.stderr)
    sys.exit(1)
print(f"check: {len(TESTS)} checks passed")
