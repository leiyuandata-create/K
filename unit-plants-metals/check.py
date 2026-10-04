#!/usr/bin/env python3
"""Pre-delivery machine checks, spec v20 section 10.2. Every item must be 0.

    python3 check.py --tex     items 1-6, 12-14   (LaTeX, PDF, source)
    python3 check.py --pptx    items 7-11         (PowerPoint export)
    python3 check.py           everything

Each check is a function returning a list of problem strings, so that
test_checks.py can plant a fault and confirm it is caught (spec 10.3.6).
"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SHEETS = ["classwork", "mock", "hw1", "hw2"]
PAIRS = [(s, f"{s}_answers") for s in SHEETS]
SHEET_PDFS = [f"{a}.pdf" for pair in PAIRS for a in pair]
DECKS = ["slides", "slides_zh"]        # English screen; Chinese screen (same notes)
PRINTED = SHEET_PDFS + [f"{d}_screen.pdf" for d in DECKS]
LOGS = [f"{a}.log" for pair in PAIRS for a in pair] + [f"{d}{x}.log" for d in DECKS for x in ("_screen", "_notes", "")]
TEX = [f"{s}.tex" for s in SHEETS] + ["slides.tex"]
UNITS = ["g/cm", "g/mL", "km/s", "m/s", "cm/s", "J/kg"]
SUPSUB = re.compile("[\u00b2\u00b3\u00b9\u2070-\u209f]")
CJK = re.compile("[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]")
MM = 72 / 25.4
QUESTION_TITLE = re.compile(r"Do Now|Practice|MCQ|Workbook|Spot the error|Classwork|Quick review")
LABEL = re.compile(r"^(Q\d*(\s|$)|\([a-z]\)|\d+\.|Teaching line, not a question slide\.)")
SAYIT = re.compile(r"^[a-z][a-z' -]*[a-z] = ([a-z]+-)*[A-Z]+(-[a-z]+)*$")


def p(name):
    return os.path.join(HERE, name)


def read(name):
    with open(p(name), encoding="utf-8") as fh:
        return fh.read()


def strip_comments(tex):
    return re.sub(r"(?<!\\)%[^\n]*", "", tex)


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


def split_macro(tex, name):
    """Return (tex with \\name{...} bodies removed, list of bodies)."""
    out, bodies, i = [], [], 0
    for m in re.finditer(r"\\" + name + r"\{", tex):
        if m.start() < i:
            continue
        body, end = brace_body(tex, m.end() - 1)
        out.append(tex[i:m.start()])
        bodies.append(body)
        i = end
    out.append(tex[i:])
    return "".join(out), bodies


def split_notes(tex):
    return split_macro(tex, "note")


def screen_of(tex):
    """Text typeset on screen: \\note and \\zh bodies removed."""
    t, _ = split_notes(tex)
    t, _ = split_macro(t, "zh")
    return t


def frames(tex):
    body = tex[tex.index("\\begin{document}"):] if "\\begin{document}" in tex else tex
    return re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", body, re.S)


def frame_title(fr):
    m = re.match(r"\s*(?:\[[^\]]*\])?\s*\{", fr)
    if not m:
        return ""
    t, _ = brace_body(fr, m.end() - 1)
    return t


def note_source_lines(note):
    return [l.strip() for l in re.split(r"\\par\b", note) if l.strip()]


# ------------------------------------------------------------ item 1
def check_logs(logs):
    probs = []
    for name in logs:
        if not os.path.exists(name):
            probs.append(f"{os.path.basename(name)}: missing log")
            continue
        txt = open(name, encoding="utf-8", errors="replace").read()
        for pat, what in ((r"Overfull \\hbox", "Overfull \\hbox"), (r"Overfull \\vbox", "Overfull \\vbox"),
                          (r"(?m)^! ", "error")):
            n = len(re.findall(pat, txt))
            if n:
                probs.append(f"{os.path.basename(name)}: {n} {what}")
    return probs


def words(pdf):
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    pages, sizes = [], []
    for pg in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', out, re.S):
        sizes.append((float(pg.group(1)), float(pg.group(2))))
        ws = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in re.findall(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', pg.group(3))]
        pages.append(ws)
    return pages, sizes


# ------------------------------------------------------------ item 1b
def check_footer_clear(pdf):
    """Footer found by its own words (the signature), never by position.
    Everything within 4 pt of the footer's top is footer."""
    probs = []
    pages, sizes = words(pdf)
    for k, (ws, (w, h)) in enumerate(zip(pages, sizes), 1):
        sig = [x for x in ws if x[4] == "Ryan"]
        if not sig:
            probs.append(f"slide {k}: no signature")
            continue
        top = min(x[1] for x in sig)
        for x in ws:
            if x[1] >= top - 4:
                continue
            if x[3] > top - 2:
                probs.append(f"slide {k}: '{x[4]}' ends {top - x[3]:.1f} pt above the footer")
        for x in ws:
            if x[0] < MM or x[2] > w - MM:
                probs.append(f"slide {k}: '{x[4]}' within 1 mm of a side edge")
    return probs


# ------------------------------------------------------------ item 1c
def check_notes_inside(pdf):
    probs = []
    pages, sizes = words(pdf)
    for k, (ws, (w, h)) in enumerate(zip(pages, sizes), 1):
        for x in ws:
            if x[0] < MM or x[1] < MM or x[2] > w - MM or x[3] > h - MM:
                probs.append(f"note page {k}: '{x[4]}' within 1 mm of the edge")
    return probs


# ------------------------------------------------------------ item 1d
GLYPH_OPS = {"Tj", "TJ", "'", '"'}


def strip_glyphs_and_images(src, dst):
    """Drop only glyph-showing operators and image Dos. BT/ET and the colour
    operators TeX sets inside them stay, so later fills keep their colour."""
    import pikepdf

    def clean(ops, resources, seen):
        new = []
        for operands, op in ops:
            o = str(op)
            if o in GLYPH_OPS:
                continue
            if o == "Do":
                name = operands[0]
                xo = resources.get("/XObject", {}).get(name) if resources is not None else None
                if xo is not None and xo.get("/Subtype") == "/Image":
                    continue
                if xo is not None and xo.get("/Subtype") == "/Form" and xo.objgen not in seen:
                    seen.add(xo.objgen)
                    sub = pikepdf.parse_content_stream(xo)
                    xo.write(pikepdf.unparse_content_stream(clean(sub, xo.get("/Resources"), seen)))
            new.append((operands, op))
        return new

    with pikepdf.open(src) as pdf:
        for page in pdf.pages:
            ops = pikepdf.parse_content_stream(page)
            page.Contents = pdf.make_stream(pikepdf.unparse_content_stream(clean(ops, page.Resources, set())))
        pdf.save(dst)


def check_dark_fills(pdf, whitelist=()):
    import cv2
    import numpy as np
    import pymupdf
    probs = []
    with tempfile.TemporaryDirectory() as td:
        stripped = os.path.join(td, "s.pdf")
        strip_glyphs_and_images(pdf, stripped)
        doc = pymupdf.open(stripped)
        for k, page in enumerate(doc, 1):
            if k in whitelist:
                continue
            pix = page.get_pixmap(dpi=72, colorspace=pymupdf.csGRAY, alpha=False)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
            dark = (img < 128).astype(np.uint8)
            dark = cv2.erode(dark, np.ones((3, 3), np.uint8))
            n, _, stats, _ = cv2.connectedComponentsWithStats(dark, connectivity=8)
            for j in range(1, n):
                if stats[j, cv2.CC_STAT_AREA] >= 200:
                    probs.append(f"{os.path.basename(pdf)} p.{k}: dark area {stats[j, cv2.CC_STAT_AREA]} pt2")
    return probs


# ------------------------------------------------------------ item 2
def check_fonts(pdfs, logs):
    probs = []
    for pdf in pdfs:
        out = subprocess.run(["pdffonts", pdf], capture_output=True, text=True, check=True).stdout
        for line in out.splitlines()[2:]:
            f = line.split()
            if len(f) >= 6 and f[-5] != "yes":
                probs.append(f"{os.path.basename(pdf)}: font not embedded: {f[0]}")
    for name in logs:
        if os.path.exists(name):
            txt = open(name, encoding="utf-8", errors="replace").read()
            for pat in (r"Missing character[^\n]*", r"Font shape `[^']*' undefined", r"font [^\n]* not found",
                        r"OMS/cmsy [^\n]* not available"):
                for m in re.findall(pat, txt):
                    probs.append(f"{os.path.basename(name)}: {m}")
    return probs


# ------------------------------------------------------------ item 3
def check_no_answers(slides_tex):
    """Reveal headers, and numerals after the last mark allocation on a line.
    Looks for both \\mk{ and \\smk{ (\\mk{ is not a substring of \\smk{)."""
    probs = []
    screen = screen_of(strip_comments(slides_tex))
    screen, _ = split_macro(screen, "flawed")
    for m in re.finditer(r"Answer:|Answer image:|Key answer:", screen):
        probs.append(f"reveal header on screen: {m.group(0)}")
    for line in screen.splitlines():
        allocs = list(re.finditer(r"\\s?mk\{\d+\}", line))
        if allocs:
            rest = line[allocs[-1].end():]
            rest = re.sub(r"\\[A-Za-z]+(\[[^\]]*\])?(\{[^}]*\})?", "", rest)
            if re.search(r"\d", rest):
                probs.append(f"numeral after a mark allocation: {line.strip()[:60]}")
    return probs


# ------------------------------------------------------------ item 4
def maths_segments(tex):
    tex = re.sub(r"\\(includegraphics|input|externaldocument)(\[[^\]]*\])?\{[^}]*\}", "", tex)
    segs = re.findall(r"(?<!\\)\$([^$]+)\$", tex)
    segs += re.findall(r"\\\[(.*?)\\\]", tex, re.S)
    return segs


def unit_free(s):
    for u in UNITS:
        s = s.replace(u, "UNIT")
    return s


def check_fractions(texts):
    probs = []
    for name, tex in texts.items():
        tex = strip_comments(tex)
        tex, _ = split_macro(tex, "flawed")
        tex = re.sub(r"\\\\\[[^\]]*\]", "", tex)          # \\[2mm] is spacing, not display maths
        for seg in maths_segments(tex):
            s = unit_free(seg)
            if re.search(r"[\w)}\]]\s*/\s*[\w({\\]", s):
                probs.append(f"{name}: slash fraction in maths: ${seg}$")
        prose = re.sub(r"(?<!\\)\$[^$]+\$", "", tex)
        if SUPSUB.search(prose):
            probs.append(f"{name}: Unicode super/subscript in text")
        # a stacked fraction or superscript on a 9 mm \alines answer line
        for body in split_macro(tex, "alines")[1]:
            pass
        for m in re.finditer(r"\\alines\{\d+\}\{", tex):
            body, _ = brace_body(tex, m.end() - 1)
            if re.search(r"\\dfrac|\\frac|\^\{", body):
                probs.append(f"{name}: fraction or superscript on a 9 mm line (use \\flines)")
        _, notes = split_notes(tex)
        for n in notes:
            np_ = re.sub(r"(?<!\\)\$[^$]+\$", "", n)
            if "^" in np_:
                probs.append(f"{name}: ^ in note prose")
            for m in re.finditer(r"\S/\S", unit_free(np_)):
                probs.append(f"{name}: unspaced slash in note prose: {m.group(0)}")
    return probs


# ------------------------------------------------------------ item 5
BANNED = r"\\(fontsize|small|footnotesize|scriptsize|tiny|resizebox|scalebox|pause|only|uncover|visible|invisible|onslide|alt)\b"


def check_banned(slides_tex):
    probs = []
    tex = strip_comments(slides_tex)
    screen, notes = split_notes(tex)
    body = screen[screen.index("\\begin{document}"):] if "\\begin{document}" in screen else screen
    for m in re.finditer(BANNED, body):
        probs.append(f"banned command {m.group(0)}")
    for pat in (r"\[shrink", r"allowframebreaks", r"font\s*=", r"\\\w+<\d"):
        for m in re.finditer(pat, body):
            probs.append(f"banned {m.group(0)}")
    for n in notes:
        if "\\includegraphics" in n:
            probs.append("\\includegraphics inside \\note")
    return probs


# ------------------------------------------------------------ item 5b
def check_frames(slides_tex):
    probs = []
    tex = strip_comments(slides_tex)
    for fr in frames(tex):
        m = re.match(r"\s*(?:\[[^\]]*\])?\s*(\{)?", fr)
        rest = fr
        if m.group(1):
            _, end = brace_body(fr, m.end() - 1)
            rest = fr[end:]
            if rest.lstrip().startswith("{"):
                probs.append(f"frame '{frame_title(fr)}': brace group after the title (becomes the subtitle)")
        if not rest.lstrip().startswith("\\relax"):
            probs.append(f"frame '{frame_title(fr)}': body does not start with \\relax")
        n = len(re.findall(r"\\note\{", fr))
        if n != 1:
            probs.append(f"frame '{frame_title(fr)}': {n} \\note")
    return probs


# ------------------------------------------------------------ item 6
def check_plots(files):
    uses = any(re.search(r"^\s*(import|from)\s+matplotlib", open(f).read(), re.M) for f in files)
    return [] if not uses else ["matplotlib used: add the extent assertion before saving"]


# ------------------------------------------------------------ items 7-11
PNS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def pptx_parts(pptx):
    from lxml import etree
    z = zipfile.ZipFile(pptx)
    pres = etree.fromstring(z.read("ppt/presentation.xml"))
    sz = pres.find("p:sldSz", PNS)
    ids = [s.get(f"{{{PNS['r']}}}id") for s in pres.find("p:sldIdLst", PNS)]
    rels = etree.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    slides = []
    for rid in ids:
        path = "ppt/" + target[rid].lstrip("/").replace("ppt/", "")
        sx = etree.fromstring(z.read(path))
        srels = etree.fromstring(z.read(path.replace("slides/", "slides/_rels/") + ".rels"))
        notes = None
        media = []
        for r in srels:
            t = r.get("Target")
            if "notesSlide" in r.get("Type"):
                notes = etree.fromstring(z.read("ppt/notesSlides/" + os.path.basename(t)))
            if "image" in r.get("Type"):
                media.append(z.read("ppt/media/" + os.path.basename(t)))
        slides.append((sx, notes, media))
    return (int(sz.get("cx")), int(sz.get("cy"))), slides


def check_alignment(slides_tex, pdf, pptx):
    import pymupdf
    probs = []
    nf = len(frames(strip_comments(slides_tex)))
    doc = pymupdf.open(pdf)
    _, slides = pptx_parts(pptx)
    if not (nf == doc.page_count == len(slides)):
        probs.append(f"frames {nf}, PDF pages {doc.page_count}, PPTX slides {len(slides)}")
    for k, page in enumerate(doc, 1):
        if abs(page.rect.width - page.rect.height * 32 / 9) > 0.5:
            probs.append(f"joined page {k}: width {page.rect.width:.1f} != height x 32/9")
    return probs


def check_pure_images(pptx):
    import struct
    probs = []
    (cx, cy), slides = pptx_parts(pptx)
    for k, (sx, _, media) in enumerate(slides, 1):
        tree = sx.find(".//p:spTree", PNS)
        shapes = [c for c in tree if c.tag.split("}")[1] not in ("nvGrpSpPr", "grpSpPr")]
        pics = [c for c in shapes if c.tag == f"{{{PNS['p']}}}pic"]
        if len(shapes) != 1 or len(pics) != 1:
            probs.append(f"slide {k}: {len(shapes)} shapes, {len(pics)} pictures")
            continue
        off = pics[0].find(".//a:off", PNS)
        ext = pics[0].find(".//a:ext", PNS)
        if (int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy"))) != (0, 0, cx, cy):
            probs.append(f"slide {k}: picture is not full bleed")
        png = media[0] if media else b""
        if png[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", png[16:24]) != (3840, 2160):
            probs.append(f"slide {k}: image is not a 3840x2160 PNG")
    return probs


def check_no_note_images(pptx):
    probs = []
    z = zipfile.ZipFile(pptx)
    for n in z.namelist():
        if n.startswith("ppt/notesSlides/notesSlide") and n.endswith(".xml"):
            x = z.read(n).decode("utf-8")
            if "<p:pic" in x or "a:blip" in x:
                probs.append(f"{n}: image in notes")
    return probs


def note_lines(notes):
    lines = []
    if notes is None:
        return lines
    for sp in notes.findall(".//p:sp", PNS):
        ph = sp.find(".//p:ph", PNS)
        if ph is None or ph.get("type") != "body":
            continue
        for para in sp.findall(".//a:p", PNS):
            txt = ""
            for el in para:
                tag = el.tag.split("}")[1]
                if tag == "r":
                    txt += "".join(t.text or "" for t in el.findall("a:t", PNS))
                elif tag == "AlternateContent":
                    txt += "".join(t.text or "" for t in el.findall(".//m:t", PNS))
            if txt.strip():
                lines.append(txt.strip())
    return lines


def notes_structure(title, lines, where):
    """Spec 5.6 / 10.2 item 10 on one slide's note lines."""
    probs = []
    labels = ("Short solution:", "Watch for:", "Diagnostic:", "Script:", "Say it:")
    for lab in labels:
        if lines.count(lab) > 1:
            probs.append(f"{where}: repeated {lab}")
    for bad in ("Answer:", "Answer image:", "Key answer:"):
        if any(l.startswith(bad) for l in lines):
            probs.append(f"{where}: {bad} header")
    if "Watch for:" in lines and ("Short solution:" not in lines or
                                 lines.index("Short solution:") > lines.index("Watch for:")):
        probs.append(f"{where}: Watch for: without a preceding Short solution:")
    order = [l for l in lines if l in labels]
    if order != sorted(order, key=labels.index):
        probs.append(f"{where}: labels out of order: {order}")
    if "Say it:" in lines:
        k = lines.index("Say it:")
        if any(l in labels for l in lines[k + 1:]):
            probs.append(f"{where}: Say it: is not the last label")
        for l in lines[k + 1:]:
            if not SAYIT.match(l) or not l.isascii():
                probs.append(f"{where}: bad Say it line {l!r}")
    if any("\\" in l for l in lines):
        probs.append(f"{where}: a LaTeX macro survives in the notes")
    if any(re.search("[\u3010\u3011\uff08\uff09]", l) for l in lines):
        probs.append(f"{where}: full-width bracket in the notes (use ASCII parentheses)")
    q = QUESTION_TITLE.search(title)
    if q:
        if not lines:
            probs.append(f"{where}: no notes")
            return probs
        if not LABEL.match(lines[0]):
            probs.append(f"{where}: first note line does not start with a label")
        if "Do Now" in title and "Diagnostic:" not in lines:
            probs.append(f"{where}: Do Now without Diagnostic:")
        # English screen + Chinese notes: answer lines are English
        if not lines[0].startswith("Teaching line"):
            ends = [lines.index(l) for l in labels if l in lines]
            end = min(ends) if ends else len(lines)
            for l in lines[:end]:
                if CJK.search(l):
                    probs.append(f"{where}: Chinese in an answer line: {l[:30]!r}")
    return probs


def check_notes_structure_src(slides_tex, chinese_screen=False):
    """Item 10 on the source: notes as written, plus no CJK on screen
    (the Chinese-screen deck is exempt from the screen rule)."""
    probs = []
    tex = strip_comments(slides_tex)
    for k, fr in enumerate(frames(tex), 1):
        title = frame_title(fr)
        _, notes = split_notes(fr)
        screen = screen_of(fr)
        if CJK.search(screen) and not chinese_screen:
            probs.append(f"slide {k} '{title}': Chinese outside \\note")
        lines = [re.sub(r"\\Lref\{[^}]*\}", "Lx", l) for l in note_source_lines(notes[0] if notes else "")]
        lines = [re.sub(r"\$[^$]*\$", "x", l) for l in lines]
        lines = [re.sub(r"\\(textdegree|textperiodcentered|_|,|%|&)(\{\})?", "", l) for l in lines]
        probs += notes_structure(title, lines, f"slide {k} '{title}'")
    return probs


def check_notes_structure(slides_tex, pptx):
    probs = []
    titles = [frame_title(f) for f in frames(strip_comments(slides_tex))]
    _, slides = pptx_parts(pptx)
    for k, (title, (_, notes, _)) in enumerate(zip(titles, slides), 1):
        probs += notes_structure(title, note_lines(notes), f"slide {k} '{title}'")
    return probs


def check_notes_maths(slides_tex, pptx):
    probs = []
    _, notes_src = split_notes(strip_comments(slides_tex))
    _, slides = pptx_parts(pptx)
    for k, (src, (_, notes, _)) in enumerate(zip(notes_src, slides), 1):
        n_src = len(re.findall(r"(?<!\\)\$[^$]+\$", src))
        acs = notes.findall(".//mc:AlternateContent", PNS) if notes is not None else []
        good = [a for a in acs if a.find("mc:Choice/a14:m/m:oMath", PNS) is not None
                and a.find("mc:Fallback", PNS) is not None]
        if len(good) != n_src or len(acs) != n_src:
            probs.append(f"slide {k}: {n_src} source equations, {len(good)} native with fallback")
        for a in good:
            om = a.find("mc:Choice/a14:m/m:oMath", PNS)
            for f in om.iter(f"{{{PNS['m']}}}fPr"):
                t = f.find("m:type", PNS)
                if t is not None and t.get(f"{{{PNS['m']}}}val") in ("lin", "skw"):
                    probs.append(f"slide {k}: linear or skewed fraction")
            joined = unit_free("".join(t.text or "" for t in om.iter(f"{{{PNS['m']}}}t")))
            if "/" in joined or "^" in joined or SUPSUB.search(joined):
                probs.append(f"slide {k}: equation text '{joined}' has / ^ or Unicode scripts")
        if notes is not None:
            for para in notes.findall(".//a:p", PNS):
                for r in para.findall("a:r", PNS):
                    t = "".join(x.text or "" for x in r.findall("a:t", PNS))
                    tu = unit_free(t)
                    if "^" in tu or SUPSUB.search(tu):
                        probs.append(f"slide {k}: ^ or Unicode script in note prose: {t!r}")
                    if re.search(r"\S/\S", re.sub(r"\S+\.pdf", "", tu)):
                        probs.append(f"slide {k}: unspaced slash in note prose: {t!r}")
    return probs


# ------------------------------------------------------------ item 12
def check_spot_error(slides_tex, sheet_texts):
    probs = []
    tex = strip_comments(slides_tex)
    for k, fr in enumerate(frames(tex), 1):
        title = frame_title(fr)
        screen, notes = split_notes(fr)
        has_flawed = "\\flawed{" in screen
        if "Spot the error" in title:
            m = re.search(r"has (\d+) errors", screen)
            if not m:
                probs.append(f"slide {k}: no 'has N errors' on screen")
                continue
            if not has_flawed:
                probs.append(f"slide {k}: Spot the error without \\flawed")
            n = int(m.group(1))
            lines = note_source_lines(notes[0])
            nums = [l for l in lines if re.match(r"\d+\.", l)]
            want = [f"{i}." for i in range(1, n + 1)]
            if [l.split()[0] for l in nums] != want:
                probs.append(f"slide {k}: note numbers {[l.split()[0] for l in nums]} != {want}")
            for l in nums:
                if not re.search(r"\\Lref\{|\bL\d+\b", l):
                    probs.append(f"slide {k}: error line without an L-reference: {l[:30]}")
        elif has_flawed:
            probs.append(f"slide {k} '{title}': \\flawed outside a Spot the error frame")
    for name, t in sheet_texts.items():
        t = strip_comments(t)
        for m in re.finditer(r"\\flawed\{", t):
            _, end = brace_body(t, m.end() - 1)
            after = t[end:end + 600]
            nm = re.search(r"\\textbf\{[^}]*?(\d+) errors", after)
            if not nm:
                probs.append(f"{name}: \\flawed not followed by a bold 'N errors'")
                continue
            n = int(nm.group(1))
            am = re.search(r"\\alines\{\d+\}\{", after)
            if not am:
                probs.append(f"{name}: no answer block after a \\flawed item")
                continue
            body, _ = brace_body(after, am.end() - 1)
            nums = re.findall(r"(?:^|\s)(\d+)\.\s", " " + body)
            if nums != [str(i) for i in range(1, n + 1)]:
                probs.append(f"{name}: answer numbering {nums} for {n} errors")
            if len(re.findall(r"\\Lref\{", body)) < n:
                probs.append(f"{name}: fewer than {n} \\Lref in the answer block")
    return probs


# ------------------------------------------------------------ item 13
def figure_text():
    """Words that figure macros print, from their definitions in shared.sty."""
    sty = strip_comments(read("shared.sty"))
    out = {}
    for m in re.finditer(r"\\newcommand\\(Fig\w+)(\[\d\])?(\[[^\]]*\])?\{", sty):
        body, _ = brace_body(sty, m.end() - 1)
        out[m.group(1)] = body
    return out


def visible(text):
    text = re.sub(r"\\[A-Za-z@]+", " ", text)
    return text.lower()


def stem(word):
    w = word.lower().split()[0]
    return w[:max(5, len(w) - 2)]


def check_sayit(slides_tex):
    probs = []
    tex = strip_comments(slides_tex)
    figs = figure_text()
    seen = {}
    texts = []
    for k, fr in enumerate(frames(tex), 1):
        _, notes = split_notes(fr)
        screen = screen_of(fr)
        extra = " ".join(figs[f] for f in re.findall(r"\\(Fig\w+)", screen) if f in figs)
        lines = note_source_lines(notes[0] if notes else "")
        words_here = []
        if "Say it:" in lines:
            words_here = [l.split(" = ")[0] for l in lines[lines.index("Say it:") + 1:]]
            body = "\n".join(lines[:lines.index("Say it:")])
        else:
            body = "\n".join(lines)
        texts.append(visible(screen + " " + extra + " " + body))
        for w in words_here:
            s = stem(w)
            if s in seen:
                probs.append(f"'{w}' pronounced on slide {seen[s]} and again on slide {k}")
                continue
            seen[s] = k
            for j, t in enumerate(texts[:-1], 1):
                if re.search(r"\b" + re.escape(s), t):
                    probs.append(f"'{w}' is first said on slide {j}, but pronounced on slide {k}")
                    break
    return probs


# ------------------------------------------------------------ item 14
def check_layout_pairs(pairs):
    """Every left-margin word of the blank version is on the same page of the
    answer version at the same height (0.5 pt). Dot leaders are excluded."""
    probs = []
    for blank, answers in pairs:
        pb, _ = words(p(blank + ".pdf"))
        pa, _ = words(p(answers + ".pdf"))
        if len(pb) != len(pa):
            probs.append(f"{blank}: {len(pb)} pages, answers {len(pa)}")
            continue
        for k, (wb, wa) in enumerate(zip(pb, pa), 1):
            real = [x for x in wb if not re.fullmatch(r"[.\u2026]+", x[4])]
            if not real:
                continue
            left = min(x[0] for x in real)
            for x in real:
                if x[0] > left + 2:
                    continue
                hit = [y for y in wa if y[4] == x[4] and abs(y[0] - x[0]) < 1 and abs(y[1] - x[1]) <= 0.5]
                if not hit:
                    probs.append(f"{blank} p.{k}: '{x[4]}' at y={x[1]:.1f} not matched in the answer version")
    return probs


# ------------------------------------------------------------ pairing
def check_deck_pair(en_tex, zh_tex):
    """The Chinese deck has the same frames, in order, with the same notes."""
    en = frames(strip_comments(en_tex))
    zh = frames(strip_comments(zh_tex))
    if len(en) != len(zh):
        return [f"English deck {len(en)} frames, Chinese deck {len(zh)}"]
    probs = []
    for k, (a, b) in enumerate(zip(en, zh), 1):
        if split_notes(a)[1] != split_notes(b)[1]:
            probs.append(f"slide {k}: notes differ between the decks")
    return probs


# ------------------------------------------------------------ runner
def run_tex():
    texts = {n: read(n) for n in TEX}
    sheet_texts = {n: read(n) for n in TEX if n != "slides.tex"}
    res = [
        ("1", "Clean compile", check_logs([p(l) for l in LOGS])),
        ("1d", "No solid dark fills", sum((check_dark_fills(p(f)) for f in PRINTED), [])),
        ("2", "Fonts embedded", check_fonts([p(f) for f in PRINTED] +
                                            [p(f"{d}{x}.pdf") for d in DECKS for x in ("_notes", "")],
                                            [p(l) for l in LOGS])),
        ("4", "No slash fractions or fake superscripts", check_fractions(texts)),
        ("6", "Plots stay on canvas (n/a: all figures are TikZ or crops)",
         check_plots([p(f) for f in os.listdir(HERE) if f.endswith(".py") and f != "check.py"])),
        ("12", "Spot the error integrity", check_spot_error(read("slides.tex"), sheet_texts)),
        ("14", "Blank and answer layouts match", check_layout_pairs(PAIRS)),
        ("7z", "Chinese deck: same frames and notes as English", check_deck_pair(read("slides.tex"), read("slides_zh.tex"))),
    ]
    for d in DECKS:
        t = read(f"{d}.tex")
        tag = "" if d == "slides" else " [zh]"
        res += [
            ("1b", "Screen text clears the footer" + tag, check_footer_clear(p(f"{d}_screen.pdf"))),
            ("1c", "Note pages do not overflow" + tag, check_notes_inside(p(f"{d}_notes.pdf"))),
            ("3", "No answers on screen" + tag, check_no_answers(t)),
            ("5", "No banned commands" + tag, check_banned(t)),
            ("5b", "Frame bodies not swallowed" + tag, check_frames(t)),
            ("10s", "Notes structure (source)" + tag, check_notes_structure_src(t, chinese_screen=d != "slides")),
            ("13", "Say it: once, where first said" + tag, check_sayit(t)),
        ]
    return res


def run_pptx():
    res = []
    for d in DECKS:
        t = read(f"{d}.tex")
        x = p(f"{d}.pptx")
        tag = "" if d == "slides" else " [zh]"
        res += [
            ("7", "Page alignment" + tag, check_alignment(t, p(f"{d}.pdf"), x)),
            ("8", "Slides are pure images" + tag, check_pure_images(x)),
            ("9", "No images in notes" + tag, check_no_note_images(x)),
            ("10", "Notes structure" + tag, check_notes_structure(t, x)),
            ("11", "Notes maths truly typeset" + tag, check_notes_maths(t, x)),
        ]
    return res


def main():
    args = sys.argv[1:]
    results = []
    if not args or "--tex" in args:
        results += run_tex()
    if not args or "--pptx" in args:
        results += run_pptx()
    bad = 0
    for item, name, probs in results:
        print(f"{item:>3}  {name:<55} {len(probs)}")
        for pr in probs[:15]:
            print(f"       - {pr}")
        bad += len(probs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
