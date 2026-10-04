#!/bin/bash
# The tutor's Chinese prep book, generated from slides.tex (\zh blocks and
# notes) and the screen PDF; run after build_slides.sh.
set -euo pipefail
cd "$(dirname "$0")"
python3 tools/build_prep.py
for pass in 1 2; do
  xelatex -interaction=nonstopmode -halt-on-error prep_zh.tex > /dev/null || { echo "compile failed: prep_zh"; exit 1; }
done
echo "prep_zh.pdf"
