#!/bin/bash
# sheets -> slides (English, then Chinese screen) -> teacher PDF -> check.py --tex -> export_pptx.py -> check.py --pptx
set -euo pipefail
cd "$(dirname "$0")"
./build_sets.sh
./build_slides.sh slides
python3 tools/build_zh_deck.py
./build_slides.sh slides_zh
./build_teacher.sh
python3 check.py --tex
python3 export_pptx.py slides
python3 export_pptx.py slides_zh
python3 check.py --pptx
