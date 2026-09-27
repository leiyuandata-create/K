#!/usr/bin/env python3
"""Every numerical answer in the unit, checked with sympy.  Run before each build.
Keys: L<n>-<file>-<item>.  An assertion failure names the item."""
from sympy import symbols, diff, integrate, solve, Rational as R, sqrt, simplify, expand, pi, nsimplify, Eq
x, t, a, b, c, k, p, q, d = symbols('x t a b c k p q d', real=True)
ok = 0
def chk(name, got, want):
    global ok
    if simplify(got - want) != 0:
        raise AssertionError('%s: got %s, want %s' % (name, got, want))
    ok += 1
def roots(expr, var=x):
    return sorted(solve(expr, var), key=lambda r: float(r))
def tangent(f, x0):
    m = diff(f, x).subs(x, x0); y0 = f.subs(x, x0)
    return expand(m * (x - x0) + y0)
def F(fp, pt):   # anti-derivative through point
    G = integrate(fp, x); cc = solve(Eq(G.subs(x, pt[0]) + c, pt[1]), c)[0]
    return expand(G + cc)

# ---------------- Lesson 1 ----------------
chk('L1-DN1', R(12 - 3, 4 - 1), 3)
chk('L1-DN2', expand(3*x*(x - 4)), 3*x**2 - 12*x)
chk('L1-DN3', -2*(x - 3) + 5, -2*x + 11)
chk('L1-DN4', roots(x**2 - 5*x + 6)[0] + 10*roots(x**2 - 5*x + 6)[1], 2 + 30)
chk('L1-WE1', diff(3*x**4 - 5*x**2 + 7*x - 2, x), 12*x**3 - 10*x + 7)
chk('L1-WE2', diff(expand((2*x + 1)*(x - 3)), x), 4*x - 5)
chk('L1-PA1', diff(5*x**3 - 4*x**2 + x - 9, x), 15*x**2 - 8*x + 1)
chk('L1-PA2', diff(x*(x**2 + 6), x), 3*x**2 + 6)
chk('L1-PA3', diff((x - 2)**2, x), 2*x - 4)
chk('L1-WE3', diff(x**3 - 6*x**2 + 4, x).subs(x, 5), 15)
chk('L1-WE4', (x**2 - 7*x + 1).subs(x, roots(2*x - 7 - 3)[0]), -9)
chk('L1-WE5', solve(diff(a*x**2 + 3*x - 1, x).subs(x, 2) - 11, a)[0], 2)
chk('L1-PB1', diff(2*x**3 + x**2 - 4*x, x).subs(x, 2), 24)
chk('L1-PB2', (x**2 + 4*x - 3).subs(x, 3), 18); chk('L1-PB2x', roots(2*x + 4 - 10)[0], 3)
chk('L1-PB3', solve(diff(k*x**3 - 2*x, x).subs(x, 2) - 22, k)[0], 2)
chk('L1-WE6', tangent(x**3 - 2*x + 1, 2), 10*x - 15)
s = solve([a + b - 5, 2*a + b - 8], [a, b]); chk('L1-WE7a', s[a], 3); chk('L1-WE7b', s[b], 2)
chk('L1-PC1', tangent(2*x**2 - 3*x + 4, 2), 5*x - 4)
chk('L1-PC2', tangent(x**2 - 4*x + 7, roots(2*x - 4 - 2)[0]), 2*x - 2)
chk('L1-PC3', roots(x**3 - tangent(x**3, 1))[0], -2)
# practice sheet originals
chk('L1-PS1', diff(6*x**4 - 3*x**3 + 2*x - 11, x), 24*x**3 - 9*x**2 + 2)
chk('L1-PS2', diff(x**3 - 4*x**2 + 5, x).subs(x, -1), 11)
chk('L1-PS3', (3*x**2 - 12*x + 2).subs(x, roots(6*x - 12 - 6)[0]), -7)
chk('L1-PS4', tangent(x**3 - 3*x**2 + 2, 3), 9*x - 25)
# homework
chk('L1-H1a', diff(4*x**5 - 2*x**3 + 9, x), 20*x**4 - 6*x**2)
chk('L1-H1b', diff(7 - 3*x + 5*x**2, x), -3 + 10*x)
chk('L1-H1c', diff(R(1, 2)*x**4 - R(1, 3)*x**3 + x, x), 2*x**3 - x**2 + 1)
chk('L1-H1d', diff((x + 4)*(x - 1), x), 2*x + 3)
chk('L1-H2', diff(x**2*(3*x - 5), x), 9*x**2 - 10*x)
chk('L1-H3', diff((2*x - 3)**2, x), 8*x - 12)
chk('L1-H4', diff(x**3 + 2*x**2 - 5*x + 1, x).subs(x, 2), 15)
chk('L1-H5', diff(4 - 3*x**2, x).subs(x, -2), 12)
chk('L1-H6', diff(x**4 - 8*x, x).subs(x, 1), -4)
chk('L1-H7', (x**2 - 6*x + 10).subs(x, roots(2*x - 6 - 4)[0]), 5)
chk('L1-H8', sum(roots(diff(x**3 - 3*x**2 - 9*x + 2, x))), 2)
r = roots(diff(x**3 - 12*x + 1, x) - 15); chk('L1-H9', r[0], -3)
chk('L1-H9y', (x**3 - 12*x + 1).subs(x, -3), 10); chk('L1-H9y2', (x**3 - 12*x + 1).subs(x, 3), -8)
chk('L1-H10', solve(diff(a*x**3 + 2*x**2 - 1, x).subs(x, 2) - 32, a)[0], 2)
chk('L1-H11', tangent(3*x**2 - x + 2, 1), 5*x - 1)
chk('L1-H12', tangent(x**3 - 4*x, -1), -x + 2)
s = solve([4*p + 2*q - 2, 4*p + q - 5], [p, q]); chk('L1-H13p', s[p], 2); chk('L1-H13q', s[q], -3)
chk('L1-H14', tangent(x**2 + 2*x - 3, roots(2*x + 2 - 6)[0]), 6*x - 7)
sa = solve((2*a*(0 - a) + a**2) + 9, a); chk('L1-H15', sorted(sa)[1], 3)
chk('L1-H15t', tangent(x**2, 3), 6*x - 9); chk('L1-H15t2', tangent(x**2, -3), -6*x - 9)

# ---------------- Lesson 2 ----------------
chk('L2-DN1', diff(expand((x - 3)*(x + 5)), x), 2*x + 2)
chk('L2-DN2', diff(x**3 - 5*x, x).subs(x, 2), 7)
chk('L2-DN3', roots(3*x**2 - 12)[1], 2)
chk('L2-DN4', roots(2*x**2 - x - 6)[0], R(-3, 2))
f = x**3 - 6*x**2 + 9*x + 1
chk('L2-WE1', roots(diff(f, x))[1], 3); chk('L2-WE1a', f.subs(x, 1), 5); chk('L2-WE1b', f.subs(x, 3), 1)
chk('L2-WE1c', diff(f, x, 2).subs(x, 1), -6)
chk('L2-PA1', (x**2 - 8*x + 3).subs(x, 4), -13)
f = 2*x**3 - 3*x**2 - 12*x
chk('L2-PA2', roots(diff(f, x))[0], -1); chk('L2-PA2a', f.subs(x, -1), 7); chk('L2-PA2b', f.subs(x, 2), -20)
chk('L2-PA3', solve(diff(x**3 + k*x, x).subs(x, 2), k)[0], -12)
chk('L2-WE3', roots(diff(5 + 4*x - x**2, x))[0], 2)
chk('L2-PB1', roots(diff(x**2 - 10*x + 1, x))[0], 5)
chk('L2-PB2', roots(diff(x**3 - 12*x + 4, x))[1], 2)
h = 2 + R(196, 10)*t - R(49, 10)*t**2
chk('L2-WE4', h.subs(t, roots(diff(h, t), t)[0]), R(216, 10))
A = x*(60 - 2*x); chk('L2-WE5', A.subs(x, roots(diff(A, x))[0]), 450)
P = 120*x - 2*x**2 - 500; chk('L2-PC1', P.subs(x, roots(diff(P, x))[0]), 1300)
A = x*(18 - x); chk('L2-PC2', A.subs(x, roots(diff(A, x))[0]), 81)
V = x*(12 - 2*x)**2; chk('L2-PC3x', roots(diff(V, x))[0], 2); chk('L2-PC3', V.subs(x, 2), 128)
chk('L2-PC3d2', diff(V, x, 2).subs(x, 2), -48)
f = x**3 - 27*x + 10; chk('L2-PS1a', f.subs(x, 3), -44); chk('L2-PS1b', f.subs(x, -3), 64)
h = R(3, 2) + R(147, 10)*t - R(49, 10)*t**2
chk('L2-PS2t', roots(diff(h, t), t)[0], R(3, 2)); chk('L2-PS2', h.subs(t, R(3, 2)), R(12525, 1000))
chk('L2-H1', (x**2 + 6*x - 7).subs(x, -3), -16)
chk('L2-H2', (3 + 10*x - x**2).subs(x, 5), 28)
chk('L2-H3a', (x**3 - 3*x + 2).subs(x, 1), 0); chk('L2-H3b', (x**3 - 3*x + 2).subs(x, -1), 4)
f = 2*x**3 + 3*x**2 - 36*x + 1
chk('L2-H4r', roots(diff(f, x))[0], -3); chk('L2-H4a', f.subs(x, -3), 82); chk('L2-H4b', f.subs(x, 2), -43)
f = x**4 - 8*x**2; chk('L2-H5', f.subs(x, 2), -16); chk('L2-H5r', len(roots(diff(f, x))), 3)
chk('L2-H6', roots(diff(x**2 - 4*x + 9, x))[0], 2)
chk('L2-H7', roots(diff(x**3 - 3*x**2 + 5, x))[1], 2)
chk('L2-H8', roots(diff(R(1, 3)*x**3 - x**2 - 8*x, x))[0], -2)
chk('L2-H9b', solve(diff(x**2 + b*x + 5, x).subs(x, 3), b)[0], -6); chk('L2-H9y', (x**2 - 6*x + 5).subs(x, 3), -4)
h = 40*t - 5*t**2; chk('L2-H10', h.subs(t, 4), 80)
C = 2*x**2 - 80*x + 1000; chk('L2-H11', C.subs(x, roots(diff(C, x))[0]), 200)
Pp = x*(20 - x); chk('L2-H12', Pp.subs(x, roots(diff(Pp, x))[0]), 100)
A = x*(40 - 2*x); chk('L2-H13', A.subs(x, roots(diff(A, x))[0]), 200)
A = 2*x*(12 - x**2); chk('L2-H14x', roots(diff(A, x))[1], 2); chk('L2-H14', A.subs(x, 2), 32)

# ---------------- Lesson 3 (sketch answers: the derivatives drawn in red) ----------------
chk('L3-DN1', (x**2 - 6*x + 1).subs(x, 3), -8)
chk('L3-DN2', roots(diff(x**3 - 3*x**2, x))[1], 2)
g = x**3 - 3*x
chk('L3-DN3A', diff(g, x).subs(x, R(-3, 2)), R(15, 4)); chk('L3-DN3C', diff(g, x).subs(x, R(1, 2)), R(-9, 4))
chk('L3-DN3D', diff(g, x).subs(x, R(17, 10)), R(567, 100))
chk('L3-PB1', diff(x**3 + R(3, 2)*x**2 - 6*x, x), 3*(x + 2)*(x - 1))
chk('L3-PB2', diff(-x**3 + R(9, 2)*x**2, x), -3*x**2 + 9*x)
chk('L3-PB3', diff(x**4 - 8*x**2, x), 4*x**3 - 16*x)
chk('L3-PS1', diff(x**3/3 - x**2 - 3*x, x), (x + 1)*(x - 3))

# homework sketches: answer curve must be the derivative (or an anti-derivative) of the given one
pairs = [(3*x - 2, 3), (4 - x/2, -R(1, 2)), (x**2 - 4*x, 2*x - 4), (3 - 2*x - x**2, -2*x - 2),
         (x**3 - 12*x, 3*x**2 - 12), (-x**3 + 3*x**2 + 1, -3*x**2 + 6*x), (x**4/4 - 2*x**2, x**3 - 4*x),
         (2*x - 1, 2), (x**2/2 - 3*x + 2, x - 3), (-x**2 - 4*x - 1, -2*x - 4), (x**3/3 - x, x**2 - 1),
         (-x**3/3 - x**2 + 3*x + 3, -x**2 - 2*x + 3), ((x - 2)**3/3 + 1, (x - 2)**2)]
for i, (f_, fp_) in enumerate(pairs, 1):
    chk('L3-HW%d' % i, diff(f_, x), fp_)
chk('L3-SP6', diff(x**3/3 - 2*x**2 + 4, x), x**2 - 4*x)
chk('L3-PS2', diff(-x**2/2 + 2*x, x), -x + 2)
chk('L3-X22-2a', diff(-R(3, 8)*x**4 - R(1, 4)*x**3 + R(33, 4)*x**2 + R(63, 4)*x - 10, x),
    expand(-R(3, 2)*(x + 3)*(x + 1)*(x - R(7, 2))))
chk('L3-X21-3c', diff(R(1, 2)*(-x**3/6 + 3*x**2 - 10*x) - 4, x), expand(-R(1, 4)*(x - 2)*(x - 10)))

# ---------------- Lesson 4 ----------------
chk('L4-DN3', diff(5*t**2 - 3*t + 8, t), 10*t - 3)
chk('L4-DN4', solve(2*9 - 4 + c - 12, c)[0], -2)
chk('L4-WE1', integrate(6*x**2 - 4*x + 5, x), 2*x**3 - 2*x**2 + 5*x)
chk('L4-WE2', F(4*x - 3, (2, 7)), 2*x**2 - 3*x + 5)
chk('L4-PA1', integrate(9*x**2 + 2*x - 7, x), 3*x**3 + x**2 - 7*x)
chk('L4-PA2', integrate(x**3 - 6*x, x), x**4/4 - 3*x**2)
chk('L4-PA3', F(6*x - 5, (1, 4)), 3*x**2 - 5*x + 6)
V = 2000 + 30*t - R(1, 2)*t**2
chk('L4-WE3a', diff(V, t).subs(t, 10), 20); chk('L4-WE3b', diff(V, t).subs(t, 40), -10)
chk('L4-WE4', roots(diff(500 + 40*t - t**2, t) - 10, t)[0], 15)
chk('L4-PB1', diff(80 - 6*t + R(1, 10)*t**2, t).subs(t, 10), -4)
chk('L4-PB2', roots(diff(15*t - t**2 + 20, t), t)[0], R(15, 2))
A = t**2 - 4*t + 10; tt = [r for r in roots(A - 31, t) if r > 0][0]
chk('L4-PB3t', tt, 7); chk('L4-PB3', diff(A, t).subs(t, tt), 10)
s_ = t**3 - 6*t**2 + 9*t
chk('L4-WE5v', diff(s_, t).subs(t, 2), -3); chk('L4-WE5a', diff(s_, t, 2).subs(t, 3), 6)
v = -R(98, 10)*t + 14; s_ = integrate(v, t) + R(12, 10)
chk('L4-WE6', s_.subs(t, roots(v, t)[0]), R(112, 10))
chk('L4-PC1', roots(diff(2*t**3 - 9*t**2 + 12*t, t), t)[1], 2)
v = integrate(R(6, 10)*t, t); s_ = integrate(v, t)
chk('L4-PC2v', v.subs(t, 5), R(75, 10)); chk('L4-PC2s', s_.subs(t, 5), R(125, 10))
v = R(245, 10) - R(98, 10)*t; s_ = integrate(v, t)
chk('L4-PC3t', roots(v, t)[0], R(5, 2)); chk('L4-PC3', s_.subs(t, R(5, 2)), R(30625, 1000))
chk('L4-PC3land', roots(s_, t)[1], 5)
chk('L4-PS1', F(12*x**2 - 2*x + 3, (1, 10)), 4*x**3 - x**2 + 3*x + 4)
s_ = integrate(8 - 2*t, t) + 5
chk('L4-PS2', s_.subs(t, 3), 20); chk('L4-PS2r', roots(8 - 2*t, t)[0], 4)
chk('L4-H1a', integrate(8*x**3, x), 2*x**4)
chk('L4-H1b', integrate(3*x**2 - 10*x + 1, x), x**3 - 5*x**2 + x)
chk('L4-H1c', integrate(5 - 2*x, x), 5*x - x**2)
chk('L4-H1d', integrate(x**2 + 4*x, x), x**3/3 + 2*x**2)
chk('L4-H2', F(2*x + 3, (0, -1)), x**2 + 3*x - 1)
chk('L4-H3', F(3*x**2 - 4, (2, 5)), x**3 - 4*x + 5)
chk('L4-H4', F(6*x**2 + 2*x, (-1, 3)), 2*x**3 + x**2 + 4)
chk('L4-H5', F(4*x - 1, (1, 2)).subs(x, 3), 16)
chk('L4-H6', diff(50*x - R(2, 10)*x**2, x).subs(x, 100), 10)
chk('L4-H7', diff(20 + 15*t - R(1, 4)*t**2, t).subs(t, 10), 10)
chk('L4-H8', roots(diff(R(5, 10) + R(8, 10)*t - R(2, 100)*t**2, t) - R(4, 10), t)[0], 10)
s_ = t**3 - 9*t**2 + 24*t
chk('L4-H9a', diff(s_, t).subs(t, 1), 9); chk('L4-H9b', roots(diff(s_, t), t)[1], 4)
chk('L4-H9c', diff(s_, t, 2).subs(t, 4), 6)
chk('L4-H10', integrate(3*t**2 + 2, (t, 0, 4)), 72)
v = integrate(6 - 2*t, t); s_ = integrate(v, t)
chk('L4-H11v', v.subs(t, 3), 9); chk('L4-H11s', s_.subs(t, 3), 18)
v = R(126, 10) - R(98, 10)*t; s_ = 2 + integrate(v, t)
chk('L4-H12', s_.subs(t, roots(v, t)[0]), R(101, 10))
v = 20 - 4*t; chk('L4-H13', integrate(v, (t, 0, roots(v, t)[0])), 50)
s_ = integrate(3*t**2 - 12*t + 9, t)
chk('L4-H14', abs(s_.subs(t, 1) - 0) + abs(s_.subs(t, 3) - s_.subs(t, 1)), 8)

# ---------------- Lesson 5 ----------------
chk('L5-DN1', diff(expand((3*x - 1)*(x + 2)), x), 6*x + 5)
chk('L5-DN2', (2*x**2 - 12*x + 7).subs(x, 3), -11)
chk('L5-DN3', F(8*x - 3, (1, 6)), 4*x**2 - 3*x + 5)
chk('L5-PA1', diff(2*x**3 - 5*x + 4, x).subs(x, -2), 19)
chk('L5-PA2', F(12*x**2 - 6, (1, 3)), 4*x**3 - 6*x + 5)
chk('L5-PA3', diff(6*t - t**2, t).subs(t, 2), 2)
s = solve([a + b + 4, 3*a + b], [a, b]); chk('L5-WEa', s[a], 2); chk('L5-WEb', s[b], -6)
s = solve([4 + p, 4 + 2*p + q - 5], [p, q]); chk('L5-PB1p', s[p], -4); chk('L5-PB1q', s[q], 9)
V = 600*t - 25*t**2; tt = roots(V - 3200, t)
chk('L5-PB2t', tt[0], 8); chk('L5-PB2a', diff(V, t).subs(t, 8), 200); chk('L5-PB2b', diff(V, t).subs(t, 16), -200)
f = 3 + 12*x - 2*x**3; chk('L5-PB3', f.subs(x, sqrt(2)), 3 + 8*sqrt(2))
Vb = x*(108 - x**2)/4; chk('L5-WE2x', roots(diff(Vb, x))[1], 6); chk('L5-WE2', Vb.subs(x, 6), 108)
chk('L5-WE2h', ((108 - x**2)/(4*x)).subs(x, 6), 3)
A = (x/4)**2 + ((48 - x)/4)**2; chk('L5-PC1x', roots(diff(A, x))[0], 24); chk('L5-PC1', A.subs(x, 24), 72)
y = x**3 - 3*a**2*x
chk('L5-PC2', simplify(y.subs(x, -a) - y.subs(x, a)), 4*a**3)
chk('L5-PS1a', diff(x**4 - 3*x**2 + 2*x, x).subs(x, -1), 4)
chk('L5-PS1b', tangent(2*x**2 - 5*x + 1, 3), 7*x - 17)
chk('L5-PS1c', F(3*x**2 - 8*x + 2, (2, 1)), x**3 - 4*x**2 + 2*x + 5)
chk('L5-PS1d', roots(diff(x**3 - 6*x**2 + 5, x))[1], 4)
chk('L5-PS2a', roots(diff(4*t**3 - 15*t**2 + 12*t, t), t)[0], R(1, 2))
chk('L5-PS2b', integrate(6*t - t**2, (t, 0, 6)), 36)
chk('L5-H1', diff(expand((x + 2)*(x**2 - 3)), x), 3*x**2 + 4*x - 3)
chk('L5-H2', (x**3 - 6*x**2 + 9).subs(x, 4), -23)
chk('L5-H3', F(6*x - 2, (-1, 8)), 3*x**2 - 2*x + 3)
s = solve([2 + b - 5, 1 + b + c - 3], [b, c]); chk('L5-H5b', s[b], 3); chk('L5-H5c', s[c], -1)
v = 5 + integrate(4 - 2*t, t); s_ = integrate(v, t)
chk('L5-H6v', v.subs(t, 2), 9); chk('L5-H6s', s_.subs(t, 2), R(46, 3))

# ---------------- Exam parts (tutor's working) ----------------
chk('X21-1a', diff(4*x**3 - 2*x**2 - 7*x + 4, x).subs(x, 3), 89)
chk('X21-1b', tangent(R(1, 2)*x**3 + R(1, 2)*x, 2), R(13, 2)*x - 8)
V = -11*t**2 + 528*t; tt = roots(V - 3520, t)
chk('X21-1ci', tt[0] + tt[1], 48); chk('X21-1ci-r', diff(V, t).subs(t, 8), 352)
chk('X21-1cii', V.subs(t, 24), 6336)
V = R(16, 10)*t**3 - 130*t**2 + 2900*t; tm = roots(diff(V, t), t)
chk('X21-1ciii', float(V.subs(t, tm[1])) > 10000, True)
chk('X21-2b', solve(diff(5 + 3*x + c*x**2 - 2*x**3, x).subs(x, 2) + 5, c)[0], 4)
v = R(28, 10) - R(98, 10)*t; chk('X21-2ci', v.subs(t, 1), -7)
tl = roots(v + R(2268, 100), t)[0]; chk('X21-2cii-t', tl, R(26, 10))
H = -integrate(v, (t, 0, tl)); smax = H + integrate(v, (t, 0, roots(v, t)[0]))
chk('X21-2cii', smax, R(26244, 1000))
chk('X21-3a', F(6*x**2 + 5*x - 1, (1, R(5, 2))).subs(x, 2), 23)
chk('X21-3b', integrate(R(3, 10)*t**2 + 1, (t, 0, 3)), R(57, 10))
A = 18*x - x**3; chk('X21-3di', 9 - roots(diff(A, x))[1]**2, 3)
A = 2*d*x - k*x**3; xs = sqrt(2*d/(3*k))
chk('X21-3dii', simplify((2*xs*(d - k*xs**2)) - (xs*k*xs**2)), 0)
chk('X22-1a', diff(2*x**4 + 4*x**3 - 20*x**2 - 5, x).subs(x, 3), 204)
chk('X22-1b', F(4 - 6*x + 2*x**2, (3, 4)), R(2, 3)*x**3 - 3*x**2 + 4*x + 1)
chk('X22-1c', roots(diff(R(2, 3)*x**3 + R(3, 2)*x**2 - 20*x - 3, x))[0], -4)
s = solve([2*p - 4*q + 10, p - 4*q + 6], [p, q]); chk('X22-1dp', s[p], -4); chk('X22-1dq', s[q], R(1, 2))
r = symbols('r', positive=True); A = 80*r - 3*pi*r**2
chk('X22-1e', A.subs(r, solve(diff(A, r), r)[0]), 1600/(3*pi))
h = R(225, 10)*t - R(49, 10)*t**2 + 1
chk('X22-2b', h.subs(t, roots(diff(h, t), t)[0]), 1 + R(50625, 1960))
P = 100*t**2 - 2*t**4 + 750; chk('X22-2ci', diff(P, t).subs(t, 6), -528)
P = k*t**2 - 2*t**4 + 750; chk('X22-2ciii', solve(diff(P, t, 2).subs(t, 4), k)[0], 192)
chk('X22-3a', tangent(2*x*(x - 3), 1), -2*x - 2)
S = sqrt(3)*(30 - 2*b)**2 + 2*sqrt(3)*b**2
chk('X22-3c', solve(diff(S, b), b)[0], 10); chk('X22-3cS', S.subs(b, 10), 300*sqrt(3))
print('all %d answers verified' % ok)
