"""Rewrite root-relative asset and page links in a built dist/ folder so the site
works when served from a GitHub Pages project subpath (https://user.github.io/repo/)
instead of the domain root. Only touches links that start with /assets/ or
/version-*, since those are the only root-relative prefixes the generator emits;
full https:// URLs (canonical tags, sitemap, JSON-LD) are left untouched.

Usage: python3 rebase_for_pages.py /repo-name  (run after site/build.py, on dist/)
"""
import pathlib
import re
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else ""
DIST = pathlib.Path(__file__).parent.parent.parent / "dist"

if not BASE:
    print("no base path given, nothing to do")
    sys.exit(0)

PATTERN = re.compile(r'(?<=["\'\s,(])/(assets|version-a1|version-a2|version-b1|version-b2)/')

count = 0
for f in list(DIST.rglob("*.html")) + list(DIST.rglob("*.css")):
    text = f.read_text(encoding="utf-8")
    new_text = PATTERN.sub(lambda m: BASE + "/" + m.group(1) + "/", text)
    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        count += 1

print(f"rebased {count} files under {BASE}")
