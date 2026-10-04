#!/usr/bin/env python3
"""Computed coordinates for the TikZ figures, written to geom.tex (spec 3.4).

* Pure metal: identical atoms (radius r) in straight rows, touching.
* Alloy: the same rows with a few larger atoms (radius R) put in place of
  small ones. Small atoms that would overlap are pushed out by relaxation
  until no two circles overlap, so the rows really are bent around the
  large atoms (nothing placed by eye).
* Calcium chloride granules in the bottom of test tube A: packed inside the
  round bottom, each centre at least one granule radius inside the glass.
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "geom.tex")

R_SMALL, R_BIG = 0.5, 0.74
ROWS, COLS = 4, 8
BIG = [(1, 2), (2, 5), (0, 6)]        # (row, col) replaced by a large atom


def lattice():
    return [[(c * 2 * R_SMALL, r * 2 * R_SMALL) for c in range(COLS)] for r in range(ROWS)]


def alloy():
    atoms = []
    for r, row in enumerate(lattice()):
        for c, (x, y) in enumerate(row):
            big = (r, c) in BIG
            atoms.append([x, y, R_BIG if big else R_SMALL, big])
    for _ in range(400):
        moved = 0.0
        for i, a in enumerate(atoms):
            for j in range(i + 1, len(atoms)):
                b = atoms[j]
                dx, dy = b[0] - a[0], b[1] - a[1]
                d = math.hypot(dx, dy) or 1e-6
                need = a[2] + b[2] + 0.01
                if d < need:
                    push = (need - d)
                    ux, uy = dx / d, dy / d
                    # large atoms stay where they are; small ones move
                    wa = 0.0 if a[3] else (0.5 if not b[3] else 1.0)
                    wb = 0.0 if b[3] else (0.5 if not a[3] else 1.0)
                    a[0] -= ux * push * wa; a[1] -= uy * push * wa
                    b[0] += ux * push * wb; b[1] += uy * push * wb
                    moved += push
        if moved < 1e-4:
            break
    # assert: no overlaps remain
    for i, a in enumerate(atoms):
        for b in atoms[i + 1:]:
            assert math.hypot(a[0] - b[0], a[1] - b[1]) >= a[2] + b[2] - 1e-3
    return atoms


def granules(tube_r=0.8, g=0.17):
    """Granule centres inside a round tube bottom of radius tube_r (centre at
    (0, tube_r)), up to height 1.3*tube_r, hexagonal packing, each centre at
    least g inside the glass."""
    pts = []
    y = g + 0.02
    row = 0
    while y < 1.3 * tube_r:
        x = -tube_r + g + (g if row % 2 else 0)
        while x < tube_r - g:
            inside = (y >= tube_r and abs(x) <= tube_r - g) or \
                     (y < tube_r and math.hypot(x, y - tube_r) <= tube_r - g - 0.01)
            if inside:
                pts.append((x, y))
            x += 2 * g
        y += g * math.sqrt(3)
        row += 1
    return pts


def main():
    out = ["% geom.tex -- written by tools/geom.py; do not edit"]
    pure = [f"{x:.3f}/{y:.3f}" for row in lattice() for (x, y) in row]
    out.append("\\def\\geomPure{" + ",".join(pure) + "}")
    al = alloy()
    out.append("\\def\\geomAlloySmall{" + ",".join(f"{a[0]:.3f}/{a[1]:.3f}" for a in al if not a[3]) + "}")
    out.append("\\def\\geomAlloyBig{" + ",".join(f"{a[0]:.3f}/{a[1]:.3f}" for a in al if a[3]) + "}")
    out.append(f"\\def\\geomRs{{{R_SMALL}}}\\def\\geomRb{{{R_BIG}}}")
    out.append("\\def\\geomGranules{" + ",".join(f"{x:.3f}/{y:.3f}" for x, y in granules()) + "}")
    open(OUT, "w").write("\n".join(out) + "\n")
    print(f"geom.tex: {len(pure)} pure atoms, {len(al)} alloy atoms, {len(granules())} granules")


if __name__ == "__main__":
    main()
