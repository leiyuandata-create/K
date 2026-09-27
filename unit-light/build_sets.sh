#!/bin/bash
# Printed A4 sheets. The handout is compiled twice so its labels settle
# (the slides read its page numbers).
set -euo pipefail
cd "$(dirname "$0")"
python3 tools/geom.py
for f in handout inclass hw1 inclass_answers hw1_answers; do
  for pass in 1 2; do
    xelatex -interaction=nonstopmode -halt-on-error "$f.tex" > /dev/null || { echo "compile failed: $f"; exit 1; }
  done
  echo "$f.pdf"
done
