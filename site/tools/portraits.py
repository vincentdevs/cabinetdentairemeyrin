"""Cut every portrait out of its background and place it on a 480x480 canvas with the head at
the same scale and the same height, so the team reads as one set inside a round frame.

    python3 site/tools/portraits.py
"""
import pathlib
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from rembg import remove, new_session

HERE = pathlib.Path(__file__).parent.parent / "assets"
OUT = HERE / "team-cut"
OUT.mkdir(exist_ok=True)
SIZE = 480
EYE_DIST = 76       # distance between the eyes in the output
EYE_Y = 210         # height of the eye line in the output
session = new_session("u2net_human_seg")
det = cv2.FaceDetectorYN.create(str(pathlib.Path(__file__).parent / "yunet.onnx"), "", (480, 640), 0.6, 0.3, 5000)

for src in sorted((HERE / "team").glob("*.jpg")):
    im = Image.open(src).convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=0.4)
    im = ImageEnhance.Color(im).enhance(0.95)
    cut = remove(im, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=10, alpha_matting_erode_size=8)
    bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    det.setInputSize((bgr.shape[1], bgr.shape[0]))
    _, faces = det.detect(bgr)
    re, le = faces[0][4:6], faces[0][6:8]
    dist = float(np.hypot(*(le - re)))
    cx, cy = (re + le) / 2
    scale = EYE_DIST / dist
    w2, h2 = round(cut.width * scale), round(cut.height * scale)
    cut2 = cut.resize((w2, h2), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    x = round(SIZE / 2 - cx * scale)
    y = round(EYE_Y - cy * scale)
    canvas.paste(cut2, (x, y), cut2)
    canvas.save(OUT / (src.stem + ".png"), "PNG", optimize=True)
    print(src.name, "eyes", round(dist), "scale", round(scale, 2), "offset", x, y)
