#!/usr/bin/env python3
"""Export slides.pptx from the double-width slides.pdf and slides.tex (spec 9.2).

* Each slide is one full-bleed 3840 x 2160 PNG of the left (screen) half.
* Notes come from the \\note{} bodies in slides.tex (brace matching, split at
  \\par). Each $...$ becomes a native PowerPoint equation (OMML from pandoc,
  inside mc:AlternateContent / a14:m) with a linear fallback.
* Project macros in the notes (\\Lref{key}) are expanded from their
  definitions in shared.sty (\\defL{key}{n}{text}); the exporter keeps no
  copy of its own (spec 9.2).
* Frames = PDF pages = PPTX slides, or nothing is written.
"""
import copy
import io
import os
import re
import subprocess
import sys
import tempfile
import zipfile

import pymupdf
from lxml import etree
from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
NOTE_PT = 16


def strip_comments(tex):
    return re.sub(r"(?<!\\)%[^\n]*", "", tex)


def brace_body(tex, start):
    """tex[start] == '{'; return (body, index after closing brace)."""
    depth = 0
    for i in range(start, len(tex)):
        c = tex[i]
        if c == "\\":
            continue
        if c == "{" and tex[i - 1] != "\\":
            depth += 1
        elif c == "}" and tex[i - 1] != "\\":
            depth -= 1
            if depth == 0:
                return tex[start + 1:i], i + 1
    raise ValueError("unbalanced braces")


def frames_and_notes(path):
    tex = open(path, encoding="utf-8").read()
    body = tex[tex.index("\\begin{document}"):]
    frames = re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", body, re.S)
    notes = []
    for fr in frames:
        idx = [m.start() for m in re.finditer(r"\\note\{", fr)]
        if len(idx) != 1:
            raise SystemExit(f"frame without exactly one \\note: {fr[:60]!r}")
        # keep the % that follows \note{ out of the text
        text, _ = brace_body(fr, idx[0] + len("\\note"))
        notes.append(strip_comments(text))
    return frames, notes


def shared_macros():
    """\\Lref{key} -> 'L<n>', read from shared.sty, longest key first."""
    sty = strip_comments(open(os.path.join(HERE, "shared.sty"), encoding="utf-8").read())
    table = {k: f"L{n}" for k, n in re.findall(r"\\defL\{([^}]*)\}\{(\d+)\}", sty)}
    if not table:
        raise SystemExit("no \\defL definitions found in shared.sty")
    return table


LREF = None


def expand_project(s):
    global LREF
    if LREF is None:
        LREF = shared_macros()

    def rep(m):
        key = m.group(1)
        if key not in LREF:
            raise SystemExit(f"\\Lref{{{key}}} is not defined in shared.sty")
        return LREF[key]
    return re.sub(r"\\Lref\{([^}]*)\}", rep, s)


TEXT_MACROS = [
    (r"\textdegree{}", "\u00b0"), (r"\textdegree", "\u00b0"),
    (r"\textperiodcentered{}", "\u00b7"), (r"\textperiodcentered", "\u00b7"),
    (r"\_", "_"), (r"\%", "%"), (r"\&", "&"), ("~", " "), (r"\,", "\u2009"),
    (r"\textbackslash{}", "\\"),
    (r"\ ", " "),
]


def expand_text(s):
    s = expand_project(s)
    for a, b in TEXT_MACROS:
        s = s.replace(a, b)
    s = re.sub(r"\s+", " ", s)
    left = re.findall(r"\\[A-Za-z]+", s)
    if left:
        raise SystemExit(f"unexpanded macro in note text: {left} in {s!r}")
    return s.strip()


def split_note(note):
    """Return a list of lines; each line is a list of ('t', text) / ('m', latex)."""
    lines = []
    for raw in re.split(r"\\par\b", note):
        raw = raw.strip()
        if not raw:
            continue
        parts = re.split(r"(\$[^$]+\$)", raw)
        segs = []
        for p in parts:
            if not p:
                continue
            if p.startswith("$"):
                segs.append(("m", p[1:-1]))
            else:
                t = expand_text(p)
                if t:
                    segs.append(("t", (" " if p[:1].isspace() else "") + t + (" " if p[-1:].isspace() else "")))
        lines.append(segs)
    return lines


def linear(latex):
    s = latex
    for _ in range(4):
        s = re.sub(r"\\dfrac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\(mathrm|text|mathbf)\{([^{}]*)\}", r"\2", s)
    s = s.replace(r"^\circ", "\u00b0").replace(r"\theta", "\u03b8").replace(r"\sin", "sin ")
    s = s.replace(r"\times", "\u00d7").replace(r"\,", "\u2009").replace(r"\ ", " ")
    s = re.sub(r"_(\w)", r"\1", s)
    s = re.sub(r"[{}]", "", s)
    return s


def omml_for(equations):
    """One pandoc call for all equations; returns a list of m:oMath elements."""
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "eq.tex")
        out = os.path.join(td, "eq.docx")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write("\\documentclass{article}\\begin{document}\n")
            for e in equations:
                fh.write(f"${e}$\n\n")
            fh.write("\\end{document}\n")
        subprocess.run(["pandoc", "-f", "latex", "-t", "docx", "-o", out, src], check=True)
        xml = zipfile.ZipFile(out).read("word/document.xml")
    root = etree.fromstring(xml)
    maths = root.findall(".//m:oMath", NS)
    if len(maths) != len(equations):
        raise SystemExit(f"pandoc returned {len(maths)} equations for {len(equations)}")
    return maths


def a_rpr(italic):
    rpr = etree.Element(f"{{{NS['a']}}}rPr", lang="en-US", sz=str(NOTE_PT * 100), i="1" if italic else "0")
    etree.SubElement(rpr, f"{{{NS['a']}}}latin", typeface="Cambria Math",
                     panose="02040503050406030204", pitchFamily="18", charset="0")
    return rpr


def to_pptx_math(om):
    om = copy.deepcopy(om)
    for r in om.iter(f"{{{NS['m']}}}r"):
        for w in r.findall(f"{{{NS['w']}}}rPr"):
            r.remove(w)
        mrpr = r.find("m:rPr", NS)
        plain = mrpr is not None and mrpr.find("m:sty", NS) is not None and \
            mrpr.find("m:sty", NS).get(f"{{{NS['m']}}}val") == "p"
        pos = 1 if mrpr is not None else 0
        txt = "".join(t.text or "" for t in r.findall("m:t", NS))
        r.insert(pos, a_rpr(not plain and any(ch.isalpha() for ch in txt)))
    for w in list(om.iter(f"{{{NS['w']}}}rPr")):
        w.getparent().remove(w)
    for c in list(om.iter(f"{{{NS['m']}}}ctrlPr")):
        if len(c) == 0:
            c.append(a_rpr(True))
    etree.cleanup_namespaces(om)
    return om


SAY_BLUE = "0046BE"     # Say it lines, same blue as the teacher PDF


def text_run(text, colour=None):
    r = etree.Element(f"{{{NS['a']}}}r")
    rpr = etree.SubElement(r, f"{{{NS['a']}}}rPr", lang="zh-CN", sz=str(NOTE_PT * 100), dirty="0")
    if colour:
        fill = etree.SubElement(rpr, f"{{{NS['a']}}}solidFill")
        etree.SubElement(fill, f"{{{NS['a']}}}srgbClr", val=colour)
    etree.SubElement(rpr, f"{{{NS['a']}}}latin", typeface="Arial")
    etree.SubElement(rpr, f"{{{NS['a']}}}ea", typeface="Microsoft YaHei")
    t = etree.SubElement(r, f"{{{NS['a']}}}t")
    t.text = text
    return r


def math_block(om, fallback):
    ac = etree.Element(f"{{{NS['mc']}}}AlternateContent", nsmap={"mc": NS["mc"]})
    ch = etree.SubElement(ac, f"{{{NS['mc']}}}Choice", Requires="a14", nsmap={"a14": NS["a14"]})
    m = etree.SubElement(ch, f"{{{NS['a14']}}}m")
    m.append(om)
    fb = etree.SubElement(ac, f"{{{NS['mc']}}}Fallback")
    fb.append(text_run(fallback))
    return ac


def main():
    deck = sys.argv[1] if len(sys.argv) > 1 else "slides"
    frames, notes = frames_and_notes(os.path.join(HERE, deck + ".tex"))
    pdf = pymupdf.open(os.path.join(HERE, deck + ".pdf"))
    if not (len(frames) == pdf.page_count):
        raise SystemExit(f"frames {len(frames)} != PDF pages {pdf.page_count}; nothing written")

    parsed = [split_note(n) for n in notes]
    eqs = [seg[1] for lines in parsed for line in lines for seg in line if seg[0] == "m"]
    maths = iter(omml_for(eqs)) if eqs else iter(())

    prs = Presentation()
    prs.slide_width = Emu(12192000)
    prs.slide_height = Emu(6858000)
    sw, sh = prs.slide_width, prs.slide_height
    blank = prs.slide_layouts[6]

    for k, page in enumerate(pdf):
        r = page.rect
        clip = pymupdf.Rect(0, 0, r.width / 2, r.height)
        mat = pymupdf.Matrix(3840 / clip.width, 2160 / clip.height)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
        if (pix.width, pix.height) != (3840, 2160):
            raise SystemExit(f"slide {k+1}: image {pix.width}x{pix.height}")
        slide = prs.slides.add_slide(blank)
        for shp in list(slide.shapes):
            shp._element.getparent().remove(shp._element)
        slide.shapes.add_picture(io.BytesIO(pix.tobytes("png")), 0, 0, width=sw, height=sh)

        tf = slide.notes_slide.notes_text_frame
        body = tf._txBody
        bpr = body.find("a:bodyPr", NS)
        for child in list(bpr):
            bpr.remove(child)
        etree.SubElement(bpr, f"{{{NS['a']}}}noAutofit")
        for p in body.findall("a:p", NS):
            body.remove(p)
        in_say = False
        for line in parsed[k]:
            p = etree.SubElement(body, f"{{{NS['a']}}}p")
            if len(line) == 1 and line[0] == ("t", "Say it:"):
                in_say = True
            for kind, val in line:
                if kind == "t":
                    p.append(text_run(val, SAY_BLUE if in_say else None))
                else:
                    p.append(math_block(to_pptx_math(next(maths)), linear(val)))
            end = etree.SubElement(p, f"{{{NS['a']}}}endParaRPr", lang="zh-CN", sz=str(NOTE_PT * 100))

    if len(prs.slides) != len(frames):
        raise SystemExit("slide count mismatch; nothing written")
    out = os.path.join(HERE, deck + ".pptx")
    prs.save(out)
    print(f"{deck}.pptx: {len(prs.slides)} slides, {len(eqs)} native equations in notes")


if __name__ == "__main__":
    main()
