#!/usr/bin/env python3
"""Generates lesson3/hw.tex (sketch homework): each question = given graph | blank grid.
Grid heights are computed to about 36 mm; answer curves are the exact derivatives or
anti-derivatives (checked in tools/verify_answers.py, L3-HW entries)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))

# (text, grade, given(xmin,xmax,ymin,ymax,name,curve), answer(ymin,ymax,name,curve), ystep_g, ystep_a, gy_g, gy_a)
Q = [
    ('The graph of $f(x)=3x-2$ is shown. Sketch $f\'(x)$.', 'A',
     (-3, 3, -12, 8, "$f(x)$", '3*\\x-2'), (-4, 4, "$f'(x)$", '3'), 4, 2, 2, 1),
    ('The graph of $f(x)=4-\\dfrac{1}{2}x$ is shown. Sketch $f\'(x)$.', 'A',
     (-4, 4, -1, 7, "$f(x)$", '4-0.5*\\x'), (-2, 2, "$f'(x)$", '-0.5'), 2, 1, 1, 1),
    ('The graph of $f(x)=x^{2}-4x$ is shown. Sketch $f\'(x)$.', 'A',
     (-1, 5, -5, 6, "$f(x)$", '\\x*\\x-4*\\x'), (-6, 6, "$f'(x)$", '2*\\x-4'), 2, 2, 1, 1),
    ('The graph of $f(x)=3-2x-x^{2}$ is shown. Sketch $f\'(x)$.', 'A',
     (-4, 2, -6, 5, "$f(x)$", '3-2*\\x-\\x*\\x'), (-6, 6, "$f'(x)$", '-2*\\x-2'), 2, 2, 1, 1),
    ('The graph of $f(x)=x^{3}-12x$ is shown. Sketch $f\'(x)$.', 'A',
     (-4, 4, -18, 18, "$f(x)$", '\\x*\\x*\\x-12*\\x'), (-12, 30, "$f'(x)$", '3*\\x*\\x-12'), 6, 6, 3, 3),
    ('The graph of $f(x)=-x^{3}+3x^{2}+1$ is shown. Sketch $f\'(x)$.', 'A',
     (-2, 4, -8, 12, "$f(x)$", '-\\x*\\x*\\x+3*\\x*\\x+1'), (-12, 6, "$f'(x)$", '-3*\\x*\\x+6*\\x'), 4, 3, 2, 3),
    ('The graph of $f(x)=\\dfrac{1}{4}x^{4}-2x^{2}$ is shown. Sketch $f\'(x)$.', 'M',
     (-3, 3, -5, 4, "$f(x)$", '0.25*\\x*\\x*\\x*\\x-2*\\x*\\x'), (-8, 8, "$f'(x)$", '\\x*\\x*\\x-4*\\x'), 2, 2, 1, 2),
    ('The graph of $y=f\'(x)$ is shown. Sketch a possible graph of $f(x)$.', 'A',
     (-3, 3, -1, 4, "$f'(x)$", '2'), (-8, 6, "$f(x)$", '2*\\x-1'), 1, 2, 1, 1),
    ('The graph of $y=f\'(x)$ is shown. Sketch a possible graph of $f(x)$.', 'A',
     (-1, 6, -4, 3, "$f'(x)$", '\\x-3'), (-4, 6, "$f(x)$", '0.5*\\x*\\x-3*\\x+2'), 1, 2, 1, 1),
    ('The graph of $y=f\'(x)$ is shown. Sketch a possible graph of $f(x)$.', 'A',
     (-5, 1, -6, 6, "$f'(x)$", '-2*\\x-4'), (-7, 4, "$f(x)$", '-\\x*\\x-4*\\x-1'), 2, 2, 1, 1),
    ('The graph of $y=f\'(x)$ is shown. Sketch a possible graph of $f(x)$.', 'M',
     (-3, 3, -2, 8, "$f'(x)$", '\\x*\\x-1'), (-6, 6, "$f(x)$", '\\x*\\x*\\x/3-\\x'), 2, 2, 1, 1),
    ('The graph of $y=f\'(x)$ is shown. Sketch a possible graph of $f(x)$ and label its maximum and minimum.', 'M',
     (-5, 3, -12, 5, "$f'(x)$", '-\\x*\\x-2*\\x+3'), (-7, 6, "$f(x)$", '-\\x*\\x*\\x/3-\\x*\\x+3*\\x+3'), 4, 2, 2, 1),
]


def sk(xmin, xmax, ymin, ymax, name, curve, ystep, gy, ans=None, unit=7.5):
    h = 36.0 / (ymax - ymin)
    keys = 'xmin=%d,xmax=%d,ymin=%d,ymax=%d,unit=%smm,yunit=%.2fmm,ystep=%d,gy=%d,name={%s}' % (
        xmin, xmax, ymin, ymax, unit, h, ystep, gy, name)
    if curve:
        keys += ',curve={%s},dmin=%d,dmax=%d' % (curve, xmin, xmax)
    if ans:
        keys += ',ans={%s},amin=%d,amax=%d' % (ans, xmin, xmax)
    return '\\sketch[%s]' % keys


out = [r'''\documentclass[11pt]{article}
\usepackage{docstyle}
\begin{document}
\sheethead{Lesson 3 \textperiodcentered\ Homework}{NCEA Level 2 \textperiodcentered\ AS 91262 \textperiodcentered\ Sketching gradient functions}{about 60 minutes}{}
Sketch on the empty axes. Line up every key $x$-value with a ruler, and label turning points.
[A] Achieved, [M] Merit, [E] Excellence.
''']
for text, g, giv, an, ysg, ysa, gyg, gya in Q:
    xmin, xmax, ymin, ymax, name, curve = giv
    aymin, aymax, aname, acurve = an
    out.append('\\par\\needspace{58mm}\\Q %s\\mk{%s}\n\\begin{center}\n%s\\hspace{10mm}%s\n\\end{center}\n' % (
        text, g, sk(xmin, xmax, ymin, ymax, name, curve, ysg, gyg),
        sk(xmin, xmax, aymin, aymax, aname, None, ysa, gya, ans=acurve)))
out.append(r'''\par\needspace{50mm}\Q Tama says: ``Where the graph of $f'(x)$ has its highest point, the graph of $f(x)$ has a maximum.''
Is Tama right? Explain, using $f(x)=x^{3}-3x$ (so $f'(x)=3x^{2}-3$) or an example of your own.\mk{M}
\ALine{No. A maximum of $f$ is where $f'(x)=0$ and $f'$ changes from $+$ to $-$.}
\ALine{A \tturn of $f'$ is where $f$ is steepest (a \tinflect), not a \tturn of $f$.}
\ALine{E.g.\ $f'(x)=3x^{2}-3$ has its lowest point at $x=0$, where $f$ is steepest downhill;}
\ALine{the maximum of $f$ is at $x=-1$, where $f'(-1)=0$.}

\par\needspace{70mm}\QX The graph of $f'(x)=(x-2)^{2}$ touches the $x$-axis at $x=2$ but does not cross it.
Sketch a possible graph of $f(x)$, and describe what happens to $f$ at $x=2$.\mk{E}
\begin{center}
''' + sk(-1, 5, -1, 9, "$f'(x)$", '(\\x-2)*(\\x-2)', 2, 1) + '\\hspace{10mm}' +
    sk(-1, 5, -5, 6, "$f(x)$", None, 2, 1, ans='(\\x-2)*(\\x-2)*(\\x-2)/3+1') + r'''
\end{center}
\ALine{$f'(x)\ge0$ everywhere, so $f$ is always increasing.}
\ALine{At $x=2$, $f'=0$ but does not change sign: $f$ is flat there (a stationary \tinflect),}
\ALineT{not a maximum or a minimum. One possible $f(x)=\dfrac{1}{3}(x-2)^{3}+1$.}

\vfill
{\small Optional extra: StudyTime Level 2 Calculus Guide, ``Sketching Gradient Functions'' from page 19.\par}
\end{document}
''')
open(os.path.join(HERE, '..', 'lesson3', 'hw.tex'), 'w').write(''.join(out))
print('lesson3/hw.tex written: %d sketch questions + 2' % len(Q))
