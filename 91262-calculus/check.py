#!/usr/bin/env python3
"""check.py [--tex | --pptx | --all] [lessonN ...]   Spec 10.2 machine checks; all must be 0.

 1  clean compile           every .log: Overfull \\hbox, Overfull \\vbox, '!' errors
 1b screen text clears foot  body words end >= 2 pt above the signature; none within 1 mm of a side
 1c notes pages fit          every note-page word >= 1 mm inside the page (off-page words included)
 1d no solid dark fills      text + image Do stripped, 72 dpi grey, <50 %, 3x3 erosion, >= 200 pt^2 fails
 2  fonts embedded           pdffonts emb (5th field from end) = yes; no font warnings in logs
 3  no answers on screen     slides.tex outside \\note{}: reveal headers; numerals after a mark allocation
 4  no slash fractions       maths in every .tex (notes included); ^ and Unicode sub/sup in note prose
 5  no banned commands       slides.tex + figures it inputs: size commands, \\pause, overlays, \\resizebox
 5b frame bodies             \\relax right after the title; exactly one \\note{} per frame
 6  plots on canvas          n/a unless a real matplotlib import exists
 7  page alignment           frames = screen = notes = joined = PPTX; joined width = height x 32/9
 8  slides are pure images   one 3840x2160 PNG per slide, full bleed against sldSz, nothing else
 9  no images in notes       p:pic / a:blip in notesSlides
 10 notes structure          labels, order, Do Now Diagnostic, no reveal headers
 11 notes maths typeset      native OMML: no lin/skw fractions, no / ^ or Unicode sub/sup; prose clean
"""
import glob, os, re, subprocess, sys, tempfile, zipfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SUPSUB = re.compile('[\u00b2\u00b3\u00b9\u2070-\u209f]')
LOGS = ['slides_screen', 'slides_notes', 'slides', 'handout', 'practice', 'practice_answers', 'hw', 'hw_answers']
PRINTED = ['handout', 'practice', 'practice_answers', 'hw', 'hw_answers', 'slides_screen']
WHITELIST_1D = {}   # {(lesson, pdf, page): reason}
MM = 72 / 25.4


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def strip_notes(tex):
    """slides.tex with every \\note{...} body removed; also returns the note bodies."""
    out, notes, i = [], [], 0
    while True:
        k = tex.find('\\note{', i)
        if k < 0:
            out.append(tex[i:]); break
        out.append(tex[i:k])
        d, j = 0, k + 5
        while True:
            ch = tex[j]
            if ch == '\\':
                j += 2; continue
            if ch == '{': d += 1
            elif ch == '}':
                d -= 1
                if d == 0: break
            j += 1
        notes.append(tex[k + 6:j]); i = j + 1
    return ''.join(out), notes


def uncomment(tex):
    return re.sub(r'(?<!\\)%.*', '', tex)


def maths_of(tex):
    tex = uncomment(tex)
    segs = re.findall(r'(?<!\\)\$([^$]+)\$', tex)
    segs += re.findall(r'\\\[(.+?)\\\]', tex, re.S)
    return segs


# ---------------------------------------------------------------- item implementations
def c1(ld):
    bad = []
    for n in LOGS:
        p = os.path.join(ld, n + '.log')
        if not os.path.exists(p):
            bad.append('%s.log missing' % n); continue
        for line in open(p, errors='replace'):
            if line.startswith('Overfull \\hbox') or line.startswith('Overfull \\vbox') or line.startswith('!'):
                bad.append('%s.log: %s' % (n, line.strip()[:90]))
    return bad


def words(pdf):
    """[(W, H, [(x0, y0, x1, y1, text)])] per page, INCLUDING text that runs off the page.
    pdftotext -bbox drops off-page words, which made an overflowing note page look clean
    (found by test_checks.py); PyMuPDF with an unbounded clip keeps them."""
    import pymupdf as fitz
    pages = []
    for pg in fitz.open(pdf):
        ws = [(w[0], w[1], w[2], w[3], w[4]) for w in pg.get_text('words', clip=fitz.INFINITE_RECT())]
        pages.append((pg.rect.width, pg.rect.height, ws))
    return pages


def c1b(ld):
    bad = []
    for i, (W, H, ws) in enumerate(words(os.path.join(ld, 'slides_screen.pdf')), 1):
        sig = [w for w in ws if w[4] == 'Auckland']
        if not sig:
            bad.append('slide %d: no signature' % i); continue
        sy0, sy1 = sig[-1][1], sig[-1][3]
        for w in ws:
            footer = abs(w[3] - sy1) < 1.5
            if not footer and w[3] > sy0 - 2:
                bad.append('slide %d: "%s" reaches the footer' % (i, w[4]))
            if w[0] < MM or w[2] > W - MM:
                bad.append('slide %d: "%s" within 1 mm of a side' % (i, w[4]))
    return bad


def c1c(ld):
    bad = []
    for i, (W, H, ws) in enumerate(words(os.path.join(ld, 'slides_notes.pdf')), 1):
        for w in ws:
            if w[0] < MM or w[1] < MM or w[2] > W - MM or w[3] > H - MM:
                bad.append('note page %d: "%s" outside' % (i, w[4]))
    return bad


def dark_fills(pdf, label):
    import pikepdf, pymupdf as fitz, cv2
    bad = []
    with pikepdf.open(pdf) as src, tempfile.TemporaryDirectory() as d:
        for pg in src.pages:
            imgs = set()
            xo = pg.resources.get('/XObject', {}) if pg.resources is not None else {}
            for k, v in xo.items():
                if v.get('/Subtype') == '/Image':
                    imgs.add(str(k))
            ops = pikepdf.parse_content_stream(pg)
            keep, intext = [], False
            for operands, op in ops:
                o = str(op)
                if o == 'BT': intext = True; continue
                if o == 'ET': intext = False; continue
                if intext: continue
                if o == 'Do' and operands and str(operands[0]) in imgs: continue
                keep.append((operands, op))
            pg.Contents = src.make_stream(pikepdf.unparse_content_stream(keep))
        tmp = os.path.join(d, 'stripped.pdf'); src.save(tmp)
        doc = fitz.open(tmp)
        for i, page in enumerate(doc, 1):
            if (label, i) in WHITELIST_1D:
                continue
            pix = page.get_pixmap(dpi=72, colorspace=fitz.csGRAY, alpha=False)
            a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w)
            m = (a < 128).astype(np.uint8)
            m = cv2.erode(m, np.ones((3, 3), np.uint8))
            n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
            for k in range(1, n):
                if st[k][4] >= 200:
                    bad.append('%s p.%d: dark area %d pt^2 at (%d,%d)' % (label, i, st[k][4], st[k][0], st[k][1]))
    return bad


def c1d(ld):
    bad = []
    for n in PRINTED:
        p = os.path.join(ld, n + '.pdf')
        if os.path.exists(p):
            bad += dark_fills(p, os.path.basename(ld) + '/' + n)
    return bad


def c2(ld):
    bad = []
    for p in glob.glob(os.path.join(ld, '*.pdf')):
        lines = run(['pdffonts', p]).splitlines()[2:]
        for L in lines:
            f = L.split()
            if len(f) >= 7 and f[-5] != 'yes':
                bad.append('%s: font not embedded: %s' % (os.path.basename(p), f[0]))
    for p in glob.glob(os.path.join(ld, '*.log')):
        for line in open(p, errors='replace'):
            if re.search(r'Missing character|Font shape .* undefined|Font .* not available|size substituted|Could not find font|font .* not found', line, re.I):
                bad.append('%s: %s' % (os.path.basename(p), line.strip()[:90]))
    return bad


def c3(ld):
    bad = []
    tex, _ = strip_notes(open(os.path.join(ld, 'slides.tex')).read())
    tex = uncomment(tex)
    for m in re.finditer(r'Answer:|Answer image:|Key answer:', tex):
        bad.append('reveal header "%s"' % m.group(0))
    for fr in re.split(r'\\begin\{frame\}', tex)[1:]:
        for m in re.finditer(r'\[\d+\]|\\mk\{\d+\}', fr):
            rest = fr[m.end():].split('\n', 1)[0]
            if re.search(r'\d', rest):
                bad.append('numeral after a mark allocation: %s' % rest[:40])
    return bad


SLASH = re.compile(r'[A-Za-z0-9)\]}]\s*/\s*[A-Za-z0-9(\\{]')
def c4(ld):
    bad = []
    files = glob.glob(os.path.join(ld, '*.tex')) + glob.glob(os.path.join(HERE, 'fig', '*.tex')) + \
        glob.glob(os.path.join(HERE, 'fig', 'ppfull', '*_ans.tex'))
    files = [f for f in files if not f.endswith('slides_join.tex')]
    for f in files:
        tex = open(f).read()
        for mseg in maths_of(tex):
            s = re.sub(r'\\mathrm\{[^{}]*\}', '', mseg)         # unit tokens are the only allowed slash
            if SLASH.search(s):
                bad.append('%s: slash fraction in $%s$' % (os.path.basename(f), mseg.strip()[:50]))
        if SUPSUB.search(uncomment(tex)):
            bad.append('%s: Unicode superscript/subscript' % os.path.basename(f))
    tex = open(os.path.join(ld, 'slides.tex')).read()
    _, notes = strip_notes(tex)
    for n in notes:
        prose = re.sub(r'\$[^$]*\$', ' ', n)
        if '^' in prose:
            bad.append('note prose has ^: %s' % prose.strip()[:50])
        if re.search(r'\w/\w', prose):
            bad.append('note prose has an unspaced slash: %s' % re.search(r'\S*\w/\w\S*', prose).group(0))
    return bad


BANNED = re.compile(r'\\(fontsize|small|footnotesize|scriptsize|tiny|resizebox|pause|only|uncover|onslide|visible|invisible|alt)(?![A-Za-z])|\[shrink|allowframebreaks|\\item<')
def c5(ld):
    bad = []
    tex = open(os.path.join(ld, 'slides.tex')).read()
    body, notes = strip_notes(uncomment(tex))
    srcs = [('slides.tex', body)]
    for fn in re.findall(r'\\input\{\.\./fig/([^}]+)\}', body):
        srcs.append((fn, uncomment(open(os.path.join(HERE, 'fig', fn)).read())))
    for name, s in srcs:
        for m in BANNED.finditer(s):
            bad.append('%s: banned %s' % (name, m.group(0)))
    for n in notes:
        if '\\includegraphics' in n:
            bad.append('\\includegraphics inside \\note{}')
    return bad


def frames(tex):
    body = tex[tex.index('\\begin{document}'):]
    return [fr[:fr.index('\\end{frame}')] for fr in re.split(r'\\begin\{frame\}', body)[1:]]


def c5b(ld):
    bad = []
    tex = uncomment(open(os.path.join(ld, 'slides.tex')).read())
    for i, fr in enumerate(frames(tex), 1):
        s = fr
        if s.startswith('['):
            s = s[s.index(']') + 1:]
        if s.startswith('{'):
            d = 0
            for j, ch in enumerate(s):
                if ch == '{': d += 1
                elif ch == '}':
                    d -= 1
                    if d == 0: break
            s = s[j + 1:]
        if not s.lstrip().startswith('\\relax'):
            bad.append('frame %d: body does not start with \\relax' % i)
        k = fr.count('\\note{')
        if k != 1:
            bad.append('frame %d: %d \\note{}' % (i, k))
    return bad


def c6(ld):
    hits = [p for p in glob.glob(os.path.join(HERE, '**', '*.py'), recursive=True)
            if re.search(r'^\s*(import matplotlib|from matplotlib)', open(p).read(), re.M)]
    return ['matplotlib figure without canvas check: %s' % h for h in hits]


def npages(p):
    out = run(['pdfinfo', p])
    m = re.search(r'Pages:\s+(\d+)', out)
    return int(m.group(1)) if m else -1


def c7(ld):
    bad = []
    tex = open(os.path.join(ld, 'slides.tex')).read()
    nf = len(frames(uncomment(tex)))
    counts = {n: npages(os.path.join(ld, n + '.pdf')) for n in ['slides_screen', 'slides_notes', 'slides']}
    pptx = os.path.join(ld, 'slides.pptx')
    if os.path.exists(pptx):
        z = zipfile.ZipFile(pptx)
        counts['pptx'] = len([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)])
    for k, v in counts.items():
        if v != nf:
            bad.append('%s has %d pages, %d frames' % (k, v, nf))
    m = re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', run(['pdfinfo', os.path.join(ld, 'slides.pdf')]))
    w, h = float(m.group(1)), float(m.group(2))
    if abs(w - h * 32 / 9) > 0.5:
        bad.append('joined page %.2f x %.2f is not 32:9' % (w, h))
    return bad


def pptx_parts(ld):
    from lxml import etree
    z = zipfile.ZipFile(os.path.join(ld, 'slides.pptx'))
    return z, etree


def c8(ld):
    from PIL import Image
    import io
    z, etree = pptx_parts(ld)
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
          'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
    pres = etree.fromstring(z.read('ppt/presentation.xml'))
    sz = pres.find('p:sldSz', ns); cx, cy = int(sz.get('cx')), int(sz.get('cy'))
    bad = []
    slides = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=lambda s: int(re.findall(r'\d+', s)[0]))
    for n in slides:
        x = etree.fromstring(z.read(n))
        tree = x.find('.//p:spTree', ns)
        shapes = [c for c in tree if not c.tag.endswith('nvGrpSpPr') and not c.tag.endswith('grpSpPr')]
        if len(shapes) != 1 or not shapes[0].tag.endswith('}pic'):
            bad.append('%s: %d shapes (need one picture)' % (n, len(shapes))); continue
        pic = shapes[0]
        off = pic.find('.//a:off', ns); ext = pic.find('.//a:ext', ns)
        if (int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))) != (0, 0, cx, cy):
            bad.append('%s: picture not full bleed against sldSz' % n)
        rid = pic.find('.//a:blip', ns).get('{%s}embed' % ns['r'])
        rels = etree.fromstring(z.read(n.replace('slides/', 'slides/_rels/') + '.rels'))
        tgt = [r.get('Target') for r in rels if r.get('Id') == rid][0]
        img = Image.open(io.BytesIO(z.read(os.path.normpath(os.path.join('ppt/slides', tgt)))))
        if img.format != 'PNG' or img.size != (3840, 2160):
            bad.append('%s: image %s %s' % (n, img.format, img.size))
    return bad


def c9(ld):
    z, _ = pptx_parts(ld)
    return ['%s contains an image' % n for n in z.namelist()
            if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml')
            and re.search(rb'<p:pic|<a:blip', z.read(n))]


def notes_paragraphs(ld):
    """per slide: list of paragraph texts (maths shown by its native text) from the PPTX."""
    z, etree = pptx_parts(ld)
    A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
    MC = '{http://schemas.openxmlformats.org/markup-compatibility/2006}'
    res = {}
    for n in z.namelist():
        m = re.match(r'ppt/notesSlides/notesSlide(\d+)\.xml$', n)
        if not m: continue
        x = etree.fromstring(z.read(n))
        pars = []
        for p in x.iter(A + 'p'):
            txt = ''
            for el in p.iter():
                if el.tag == A + 't' and not any(a.tag == MC + 'Fallback' for a in el.iterancestors()):
                    txt += el.text or ''
                elif el.tag.endswith('}t') and el.tag != A + 't':
                    txt += el.text or ''
            pars.append(txt)
        res[int(m.group(1))] = [t for t in pars if t.strip()]
    # map notesSlideN to slide order via slide rels
    order = {}
    for n in z.namelist():
        m = re.match(r'ppt/slides/_rels/slide(\d+)\.xml\.rels$', n)
        if m:
            t = re.search(rb'notesSlides/notesSlide(\d+)\.xml', z.read(n))
            order[int(m.group(1))] = res.get(int(t.group(1)), []) if t else []
    return [order[k] for k in sorted(order)]


LABELS = ['Short solution:', 'Watch for:', 'Diagnostic:']
QTITLE = re.compile(r'Do Now|Practice|MCQ|Workbook')
LABEL_FIRST = re.compile(r'^(Q\d+|\([a-z]{1,3}\)|WE\d|[A-D]\b)')
def c10(ld):
    bad = []
    tex = uncomment(open(os.path.join(ld, 'slides.tex')).read())
    titles = []
    for fr in frames(tex):
        s = fr[fr.index(']') + 1:] if fr.startswith('[') else fr
        titles.append(s[1:s.index('}\\relax')] if s.startswith('{') else '')
    pars = notes_paragraphs(ld)
    _, srcnotes = strip_notes(tex)
    for i, (t, ps) in enumerate(zip(titles, pars), 1):
        q = bool(QTITLE.search(t)) and not re.match(r'Lesson \d', t)   # a lesson divider is never a question slide
        if q and not ps:
            bad.append('slide %d (%s): question slide without notes' % (i, t)); continue
        if q and not LABEL_FIRST.match(ps[0]):
            bad.append('slide %d (%s): first note line has no label: %s' % (i, t, ps[0][:30]))
        labs = [p.strip() for p in ps if p.strip() in LABELS]
        for L in set(labs):
            if labs.count(L) > 1:
                bad.append('slide %d: repeated label %s' % (i, L))
        if 'Watch for:' in labs and 'Short solution:' not in labs:
            bad.append('slide %d: Watch for: without Short solution:' % i)
        if 'Watch for:' in labs and 'Short solution:' in labs and labs.index('Short solution:') > labs.index('Watch for:'):
            bad.append('slide %d: Watch for: before Short solution:' % i)
        if 'Do Now' in t and 'Diagnostic:' not in labs:
            bad.append('slide %d: Do Now without Diagnostic:' % i)
        for p in ps:
            if re.match(r'\s*(Answer:|Answer image:|Key answer:)', p):
                bad.append('slide %d: reveal header in notes' % i)
    for n in srcnotes:
        n = re.sub(r'\$[^$]*\$', ' ', n)          # f''(x) in maths is not a quote
        if '``' in n or "''" in n:
            bad.append('TeX quotes in notes (use typographic quotes)')
    return bad


def c11(ld):
    z, etree = pptx_parts(ld)
    ns = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
          'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
          'a14': 'http://schemas.microsoft.com/office/drawing/2010/main'}
    bad = []
    tex = open(os.path.join(ld, 'slides.tex')).read()
    _, srcnotes = strip_notes(uncomment(tex))
    # notes in slide order
    order = {}
    for n in z.namelist():
        m = re.match(r'ppt/slides/_rels/slide(\d+)\.xml\.rels$', n)
        if m:
            t = re.search(rb'notesSlides/notesSlide(\d+)\.xml', z.read(n))
            order[int(m.group(1))] = 'ppt/notesSlides/notesSlide%s.xml' % t.group(1).decode()
    for i, k in enumerate(sorted(order)):
        x = etree.fromstring(z.read(order[k]))
        acs = x.findall('.//mc:AlternateContent', ns)
        nsrc = len(re.findall(r'\$[^$]+\$', srcnotes[i])) if i < len(srcnotes) else 0
        good = [ac for ac in acs if ac.find('mc:Choice/a14:m/m:oMath', ns) is not None and ac.find('mc:Fallback', ns) is not None]
        if len(good) != nsrc:
            bad.append('slide %d: %d source equations, %d native+fallback' % (k, nsrc, len(good)))
        for om in x.findall('.//a14:m/m:oMath', ns):
            for ty in om.findall('.//m:fPr/m:type', ns):
                if ty.get('{%s}val' % ns['m']) in ('lin', 'skw'):
                    bad.append('slide %d: linear/skewed fraction' % k)
            txt = ''.join(om.xpath('.//m:t/text()', namespaces=ns))
            txt_nounits = re.sub(r'm/s', '', txt)
            if '/' in txt_nounits or '^' in txt or SUPSUB.search(txt):
                bad.append('slide %d: equation text not typeset: %s' % (k, txt[:40]))
        for t in x.findall('.//a:t', ns):
            if any(a.tag.endswith('}Fallback') for a in t.iterancestors()):
                continue
            s = t.text or ''
            if '^' in s or SUPSUB.search(s) or re.search(r'\w/\w', s):
                bad.append('slide %d: note prose not typeset: %s' % (k, s[:40]))
    return bad


TEX_ITEMS = [('1', c1), ('1b', c1b), ('1c', c1c), ('1d', c1d), ('2', c2), ('3', c3), ('4', c4), ('5', c5), ('5b', c5b), ('6', c6)]
PPTX_ITEMS = [('7', c7), ('8', c8), ('9', c9), ('10', c10), ('11', c11)]


def main(argv):
    mode = '--all'
    if argv and argv[0].startswith('--'):
        mode, argv = argv[0], argv[1:]
    lessons = argv or sorted(d for d in os.listdir(HERE) if re.match(r'lesson\d$', d))
    items = (TEX_ITEMS if mode in ('--tex', '--all') else []) + (PPTX_ITEMS if mode in ('--pptx', '--all') else [])
    total = 0
    for L in lessons:
        ld = os.path.join(HERE, L)
        row = []
        for name, fn in items:
            try:
                bad = fn(ld)
            except Exception as e:  # a check that cannot run is a failure, never a pass
                bad = ['check %s could not run: %r' % (name, e)]
            total += len(bad)
            row.append('%s=%d' % (name, len(bad)))
            for b in bad[:12]:
                print('  [%s] %s: %s' % (name, L, b))
            if len(bad) > 12:
                print('  [%s] %s: ... %d more' % (name, L, len(bad) - 12))
        print('%s  %s' % (L, '  '.join(row)))
    print('TOTAL', total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
