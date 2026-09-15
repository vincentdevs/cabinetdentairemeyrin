"""Turn the Meyrin treatment-room photo into a flat poster illustration, once per brand palette."""
import pathlib
import cv2
import numpy as np
from PIL import Image
HERE = pathlib.Path(__file__).parent.parent / "assets"
PALETTES = {  # darkest to lightest, RGB
    "a": [(11, 82, 105), (15, 96, 123), (60, 150, 180), (140, 200, 220), (217, 238, 245), (234, 245, 249), (250, 249, 246)],
    "b": [(22, 55, 78), (25, 77, 152), (77, 183, 207), (139, 216, 232), (228, 244, 248), (245, 168, 174), (250, 247, 241)],
}
src = cv2.imread(str(HERE / "photos" / "cabinet-hero.jpg"))
src = cv2.resize(src, (900, 1350), interpolation=cv2.INTER_AREA)
sm = src.copy()
for _ in range(7):
    sm = cv2.bilateralFilter(sm, 9, 70, 7)
Z = sm.reshape((-1, 3)).astype(np.float32)
K = 7
_, labels, centers = cv2.kmeans(Z, K, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0), 5, cv2.KMEANS_PP_CENTERS)
order = np.argsort(centers.mean(axis=1))  # cluster ids sorted dark -> light
rank = {int(c): i for i, c in enumerate(order)}
gray = cv2.medianBlur(cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY), 5)
edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
edges = cv2.dilate(255 - edges, np.ones((2, 2), np.uint8)) > 0
for theme, pal in PALETTES.items():
    lut = np.array([pal[rank[i]] for i in range(K)], dtype=np.uint8)  # RGB per cluster
    out = lut[labels.flatten()].reshape(sm.shape)
    ink = np.array(pal[0], dtype=np.float32)
    out = out.astype(np.float32)
    out[edges] = out[edges] * 0.3 + ink * 0.7
    out = cv2.GaussianBlur(out.astype(np.uint8), (0, 0), 0.6)
    Image.fromarray(out).save(HERE / "stock" / f"cabinet-illustration-{theme}.png", "PNG", optimize=True)
print("illustrations ok")
