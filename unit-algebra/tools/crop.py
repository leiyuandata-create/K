#!/usr/bin/env python3
"""crop.py N -- crops for lesson N's printed past-paper set (spec 3.7, 6.3).

Booklet questions go to fig/L<N>/ppfull/ at natural size (300 dpi), schedule
rows to fig/L<N>/ms/. Cuts come from the PDF's own label positions (text layer)
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
END = 795           # schedule: the last rule within 45 pt above this

# name: (page, kind, top anchor y, bottom anchor y)   y in PDF points
#   booklet: cut at top-8 and bottom-12, then trim white to 5 px
#   ms:      cut at the table rule just above each anchor
# name: (page, "ms", [(top, bottom), ...]): several row bands of one page
#   stacked (the header row, then the rows wanted), each cut at its rules.
#   A bottom anchor of END finds the last table rule above the footer.
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
    2: {
        "ppfull/q1": (14, "booklet", 54, FOOT, 236),   # 2021 Q TWO (c) stem, (i), (ii); under the header
        "ppfull/q2": (15, "booklet", 54, FOOT, 255),   # Rule of 72, (iii)
        "ppfull/q3": (40, "booklet", 169, FOOT),   # 2022 Q THREE (a)(ii), (b)
        "ppfull/q4": (41, "booklet", 54, FOOT, 255),   # (c)(i)
        "ppfull/q5": (42, "booklet", 55, FOOT),    # (c)(ii)
        "ms/q1": (5, "ms", [(66, 111), (269, END)]),        # header + (c)(i)(ii)(iii)
        "ms/q3": (29, "ms", [(49, 72), (107, 327)]),        # header + (a)(ii), (b)
        "ms/q4": (29, "ms", [(49, 72), (327, 479)]),        # header + (c)(i)
        "ms/q5": (29, "ms", [(49, 72), (479, 697)]),        # header + (c)(ii); stop above the grade row
    },
}


def render(page, clip):
    pix = page.get_pixmap(dpi=DPI, clip=clip, colorspace=pymupdf.csGRAY, alpha=False)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).copy()


def rule_above(page, y, x0, x1, search=30):
    if y == END:
        y, search = END, 45
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


def cap_space(img, max_mm):
    """Cap every run of blank rows (no ink at all) at the largest cap that keeps
    the crop within max_mm (spec 5.5, 6.3). Answer lines are ink, so they stay;
    nothing of the question is removed and nothing is scaled."""
    blank = ~(img < 200).any(axis=1)
    runs, start = [], None
    for i, b in enumerate(blank):
        if b and start is None:
            start = i
        if not b and start is not None:
            runs.append((start, i)); start = None
    if start is not None:
        runs.append((start, len(blank)))
    limit = max_mm / 25.4 * DPI
    for cap_mm in [x / 2 for x in range(80, 5, -1)]:
        cap = int(cap_mm / 25.4 * DPI)
        h = img.shape[0] - sum(max(0, (b - a) - cap) for a, b in runs)
        if h <= limit:
            keep = np.ones(img.shape[0], bool)
            for a, b in runs:
                if b - a > cap:
                    keep[a + cap:b] = False
            return img[keep]
    raise SystemExit(f"cannot fit within {max_mm} mm by capping white space")


def main(n):
    for sub in ("ppfull", "ms"):
        os.makedirs(os.path.join(HERE, "fig", f"L{n}", sub), exist_ok=True)
    doc = pymupdf.open(SRC)
    for name, spec in TABLE[int(n)].items():
        if len(spec) == 3:
            pg, kind, bands = spec
            page = doc[pg - 1]
            x0, x1 = 30, 566
            parts = []
            for top, bottom in bands:
                t = rule_above(page, top, x0, x1) - 1.5
                b = rule_above(page, bottom, x0, x1) + 1.5
                parts.append(render(page, pymupdf.Rect(x0, t, x1, b)))
            img = trim(np.vstack(parts))
            out = os.path.join(HERE, "fig", f"L{n}", name + ".png")
            Image.fromarray(img).save(out, dpi=(DPI, DPI))
            print(f"{name}.png  {img.shape[1] * 25.4 / DPI:.0f} x {img.shape[0] * 25.4 / DPI:.0f} mm")
            continue
        pg, kind, top, bottom, *rest = spec
        page = doc[pg - 1]
        if kind == "booklet":
            clip = pymupdf.Rect(36, top - 8, 562, bottom - 12)
        else:
            x0, x1 = 30, 566
            t = rule_above(page, top, x0, x1) - 1.5
            b = rule_above(page, bottom, x0, x1) + 1.5
            clip = pymupdf.Rect(x0, t, x1, b)
        img = trim(render(page, clip))
        if rest:
            img = cap_space(img, rest[0])
        out = os.path.join(HERE, "fig", f"L{n}", name + ".png")
        Image.fromarray(img).save(out, dpi=(DPI, DPI))
        print(f"{name}.png  {img.shape[1] * 25.4 / DPI:.0f} x {img.shape[0] * 25.4 / DPI:.0f} mm")


if __name__ == "__main__":
    main(sys.argv[1])
