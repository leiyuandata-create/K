#!/bin/bash
# sheets -> slides (English, projected) -> tutor's deck (Chinese, answers in
# red) -> teacher PDF -> check.py --tex. No PPTX for this unit (PDF only).
set -euo pipefail
cd "$(dirname "$0")"
./build_sets.sh
./build_slides.sh slides
python3 tools/build_zh_deck.py
./build_slides.sh slides_zh
./build_teacher.sh
python3 check.py --tex
