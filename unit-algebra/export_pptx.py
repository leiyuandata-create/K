#!/usr/bin/env python3
"""export_pptx.py N -- slidesN.pptx from slidesN.pdf (double width) and slidesN.tex (spec 9.2).

* Each slide is one full-bleed 3840 x 2160 PNG of the left (screen) half,
  re-encoded losslessly with maximum compression.
* Notes come from the \\note{} bodies in slidesN.tex (brace matching, split
  at \\par). Project macros (\\Lref, \\Lprefix, term macros) are expanded from
  their definitions in shared.sty -- the exporter keeps no copy of them.
* Each $...$ becomes a native PowerPoint equation (OMML from one pandoc call,
  inside mc:AlternateContent / a14:m) with a linear fallback.
* Every text run names a Latin and an East Asian font.
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
    depth, i = 0, start
    while i < len(tex):
        c = tex[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return tex[start + 1:i], i + 1
        i += 1
    raise ValueError("unbalanced braces")


class Expander:
    """Expands project macros in note text, reading their definitions from shared.sty."""

    def __init__(self, sty):
        src = strip_comments(open(sty, encoding="utf-8").read())
        self.L = {k: n for k, n, _ in re.findall(r"\\defL\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", src)}
        m = re.search(r"\\newcommand\\Lprefix\{([^}]*)\}", src)
        self.prefix = m.group(1) if m else "L"
        self.terms = {}
        for m in re.finditer(r"\\newcommand\\(T[A-Za-z]+)\{", src):
            body, _ = brace_body(src, m.end() - 1)
            self.terms[m.group(1)] = body

    def expand(self, s):
        s = re.sub(r"\\Lref\{([^}]*)\}", lambda m: self.prefix + self.L[m.group(1)], s)
        s = s.replace("\\Lprefix{}", self.prefix).replace("\\Lprefix", self.prefix)
        # longest name first, so \Tdots does not eat the start of \TDots-like names
        for name in sorted(self.terms, key=len, reverse=True):
            s = re.sub(r"\\" + name + r"(\{\})?(?![A-Za-z])", lambda _m, b=self.terms[name]: b, s)
        return s


def frames_and_notes(path):
    tex = strip_comments(open(path, encoding="utf-8").read())
    body = tex[tex.index("\\begin{document}"):]
    frames = re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", body, re.S)
    notes = []
    for fr in frames:
        idx = [m.start() for m in re.finditer(r"\\note\{", fr)]
        if len(idx) != 1:
            raise SystemExit(f"frame without exactly one \\note: {fr[:60]!r}")
        text, _ = brace_body(fr, idx[0] + len("\\note"))
        notes.append(text)
    return frames, notes


TEXT_MACROS = [
    (r"\textdegree{}", "\u00b0"), (r"\textdegree", "\u00b0"),
    (r"\textperiodcentered{}", "\u00b7"), (r"\textperiodcentered", "\u00b7"),
    (r"\ldots{}", "\u2026"), (r"\ldots", "\u2026"),
    (r"\_", "_"), (r"\%", "%"), (r"\&", "&"), ("~", " "), (r"\,", "\u2009"),
    (r"\ ", " "), ("``", "\u201c"), ("''", "\u201d"), ("--", "\u2013"),
]


def expand_text(s):
    for a, b in TEXT_MACROS:
        s = s.replace(a, b)
    s = re.sub(r"\s+", " ", s)
    left = re.findall(r"\\[A-Za-z]+", s)
    if left:
        raise SystemExit(f"unexpanded macro in note text: {left} in {s!r}")
    return s


def split_note(note, expand):
    """A list of lines; each line is a list of ('t', text) / ('m', latex)."""
    lines = []
    for raw in re.split(r"\\par\b", note):
        raw = expand(raw).strip()
        if not raw:
            continue
        segs = []
        for part in re.split(r"(?<!\\)(\$[^$]+\$)", raw):
            if not part:
                continue
            if part.startswith("$"):
                segs.append(("m", part[1:-1]))
            else:
                t = expand_text(part)
                if t.strip():
                    segs.append(("t", t))
        if segs and segs[0][0] == "t":
            segs[0] = ("t", segs[0][1].lstrip())
        if segs and segs[-1][0] == "t":
            segs[-1] = ("t", segs[-1][1].rstrip())
        lines.append(segs)
    return lines


def linear(latex):
    s = latex
    for _ in range(4):
        s = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
        s = re.sub(r"\\sqrt\[([^\]]*)\]\{([^{}]*)\}", "\\1\u221a(\\2)", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", "\u221a(\\1)", s)
    s = re.sub(r"\\(mathrm|text|mathbf)\{([^{}]*)\}", r"\2", s)
    for a, b in ((r"\times", "\u00d7"), (r"\div", "\u00f7"), (r"\neq", "\u2260"), (r"\pm", "\u00b1"),
                 (r"\leq", "\u2264"), (r"\geq", "\u2265"), (r"\quad", "  "), (r"\qquad", "    "),
                 (r"\Bigl", ""), (r"\Bigr", ""), (r"\left", ""), (r"\right", ""), (r"\cdot", "\u00b7"),
                 (r"\,", "\u2009"), (r"\ ", " "), (r"\;", " ")):
        s = s.replace(a, b)
    s = re.sub(r"\\[A-Za-z]+", "", s)
    s = re.sub(r"[{}]", "", s)
    return s


def omml_for(equations):
    """One pandoc call for all equations; returns a list of m:oMath elements."""
    from lxml import etree
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
    from lxml import etree
    rpr = etree.Element(f"{{{NS['a']}}}rPr", lang="en-US", sz=str(NOTE_PT * 100), i="1" if italic else "0")
    etree.SubElement(rpr, f"{{{NS['a']}}}latin", typeface="Cambria Math",
                     panose="02040503050406030204", pitchFamily="18", charset="0")
    return rpr


def to_pptx_math(om):
    from lxml import etree
    om = copy.deepcopy(om)
    for r in om.iter(f"{{{NS['m']}}}r"):
        for w in r.findall(f"{{{NS['w']}}}rPr"):
            r.remove(w)
        mrpr = r.find("m:rPr", NS)
        sty = mrpr.find("m:sty", NS) if mrpr is not None else None
        plain = sty is not None and sty.get(f"{{{NS['m']}}}val") == "p"
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


def text_run(text):
    from lxml import etree
    r = etree.Element(f"{{{NS['a']}}}r")
    rpr = etree.SubElement(r, f"{{{NS['a']}}}rPr", lang="zh-CN", altLang="en-US", sz=str(NOTE_PT * 100), dirty="0")
    etree.SubElement(rpr, f"{{{NS['a']}}}latin", typeface="Arial")
    etree.SubElement(rpr, f"{{{NS['a']}}}ea", typeface="Microsoft YaHei")
    t = etree.SubElement(r, f"{{{NS['a']}}}t")
    t.text = text
    return r


def math_block(om, fallback):
    from lxml import etree
    ac = etree.Element(f"{{{NS['mc']}}}AlternateContent", nsmap={"mc": NS["mc"]})
    ch = etree.SubElement(ac, f"{{{NS['mc']}}}Choice", Requires="a14", nsmap={"a14": NS["a14"]})
    m = etree.SubElement(ch, f"{{{NS['a14']}}}m")
    m.append(om)
    fb = etree.SubElement(ac, f"{{{NS['mc']}}}Fallback")
    fb.append(text_run(fallback))
    return ac


def export(n, here=HERE):
    import pymupdf
    from lxml import etree
    from PIL import Image
    from pptx import Presentation
    from pptx.util import Emu

    s = f"slides{n}"
    ex = Expander(os.path.join(here, "shared.sty"))
    frames, notes = frames_and_notes(os.path.join(here, s + ".tex"))
    pdf = pymupdf.open(os.path.join(here, s + ".pdf"))
    if len(frames) != pdf.page_count:
        raise SystemExit(f"frames {len(frames)} != PDF pages {pdf.page_count}; nothing written")

    parsed = [split_note(nt, ex.expand) for nt in notes]
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
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        buf.seek(0)
        slide = prs.slides.add_slide(blank)
        for shp in list(slide.shapes):
            shp._element.getparent().remove(shp._element)
        slide.shapes.add_picture(buf, 0, 0, width=sw, height=sh)

        body = slide.notes_slide.notes_text_frame._txBody
        bpr = body.find("a:bodyPr", NS)
        for child in list(bpr):
            bpr.remove(child)
        etree.SubElement(bpr, f"{{{NS['a']}}}noAutofit")
        for p_ in body.findall("a:p", NS):
            body.remove(p_)
        for line in parsed[k]:
            p_ = etree.SubElement(body, f"{{{NS['a']}}}p")
            for kind, val in line:
                if kind == "t":
                    p_.append(text_run(val))
                else:
                    p_.append(math_block(to_pptx_math(next(maths)), linear(val)))
            etree.SubElement(p_, f"{{{NS['a']}}}endParaRPr", lang="zh-CN", sz=str(NOTE_PT * 100))

    if len(prs.slides) != len(frames):
        raise SystemExit("slide count mismatch; nothing written")
    out = os.path.join(here, s + ".pptx")
    prs.save(out)
    mb = os.path.getsize(out) / 1e6
    print(f"{s}.pptx: {len(prs.slides)} slides, {len(eqs)} native equations in notes, {mb:.1f} MB")
    if mb > 30:
        raise SystemExit(f"{s}.pptx is {mb:.1f} MB, over the 30 MB upload limit")


if __name__ == "__main__":
    export(sys.argv[1])
