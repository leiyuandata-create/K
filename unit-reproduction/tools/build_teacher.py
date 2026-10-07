#!/usr/bin/env python3
"""Write teacher_pages.tex: one page per slide for the tutor.

The page shows page k of slides_zh_screen.pdf -- the slide in Chinese with
the answers already written on it in red -- and, under it, that frame's
\\hint{} from slides_zh_frames.tex (how to run the slide, what she gets
wrong). A slide whose \\note{} in slides.tex has Say it: lines gets a blue
"Say it" column on the right. build_teacher.sh joins the pages with
slides_screen.pdf into slides_teacher.pdf: English slide on the left (the
half that is projected), tutor's page on the right.

The hint sits in a \\vbox of fixed height and each pronunciation in an
\\mbox, so text that does not fit reports Overfull in the log (spec 10.4).
"""
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
\usepackage{shared}
\definecolor{sayblue}{RGB}{0,70,190}
\definecolor{hintink}{gray}{0.18}
\pagestyle{empty}
\setlength\parindent{0pt}
\setlength\fboxsep{0pt}
\setlength\fboxrule{0.4pt}
\newcommand\sigline[1]{\hbox to\paperwidth{\hfil\fontsize{6}{7}\selectfont\color{sig}Dr. Ryan Lei \textperiodcentered{} Auckland \quad 第 #1 页\hspace{4mm}}}
% hint box: width #1, height #2; too much text reports Overfull \vbox
\newcommand\hintbox[3]{\vbox to#2{\hsize=#1
  \fontsize{8.4}{10.6}\selectfont\lineskiplimit=0pt\lineskip=1pt\color{hintink}\raggedright
  \leavevmode #3\par\vfil}}
% one hard word: the word in bold, its pronunciation unbroken on the next line
\newcommand\sayline[2]{\textbf{#1}\par\hspace*{2mm}\mbox{#2}\par\vspace{1mm}}
% Layout A (no hard words): slide 0.82 of the page width, centred; hint below.
\newcommand\teacherpage[3]{%
  \newpage\nointerlineskip
  \vbox to\paperheight{\offinterlineskip
    \vskip1.5mm
    \hbox to\paperwidth{\hfil\fbox{\includegraphics[page=#1,width=0.82\paperwidth]{slides_zh_screen.pdf}}\hfil}
    \vskip1mm
    \hbox to\paperwidth{\hfil\hintbox{0.82\paperwidth}{9.6mm}{#2}\hfil}
    \vfil\sigline{#1}\vskip1.3mm}}
% Layout B (hard words): left, slide 0.74 wide with the hint below it;
% right, the blue Say it column over the full height. The two columns are
% \vtops top-aligned at height 0; the divider rule hangs below the
% baseline, or it would add its height to the page.
\newlength\sayw \setlength\sayw{34mm}
\newcommand\teacherpagesay[3]{%
  \newpage\nointerlineskip
  \vbox to\paperheight{\offinterlineskip
    \vskip1.5mm
    \hbox to\paperwidth{\hspace{2.5mm}%
      \vtop{\hsize=0.74\paperwidth\vskip0pt
        \hbox{\fbox{\includegraphics[page=#1,width=0.74\paperwidth]{slides_zh_screen.pdf}}}
        \vskip1mm
        \hintbox{0.74\paperwidth}{17.5mm}{#2}}%
      \hfil{\color{sayblue}\vrule width0.4pt height0pt depth88mm}\hspace{2mm}%
      \vtop{\hsize=\sayw\vskip0pt
        \fontsize{8.8}{10.3}\selectfont\lineskiplimit=0pt\lineskip=1pt\color{sayblue}\raggedright\parindent=0pt
        \vbox to 88mm{{\bfseries Say it 读音}\par\vspace{1.2mm}#3\par\vfil}}%
      \hspace{2.5mm}}
    \vfil\sigline{#1}\vskip1.3mm}}
\begin{document}
"""


def say_it_lines():
    """Say it: lines of every frame's note in slides.tex (the one source)."""
    en = open(os.path.join(HERE, "slides.tex"), encoding="utf-8").read()
    frames = re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", en[en.index("\\begin{document}"):], re.S)
    out = []
    for fr in frames:
        m = re.search(r"\\note\{", fr)
        note, _ = brace_body(fr, m.end() - 1)
        lines = [l.strip() for l in re.split(r"\\par\b", note) if l.strip()]
        out.append(lines[lines.index("Say it:") + 1:] if "Say it:" in lines else [])
    return out


def main():
    say = say_it_lines()
    src = open(os.path.join(HERE, "slides_zh_frames.tex"), encoding="utf-8").read()
    blocks = re.split(r"^%%% FRAME (\d+) \{.*\}\s*$", src, flags=re.M)
    out = [HEAD]
    n = 0
    for i in range(1, len(blocks), 2):
        k, body = int(blocks[i]), blocks[i + 1]
        m = re.search(r"\\hint\{", body)
        if not m:
            raise SystemExit(f"frame {k}: no \\hint block")
        hint, _ = brace_body(body, m.end() - 1)
        items = "".join("\\sayline{%s}{%s}" % tuple(l.split(" = ")) for l in say[k - 1])
        if items:
            out.append(f"\\teacherpagesay{{{k}}}{{{hint}}}{{{items}}}\n")
        else:
            out.append(f"\\teacherpage{{{k}}}{{{hint}}}{{}}\n")
        n += 1
    out.append("\\end{document}\n")
    open(os.path.join(HERE, "teacher_pages.tex"), "w", encoding="utf-8").write("\n".join(out))
    print(f"teacher_pages.tex: {n} pages")


if __name__ == "__main__":
    main()
