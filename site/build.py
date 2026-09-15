#!/usr/bin/env python3
"""Build the Cabinet Dentaire Meyrin site.

    python3 site/build.py            # writes dist/
    python3 site/build.py --serve    # builds, then serves dist/ on :4821

Output:
    dist/index.html          French home page (root)
    dist/en/...               English pages
    dist/assets/...          fonts, photos (responsive jpg + webp), illustrations
"""
import html
import json
import pathlib
import shutil
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
DIST = ROOT / "dist"
ASSETS = HERE / "assets"
WIDTHS = (480, 960, 1600)

sys.path.insert(0, str(HERE))
import content as C  # noqa: E402


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ images
_DIMS = {}


def build_images():
    """Responsive jpg + webp variants for every photo, written once to dist/assets/img."""
    for folder, srcdir, ext in (("photos", "photos-graded", "jpg"), ("stock", "stock", "jpg"), ("stock", "stock", "png"), ("team", "team-cut", "png")):
        out = DIST / "assets" / "img" / folder
        out.mkdir(parents=True, exist_ok=True)
        for src in sorted((ASSETS / srcdir).glob("*." + ext)):
            key = f"{folder}/{src.name}"
            with Image.open(src) as im:
                w, h = im.size
                _DIMS[key] = (w, h)
                for tw in WIDTHS:
                    if tw > w and tw != WIDTHS[0]:
                        continue
                    tw2 = min(tw, w)
                    fallback = out / f"{src.stem}-{tw}.{ext}"
                    webp = out / f"{src.stem}-{tw}.webp"
                    if fallback.exists() and webp.exists():
                        continue
                    th = round(h * tw2 / w)
                    if ext == "png":
                        r = im.convert("RGBA").resize((tw2, th), Image.LANCZOS)
                        r.save(fallback, "PNG", optimize=True)
                        r.save(webp, "WEBP", quality=88, method=6)
                    else:
                        r = im.convert("RGB").resize((tw2, th), Image.LANCZOS)
                        r.save(fallback, "JPEG", quality=82, optimize=True, progressive=True)
                        r.save(webp, "WEBP", quality=80, method=6)


def picture(key, alt, sizes="100vw", cls="", eager=False, fetchpriority=None):
    """<picture> with webp + jpg srcset. key is 'folder/name.jpg'."""
    folder, name = key.split("/")
    stem, ext = name.rsplit(".", 1)
    w, h = _DIMS[key]
    ws = [x for x in WIDTHS if x <= w] or [WIDTHS[0]]
    base = f"/assets/img/{folder}/{stem}"
    webp = ", ".join(f"{base}-{x}.webp {min(x, w)}w" for x in ws)
    jpg = ", ".join(f"{base}-{x}.{ext} {min(x, w)}w" for x in ws)
    loading = "" if eager else ' loading="lazy" decoding="async"'
    fp = f' fetchpriority="{fetchpriority}"' if fetchpriority else ""
    return (f'<picture{" class=" + chr(34) + cls + chr(34) if cls else ""}>'
            f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="{base}-{ws[-1]}.{ext}" srcset="{jpg}" sizes="{sizes}" alt="{esc(alt)}" width="{w}" height="{h}"{loading}{fp}>'
            f'</picture>')


# ------------------------------------------------------------------ html shell
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def head(title, desc, path, prefix, css, theme, ldobjs=(), og="photos/cabinet-hero.jpg", extra="", lang="fr-CH", skip="Aller au contenu"):
    url = C.DOMAIN + prefix + path
    ogimg = C.DOMAIN + "/assets/img/" + og.rsplit(".", 1)[0] + "-960." + og.rsplit(".", 1)[1]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="{theme}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CH">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ogimg}">
<link rel="icon" href="{prefix.split(chr(47)+chr(101)+chr(110))[0]}/favicon.svg" type="image/svg+xml">
{extra}
<link rel="stylesheet" href="{prefix.split(chr(47)+chr(101)+chr(110))[0]}/styles.css">
{''.join(ld(o) for o in ldobjs)}
</head>
<body>
<a class="skip" href="#contenu">{skip}</a>
"""


def write(prefix, path, body):
    """path like '/', '/soins/', '/404.html'."""
    out = DIST / prefix.strip("/")
    if path.endswith(".html"):
        f = out / path.strip("/")
    else:
        f = out / path.strip("/") / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(body, encoding="utf-8")
    return path


# ------------------------------------------------------------------ main
def main():
    if DIST.exists():
        for child in DIST.iterdir():
            if child.name != "assets":
                shutil.rmtree(child) if child.is_dir() else child.unlink()
    (DIST / "assets").mkdir(parents=True, exist_ok=True)
    build_images()
    brand_out = DIST / "assets" / "brand"
    if brand_out.exists():
        shutil.rmtree(brand_out)
    shutil.copytree(ASSETS / "brand", brand_out)
    ill_out = DIST / "assets" / "illustrations"
    if ill_out.exists():
        shutil.rmtree(ill_out)
    shutil.copytree(ASSETS / "illustrations", ill_out)
    fonts_out = DIST / "assets" / "fonts"
    if fonts_out.exists():
        shutil.rmtree(fonts_out)
    shutil.copytree(ASSETS / "fonts", fonts_out)

    import render
    urls = []
    for theme, T in render.THEMES.items():
        urls += [T["prefix"] + u for u in render.build(theme, picture, head, write, ld)]
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {C.DOMAIN}/sitemap.xml\n", encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{C.DOMAIN}{u}</loc></url>\n" for u in urls if not u.endswith(".html"))
        + "</urlset>\n", encoding="utf-8")
    print(f"built {len(urls)} pages into {DIST}")


if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        import functools
        import http.server
        H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
        print("serving on http://localhost:4821/")
        http.server.ThreadingHTTPServer(("127.0.0.1", 4821), H).serve_forever()
