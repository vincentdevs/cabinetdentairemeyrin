"""Compose all six team members side by side on one flat tinted background for the équipe page banner.
Each source photo is first cropped to the same head-and-shoulders framing around the detected face,
so every person ends up the same size and shape before the background is removed and pasted, avoiding
the mismatched crops and stray background edges of a plain eye-aligned paste."""
import pathlib
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from rembg import remove, new_session

HERE = pathlib.Path(__file__).parent.parent / "assets"
session = new_session("u2net_human_seg")
det = cv2.FaceDetectorYN.create(str(pathlib.Path(__file__).parent / "yunet.onnx"), "", (480, 640), 0.6, 0.3, 5000)

PEOPLE = ["victor-palmen", "edouard-di-donna", "cilien-prieu", "juliana", "zainne", "luana"]
W, H = 2400, 900
EYE, EYE_Y = 92, 300
N = len(PEOPLE)
SLOT = W / N
canvas = Image.new("RGBA", (W, H), (222, 238, 244, 255))


def detect(im):
    bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    det.setInputSize((bgr.shape[1], bgr.shape[0]))
    _, faces = det.detect(bgr)
    re, le = faces[0][4:6], faces[0][6:8]
    return re, le


for i, name in enumerate(PEOPLE):
    cx = round(SLOT * i + SLOT / 2)
    im = Image.open(HERE / "team" / f"{name}.jpg").convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=0.4)
    im = ImageEnhance.Color(im).enhance(0.95)

    re, le = detect(im)
    dist = float(np.hypot(*(le - re)))
    ex, ey = (re + le) / 2

    # fixed head-and-shoulders crop around the face, same proportions for everyone,
    # clamped so the box never runs past the real photo and pads with black
    crop_w = dist * 5.6
    crop_h = crop_w * 4 / 3
    if crop_w > im.width:
        crop_w = im.width
        crop_h = crop_w * 4 / 3
    if crop_h > im.height:
        crop_h = im.height
        crop_w = crop_h * 3 / 4
    left = ex - crop_w / 2
    top = ey - crop_h * 0.34
    left = max(0, min(left, im.width - crop_w))
    top = max(0, min(top, im.height - crop_h))
    box = (round(left), round(top), round(left + crop_w), round(top + crop_h))
    im = im.crop(box)

    re, le = detect(im)
    dist = float(np.hypot(*(le - re)))
    ex, ey = (re + le) / 2
    scale = EYE / dist

    cut = remove(im, session=session, alpha_matting=True, alpha_matting_foreground_threshold=245, alpha_matting_background_threshold=10, alpha_matting_erode_size=10)
    cut = cut.resize((round(cut.width * scale), round(cut.height * scale)), Image.LANCZOS)
    canvas.paste(cut, (round(cx - ex * scale), round(EYE_Y - ey * scale)), cut)

canvas.convert("RGB").save(HERE / "stock" / "team-banner.jpg", "JPEG", quality=90, optimize=True, progressive=True)
print("team banner ok")
