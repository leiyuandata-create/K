#!/usr/bin/env python3
"""Mutation tests for check.py (spec 10.3.6): every check must catch a planted fault.

A three-frame fixture deck and a one-page fixture sheet are written here,
so the tests never change when a lesson does. The clean fixture is run
through every check first and must pass all of them; then one fault per
item is planted in a scratch copy and must be caught. Faults about
silence (an overflow nothing else reports) also assert the fault is
really present.

    python3 test_checks.py          (about four minutes: run it in the background)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check  # noqa: E402
import export_pptx  # noqa: E402

DECK = r"""\documentclass[aspectratio=169,11pt,xcolor=table,t]{beamer}
\usepackage{slidestyle}
\ifdefined\notesmode\setbeameroption{show only notes}\else\setbeameroption{hide notes}\fi
\begin{document}
\begin{frame}{Do Now}
\relax
\qline{1} Simplify $x^{5}\times x^{3}$.%BODY1
\note{%
Q1 $x^{8}$\par
Short solution:\par
Q1 同底数相乘，index 相加\par
Watch for:\par
答 $x^{15}$\par
Diagnostic:\par
答错：多讲一遍%NOTE1
\par
Say it:\par
index = IN-deks}
\end{frame}
\begin{frame}{Spot the error (1)}
\relax
\textbf{Sam's answer has 2 errors.} Find each one.
\begin{samcard}\flawed{(3x\hsp{2})\hsp{3} = 3x\hsp{6}}\end{samcard}
\note{%
1. the 3 is cubed too (\Lref{coef})\par
2. the index is 6 (\Lref{negindex})%NOTE2
}
\end{frame}
\begin{frame}{Practice}
\relax
\qline{Q1} Factorise $x^{2}-9$.\smk{2}%BODY3
\note{%
Q1 $(x-3)(x+3)$\par
Short solution:\par
Q1 difference of two squares%NOTE3
}
\end{frame}
\end{document}
"""

SHEET = r"""\documentclass[11pt]{article}
\usepackage{docstyle}
\begin{document}
\sheethead{Fixture}{Sheet}{[A]}
\qpart{(a)}Simplify $\dfrac{x^{2}}{x}$.\lvl{A}
\al{$x$}%SHEET1
\qpart{(b)}\textbf{Sam's answer has 1 error.} Fix it.
\begin{samcard}\flawed{x\hsp{2} \hminus 9 = (x \hminus 9)(x + 9)}\end{samcard}
\begin{errorlist}
\erritem{1}{root the 9 too (\Lref{coef})}
\end{errorlist}
\al{}
\end{document}
"""


class Fixture:
    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="checkfix_")
        for f in ("slidestyle.sty", "docstyle.sty", "shared.sty", "build_slides.sh"):
            shutil.copy(os.path.join(HERE, f), self.dir)
        os.symlink(os.path.join(HERE, "fonts"), os.path.join(self.dir, "fonts"))

    def p(self, name):
        return os.path.join(self.dir, name)

    def deck(self, text=DECK):
        with open(self.p("slides9.tex"), "w") as fh:
            fh.write(text)
        r = subprocess.run(["bash", self.p("build_slides.sh"), "9"], capture_output=True, text=True)
        return r.returncode == 0

    def sheet(self, text=SHEET):
        with open(self.p("hw9.tex"), "w") as fh:
            fh.write(text)
        ok = True
        for args in (["hw9.tex"], ["-jobname=hw9_answers", r"\def\withanswers{1}\input{hw9.tex}"]):
            for _ in range(2):
                ok &= subprocess.run(["xelatex", "-interaction=nonstopmode"] + args, cwd=self.dir,
                                     capture_output=True).returncode == 0
        return ok

    def pptx(self):
        export_pptx.export(9, here=self.dir)
        return self.p("slides9.pptx")


def all_tex_checks(fx):
    ex = export_pptx.Expander(fx.p("shared.sty")).expand
    deck = open(fx.p("slides9.tex")).read()
    sheet = open(fx.p("hw9.tex")).read()
    logs = [fx.p(x) for x in ("slides9_screen.log", "slides9_notes.log", "slides9.log", "hw9.log", "hw9_answers.log")]
    printed = [fx.p(x) for x in ("slides9_screen.pdf", "hw9.pdf", "hw9_answers.pdf")]
    return {
        "1": check.check_logs(logs),
        "1b": check.check_footer_clear(fx.p("slides9_screen.pdf")),
        "1c": check.check_notes_inside(fx.p("slides9_notes.pdf")),
        "1d": sum((check.check_dark_fills(f, whitelist={}) for f in printed), []),
        "2": check.check_fonts(printed, logs),
        "3": check.check_no_answers(deck),
        "4": check.check_fractions({"slides9.tex": deck, "hw9.tex": sheet}),
        "5": check.check_banned(deck),
        "5b": check.check_frames(deck),
        "10s": check.check_notes_source(deck, ex),
        "12": check.check_spot_error(deck, {"hw9.tex": sheet}, fx.p("shared.sty")),
        "13": check.check_say_it(deck, ex),
        "14": check.check_layout_pair(fx.p("hw9.pdf"), fx.p("hw9_answers.pdf")),
        "15": check.check_page_numbers(fx.p("slides9_screen.pdf")),
        "16": check.check_languages(deck, {"hw9.tex": sheet}),
    }


def all_pptx_checks(fx, pptx):
    deck = open(fx.p("slides9.tex")).read()
    return {
        "7": check.check_alignment(deck, fx.p("slides9.pdf"), pptx),
        "8": check.check_pure_images(pptx),
        "9": check.check_no_note_images(pptx),
        "10": check.check_notes_pptx(deck, pptx),
        "11": check.check_notes_maths(deck, pptx),
    }


# item: (description, deck mutation or None, sheet mutation or None)
def sub(marker, text):
    return lambda s: s.replace(marker, text)


TEX_MUTATIONS = [
    ("1", "overfull formula box", sub("%BODY1", r"\fbx{x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x}"), None),
    ("1b", "overlay node in the footer", sub("%BODY1",
        r"\tikz[remember picture,overlay]\node[anchor=south west] at ([xshift=40mm,yshift=2mm]current page.south west) {intruder};"), None),
    ("1c", "note running off the page", sub("%NOTE1", "".join(r"\par 多余的一行 extra line" for _ in range(60))), None),
    ("1d", "solid dark bar", sub("%BODY1", r"\par\rule{40mm}{12mm}"), None),
    ("2", "glyph missing from the font", sub("%BODY1", "\u2603"), None),
    ("3", "numeral after a mark allocation", sub(r"\smk{2}%BODY3", r"\smk{2} 3"), None),
    ("3", "reveal header on screen", sub("%BODY3", "Answer: 7"), None),
    ("4", "slash fraction in maths", sub("%BODY1", r"$x/y$"), None),
    ("4", "stacked fraction on a 9 mm line", None, sub("%SHEET1", r"\al{$\dfrac{1}{2}$}")),
    ("4", "unspaced slash in note prose", sub("%NOTE3", r"\par a/b"), None),
    ("5", "banned size command", sub("%BODY1", r"{\small tiny text}"), None),
    ("5b", "frame body without relax", lambda s: s.replace("\\begin{frame}{Practice}\n\\relax", "\\begin{frame}{Practice}"), None),
    ("10s", "labels out of order", lambda s: s.replace("Short solution:\\par\nQ1 difference", "Watch for:\\par\nx\\par\nShort solution:\\par\nQ1 difference"), None),
    ("10s", "Do Now without Diagnostic", lambda s: s.replace("Diagnostic:\\par", "Ask:\\par"), None),
    ("10s", "bad Say it line", lambda s: s.replace("index = IN-deks", "index = index"), None),
    ("12", "count does not match the numbering", lambda s: s.replace("has 2 errors", "has 3 errors"), None),
    ("12", "sheet: answer block shorter than the count", None, lambda s: s.replace("has 1 error.", "has 2 errors.")),
    # the word is on slide 1, its Say it on slide 3: said before it is pronounced
    ("13", "word used before its Say it",
     lambda s: s.replace("%BODY1", " cuboid").replace("%NOTE3", "\\par\nSay it:\\par\ncuboid = KYOO-boyd"), None),
    # the same word (same stem) pronounced on slide 1 and again on slide 3
    ("13", "word pronounced twice", sub("%NOTE3", "\\par\nSay it:\\par\nindex = IN-deks"), None),
    ("14", "answer-only line moves the layout", None, sub("%SHEET1", r"\ifansmode\par extra answer line\par\fi")),
    ("14", "answer printed on the blank sheet", None, sub("%SHEET1", r"\par{\color{ansred}leaked}")),
    ("15", "page number removed", lambda s: s.replace("\\begin{document}", "\\renewcommand\\thetotal{}\\begin{document}"), None),
    ("16", "Chinese on screen", sub("%BODY1", "中文"), None),
]


def run():
    fails = []
    fx = Fixture()
    assert fx.deck() and fx.sheet(), "fixture does not compile"
    clean = all_tex_checks(fx)
    noisy = {k: v for k, v in clean.items() if v}
    if noisy:
        print("clean fixture is not clean:", noisy)
        return 1
    pptx = fx.pptx()
    noisy = {k: v for k, v in all_pptx_checks(fx, pptx).items() if v}
    if noisy:
        print("clean fixture PPTX is not clean:", noisy)
        return 1
    print("clean fixture passes every check")

    only = sys.argv[1:]
    for item, what, dm, sm in TEX_MUTATIONS:
        if only and item not in only:
            continue
        f2 = Fixture()
        d = dm(DECK) if dm else DECK
        s = sm(SHEET) if sm else SHEET
        assert d != DECK or s != SHEET, f"mutation '{what}' changed nothing"
        f2.deck(d)
        f2.sheet(s)
        if item == "1c":    # the fault must really be there: words off the page are not reported
            assert subprocess.run(["pdftotext", f2.p("slides9_notes.pdf"), "-"], capture_output=True,
                                  text=True).stdout.count("extra line") < 60, "overflow fixture did not overflow"
        res = all_tex_checks(f2)
        caught = bool(res[item])
        print(f"{'caught' if caught else 'MISSED':7} {item:>4}  {what}")
        if not caught:
            fails.append((item, what))
        shutil.rmtree(f2.dir, ignore_errors=True)

    # PPTX mutations edit the exported file
    def edit(pptx, fn, out):
        zin = zipfile.ZipFile(pptx)
        zout = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
        for it in zin.infolist():
            data = zin.read(it.filename)
            data = fn(it.filename, data)
            if data is not None:
                zout.writestr(it, data)
        zout.close()
        return out

    def drop_slide(name, data):
        if name == "ppt/presentation.xml":
            return re.sub(rb"<p:sldId [^>]*/>", b"", data, count=1)
        return data

    def extra_shape(name, data):
        if name == "ppt/slides/slide1.xml":
            return data.replace(b"</p:spTree>", b'<p:sp><p:nvSpPr><p:cNvPr id="99" name="x"/><p:cNvSpPr/>'
                                b'<p:nvPr/></p:nvSpPr><p:spPr/></p:sp></p:spTree>')
        return data

    def note_pic(name, data):
        if name == "ppt/notesSlides/notesSlide1.xml":
            return data.replace(b"</p:spTree>", b'<p:pic><p:nvPicPr><p:cNvPr id="98" name="p"/><p:cNvPicPr/>'
                                b'<p:nvPr/></p:nvPicPr><p:blipFill/><p:spPr/></p:pic></p:spTree>')
        return data

    def slash_in_math(name, data):
        if name == "ppt/notesSlides/notesSlide1.xml":
            return re.sub(rb"(<m:t[^>]*>)x", rb"\1x/2", data, count=1)
        return data

    def note_header(name, data):
        if name == "ppt/notesSlides/notesSlide1.xml":
            return data.replace("Short solution:".encode(), "Answer:".encode(), 1)
        return data

    for item, what, fn in (("7", "slide missing", drop_slide), ("8", "extra shape on a slide", extra_shape),
                           ("9", "picture in the notes", note_pic), ("10", "Answer: header", note_header),
                           ("11", "slash inside a native equation", slash_in_math)):
        bad = edit(pptx, fn, fx.p("bad.pptx"))
        caught = bool(all_pptx_checks(fx, bad)[item])
        print(f"{'caught' if caught else 'MISSED':7} {item:>4}  {what}")
        if not caught:
            fails.append((item, what))

    # item 6: a real matplotlib import in a helper script
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write("import matplotlib.pyplot as plt\n")
    caught = bool(check.check_plots([fh.name]))
    print(f"{'caught' if caught else 'MISSED':7} {'6':>4}  matplotlib import")
    if not caught:
        fails.append(("6", "matplotlib import"))
    os.unlink(fh.name)

    shutil.rmtree(fx.dir, ignore_errors=True)
    print(f"\n{len(fails)} missed" if fails else "\nevery planted fault was caught")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(run())
