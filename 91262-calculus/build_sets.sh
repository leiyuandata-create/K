#!/bin/bash
# build_sets.sh <lessondir>: handout + practice/homework, blank and answer versions (same source)
set -e
cd "$(dirname "$0")"
L="$1"
tools/tx.sh "$L" handout.tex
for j in practice hw; do
  tools/tx.sh "$L" $j.tex
  tools/tx.sh "$L" $j.tex ${j}_answers '\def\withanswers{1}'
done
