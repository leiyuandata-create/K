#!/usr/bin/env python3
"""Pre-delivery machine checks, spec v20 section 10.2. Every item must be 0.

    python3 check.py N --tex     items 1-6 and 12-16 (LaTeX, PDF, source)
    python3 check.py N --pptx    items 7-11          (PowerPoint export)
    python3 check.py N           everything

Each check is a function over explicit paths returning a list of problem
strings, so test_checks.py can plant a fault and confirm it is caught.
"""
import html
import os
import re
import unicodedata
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
UNITS = ["km/s", "m/s", "cm/s", "J/kg"]
SUPSUB = re.compile("[\u00b2\u00b3\u00b9\u2070-\u209f]")
CJK = re.compile("[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef\u3010\u3011]")
MM = 72 / 25.4
QWORDS = r"Do Now|Practice|MCQ|Workbook|Spot the error|Classwork|Quick review"
LABELS = ["Short solution:", "Watch for:", "Diagnostic:", "Ask:", "Say it:"]
FIRST = re.compile(r"^(\([a-z]\)|\((i|ii|iii|iv|v)\)|Q\d*\b|Q\d+\s*\([a-z]\)|\d+\.|Gap\b|Teaching line)")
SAYIT = re.compile(r"^([A-Za-z][A-Za-z' -]*?) = ([a-z]+-)*[A-Z]+(-[a-z]+)*$")
# whitelist for check 1d: {(pdf basename, page): reason}
DARK_WHITELIST = {}


def p(name):
    return os.path.join(HERE, name)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def strip_comments(tex):
    return re.sub(r"(?<!\\)%[^\n]*", "", tex)


def brace_body(tex, start):
    """tex[start] == '{'; return (body, index after the closing brace)."""
    depth = 0
    i = start
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


def cut_macro(tex, name):
    """Return (tex with every \\name{...} removed, list of bodies)."""
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
    return cut_macro(tex, "note")


def doc_body(tex):
    return tex[tex.index("\\begin{document}"):] if "\\begin{document}" in tex else tex


def frames(tex):
    return re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", doc_body(tex), re.S)


def frame_title(fr):
    m = re.match(r"\s*(?:\[[^\]]*\])?\s*\{", fr)
    if not m:
        return ""
    t, _ = brace_body(fr, m.end() - 1)
    return t


def note_of(fr):
    _, notes = split_notes(fr)
    return notes[0] if notes else None


def note_lines_src(note):
    return [l.strip() for l in re.split(r"\\par\b", strip_comments(note)) if l.strip()]


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
    """pdftotext -bbox: per page a list of (xmin, ymin, xmax, ymax, text), and page sizes."""
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    pages, sizes = [], []
    for pg in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', out, re.S):
        sizes.append((float(pg.group(1)), float(pg.group(2))))
        ws = [(float(a), float(b), float(c), float(d), unicodedata.normalize("NFKC", html.unescape(t)))
              for a, b, c, d, t in re.findall(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', pg.group(3))]
        pages.append(ws)
    return pages, sizes


def footer_top(ws):
    """The footer is found by its own words (the signature), never by position."""
    sig = [x for x in ws if x[4] == "Ryan"]
    if not sig:
        return None
    sig_top = min(x[1] for x in sig)
    return min(x[1] for x in ws if x[1] >= sig_top - 4)


# ------------------------------------------------------------ item 1b
def check_footer_clear(pdf):
    import pymupdf
    probs = []
    pages, sizes = words(pdf)
    doc = pymupdf.open(pdf)
    for k, (ws, (w, h)) in enumerate(zip(pages, sizes), 1):
        top = footer_top(ws)
        if top is None:
            probs.append(f"slide {k}: no signature")
            continue
        for x in ws:
            if x[1] >= top:
                continue
            if x[3] > top - 2:
                probs.append(f"slide {k}: '{x[4]}' ends {top - x[3]:.1f} pt above the footer")
        for x in ws:
            if x[0] < MM or x[2] > w - MM:
                probs.append(f"slide {k}: '{x[4]}' within 1 mm of a side edge")
        for info in doc[k - 1].get_image_info():
            x0, y0, x1, y1 = info["bbox"]
            if y1 > top - 2:
                probs.append(f"slide {k}: picture ends {top - y1:.1f} pt above the footer")
            if x0 < MM - 0.01 or x1 > w - MM + 0.01:
                probs.append(f"slide {k}: picture within 1 mm of a side edge")
    return probs


# ------------------------------------------------------------ item 1c
def check_notes_inside(pdf):
    probs = []
    pages, sizes = words(pdf)
    for k, (ws, (w, h)) in enumerate(zip(pages, sizes), 1):
        for x in ws:
            if x[0] < MM or x[1] < MM or x[2] > w - MM or x[3] > h - MM:
                probs.append(f"note page {k}: '{x[4]}' within 1 mm of the edge")
        # by position, not stream order: the header's n / N is extracted after the note
        last = [x[4] for x in sorted(ws, key=lambda x: (round(x[3], 1), x[0]))[-3:]]
        if last != ["end", "of", "notes"]:
            probs.append(f"note page {k}: sentinel 'end of notes' missing (note ran off the page)")
    return probs


# ------------------------------------------------------------ item 1d
GLYPH_OPS = {"Tj", "TJ", "'", '"'}


def strip_glyphs_and_images(src, dst):
    """Drop only glyph-showing operators and image Dos, keeping colour operators."""
    import pikepdf

    def clean(obj, resources, seen):
        ops = pikepdf.parse_content_stream(obj)
        new = []
        for operands, op in ops:
            o = str(op)
            if o in GLYPH_OPS:
                continue
            if o == "Do" and resources is not None:
                xo = resources.get("/XObject", {}).get(operands[0])
                if xo is not None and xo.get("/Subtype") == "/Image":
                    continue
                if xo is not None and xo.get("/Subtype") == "/Form" and xo.objgen not in seen:
                    seen.add(xo.objgen)
                    xo.write(clean(xo, xo.get("/Resources", resources), seen))
            new.append((operands, op))
        return pikepdf.unparse_content_stream(new)

    with pikepdf.open(src) as pdf:
        seen = set()
        for page in pdf.pages:
            data = clean(page, page.Resources, seen)
            page.Contents = pdf.make_stream(data)
        pdf.save(dst)


def check_dark_fills(pdf, whitelist=None):
    import cv2
    import numpy as np
    import pymupdf
    whitelist = DARK_WHITELIST if whitelist is None else whitelist
    probs = []
    with tempfile.TemporaryDirectory() as td:
        stripped = os.path.join(td, "s.pdf")
        strip_glyphs_and_images(pdf, stripped)
        doc = pymupdf.open(stripped)
        for k, page in enumerate(doc, 1):
            if (os.path.basename(pdf), k) in whitelist:
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
            if len(f) >= 7 and f[-5] != "yes":
                probs.append(f"{os.path.basename(pdf)}: font not embedded: {f[0]}")
    for name in logs:
        if os.path.exists(name):
            txt = open(name, encoding="utf-8", errors="replace").read()
            for pat in (r"Missing character[^\n]*", r"Font shape `[^']*' undefined", r"Package fontspec Error[^\n]*",
                        r"OMS/cmsy[^\n]* not available", r"The font \"[^\"]*\" cannot be found"):
                for m in re.findall(pat, txt):
                    probs.append(f"{os.path.basename(name)}: {m}")
    return probs


# ------------------------------------------------------------ item 3
def check_no_answers(slides_tex):
    probs = []
    screen, _ = split_notes(strip_comments(slides_tex))
    screen, _ = cut_macro(screen, "flawed")
    for m in re.finditer(r"Answer:|Answer image:|Key answer:", screen):
        probs.append(f"reveal header on screen: {m.group(0)}")
    for line in screen.splitlines():
        last = None
        for m in re.finditer(r"\\s?mk\{[^}]*\}", line):
            last = m
        if last is None:
            continue
        rest = line[last.end():]
        rest = re.sub(r"\\[A-Za-z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", rest)   # commands and their args
        rest = re.sub(r"\d+(\.\d+)?\s*(pt|mm|cm|em|ex)", " ", rest)            # dimensions
        if re.search(r"\d", rest):
            probs.append(f"numeral after a mark allocation: {line.strip()[:70]}")
    return probs


# ------------------------------------------------------------ item 4
def maths_segments(tex):
    tex = re.sub(r"\\(includegraphics|input|externaldocument|labfig)(\[[^\]]*\])?\{[^}]*\}", "", tex)
    segs = re.findall(r"(?<!\\)\$([^$]+)\$", tex)
    segs += re.findall(r"\\\[(.*?)\\\]", tex, re.S)
    for mac in ("fbx", "wline", "af"):
        _, bodies = cut_macro(tex, mac)
        segs += bodies
    return segs


def unit_free(s):
    for u in UNITS:
        s = s.replace(u, "UNIT")
    return s


def check_fractions(texts):
    probs = []
    for name, tex in texts.items():
        tex = strip_comments(tex)
        tex, _ = cut_macro(tex, "flawed")
        tex = re.sub(r"\\\\\[[^\]]*\]", "", tex)          # \\[2mm] is spacing, not display maths
        for seg in maths_segments(tex):
            s = unit_free(seg)
            if re.search(r"[\w)}\]]\s*/\s*[\w({\\]", s):
                probs.append(f"{name}: slash fraction in maths: {seg.strip()[:50]}")
        prose = re.sub(r"(?<!\\)\$[^$]+\$", "", tex)
        if SUPSUB.search(prose):
            probs.append(f"{name}: Unicode super/subscript in text")
        _, als = cut_macro(tex, "al")
        for a in als:
            if re.search(r"\\[dt]?frac\b", a):
                probs.append(f"{name}: stacked fraction on a 9 mm \\al line (needs \\af): {a[:40]}")
        _, notes = split_notes(tex)
        for n in notes:
            np_ = re.sub(r"(?<!\\)\$[^$]+\$", "", n)
            if "^" in np_:
                probs.append(f"{name}: ^ in note prose")
            if SUPSUB.search(np_):
                probs.append(f"{name}: Unicode super/subscript in note prose")
            for m in re.finditer(r"[^\s/]/[^\s/]", unit_free(np_)):
                probs.append(f"{name}: unspaced slash in note prose: {m.group(0)}")
    return probs


# ------------------------------------------------------------ item 5
BANNED = (r"\\(fontsize|small|footnotesize|scriptsize|tiny|resizebox|scalebox|pause|only|uncover|"
          r"visible|invisible|onslide|alt)\b")


def check_banned(slides_tex):
    probs = []
    tex = strip_comments(slides_tex)
    screen, notes = split_notes(tex)
    body = doc_body(screen)
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
    uses = any(re.search(r"^\s*(import|from)\s+matplotlib", read(f), re.M) for f in files)
    return [] if not uses else ["matplotlib used: add the extent assertion before saving"]


# ------------------------------------------------------------ item 10 (source half)
def note_structure(title, lines, where):
    probs = []
    q = re.search(QWORDS, title)
    if q and not lines:
        return [f"{where}: no notes"]
    if not lines:
        return probs
    if q and not FIRST.match(lines[0]):
        probs.append(f"{where}: first note line does not start with a label: {lines[0][:40]!r}")
    for bad in ("Answer:", "Answer image:", "Key answer:"):
        if any(l.startswith(bad) for l in lines):
            probs.append(f"{where}: {bad} header")
    pos = []
    for lab in LABELS:
        c = lines.count(lab)
        if c > 1:
            probs.append(f"{where}: repeated {lab}")
        if c:
            pos.append((lines.index(lab), lab))
    if [lab for _, lab in sorted(pos)] != [lab for lab in LABELS if lab in lines]:
        probs.append(f"{where}: labels out of order")
    if "Watch for:" in lines and "Short solution:" not in lines:
        probs.append(f"{where}: Watch for: without Short solution:")
    if "Do Now" in title and "Diagnostic:" not in lines:
        probs.append(f"{where}: Do Now without Diagnostic:")
    if "Say it:" in lines:
        k = lines.index("Say it:")
        if k != max(i for i, _ in pos):
            probs.append(f"{where}: Say it: is not the last label")
        after = lines[k + 1:]
        if not after:
            probs.append(f"{where}: empty Say it:")
        for l in after:
            if not SAYIT.match(l) or not l.isascii():
                probs.append(f"{where}: Say it line not 'word = SYL-la-ble': {l!r}")
    for l in lines:
        if re.search(r"\\[A-Za-z]+", strip_maths(l)):
            probs.append(f"{where}: macro survives in note: {l[:50]!r}")
    return probs


def strip_maths(s):
    return re.sub(r"(?<!\\)\$[^$]+\$", "", s)


def check_notes_source(slides_tex, expand):
    probs = []
    for k, fr in enumerate(frames(strip_comments(slides_tex)), 1):
        title = frame_title(fr)
        note = note_of(fr) or ""
        lines = [expand(l) for l in note_lines_src(note)]
        probs += note_structure(title, lines, f"frame {k} '{title}'")
    return probs


# ------------------------------------------------------------ item 12
def check_spot_error(slides_tex, sheet_texs, shared_sty):
    probs = []
    keys = set(re.findall(r"\\defL\{([^}]*)\}", read(shared_sty)))
    for k, fr in enumerate(frames(strip_comments(slides_tex)), 1):
        title = frame_title(fr)
        screen, notes = split_notes(fr)
        has_flawed = "\\flawed{" in screen
        if "Spot the error" in title:
            m = re.search(r"has (\d+) errors?", screen)
            if not m:
                probs.append(f"frame {k}: Spot the error without 'has N errors' on screen")
                continue
            n = int(m.group(1))
            if not has_flawed:
                probs.append(f"frame {k}: Spot the error without \\flawed{{}}")
            lines = note_lines_src(notes[0]) if notes else []
            nums = [l for l in lines if re.match(r"^\d+\.", l)]
            if [int(re.match(r"(\d+)", l).group(1)) for l in nums] != list(range(1, n + 1)):
                probs.append(f"frame {k}: note numbering does not run 1..{n}")
            for l in nums:
                refs = re.findall(r"\\Lref\{([^}]*)\}", l)
                if not refs:
                    probs.append(f"frame {k}: line '{l[:30]}' has no L-reference")
                for r in refs:
                    if r not in keys:
                        probs.append(f"frame {k}: undefined L key {r}")
        elif has_flawed:
            probs.append(f"frame {k} '{title}': \\flawed{{}} outside a Spot the error frame")
    for name, tex in sheet_texs.items():
        tex = strip_comments(tex)
        if re.match(r"handout", os.path.basename(name)) and "\\flawed{" in tex:
            probs.append(f"{name}: \\flawed{{}} in a handout")
            continue
        for m in re.finditer(r"\\flawed\{", tex):
            after = tex[m.start():m.start() + 4000]
            # the stated count is bold and precedes the card (it is in the stem)
            before = tex[max(0, m.start() - 1500):m.start()]
            c = re.findall(r"\\textbf\{[^}]*?(\d+) errors?[.:]?\}", before)
            if not c:
                probs.append(f"{name}: \\flawed{{}} without a bold 'N errors' before it")
                continue
            n = int(c[-1])
            block = re.search(r"\\begin\{errorlist\}(.*?)\\end\{errorlist\}", after, re.S)
            if not block:
                probs.append(f"{name}: no errorlist answer block after \\flawed{{}}")
                continue
            items = re.findall(r"\\erritem", block.group(1))
            refs = re.findall(r"\\Lref\{([^}]*)\}", block.group(1))
            if len(items) != n or len(refs) < n:
                probs.append(f"{name}: {n} errors stated, {len(items)} answers, {len(refs)} L-references")
            for r in refs:
                if r not in keys:
                    probs.append(f"{name}: undefined L key {r}")
    return probs


# ------------------------------------------------------------ item 13
SUFFIXES = ("isation", "ising", "ised", "ises", "ise", "ions", "ion", "ing", "ed", "es", "s")


def stem(w):
    w = w.lower()
    for s in SUFFIXES:
        if w.endswith(s) and len(w) - len(s) >= 4:
            return w[:-len(s)]
    return w


def plain_words(tex):
    tex = re.sub(r"\\(includegraphics|input|label|ref|pageref|fref|externaldocument)(\[[^\]]*\])?\{[^}]*\}", " ", tex)
    tex = re.sub(r"\\[A-Za-z]+", " ", tex)
    return [w.lower() for w in re.findall(r"[A-Za-z]+", tex)]


def check_say_it(slides_tex, expand):
    probs = []
    seen_in = {}
    texts = []
    for k, fr in enumerate(frames(strip_comments(slides_tex)), 1):
        screen, notes = split_notes(fr)
        lines = [expand(l) for l in note_lines_src(notes[0])] if notes else []
        said = []
        if "Say it:" in lines:
            for l in lines[lines.index("Say it:") + 1:]:
                said.append(l.split("=")[0].strip())
            body = lines[:lines.index("Say it:")]
        else:
            body = lines
        words_here = plain_words(expand(screen)) + plain_words(" ".join(body))
        for w in said:
            st = stem(w)
            if st in seen_in:
                probs.append(f"'{w}' pronounced again on slide {k} (first on slide {seen_in[st]})")
                continue
            seen_in[st] = k
            for j, earlier in enumerate(texts, 1):
                if any(x.startswith(st) for x in earlier):
                    probs.append(f"'{w}' pronounced on slide {k} but already used on slide {j}")
                    break
        texts.append(words_here)
    return probs


# ------------------------------------------------------------ item 14
RED = (200 / 255, 16 / 255, 46 / 255)


def is_red(c):
    if c is None:
        return False
    if isinstance(c, int):
        c = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
    if len(c) != 3:
        return False
    r, g, b = c
    return r > 0.55 and g < 0.35 and b < 0.4


def ms_pages(pdf):
    pages, _ = words(pdf)
    return {k for k, ws in enumerate(pages, 1) if " ".join(x[4] for x in ws).find("Official assessment schedule") >= 0}


def check_layout_pair(blank, answers):
    import pymupdf
    probs = []
    bp, _ = words(blank)
    ap, _ = words(answers)
    drop = ms_pages(answers)
    ap = [ws for k, ws in enumerate(ap, 1) if k not in drop]
    if len(bp) != len(ap):
        probs.append(f"{os.path.basename(blank)}: {len(bp)} pages, answers {len(ap)} (mark-scheme pages dropped)")
        return probs
    for k, (bw, aw) in enumerate(zip(bp, ap), 1):
        if not bw:
            continue
        left = min(x[0] for x in bw)
        margin = [x for x in bw if x[0] < left + 3 and not re.fullmatch(r"[.\u2026]+", x[4])]
        for x in margin:
            if not any(y[4] == x[4] and abs(y[1] - x[1]) <= 0.5 for y in aw):
                probs.append(f"{os.path.basename(blank)} p.{k}: '{x[4]}' at y={x[1]:.1f} moved in the answer version")
    doc = pymupdf.open(blank)
    for k, page in enumerate(doc, 1):
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip() and is_red(s["color"]):
                        probs.append(f"{os.path.basename(blank)} p.{k}: red text '{s['text'][:20]}' on the blank sheet")
        for d in page.get_drawings():
            if is_red(d.get("color")) or is_red(d.get("fill")):
                probs.append(f"{os.path.basename(blank)} p.{k}: red drawing on the blank sheet")
                break
    return probs


# ------------------------------------------------------------ item 15
def check_page_numbers(pdf):
    probs = []
    pages, _ = words(pdf)
    n = len(pages)
    for k, ws in enumerate(pages, 1):
        top = footer_top(ws)
        if top is None:
            probs.append(f"slide {k}: no footer")
            continue
        foot = " ".join(x[4] for x in sorted(ws, key=lambda x: x[0]) if x[1] >= top)
        if not re.search(rf"(^|\s){k}\s*/\s*{n}(\s|$)", foot):
            probs.append(f"slide {k}: footer lacks '{k} / {n}': {foot!r}")
    return probs


# ------------------------------------------------------------ item 16
def check_languages(slides_tex, sheet_texs):
    probs = []
    tex = strip_comments(slides_tex)
    screen, notes = split_notes(tex)
    for m in CJK.finditer(screen):
        probs.append(f"slides: CJK on screen: {screen[max(0, m.start() - 15):m.end() + 5]!r}")
        break
    for name, t in sheet_texs.items():
        if CJK.search(strip_comments(t)):
            probs.append(f"{name}: CJK in a printed sheet")
    for k, n in enumerate(notes, 1):
        lines = note_lines_src(n)
        after = False
        for l in lines:
            if l == "Say it:":
                after = True
            if (l in LABELS or l.startswith("Teaching line") or after) and CJK.search(l):
                probs.append(f"note {k}: CJK in a label or Say it line: {l[:30]!r}")
    return probs


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
        notes, media = None, []
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
            probs.append(f"slide {k}: picture is not full bleed against sldSz")
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


def note_lines_pptx(notes):
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
                    txt += "$" + "".join(t.text or "" for t in el.findall(".//m:t", PNS)) + "$"
            if txt.strip():
                lines.append(txt.strip())
    return lines


def check_notes_pptx(slides_tex, pptx):
    probs = []
    titles = [frame_title(f) for f in frames(strip_comments(slides_tex))]
    _, slides = pptx_parts(pptx)
    for k, (title, (_, notes, _)) in enumerate(zip(titles, slides), 1):
        probs += note_structure(title, note_lines_pptx(notes), f"slide {k} '{title}'")
    return probs


def check_notes_maths(slides_tex, pptx):
    probs = []
    notes_src = [note_of(f) or "" for f in frames(strip_comments(slides_tex))]
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
                    if re.search(r"[^\s/]/[^\s/]", re.sub(r"\S+\.pdf", "", tu)):
                        probs.append(f"slide {k}: unspaced slash in note prose: {t!r}")
    return probs


# ------------------------------------------------------------ runner
def lesson_files(n):
    sheets = [f"handout{n}"]
    pairs = []
    extra = ("mock",) if str(n) == "4" else ()
    for s in (f"classwork{n}", f"hw{n}", f"practice{n}") + extra:
        if os.path.exists(p(s + ".tex")):
            sheets += [s, s + "_answers"]
            pairs.append((s, s + "_answers"))
    return sheets, pairs


def expander():
    sys.path.insert(0, HERE)
    from export_pptx import Expander
    return Expander(p("shared.sty")).expand


def run_tex(n):
    s = f"slides{n}"
    sheets, pairs = lesson_files(n)
    slides = read(p(s + ".tex"))
    sheet_texs = {f"{x}.tex": read(p(f"{x}.tex")) for x in sheets if not x.endswith("_answers")}
    logs = [p(f"{x}.log") for x in sheets] + [p(f"{s}_screen.log"), p(f"{s}_notes.log"), p(f"{s}.log")]
    printed = [p(f"{x}.pdf") for x in sheets] + [p(f"{s}_screen.pdf")]
    ex = expander()
    return [
        ("1", "Clean compile", check_logs(logs)),
        ("1b", "Screen text clears the footer", check_footer_clear(p(f"{s}_screen.pdf"))),
        ("1c", "Note pages do not overflow", check_notes_inside(p(f"{s}_notes.pdf"))),
        ("1d", "No solid dark fills", sum((check_dark_fills(f) for f in printed), [])),
        ("2", "Fonts embedded", check_fonts(printed + [p(f"{s}_notes.pdf"), p(f"{s}.pdf")], logs)),
        ("3", "No answers on screen", check_no_answers(slides)),
        ("4", "No slash fractions or fake superscripts", check_fractions({f"{s}.tex": slides, **sheet_texs})),
        ("5", "No banned commands", check_banned(slides)),
        ("5b", "Frame bodies not swallowed", check_frames(slides)),
        ("6", "Plots stay on canvas (n/a: no matplotlib)",
         check_plots([p(f) for f in os.listdir(HERE) if f.endswith(".py") and f not in ("check.py", "test_checks.py")])),
        ("10s", "Notes structure (source)", check_notes_source(slides, ex)),
        ("12", "Spot the error integrity", check_spot_error(slides, sheet_texs, p("shared.sty"))),
        ("13", "Say it: once, where first said", check_say_it(slides, ex)),
        ("14", "Blank and answer layouts match",
         sum((check_layout_pair(p(a + ".pdf"), p(b + ".pdf")) for a, b in pairs), [])),
        ("15", "Page number on every slide", check_page_numbers(p(f"{s}_screen.pdf"))),
        ("16", "Languages kept apart", check_languages(slides, sheet_texs)),
    ]


def run_pptx(n):
    s = f"slides{n}"
    slides = read(p(s + ".tex"))
    x = p(s + ".pptx")
    return [
        ("7", "Page alignment", check_alignment(slides, p(s + ".pdf"), x)),
        ("8", "Slides are pure images", check_pure_images(x)),
        ("9", "No images in notes", check_no_note_images(x)),
        ("10", "Notes structure (PPTX)", check_notes_pptx(slides, x)),
        ("11", "Notes maths truly typeset", check_notes_maths(slides, x)),
    ]


def main():
    args = sys.argv[1:]
    n = next(a for a in args if a.isdigit())
    results = []
    if "--pptx" not in args:
        results += run_tex(n)
    if "--tex" not in args:
        results += run_pptx(n)
    bad = 0
    for item, name, probs in results:
        print(f"{item:>3}  {name:<45} {len(probs)}")
        for pr in probs[:15]:
            print(f"       - {pr}")
        bad += len(probs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
