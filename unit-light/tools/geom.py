#!/usr/bin/env python3
"""Compute every figure coordinate for the Light unit and write geom.tex.

Nothing in the TikZ figures is placed by eye: rays obey the law of
reflection, Snell's law (n1 sin i = n2 sin r) or the thin-lens equation,
and shadow edges are straight lines through the edges of source and object.
Each value is written as a \\def macro (\\g<Name>) that shared.sty reads.
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "geom.tex")
defs = []


def d(name, value):
    defs.append((name, value))


def dp(name, pt):
    d(name + "x", pt[0])
    d(name + "y", pt[1])


def rad(a):
    return math.radians(a)


def deg(a):
    return math.degrees(a)


def snell(n1, n2, i_deg):
    s = n1 * math.sin(rad(i_deg)) / n2
    if s >= 1:
        raise ValueError("total internal reflection: no refracted ray")
    return deg(math.asin(s))


def line_x(p, q, x):
    """y on the line p-q at abscissa x."""
    t = (x - p[0]) / (q[0] - p[0])
    return p[1] + t * (q[1] - p[1])


def circle_hit(p, direc, r, c=(0.0, 0.0)):
    """First forward intersection of ray p + t*direc (t>1e-9) with circle."""
    px, py = p[0] - c[0], p[1] - c[1]
    dx, dy = direc
    a = dx * dx + dy * dy
    b = 2 * (px * dx + py * dy)
    cc = px * px + py * py - r * r
    disc = b * b - 4 * a * cc
    ts = sorted([(-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)])
    t = [t for t in ts if t > 1e-9][0]
    return (p[0] + t * dx, p[1] + t * dy)


# ---------------------------------------------------------------- shadows
# Side view. Source at x=0, object (half-height H) at x=D, screen at x=L.
H, D, L = 0.8, 3.0, 6.0
d("ShObjH", H); d("ShObjX", D); d("ShScrX", L)
# point source: edge rays through object edges
d("ShPtEdge", H * L / D)                      # 1.6
# extended source of half-height A (a flat lamp face)
A = 1.0
d("ShSrcA", A)
d("ShUmbra", A + (H - A) * L / D)            # umbra edge on screen
d("ShPen", -A + (H + A) * L / D)             # outer penumbra edge on screen

# --------------------------------------------------------------- reflection
I_REFL = 40.0
Lr = 3.6
d("RefI", I_REFL)
dp("RefP", (-Lr * math.sin(rad(I_REFL)), Lr * math.cos(rad(I_REFL))))
dp("RefQ", (Lr * math.sin(rad(I_REFL)), Lr * math.cos(rad(I_REFL))))

# ---------------------------------------------------------- plane mirror image
# Mirror on x=0; object arrow at x=-OX from y=OB to y=OT; image at x=+OX.
OX, OB, OT = 2.5, -1.2, 1.2
d("PmOX", OX); d("PmOB", OB); d("PmOT", OT)
img = (OX, OT)
for k, (py, xend) in enumerate([(-0.2, -2.0), (-1.0, -2.0)], start=1):
    P = (0.0, py)
    yend = line_x(img, P, xend)
    dp(f"PmP{'AB'[k-1]}", P)
    dp(f"PmE{'AB'[k-1]}", (xend, yend))
    # check law of reflection: incident from object tip, reflected to end
    inc = (P[0] - (-OX), P[1] - OT)
    ref = (xend - P[0], yend - P[1])
    ai = deg(math.atan2(abs(inc[1]), abs(inc[0])))
    ar = deg(math.atan2(abs(ref[1]), abs(ref[0])))
    assert abs(ai - ar) < 1e-9, (ai, ar)

# -------------------------------------------------------------- periscope
# Mirrors on the lines x+y=6.1 (top) and x+y=1.1 (bottom): both at 45 deg.
dp("PsTopA", (0.1, 6.0)); dp("PsTopB", (1.1, 5.0))
dp("PsBotA", (0.1, 1.0)); dp("PsBotB", (1.1, 0.0))
dp("PsHitTop", (0.6, 5.5)); dp("PsHitBot", (0.6, 0.5))

# ------------------------------------------------------ refraction rules
N_GLASS = 1.5
I_R = 45.0
R_R = snell(1.0, N_GLASS, I_R)
d("RrI", I_R); d("RrR", R_R)
Lin, Lout = 2.4, 2.4
dp("RrIn", (-Lin * math.sin(rad(I_R)), Lin * math.cos(rad(I_R))))
dp("RrOut", (Lout * math.sin(rad(R_R)), -Lout * math.cos(rad(R_R))))

# -------------------------------------------------------- rectangular block
# Block top y=0, bottom y=-BH. Ray hits top at (0,0) with angle BI.
BH, BI = 2.4, 50.0
BR = snell(1.0, N_GLASS, BI)
d("BkH", BH); d("BkI", BI); d("BkR", BR)
exit_pt = (BH * math.tan(rad(BR)), -BH)
dp("BkIn", (-2.2 * math.sin(rad(BI)), 2.2 * math.cos(rad(BI))))
dp("BkExit", exit_pt)
dp("BkOut", (exit_pt[0] + 2.2 * math.sin(rad(BI)), exit_pt[1] - 2.2 * math.cos(rad(BI))))
# extension of the original ray (dashed) to show the sideways shift
dp("BkStraight", (BH * math.tan(rad(BI)), -BH))
# in-class version (different angle; answer drawn in red)
BI2 = 35.0
BR2 = snell(1.0, N_GLASS, BI2)
d("BkbI", BI2); d("BkbR", BR2)
ex2 = (BH * math.tan(rad(BR2)), -BH)
dp("BkbIn", (-2.2 * math.sin(rad(BI2)), 2.2 * math.cos(rad(BI2))))
dp("BkbExit", ex2)
dp("BkbOut", (ex2[0] + 2.0 * math.sin(rad(BI2)), ex2[1] - 2.0 * math.cos(rad(BI2))))

# ---------------------------------------------------------- semicircle
SR = 2.4
SI = 45.0
SRr = snell(1.0, N_GLASS, SI)
d("ScR", SR); d("ScI", SI); d("ScRr", SRr)
dp("ScIn", (-2.0 * math.sin(rad(SI)), 2.0 * math.cos(rad(SI))))
curved = (SR * math.sin(rad(SRr)), -SR * math.cos(rad(SRr)))
dp("ScHit", curved)
dp("ScOut", (curved[0] + 1.3 * math.sin(rad(SRr)), curved[1] - 1.3 * math.cos(rad(SRr))))


# --------------------------------------------------------- apparent depth
def apparent(name, fish, angles, n, top_len):
    """Rays leave `fish` (below y=0) at the given water angles, refract at
    y=0 and travel `top_len` in air. Back-extensions of the two rays meet
    at the image. Writes surface points, air ends and the image."""
    pts = []
    for k, aw in enumerate(angles):
        sx = fish[0] + (-fish[1]) * math.tan(rad(aw))
        aa = snell(n, 1.0, aw)
        end = (sx + top_len * math.sin(rad(aa)), top_len * math.cos(rad(aa)))
        pts.append((sx, aa))
        dp(f"{name}S{'AB'[k]}", (sx, 0.0))
        dp(f"{name}E{'AB'[k]}", end)
    (x1, a1), (x2, a2) = pts
    # back-extension: x = xk + y*tan(ak) for y<0
    y = (x2 - x1) / (math.tan(rad(a1)) - math.tan(rad(a2)))
    x = x1 + y * math.tan(rad(a1))
    dp(f"{name}Img", (x, y))
    return (x, y)


N_WATER = 1.33
dp("FiFish", (0.0, -2.6))
apparent("Fi", (0.0, -2.6), [30.0, 38.0], N_WATER, 2.6)


def fish_to_eye(name, fish, eye, n, delta=0.6):
    """Single refracted ray from fish to eye (solve for surface point by
    bisection on Snell's law), plus the image from a pair of neighbouring
    rays straddling it."""
    fx, fy = fish
    ex, ey = eye

    def mismatch(sx):
        aw = math.atan2(sx - fx, -fy)
        aa = math.atan2(ex - sx, ey)
        return n * math.sin(aw) - math.sin(aa)

    lo, hi = fx + 1e-6, ex - 1e-6
    for _ in range(200):
        mid = (lo + hi) / 2
        if mismatch(lo) * mismatch(mid) <= 0:
            hi = mid
        else:
            lo = mid
    sx = (lo + hi) / 2
    dp(f"{name}S", (sx, 0.0))
    aw = deg(math.atan2(sx - fx, -fy))
    xs = []
    for a in (aw - delta, aw + delta):
        xk = fx + (-fy) * math.tan(rad(a))
        xs.append((xk, snell(n, 1.0, a)))
    (x1, a1), (x2, a2) = xs
    y = (x2 - x1) / (math.tan(rad(a1)) - math.tan(rad(a2)))
    x = x1 + y * math.tan(rad(a1))
    dp(f"{name}Img", (x, y))
    d(f"{name}Aw", aw)
    d(f"{name}Aa", deg(math.atan2(ex - sx, ey)))


# in-class: spear fisher
dp("SpFish", (0.0, -2.2)); dp("SpEye", (4.6, 2.6))
fish_to_eye("Sp", (0.0, -2.2), (4.6, 2.6), N_WATER)
# homework: pool floor coin
dp("PoFish", (0.0, -2.8)); dp("PoEye", (5.0, 2.4))
fish_to_eye("Po", (0.0, -2.8), (5.0, 2.4), N_WATER)

# ------------------------------------------------------------- prism
# Equilateral prism, side S, base on y=0 from (0,0) to (S,0).
S = 4.0
apex = (S / 2, S * math.sqrt(3) / 2)
dp("PrApex", apex)
d("PrS", S)
# entry point on left face, 45% of the way up
t_in = 0.45
P_in = (apex[0] * t_in, apex[1] * t_in)
dp("PrIn", P_in)
# incoming white ray direction (angle above horizontal)
in_dir_deg = -12.0    # slightly downward before entry? use upward entry
in_dir_deg = 18.0
# Exaggerated spread so the fan is visible; named in the delivery note.
colours = [("red", 1.48), ("orange", 1.52), ("yellow", 1.56), ("green", 1.60),
           ("blue", 1.64), ("indigo", 1.68), ("violet", 1.72)]


def refract_vec(v, nrm, n1, n2):
    """Vector Snell. nrm points towards the incident side (unit)."""
    vx, vy = v
    nx, ny = nrm
    cosi = -(vx * nx + vy * ny)
    eta = n1 / n2
    k = 1 - eta * eta * (1 - cosi * cosi)
    if k < 0:
        raise ValueError("TIR")
    a = eta * cosi - math.sqrt(k)
    return (eta * vx + a * nx, eta * vy + a * ny)


vin = (math.cos(rad(in_dir_deg)), math.sin(rad(in_dir_deg)))
start = (P_in[0] - 2.4 * vin[0], P_in[1] - 2.4 * vin[1])
dp("PrStart", start)
n_left = (-math.sqrt(3) / 2, 0.5)     # outward normal of left face
n_right = (math.sqrt(3) / 2, 0.5)     # outward normal of right face
for k, (cname, n) in enumerate(colours):
    v1 = refract_vec(vin, n_left, 1.0, n)
    # intersect with right face: points apex + s*((S,0)-apex)
    bx, by = S - apex[0], 0 - apex[1]
    # P_in + t v1 = apex + s (bx,by)
    det = v1[0] * (-by) - v1[1] * (-bx)
    rx, ry = apex[0] - P_in[0], apex[1] - P_in[1]
    t = (rx * (-by) - ry * (-bx)) / det
    P_out = (P_in[0] + t * v1[0], P_in[1] + t * v1[1])
    # inside the prism, the normal towards the incident side is -n_right
    v2 = refract_vec(v1, (-n_right[0], -n_right[1]), n, 1.0)
    end = (P_out[0] + 3.0 * v2[0], P_out[1] + 3.0 * v2[1])
    dp(f"PrOut{'abcdefg'[k]}", P_out)
    dp(f"PrEnd{'abcdefg'[k]}", end)

# ----------------------------------------------------------------- eye
R_EYE = 2.2
C_CX, C_R = -1.55, 1.05
# sclera / cornea junction
xj = (C_R ** 2 - R_EYE ** 2 - C_CX ** 2) / (2 * C_CX) * -1
# solve (x - C_CX)^2 - x^2 = C_R^2 - R^2  ->  -2 C_CX x + C_CX^2 = C_R^2 - R^2
xj = (C_CX ** 2 - (C_R ** 2 - R_EYE ** 2)) / (2 * C_CX)
yj = math.sqrt(R_EYE ** 2 - xj ** 2)
d("EyR", R_EYE); d("EyCx", C_CX); d("EyCr", C_R)
d("EyScA", deg(math.atan2(yj, xj)))            # sclera arc end angle
d("EyCoA", deg(math.atan2(yj, xj - C_CX)))     # cornea arc start angle
d("EyCoB", 360 - deg(math.atan2(yj, xj - C_CX)))
d("EyLensX", -1.25); d("EyLensRx", 0.30); d("EyLensRy", 0.78)
d("EyIrisX", -1.62)
d("EyIrisIn", 0.42)
d("EyIrisOut", math.sqrt(R_EYE ** 2 - 1.62 ** 2) - 0.12)
R_RET = 2.05
d("EyRet", R_RET)
NERVE = -20.0
d("EyNerve", NERVE)
dp("EyBlind", (R_RET * math.cos(rad(NERVE)), R_RET * math.sin(rad(NERVE))))
for tag, a in (("NA", NERVE + 6.5), ("NB", NERVE - 6.5)):
    p = (R_EYE * math.cos(rad(a)), R_EYE * math.sin(rad(a)))
    dp(f"Ey{tag}", p)
    dp(f"Ey{tag}e", (p[0] + 1.3 * math.cos(rad(NERVE)), p[1] + 1.3 * math.sin(rad(NERVE))))
dp("EyFovea", (R_RET, 0.0))
# label anchors on the parts (leader lines end exactly on these)
dp("EyCorneaPt", (C_CX + C_R * math.cos(rad(140)), C_R * math.sin(rad(140))))
dp("EyRetinaPt", (R_RET * math.cos(rad(55)), R_RET * math.sin(rad(55))))
dp("EyScleraPt", (R_EYE * math.cos(rad(-60)), R_EYE * math.sin(rad(-60))))
dp("EyNervePt", (R_EYE * math.cos(rad(NERVE)) + 0.9 * math.cos(rad(NERVE)),
                 R_EYE * math.sin(rad(NERVE)) + 0.9 * math.sin(rad(NERVE))))
dp("EyLensPt", (-1.25 + 0.30 * math.cos(rad(-60)), 0.78 * math.sin(rad(-60))))


# -------------------------------------------------------- eye defects
# Small eye: radius RE, eye lens at x=XL, retina back point (RE,0).
RE, XL, XG = 1.5, -1.0, -2.6
d("EdR", RE); d("EdL", XL); d("EdG", XG)
back = RE - XL                                   # lens-to-retina distance 2.5
Y0 = 0.4


def eye_defect(tag, f_eye, f_glass):
    # uncorrected: parallel rays at +-Y0 through lens, focus at XL+f_eye
    fx = XL + f_eye
    d(f"{tag}F", fx)
    for s, lab in ((1, "U"), (-1, "D")):
        p = (XL, s * Y0)
        direc = (fx - XL, -s * Y0)
        hit = circle_hit(p, direc, RE)
        dp(f"{tag}Hit{lab}", hit)
    # corrected: glasses at XG with focal length f_glass (negative = concave)
    # after glasses the ray heads from/to point (XG + f_glass, 0)
    gy = Y0
    fp = XG + f_glass
    y_at_lens = gy + (XL - XG) * (-gy / (fp - XG)) if f_glass > 0 else \
        gy + (XL - XG) * (gy / (XG - fp))
    d(f"{tag}Yl", y_at_lens)
    # check that eye lens then focuses on the retina (thin-lens equation)
    u = (XL - fp)            # object distance (virtual source on the left)
    v_target = back
    if f_glass < 0:
        v = 1 / (1 / f_eye - 1 / u)
    else:
        u2 = fp - XL         # rays converge towards a point behind the lens
        v = 1 / (1 / f_eye + 1 / u2)
    assert abs(v - v_target) < 1e-6, (tag, v, v_target)
    d(f"{tag}Gp", fp)


def glass_for(f_eye, concave):
    if concave:
        u = 1 / (1 / f_eye - 1 / back)       # virtual object distance needed
        return -(u - (XL - XG))
    u2 = 1 / (1 / back - 1 / f_eye)
    return u2 + (XL - XG)


F_MY, F_HY = 1.8, 3.2
d("MyFeye", F_MY); d("HyFeye", F_HY)
eye_defect("My", F_MY, glass_for(F_MY, True))
eye_defect("Hy", F_HY, glass_for(F_HY, False))
# hyperopia: where the uncorrected rays are when they reach the retina
d("HyRetY", Y0 * (1 - back / F_HY))

# ----------------------------------------------------------------- lenses
d("CvThinF", 3.2); d("CvThickF", 1.8)
# extension: object outside 2F
f, u, h = 2.0, 5.0, 1.2
v = 1 / (1 / f - 1 / u)
d("LrF", f); d("LrU", u); d("LrH", h); d("LrV", v); d("LrHi", -h * v / u)
# extension: magnifying glass (object inside F)
f2, u2, h2 = 3.0, 2.0, 0.8
v2 = 1 / (1 / f2 - 1 / u2)            # negative -> virtual
d("MgF", f2); d("MgU", u2); d("MgH", h2); d("MgV", v2); d("MgHi", -h2 * v2 / u2)
# the image is on the object side: x = v2 (negative), height h2*|v2|/u2
assert v2 < 0

# ------------------------------------------------ in-class reflection task
# Ray meets a horizontal mirror at 30 deg to the SURFACE -> i = 60.
ang_surface = 30.0
i_ic = 90 - ang_surface
d("IcAs", ang_surface); d("IcI", i_ic)
dp("IcIn", (-3.4 * math.cos(rad(ang_surface)), 3.4 * math.sin(rad(ang_surface))))
dp("IcOut", (3.4 * math.cos(rad(ang_surface)), 3.4 * math.sin(rad(ang_surface))))

# homework: 20 deg to the surface
dp("HwIn", (-3.4 * math.cos(rad(20)), 3.4 * math.sin(rad(20))))
dp("HwOut", (3.4 * math.cos(rad(20)), 3.4 * math.sin(rad(20))))

# ------------------------------------------ in-class plane mirror triangle
tri = {"A": (-1.6, 1.8), "B": (-3.4, 0.4), "C": (-1.0, -0.2)}
for k, p in tri.items():
    dp(f"Tr{k}", p)
    dp(f"Tr{k}i", (-p[0], p[1]))
eye = (-4.2, -2.4)
dp("TrEye", eye)
A_img = (-tri["A"][0], tri["A"][1])
# two rays from A to the eye (top and bottom of the eye, 0.25 apart)
for tag, e in (("U", (eye[0], eye[1] + 0.22)), ("D", (eye[0], eye[1] - 0.22))):
    P = (0.0, line_x(A_img, e, 0.0))
    dp(f"TrP{tag}", P)
    dp(f"TrE{tag}", e)

for name, _ in defs:
    assert name.isalpha(), f"TeX macro names must be letters only: {name}"
with open(OUT, "w") as fh:
    fh.write("% generated by tools/geom.py -- do not edit\n")
    for name, value in defs:
        fh.write(f"\\def\\g{name}{{{value:.4f}}}\n")
print(f"wrote {len(defs)} values to {os.path.normpath(OUT)}")
