#!/bin/bash
# build.sh N -- sheets -> slides -> check.py --tex -> export_pptx.py -> check.py --pptx
# One lesson per call: a lesson takes over a minute (spec 9.1).
set -euo pipefail -o pipefail
cd "$(dirname "$0")"
N=${1:?lesson number}
./build_sets.sh $N
./build_slides.sh $N
python3 check.py $N --tex
python3 export_pptx.py $N
python3 check.py $N --pptx
