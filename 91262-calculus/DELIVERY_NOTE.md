# Delivery note: NCEA Level 2 Calculus (AS 91262), 5 lessons

Built to Teaching Materials Specification v16. The setting is the one the tutor chose:

- **Teaching mode and viewing distance:** mixed, big TV viewed near
- **Font floor:** 12 pt, set by the tutor
- **Materials:** printed handout, all English
- **Target:** secure Achieved, aim for Merit, some Excellence (marked Extension)

**Structure:** 4 teaching lessons plus 1 mixed practice lesson, each 1 h 45 min:

| Time | Activity |
|---|---|
| 10 min | Do Now |
| about 60 min | 3 rounds of "teach, then practise" |
| 30 min | practice sheet |
| 5 min | wrap-up and homework |

**Machine checks:** all §10.2 items are 0 for every lesson (`check.py --all`). Every item was proven by a planted fault (`test_checks.py`: no blind checks). `tools/verify_answers.py` checks 227 numerical answers with sympy.

## Figures produced

TikZ figures, shared by handout and slides:

| Lesson | Figures |
|---|---|
| 1 | `fig/L1_tangents.tex` |
| 2 | `fig/L2_turning.tex`, `L2_pen.tex`, `L2_box.tex`, `L2_rect.tex` |
| 3 | `fig/L3_parab_f.tex`, `L3_parab_fp.tex`, `L3_cubic_f.tex`, `L3_cubic_fp.tex`, `L3_rev_fp.tex`, `L3_rev_f.tex`, `L3_dn.tex` |
| 4 | `fig/L4_chain.tex` |

- **Graph grids:** all drawn by the `\sketch` macro in `shared.sty`, with computed curves. This covers the Lesson 3 practice rounds, the sketch page, the practice sheet and the 14-question homework.
- **Exam crops:** 26 crops in `fig/ppfull/` at natural size (300 dpi, at most 181 mm wide), plus red answer overlays (`*_ans.tex`). The graph overlays are generated from pixel calibration by `tools/graph_overlays.py`.

## Removed from exam questions, and why

- **Page furniture:** page numbers, the "Mathematics and Statistics 91262, year" footers, "QUESTION ONE/TWO/THREE" headings, and the cross-hatched assessor margin. These carry provenance or point to booklet layout.
- **Redraw callouts:** "If you need to redraw this graph, use the grid on page 12/13" (2021 Q2(a), Q3(c); 2022 Q2(a), Q3(b)(i), (ii)). They point to pages that do not exist in our sets.
- **Spare-grid pages and extra-space pages:** not included.
- **Answer-line whitespace:** capped at the largest cap that keeps each part on one A4 page. Nothing of the question itself was removed.

Kept exactly as printed:

- **2022 Q3(b)(iii):** "using the graphs on pages 8 and 9". In our sheet those graphs are on the previous page and the same page.
- **2022 Q3(c):** the grey photo placeholder and its source URL line.

## Deliberately left out

- **Past papers on slides:** none. Every real question is in the printed practice or homework sets at natural size, where the student can write on it. Slides carry only original questions.
- **Official marking:** no assessment schedules were supplied. There are no mark-scheme extracts; every exam answer is tutor's working and labelled so.
- **Negative and fractional powers:** not included. Both papers use polynomials only.

## Deviations from the specification

1. **Grade tags instead of marks.** NCEA is marked holistically, so questions carry [A] / [M] / [E] tags at the right margin instead of [n] marks. Headers show time only, not a marks total.
2. **Short exam parts may share a page.** They go on one page with another question only when the whole crop plus its heading fits (`\ppQQ`, which uses the crop's measured height). Nothing is ever split or shrunk. Long parts start a new page (`\ppQ`). This saves paper: Lesson 1 practice is 4 pages instead of 7.
3. **2022 Q2(a) heading sits beside the crop** (`\ppQside`). The crop is 240 mm tall even at the tightest whitespace cap, so a heading line above it would not fit.
4. **Slide sizes.** The tutor set a 12 pt floor. Used sizes: title 17, emphasis 15, body/questions/sub-parts/summary/TikZ labels 13, formula box 18, footer 8 pt. Notes pages are 8.5 pt (notes are exempt).
5. **Slide margins.** Side margins are set with `\setbeamersize` (5 mm, 160 mm text block). The 16:9 paper is set with `\geometry` without a margin override: an override pushed the footer off the page, which check 1b caught.
6. **Signature "light weight".** TeX Gyre has no light weight, so the signature is set in 55% grey.
7. **Lesson 3 sketch page.** The practice sheet opens with a sketch page of 6 blank grids for the in-lesson practice rounds. Its answer version shows the red answers.
8. **Lesson 3 homework is generated.** `lesson3/hw.tex` is produced by `tools/make_hw3.py`. Edit the generator, not the `.tex`.
9. **Vertical scale of unlabelled graph answers.** 2021 Q2(a) and Q3(c) have unlabelled axes, so the red sketch's vertical scale is illustrative; the key x-values are exact. See `SOURCE_MAP.md`.
10. **Check refinements** (each confirmed by `test_checks.py`):
    - **1b / 1c:** words come from PyMuPDF with an unbounded clip. pdftotext silently drops off-page text, which made an overflowing notes page look clean.
    - **2:** the font-warning pattern is narrowed. "not available" matched a `pdfcol` info line (a false alarm).
    - **10:** a "Lesson N" divider title is not a question slide (Lesson 5's divider contains "Practice"). The TeX-quote test ignores maths, because f''(x) is not a quote.
11. **Check 1d whitelist:** none. **PDFs fixed in place:** none. **Handout trims below the readable minimum:** none.

## Still needs a real-machine check

- **PowerPoint presenter view** (Microsoft 365): native equations in the notes pane, at 16 pt. This cannot be checked in the container.
- **A printed copy:** grey grids and answer rules visible, no dark areas. Print exam crops at "actual size" (100%) so they stay natural size.
