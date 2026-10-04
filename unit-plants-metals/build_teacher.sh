#!/bin/bash
# Teacher PDF: English slide on the left (projected), Chinese slide with
# the answers in red on the right. Run after both decks are built.
set -euo pipefail
cd "$(dirname "$0")"
run() { xelatex -interaction=nonstopmode -halt-on-error "$@" > /dev/null || { echo "compile failed: $*"; exit 1; }; }
python3 tools/build_teacher.py
run teacher_pages.tex
n_en=$(python3 -c "import pymupdf;print(pymupdf.open('slides_screen.pdf').page_count)")
n_t=$(python3 -c "import pymupdf;print(pymupdf.open('teacher_pages.pdf').page_count)")
if [ "$n_en" != "$n_t" ]; then echo "page counts differ: English $n_en, teacher $n_t"; exit 1; fi
python3 - "$n_en" <<'PYEOF'
import sys
n = int(sys.argv[1])
pages = ",".join(f"slides_screen.pdf,{i},teacher_pages.pdf,{i}" for i in range(1, n + 1))
with open("teacher_join.tex", "w") as fh:
    fh.write("\\documentclass{article}\n"
             "\\usepackage[paperwidth=340mm,paperheight=95.625mm,margin=0mm]{geometry}\n"
             "\\usepackage{pdfpages}\n\\begin{document}\n"
             f"\\includepdfmerge[nup=2x1,noautoscale,delta=0 0]{{{pages}}}\n"
             "\\end{document}\n")
PYEOF
run -jobname=slides_teacher teacher_join.tex
echo "slides_teacher.pdf: $n_en double-width pages"
