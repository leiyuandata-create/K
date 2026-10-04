# Teaching Materials Specification v24

The single current version; replaces all earlier ones. Each rule is written once, where it applies: global §3, handouts §4, slides §5, homework, classwork and answer files §6, paired output §7.

## Changes in v24 (from v23)

- The teacher PDF keeps the pronunciations: on every slide whose notes have Say it:, the right half shows the red answers on the left and a **blue Say it column** on the right (§5.9).
- In the PPTX notes, Say it: lines are blue (same blue, RGB 0,70,190) (§9.2).
- Check 7t also confirms the blue column appears on exactly the slides whose notes have Say it: (§10.2).
- Nothing else changed. Existing check numbers are unchanged.

## 1. Ask before building

On every new input, ask at most 5 multiple-choice questions, then start. The only exception is when the user explicitly asks for more.

- Ask only what affects structure: output type, exam board / year / syllabus / unit, the §2 parameters, existing material, length, and whether diagrams are needed.
- Decide wording and detail yourself, stating the assumption in one sentence at the start.
- If the named exam system does not match the uploaded material, ask. The material is usually right, but the marking language and the Core/Extended split depend on the answer.
- Check a syllabus claim against the material before building on it. Whether a formula is examined is answerable from the question pack itself — OCR it and look — and the answer changes what gets drilled. "It comes up at AS" is a guess until a paper shows it.
- An unanswered question takes its default (§2), and the delivery note says so.

Triggers: Handout / Notes → §4; slides / PPT → §5; homework / answers → §6; classwork → §6.5; handout + slides → §7.

## 2. Scenario parameters

| Parameter | Values | Affects |
|---|---|---|
| Teaching mode | slide-led, fixed (the tutor has no whiteboard) | the slides carry all teaching |
| Viewing distance | far (TV, back row) / near (one-to-one on a tablet, self-study) | font floor, content per slide |
| Student activity | handwriting on printed sheets / following the screen / self-study after class | handout printing, pace |
| Language | English (Cambridge) / English screen + Chinese notes / bilingual / mainly Chinese | everything, notes included |
| Depth | first contact / consolidation / exam sprint | depth, how much derivation to keep |
| Tutor's subject background | specialist / non-specialist | non-specialist adds a Chinese-screen deck (§5.9) |

Defaults (say when used): far / printed handout / English / consolidation. Materials are always handed out in the lesson and collected at the end. Anything the student writes goes on a printed sheet.

**English screen + Chinese notes.** Every student-facing output (the slides on screen, handouts, sheets, answer files) is English, because the exam is English. Only the tutor's `\note{}` text is Chinese, under the rules in §5.6.

## 3. Global non-negotiables

### 3.1 Honesty about sources

Student-facing output carries no provenance labels: no paper codes, no exam-style or past paper tags, no provenance headers. The tutor keeps the question-to-source mapping outside the deliverables, in the delivery note. Claims made in that mapping, and in answer-file labels, follow three tiers:

| Tier | Source | May be claimed |
|---|---|---|
| 1 | Official past paper / mark scheme | real exam question / real mark scheme |
| 2 | Traceable third party (PMT, publisher workbook) | exam-style material from that publisher; never an exam-board source |
| 3 | Own question / own working | tutor's own; never a mark scheme |

- Never invent a citation, session code or past-paper source. A code not read directly from the material is not recorded. Guessing which of several codes on a page belongs to which question is inventing.
- Two labels always stay, because they protect the student.
  - Tutor's working is marked "tutor's working, not an official mark scheme".
  - Official mark-scheme extracts are marked as such, and are never called tutor's working.
- Untraceable lost-mark points: if they cannot be traced to an examiner report, the page says they come from the material plus teaching observation.
- A student's own marked script (a returned test) is used only as a source of lost-mark points and of errors to rewrite for Spot the error (§5.7). His name, his handwriting and the verbatim questions never appear in a deliverable.

### 3.2 Real mathematical typesetting

- Fractions are stacked (`\dfrac`), never slashed. d/t, Ns/Np and Vp/Vs are forbidden, turns ratios included.
- Powers are real superscripts (`^{}`), never a ^ character or Unicode ² ³.
- Chemistry uses real sub- and superscripts: `\ch{}` in text, `\chm{}` in maths.
- These apply to every output, PPTX notes included (§5.6).
- Unit tokens are the only allowed slash: m/s, cm/s, J/kg inside `\mathrm{}`, whitelisted by checks 4 and 11. Every other slash between two symbols is a wrong fraction.
- Formulae are typeset in LaTeX, never pasted as images. A full-page slide image in the PPTX is fine, since XeLaTeX typeset it (§9.2).
- Symbols are correct (f′, v_w, λ′, θ, ω, µm), notation is consistent, and nothing is approximated in ASCII.
- Round only at the end, especially with small denominators or small differences.
- Deliberately wrong work inside `\flawed{}` is exempt (§5.7).

### 3.3 Layout safety

- Emphasis that may exceed half a line is bold. `\colorbox`, beamercolorbox and shading cannot break and run out of the text block, so reserve boxes for short terms.
- A display formula is 2–3 line heights; too tall shows up as Overfull \vbox.
- The fix order is always delete → move → split.
  - Slides never shrink text (§5.4).
  - Handouts may trim slightly above the readable minimum; record it in the delivery note.
  - Chasing the figure size is not one of the three fixes. Shrinking a picture by 10% at a time to clear an overflow converges slowly and costs more compiles than deleting the sentence the figure already says.
- Bracket a `\dfrac` with `\Bigl(...\Bigr)`, not `\left(...\right)`, which is about 9 pt taller — enough to overflow a page.
- In TikZ nodes and answer boxes, start every `\vtop` or paragraph with `\leavevmode` before any `\color`. Otherwise the colour whatsit becomes the first item and the text drops onto the rule below.
- A length passed into a box macro is re-evaluated inside the box. With #1 = 0.44\textwidth, `\begin{minipage}{#1}\includegraphics[width=#1]` gives 0.44 × 0.44.
  - Store the length in a `\newlength` before opening the box.
  - Nothing warns about this (§10.3.7).
- A TikZ picture beside text in a [t] minipage needs `baseline=(current bounding box.north)`. Otherwise its bottom aligns with the first text line and the text drops by the picture's height.
- A narrow column is set ragged right. Justified text in a 0.34-width minipage stretches inter-word spaces into gaps ("Why does it bend?") and hyphenates technical words. On printed sheets, set `\emergencystretch` instead of ragging the whole sheet.
- Nothing that prints carries a solid dark fill: handouts, homework, classwork, practice sets, answer files, and slides (printed 2-up, §5.5). Materials are printed for every lesson, and a dark bar is pure toner.
  - Section headings are bold text over a rule of at most 1 pt. Boxes are an outline, with a fill no darker than about 10% grey. White text is then never needed.
  - Set this in the heading and box macros (docstyle.sty, slidestyle.sty), never per page; check 1d confirms it.
  - Scans, photos and crops are outside the rule. A figure that genuinely needs a dark area is whitelisted in check 1d by page, with the reason in the delivery note.
  - An old PDF with no source may be fixed in place by rewriting its content stream (dark fill → rule or outline, white text → black). Record it in the delivery note; the macro still gets fixed before the next compile.

### 3.4 Figures must be real

- Coordinates are computed, never placed by eye.
  - Points on a circle come from the radius.
  - A rolling object is offset one radius along the slope normal.
  - Arrow ends sit on the target's boundary or centre, and the text says which.
  - Label lines start on the part they name; the point is computed from the part's geometry and the computation is written as a comment beside the macro (e.g. funnel wall at y=3.1: x = -(0.1+0.6923*0.6)). Labels on one side are at least one text height apart.
- Draw only what is physically true. A critical-angle panel draws the refracted ray only when n sin i < 1. A lens figure computes the image from u and f. A Bunsen flame stops below the gauze; a thermometer bulb does not touch the beaker.
- A figure with a singular case must not evaluate it. At u = f a lens has no image and 1/f − 1/u is zero. pgfmath's ifthenelse evaluates both branches, so guarding the result still divides by zero; guard the denominator (`\den + ifthenelse(abs(\den)<0.02, 1, 0)`) and suppress the drawing with `\ifdim`.
- A `\clip` lives inside a scope. An unscoped clip also clips every node drawn after it, including the caption, and nothing warns — the caption simply disappears.
- Labels inside a small figure collide, because the type does not shrink with the drawing. At `\figunit` = 0.44cm a 15 pt word is about two drawing units wide. Place medium labels outside the construction, not in the gaps between rays, and check the render.
- Every figure is printable in black and white, fully labelled, and serves exactly one section.
- A figure the student must measure (a ruler reading, a line to measure for magnification, a ray-construction grid) is drawn in TikZ at true size, and the sheet says "print at 100%". Where possible the ruler is drawn beside the line, so a scaled print still gives the right reading.
- Existing figures are cropped, not redrawn (§3.7), unless the crop's text would be unreadable at the target size.
  - Then re-typeset tables in LaTeX, and redraw simple line figures (number lines, grids, Periodic Table sections) in TikZ with identical wording.
  - Photos, 3-D models and complex drawings stay as crops, cut cell by cell if needed.
  - Note "re-typeset" / "re-drawn" in the delivery note.
- Deliberately wrong figures inside `\flawed{}` are exempt from "draw only what is true" and nothing else (§5.7).

### 3.5 Other

- No emoji.
- English outputs contain no Chinese anywhere, notes included, unless the language parameter says otherwise. Under English screen + Chinese notes, Chinese may appear only inside `\note{}` (and so in the notes pane, presenter view and the notes half of the PDF) and in the delivery note; a Chinese character on screen, on a sheet or in an answer file is still a failure. Full-width brackets such as 【】 count as Chinese: they also lack a glyph in the TeX Gyre fonts.
- Bold only the words that score marks.
- Every page carries Dr. Ryan Lei · Auckland in a light weight at the page edge.

### 3.6 Delivery baseline

The compile log is the authority; an uncompiled .tex is a draft. Before delivery, compile and read every .log:

- Overfull \hbox and Overfull \vbox are both 0;
- no missing-font or missing-glyph warnings;
- every pdffonts emb entry is yes;
- check 1d finds no solid dark fill.

Slides also run the PPTX export and §10.2 items 7–11.

Eyes are used only in two places:

- Every figure, individually: crop edges, coordinates on lines, complete labels. Logs cannot see these, so use a contact sheet.
- Spot-checked pages: the first page of each layout type, every formula-box page, every scanned or cropped page, every two-column page, every Spot the error page, and every page of a red-answer overlay (§6.2).

A page the compiler did not warn about has passed. If an accident gets past the log, fix the macro (§10.4); never return to page-by-page reading.

Deliverables every round: complete compilable .tex files; new or changed fig/*.png; compiled .pdfs; slides.pptx; .sty files only if changed, with a note; build.sh. The delivery note is in §10.1.

### 3.7 Material uploaded by the user

All uploaded material may be used directly: handouts, worksheets, questions, answers and mark schemes, images. Question text may go on screen word for word, and figures may be cropped straight out. No permission is needed, and nothing is reworded to avoid copying.

**Exception — the student's own test or exam.** When the upload is a paper the student has already sat, questions are rewritten (new context, new numbers) so that he does not meet the same item again; figures may still be reused as crops. The tutor-side mapping (new question → original item) goes in the delivery note.

**Ask for PDF, not screenshots** — answers and mark schemes too.

- The text layer gives exact superscripts, minus signs and root indices (e.g. (16/81)^(-5/4)); a screenshot forces guessing, and one misread minus ruins a question.
- Figures extract losslessly (pdfimages) or render sharply at high DPI.
- Page numbers make Notes p.4 footers work.
- Notes are transcribed from the text layer (§5.6).

A separate image is justified only for ① a photo of handwriting or a whiteboard, or ② a specific crop that is wanted exactly.

**OCR the question packs once, at the start.** A pack whose questions are images has no searchable text, so every decision about it — which questions exist, which are tagged extended, whether a formula is ever examined — is guesswork until it is OCR'd. One pass at 150 dpi over the topic's packs gives a searchable corpus for selection, for the Core/Extended split, and for answering syllabus questions from evidence. It takes a few minutes and is reusable for the whole unit.

**Figures embedded in a notes PDF**

- Render the page clipped to the image rectangle (`get_image_rects` → `get_pixmap(dpi=…, clip=…)`), not the raw image object. Clipping composites soft masks and gives a white background.
- Pixel-scan to trim the border to about 5 px.
- Image rectangles can overlap by a few points, so a clip may pick up the tail of the figure above (a watermark line, caption or stray band). Trim a fixed fraction off that edge and confirm on the contact sheet.

**Phone photos of a marked paper** (the usual form of a returned test)

- Crop from the full-resolution page image, never from a thumbnail.
- Push the off-white paper to white only where it is unsaturated. Keep coloured and dark pixels, so the figure survives while show-through handwriting from the back of the page goes.
- Remove pen lines crossing a figure by fitting the line per object and inpainting a band around it (`cv2.inpaint`). Check the result on the contact sheet; a faint seam is acceptable, and a missed line is not.
- Never crop the student's own marks or the marker's red ink into a figure.

**Scanned pages are normalised first:**

1. Extract losslessly (`pdfimages -png`).
2. Split spreads into single pages.
3. Deskew on the footer bar. The widest dark band is usually the scanner edge, so take the uppermost thick band that does not touch the half-page border.
4. Anchor on the bar's outer end.
5. Remove gutter shadow and scanner borders in the margin strips only.

Check one contact sheet before placing anything.

**Question packs whose questions are images** (e.g. PMT topic packs)

- The text layer holds only pack numbers and paper codes, each code after its question. That ordering is an inference, so codes are never transcribed into a deliverable.
- Numbers can merge ("85" = Q8 + hidden original 5), and digits can be look-alike Greek glyphs (Q1ϲ. = Q16.).
  - Check the sequence, and list start positions by hand where it breaks.
  - A label may be split across spans, so read the line, not the span.
- Never composite by bounding box: the images overlap and rely on clipping (A.4). Strip the text operators (BT…ET, e.g. with pikepdf), render, and cut between consecutive question-number positions.
- Screen text is re-typeset from the image, checked word by word.
- A crop may cover only part of a question. When the wanted part starts mid-question, cut from that page's top to the next question's label, and say on the sheet which parts are missing (§5.5).

**Cropping** (subject to §3.4)

- Find edges by pixel-scanning rows and columns for dark bands, and leave about 5 px of white.
- Trim a trailing blank region by finding the last full-width rule, not by trimming white: a table that ends halfway down a page leaves a page-footer mark below it, so a white-border trim keeps the gap.
- Check that nothing at either end is cut and no stray text line crept in. Cropping by eye always clips a curve or picks up a mark.

**Slides without a handout:** the user's PDF or workbook becomes the handout, referenced by Notes p.X / WB p.X footers. Formula sheets and definitions still stay off screen.

## 4. Handouts (XeLaTeX → PDF)

An exam-aligned reference the student studies closely in the lesson.

- Density is a strength; slide font and page limits do not apply.
- One handout = one teachable unit of one syllabus topic, so that everything the test asks is on these pages. Thorough, but not a question bank.
- Printed for the student, so exact content (formula sheets, definitions, unit conversions) lives here, not on slides.
- No `\flawed{}` content. The handout carries only correct models, plus the "versions [board] won't accept" table (§4.3).

### 4.1 One complete PDF

- One file: answers, key points and full worked examples are in the body.
- No blank version, no version switch, no fill-in gaps.
- Do Now and practice questions belong to the slides, classwork and homework, not here.

### 4.2 Keyword emphasis

Scoring keywords are printed in full and emphasised by one method throughout — a box (short terms only), bold, or a light highlight. Methods are never stacked.

- Keywords, mnemonics, defined words: boxed or bold, with the answer inside.
- Diagram labels (directions, polarities, in/out): fully labelled and emphasised, e.g. Left hand: thuMb = Motion｜First = Field｜seCond = Current. No empty outlines.
- Worked examples: the Step 1 / Step 2 skeleton plus the full solution, key steps bold, no answer boxes. Marking points are tagged (MP1) at the right margin.

Density is "medium": key terms, key words in cause-and-effect chains, and worked-example scoring points. A fully highlighted page highlights nothing.

### 4.3 Techniques (choose per unit)

- **The one idea:** the unit compressed into one core idea, taught before any equation.
- **Write it in this order:** numbered answer order for explain questions, following the causal chain. Almost always include this.
- **Choosing the equation or route:** a two-second derivation plus a consistency check, instead of rote rules.
- **Question types + full worked examples:** classify first, use real arithmetic, and include a consistency check.
- **Case tables:** situation | what you see | why it scores — for the most error-prone boundaries.
- **"Versions [board] won't accept":** the wrong answer, and why it gets no credit.
- **Ways to lose marks,** numbered and taken from real reports, so marking can refer to them.
- **Sentence frames** for explain questions, with the marker's words marked.
- **Quick review pages:** the facts behind the deck's Quick review slides (§5.8), set out as compact tables (part | job, symbol | meaning | precaution), grouped by topic, after the unit's own sections. The slides point to them.

Length and columns are decided per unit.

## 5. Slides (Beamer → PDF → PPTX)

### 5.1 First principles, in order

1. Whether it belongs on a slide comes before how to place it. Content that does not fit usually moves to speech, the notes, the handout or the textbook. There is no whiteboard to move it to.
2. If the least-favoured viewer cannot read it comfortably, the slide does not exist.

### 5.2 On screen or not

**Always on screen:** slow-to-draw diagrams, question text word for word, data and photos, and Do Now.

**Explanations and derivations always go on screen** (the lesson is slide-led). They are built up across split slides, never with overlays, and never shown finished at once. Each build slide adds one step and asks one question about it; the answer is in that slide's notes. A labelled model diagram may be completed on the last build slide, because the drawing is the content being taught.

- A derivation the student is expected to reproduce gets one slide per step. Three is the usual number: set up the geometry, do the one cancellation, substitute. The same figure appears on each, gaining one label at a time, so the student sees what changed.
- Near-distance tablet lessons may leave empty boxes and dotted lines for the student to write on.
- Far-distance lessons give the student a printed sheet to write on. The screen shows short gaps (`\gap{}`) that he answers aloud.

**Never on screen:**

- Any answer. Answers, scoring points and error notes for every question type go in that slide's `\note{}` (§5.6). Worked examples show the method with the result blank. No exceptions.
- Copying pages. Formula sheets, definitions and conversions are in the handout; a Handout p.X / WB p.X / Notes p.X footer points back. No "PLEASE TAKE NOTES" or yellow pages.
- Dense handout text. Slides carry trigger words, or a skeleton plus one sentence.

**Other rules:**

- Do not pre-convert word problems to symbols (no d = 50 m). Students must practise reading the stem; demonstrate the extraction in `\note{}`.
- Data printed in a stem (e.g. n = 1.58) is not an answer.
- ABCD cards only for whole-class teaching with 8–10 or more questions.

A deck is usable only where its notes can be shown (§9).

### 5.3 Structure

No hard page limit. The test is "would teaching get worse without this slide?" — never a textbook chapter moved onto slides.

```
Do Now (concept diagnostic, answers in notes)
→ the one idea
→ for each teachable point: Quick review of the facts it rests on (optional, §5.8)
    → explanation (built across split slides)
    → Spot the error (optional, §5.7) → workbook/source task if any
→ after each group of points: one slide of 2–3 original questions (§5.5)
→ Classwork slide (if a classwork sheet is set, §6.5)
→ past-paper run: any number of slides, contiguous (§5.5, optional)
→ ways to lose marks → Summary → homework page
```

- Every unit has a Do Now.
  - Its notes add Diagnostic: (what a wrong answer reveals).
  - Review with the question on screen while the student self-corrects.
  - It tests the previous lesson or this lesson's prerequisites — ask which (§1).
- Each lesson has one lose-marks slide, with the 4–6 most common points.
- A multi-lesson deck opens each lesson with a divider slide (e.g. LESSON 2 · Nodal Lines) carrying its learning intention.
- A 90-minute slide-led lesson runs to roughly 45 slides once derivations are built step by step and a classwork sheet takes a quarter of the time. A topic that needs more than that is two lessons; say so before building rather than compressing the builds.

### 5.4 Minimum font sizes

aspectratio=169, paper 170mm × 95.625mm, 5 mm margins → a 160 mm text block. Beamer's own 16:9 paper is only 160 mm wide.

Generic Beamer body sizes are invalid; this table governs. The PPTX is a full-page image, so it matches the PDF.

| Page type | Far | Near |
|---|---|---|
| Diagram / question / data | ≥ 15 pt | ≥ 9.5 pt |
| ABCD page | stem 17 / options 15 | stem 11.5 / options 9.5 |
| Sub-parts (a)(b)(c) | ≥ 14 pt | ≥ 9.5 pt |
| Summary | ≥ 15 pt (≤ 4 lines) | ≥ 10.5 pt |
| Title | 21 pt | ≥ 14 pt |
| Emphasis | 19 pt | ≥ 11.5 pt |
| Handwriting (Sam's work, §5.7) | 17 pt | ≥ 11.5 pt |

Floor: 13 pt far / 8.5 pt near. The handwriting face is narrow, so it sits 2 pt above the body size.

- Only footers, page numbers and routine prompts (e.g. WB p.6) may be 8 pt, never lower.
- Past-paper screenshots, workbook crops and notes are outside the table.

**Size is a property of a macro, not a check.**

- All text goes through the .sty size macros: title, emphasis, question, body, sub-part, handwriting, workbook text, footer. `\normalsize` itself is redefined to the body size, so TikZ labels and table cells inherit it.
- Banned in slides.tex, TikZ `font=` options included: raw `\fontsize`, `\small`, `\footnotesize`, `\scriptsize`, `\tiny`, `\resizebox` on text, `[shrink]`, `allowframebreaks`.
- A page below the floor should be impossible to write. A label that does not fit at 14 pt gets shortened.

**Shrink the drawing unit, not the picture.**

- `\scalebox` silently takes the labels below the floor.
- Draw every figure in a `\figunit` length and shrink that: the geometry shrinks, the type does not.
- An `\includegraphics` image may be resized; its caption may not.

**Formula glyphs must pass too.** A superscript is about 70% of its base, and a fraction inside a superscript about 49%.

- A fraction in an exponent ((16/81)^(-5/4)) needs a ≥ 18 pt base, in the formula-box macro, never inline.
- A single-level superscript needs ≥ 13 pt.
- A display fraction in a narrow column is the usual cause of an overflowing two-column slide. Two of them in a 0.34-width minipage are five line heights. Move them to a full-width formula box below the figure.

Mark allocations use `\smk{n}` (flush right, drops to a new line only when it must, then still flush right). Never `\hfill[n]`.

Bold may replace enlargement, not deletion — at most two places per slide (§4.2).

**If it does not fit:** delete → move → split → two columns (at most). Never shrink text.

- A non-zero Overfull means not delivered.
- Images and tables may be resized; text may not.
- What must be seen together stays on one slide: Do Now, or a single question's full stem.
- Last resort: cut modifiers and connectives — never the question's wording, numbers, units or named context.

### 5.5 Practice questions

**Original questions** ("can I do it"). After each point or small group of points, one slide of two or three — two when a question has a figure or a long stem. The stem is exact, data and figures are complete, and there are no answer boxes.

- Content: cover the most tested points and the easiest-to-confuse traps.
- Honesty: never fake a past-paper citation, and add no source label (§3.1).
- Command words (§8): explain → causal chain; calculate → steps with units; NCEA → M/E; CAIE → M/A split; school papers marked point by point → MP1/MP2.
- Never split a set across slides. Cut modifiers first, then drop to two questions.
- No repeats with the same numbers anywhere in the unit (workbook, homework, classwork, past papers, Do Now, handout worked examples). Change the substance or the numbers. A worked example on a build slide counts: reusing its numbers in the practice set two slides later teaches recall, not method.

**Past-paper questions** ("what the exam looks like"; only if supplied). They come after the originals, one per slide, exactly as printed — stem, figure and options unchanged, not rearranged, not supplemented.

- Screenshots, re-typeset only if the crop would fall below the floor (§3.4).
- Any number of slides, in one contiguous run, so they print as one page range. Printed form: 2-up on A4, cut into half-pages. A natural order is MCQs first, then structured questions.
- Structured questions: screen plus a printed set.
  - A full Paper 3/4 question is roughly A4 portrait. On a 16:9 slide it fills about half the width, so a half-page print shows it at about 60% of natural size — too small to write on. MCQ crops print fine at half-page.
  - The question stays on screen, exactly as printed, for discussion.
  - The readable copy is the printed practice set at natural size (§6.3).
  - Record the split in the delivery note.
- Answer-line whitespace may be compressed, for both uses.
  - Classify each pixel row as content or space; a dotted rule counts as space (sparse ink, many light/dark transitions).
  - Cap every run of space — hard on screen; on paper, at the largest cap that still fits one A4 page, so the student keeps room to write.
  - Nothing of the question is removed.
- Codes are read, never guessed, never printed.
- At far distance, fit decides selection. At 17/15 pt only short items fit, since the wording may not be cut.
  - Long options, long-header tables and a figure plus a long stem move to the printed set; list every swap in the delivery note.
  - When only some parts of a structured question are shown, the footer says which are missing.
- Question-slide titles are neutral: Do Now, Practice, MCQ, Workbook, Spot the error (k), Classwork, Quick review: <topic>. Nothing on screen says "past paper" or names a paper.
- A student's own sat paper is never a past-paper run; its items are rewritten (§3.7).

No past papers supplied → none included. Never invent them, and never present originals as past papers.

The deck always ends with a homework page. Do Now (the unit-start diagnostic) and these questions (consolidation) never repeat each other.

### 5.6 Notes (`\note{}` → PPTX notes pane, tutor only)

Notes are exempt from §5.4 and from density limits, and follow the language parameter (English by default; Chinese prose under English screen + Chinese notes, see below).

**The standard:** at the lectern, I find the line I need within two seconds.

- Text and formulae only; no images — the notes pane and presenter view do not show them (A.1).
- Uploaded answers and mark schemes are transcribed, not cropped. Take values from the PDF text layer, then check each against the original.
- Re-set the working (maths per §3.2) when the original is unreadable, gives only final answers where steps are needed, or must match the lost-mark numbering (L1/L2…).
- A question that needs its figure: the figure is on screen; the notes say where to look.
- Tutor-side source mapping stays out of the notes (§3.1): no paper names or question numbers of the original.

**Fixed format, in this order, never one paragraph:**

```
(a) answer
(b) answer
Short solution:
(a) key step
(b) key step
Watch for:
common mistakes and reminders
Diagnostic:            ← Do Now only
what a wrong answer reveals
Script:                ← Chinese notes only, every slide
the read-aloud script, in teaching order
Say it:                ← optional, always last
anomalous = uh-NOM-uh-lus
```

- Answers come first, with no header: one sub-part per line, label first. MCQs take one line each (Q7  B). Multi-question slides label lines Q1 (a), Q2. A single-question slide may use Q. Spot the error answers are numbered 1. … N. (§5.7).
- No Answer: / Answer image: / Key answer: headers; label-first lines are what make the two-second rule work.
- Short solution: also takes one sub-part per line, with scoring steps only.
- Several questions on one slide: either all answers first, then one shared Short solution: / Watch for:; or grouped by question in the order above, with a blank line between groups.
- No Source: line. A non-question slide may open with `Teaching line, not a question slide.` — including one whose title carries a question keyword, such as the Classwork slide.

**Say it: — pronunciation of hard words**

- Purpose: the tutor reads the word aloud correctly the first time the student meets it.
- Format: one word per line, word = say-it.
  - Syllables are joined by hyphens, and the stressed syllable is in capitals: cartilage = KAR-tih-lij, Daphnia = DAF-nee-uh, Mereana = meh-reh-AH-nah.
  - ASCII only. 【】 is full-width, which breaks §3.5 and has no glyph in the fonts. Two spaces collapse on the PDF note page, so the separator is =.
- Which words: only hard ones:
  - three or more syllables with a non-obvious stress;
  - Latin or Greek scientific terms;
  - Māori words and names;
  - names whose spelling misleads (Achilles = uh-KIL-eez).
  - Not everyday words.
- Once per deck: only in the notes of the slide where the tutor first says the word — the first slide that uses it on screen or in its notes, counting inflected forms: a title slide listing "Dispersion" is the tutor saying it, and "endoscopes" is the tutor saying "endoscope". Words the student meets first in the homework go on the homework slide's notes.
- Always the last label. A teaching slide may carry only `Teaching line, not a question slide.` and a Say it: block.
- Checks 10 and 13 audit it.

**Chinese notes (language = English screen + Chinese notes)**

- **Where they live.** In `\note{}`, which the exporter puts in the PPTX notes pane; they therefore also show in presenter view and on the right half of the double-width slides.pdf. Never in a separate .md file, lesson script or Word document. One source keeps the notes aligned with the slides; a second copy drifts. The delivery note (.md) holds the tutor-side mapping and timetable, not the notes.
- **Prose is Chinese:** explanations, timing, what to ask, Short solution: reasoning, Watch for: and Diagnostic:.
- **Every scientific term stays English** and is never translated: 叶片背面的 stomata 在晚上关闭, not 气孔. The student must write the English term in the exam, so the tutor says the same word she will write. No Chinese gloss stands in for a term.
- **Also English:** command words (describe, explain, compare, evaluate), units, equations and word equations, and anything quoted from the screen.
- **Answer lines are English,** written exactly as the student should write them, because they are what scores. The Short solution: steps may wrap English terms in Chinese prose.
- **Label lines keep their English form exactly** (Short solution:, Watch for:, Diagnostic:, Say it:, `Teaching line, not a question slide.`), so checks 10 and 13 work unchanged.
- **Say it: is not optional for hard words** under Chinese notes. Every hard term (rules above) gets one line at its first say, still in ASCII.
- **Punctuation:** Chinese prose may use Chinese punctuation (，。：“”), but never full-width brackets 【】 or （）; use ASCII parentheses (§3.5).
- **Script: (every slide).** After Diagnostic: and before Say it:, a script the tutor reads aloud in teaching order, one action per line: what to say (说：), what to ask (问：/ 念第 n 题), the expected answer (她应答：) in the English she should give, and what to say if she is wrong. Mixed Chinese and English; science terms stay English and may carry a Chinese gloss in ASCII parentheses the first time they appear in the deck, e.g. stomata (气孔). It is written for a tutor who is not a subject specialist: it never assumes the tutor knows the answer. On a teaching slide it follows the Chinese teaching lines.

```latex
\note{%
(a) stomata\par
(b) guard cells\par
Short solution:\par
(a) 气体交换发生在叶片背面的 stomata：\chm{CO2} 进，\chm{O2} 和 water vapour 出\par
(b) 两个 guard cells 吸水变 turgid，stomata 张开\par
Watch for:\par
(a) 拼写：stomata 是复数，单数是 stoma\par
(b) 只写 “they open” 只能拿 A；要拿 M 必须说明是 guard cells 的形状变化\par
Say it:\par
stomata = STOH-muh-tuh}
```

**Maths becomes native PowerPoint equations (§9.2).**

- Write `$\dfrac{N_s}{N_p}$`, `$x^{2}$`, `$\chm{H2O}$` as usual.
- Verified September 2026 (Microsoft 365, Windows and Mac): the notes pane and presenter view both show them.
- The linear fallback appears only in software without equation support, and does not break §3.2.
- Prose slashes: spaced ones ("C / N / O") are allowed; unspaced ones are not — write "dense to less dense".

**Source syntax.** One line per paragraph, separated by `\par`. Label lines are exactly Short solution:, Watch for:, Diagnostic:, Say it:. Beamer's note page and the PPTX pane both split at `\par`. Project macros used in notes (`\Lref{}`, term macros, `\um`) are expanded by the exporter, which reads their definitions from shared.sty (§9.2).

```latex
\note{%
(a) $\dfrac{243}{32}$\par
(b) $11.5\ \mathrm{V}$\par
Short solution:\par
(a) $\Bigl(\dfrac{16}{81}\Bigr)^{-\frac{5}{4}}
     = \Bigl(\dfrac{81}{16}\Bigr)^{\frac{5}{4}}
     = \Bigl(\dfrac{3}{2}\Bigr)^{5}$\par
(b) $V_s = V_p \times \dfrac{N_s}{N_p} = 230 \times \dfrac{20}{400}$\par
Watch for:\par
(a) take the reciprocal first for a negative power; an answer below 1 means the sign was ignored\par
(b) inverting the turns ratio gives 4600 V\par
Say it:\par
reciprocal = rih-SIP-ruh-kul}
```

- Quotes in notes are typographic (“ ”), not `` '', because notes export as text.
- Notes are real text in both the PDF and the PPTX, so check 3 scans only outside `\note{}`.

### 5.7 Spot the error

The student hunts for planted mistakes in a fictional student's work. For each one he must find it, fix it, and say why it loses marks. This turns lost-mark points into something he recognises in other people's work before he meets them in his own.

**Source of the errors**

- Every planted error is a lost-mark point from this unit's L-list (§4.3). The answer names its L-number. Invented slips that match nothing in the list are not used.
- Mix two sources: the student's real errors, rewritten into a new question and context, and common errors for the topic. Never use the real student's name, his handwriting scan or the verbatim original question (§3.1, §3.7).
- Sam's conclusion may happen to be right while his reasoning is wrong. That version is worth setting deliberately: it forces the student to mark the working, not the verdict.

**Form**

- The fictional student is "Sam", the same name in every file.
- Sam's text is set in the handwriting font (fonts/PatrickHand-Regular.ttf, OFL) inside `\flawed{}`, in a samcard box titled "Sam's answer".
- Sam's drawings are TikZ inside `\flawed{}`, in the pencil grey, with handwritten labels.
- Nothing Sam writes may look like a model answer.
- The stem states the count: "Sam's answer has N errors." The task line is: find each one, fix it, and say why it loses marks.
- Nothing on screen marks the errors: no circles, no colour, no arrows. The answers go in the notes as numbered lines 1. … N., each ending with its L-number. Then come Short solution: (the model answer, or the fix) and Watch for:.
- Placement: after the teaching point it tests and before that point's practice. At most one per teaching point. Title: Spot the error (k).
- Size (far): Sam's text is 17 pt (§5.4). A Sam drawing uses `\figunit` like any figure.

**Exemptions and limits**

- `\flawed{}` content is exempt from §3.2 (slash fractions, fake superscripts), from "draw only what is true" in §3.4, and from checks 3 and 4. It has no other exemptions.
- It is not exempt from check 1d. A "shaded" error is drawn as light grey hatching (pattern=north east lines, grey), never as a solid fill.
- The handwriting font lacks µ and →. Use `\samu` for µ, or avoid the symbol; a missing glyph is a check 2 failure.
- `\flawed{}` may appear only on a Spot the error slide or in a sheet item that states "N errors" (check 12). It never appears in a handout (§4).

On sheets (§6.4): same form. The item is worth N marks, and the answer version lists each error, its fix and its L-number.

### 5.8 Quick review

Content the student met earlier (last term, or a test he has already sat) is revisited rather than assumed. Scoring on it once is not the same as keeping it.

- **Form:** a slide titled Quick review: <topic>, with 3–6 short items the student answers aloud:
  - fill a gap;
  - match;
  - name the lettered parts of a figure;
  - true or false;
  - put steps in order;
  - a one-line calculation.
- **No teaching on the slide.** If an item needs explaining, the explanation goes in the notes, and the full fact is on the handout's quick review page (footer Handout p.X).
- **Placement:** interleaved next to the teaching point it supports, never all at the start. For example, hazard symbols go before the hazard-symbol explanation, and muscle pairs before the tendon Spot the error.
- **Sources:** every topic on the student's past papers that the lesson does not otherwise teach. Items whose answer he got wrong come first; the notes' Watch for: names that trap without citing the paper (§3.1). When no past paper is available, the source is the parts of the same syllabus topic the lesson deliberately does not cover — say so in the delivery note.
- **Figures** are reused crops or shared TikZ macros, labelled with large letters (A–F) typeset over or beside the figure. Small printed letters in a crop are cut off and replaced, because they fall below the floor at far distance.
- **Notes:** label-first answers, as for any question slide (check 10), with Short solution: and Watch for: when useful, and Say it: for hard words.
- **Pace:** 60–90 seconds each. If the lesson runs long, the last Quick reviews move to the start of the next lesson. They are never cut from the homework, which carries a short quick-review section on the same topics with new items.
- **No repeats:** homework quick-review items ask the same facts in a new form (a patient's symptom rather than a part's job), never the slide's wording.

### 5.9 Chinese-screen deck (non-specialist tutor)

When the tutor is not a specialist in the subject, the English deck comes with slides_zh.pptx (and slides_zh.pdf): the same deck with the screen in Chinese. It is for the tutor to prepare from and may be shown to the student; the exam stays English, so the English deck remains the teaching default.

- **Page for page.** Same frames in the same order, same figures, same gaps, same layout rules (§5.4 sizes, no answers on screen, split slides).
- **Wording.** Sentences in Chinese. Every science term stays in English with the Chinese in brackets, e.g. stigma（柱头）, at least the first time it appears on each slide where it matters; in tables, the English term and the Chinese side by side. Sam's work in Spot the error stays in English, because the student marks English answers.
- **Figure labels** switch to Chinese through `\zhdecktrue` and the `\zhen{中文}{English}` macro in shared.sty; lettered labels (A–H) stay letters.
- **One source for the notes.** The Chinese screens live in slides_zh_frames.tex, one block per frame (`%%% FRAME n {title}`). tools/build_zh_deck.py joins each block with that frame's `\note{}` from slides.tex to write slides_zh.tex, so the notes are typed once and are identical in both decks (check 7z).
- **No separate prep book.** A book laid out differently from the deck is harder to follow than the deck itself; do not add one unless asked.
- **Teacher PDF (slides_teacher.pdf).** Each frame block in slides_zh_frames.tex carries `\answers{...}`: short answers to every gap and question on that slide, in the English the student should give, with brief Chinese where it helps; on slides with no question, one line on what to do. `\answers` typesets nothing on a slide. tools/build_teacher.py writes teacher_pages.tex, one page per slide: page k of slides_zh_screen.pdf at 0.63 of the width, framed, and the answers below in bold red in a fixed-height `\vbox` (an answer that does not fit reports Overfull \vbox). build_teacher.sh joins slides_screen.pdf (left) and teacher_pages.pdf (right) into slides_teacher.pdf, presented like slides.pdf (§9.2): the left half goes to the projector.
- **Say it on the teacher page.** The Say it: lines are read from the slide's own `\note{}` in slides.tex, never retyped. A slide with hard words uses layout B: Chinese slide at 0.60 of the width with the red answers below it on the left, and on the right a full-height blue column headed "Say it 读音", one word per entry: the word in bold, its pronunciation unbroken (`\mbox`) on the next line. A pronunciation too wide for the column reports Overfull \hbox. A slide without hard words keeps layout A (slide 0.63 wide, answers full width). The two columns are `\vtop`s top-aligned at height 0; the divider rule hangs below the baseline (`height0pt depth86mm`), or it adds its height to the page.
- Check 10s exempts this deck from "no Chinese on screen"; every other slide check runs on it.

## 6. Homework, classwork and answer files

### 6.1 Homework sheets

- One source, two outputs: hwN.pdf (blank, A4) and hwN_answers.pdf (same layout, answers in red), switched by `\def\withanswers{1}`. The layout never changes between them.
- The answer goes inside the switch: `\ifansmode\color{ansred}#1\fi`.
- Nothing answer-only may change the layout.
  - A bare `\ifansmode` block is the rule's main violation, not an exception to it. The "tutor's working, not an official mark scheme" header line was written that way and pushed a whole sheet onto an extra page. It uses `\ansnote{h}{…}`.
  - Answer-only text inside a line is `\smash`ed: the header label and red text in blanks.
  - A blank that is `\smash`ed in only one version is still a layout change. `\blank` smashes in both, because the underline's depth otherwise makes the blank version's line 1.8 pt taller.
  - Answer-only blocks (marking notes under a drawing or graph) use `\ansnote{height}{…}`, which reserves the same height in the blank version and reports Overfull \vbox if the note outgrows it.
  - Check 14 compares the two PDFs.
- `\ifansmode\color{ansred}\fi #1` prints the answer in both versions.
- Always check the blank version: scan its text for answer words, and render it to confirm there is no red outside the photos.
- Figures the student reads stay black in the answer version (a ruler, a question diagram). Only answer drawings use the red apparatus colour.
- Answers sit on dotted lines, in short blanks, or in drawing boxes (red diagrams via the shared TikZ macros).
- Two pitches:
  - `\lines` / `\al`: 9 mm, with the baseline 1.2 mm above the rule, for plain text.
  - `\flines` / `\af`: 18 mm, with the baseline 6 mm above the rule, for a stacked fraction or a displayed superscript (§3.3). A fraction on `\lines` puts its denominator through the rule, and nothing warns (check 4). `\sin^{-1}` counts as a displayed superscript.
  - Each block is a `\vbox` to n × pitch, so an outgrown answer reports Overfull \vbox instead of printing through the rule.
- A drawing prompt and its box share a page; force a break if needed.
- Header: title, syllabus, time, total marks. The answer version adds "tutor's working, not an official mark scheme" through `\ansnote`.
- Marks and length: [n] at the right margin; length about one mark per minute plus reading time; extension items labelled Extension.
- Drawing and graph items print their marking points in red under the box in the answer version.
- Footer: lists any workbook Practice/Challenge tasks also set.

### 6.2 Red answers on scanned workbook pages

- Never place by eye. Start from the normalised pages (§3.7). Detect dotted lines, table rules and underscores in the image, and snap answers to them. Labelled 100 px grid views only match features to questions.
- Answers are TikZ nodes in page-pixel coordinates over the image (vector red text, not burned into pixels). Diagrams use the shared macros.
- Check every page after rendering: nothing crosses printed text, and diagrams fit their cells. Adjust diagram scale; never set text below 7.5 pt.
- Each page carries "Tutor's working, not an official mark scheme · Dr. Ryan Lei · Auckland".
- Graphs: state the scale, plot every point, circle agreed anomalies, and say how the line was drawn (e.g. "through (0,0) using the theoretical ratio").
- Delivery: one PDF — workbook pages first, then the homework answer versions.

### 6.3 Past-paper practice and homework sets

- Questions are cropped (§3.7) and printed at natural size (about 165 mm wide for A4), with answer spaces kept. This is the readable copy of anything too small on screen.
- Each structured question and each section heading starts a new page; MCQs may share a page.
- One question per page: search downward for the largest whitespace cap (§5.5) that keeps the question under one page at natural width. Never shrink the question.
- Separate answer file, if asked: built from the same source via `\withanswers`.
  - MCQ letters in red, from the answer-key PDF.
  - Official mark-scheme rows cropped under a red heading per question, cut between the scheme's own question labels, with text operators stripped first (§3.7).
  - Labelled as official mark-scheme extracts, never tutor's working.
  - This is the one sheet whose answer version legitimately has more pages than the blank. Check 14 identifies the mark-scheme pages and drops them before comparing; it never relaxes the rule for any other pair.
- No item repeats across slides, classwork, practice set and homework.

### 6.4 Spot the error on sheets

- The same rules as §5.7. The item states "Sam's answer has N errors" (or "drawing", "chart") in bold, and is worth N marks.
- The answer lines hold 1. … N., each with its fix and `\Lref{}`. Check 12 compares the stated count with the numbering.

### 6.5 Classwork sheets (in-class work)

- The printed task the student does in the lesson, about a quarter of the lesson's time. It is built like homework: classwork.tex → classwork.pdf + classwork_answers.pdf via `\withanswers`.
- No time is printed on a classwork sheet, neither in the header nor per item. The header shows title, subtitle and total marks only.
- It practises the lesson's main points with new items, and ends with at least one extended task (a method, a diagram or a graph) that needs paper.
- A sheet carrying a true-size figure says "print this sheet at 100%" in its header (§3.4).
- The deck has one Classwork slide listing the sheet's sections. Its notes summarise the key answers and name the answer file, and open with `Teaching line, not a question slide.`
- No repeats with slides, handout worked examples or homework (§5.5).

## 7. Paired handout + slides

The handout is made first and is the content source; the slides are its projected index.

| | Handout | Slides |
|---|---|---|
| Role | content source, close reading | prompts, pace, focus, step-by-step builds |
| Density | complete | one idea per slide |
| Worked examples | full solution + M/A (or MP) marks | stem + step skeleton, built across split slides |
| Formula sheet / definitions / conversions | printed in full | not shown; Handout p.X footer |
| Lost-mark points | full numbered list | 4–6 most common |
| Do Now | no | yes |
| Spot the error | no | yes (§5.7) |
| Practice questions | no | 2–3 original per group; past papers if supplied |
| Answers | in the body | in `\note{}` only |

1. **Same figures:** both point `\includegraphics` at the same fig/ file, or call the same shared.sty TikZ macro. Never copy, redraw or version it; to change it, regenerate that file or edit that macro.
2. **Shared numbering:** L1/L2… are macros defined once in shared.sty (`\defL{key}{n}{text}`, used as `\Lref{key}` / `\Ltext{key}`) by both. Nothing else may hold a second copy of them — the PPTX exporter reads them from shared.sty (§9.2).
3. Every content slide has a cross-reference footer: Handout p.X / Notes p.X / WB p.X.
4. **Identical terms:** each term is a shared.sty macro, used everywhere including TikZ nodes (split-ring commutator, never commutator ring). A sentence-start or title form of the same term is a second macro beside it (`\Tcrit` / `\TCrit`), never a hand-typed capital.
5. **No double carrying:** slide questions are original, and dense handout text stays off screen.

## 8. Exam systems

The science is the same. What changes is the identification codes, traceable sources, marking language, formula-booklet role and lost-mark points.

| Dimension | NCEA (NZQA) | CAIE / Cambridge | IB Diploma |
|---|---|---|---|
| Identification (tutor-side) | Level · AS 9152x · unit · year | IGCSE/AS/A · syllabus (0625/0653/9702) · Paper · unit · year + series | Physics SL/HL · Theme · Paper 1/2/3 · year + series |
| Traceable source | Assessment Report + Schedule | Examiner Report + Mark Scheme | Subject Report + Markscheme |
| Marking unit | holistic → N0–E8, judged A/M/E | point by point: M / A / B / C | markpoints; long answers by markbands |
| Higher grade | Merit = linked/quantified; Excellence = integrated + justified | precision + complete chain for the command term | command-term depth + data support |
| Formula booklet | Resource Booklet, partial | A Level given; IGCSE very little | data booklet, complete |
| Sig. figs | 2–3 until the last step; no "e" notation | final 2–3 sf; "show that" gives one extra | match the data; units always |
| Error carried forward | consequential error | e.c.f. | ECF / OWTTE |

**NCEA**

- Holistic: one grade per question.
- Sentence frames target M/E.
- Numerical answers need SI units + direction; convert prefixes before substituting.

**CAIE**

- Point by point. "Write it in this order" separates M from A. Notes may mark steps M1 / A1.
- Command terms set the depth; give a comparison table.
- "Show that" lists every step and gives one extra figure.
- Check Core vs Supplement against the current syllabus. If unchecked, mark borderline content Extension and say so. A PMT topic pack tags its own extended-only questions, so the split can be read from the material rather than recalled.
- Geometric optics is IGCSE-only in this board. 9702 drops lenses entirely, so "it comes up at AS" is never the reason to teach a lens formula. In 0625 the focal length is always measured off a printed grid, never calculated.
- Mixed-paper topic packs: mark each question Core (Papers 1, 3) or Extension (2, 4), and say so.

**School internal papers** (e.g. Cambridge Lower Secondary schools)

- Marked point by point by the teacher, written MP1, MP2, … on the script ("No MP2" = the second marking point is missing). Handouts and notes use the same tags.
- No public mark scheme exists. All answers are tutor's working (§3.1).

**IB**

- ⚠️ The 2023 syllabus (first exams 2025) uses themes A–E. Confirm sub-codes before starting; hard-code nothing untraceable.
- All formulae are given; exams test equation choice, reasoning chains and data.

**Off-syllabus content the user asks for.** Teach it on one slide marked Extension, and keep it out of every exercise, unless the user says otherwise. Say on the slide what the examined skill is instead. Record the decision in the delivery note.

**New system:** ① identify system, year and unit (ask if unsure) → ② record the tutor-side mapping → ③ pull traceable anchors (source of lose-marks and won't-accept) → ④ adjust marking language → ⑤ decide "memorise" vs "logic" formula page → ⑥ everything else as usual.

## 9. Implementation

Goal: the same .tex gives the same PDF and PPTX tomorrow.

XeLaTeX for everything. It loads project OpenType fonts and keeps bilingual and Chinese output possible: add a CJK font to fonts/ and a CJK-capable family for that text. Slower compiles are accepted.

- Under English screen + Chinese notes, slidestyle.sty loads xeCJK with the CJK font from fonts/ (e.g. `\setCJKmainfont[Path=fonts/]{wqy-microhei.ttc}`, and the same for `\setCJKsansfont`), so the note pages embed it (check 2). The screen pages contain no CJK text (§3.5), and the printed sheets do not load xeCJK at all.

Fonts live in fonts/, loaded by fontspec with Path=, even when installed system-wide.

- A missing font is silently replaced with different metrics. Every line break moves, and the Overfull count then describes a document you do not have.
- Defaults: TeX Gyre Heros (slides) and TeX Gyre Pagella (printed sheets) ship with TeX Live. Patrick Hand (OFL, from the google/fonts repository on GitHub) is Sam's handwriting (§5.7).
- shared.sty must not `\RequirePackage{fontspec}`. slidestyle/docstyle load mathspec, which loads fontspec with options, and loading it first without them is an option clash. Define Sam's family inside `\AtBeginDocument`, after fontspec is in place.
- Projector fonts do not matter. The PPTX screen is an image; a missing notes font changes only the notes' look.

**Maths in the text font**

- Use mathspec with `\setmathsfont(Digits,Latin)[Path=…,…]{font}`. Options go before the font name. The fontspec order `{font}[…]` makes mathspec look for a system font and fail. Beamer adds `\usefonttheme{professionalfonts}`.
- Greek letters and symbols stay Computer Modern (embedded). For µ in units, use the text glyph (`\um` = `\mbox{µm}`), not `\mu`, which is italic.
- Load type1cm and fix-cm, or 18 pt formula boxes warn "OMS/cmsy not available, size substituted".
- Not mathastext (A.5).

### 9.1 Container constraints (every session)

- The file system resets. Check before installing. TeX Live, poppler-utils, pandoc, python-pptx, lxml, pikepdf, pymupdf, opencv-python, pytesseract and Pillow are often present — but not always the same set twice, so check rather than assume.
  - Redirect install output.
  - pip needs `--break-system-packages`.
- CTAN is unreachable and tlmgr fails. Use only apt-packaged packages, and confirm before choosing one. GitHub raw files are usually reachable (fonts).
- texlive-fonts-extra is not needed (over 1 GB).
- The shell is sh.
  - No brace expansion or `time` in one-liners; call bash if needed.
  - Never wrap a script containing single quotes in `bash -c '…'`: the first inner quote ends the string. Use a file or a quoted heredoc.
  - Never reuse EOF for nested heredocs.
- Shell scripts copied from a previous unit lose their executable bit. `chmod +x *.sh` before the first build.
- Long jobs need a background run. OCR over a few hundred pages, or the mutation suite, exceeds a single command's time limit; start them with `nohup … &` and poll.
- Names that clash or mislead:
  - `\marks` is an e-TeX primitive, and `\tag` is amsmath's (loaded by Beamer). Use `\mk`, `\smk`, `\qtag`.
  - `\mk{` is not a substring of `\smk{`. Any tool that searches the source for a mark allocation must look for both spellings; one that looks only for the short one silently matches nothing.
- A pgfmath string array evaluates to a number: `\pgfmathparse{\lab[\k]}` on `{{"radio","micro"}}` prints something like 0.48. Use `\foreach \k/\name in {0/radio,1/micro}`.
- A `\foreach` list item containing a comma splits there (the fact, with the science word became two items and a pgfmath error). Write such nodes out one by one.
- ifthenelse in pgfmath evaluates BOTH branches, so it cannot guard a division by zero. Make the denominator safe instead.
- `\pgfmathsetmacro` results compare with `\ifdim <macro>pt<1pt` — how a figure decides whether a refracted ray exists.
- Flush-right marks: `\unskip\nobreak\hfil\penalty50\hskip1em\hbox{}\nobreak\hfill[n]` with `\parfillskip=0pt`. Two `\hfil` put the mark mid-line.

### 9.2 Slide settings and export

**Beamer**

- Class and page: `\documentclass[aspectratio=169,11pt,xcolor=table]{beamer}`; `\geometry{paperwidth=170mm,paperheight=95.625mm}`; 5 mm margins.
- The double-width PDF (slide | notes) joins two compiles:
  - slides_screen.pdf (`\setbeameroption{hide notes}`) and slides_notes.pdf (show only notes);
  - switched from the command line with `xelatex -jobname=slides_notes "\def\notesmode{1}\input{slides.tex}"`;
  - merged with pdfpages (`\includepdfmerge[nup=2x1]`, pages interleaved screen i, notes i) on a double-width page, after asserting equal page counts.
  - It is the PPTX input and the backup presentation file.
  - Not show notes on second screen (A.3).
  - Not RTF text notes: they align by delimiter and page order, so any added slide shifts everything after it.
- Note-page minipage uses `\textwidth`, not `\paperwidth`; the latter gives one Overfull \hbox per note page. Under Chinese notes with a Script:, the note page may be set in two columns (multicol) so every note still fits on one page.
- Every frame has exactly one `\note{}`, inside the frame, so both compiles have equal page counts.
- Split slides, never overlays. `\pause`, overlays and allowframebreaks break frames = PDF pages = PPTX slides — the only guarantee that notes stay aligned.
- No macros with parameters (#1) inside a frame, because the body is a macro argument. Put them in the .sty.
- Beamer silently lets content run into the footer unless Overfull \vbox fires. Keep the report on (no `[shrink]`), and spot-check pages with a last line near the footer; check 1b measures the gap. An overlay node (`remember picture,overlay`) writes into the footer with no warning at all — that is the case 1b exists for.
- A brace group right after the frame title becomes the subtitle, and the body vanishes without warning. Start every frame body with `\relax` (check 5b).

**Export slides.pptx** — the last step of build.sh, only after §10.2 items 1–6 are zero.

- Screen → full-page image.
  - Render the left half of the double-width PDF as a 3840 × 2160 PNG (609.6 dpi; PNG keeps text sharp).
  - One image per slide, filling the canvas, nothing else.
  - Size it from the presentation's own sldSz, not a constant: Inches(13.333) = 12 191 695 EMU ≠ 12 192 000, so a constant-based check fires on every slide.
- Notes → text + native equations.
  - Take each `\note{}` from slides.tex by brace matching; PDF text scatters fractions. Split at `\par`.
  - Expand project macros first, reading their definitions from shared.sty (`\defL` for `\Lref{}`, `\newcommand{\Txxx}` for terms), never from a table kept inside the exporter. A duplicated table goes stale silently, and the notes then ship reading `\Lref{surface}`. Expand the longest macro name first, so `\Tcrit` does not eat the start of `\TCrit`.
  - Convert each `$...$` with pandoc (texmath) to OMML, inside mc:AlternateContent / a14:m, with Cambria Math a:rPr on each math run and a linear fallback.
  - Use one pandoc call for all equations, and assert the returned count.
- Alignment assertion: frames = PDF pages = PPTX slides, or stop without writing.
- Notes are 16 pt with autofit off. If they look small, use presenter-view zoom instead.
- Under Chinese notes, the Say it: label and every line after it are coloured blue (`a:solidFill` RGB 0046BE), so the pronunciations stand out from the answers.
- Under Chinese notes, every text run carries an East Asian typeface beside its Latin one (`a:latin` Arial, `a:ea` Microsoft YaHei); macOS substitutes PingFang. Without `a:ea`, PowerPoint falls back per machine and the notes' line breaks move.

**Presenting:**

- First choice: PowerPoint presenter view (Microsoft 365, Windows or Mac), pen available. With no whiteboard, the pen on the slide is the only place to write live.
- Backup: the double-width PDF in SlidePilot (macOS) or pympress (Windows).

Master copy: slides.tex only. PPTX slides are images; anything edited in PowerPoint is overwritten by the next export.

### 9.3 Directory layout (one folder per unit)

```
unit-xx/
  handout.tex   slides.tex   classwork.tex   practice.tex   hw1.tex   hw2.tex
  shared.sty        colours, fonts, \flawed + Sam's font, apparatus/diagram macros,
                    term macros, lost-mark numbering (\defL / \Lref / \Ltext)
  slidestyle.sty    slide sizes (§5.4), \smk, footer, note page, formula box, slide headings (§3.3)
  docstyle.sty      printed A4 sheets: headings and boxes (§3.3), answer switch, answer lines
                    (\lines/\al, \flines/\af), \ansnote, drawing boxes, true-size grids, \blank
  fig/              figures shared by all files (never copied)
  fig/pp/           past-paper crops for screen
  fig/ppfull/       the same questions at natural size for print
  fig/ms/           official mark-scheme crops for the answer version
  fonts/            font files (TeX Gyre, PatrickHand-Regular.ttf; a CJK font under Chinese notes)
  build_wb.py       red-answer overlay generator (§6.2)
  build_slides.sh   screen + notes compiles, joined into slides.pdf
  build_sets.sh     printed sheets, blank + answers
  slides_zh_frames.tex  Chinese screens, one block per frame (§5.9); tools/build_zh_deck.py
                    joins them with the notes of slides.tex into slides_zh.tex
  build_teacher.sh  teacher PDF: English slide | Chinese slide + red answers (§5.9)
  build.sh          sheets → slides → slides_zh → teacher PDF → check.py --tex → export_pptx.py (both) → check.py --pptx
  export_pptx.py    PPTX export
  check.py          §10.2, all items
  test_checks.py    mutation tests for every check (§10.3.6)
  tools/            crop pipeline (§3.7); geom.py for computed figure coordinates
```

Deliver the double-width slides.pdf and slides.pptx together.

## 10. Pre-delivery checks

Rules live in their sections; this list only confirms them.

**General**

- Parameters are set and consistent, and every page earns its place.
- Every figure is checked, and pages are spot-checked (§3.6).
- Nothing touches an edge.
- Nothing that prints has a solid dark fill (§3.3, check 1d).
- Fractions are stacked and powers are real superscripts.
- The signature is on every page.
- The output language is as set, and there are no provenance labels.
- .tex, .pdf, .pptx and figures are all delivered.

**Handout:** one PDF with no gaps; one emphasis method; a numbered lost-mark list; no `\flawed{}`.

**Slides**

- The floor is met, TikZ fonts included, and every fraction-in-exponent is in a formula box.
- Do Now, Summary and one lose-marks slide per lesson are present, with 2–3 originals per group.
- Past papers appear only if supplied, in one contiguous run, under neutral titles.
- No answers on screen; at most two bold items per slide; unreadable crops are re-typeset.
- Every derivation is built across split slides (no whiteboard).
- Past-paper topics not taught in the lesson appear as Quick reviews (§5.8).

**Notes**

- Every question slide has notes in the §5.6 format, and values are checked against the original.
- Hard words carry Say it: once, where first said.
- No LaTeX macro survives into the notes (check 10).
- Under Chinese notes: prose is Chinese, every scientific term and every answer line is English, and no Chinese appears outside `\note{}` (check 10).
- Presenter view on a real machine cannot be checked in the container, so it is always listed as outstanding.

**Spot the error:** the count is stated, the errors are unmarked on screen, each maps to an L-number, and Sam never looks like a model.

**Homework, classwork and answer files**

- The blank version is checked for leaks, and answers sit on the lines.
- Prompts share a page with their boxes, and every overlay page is checked.
- Labels are correct; classwork carries no time; any true-size sheet says "print at 100%".

**Pairing:** §7 items 1–5.

### 10.1 Delivery note

At the top, list:

- every figure produced;
- what was removed from questions, and why;
- what was deliberately left out;
- every deviation from this specification, including re-typeset or re-drawn figures, handout trims, past-paper swaps, the screen/print split, check 1d whitelist entries and PDFs fixed in place;
- the tutor-side mapping (new item → original item) for any rewritten material (§3.7);
- defaults taken for unanswered questions (§1);
- any syllabus finding that changed the build, with the evidence it came from (§1);
- what still needs a real-machine check.

### 10.2 Machine checks

All items must be zero before delivery. Items 1–6 and 12–14 cover LaTeX, PDF and source; 7–11 cover the PPTX.

| # | Check | Method | Pass |
|---|---|---|---|
| 1 | Clean compile | Every .log (screen, notes, joined, sheets, answer versions): count Overfull \hbox, Overfull \vbox, ! errors. | all 0 |
| 1b | Screen text clears the footer | `pdftotext -bbox` on the screen PDF. Locate the footer by its own words (the signature), never by assuming it sits in the bottom 20 pt — a footer that has drifted otherwise hides from the check. Everything within 4 pt of the footer's top is footer (tight glyph boxes put a separator slightly higher than the words beside it). Body words end ≥ 2 pt above it; no word within 1 mm of a side edge. | 0 |
| 1c | Note pages do not overflow | `pdftotext -bbox` on the notes PDF: every word ends ≥ 1 mm inside the page. | 0 |
| 1d | No solid dark fills | Every printed PDF (sheets, answer versions, screen slides): with pikepdf, drop only the glyph-showing operators (Tj, TJ, ', ") and image Dos, in page streams and form XObjects. Dropping whole BT…ET blocks also drops the colour operators TeX sets inside them, so a dark box afterwards paints in whatever colour was left on the stack. Then render at 72 dpi greyscale, threshold at 50%, erode with a 3 × 3 px kernel so rules, frames, arrowheads and figure lines vanish. Any remaining dark component ≥ 200 pt² fails. Whitelist by page only, with the reason in the delivery note. | 0 |
| 2 | Fonts embedded | pdffonts emb = fifth field from the end (the object ID is two fields; the fourth is sub, also yes). Grep logs for font messages only, including Missing character. | all yes, no warnings |
| 3 | No answers on screen | slides.tex outside `\note{}` and `\flawed{}`: reveal headers (Answer:, Answer image:, Key answer:), and numerals after the last mark allocation on a line — searching for both `\mk{` and `\smk{` — ignoring TeX commands and their dimension arguments. | 0 |
| 4 | No slash fractions or fake superscripts | Extract maths first (notes included, `\flawed{}` excluded), then find x/y. In prose, find ^ and Unicode sub/superscripts. A `\dfrac` or `^{}` on a 9 mm `\al` line is an error: it needs `\af`. Units, paper codes and file paths are whitelisted. | 0 |
| 5 | No banned commands | The §5.4 list plus `\pause` and overlays, TikZ `font=` included. Size commands inside `\note{}` are allowed; `\includegraphics` in `\note{}` is always an error. | 0 |
| 5b | Frame bodies not swallowed | No brace group right after a frame title (every body starts with `\relax`); exactly one `\note{}` per frame. | 0 |
| 6 | Plots stay on canvas | Before saving a matplotlib figure, assert that every ax.texts + ax.patches + ax.lines extent is inside the figure bbox. Report n/a if all figures are TikZ. | none outside |
| 7 | Page alignment | Frames = PDF pages = PPTX slides; joined width = height × 32/9. | equal |
| 8 | Slides are pure images | Per slide: one 3840 × 2160 PNG, full bleed against sldSz, no other shapes. | pass |
| 9 | No images in notes | p:pic / a:blip in any notesSlide XML. | 0 |
| 10 | Notes structure | Question slides (title contains Do Now / Practice / MCQ / Workbook / Spot the error / Classwork / Quick review) have notes. First line starts with a label ((a), Q1, 1., Teaching line…). Short solution: precedes Watch for:; Watch for: alone or a repeated label line is an error. Do Now has Diagnostic:. Labels appear in the order Short solution:, Watch for:, Diagnostic:, Script:, Say it:. Say it:, if present, is the last label and every line after it is word = SYL-la-ble (ASCII, one capitalised syllable). No Answer: / Answer image: / Key answer:. No \macro survives anywhere in the notes. Under English screen + Chinese notes, label-first answer lines contain no CJK character, and slides.tex outside `\note{}` contains none either. Run on the source and on the PPTX. | 0 |
| 11 | Notes maths truly typeset | Native branch only: m:f type not lin/skw; the joined m:t text per oMath has no /, ^ or Unicode sub/superscripts. Note prose has no ^, no Unicode sub/superscripts, no unspaced a/b. Each source $...$ has one native equation plus fallback. Units, codes and file names are whitelisted; spaced prose slashes are allowed. | 0 |
| 12 | Spot the error integrity | Every Spot the error frame states "has N errors" on screen and holds `\flawed{}`; its note numbers exactly 1. … N., each line with an L-reference. `\flawed{}` appears in no other frame. In sheets, every `\flawed{}` is followed by a bold "N errors" and an answer block numbered 1 … N with at least N `\Lref{}`. | 0 |
| 13 | Say it: once, where first said | Across the deck, each word is pronounced in at most one Say it: block, and no earlier slide uses the word on screen or in its notes. Match on the word stem, not the whole word, or a plural slips through. | 0 |
| 7t | Teacher PDF | Every frame block in slides_zh_frames.tex has `\answers{}`; teacher pages = joined pages = frames; joined pages are double width; teacher pages pass 1c; the blue Say it column appears on exactly the slides whose notes have Say it:. | 0 |
| 7z | Chinese deck paired | slides_zh.tex has the same number of frames as slides.tex, and each frame's `\note{}` is identical. | 0 |
| 14 | Blank and answer layouts match | For each sheet pair: equal page counts, and every word at the left margin present on the same page of the answer version at the same height (≤ 0.5 pt). The answer version holds extra left-margin words (the answers), so the two lists cannot be zipped — each blank word is looked up in the answer page. Dot leaders are excluded: every rule prints the same run of dots, so comparing them by position pairs unrelated rules. The practice set's mark-scheme pages are identified and dropped first (§6.3). | 0 |

### 10.3 Seven disciplines from practice

1. **Compute anything that depends on "about N characters per line".** An estimate once over-spaced nine of thirty questions and crushed one; TeX does this now. Never put a characters-per-line table in this spec — someone will treat it as authoritative.
2. **When a check fires, check the check before editing the file.** Fixing a false alarm breaks correct work. Answer checks look for reveal forms, never topic words. Known false alarms and blind spots:
   - Item 4: read $-to-$ and counted the slash in fig/f05.png (18 reported, 0 real); mistook `\\[2mm]` for display maths.
   - Item 3: the keyword answer flagged "a minus sign does not make the answer negative"; TikZ x=7.2mm matched until a space before = was required; stem data was flagged until the check was restricted to text after the mark allocation. It also flagged `[2]\par\vskip2mm` (the 2 of the dimension) on six slides, and a teaching line "[2] = two links, [3] = three". And it searched only for `\mk{`, which is not a substring of `\smk{`, so it passed a whole deck without testing anything.
   - Item 11: without the whitelist, it flags paper codes, and the / of m/s because OMML gives it its own run.
   - Item 2: "not found" matched a pdftexcmds info line; it also read the wrong pdffonts column for a whole round, passing everything.
   - Item 6: matched the word "matplotlib" inside the test file (match real imports).
   - Item 1d: a content-stream scan (fills darker than 50% grey over 200 pt²) flagged every framed box, because tcolorbox draws its frame as a full-size dark fill under a lighter interior. The rendered version sees only what prints: 12 of 12 on the old handout, 0 on the fixed one.
   - Item 1b: found the footer by position, so a footer that had moved was invisible to it; and once it found the footer by text, a separator glyph on the footer's own line read as body text.
   - Item 14: zipped the blank and answer word lists, which pairs unrelated dot leaders with each other and reports enormous fake offsets.
3. **Overflow is fixed only by deleting, moving or splitting, never by shrinking.** "Just a little smaller" always slides further, so the compiler is the assertion.
   - What worked: delete an intermediate step, move an explanation to the notes, split a four-step sequence over two slides, shrink an image (never text).
   - The split also improved the build-up: overflow often signals content organisation, not just layout.
   - Shrinking the figure by 10% at a time is the slow version of the same mistake. Three rounds of that on one slide were beaten by deleting a single sentence the figure already said.
4. **Compiling is verification, not sightseeing.** Read the log rather than every page — except figures and overlays, which get checked on a contact sheet.
5. **Every coordinate is computed or not drawn.**
   - √53 on a number line sits at (√53 − 7)/(8 − 7) = 0.2801.
   - Leader arrows end at the glyph's bounding box.
   - Crops and answer placement come from pixel scans, not thumbnails.
   - Grains inside a filter-paper cone satisfy |x| + 1.5 r ≤ paper half-width at (y − r) (tools/geom.py).
   - A refraction construction solves for its own vertices: B = (L cos²i, L sin i cos i), D = (L sin²r, −L sin r cos r).
6. **Test the tests.** After writing or changing a check, plant one fault per item in a scratch copy and confirm it is caught; a check that has never failed is unproven. Verify the fixture too. Each of these made a check look blind:
   - a planted overflow pushed its text onto a second page;
   - an "unembedded font" PDF had no font at all;
   - a font-stripping fixture walked pdf.objects and missed descriptors hanging off page resources;
   - a walker deduplicated on id(), which pikepdf recycles after garbage collection, so it stopped after one object;
   - a footer fixture's `\vskip` was absorbed by Beamer, so the footer never moved — only an overlay node produces a footer collision that is genuinely silent;
   - a dark-fill fixture's `\colorbox{\parbox{…}{\vskip6mm\hbox{}}}` collapsed to a 4 px tick instead of a bar; `\rule` is unambiguous.

   A fixture may not quote a long literal from the material it mutates. Five broke at once when the deck was rewritten. Anchor on a short pattern, and build the replacement with a callable so no escape processing applies — `re.sub` reads `\noindent` as a bad escape and `\n` as a newline. A verifier that only checks a file exists is not a verifier. It must assert the fault is present and, where the check is about silence, that the log is still clean.
7. **Silent failures produce no log line.** Examples:
   - a length re-evaluated in a minipage;
   - a pgfmath string array printing 0.48;
   - a misplaced `\fi` printing answers on the blank sheet;
   - labels scaled below the floor;
   - `\hfill[2]` at a line end leaving the mark alone at the left of the next line (now `\smk`);
   - a fraction on a 9 mm answer line crossing the rule (now `\flines` and check 4);
   - a TikZ picture in a [t] minipage dropping the text beside it (§3.3);
   - a macro argument (#2) left pointing at the wrong parameter after a signature change, which built a 1.2 mm box around every answer;
   - a header label 2.7 pt taller only in the answer version, which moved an answer block to a new page (now `\smash` and check 14);
   - an answer-only `\ifansmode` header line changing the blank sheet's pagination (now `\ansnote`, check 14);
   - `\blank` smashed in only one version, leaving the blank sheet's underline depth in the line (check 14);
   - an unscoped TikZ `\clip` removing the caption drawn after it;
   - the PPTX exporter holding its own stale copy of `\Lref{}` and the term macros, so 26 notes slides shipped reading `\Lref{surface}` (now read from shared.sty, check 10).

   A label macro called with five arguments instead of four did leave a log line. The extra argument became stray text in the TikZ picture, and every letter reported Missing character … in font nullfont, which check 2 catches. When nullfont appears, look for a wrong argument count before looking at fonts. Each, once found, becomes a macro that cannot be written wrongly (§10.4) or a check.

### 10.4 When an accident gets past the log

Never return to page-by-page checking. Fix the macro so the same mistake becomes a log line; that is the only way §10 stays trustworthy.

- Formula box: a fixed-width `\hbox` with `\hfil`, not `\hss` (which shrinks without limit and swallows the warning). An overlong formula then reports Overfull \hbox.
- Answer line: a `\vbox` to its pitch, so an outgrown answer reports Overfull \vbox.
- Answer-only content: `\ansnote{h}{…}`, which reserves the height in both versions and overflows visibly if it grows.
- Question labels: `\qline[w]{label}` sets the label in `\hbox to w{…\hfil}`; "Step 1" in a 14 mm box ran into the text with no warning until this change.
- PPTX: first change export_pptx.py or add a §10.2 check, then fix the file.
- A duplicated definition: delete the duplicate and read the original. The exporter's copy of the L-numbers could not be kept in step by discipline; reading shared.sty removed the possibility.

## Appendix A: tried, do not retry

**A.1 Images in notes.**

- Tried: injecting p:pic plus a relationship into the notesSlide with lxml.
- Result: the file is valid, but the image shows only in Notes Page view and printouts, not in the notes pane or presenter view (real machine).
- Rule: no images in notes (§5.6). Retry only after PowerPoint changes and a real-machine retest confirms it.

**A.2 PPTX directly from Marp or Quarto.**

- Marp: full-image slides with text notes. Editable export goes through LibreOffice, and layout is unstable. No better than Beamer, and it loses the compile log.
- Quarto: gives native equations, but layout is template-bound, and PowerPoint neither reports overflow nor stops auto-shrinking. Every assertion in §3, §5 and §10 would need rewriting.
- Rule: layout stays in XeLaTeX; pandoc is used only for LaTeX → OMML in notes.

**A.3 pgfpages show notes on second screen under XeLaTeX.**

- Result: plain paragraphs and tables vanished from the slide half, while lists, titles and TikZ survived; pdftotext still found the text.
- Working diagnosis: the colour stack across pgfpages' logical pages under xdvipdfmx.
- Rule: use separate compiles joined by pdfpages (§9.2).

**A.4 Compositing question images by bounding box.**

- Tried: pasting pdfimages output at pdfplumber boxes.
- Result: other questions' options and tables appeared in crops, because the images overlap and rely on clipping. Stacking the images instead lost the answer spaces.
- Rule: strip text operators and render (§3.7).

**A.5 mathastext under XeLaTeX.**

- Result: letters switched, but digits (superscripts included) stayed CMR10 in pdffonts.
- Rule: use mathspec (§9).

**A.6 Splitting a tall past-paper question into two columns.**

- Result: after whitespace compression the question is nearly square. Two halves side by side form 4.5:1 on a 2.1:1 slide, height-limited to about 35 mm of 75 mm. One centred image was larger (84 × 75 mm vs 160 × 35 mm).
- Rule: show one image, and put the readable copy in the printed set (§5.5, §6.3).

**A.7 Pronunciation in full-width brackets (【trans - LU – cent】).**

- Result: it breaks §3.5, has no glyph in TeX Gyre, and en dashes are not ASCII.
- Rule: use Say it: with word = trans-LOO-sent (§5.6).

**A.8 Guarding a pgfmath singularity with ifthenelse.**

- Tried: `\pgfmathsetmacro{\vv}{ifthenelse(\dd<0.02, 0, 1/(1/\ff - 1/\uu))}` to stop a lens figure dividing by zero at u = f.
- Result: "You've asked me to divide 1 by 0.0" — pgfmath evaluates both branches.
- Rule: make the denominator safe (`\den + ifthenelse(abs(\den)<0.02, 1, 0)`) and suppress the drawing with `\ifdim` (§3.4).
