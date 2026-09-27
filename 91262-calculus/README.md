# NCEA Level 2 Calculus (AS 91262): 5 lessons

Five 1 h 45 min lessons for a student who needs a slow, well-supported path to Achieved and Merit, with some Excellence.

| Lesson | Topic |
|---|---|
| 1 | Gradients, differentiation and tangents |
| 2 | Turning points and optimisation |
| 3 | Sketching gradient functions (f to f′ and back) |
| 4 | Anti-differentiation, rates of change and kinematics |
| 5 | Mixed practice: exam guide, timed practice, Excellence homework |

## In each `lessonN/` folder

| File | Use |
|---|---|
| `handout.pdf` | printed notes and worked examples (hand out, collect at the end) |
| `slides.pptx` | teach from this: slides are images, answers are in the presenter notes |
| `slides.pdf` | backup: slide on the left, notes on the right |
| `slides_screen.pdf` | slides only (print 2-up if wanted) |
| `practice.pdf` / `practice_answers.pdf` | the 30-minute in-class practice sheet, blank and red-answer versions |
| `hw.pdf` / `hw_answers.pdf` | the 60-minute homework, blank and red-answer versions |

Print exam pages at **actual size (100%)**.

- **`SOURCE_MAP.md`** (tutor only) lists where each exam question came from.
- **`DELIVERY_NOTE.md`** lists deviations and what still needs a real-machine check.

## Rebuild

```
./build.sh              # everything: answers -> crops -> sheets -> slides -> checks -> PPTX -> checks
./build.sh lesson2      # one lesson
python3 check.py --all  # spec section 10.2 checks, must print TOTAL 0
python3 test_checks.py  # plants one fault per check and confirms each is caught
```

Needs XeLaTeX (TeX Live), poppler-utils and pandoc, plus the Python packages pymupdf, pikepdf, python-pptx, lxml, opencv-python-headless and sympy. Fonts are in `fonts/` (TeX Gyre, GUST Font License).
