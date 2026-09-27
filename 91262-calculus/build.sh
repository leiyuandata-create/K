#!/bin/bash
# build.sh: answers -> crops/overlays -> sheets -> slides -> check.py --tex -> PPTX -> check.py --pptx
set -e
cd "$(dirname "$0")"
LESSONS="${*:-lesson1 lesson2 lesson3 lesson4 lesson5}"
python3 tools/verify_answers.py
if [ -f "/root/.claude/uploads/6a876be3-23aa-5e8f-9c18-b92963ea9869/ceb38c27-91262-exm-2021.pdf" ]; then
  python3 tools/crop_pp.py > /dev/null && echo "exam crops regenerated"
else
  echo "source exam PDFs not present: using committed crops in fig/ppfull/"
fi
python3 tools/graph_overlays.py > /dev/null
python3 tools/make_hw3.py > /dev/null
for L in $LESSONS; do
  ./build_sets.sh "$L"
  ./build_slides.sh "$L"
done
python3 check.py --tex $LESSONS
for L in $LESSONS; do python3 export_pptx.py "$L"; done
python3 check.py --pptx $LESSONS
