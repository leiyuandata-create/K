#!/usr/bin/env python3
"""Rotate a booklet photo upright and write a 100 px grid view (for locating
figures only; the crop itself is cut by pixel scan in crop.py)."""
import sys, cv2
src, rot, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = cv2.imread(src)
if rot == "cw":
    im = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)
elif rot == "ccw":
    im = cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)
x0, y0, x1, y1 = (int(v) for v in sys.argv[4:8]) if len(sys.argv) > 7 else (0, 0, im.shape[1], im.shape[0])
im = im[y0:y1, x0:x1].copy()
step = int(sys.argv[8]) if len(sys.argv) > 8 else 100
for x in range(0, im.shape[1], step):
    cv2.line(im, (x, 0), (x, im.shape[0]), (0, 0, 255), 1)
    cv2.putText(im, str(x + x0), (x + 2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
for y in range(0, im.shape[0], step):
    cv2.line(im, (0, y), (im.shape[1], y), (255, 0, 0), 1)
    cv2.putText(im, str(y + y0), (2, y + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
cv2.imwrite(out, im)
print(im.shape)
