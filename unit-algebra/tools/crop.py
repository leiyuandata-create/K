#!/usr/bin/env python3
"""crop.py N -- crops for lesson N's printed past-paper set (spec 3.7, 6.3).

Booklet questions go to fig/ppfull/ at natural size (300 dpi), schedule
rows to fig/ms/. Cuts come from the PDF's own label positions (text layer)
and, for schedule tables, from the table rules found by a pixel scan just
above the label -- never from coordinates read off a thumbnail.

Mode A (keep all text inside the clip) for every crop here: the text is
the question. Page headers and footers (which carry paper codes) are
outside every clip.
"""
import os
import sys

import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("PP_SOURCE", "/root/.claude/uploads/5ece282d-2012-5219-b8ca-64b9b001d1fa/"
                      "123c128b-91261-frm-2023_1_merge.pdf")
DPI = 300
FOOT = 800          # booklet footer line sits at y = 812; stop above it

# name: (page, kind, top anchor y, bottom anchor y)   y in PDF points
#   booklet: cut at top-8 and bottom-12, then trim white to 5 px
#   ms:      cut at the table rule just above each anchor
TABLE = {
    1: {
        "ppfull/q1": (10, "booklet", 55, 447),     # Q ONE (a)(i)(ii); stop before (b)
        "ppfull/q2": (13, "booklet", 55, FOOT),    # Q TWO (a)(b)
        "ppfull/q3": (16, "booklet", 55, FOOT),    # Q THREE stem, (a)
        "ppfull/q4": (17, "booklet", 54, FOOT),    # (b)
        "ppfull/q5": (18, "booklet", 54, FOOT),    # (c)
        "ppfull/q6": (33, "booklet", 55, FOOT),    # Q ONE (a)(b)(i)(ii)
        "ppfull/q7": (40, "booklet", 55, 169),     # Q THREE (a)(i); stop before (ii)
        "ms/q1": (3, "ms", 127, 232),              # header row .. before (b)
        "ms/q2": (5, "ms", 66, 269),               # header row .. before (c)(i)
        "ms/q3": (7, "ms", 68, 378),               # header row .. before (d)(i)
        "ms/q6": (25, "ms", 106, 359),             # header row .. before (c)(i)
        "ms/q7": (29, "ms", 49, 107),              # header row .. before (ii)
    },
}


def render(page, clip):
    pix = page.get_pixmap(dpi=DPI, clip=clip, colorspace=pymupdf.csGRAY, alpha=False)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).copy()


def rule_above(page, y, x0, x1, search=30):
    """y (pt) of the lowest horizontal table rule within `search` pt above y."""
    img = render(page, pymupdf.Rect(x0, y - search, x1, y))
    dark = (img < 140).mean(axis=1)
    rows = np.where(dark > 0.5)[0]
    if len(rows) == 0:
        return y - 4
    return y - search + rows[-1] * 72 / DPI


def trim(img, pad=5):
    ink = img < 200
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    r0, r1 = max(rows[0] - pad, 0), min(rows[-1] + pad + 1, img.shape[0])
    c0, c1 = max(cols[0] - pad, 0), min(cols[-1] + pad + 1, img.shape[1])
    return img[r0:r1, c0:c1]


def main(n):
    doc = pymupdf.open(SRC)
    for name, (pg, kind, top, bottom) in TABLE[int(n)].items():
        page = doc[pg - 1]
        if kind == "booklet":
            clip = pymupdf.Rect(36, top - 8, 562, bottom - 12)
        else:
            x0, x1 = 30, 566
            t = rule_above(page, top, x0, x1) - 1.5
            b = rule_above(page, bottom, x0, x1) + 1.5
            clip = pymupdf.Rect(x0, t, x1, b)
        img = trim(render(page, clip))
        out = os.path.join(HERE, "fig", name + ".png")
        Image.fromarray(img).save(out, dpi=(DPI, DPI))
        print(f"{name}.png  {img.shape[1] * 25.4 / DPI:.0f} x {img.shape[0] * 25.4 / DPI:.0f} mm")


if __name__ == "__main__":
    main(sys.argv[1])
