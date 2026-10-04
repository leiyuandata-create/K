#!/usr/bin/env python3
"""Build the tutor's Chinese prep book source (prep_zh_body.tex) from
slides.tex, so the book can never drift from the deck (spec v21):

* a glossary: English term, Chinese meaning, one-line note, and the
  pronunciation taken from the deck's own Say it: lines;
* one entry per slide: a thumbnail of the screen (from slides_screen.pdf),
  the slide's \\zh{} block (Chinese translation + background), the answers
  and explanation from its \\note{}, and its Script: lines.
"""
import os
import re

import pymupdf

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THUMBS = os.path.join(HERE, "thumbs")


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


def macro_body(fr, name):
    m = re.search(r"\\" + name + r"\{", fr)
    if not m:
        return ""
    body, _ = brace_body(fr, m.end() - 1)
    return strip_comments(body)


def frame_title(fr):
    m = re.match(r"\s*\{", fr)
    if not m:
        return ""
    t, _ = brace_body(fr, m.end() - 1)
    return t


def lines_of(body):
    return [l.strip() for l in re.split(r"\\par\b", body) if l.strip()]


LABELS = ("Short solution:", "Watch for:", "Diagnostic:", "Script:", "Say it:")
LABEL_ZH = {"Short solution:": "讲解 (Short solution)", "Watch for:": "注意 (Watch for)",
            "Diagnostic:": "诊断 (Diagnostic)"}


def main():
    tex = open(os.path.join(HERE, "slides.tex"), encoding="utf-8").read()
    body = tex[tex.index("\\begin{document}"):]
    frames = re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", body, re.S)

    # thumbnails of the screen slides
    os.makedirs(THUMBS, exist_ok=True)
    doc = pymupdf.open(os.path.join(HERE, "slides_screen.pdf"))
    if doc.page_count != len(frames):
        raise SystemExit(f"frames {len(frames)} != screen pages {doc.page_count}")
    for k, page in enumerate(doc, 1):
        page.get_pixmap(dpi=150).save(os.path.join(THUMBS, f"slide-{k:02d}.png"))

    # pronunciation from the deck's Say it: lines
    say = {}
    notes = [macro_body(fr, "note") for fr in frames]
    for n in notes:
        ls = lines_of(n)
        if "Say it:" in ls:
            for l in ls[ls.index("Say it:") + 1:]:
                w, p = l.split(" = ")
                say[w.lower()] = p

    def pron(term):
        for part in re.split(r"\s*/\s*", term):
            w = part.lower()
            for cand in (w, w + "s", w.rstrip("s"), w.split()[0]):
                if cand in say:
                    return say[cand]
        return ""

    out = ["% prep_zh_body.tex -- written by tools/build_prep.py; do not edit"]
    out.append("\\section*{术语表 Glossary}")
    out.append("英文术语是考试要写的词；读音来自课件备注里的 Say it（大写的音节读重音）。\\par\\medskip")
    for unit, name in (("GM", "Green Machines（植物）"), ("MM", "Metallic materials（金属）")):
        out.append(f"\\subsection*{{{name}}}")
        out.append("\\begin{longtable}{@{}p{36mm}p{30mm}p{36mm}p{60mm}@{}}\\toprule")
        out.append("\\textbf{English} & \\textbf{中文} & \\textbf{读音 Say it} & \\textbf{说明}\\\\\\midrule\\endhead")
        for row in open(os.path.join(HERE, "tools", "glossary_zh.tsv"), encoding="utf-8"):
            if row.startswith("#") or not row.strip():
                continue
            term, zh, note, u = row.rstrip("\n").split("\t")
            if u != unit:
                continue
            note = note.replace("cm3", "cm$^{3}$")
            out.append(f"{term} & {zh} & {{\\sffamily\\small {pron(term)}}} & {note}\\\\")
        out.append("\\bottomrule\\end{longtable}")
    out.append("\\clearpage")

    for k, fr in enumerate(frames, 1):
        title = frame_title(fr) or ("课程封面" if k == 1 else "Lesson divider")
        zh = lines_of(macro_body(fr, "zh"))
        ls = lines_of(notes[k - 1])
        if ls and ls[0].startswith("Teaching line"):
            ls = ls[1:]
        cut = [ls.index(l) for l in ("Script:", "Say it:") if l in ls]
        main_part = ls[:min(cut)] if cut else ls
        script = []
        if "Script:" in ls:
            i = ls.index("Script:") + 1
            j = ls.index("Say it:") if "Say it:" in ls else len(ls)
            script = ls[i:j]
        sayit = ls[ls.index("Say it:") + 1:] if "Say it:" in ls else []

        out.append(f"\\prepentry{{{k}}}{{{title}}}{{thumbs/slide-{k:02d}.png}}{{%")
        out.append("\\par\n".join(zh) + "}")
        out.append("\\prepblock{答案与讲解}{%")
        rendered = []
        for l in main_part:
            if l in LABEL_ZH:
                rendered.append(f"\\textbf{{{LABEL_ZH[l]}}}")
            else:
                rendered.append(l)
        out.append("\\par\n".join(rendered) if rendered else "（本页没有题目）")
        out.append("}")
        if script:
            out.append("\\prepblock{讲稿 Script}{%")
            out.append("\\par\n".join(script) + "}")
        if sayit:
            out.append("\\prepblock{读音 Say it}{%")
            out.append("\\quad ".join(f"{{\\sffamily {s}}}" for s in sayit) + "}")
        out.append("\\prependentry")
    open(os.path.join(HERE, "prep_zh_body.tex"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"prep_zh_body.tex: {len(frames)} slides, {len(say)} pronunciations")


if __name__ == "__main__":
    main()
