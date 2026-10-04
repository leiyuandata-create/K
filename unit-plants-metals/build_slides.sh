#!/bin/bash
# Screen and notes compiles, joined side by side into the double-width
# slides.pdf (spec 9.2).
set -euo pipefail
cd "$(dirname "$0")"

run() { xelatex -interaction=nonstopmode -halt-on-error "$@" > /dev/null || { echo "compile failed: $*"; exit 1; }; }

for pass in 1 2; do
  run -jobname=slides_screen slides.tex
  run -jobname=slides_notes "\def\notesmode{1}\input{slides.tex}"
done

n_screen=$(python3 -c "import pymupdf;print(pymupdf.open('slides_screen.pdf').page_count)")
n_notes=$(python3 -c "import pymupdf;print(pymupdf.open('slides_notes.pdf').page_count)")
if [ "$n_screen" != "$n_notes" ]; then
  echo "page counts differ: screen $n_screen, notes $n_notes"; exit 1
fi

python3 - "$n_screen" <<'PYEOF'
import sys
n = int(sys.argv[1])
pages = ",".join(f"slides_screen.pdf,{i},slides_notes.pdf,{i}" for i in range(1, n + 1))
with open("slides_join.tex", "w") as fh:
    fh.write("\\documentclass{article}\n"
             "\\usepackage[paperwidth=340mm,paperheight=95.625mm,margin=0mm]{geometry}\n"
             "\\usepackage{pdfpages}\n\\begin{document}\n"
             f"\\includepdfmerge[nup=2x1,noautoscale,delta=0 0]{{{pages}}}\n"
             "\\end{document}\n")
PYEOF
run -jobname=slides slides_join.tex
echo "slides.pdf: $n_screen double-width pages"
