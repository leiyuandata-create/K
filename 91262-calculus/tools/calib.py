#!/usr/bin/env python3
"""Grid calibration for past-paper graph crops (answer overlays are placed from these
numbers, never by eye).  For each grid: axis pixel positions, grid pitch, grid box, and
the printed curve sampled per column."""
import cv2, numpy as np, json, sys

def longest_run(v):
    best = cur = 0
    for t in v:
        cur = cur + 1 if t else 0
        best = max(best, cur)
    return best

def grid_box(a, y0, y1, x0=0, x1=None):
    """Bounding box of grey/dark grid lines in the window."""
    x1 = x1 or a.shape[1]
    w = a[y0:y1, x0:x1]
    g = w < 235
    cols = [x for x in range(w.shape[1]) if longest_run(g[:, x]) > 0.6 * (y1 - y0) * 0.5]
    rows = [y for y in range(w.shape[0]) if longest_run(g[y, :]) > 0.5 * (x1 - x0) * 0.5]
    return x0 + min(cols), y0 + min(rows), x0 + max(cols), y0 + max(rows), [x0 + c for c in cols], [y0 + r for r in rows]

def lines_from(idx):
    out = []
    for i in idx:
        if out and i - out[-1][-1] <= 2: out[-1].append(i)
        else: out.append([i])
    return [sum(o) / len(o) for o in out]

def calibrate(cid, y0, y1, x0=0, x1=None):
    a = cv2.imread('fig/ppfull/%s.png' % cid, 0)
    bx0, by0, bx1, by1, cols, rows = grid_box(a, y0, y1, x0, x1)
    d = a < 90
    ax_x = [x for x in range(bx0, bx1 + 1) if longest_run(d[by0:by1, x]) > 0.8 * (by1 - by0)]
    ax_y = [y for y in range(by0, by1 + 1) if longest_run(d[y, bx0:bx1]) > 0.8 * (bx1 - bx0)]
    vx = lines_from(cols); hy = lines_from(rows)
    pitch_x = float(np.median(np.diff(vx))); pitch_y = float(np.median(np.diff(hy)))
    return dict(cid=cid, box=[bx0, by0, bx1, by1], axis_x=float(np.mean(ax_x)) if ax_x else None,
                axis_y=float(np.mean(ax_y)) if ax_y else None, pitch_x=pitch_x, pitch_y=pitch_y,
                vlines=vx, hlines=hy)

def curve(cid, cal, thr=90):
    """Mean y of curve ink per column (axes and labels excluded)."""
    a = cv2.imread('fig/ppfull/%s.png' % cid, 0)
    bx0, by0, bx1, by1 = cal['box']
    pts = []
    for x in range(bx0 + 3, bx1 - 3):
        if cal['axis_x'] and abs(x - cal['axis_x']) < 6: continue
        ys = [y for y in range(by0 + 2, by1 - 2) if a[y, x] < thr and not (cal['axis_y'] and abs(y - cal['axis_y']) < 5)]
        if ys: pts.append((x, float(np.mean(ys)), len(ys)))
    return pts

if __name__ == '__main__':
    cid, y0, y1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    x0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    x1 = int(sys.argv[5]) if len(sys.argv) > 5 else None
    c = calibrate(cid, y0, y1, x0, x1)
    print(json.dumps({k: v for k, v in c.items() if k not in ('vlines', 'hlines')}))
    print('vlines', [round(v) for v in c['vlines']])
    print('hlines', [round(v) for v in c['hlines']])
