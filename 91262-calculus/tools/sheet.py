#!/usr/bin/env python3
"""sheet.py <pdf> <out.png> [dpi] [cols]: contact sheet of every page (eyes on figures/overlays)."""
import sys, subprocess, tempfile, glob, cv2, numpy as np
pdf, out = sys.argv[1], sys.argv[2]
dpi = sys.argv[3] if len(sys.argv) > 3 else '40'; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 3
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['pdftoppm', '-r', dpi, '-png', pdf, d + '/p'], check=True)
    ims = [cv2.copyMakeBorder(cv2.imread(f), 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(0, 0, 255)) for f in sorted(glob.glob(d + '/p*.png'))]
h = max(i.shape[0] for i in ims); w = max(i.shape[1] for i in ims)
ims = [cv2.copyMakeBorder(i, 0, h - i.shape[0], 0, w - i.shape[1], cv2.BORDER_CONSTANT, value=(255, 255, 255)) for i in ims]
while len(ims) % cols: ims.append(np.full_like(ims[0], 255))
cv2.imwrite(out, np.vstack([np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)]))
