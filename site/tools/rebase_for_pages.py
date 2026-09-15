"""Rewrite root-relative links in a built dist/ folder so the site works when
served from a GitHub Pages project subpath (https://user.github.io/repo/)
instead of the domain root. The site itself is built with root-relative paths
(href="/soins/", src="/assets/..."), which is correct for a real domain but
wrong under a Pages subpath, so every such path gets the subpath prepended.
Full https:// URLs (canonical tags, sitemap, JSON-LD, the real future domain)
are left untouched, since only a "/" preceded by a quote, whitespace, comma,
or "(" is a path start rather than part of "https://something".

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

PATTERN = re.compile(r'(?<=["\'\s,(])/(?!/)')

count = 0
for f in list(DIST.rglob("*.html")) + list(DIST.rglob("*.css")):
    text = f.read_text(encoding="utf-8")
    new_text = PATTERN.sub(BASE + "/", text)
    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        count += 1

print(f"rebased {count} files under {BASE}")
