#!/usr/bin/env python3
"""Label anchors for the booklet crops, written to fig/anchors.tex.

Arrow tails (mode R): inside a search window around the printed leader's
tail, the right-most dark pixel (pixel scan, not eye placement).
Number discs (mode N): the printed black disc near the given point is
found as the dark connected component of disc size after closing the
white digit; its centroid is the anchor. Mode W (a disc lying inside a
dark region): centroid of the white digit instead.
Coordinates are fractions of the crop width, y measured upward, so the
TikZ overlay scales with the image width.
"""
import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(HERE), "fig")

SPEC = {
    # male front view (booklet p.10): tails of the eight printed arrows
    "mfront": {
        "bladder": (430, 70, 485, 96, "R"), "seminal": (470, 202, 525, 226, "R"),
        "prostate": (495, 234, 538, 256, "R"), "spermduct": (500, 277, 538, 298, "R"),
        "urethra": (395, 336, 455, 357, "R"), "epididymis": (395, 403, 455, 425, "R"),
        "testis": (415, 459, 470, 472, "R"), "scrotum": (415, 473, 470, 486, "R"),
    },
    # female side view (booklet p.8): the ten printed number discs
    "fside": {
        "n1": (267, 81, "N"), "n2": (212, 92, "N"), "n3": (216, 222, "N"),
        "n4": (225, 304, "N"), "n5": (266, 158, "N"), "n6": (382, 166, "W"),
        "n7": (154, 359, "N"), "n8": (201, 272, "N"), "n9": (311, 344, "N"),
        "n10": (303, 224, "N"),
    },
}


def tail(g, x0, y0, x1, y1):
    ys, xs = np.nonzero(g[y0:y1, x0:x1] < 175)
    if len(xs) == 0:
        raise SystemExit(f"no dark pixel in window {(x0, y0, x1, y1)}")
    k = np.argmax(xs)
    return x0 + xs[k], y0 + ys[k]


def disc(g, x, y, mode, r=15):
    y0, x0 = max(y - r, 0), max(x - r, 0)
    w = g[y0:y + r + 1, x0:x + r + 1]
    if mode == "W":
        yy, xx = np.mgrid[:w.shape[0], :w.shape[1]]
        m = (w > 170) & ((xx - (x - x0)) ** 2 + (yy - (y - y0)) ** 2 <= 9 ** 2)
        ys, xs = np.nonzero(m)
        return x0 + xs.mean(), y0 + ys.mean()
    dark = (w < 80).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    n, lab, st, cen = cv2.connectedComponentsWithStats(dark, 8)
    best = None
    for i in range(1, n):
        d = np.hypot(cen[i][0] - (x - x0), cen[i][1] - (y - y0))
        if best is None or d < best[0]:
            best = (d, cen[i])
    if best is None:
        raise SystemExit(f"no disc near {(x, y)}")
    return x0 + best[1][0], y0 + best[1][1]


def main():
    out = ["% fig/anchors.tex -- written by tools/anchors.py; do not edit"]
    for fig, labels in SPEC.items():
        g = cv2.imread(os.path.join(FIG, fig + ".png"), 0)
        h, w = g.shape
        chk = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
        out.append(f"\\def\\anc{fig}aspect{{{h / w:.4f}}}")
        for lab, win in labels.items():
            x, y = tail(g, *win[:4]) if win[-1] == "R" else disc(g, win[0], win[1], win[2])
            cv2.circle(chk, (int(round(x)), int(round(y))), 11 if win[-1] != "R" else 3, (0, 0, 255), 1)
            out.append(f"\\expandafter\\def\\csname anc@{fig}@{lab}\\endcsname"
                       f"{{{x / w:.4f},{(h - y) / w:.4f}}}")
        os.makedirs(os.path.join(os.path.dirname(FIG), "src", "view"), exist_ok=True)
        cv2.imwrite(os.path.join(os.path.dirname(FIG), "src", "view", fig + "_anchors.png"),
                    cv2.resize(chk, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC))
    open(os.path.join(FIG, "anchors.tex"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
