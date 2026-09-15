"""Rewrite root-relative links in a built dist/ folder so the site works when
served from a GitHub Pages project subpath (https://user.github.io/repo/)
instead of the domain root. The site is built with root-relative paths
(href="/soins/", src="/assets/..."), which is correct for a real domain but
wrong under a Pages subpath, so every such path gets the subpath prepended.

Only real URL positions are touched:
  HTML  - the value of a URL attribute (href, src, action, ...), and every
          candidate of a srcset list
  CSS   - the inside of url(...) and the target of @import "..."
  JSON  - string values that are a path, used by the search index

Anything else keeps its slashes. That matters, because a naive "any slash
after a quote or a space" rewrite also destroys CSS comment openers (/*),
CSS value separators (aspect-ratio: 16 / 9, grid-area: 1 / 1), self-closing
tags in inline SVG (stroke-width="2"/>) and the breadcrumb separator
(content: "/"), which silently breaks the layout of the deployed site.

Full https:// URLs (canonical tags, sitemap, JSON-LD, the real future domain)
and protocol-relative //... URLs are left untouched, as are mailto:, tel: and
fragment links.

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

BASE = "/" + BASE.strip("/")

# Attributes whose value is a URL. "content" is included for meta refresh and
# og:image style tags; values that are not paths are skipped by the path test.
URL_ATTRS = (
    "href", "src", "action", "poster", "formaction", "cite", "data",
    "data-src", "data-index", "data-href", "content", "ping", "manifest",
)
SRCSET_ATTRS = ("srcset", "imagesrcset")

ATTR_RE = re.compile(
    r'\b(' + "|".join(URL_ATTRS) + r')\s*=\s*"(/(?!/)[^"]*)"',
    re.IGNORECASE,
)
SRCSET_RE = re.compile(
    r'\b(' + "|".join(SRCSET_ATTRS) + r')\s*=\s*"([^"]*)"',
    re.IGNORECASE,
)
CSS_URL_RE = re.compile(r'url\(\s*(["\']?)(/(?!/)[^"\')]*)\1\s*\)')
CSS_IMPORT_RE = re.compile(r'@import\s+(["\'])(/(?!/)[^"\']*)\1')
JSON_PATH_RE = re.compile(r'"(/(?!/)[^"]*)"')


def rebase_attrs(text):
    text = ATTR_RE.sub(lambda m: f'{m.group(1)}="{BASE}{m.group(2)}"', text)

    def srcset(m):
        parts = []
        for candidate in m.group(2).split(","):
            candidate = candidate.strip()
            if not candidate:
                continue
            if candidate.startswith("/") and not candidate.startswith("//"):
                candidate = BASE + candidate
            parts.append(candidate)
        return f'{m.group(1)}="{", ".join(parts)}"'

    return SRCSET_RE.sub(srcset, text)


def rebase_css(text):
    text = CSS_URL_RE.sub(
        lambda m: f'url({m.group(1)}{BASE}{m.group(2)}{m.group(1)})', text
    )
    return CSS_IMPORT_RE.sub(
        lambda m: f'@import {m.group(1)}{BASE}{m.group(2)}{m.group(1)}', text
    )


def rebase_json(text):
    return JSON_PATH_RE.sub(lambda m: f'"{BASE}{m.group(1)}"', text)


count = 0
for f in sorted(DIST.rglob("*")):
    if not f.is_file():
        continue
    if f.suffix == ".html":
        rewrite = lambda t: rebase_css(rebase_attrs(t))
    elif f.suffix == ".css":
        rewrite = rebase_css
    elif f.suffix == ".json" and f.name != "sitemap.json":
        rewrite = rebase_json
    else:
        continue
    text = f.read_text(encoding="utf-8")
    new_text = rewrite(text)
    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        count += 1

print(f"rebased {count} files under {BASE}")
