# Source map (tutor only; not a deliverable)

This is the only place where exam questions are tied to their source. Student-facing sheets, slides and handouts carry no paper codes, years or "past paper" labels.

| Tier | Source | Used as |
|---|---|---|
| 1 | NZQA examination papers, AS 91262, 2021 and 2022 (uploaded PDFs) | real exam questions, cropped exactly as printed |
| 1 | NZQA L2-MATHF formulae sheet, 2023 (uploaded) | reference for what students are given |
| 2 | StudyTime NZ, *Level 2 Calculus Walkthrough Guide* (uploaded capture) | optional extra reading pointed to in homework footers (printed page numbers) |
| 3 | Everything else: original questions, worked examples, all answers | tutor's own work |

No assessment schedules (official marking) were supplied. Every answer to an exam question is therefore **tutor's working, not an official mark scheme**, and is labelled that way on each answer version.

## Where each exam question is used

| Lesson | Sheet | Our question | Paper | Question part | Crop id |
|---|---|---|---|---|---|
| 1 | practice | 5 | 2021 | Q1 (a) | a21_1a |
| 1 | practice | 6 | 2021 | Q1 (b) | a21_1b |
| 1 | practice | 7 | 2021 | Q2 (b) | a21_2b |
| 1 | practice | 8 | 2022 | Q1 (a) | a22_1a |
| 1 | practice | 9 | 2022 | Q1 (d) | a22_1d |
| 1 | practice | 10 | 2022 | Q3 (a) | a22_3a |
| 2 | practice | 3 | 2022 | Q1 (c) | a22_1c |
| 2 | practice | 4 | 2022 | Q2 (b) | a22_2b |
| 2 | practice | 5 | 2021 | Q1 (c)(i)(ii) | a21_1c |
| 2 | practice | 6 | 2021 | Q3 (d)(i) | a21_3d |
| 2 | practice | 7 (Extension) | 2022 | Q1 (e) | a22_1e |
| 3 | practice | 3 | 2021 | Q2 (a) | a21_2a |
| 3 | practice | 4 | 2021 | Q3 (c) | a21_3c |
| 3 | practice | 5 | 2022 | Q2 (a) | a22_2a |
| 3 | practice | 6 | 2022 | Q3 (b)(i) | a22_3b1 |
| 3 | practice | 7 | 2022 | Q3 (b)(ii)(iii) | a22_3b2 |
| 4 | practice | 3 | 2021 | Q3 (a) | a21_3a |
| 4 | practice | 4 | 2022 | Q1 (b) | a22_1b |
| 4 | practice | 5 | 2021 | Q3 (b) | a21_3b |
| 4 | practice | 6 | 2021 | Q2 (c)(i) | a21_2c1 |
| 4 | practice | 7 | 2021 | Q2 (c)(ii) | a21_2c2 |
| 4 | practice | 8 | 2022 | Q2 (c)(i)(ii) | a22_2c |
| 5 | practice | 3 | 2022 | Q2 (c)(iii) | a22_2c3 |
| 5 | homework | 7 | 2021 | Q1 (c)(iii) | a21_1c3 |
| 5 | homework | 8 | 2022 | Q3 (c) | a22_3c |
| 5 | homework | 9 (Extension) | 2021 | Q3 (d)(ii) | a21_3d2 |

All 26 exam parts from the two papers are used exactly once. No exam question repeats an original question's numbers.

## Readings behind the graph answers (tutor's working)

These were read from the printed graphs by pixel calibration (`tools/calib.py`, `tools/graph_overlays.py`), not by eye:

- **2021 Q2(a):** f has turning points exactly on grid lines x = -6, 0, 6 squares (minimums -5, maximum 16). The f′ answer is a cubic with those zeros. The axes are unlabelled, so the vertical scale is a sketch.
- **2021 Q3(c):** f′ = -0.5(x - 2)(x - 10) in grid squares (vertex (6, 8), f′(0) = -10). A possible f has a minimum at x = 2 and a maximum at x = 10. The vertical scale is a sketch.
- **2022 Q2(a):** f′ = -1.5(x + 3)(x + 1)(x - 3.5) (zeros read at -3, -1, 3.5; f′(0) about 16). A possible f has a maximum at -3, a minimum at -1 and a maximum at 3.5.
- **2022 Q3(b):** f = -x, g = x, h = x² (h passes through (2, 4)), p = |x|.

## Interpretations the tutor should know about

- **2022 Q1(e), H logo:** area = rectangle 2r × L minus two semicircles (the semicircles curve inward, as in the diagrams), and the perimeter is 2L + 2πr = 80. This gives r = 40/(3π) ≈ 4.24 cm and a maximum area of 1600/(3π) ≈ 169.8 cm².
- **2021 Q1(c)(iii):** the monetising time is t ≈ 4.20 months. After that, the local minimum is V(38.46) ≈ 10 264 > 10 000, and V(48) = 16 627, so the stream never stops earning.
