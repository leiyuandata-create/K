#!/usr/bin/env python3
"""Mutation tests for check.py (spec 10.3.6): plant one fault per item in a
scratch copy and confirm it is caught. Each fixture is verified too, so a
check cannot look blind because the fixture lacked the fault."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import pymupdf
from lxml import etree
from pptx import Presentation
from pptx.util import Pt

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
TD = tempfile.mkdtemp()
results = []


def case(item, name, caught, fixture_ok=True):
    ok = bool(caught) and fixture_ok
    results.append((item, name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {item:>3}  {name}")


def tmp(name):
    return os.path.join(TD, name)


# 1 -------------------------------------------------------------------
log = tmp("a.log")
open(log, "w").write("Overfull \\hbox (3.0pt too wide) in paragraph\n! Undefined control sequence.\n")
case("1", "Overfull and error in a log", len(C.check_logs([log])) == 2)

# 1b ------------------------------------------------------------------
pdf = tmp("footer.pdf")
d = pymupdf.open()
pg = d.new_page(width=481.89, height=271.06)
pg.insert_text((300, 265), "Dr. Ryan Lei", fontsize=8)
pg.insert_text((20, 264), "overflow", fontsize=15)
d.save(pdf)
ws, _ = C.words(pdf)
fx = any(w[4] == "overflow" for w in ws[0]) and any(w[4] == "Ryan" for w in ws[0])
case("1b", "body word running into the footer", C.check_footer_clear(pdf), fx)

# 1c ------------------------------------------------------------------
pdf = tmp("notes.pdf")
d = pymupdf.open()
pg = d.new_page(width=481.89, height=271.06)
pg.insert_text((1, 100), "edge", fontsize=9)
d.save(pdf)
case("1c", "note text touching the edge", C.check_notes_inside(pdf))

# 1d ------------------------------------------------------------------
pdf = tmp("dark.pdf")
d = pymupdf.open(os.path.join(HERE, "handout.pdf"))
d.select([0])
d[0].draw_rect(pymupdf.Rect(100, 700, 160, 730), color=(0, 0, 0), fill=(0, 0, 0))
d.save(pdf)
img = d[0].get_pixmap(dpi=72, colorspace=pymupdf.csGRAY, clip=pymupdf.Rect(110, 705, 150, 725))
fx = max(img.samples) < 60
case("1d", "solid dark rectangle on a handout page", C.check_dark_fills(pdf), fx)
clean = tmp("clean.pdf")
d = pymupdf.open(os.path.join(HERE, "handout.pdf"))
d.select([0])
d.save(clean)
case("1d", "framed box (keybox) is not a false alarm", not C.check_dark_fills(clean))

# 2 -------------------------------------------------------------------
pdf = tmp("font.pdf")
d = pymupdf.open()
d.new_page().insert_text((72, 72), "unembedded", fontname="helv")
d.save(pdf)
out = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
fx = "no" in out.splitlines()[2].split()
case("2", "base-14 font not embedded", C.check_fonts([pdf], []), fx)

# 3 -------------------------------------------------------------------
tex = "\\begin{document}\\begin{frame}{Practice}\\relax Q1 [2] What is 3?\\note{Q1 3}\\end{frame}"
case("3", "numeral after a mark allocation", C.check_no_answers(tex))
tex = "\\begin{document}\\begin{frame}{Practice}\\relax Answer: 5\\note{Q1 5}\\end{frame}"
case("3", "Answer: header on screen", C.check_no_answers(tex))
tex = "\\begin{document}\\begin{frame}{Practice}\\relax Q1\\note{Q1 Answer: 5}\\end{frame}"
case("3", "Answer: inside a note is not flagged", not C.check_no_answers(tex))

# 4 -------------------------------------------------------------------
case("4", "slash fraction $d/t$", C.check_fractions({"x": "speed $= d/t$"}))
case("4", "unit km/s is whitelisted", not C.check_fractions({"x": "$300\\ \\mathrm{km/s}$"}))
case("4", "Unicode superscript in text", C.check_fractions({"x": "area in m\u00b2"}))
case("4", "^ in note prose", C.check_fractions({"x": "\\note{x^2 is wrong}"}))
case("4", "\\\\[2mm] is not display maths", not C.check_fractions({"x": "a\\\\[2mm] b/c"}))

# 5 -------------------------------------------------------------------
case("5", "\\small in a frame", C.check_banned("\\begin{document}\\begin{frame}{T}\\relax\\small x\\note{y}\\end{frame}"))
case("5", "\\pause in a frame", C.check_banned("\\begin{document}\\begin{frame}{T}\\relax a\\pause b\\note{y}\\end{frame}"))
case("5", "TikZ font= option", C.check_banned("\\begin{document}\\begin{frame}{T}\\relax\\node[font=\\large]{a};\\note{y}\\end{frame}"))
case("5", "size command inside a note is allowed",
     not C.check_banned("\\begin{document}\\begin{frame}{T}\\relax a\\note{\\small y}\\end{frame}"))

# 5b ------------------------------------------------------------------
case("5b", "brace group after the title", C.check_frames("\\begin{frame}{T}{body}\\note{x}\\end{frame}"))
case("5b", "two notes in a frame", C.check_frames("\\begin{frame}{T}\\relax a\\note{x}\\note{y}\\end{frame}"))
case("5b", "body without \\relax", C.check_frames("\\begin{frame}{T} a\\note{x}\\end{frame}"))

# 6 -------------------------------------------------------------------
py = tmp("plot.py")
open(py, "w").write("import matplotlib.pyplot as plt\n")
case("6", "real matplotlib import", C.check_plots([py]))
open(py, "w").write("# the word matplotlib in a comment\n")
case("6", "the word alone is not an import", not C.check_plots([py]))

# 7-11: mutate a copy of the real deck ---------------------------------
SRC = os.path.join(HERE, "slides.pptx")
slides_tex = open(os.path.join(HERE, "slides.tex"), encoding="utf-8").read()

extra = slides_tex.replace("\\end{document}", "\\begin{frame}{X}\\relax\\note{x}\\end{frame}\n\\end{document}")
case("7", "one frame more than slides", C.check_alignment(extra, os.path.join(HERE, "slides.pdf"), SRC))

x8 = tmp("x8.pptx")
prs = Presentation(SRC)
prs.slides[0].shapes.add_textbox(0, 0, Pt(100), Pt(20)).text = "stray"
prs.save(x8)
case("8", "text box on a slide", C.check_pure_images(x8))

def edit_notes(src, dst, slide_no, fn):
    zin = zipfile.ZipFile(src)
    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    rels = zin.read(f"ppt/slides/_rels/slide{slide_no}.xml.rels").decode()
    target = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', rels).group(1)
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == f"ppt/notesSlides/{target}":
            data = fn(data.decode("utf-8")).encode("utf-8")
        zout.writestr(item, data)
    zout.close()


x9 = tmp("x9.pptx")
PIC = ('<p:pic><p:nvPicPr><p:cNvPr id="99" name="pic"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>'
       '<p:blipFill><a:blip r:embed="rId99"/></p:blipFill><p:spPr/></p:pic>')
edit_notes(SRC, x9, 2, lambda s: s.replace("</p:spTree>", PIC + "</p:spTree>", 1))
fx = "<p:pic" in zipfile.ZipFile(x9).read("ppt/notesSlides/notesSlide2.xml").decode()
case("9", "picture in a notes slide", C.check_no_note_images(x9), fx)



x10 = tmp("x10.pptx")
edit_notes(SRC, x10, 2, lambda s: s.replace(">Diagnostic:<", ">Notes:<"))
fx = "Diagnostic:" not in zipfile.ZipFile(x10).read("ppt/notesSlides/notesSlide2.xml").decode()
case("10", "Do Now without Diagnostic:", C.check_notes_structure(slides_tex, x10), fx)

x10b = tmp("x10b.pptx")
edit_notes(SRC, x10b, 8, lambda s: s.replace(">Q1 <", ">Answer: <", 1))
case("10", "Answer: header in notes", C.check_notes_structure(slides_tex, x10b))

x11 = tmp("x11.pptx")
edit_notes(SRC, x11, 8, lambda s: s.replace("<m:t>500</m:t>", "<m:t>500/2</m:t>", 1))
fx = "500/2" in zipfile.ZipFile(x11).read("ppt/notesSlides/notesSlide8.xml").decode()
case("11", "slash inside a native equation", C.check_notes_maths(slides_tex, x11), fx)

x11b = tmp("x11b.pptx")
edit_notes(SRC, x11b, 8, lambda s: re.sub(r"<mc:Fallback>.*?</mc:Fallback>", "", s, count=1, flags=re.S))
case("11", "equation without a fallback", C.check_notes_maths(slides_tex, x11b))

x11c = tmp("x11c.pptx")
edit_notes(SRC, x11c, 8, lambda s: s.replace("Short solution:", "x^2 Short solution:", 1))
case("11", "^ in note prose", C.check_notes_maths(slides_tex, x11c))

shutil.rmtree(TD)
failed = [r for r in results if not r[2]]
print(f"\n{len(results) - len(failed)} of {len(results)} planted faults handled correctly")
sys.exit(1 if failed else 0)
