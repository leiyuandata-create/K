#!/bin/bash
# sheets -> slides -> check.py --tex -> export_pptx.py -> check.py --pptx
set -euo pipefail
cd "$(dirname "$0")"
./build_sets.sh
./build_slides.sh
python3 check.py --tex
python3 export_pptx.py
python3 check.py --pptx
