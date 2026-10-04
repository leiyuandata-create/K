#!/usr/bin/env python3
"""Mutation tests for check.py (spec 10.3.6): plant one fault per item in a
scratch copy and confirm it is caught. Each fixture is verified too, so a
check cannot look blind because the fixture lacked the fault. Fixtures
anchor on short patterns and build replacements with callables, never on
long literals from the material (spec 10.3.6)."""
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

import pymupdf

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


SLIDES = C.read("slides.tex")


def sub1(pattern, repl, text):
    """One regex substitution with a callable; asserts the anchor matched."""
    new, n = re.subn(pattern, lambda m: repl(m), text, count=1)
    assert n == 1, f"fixture anchor not found: {pattern}"
    return new


# 1 -------------------------------------------------------------------
log = tmp("a.log")
open(log, "w").write("Overfull \\vbox (3.0pt too high) detected\n! Undefined control sequence.\n")
case("1", "Overfull \\vbox and an error in a log", len(C.check_logs([log])) == 2)

# 1b ------------------------------------------------------------------
pdf = tmp("footer.pdf")
d = pymupdf.open()
pg = d.new_page(width=481.89, height=271.06)
pg.insert_text((300, 200), "Dr. Ryan Lei", fontsize=8)      # a footer that has drifted up
pg.insert_text((20, 199), "overflow", fontsize=15)
d.save(pdf)
ws, _ = C.words(pdf)
fx = any(w[4] == "overflow" for w in ws[0])
case("1b", "body word on a drifted footer (found by text, not position)", C.check_footer_clear(pdf), fx)

# 1c ------------------------------------------------------------------
pdf = tmp("notes.pdf")
d = pymupdf.open()
d.new_page(width=481.89, height=271.06).insert_text((1, 100), "edge", fontsize=9)
d.save(pdf)
case("1c", "note text touching the edge", C.check_notes_inside(pdf))

# 1d ------------------------------------------------------------------
import pikepdf
pdf = tmp("dark.pdf")
with pikepdf.new() as pd:
    pd.add_blank_page(page_size=(595, 842))
    # white set outside, black set inside BT..ET (as TeX does), then a fill
    pd.pages[0].Contents = pd.make_stream(b"1 g BT 0 g ET 100 100 120 60 re f")
    pd.save(pdf)
ren = pymupdf.open(pdf)[0].get_pixmap(dpi=72, colorspace=pymupdf.csGRAY)
fx = min(ren.samples) < 60
case("1d", "dark fill whose colour is set inside BT..ET", C.check_dark_fills(pdf), fx)
case("1d", "a real sheet (outlined boxes) is not a false alarm", not C.check_dark_fills(C.p("classwork_answers.pdf")))

# 2 -------------------------------------------------------------------
pdf = tmp("font.pdf")
d = pymupdf.open()
d.new_page().insert_text((72, 72), "unembedded", fontname="helv")
d.save(pdf)
out = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
fx = len(out.splitlines()) > 2 and out.splitlines()[2].split()[-5] == "no"
case("2", "unembedded base-14 font", C.check_fonts([pdf], []), fx)
log = tmp("b.log")
open(log, "w").write("Missing character: There is no x in font nullfont!\n")
case("2", "Missing character in a log", C.check_fonts([], [log]))

# 3 -------------------------------------------------------------------
t = sub1(r"\\slv\{A\}", lambda m: r"\smk{2} 1.8 mm", SLIDES)
case("3", "numeral after a \\smk allocation", C.check_no_answers(t), r"\smk{2} 1.8" in t)
t = sub1(r"\\qline\{1\}", lambda m: r"Answer: anther \qline{1}", SLIDES)
case("3", "reveal header on screen", C.check_no_answers(t))

# 4 -------------------------------------------------------------------
t = sub1(r"= \\dfrac\{36", lambda m: r"= 36/20 + \dfrac{36", SLIDES)
case("4", "slash fraction in note maths", C.check_fractions({"slides.tex": t}))
hw = C.read("hw1.tex")
t = sub1(r"\\alines\{1\}\{12 g", lambda m: r"\alines{1}{$\dfrac{12}{1}$ 12 g", hw)
case("4", "stacked fraction on a 9 mm line", C.check_fractions({"hw1.tex": t}))
case("4", "real sources are clean", not C.check_fractions({n: C.read(n) for n in C.TEX}))

# 5 / 5b --------------------------------------------------------------
t = sub1(r"\\qline\{1\} Which part", lambda m: r"\small\qline{1} Which part", SLIDES)
case("5", "\\small in a frame", C.check_banned(t))
t = sub1(r"\\begin\{frame\}\{Do Now\}\n\\relax", lambda m: "\\begin{frame}{Do Now}\n{oops}\\relax", SLIDES)
case("5b", "brace group after a frame title", C.check_frames(t))

# 10 (source) ---------------------------------------------------------
t = sub1(r"Q1 anther\\par", lambda m: "Q1 花药 anther\\par", SLIDES)
case("10s", "Chinese in an answer line", C.check_notes_structure_src(t))
t = sub1(r"Which part of a flower", lambda m: "花 Which part of a flower", SLIDES)
case("10s", "Chinese on screen", C.check_notes_structure_src(t))
t = sub1(r"ovule = OV-yool", lambda m: "ovule = ov-yool", SLIDES)
case("10s", "Say it line without a stressed syllable", C.check_notes_structure_src(t))
t = sub1(r"Diagnostic:\\par", lambda m: "Diagnostic:\\par\nShort solution:\\par", SLIDES)
case("10s", "repeated label line", C.check_notes_structure_src(t))
t = sub1(r"Q1 anther\\par", lambda m: "Q1 anther\uff08x\uff09\\par", SLIDES)
case("10s", "full-width bracket in a note", C.check_notes_structure_src(t))
case("10s", "real deck is clean", not C.check_notes_structure_src(SLIDES))

# 10 / 11 (PPTX) ------------------------------------------------------
src = C.p("slides.pptx")
bad = tmp("bad.pptx")


def mutate_pptx(fn):
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(bad, "w", zipfile.ZIP_DEFLATED) as zo:
        done = False
        for item in zi.infolist():
            data = zi.read(item.filename)
            if not done and item.filename.startswith("ppt/notesSlides/notesSlide"):
                new = fn(data.decode("utf-8"))
                if new is not None:
                    data, done = new.encode("utf-8"), True
            zo.writestr(item, data)
    return done


fx = mutate_pptx(lambda x: x.replace("<a:t>Q1 anther</a:t>", "<a:t>Q1 \\Lref{pollfert}</a:t>", 1)
                 if "<a:t>Q1 anther</a:t>" in x else None)
case("10", "LaTeX macro surviving into the notes", C.check_notes_structure(SLIDES, bad), fx)
fx = mutate_pptx(lambda x: re.sub(r"<m:fPr>", '<m:fPr><m:type m:val="lin"/>', x, count=1)
                 if "<m:fPr>" in x else None)
case("11", "linear fraction in note maths", C.check_notes_maths(SLIDES, bad), fx)

# 12 ------------------------------------------------------------------
t = sub1(r"has 3 errors", lambda m: "has 4 errors", SLIDES)
case("12", "stated count differs from the numbered answers", C.check_spot_error(t, {}))
t = sub1(r"\\qline\{1\} Which part", lambda m: r"\flawed{x}\qline{1} Which part", SLIDES)
case("12", "\\flawed outside a Spot the error frame", C.check_spot_error(t, {}))
hw = C.read("hw1.tex")
t = sub1(r"\(\\Lref\{respire\}\)", lambda m: "", hw)
case("12", "sheet answer block with too few \\Lref", C.check_spot_error(SLIDES, {"hw1.tex": t}))

# 13 ------------------------------------------------------------------
t = sub1(r"cuticle = KYOO-tih-kul\\par", lambda m: "cuticle = KYOO-tih-kul\\par\nstamens = STAY-munz\\par", SLIDES)
case("13", "plural pronounced twice (stem match)", C.check_sayit(t))
t = sub1(r"Which part of a flower makes pollen\?", lambda m: "Which part of a flower makes pollen? (palisade)", SLIDES)
case("13", "word used on screen before its Say it slide", C.check_sayit(t))
case("13", "real deck is clean", not C.check_sayit(SLIDES))

# 14 ------------------------------------------------------------------
for f in ("hw1.pdf", "hw1_answers.pdf"):
    shutil.copy(C.p(f), tmp(f))
d = pymupdf.open(C.p("hw1_answers.pdf"))
nd = pymupdf.open()
nd.insert_pdf(d)
page = nd[0]
# move the whole page content down 3 pt: every left-margin word shifts
page.set_mediabox(pymupdf.Rect(0, -3, page.rect.width, page.rect.height - 3))
nd.save(tmp("hw1s_answers.pdf"))
shutil.copy(C.p("hw1.pdf"), tmp("hw1s.pdf"))
orig_p = C.p
C.p = lambda name: tmp(name)
caught = C.check_layout_pairs([("hw1s", "hw1s_answers")])
clean = C.check_layout_pairs([("hw1", "hw1_answers")])
C.p = orig_p
case("14", "answer page shifted by 3 pt", caught)
case("14", "real pair is clean", not clean)

print()
n_fail = sum(1 for r in results if not r[2])
print(f"{len(results) - n_fail} of {len(results)} planted faults caught as expected")
raise SystemExit(1 if n_fail else 0)
