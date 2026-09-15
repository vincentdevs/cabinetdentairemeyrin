#!/usr/bin/env python3
"""Build both directions of the Cabinet Dentaire Meyrin site.

    python3 site/build.py            # writes dist/
    python3 site/build.py --serve    # builds, then serves dist/ on :4821

Output:
    dist/index.html          comparison page
    dist/version-a/...       Clinique éditoriale
    dist/version-b/...       Cabinet graphique
    dist/assets/...          shared fonts, photos (responsive jpg + webp)
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
    (DIST / "index.html").write_text(comparison(), encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {C.DOMAIN}/sitemap.xml\n", encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{C.DOMAIN}{u}</loc></url>\n" for u in urls if not u.endswith(".html"))
        + "</urlset>\n", encoding="utf-8")
    print(f"built {len(urls)} pages into {DIST}")


def comparison():
    return f"""<!doctype html>
<html lang="fr-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cabinet Dentaire Meyrin, quatre versions</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/assets/fonts/Newsreader.css"><link rel="stylesheet" href="/assets/fonts/Instrument-Sans.css">
<link rel="stylesheet" href="/assets/fonts/Bricolage-Grotesque.css"><link rel="stylesheet" href="/assets/fonts/DM-Sans.css">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f1ec;color:#252123;font:17px/1.6 "Instrument Sans",system-ui,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:64px 24px 96px}}h1{{font:500 clamp(30px,4.2vw,52px)/1.12 Newsreader,Georgia,serif;letter-spacing:-.02em;margin:0 0 .4em;text-wrap:balance}}
p{{max-width:62ch;text-wrap:pretty}}.two{{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;margin-top:48px}}@media(max-width:700px){{.two{{grid-template-columns:1fr}}}}
a.card{{display:block;padding:32px;border-radius:12px;color:inherit;text-decoration:none;min-height:320px;display:flex;flex-direction:column;justify-content:space-between}}
a.card:focus-visible{{outline:3px solid #0F607B;outline-offset:3px}}
.a{{background:#EAF5F9;border:1px solid #D9EEF5}}.a h2{{font:500 34px/1.15 Newsreader,Georgia,serif;color:#0B5269;margin:0 0 .3em}}
.b{{background:#194D98;color:#FAF7F1}}.b h2{{font:800 34px/1.1 "Bricolage Grotesque",system-ui,sans-serif;margin:0 0 .3em;letter-spacing:-.02em}}
.card p{{margin:0 0 1em}}.card span{{font-weight:600;text-decoration:underline;text-underline-offset:4px}}
small{{display:block;margin-top:40px;color:#5f6467}}
</style></head><body><main>
<h1>Cabinet Dentaire, Meyrin et Nyon, quatre versions à comparer</h1>
<p>Un seul site, deux cabinets, deux habillages. Ouvrez l’un ou l’autre, tout le site est derrière : accueil, cabinets, soins, équipe, première visite, urgences, contact.</p>
<div class="two">
<a class="card a" href="/version-a1/"><div><h2>A1, bleus, photo</h2><p>Bleu pâle et pétrole, titres en serif, angles droits. Hero sur la photo de la salle de soins.</p></div><span>Ouvrir A1</span></a>
<a class="card a" href="/version-a2/"><div><h2>A2, bleus, photo</h2><p>Même système, hero sur la photo du fauteuil et de l’écran.</p></div><span>Ouvrir A2</span></a>
<a class="card b" href="/version-b1/"><div><h2>B1, rose et cobalt, illustration plate</h2><p>Deux sans-serif, angles arrondis, illustration vectorielle aux aplats doux.</p></div><span>Ouvrir B1</span></a>
<a class="card b" href="/version-b2/"><div><h2>B2, rose et cobalt, illustration géométrique</h2><p>Même système, illustration en blocs de couleur plus graphique.</p></div><span>Ouvrir B2</span></a>
</div>
<small>Page de comparaison interne, non indexée.</small>
</main></body></html>"""


if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        import functools
        import http.server
        H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
        print("serving on http://localhost:4821/")
        http.server.ThreadingHTTPServer(("127.0.0.1", 4821), H).serve_forever()
