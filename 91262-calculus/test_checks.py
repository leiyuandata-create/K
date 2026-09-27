#!/usr/bin/env python3
"""test_checks.py: mutation tests for check.py (spec 10.3.6).
Copies the project to a scratch directory, plants ONE fault per check item in lesson1,
rebuilds only what the fault needs, verifies the fixture really contains the fault, and
asserts that the item fires (and that the clean copy gives 0)."""
import os, re, shutil, subprocess, sys, tempfile, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)


def fresh(tmp):
    d = os.path.join(tmp, 'proj')
    if os.path.exists(d):
        shutil.rmtree(d)
    shutil.copytree(HERE, d, ignore=shutil.ignore_patterns('lesson2', 'lesson3', 'lesson4', 'lesson5', '.git'))
    return d


def item(d, name):
    sys.path.insert(0, d)
    import importlib
    import check
    importlib.reload(check)
    fn = dict(check.TEX_ITEMS + check.PPTX_ITEMS)[name]
    return fn(os.path.join(d, 'lesson1'))


def edit(path, old, new, count=1):
    s = open(path).read()
    assert old in s, 'fixture anchor missing: %r' % old
    open(path, 'w').write(s.replace(old, new, count))


def main():
    tmp = tempfile.mkdtemp()
    results = []

    def case(name, plant, fixture_ok, rebuild):
        d = fresh(tmp)
        L = os.path.join(d, 'lesson1')
        plant(d, L)
        if rebuild:
            sh(rebuild, d)
        assert fixture_ok(d, L), 'fixture for item %s does not contain its fault' % name
        n = len(item(d, name))
        results.append((name, n))
        print('item %-3s planted fault -> %d finding(s)%s' % (name, n, '' if n else '   <-- BLIND'))

    # baseline: clean copy passes every item
    d = fresh(tmp)
    import importlib
    sys.path.insert(0, d)
    import check
    base = sum(len(fn(os.path.join(d, 'lesson1'))) for _, fn in check.TEX_ITEMS + check.PPTX_ITEMS)
    print('baseline (clean copy): %d finding(s)' % base)
    assert base == 0

    tex = lambda L, f: os.path.join(L, f)
    case('1', lambda d, L: edit(tex(L, 'handout.tex'), '\\section{Words and symbols}',
                                '\\noindent\\hbox to 1.5\\textwidth{overflow}\\par\\section{Words and symbols}'),
         lambda d, L: 'Overfull \\hbox' in open(tex(L, 'handout.log')).read(), 'tools/tx.sh lesson1 handout.tex')
    case('1b', lambda d, L: edit(tex(L, 'slides.tex'), 'Ask the student to say each line back before looking at the screen.}',
                                 'Ask the student to say each line back before looking at the screen.}\n\\vskip44mm FOOTERHIT', 1),
         lambda d, L: 'FOOTERHIT' in sh('pdftotext lesson1/slides_screen.pdf -', d).stdout and 'Overfull \\vbox' in open(tex(L, 'slides_screen.log')).read(), './build_slides.sh lesson1')
    case('1c', lambda d, L: edit(tex(L, 'slides.tex'), 'Ask the student to say each line back before looking at the screen.}',
                                 'Ask the student to say each line back before looking at the screen.' + '\\par long note line' * 60 + '}'),
         lambda d, L: 'Overfull \\vbox' in open(tex(L, 'slides_notes.log')).read(),
         './build_slides.sh lesson1')
    case('1d', lambda d, L: edit(tex(L, 'handout.tex'), '\\section{Words and symbols}',
                                 '\\noindent\\rule{60mm}{15mm}\\par\\section{Words and symbols}'),
         lambda d, L: True, 'tools/tx.sh lesson1 handout.tex')

    def unembed(d, L):
        import pikepdf
        p = tex(L, 'handout.pdf')
        pdf = pikepdf.open(p, allow_overwriting_input=True)
        hit = 0
        for pg in pdf.pages:                       # walk fonts hanging off page resources
            for _, f in pg.resources.get('/Font', {}).items():
                for desc in [f.get('/FontDescriptor')] + [x.get('/FontDescriptor') for x in f.get('/DescendantFonts', [])]:
                    if desc is not None:
                        for k in ('/FontFile', '/FontFile2', '/FontFile3'):
                            if k in desc:
                                del desc[k]; hit += 1
        pdf.save(p)
        assert hit
    case('2', unembed, lambda d, L: ' no ' in sh('pdffonts lesson1/handout.pdf', d).stdout, None)
    case('3', lambda d, L: edit(tex(L, 'slides.tex'), '\\qn{3} $y=(x-2)^{2}$', '\\qn{3} $y=(x-2)^{2}$ Answer: $2x-4$'),
         lambda d, L: True, None)
    case('4', lambda d, L: edit(tex(L, 'handout.tex'), 'Differentiate each term on its own.',
                                'Differentiate each term on its own. Speed $v=d/t$.'), lambda d, L: True, None)
    case('5', lambda d, L: edit(tex(L, 'slides.tex'), '\\qn{1} $f(x)=5x^{3}-4x^{2}+x-9$', '{\\small \\qn{1}} $f(x)=5x^{3}-4x^{2}+x-9$'),
         lambda d, L: True, None)
    case('5b', lambda d, L: edit(tex(L, 'slides.tex'), '\\begin{frame}{Summary}\\relax', '\\begin{frame}{Summary}{\\relax}'),
         lambda d, L: True, None)
    case('6', lambda d, L: open(os.path.join(d, 'tools', 'plot_extra.py'), 'w').write('import matplotlib\n'),
         lambda d, L: True, None)
    case('7', lambda d, L: edit(tex(L, 'slides.tex'), '\\end{document}',
                                '\\begin{frame}{Extra}\\relax x\\note{Teaching line, not a question slide.}\\end{frame}\n\\end{document}'),
         lambda d, L: True, None)

    def add_shape(d, L):
        from pptx import Presentation
        from pptx.util import Inches
        p = tex(L, 'slides.pptx'); prs = Presentation(p)
        prs.slides[3].shapes.add_textbox(Inches(1), Inches(1), Inches(2), Inches(1)).text = 'extra'
        prs.save(p)
    case('8', add_shape, lambda d, L: True, None)

    def pic_in_notes(d, L):
        p = tex(L, 'slides.pptx'); tmpz = p + '.tmp'
        with zipfile.ZipFile(p) as zi, zipfile.ZipFile(tmpz, 'w', zipfile.ZIP_DEFLATED) as zo:
            for it in zi.infolist():
                data = zi.read(it.filename)
                if it.filename == 'ppt/notesSlides/notesSlide3.xml':
                    data = data.replace(b'</p:spTree>', b'<p:pic><p:nvPicPr><p:cNvPr id="9" name="x"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId9"/></p:blipFill><p:spPr/></p:pic></p:spTree>')
                zo.writestr(it, data)
        os.replace(tmpz, p)
    case('9', pic_in_notes, lambda d, L: True, None)
    case('10', lambda d, L: edit(tex(L, 'slides.tex'), 'Diagnostic:\\par\nQ1 wrong: gradient idea', 'Q1 wrong: gradient idea'),
         lambda d, L: True, 'python3 export_pptx.py lesson1')

    def caret_prose(d, L):
        p = tex(L, 'slides.pptx'); tmpz = p + '.tmp'
        with zipfile.ZipFile(p) as zi, zipfile.ZipFile(tmpz, 'w', zipfile.ZIP_DEFLATED) as zo:
            for it in zi.infolist():
                data = zi.read(it.filename)
                if it.filename == 'ppt/notesSlides/notesSlide2.xml':
                    data = data.replace(b'<a:t>Q1 </a:t>', b'<a:t>Q1 x^2 </a:t>', 1)
                zo.writestr(it, data)
        os.replace(tmpz, p)
    case('11', caret_prose, lambda d, L: b'x^2' in zipfile.ZipFile(tex(L, 'slides.pptx')).read('ppt/notesSlides/notesSlide2.xml'), None)

    shutil.rmtree(tmp)
    blind = [n for n, k in results if k == 0]
    print('blind checks:', blind or 'none')
    return 1 if blind else 0


if __name__ == '__main__':
    sys.exit(main())
