#!/usr/bin/env python3
"""Crop booklet figures from the phone photos (spec 3.7).

For each figure: rotate the page photo upright, cut the located box, push
unsaturated off-white paper to white (dark and coloured pixels are kept),
paint out the given handwriting rectangles, then trim the border by pixel
scan to about 5 px of white. Output: fig/<name>.png plus fig/<name>.json
holding the crop size and the edge points where printed leader arrows
leave the crop (found by scanning the edge columns), which shared.sty uses
to place the letter labels.
"""
import json, os, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(HERE)
SRC = os.path.join(UNIT, "src", "pages")
FIG = os.path.join(UNIT, "fig")

# name: (page image, rotation, box x0 y0 x1 y1 in the upright image,
#        rectangles to paint white, relative to the box)
FIGS = json.load(open(os.path.join(HERE, "crops.json")))


def whiten(im, level=198):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    v = hsv[..., 2].astype(np.float32)
    s = hsv[..., 1]
    # local paper level: a large max filter of V (the paper is the brightest
    # thing in any 121 px window, even inside a grey-filled drawing), smoothed
    bg = cv2.dilate(hsv[..., 2], np.ones((121, 121), np.uint8))
    bg = cv2.GaussianBlur(bg, (0, 0), 25).astype(np.float32)
    norm = np.clip(v / np.maximum(bg, 1) * 255, 0, 255)
    out = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    out = np.clip(out / np.maximum(bg, 1) * 255, 0, 255)
    paper = (norm > level) & (s < 60)
    out[paper] = 255
    # gentle contrast stretch on the rest
    out = np.where(paper, 255, np.clip((out - 40) * 255 / (215 - 40), 0, 255))
    return out.astype(np.uint8)


def despeckle(g, min_area):
    """Paint out small isolated marks (show-through, pencil specks)."""
    ink = (g < 235).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(ink, 8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < min_area:
            g[lab == i] = 255
    return g


def trim(g, pad=5, thr=200):
    dark = g < thr
    rows = np.where(dark.sum(1) > 0)[0]
    cols = np.where(dark.sum(0) > 0)[0]
    y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad + 1, g.shape[0])
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad + 1, g.shape[1])
    return g[y0:y1, x0:x1]


def main():
    os.makedirs(FIG, exist_ok=True)
    only = sys.argv[1:]
    for name, spec in FIGS.items():
        if only and name not in only:
            continue
        src = os.path.join(SRC, spec["page"])
        if not os.path.exists(src):
            # the booklet photos are not shipped with the source bundle
            if os.path.exists(os.path.join(FIG, name + ".png")):
                print(f"{name}: page photo missing, keeping fig/{name}.png")
                continue
            raise SystemExit(f"{name}: neither {src} nor fig/{name}.png exists")
        im = cv2.imread(src)
        im = cv2.rotate(im, {"ccw": cv2.ROTATE_90_COUNTERCLOCKWISE,
                             "cw": cv2.ROTATE_90_CLOCKWISE}[spec["rot"]]) if spec["rot"] else im
        if spec.get("deskew"):
            h, w = im.shape[:2]
            m = cv2.getRotationMatrix2D((w / 2, h / 2), spec["deskew"], 1)
            im = cv2.warpAffine(im, m, (w, h), borderValue=(255, 255, 255))
        x0, y0, x1, y1 = spec["box"]
        g = whiten(im[y0:y1, x0:x1], spec.get("paper", 198))
        for rx0, ry0, rx1, ry1 in spec.get("mask", []):
            g[ry0:ry1, rx0:rx1] = 255
        if spec.get("circle"):
            # keep only the inside of the magnified circle (Hough fit)
            c = cv2.HoughCircles(cv2.GaussianBlur(g, (5, 5), 1.5), cv2.HOUGH_GRADIENT,
                                 dp=1, minDist=200, param1=80, param2=30,
                                 minRadius=100, maxRadius=140)
            cx, cy, r = c[0][0]
            yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
            g[(xx - cx) ** 2 + (yy - cy) ** 2 > (r + 4) ** 2] = 255
            # re-ink the circle outline on the fitted circle: the light-grey
            # printed outline does not survive the paper threshold
            cv2.circle(g, (int(round(cx)), int(round(cy))), int(round(r)), 40, 2, cv2.LINE_AA)
        g = despeckle(g, spec.get("speck", 150))
        g = trim(g)
        cv2.imwrite(os.path.join(FIG, name + ".png"), g)
        print(f"{name}: {g.shape[1]}x{g.shape[0]}")


if __name__ == "__main__":
    main()
