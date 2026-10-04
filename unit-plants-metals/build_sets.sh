#!/bin/bash
# Printed A4 sheets: each source gives a blank version and an answer
# version on the identical layout (spec 6.1).
set -euo pipefail
cd "$(dirname "$0")"
python3 tools/geom.py
python3 tools/anchors.py > /dev/null
run() { xelatex -interaction=nonstopmode -halt-on-error "$@" > /dev/null || { echo "compile failed: $*"; exit 1; }; }
for f in ${SHEETS:-classwork mock hw1 hw2}; do
  for pass in 1 2; do
    run "$f.tex"
    run -jobname="${f}_answers" "\def\withanswers{1}\input{$f.tex}"
  done
  echo "$f.pdf  ${f}_answers.pdf"
done
