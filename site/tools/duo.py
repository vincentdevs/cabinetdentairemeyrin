"""Compose the two dentists side by side on a flat tinted background for the home hero, eyes on one line, same scale."""
import pathlib
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from rembg import remove, new_session
HERE = pathlib.Path(__file__).parent.parent / "assets"
session = new_session("u2net_human_seg")
det = cv2.FaceDetectorYN.create(str(pathlib.Path(__file__).parent / "yunet.onnx"), "", (480, 640), 0.6, 0.3, 5000)
W, H = 1200, 900
EYE, EYE_Y = 78, 330
canvas = Image.new("RGBA", (W, H), (222, 238, 244, 255))
for name, cx in (("victor-palmen", 420), ("edouard-di-donna", 790)):
    im = Image.open(HERE / "team" / f"{name}.jpg").convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=0.4); im = ImageEnhance.Color(im).enhance(0.95)
    bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR); det.setInputSize((bgr.shape[1], bgr.shape[0]))
    _, faces = det.detect(bgr); re, le = faces[0][4:6], faces[0][6:8]
    dist = float(np.hypot(*(le - re))); ex, ey = (re + le) / 2
    scale = EYE / dist
    cut = remove(im, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=8)
    cut = cut.resize((round(cut.width * scale), round(cut.height * scale)), Image.LANCZOS)
    canvas.paste(cut, (round(cx - ex * scale), round(EYE_Y - ey * scale)), cut)
canvas.convert("RGB").save(HERE / "stock" / "duo-dentistes.jpg", "JPEG", quality=88, optimize=True, progressive=True)
print("duo ok")
