#!/usr/bin/env python3
"""Write slides_zh.tex: the Chinese screen of each slide (from
slides_zh_frames.tex) joined with that slide's \\note{} from slides.tex,
so the notes are written once and the two decks stay page for page."""
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def main():
    en = open(os.path.join(HERE, "slides.tex"), encoding="utf-8").read()
    pre = en[:en.index("\\begin{document}")]
    frames = re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", en[en.index("\\begin{document}"):], re.S)
    notes = []
    for fr in frames:
        m = re.search(r"\\note\{", fr)
        body, _ = brace_body(fr, m.end() - 1)
        notes.append(body)

    src = open(os.path.join(HERE, "slides_zh_frames.tex"), encoding="utf-8").read()
    blocks = re.split(r"^%%% FRAME (\d+) \{(.*)\}\s*$", src, flags=re.M)
    zh = {int(blocks[i]): (blocks[i + 1], blocks[i + 2].strip()) for i in range(1, len(blocks), 3)}
    if sorted(zh) != list(range(1, len(frames) + 1)):
        raise SystemExit(f"slides_zh_frames.tex has frames {sorted(zh)}; slides.tex has {len(frames)}")

    out = ["% slides_zh.tex -- written by tools/build_zh_deck.py; do not edit.",
           "% Screen: slides_zh_frames.tex. Notes: slides.tex.",
           pre.replace("\\title{", "\\zhdecktrue\n\\title{", 1), "\\begin{document}\n"]
    for k in range(1, len(frames) + 1):
        title, body = zh[k]
        head = f"\\begin{{frame}}{{{title}}}" if title else "\\begin{frame}"
        out.append(f"{head}\n\\relax\n{body}\n\\note{{{notes[k - 1]}}}\n\\end{{frame}}\n")
    out.append("\\end{document}\n")
    open(os.path.join(HERE, "slides_zh.tex"), "w", encoding="utf-8").write("\n".join(out))
    print(f"slides_zh.tex: {len(frames)} frames")


if __name__ == "__main__":
    main()
