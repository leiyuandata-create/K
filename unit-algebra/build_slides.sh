#!/bin/bash
# build_slides.sh N -- screen and notes compiles of slidesN.tex, joined
# side by side into the double-width slidesN.pdf (spec 9.2). The handout
# must be compiled first: the slide footers read its page numbers via xr.
set -euo pipefail
cd "$(dirname "$0")"
N=${1:?lesson number}
S=slides$N

run() { xelatex -interaction=nonstopmode -halt-on-error "$@" > /dev/null || { echo "compile failed: $*"; exit 1; }; }

# screen twice, so Beamer's own total (n / N) is right
run -jobname=${S}_screen $S.tex
run -jobname=${S}_screen $S.tex
total=$(python3 -c "import pymupdf,sys;print(pymupdf.open(sys.argv[1]).page_count)" ${S}_screen.pdf)
# the notes compile cannot count frames: it is given the total
run -jobname=${S}_notes "\def\notesmode{1}\def\totalframes{$total}\input{$S.tex}"
run -jobname=${S}_notes "\def\notesmode{1}\def\totalframes{$total}\input{$S.tex}"

n_notes=$(python3 -c "import pymupdf,sys;print(pymupdf.open(sys.argv[1]).page_count)" ${S}_notes.pdf)
if [ "$total" != "$n_notes" ]; then
  echo "page counts differ: screen $total, notes $n_notes"; exit 1
fi

python3 - "$total" "$S" <<'PYEOF'
import sys
n, s = int(sys.argv[1]), sys.argv[2]
pages = ",".join(f"{s}_screen.pdf,{i},{s}_notes.pdf,{i}" for i in range(1, n + 1))
with open(f"{s}_join.tex", "w") as fh:
    fh.write("\\documentclass{article}\n"
             "\\usepackage[paperwidth=340mm,paperheight=95.625mm,margin=0mm]{geometry}\n"
             "\\usepackage{pdfpages}\n\\begin{document}\n"
             f"\\includepdfmerge[nup=2x1,noautoscale,delta=0 0]{{{pages}}}\n"
             "\\end{document}\n")
PYEOF
run -jobname=$S ${S}_join.tex
echo "$S.pdf: $total double-width pages"
