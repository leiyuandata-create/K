#!/usr/bin/env python3
"""Contact sheets of a PDF: tools/sheet.py file.pdf prefix [cols rows dpi]."""
import sys, os
import pymupdf, numpy as np, cv2
pdf, pre = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
rows = int(sys.argv[4]) if len(sys.argv) > 4 else 4
dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 60
doc = pymupdf.open(pdf)
ims = []
for k, page in enumerate(doc, 1):
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)[:, :, ::-1].copy()
    cv2.rectangle(im, (0, 0), (im.shape[1] - 1, im.shape[0] - 1), (160, 160, 160), 1)
    cv2.putText(im, str(k), (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
    ims.append(im)
per = cols * rows
for s in range(0, len(ims), per):
    chunk = ims[s:s + per]
    while len(chunk) % cols:
        chunk.append(np.full_like(ims[0], 255))
    grid = np.vstack([np.hstack(chunk[i:i + cols]) for i in range(0, len(chunk), cols)])
    cv2.imwrite(f"{pre}{s // per}.png", grid)
print(len(ims), "pages")
