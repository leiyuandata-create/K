# Green Machines + Metallic materials 冲刺课 · 交付说明

Year 9 Science · 两小时一对一考前冲刺（投屏，远距离）· 学校考试按 A / M / E 评分 · 规范 v24

## 参数

| 参数 | 取值 |
|---|---|
| 教学方式 | slide-led，没有白板（讲解都拆成多页逐步出） |
| 观看距离 | far，字号按 §5.4 far 一栏 |
| 学生活动 | 打印 In-class work（含 Mini mock）和 Homework，下课收回 |
| 语言 | English screen + Chinese notes：屏幕和纸全英文；PPTX 备注中文，术语全英文，难词有 `Say it:`；每页备注有中英混合讲稿 `Script:` |
| 老师背景 | non-specialist：另附中文版课件 `slides_zh.pptx`（v22，取代备课手册） |
| 深度 | exam sprint：范围和难度不超出两本 booklet，只换提问角度 |
| 考试 | 学校年底考试，A / M / E |

## 文件

| 文件 | 内容 | 页数 |
|---|---|---|
| `slides.pptx` | 课件：每页一张全屏图片；备注是中文 + 英文术语 + 原生公式 | 61 张 |
| `slides.pdf` | 双宽 PDF（左幻灯片、右备注，备注两栏排），PPTX 的来源，也是备用放映文件 | 61 页 |
| `slides_zh.pptx` | **中文版课件**：和英文版一页对一页，句子是中文，术语保留英文、括号附中文，如 stigma（柱头）；图里的标签也换成中文；Sam 的答案保留英文（学生要改的是英文答案）；备注和英文版完全一样 | 61 张 |
| `slides_zh.pdf` | 中文版的双宽 PDF（左幻灯片、右备注），备用 | 61 页 |
| `slides_teacher.pdf` | **老师用的双宽 PDF**：左边是英文幻灯片（投屏用）；右边是同一页的中文幻灯片，下面用红色粗体写出这一页的答案；有难词的页（25 页），右侧另有一栏蓝色的自然拼读 Say it | 61 页 |
| `inclass.pdf` / `inclass_answers.pdf` | **In-class work + Mini mock**（一份纸）：Part A–C 第一课后做，Part D–F 第二课后做，Part G 是 17 分钟的 Mini mock；Part C 有一张真实尺寸的坐标纸（需按 100 % 打印）；答案版同版面红字 | 6 / 6 |
| `homework.pdf` / `homework_answers.pdf` | **Homework**（一份纸）：Part 1 Green Machines、Part 2 Metallic materials，各约 40 分钟，分两天做；答案版同版面红字 | 5 / 5 |

重新生成：`./build.sh`（sheets → 英文版课件 → 中文版课件 → 老师用 PDF → `check.py --tex` → 两份 PPTX → `check.py --pptx`）。所有检查对两份课件都跑。`python3 test_checks.py` 在草稿副本里对每项检查植入错误，38 个全部被抓到。

**老师用 PDF 怎么放映**：用 SlidePilot (Mac) 或 pympress (Windows) 打开 `slides_teacher.pdf`，选“右半边是备注”的模式：投影仪显示左边的英文幻灯片，你的电脑屏幕显示右边的中文页和红色答案。答案写在 `slides_zh_frames.tex` 每一页的 `\answers{...}` 里，改答案只改这里。蓝色读音直接取自 `slides.tex` 备注里的 `Say it:`，改读音只改备注。PPTX 备注里的 Say it 也是蓝色。

**中文版怎么来的**：中文屏幕内容写在 `slides_zh_frames.tex`（每页一段）；`tools/build_zh_deck.py` 把它和 `slides.tex` 里同一页的备注拼成 `slides_zh.tex`，所以两份课件的备注永远一样（第 7z 项检查）。改备注只改 `slides.tex`；改中文屏幕只改 `slides_zh_frames.tex`。讲稿在备注的 `Script:` 段。上一版的中文备课手册已经删掉。

## 课堂时间表（每页备注里也写了）

| 时间 | 内容 | 页 |
|---|---|---|
| 0:00–0:05 | 开场、Lesson 1 divider、Do Now | 1–3 |
| 0:05–0:19 | Loop 1 reproduction：花的结构、sexual / asexual、pollen → seed、wind / insect、Spot the error 1、种子、Practice | 4–12 |
| 0:19–0:30 | Loop 2 photosynthesis / respiration：叶片结构、两个方程式、淀粉测试、foil leaf、Spot the error 2、Practice | 13–19 |
| 0:30–0:39 | Loop 3 transport：运输词汇、水的路线、transpiration pull、osmosis、Visking tubing、Spot the error 3、Practice | 20–26 |
| 0:39–0:50 | Ways to lose marks、Summary、Classwork Part A–C | 27–29 |
| 0:50–0:55 | Lesson 2 divider、Do Now、one idea | 30–32 |
| 0:55–1:05 | Loop 1 properties + density（含 Spot the error 4） | 33–39 |
| 1:05–1:12 | Loop 2 heat treatment + alloys | 40–45 |
| 1:12–1:20 | Loop 3 corrosion + rusty nail（含 Spot the error 5） | 46–51 |
| 1:20–1:27 | Loop 4 reactions + reactivity series（含 Spot the error 6） | 52–56 |
| 1:27–1:40 | Ways to lose marks、Summary、Classwork Part D–F | 57–59 |
| 1:40–1:57 | Mini mock（In-class work Part G） | 60 |
| 1:57–2:00 | Homework | 61 |

她最容易丢分的四类，每个 loop 都有覆盖：
- **Explain 长答题**：4 页 “write it in this order”（variation、transpiration pull、justify a choice、rusty nail 结论），alloy 的第二页也是同样的链条；每页标出 A / M / E 各写到哪一步；6 个 Spot the error 让她改 Sam 的答案。
- **实验题**：淀粉测试每一步的原因、foil leaf、bell jar + soda lime、cress 种子四管、rusty nail 两页、rusting 实验设计、reactivity 实验设计（Classwork Part F）。
- **术语、定义、拼写**：每个 loop 开头一个 Quick review；Mock Q1 拼写计分；作业另布置 booklet p.24 glossary 和 Metals p.16 crossword。
- **计算和图表**：density 三种题型（规则物体、排水法、对表认金属）、Visking tubing 速率、alloy melting point 图、In-class work Part C 画图、Homework Part 2 温度数据表。

## 生成的图

**从她的 booklet 照片裁出来的图（fig/，6 张）**：花的剖面 (GM p.6)、打开的豆子 (GM p.12)、叶片横切面 (GM p.15)、osmosis 放大圆 (GM p.19)、Visking tubing 装置 (GM p.18)、盖了锡箔的 variegated leaf (GM p.22)。
- 处理：手机照片转正 → 纸张提白（只白化不饱和的浅色像素，保留灰色填充）→ 用矩形把 Mila 的手写标签涂掉 → 去掉小噪点 → 按像素扫描留约 5 px 白边。没有裁进任何她的笔迹。
- 原图上的小字标签远距离看不清，所以去掉，改成大号字母 A–H（叶片用自己画的引线，其他图把字母放在原印刷箭头的尾端）。字母位置由 `tools/anchors.py` 扫描像素算出。
- osmosis 圆：原图的浅灰圆框在提白时丢了，按 Hough 拟合出的同一个圆重新描了一圈。

**TikZ 图（全部写在 `shared.sty`）**：green machine 三件事、metals 两排关系图、纯金属层和滑动后的层、alloy 层（大原子周围的小原子由 `tools/geom.py` 松弛计算，确实不重叠）、三支 rusty nail 试管（钉子靠在管壁或颗粒上，B 管钉子落点按圆底几何计算）、reactivity series（按 booklet p.20 的分组和措辞重画）、量筒（刻度按 0.2 单位每 mL 计算）、X / Y 合金熔点图（编的数据）。

## 与规范（v20）不同的地方

1. **用 A / M / E 等级代替 [n] 分**（按你的选择）。题目标 [A] / [M] / [E]，表头写 “Each question: A / M / E”，没有总分。
2. **没有讲义**（按你的选择）。中文版课件也不是讲义，只是同一份课件的中文屏幕。两本 booklet 当讲义用，每页页脚写 `Green Machines p.X` 或 `Metals p.X`。§7（讲义和课件配对）不适用，所以没有 term macros。
3. **两课合一份课件**：每课各有 Do Now、divider、lose-marks、Summary，各有一页 Classwork（共两页，不是整份课件一页）。
4. **rusty nail 试管和 reactivity series 是重画的**，没有裁图：原图标签在远距离看不清。重画时用了 booklet 的原词。
5. **备注页（双宽 PDF 右半边）改为两栏、字号 6.9 pt**，加了讲稿后每页备注仍能放在一页；PPTX 备注栏仍是 16 pt，可以滚动。
6. 没有提供真题，所以没有 past-paper 页。一对一，不用 ABCD 卡。
7. 第 1d 项没有白名单（裁图是图片，检查时按规范剔除），没有就地改过的 PDF。

## booklet 里要注意的科学问题

- **guard cells**：booklet p.16 写 guard cells “swell to close the stomata and shrink to open it”，真实情况相反（吸水 swell 时 stomata 打开）。课件没有出这个方向的题，只在 Quick review 的备注里提醒。
- **chlorophyll**：booklet p.20 说它 “speeds up the reaction”（当作催化剂）。课件备注写 absorbs light energy，两种说法都接受。
- **rusting 的产物**：booklet 词汇表写 “iron hydroxide”，课件和练习都不问产物名称。
- **拼写**：booklet 印的是 “Radical”，正确拼写 radicle，备注里提醒了。
- nitric acid 和大多数金属反应实际上不放出 hydrogen（只有很稀的 nitric acid 和 magnesium 才会），所以课件和练习没有另外出 nitric acid 的题；booklet p.22 summary 里的 magnesium + nitric acid 留给她自己做。

## 刻意没放进去的内容

- Metals p.14 electroplating（optional activity）、p.11 thermobile 演示、p.2 的 Extension（structure and bonding）、p.18 “Extra for experts” 的 sulfate / nitrate。
- Metals 学习目标里有 “conduct an experiment on thermal conductivity”，但照片里的 booklet 没有对应页，所以没教。
- magnetic metals 只在 Do Now 出现一次；GM p.14 life cycle、plant parts 和 p.9 花粉显微镜实验没有单独出页。
- 种子散布的照片 (GM p.11) 没有裁，用文字题代替。

## 出处和题目对应（老师自留，不出现在学生材料里）

- 所有题目（Do Now、Practice、Quick review、Classwork、Mock、Homework、Spot the error）都是自编的（第 3 级），不是真题，也不是任何考试局的材料。各份材料之间没有重复的题目或数字。
- 失分点 L1–L16 来自 booklet 和教学观察，没有引用考官报告。答案文件都标注 “Tutor's working, not an official mark scheme”。
- 根据 Mila booklet 里的错误改写的题（新情境、新对象）：
  - p.4 spider plantlets 打勾 “involves gametes” → Spot the error 1（草莓 runners）
  - p.4 density 表最后一行用了乘法、体积单位写 cm → Spot the error 4（螺栓）
  - p.17 rusty nail 试管 B 写 “slight rusting” → Spot the error 5（回形针，试管 P / Q / R）
  - p.17 celery 演示只写到 A → “Why the water moves up” 一页 + Spot the error 3（康乃馨）
  - p.15 把 transports water and minerals 填成 spongy layer → 叶片 Quick review 的 Watch for
  - p.8 hair clip 写 annealing → heat treatment Quick review 第 4 题
  - p.6 copper wiring 理由不完整 → “Justify a choice” 一页
  - p.21 soda lime 实验没写原因 → Loop 2 Practice Q1（bell jar）
- booklet 里她没写的 workbook 题直接用作 Workbook 页：GM p.22 foil leaf、GM p.18 Visking tubing 结论。

## 没有回答的问题

两轮 8 个问题都回答了，没有使用默认值。

## 其他

- **Mila 的 booklet 照片没有提交到仓库**（上面有她的名字和笔迹）。`tools/crop.py` 重新裁图时需要先把 PDF 的页面图片放到 `../src/pages/`（`pdfimages -j booklets.pdf src/pages/p`）；`fig/` 里已经是处理好的图，平时 build 不需要原图。
- 字体：TeX Gyre Heros / Pagella，Sam 的手写体 Patrick Hand (OFL)，备注中文 WenQuanYi Micro Hei；PPTX 备注中文字体设为 Microsoft YaHei，Mac 上自动换成苹方。

## 还需要在真机上检查

- PowerPoint 演讲者视图（Microsoft 365，Windows 或 Mac）里中文备注和原生公式的显示（容器里无法检查）。讲稿较长，演讲者视图里可以把备注字号放大或滚动。
- Classwork 第 2 页的坐标纸按 100 % 打印后，1 cm 格子是否准确。
- 课件 2-up 打印时，裁图（叶片、花）的细节在黑白打印里是否清楚。

## 这一版的改动

- 原来的 Classwork 和 Mini mock 合成一份 In-class work（Mini mock 是 Part G）；原来的 hw1 和 hw2 合成一份 Homework（Part 1、Part 2）。每份都有同版面的红字答案版。题目内容没有变。
- Part G 标了 17 分钟，和 §6.5“课堂练习不印时间”不同：这是模考，需要计时。
- 课件里提到文件名的页（第 1、29、59、60、61 页和备注、老师用 PDF 的红字答案）都改成新名字。
