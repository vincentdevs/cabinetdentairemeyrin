"""Give every photo the same warm-highlight, cool-shadow grade so the set reads as one shoot.

    python3 site/tools/grade.py

Sources: site/assets/refs/*.png (the reference stills), site/assets/photos/*.jpg (the practice's
own photos), site/assets/team/*.jpg (portraits, lighter touch).
Output: site/assets/stock/*.jpg, site/assets/photos-graded/*.jpg, site/assets/team-graded/*.jpg.
"""
import pathlib
from PIL import Image, ImageEnhance, ImageOps

HERE = pathlib.Path(__file__).parent.parent / "assets"
WARM = (255, 236, 214)
COOL = (28, 60, 92)


def grade(im, strength=0.14, sat=0.9, contrast=1.06):
    im = im.convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=0.4)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    lum = im.convert("L")
    warm = Image.new("RGB", im.size, WARM)
    cool = Image.new("RGB", im.size, COOL)
    tint = Image.composite(warm, cool, lum)
    return Image.blend(im, tint, strength)


def save(im, path, q=86):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)


for src in sorted((HERE / "refs").glob("*.png")):
    save(grade(Image.open(src)), HERE / "stock" / (src.stem + ".jpg"))
for src in sorted((HERE / "photos").glob("*.jpg")):
    save(grade(Image.open(src), strength=0.10, sat=0.92), HERE / "photos-graded" / src.name)
for src in sorted((HERE / "team").glob("*.jpg")):
    save(grade(Image.open(src), strength=0.06, sat=0.95, contrast=1.03), HERE / "team-graded" / src.name)
print("graded")
