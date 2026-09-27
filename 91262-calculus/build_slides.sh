#!/bin/bash
# build_slides.sh <lessondir>: slides_screen.pdf + slides_notes.pdf -> slides.pdf (slide | notes)
set -e
cd "$(dirname "$0")/$1"
export TEXINPUTS=.:..:
run() { xelatex -interaction=nonstopmode -halt-on-error "$@" > /dev/null 2>&1 || { echo "XeLaTeX failed: $*"; exit 1; }; }
for i in 1 2; do
  run -jobname=slides_screen "\input{slides.tex}"
  run -jobname=slides_notes "\def\notesmode{1}\input{slides.tex}"
done
ns=$(pdfinfo slides_screen.pdf | awk '/^Pages/{print $2}')
nn=$(pdfinfo slides_notes.pdf | awk '/^Pages/{print $2}')
if [ "$ns" != "$nn" ]; then echo "page count mismatch: screen $ns, notes $nn"; exit 1; fi
cat > slides_join.tex <<EOF
\documentclass{article}
\usepackage[paperwidth=340mm,paperheight=95.625mm,margin=0mm]{geometry}
\usepackage{pdfpages}
\begin{document}
\includepdfmerge[nup=2x1,pages=-]{slides_screen.pdf,1,slides_notes.pdf,1$(for i in $(seq 2 $ns); do printf ',slides_screen.pdf,%d,slides_notes.pdf,%d' $i $i; done)}
\end{document}
EOF
run slides_join.tex
mv slides_join.pdf slides.pdf
cp slides_join.log slides.log
echo "$1: $ns slides joined"
