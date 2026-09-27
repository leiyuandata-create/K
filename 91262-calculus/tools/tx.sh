#!/bin/bash
# tx.sh <dir> <file.tex> [jobname] [pre-tex]: compile twice with XeLaTeX, print problems
cd "$1" || exit 1
f="$2"; job="${3:-${f%.tex}}"; pre="$4"
export TEXINPUTS=.:..:
for i in 1 2; do xelatex -interaction=nonstopmode -halt-on-error -jobname="$job" "${pre}\\input{$f}" > /dev/null 2>&1; done
echo "== $1/$job: $(pdfinfo $job.pdf 2>/dev/null | grep Pages | awk '{print $2}') pages"
grep -E "^!|Overfull|Missing character|not found|undefined" "$job.log" | sort | uniq -c | head -20
