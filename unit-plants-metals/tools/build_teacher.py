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
\definecolor{sayblue}{RGB}{0,70,190}
\newcommand\sigline[1]{\hbox to\paperwidth{\hfil\fontsize{6}{7}\selectfont\color{sig}Dr. Ryan Lei \textperiodcentered{} Auckland \quad 第 #1 页\hspace{5mm}}}
% red answer box: width #1, height #2; too much text reports Overfull \vbox
\newcommand\anscol[3]{\vbox to#2{\hsize=#1
  \fontsize{9.8}{11.6}\selectfont\lineskiplimit=0pt\lineskip=1pt\color{ansred}\raggedright\bfseries
  \leavevmode #3\par\vfil}}
% one hard word: the word in bold, its pronunciation unbroken on the next line
\newcommand\sayline[2]{\textbf{#1}\par\hspace*{3mm}\mbox{#2}\par\vspace{1.2mm}}
% Layout A (no hard words): slide 0.63 wide, centred; answers full width below.
\newcommand\teacherpage[3]{%
  \newpage\nointerlineskip
  \vbox to\paperheight{\offinterlineskip
    \vskip2.5mm
    \hbox to\paperwidth{\hfil\fbox{\includegraphics[page=#1,width=0.63\paperwidth]{slides_zh_screen.pdf}}\hfil}
    \vskip1.8mm
    \hbox to\paperwidth{\hspace{5mm}\anscol{\dimexpr\paperwidth-10mm\relax}{26mm}{#2}\hfil}
    \vfil\sigline{#1}\vskip1.8mm}}
% Layout B (hard words): left, slide 0.60 wide with the red answers below;
% right, the blue Say it column over the full height. An unbroken
% pronunciation wider than the column reports Overfull \hbox.
\newlength\sayw \setlength\sayw{46mm}
\newcommand\teacherpagesay[3]{%
  \newpage\nointerlineskip
  \vbox to\paperheight{\offinterlineskip
    \vskip2.5mm
    \hbox to\paperwidth{\hspace{4mm}%
      \vtop{\hsize=0.60\paperwidth\vskip0pt  % both columns top-aligned at height 0
        \hbox{\fbox{\includegraphics[page=#1,width=0.60\paperwidth]{slides_zh_screen.pdf}}}
        \vskip1.8mm
        \anscol{0.60\paperwidth}{29mm}{#2}}%
      \hfil{\color{sayblue}\vrule width0.4pt height0pt depth86mm}\hspace{2.5mm}%
      \vtop{\hsize=\sayw\vskip0pt
        \fontsize{9.4}{11}\selectfont\lineskiplimit=0pt\lineskip=1pt\color{sayblue}\raggedright\parindent=0pt
        \vbox to 84mm{{\bfseries Say it 读音}\par\vspace{1.5mm}#3\par\vfil}}%
      \hspace{4mm}}
    \vfil\sigline{#1}\vskip1.8mm}}
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
        m = re.search(r"\\answers\{", body)
        if not m:
            raise SystemExit(f"frame {k}: no \\answers block")
        ans, _ = brace_body(body, m.end() - 1)
        ans = re.sub(r"^%\n", "", ans)
        items = "".join("\\sayline{%s}{%s}" % tuple(l.split(" = ")) for l in say[k - 1])
        if items:
            out.append(f"\\teacherpagesay{{{k}}}{{{ans}}}{{{items}}}\n")
        else:
            out.append(f"\\teacherpage{{{k}}}{{{ans}}}{{}}\n")
        n += 1
    out.append("\\end{document}\n")
    open(os.path.join(HERE, "teacher_pages.tex"), "w", encoding="utf-8").write("\n".join(out))
    print(f"teacher_pages.tex: {n} pages")


if __name__ == "__main__":
    main()
