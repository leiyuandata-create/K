#!/usr/bin/env python3
"""Write teacher_pages.tex: for every slide, the Chinese screen (page k of
slides_zh_screen.pdf, scaled) with that slide's \\answers{} from
slides_zh_frames.tex printed underneath in red. build_teacher.sh joins it
with slides_screen.pdf into slides_teacher.pdf: English slide on the left
(the half that is projected), Chinese slide + red answers on the right.

The answer area is a \\vbox of fixed height with \\vfil, so an answer that
does not fit reports Overfull \\vbox in the log (spec 10.4)."""
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def brace_body(tex, start):
    depth = 0
    for i in range(start, len(tex)):
        c = tex[i]
        if c == "{" and tex[i - 1] != "\\":
            depth += 1
        elif c == "}" and tex[i - 1] != "\\":
            depth -= 1
            if depth == 0:
                return tex[start + 1:i], i + 1
    raise ValueError("unbalanced braces")


HEAD = r"""% teacher_pages.tex -- written by tools/build_teacher.py; do not edit.
\documentclass{article}
\usepackage[paperwidth=170mm,paperheight=95.625mm,margin=0mm]{geometry}
\usepackage{fontspec}
\setmainfont[Path=fonts/, Extension=.otf, UprightFont=*-regular,
  BoldFont=*-bold, ItalicFont=*-italic, BoldItalicFont=*-bolditalic]{texgyreheros}
\usepackage{xeCJK}
\setCJKmainfont[Path=fonts/, AutoFakeBold=2]{wqy-microhei.ttc}
\usepackage{graphicx,xcolor}
\definecolor{ansred}{RGB}{200,16,46}
\definecolor{sig}{gray}{0.55}
\pagestyle{empty}
\setlength\parindent{0pt}
\setlength\fboxsep{0pt}
\setlength\fboxrule{0.4pt}
% slide image: 0.63 of the page width, centred; answers below it
\newlength\ansh \setlength\ansh{26mm}
% the whole page is one \vbox to \paperheight, so it never spills over;
% an answer that does not fit its box reports Overfull \vbox
\newcommand\teacherpage[2]{%
  \newpage\nointerlineskip
  \vbox to\paperheight{\offinterlineskip
    \vskip2.5mm
    \hbox to\paperwidth{\hfil\fbox{\includegraphics[page=#1,width=0.63\paperwidth]{slides_zh_screen.pdf}}\hfil}
    \vskip1.8mm
    \hbox to\paperwidth{\hspace{5mm}\vbox to\ansh{\hsize=\dimexpr\paperwidth-10mm\relax
      \fontsize{9.8}{11.6}\selectfont\lineskiplimit=0pt\lineskip=1pt\color{ansred}\raggedright\bfseries
      \leavevmode #2\par\vfil}\hfil}
    \vfil
    \hbox to\paperwidth{\hfil\fontsize{6}{7}\selectfont\color{sig}Dr. Ryan Lei \textperiodcentered{} Auckland \quad 第 #1 页\hspace{5mm}}
    \vskip1.8mm}}
\begin{document}
"""


def main():
    src = open(os.path.join(HERE, "slides_zh_frames.tex"), encoding="utf-8").read()
    blocks = re.split(r"^%%% FRAME (\d+) \{.*\}\s*$", src, flags=re.M)
    out = [HEAD]
    n = 0
    for i in range(1, len(blocks), 2):
        k, body = int(blocks[i]), blocks[i + 1]
        m = re.search(r"\\answers\{", body)
        if not m:
            raise SystemExit(f"frame {k}: no \\answers block")
        ans, _ = brace_body(body, m.end() - 1)
        ans = re.sub(r"^%\n", "", ans)
        out.append(f"\\teacherpage{{{k}}}{{{ans}}}\n")
        n += 1
    out.append("\\end{document}\n")
    open(os.path.join(HERE, "teacher_pages.tex"), "w", encoding="utf-8").write("\n".join(out))
    print(f"teacher_pages.tex: {n} pages")


if __name__ == "__main__":
    main()
