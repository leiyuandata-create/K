#!/usr/bin/env python3
"""Crop exam-paper parts for the printed practice sets (spec 3.7, 5.5, 6.3).

* Regions come from the text layer: the y of each part label, the footer line at y=812
  and the hatched strip at x>556 pt are read from the PDF, never guessed.
* Output is natural size (300 dpi, width = 521 pt = 184 mm), for A4 sheets with
  12 mm side margins, so nothing is shrunk.
* The "If you need to redraw ... page 12" callouts are removed (they point at pages that
  do not exist in our sets); footers, page numbers and QUESTION headings are outside the
  crops.
* Whitespace runs (blank rows and the light-grey answer rules) are capped at the largest
  cap that keeps the part on one A4 page.  Rule positions after compression are written
  to <id>.tex so answer overlays sit on the rules.
"""
import json, os, sys
import numpy as np
import pymupdf as fitz
import cv2

UP = '/root/.claude/uploads/6a876be3-23aa-5e8f-9c18-b92963ea9869/'
SRC = {'21': UP + 'ceb38c27-91262-exm-2021.pdf', '22': UP + '7037cfcd-91262-exm-2022_1.pdf'}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fig', 'ppfull')
DPI = 300
X0, X1 = 35, 556           # content column (hatched strip starts right of 556 pt)
FOOT = 800                 # footer text sits at y = 812 pt
INK = 150                  # darker than this = content (answer rules are grey 189)
MAX_H_MM = 236             # practice/homework text height is 246 mm (measured); minus the question heading

# id, paper, page (1-based), y0, y1  (y0/y1 in pt, from the label positions)
CROPS = [
    # lesson 1
    ('a21_1a', '21', 2, 72, 334), ('a21_1b', '21', 2, 332, FOOT), ('a21_2b', '21', 6, 46, 318),
    ('a22_1a', '22', 2, 72, 350), ('a22_1d', '22', 3, 452, FOOT), ('a22_3a', '22', 8, 72, 269),
    # lesson 2
    ('a22_1c', '22', 3, 60, 450), ('a22_2b', '22', 6, 46, 398), ('a21_1c', '21', 3, 46, FOOT),
    ('a21_3d', '21', 10, 46, FOOT), ('a22_1e', '22', 4, 46, FOOT),
    # lesson 3
    ('a21_2a', '21', 5, 72, FOOT), ('a21_3c', '21', 9, 46, FOOT), ('a22_2a', '22', 5, 72, FOOT),
    ('a22_3b1', '22', 8, 269, FOOT), ('a22_3b2', '22', 9, 46, FOOT),
    # lesson 4
    ('a21_3a', '21', 8, 72, 376), ('a21_3b', '21', 8, 376, FOOT), ('a21_2c1', '21', 6, 318, FOOT),
    ('a21_2c2', '21', 7, 60, FOOT), ('a22_1b', '22', 2, 350, FOOT), ('a22_2c', '22', 6, 398, FOOT),
    # lesson 5
    ('a21_1c3', '21', 4, 46, FOOT), ('a21_3d2', '21', 11, 46, FOOT), ('a22_2c3', '22', 7, 46, FOOT),
    ('a22_3c', '22', 10, 46, FOOT),
]


def callout_rects(page, clip):
    """Rectangles (pt) around 'If you need to ... redraw' callouts inside clip."""
    ws = page.get_text('words')
    rects = []
    for i, w in enumerate(ws):
        if w[4] == 'If' and i + 2 < len(ws) and ws[i + 1][4] == 'you' and ws[i + 2][4] == 'need':
            r = fitz.Rect(w[:4])
            for w2 in ws[i:i + 30]:
                r2 = fitz.Rect(w2[:4])
                if abs(r2.x0 - r.x0) < 60 and 0 <= r2.y0 - r.y1 < 70:
                    r |= r2
            if r.intersects(clip):
                rects.append(r)
    return rects


def whiten_callout(a, r, clip):
    """Whiten the callout: find the closed border component whose box contains the
    'If' word, then whiten everything inside that box (border included)."""
    s = DPI / 72
    cx = (r.x0 + 4 - clip.x0) * s; cy = (r.y0 + 4 - clip.y0) * s
    n, lab, st, _ = cv2.connectedComponentsWithStats((a < 200).astype(np.uint8), connectivity=8)
    best = None
    for k in range(1, n):
        x, y, w, h, _ = st[k]
        if x < cx < x + w and y < cy < y + h and w < 220 * s and h < 140 * s:
            if best is None or w * h > best[2] * best[3]:
                best = (x, y, w, h)
    if best is None:
        raise SystemExit('callout border not found near %s' % r)
    x, y, w, h = best
    a[max(y - 3, 0):y + h + 3, max(x - 3, 0):x + w + 3] = 255


def trim(a):
    ys, xs = np.where(a < 235)
    y0, y1 = max(ys.min() - 5, 0), min(ys.max() + 6, a.shape[0])
    x0, x1 = max(xs.min() - 5, 0), min(xs.max() + 6, a.shape[1])
    return a[y0:y1, x0:x1]


def compress(a, cap):
    content = (a < INK).any(1)
    keep, run = [], []
    for y in range(a.shape[0]):
        if content[y]:
            keep += run[:cap]; run = []; keep.append(y)
        else:
            run.append(y)
    keep += run[:cap]
    return a[keep]


def rule_rows(a):
    """y of each light-grey answer rule (rows mostly grey, no ink)."""
    grey = ((a > 150) & (a < 225)).sum(1)
    ys = [y for y in range(a.shape[0]) if grey[y] > 0.5 * a.shape[1] and not (a[y] < INK).any()]
    rows = []
    for y in ys:
        if rows and y - rows[-1][-1] <= 2:
            rows[-1].append(y)
        else:
            rows.append([y])
    return [int(round(sum(r) / len(r))) for r in rows]


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    docs = {k: fitz.open(v) for k, v in SRC.items()}
    report = []
    for cid, paper, pno, y0, y1 in CROPS:
        if only and cid not in only:
            continue
        page = docs[paper][pno - 1]
        clip = fitz.Rect(X0, y0, X1, y1)
        pix = page.get_pixmap(dpi=DPI, clip=clip, colorspace=fitz.csGRAY, alpha=False)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w).copy()
        for r in callout_rects(page, clip):
            whiten_callout(a, r, clip)
        a = trim(a)
        maxpx = int(MAX_H_MM / 25.4 * DPI)
        cap = 2000
        b = compress(a, cap)
        while b.shape[0] > maxpx and cap > 20:
            cap -= 10
            b = compress(a, cap)
        rules = rule_rows(b)
        rx = [int(np.argmax((b[y] > 150) & (b[y] < 225))) for y in rules]
        cv2.imwrite(os.path.join(OUT, cid + '.png'), b)
        info = dict(id=cid, w=int(b.shape[1]), h=int(b.shape[0]), cap=cap, rules=rules,
                    w_mm=round(b.shape[1] / DPI * 25.4, 1), h_mm=round(b.shape[0] / DPI * 25.4, 1))
        with open(os.path.join(OUT, cid + '.json'), 'w') as f:
            json.dump(info, f)
        # TeX side: size and rule positions (px) for overlays
        with open(os.path.join(OUT, cid + '.tex'), 'w') as f:
            f.write('\\expandafter\\def\\csname pp@w@%s\\endcsname{%d}\n' % (cid, b.shape[1]))
            f.write('\\expandafter\\def\\csname pp@h@%s\\endcsname{%d}\n' % (cid, b.shape[0]))
            for k, (y, x0) in enumerate(zip(rules, rx), 1):
                f.write('\\expandafter\\def\\csname pp@r@%s@%d\\endcsname{%d}\n' % (cid, k, y))
                f.write('\\expandafter\\def\\csname pp@x@%s@%d\\endcsname{%d}\n' % (cid, k, x0))
        report.append('%-9s %4.0f x %5.1f mm  cap=%4d  rules=%d' % (cid, info['w_mm'], info['h_mm'], cap, len(rules)))
    print('\n'.join(report))


if __name__ == '__main__':
    main()
