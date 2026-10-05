#!/bin/bash
# build_sets.sh N -- printed A4 sheets for lesson N: the handout, then each
# sheet in two versions from one source (blank, and _answers through
# \withanswers). Each is compiled twice so n / N and labels settle.
set -euo pipefail
cd "$(dirname "$0")"
N=${1:?lesson number}

run() { xelatex -interaction=nonstopmode -halt-on-error "$@" > /dev/null || { echo "compile failed: $*"; exit 1; }; }

if [ -f tools/crop.py ] && [ -f practice$N.tex ]; then python3 tools/crop.py $N; fi

run handout$N.tex; run handout$N.tex; echo "handout$N.pdf"
for f in classwork$N hw$N practice$N; do
  [ -f $f.tex ] || continue
  run $f.tex; run $f.tex
  run -jobname=${f}_answers "\def\withanswers{1}\input{$f.tex}"
  run -jobname=${f}_answers "\def\withanswers{1}\input{$f.tex}"
  echo "$f.pdf  ${f}_answers.pdf"
done
