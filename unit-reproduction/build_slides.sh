#!/bin/bash
# Screen and notes compiles, joined side by side into the double-width
# slides.pdf (spec 9.2).
set -euo pipefail
cd "$(dirname "$0")"
D=${1:-slides}          # slides (English screen) or slides_zh (Chinese screen)

run() { xelatex -interaction=nonstopmode -halt-on-error "$@" > /dev/null || { echo "compile failed: $*"; exit 1; }; }

for pass in 1 2; do
  run -jobname=${D}_screen $D.tex
  run -jobname=${D}_notes "\def\notesmode{1}\input{$D.tex}"
done

n_screen=$(python3 -c "import pymupdf;print(pymupdf.open('${D}_screen.pdf').page_count)")
n_notes=$(python3 -c "import pymupdf;print(pymupdf.open('${D}_notes.pdf').page_count)")
if [ "$n_screen" != "$n_notes" ]; then
  echo "page counts differ: screen $n_screen, notes $n_notes"; exit 1
fi

python3 - "$n_screen" "$D" <<'PYEOF'
import sys
n, d = int(sys.argv[1]), sys.argv[2]
pages = ",".join(f"{d}_screen.pdf,{i},{d}_notes.pdf,{i}" for i in range(1, n + 1))
with open(f"{d}_join.tex", "w") as fh:
    fh.write("\\documentclass{article}\n"
             "\\usepackage[paperwidth=340mm,paperheight=95.625mm,margin=0mm]{geometry}\n"
             "\\usepackage{pdfpages}\n\\begin{document}\n"
             f"\\includepdfmerge[nup=2x1,noautoscale,delta=0 0]{{{pages}}}\n"
             "\\end{document}\n")
PYEOF
run -jobname=$D ${D}_join.tex
echo "$D.pdf: $n_screen double-width pages"
