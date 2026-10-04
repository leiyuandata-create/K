#!/usr/bin/env python3
"""Label anchors for the booklet crops, written to fig/anchors.tex.

Arrow tails: inside a small search window around the printed leader's
tail, take the extreme dark pixel in the given direction (pixel scan, not
eye placement). Part targets for figures whose printed leaders were
cropped away (leaf): window centre refined to the darkest-outlined point
is not needed; the target is the window centre, checked on the contact
sheet. Coordinates are written as fractions of the crop size, y measured
upward, so the TikZ overlay scales with the image width.
"""
import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(HERE), "fig")

# fig: {label: (x0, y0, x1, y1, mode)}  window in crop pixels
# mode: "L"/"R"/"T" extreme dark pixel; "C" window centre (part target)
SPEC = {
    "flower": {
        "stigma": (40, 10, 90, 45, "L"), "style": (0, 115, 40, 145, "L"),
        "ovary": (0, 212, 40, 240, "L"), "anther": (320, 40, 364, 72, "R"),
        "filament": (300, 205, 364, 250, "R"), "sepal": (320, 320, 364, 377, "R"),
    },
    "seed": {
        "testa": (400, 8, 448, 32, "R"), "plumule": (400, 92, 448, 116, "R"),
        "radicle": (400, 186, 448, 210, "R"), "cotyledon": (0, 180, 40, 206, "L"),
    },
    "leaf": {
        "cuticle": (20, 6, 60, 18, "C"), "upper": (30, 26, 60, 44, "C"),
        "palisade": (18, 80, 38, 108, "C"), "spongy": (120, 156, 142, 176, "C"),
        "vein": (127, 278, 147, 298, "C"), "lower": (30, 382, 60, 400, "C"),
        "guard": (236, 398, 252, 414, "C"), "stoma": (283, 386, 299, 402, "C"),
    },
    "visking": {
        "capillary": (55, 40, 79, 64, "R"), "sucrose": (55, 432, 79, 450, "R"),
        "tubing": (55, 550, 79, 570, "R"),
    },
    "varleaf": {
        "green": (160, 0, 210, 20, "R"), "white": (170, 30, 215, 52, "R"),
    },
}


def tail(d, x0, y0, x1, y1, mode):
    if mode == "C":
        return (x0 + x1) / 2, (y0 + y1) / 2
    ys, xs = np.nonzero(d[y0:y1, x0:x1])
    if len(xs) == 0:
        raise SystemExit(f"no dark pixel in window {(x0, y0, x1, y1)}")
    k = {"L": np.argmin(xs), "R": np.argmax(xs), "T": np.argmin(ys)}[mode]
    return x0 + xs[k], y0 + ys[k]


def main():
    out = ["% fig/anchors.tex -- written by tools/anchors.py; do not edit"]
    for fig, labels in SPEC.items():
        g = cv2.imread(os.path.join(FIG, fig + ".png"), 0)
        h, w = g.shape
        d = g < 175
        out.append(f"\\def\\anc{fig}aspect{{{h / w:.4f}}}")
        for lab, win in labels.items():
            x, y = tail(d, *win)
            out.append(f"\\expandafter\\def\\csname anc@{fig}@{lab}\\endcsname"
                       f"{{{x / w:.4f},{(h - y) / w:.4f}}}")
    open(os.path.join(FIG, "anchors.tex"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
