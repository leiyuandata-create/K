#!/usr/bin/env python3
"""sheet.py OUT.png IMG... -- contact sheet of images (or PDF pages as PDF:page) for one look."""
import sys

import pymupdf
from PIL import Image, ImageDraw


def load(spec, w):
    if ".pdf:" in spec:
        f, pg = spec.rsplit(":", 1)
        pix = pymupdf.open(f)[int(pg) - 1].get_pixmap(dpi=110)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    else:
        im = Image.open(spec).convert("RGB")
    s = w / im.width
    return im.resize((w, max(1, int(im.height * s))))


def main(out, specs, w=520, cols=3):
    ims = [load(s, w) for s in specs]
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    H = sum(max(i.height for i in r) + 30 for r in rows)
    sheet = Image.new("RGB", (cols * (w + 20), H), "white")
    d = ImageDraw.Draw(sheet)
    y, k = 0, 0
    for r in rows:
        for j, im in enumerate(r):
            sheet.paste(im, (j * (w + 20) + 10, y + 22))
            d.rectangle([j * (w + 20) + 10, y + 22, j * (w + 20) + 10 + w, y + 22 + im.height], outline="red")
            d.text((j * (w + 20) + 10, y + 4), specs[k].split("/")[-1], fill="black")
            k += 1
        y += max(i.height for i in r) + 30
    sheet.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
