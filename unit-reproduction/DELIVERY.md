# Human Reproduction 冲刺课 · 交付说明

Year 9 Science · 两小时一对一考前冲刺，中间不休息（投屏，远距离）· 学校考试按 A / M / E 评分 · 规范 v25

来源：你上传的《Human Reproduction · Year 9 2026》booklet 照片（p.1–37，21 张；p.26–27 拍了两次）。

## 1. 参数

| 参数 | 取值 | 来源 |
|---|---|---|
| 考试范围 | 全本 19 条 Learning Objectives 都考；星号是她自己标的 | 你的回答 |
| 课堂结构 | 4 个 loop，每个 loop 讲完做 In-class work 的一个 Part（约 6 分钟），结尾 Mini mock | 你的回答 |
| 重点练习类型 | 看图标注和功能、月经周期和激素、Explain 长答题、数据和图表题，四类都加量 | 你的回答 |
| 敏感内容 | 都正常讲，考什么讲什么 | 你的回答 |
| 老师页 | 红字答案直接写在中文页上；下方一行中文提示；右侧蓝色读音栏 | 你的回答（规范 v25 新增） |
| 交付格式 | 只要 PDF，备注从简：没有 PPTX，备注里只有答案行和 Say it | 你的回答 |
| 作业 | 两部分，各约 40 分钟 | 你的回答 |
| 附加材料 | 不要 | 你的回答 |
| 学生、观看距离、评分 | 上次那位 Year 9 学生，一对一，电视远距离，没有白板，A / M / E | 我的假设，沿用上节课 |
| 讲义 | 不做；页脚指向她手里的 booklet（Booklet p.X） | 沿用上节课 |

## 2. 文件

| 文件 | 内容 | 页数 |
|---|---|---|
| `slides_teacher.pdf` | **老师用的双宽 PDF**：左半边是英文幻灯片（投屏），右半边是老师页 | 53 |
| `slides_screen.pdf` | 只有英文幻灯片，单屏放映或打印用 | 53 |
| `teacher_pages.pdf` | 只有老师页，可以放在另一台设备上对着看，页码和幻灯片一一对应 | 53 |
| `inclass.pdf` / `inclass_answers.pdf` | In-class work + Mini mock：Part A–D 对应四个 loop，Part E 是 12 分钟的 Mini mock（从新的一页开始） | 5 / 5 |
| `homework.pdf` / `homework_answers.pdf` | Homework：Part 1（p.1–2）、Part 2（p.3–4），各约 40 分钟；Part 1 有一张真实尺寸的坐标纸，按 100 % 打印 | 4 / 4 |
| `unit-reproduction-source.zip` | 全部源文件、图、字体、脚本、规范 v25 | |

**老师页怎么看**
- 中文页：和左边的英文页一页对一页，句子是中文，科学术语保留英文，后面括号里是中文。
- 红色粗体：这一页的答案，直接写在空格里和每道题下面；图上的字母后面直接写出名称。
- 中文页下方的小字：这一页的时间点、怎么讲、她容易错在哪里（括号里的 L 编号对应失分点清单）。
- 右侧蓝色栏 “Say it 读音”：这一页第一次出现的难词，大写的音节读重音。没有难词的页没有这一栏，中文页更大。

**怎么放映**：用 SlidePilot（Mac）或 pympress（Windows）打开 `slides_teacher.pdf`，选“右半边是备注”的模式：电视显示左半边，你的电脑显示右半边。不用这类软件的话，电视放 `slides_screen.pdf`，另一台设备开 `teacher_pages.pdf`。

重新生成：`./build.sh`（sheets → 英文课件 → 中文老师页 → 老师用 PDF → `check.py --tex`）。答案和提示只改 `slides_zh_frames.tex`；读音只改 `slides.tex` 备注里的 `Say it:`。

## 3. 课堂时间表（每页老师页下方也写了）

| 时间 | 内容 | 页 |
|---|---|---|
| 0:00–0:04 | 开场、Do Now、核心思想（从两个细胞到一个婴儿） | 1–3 |
| 0:04–0:20 | Loop 1：性细胞和 adaptations、女性正面图和侧面图、男性图、sperm 的路径、Spot the error 1、Practice | 4–13 |
| 0:20–0:26 | In-class work Part A | 14 |
| 0:26–0:43 | Loop 2：puberty、周期四个阶段、四种激素、两张激素图、“卵没受精”链条、Spot the error 2、Practice | 15–23 |
| 0:43–0:49 | In-class work Part B | 24 |
| 0:49–1:06 | Loop 3：从 intercourse 到 fertilisation、zygote / embryo / foetus、染色体、性别决定、双胞胎、booklet p.18–19 原题、Spot the error 3、Practice | 25–34 |
| 1:06–1:12 | In-class work Part C | 35 |
| 1:12–1:36 | Loop 4：子宫里的 foetus、placenta 交换、booklet p.26 原题、oxygen 链条、有害物质、几个数字、出生三阶段、不孕和 IVF、booklet p.35–36 图表题、Spot the error 4、Practice | 36–48 |
| 1:36–1:42 | In-class work Part D | 49 |
| 1:42–1:44 | Ways to lose marks、Summary | 50–51 |
| 1:44–1:59 | Mini mock（写 12 分钟，对答案 3 分钟） | 52 |
| 1:59–2:00 | Homework | 53 |

Loop 4 比前三个长 7 分钟，因为 booklet 后半本（p.26 以后）她几乎没写，而且图表题在这一段。时间不够时，先省 Practice 的 Q3（口头说），不要省 In-class work。

四类弱项的覆盖：
- **看图标注 + 功能**：性细胞、女性正面和侧面、男性、子宫里的 foetus 共 5 张图各一页 Quick review；两张“每部分的作用”填空表；纸上的标注题改成“写出做这件事的那个部位的字母”，和屏幕上的问法不重复。
- **月经周期和激素**：周期条形图两页、四种激素表、卵巢激素图和垂体激素图各一页、Part B 的 progesterone 数据表、作业的体温数据和画图。
- **Explain 长答题**：3 页 “write it in this order”（卵没受精、下一个是男孩吗、oxygen 到胎儿），每页标出 A / M / E 各写到哪一行；4 个 Spot the error；每个 Practice 的 Q3 是 E。
- **数据和图表**：booklet p.35–36 的折线图分两页做（describe 一页，suggest 和 predict 一页）；Part B、Part D、Mini mock、作业各有一道数据题，都按 “describe = 趋势 + 数字，suggest = 原因” 来问。

## 4. 图

**从 booklet 照片裁的图（`fig/`，2 张）**
- `fside`：女性侧面图（p.8）。处理：照片转正 → 纸张提白 → 按像素扫描留约 5 px 白边。原图的数字圆点放到电视上只有约 8 pt，低于 13 pt 下限，所以在原位置重排成大号数字；10 个位置由 `tools/anchors.py` 找圆点的连通域算出，逐个在检查图上看过。
- `mfront`：男性正面图（p.10 下半）。处理同上，另外用矩形涂掉了两处背面透过来的印迹；她的手写标签在裁剪框外，没有裁进任何笔迹。字母 A–H 放在 8 个印刷箭头的尾端，位置由像素扫描算出。B、C、D 三个箭头和 G、H 两个箭头挨得近，所以 B 放在箭头上方，G 向右移了 6.5 mm、H 放在箭头下方。
- p.10 上半的男性侧面图没有用：她画的引线穿过了图。

**TikZ 自绘（全部在 `shared.sty`）**：女性正面图（对称的子宫、输卵管、卵巢）、sperm、egg、周期条形图（内膜厚度 + 四个阶段）、两张激素曲线图（形状参照 booklet p.14，用高斯曲线叠加）、染色体数目流程、性别决定方格、两种双胞胎、子宫里的 foetus、placenta 交换示意、“从两个细胞到一个婴儿”流程。引线的落点坐标写在源码注释里。

**重画的图**：booklet p.35 的 multiple births 折线图。照片上的字太小，按原图的坐标轴和文字重画，两条线的数值是从照片上读的近似值（20–24 岁约 8–10，40–44 岁从约 14 升到约 25）。纵轴标题从竖排改成放在图的上方，文字没变。课件页脚注明 “graph re-drawn”。

## 5. 题目来源和改动

- **Workbook 页（第 30、31、38、43、45、46 页）** 用的是 booklet 的原题，逐字照搬：p.19 双胞胎判断题、p.18 三道问答、p.26 placenta 三问、p.32 不孕问题表、p.35–36 第 3、4 题。这些都是她空着的页，课上让她直接把答案写到 booklet 上。
  - 第 43 页的表：左栏“问题”是我从 p.31 的两段文字里概括的短语（booklet 的表只印了第一行），右栏第一行是书上已给的原文。
  - 第 46 页把三条报纸标题排成了一行文字。
- **In-class work 和 Homework 全部是原创题**（规范的第 3 级：tutor's own），答案版页眉标了 “Tutor's working, not an official mark scheme”。没有真题，所以没有真题连播页。
- **数据都是为练习编的**，数值按常见范围取整：progesterone 水平（Part B）、胎儿质量（Part D）、IVF 成功率按年龄（Mini mock）、每日体温（Homework Part 1）、早产比例（Homework Part 2）。
- **Spot the error 的来源**：第 1 个里 “cervix 是胎儿发育的地方” 来自她在 booklet p.8 正面图上把 uterus 和 cervix 标反；其余是这个单元的常见错误。四个都只用新的句子，没有用她的原话和笔迹。
- **失分点清单 L1–L14**（在 `shared.sty`）：来自 booklet 内容加教学观察，没有 examiner report 可追溯。
- 课件上的 Practice、纸上的题、Workbook 原题之间没有重复的题；同一个知识点换了问法或换了数据。

## 6. booklet 里需要你知道的几处

- **p.8 侧面图、p.10 正面图都没有印答案。** 老师页上的名称是我按解剖位置判读的。侧面图：1 ovary，2 fallopian tube，3 bladder，4 vagina，5 uterus，6 rectum，7 vulva，8 urethra，9 anus，10 cervix。如果学校老师给过不同的答案，以学校为准。
- **p.35 折线图的纵轴** 印的是 “Percentage … 0–30”。现实中的多胎比例大约是每 1000 次妊娠 10–25 次，也就是 1–2.5 %，这个轴很可能本来是 “per 1000”。课件和答案都按 booklet 印的写（约 11 %–25 %），这样她的答案和学校的图一致。
- **embryo 什么时候改叫 foetus**：glossary（p.37）写 after 8 weeks，p.28 写 nine weeks。答案写 8，老师页提示里注明 8 或 9 都对。
- **premature**：glossary 写 before 38 weeks，答案按这个写。
- **p.17 的 fertilisation 定义** 她还空着，第 26 页的提示里给了要她写的句子。
- **p.9、p.11 的填空和 p.12 的打勾表** 她也空着，这次课件没有覆盖（时间不够），作业里有一道同类型的题（8 个部位写 M / F / B）。

## 7. 和上节课不同的地方（规范 v25）

1. **红字答案写在中文页上**，不再放在中文页下方。中文页因此是“老师页”，字号比投屏的英文页小（正文 11 pt），只给你看，不给学生看。
2. **中文页下方多了一行提示**（`\hint{}`）：时间、讲法、易错点。
3. **只出 PDF**：没有 `slides.pptx` 和 `slides_zh.pptx`；`slides.tex` 的备注里只有英文答案行和 `Say it:`，没有 Script 讲稿。
4. **检查 7t 改写，新增检查 14r**：每个老师页都有提示；凡是英文页有提问的，中文页上必须有红字答案；英文课件源文件里不能出现红字宏；空白练习纸和英文投屏 PDF 逐页按颜色扫描，不能有红色。
5. 规范文件 `SPEC.md` 已升到 v25，在源文件压缩包里。

## 8. 机器检查

`check.py --tex` 全部为 0：编译日志（Overfull、错误）、深色填充、字体嵌入、斜杠分数、Spot the error 结构、空白版和答案版版式一致、空白版和投屏版无红色、中英两份课件备注一致、老师 PDF、页脚、备注页、禁用命令、备注结构、Say it 只在第一次出现的那一页。

- 新增和改写的检查（7t、14r）各植入了错误确认能抓到：删掉一页的提示、删掉一页的红字答案、把红字宏写进英文课件、把答案版当作空白版去扫描。
- **上节课那套 38 项的植入错误测试（`test_checks.py`）没有移植到这个单元**：它的样本是按上个单元的课件内容写的。其余检查的代码和上节课相同，没有改动。
- 目检：全部 53 张老师页、53 张英文页、两份练习纸的空白版和答案版，都在接触表上逐页看过。

## 9. 还需要你在真机上确认

- SlidePilot 或 pympress 的分屏模式：电视只显示左半边。
- `homework.pdf` 按 100 % 打印，第 2 页的坐标纸才是 1 cm 一大格。
- 黑白打印时 Sam 的手写体和图里的灰色是否清楚。
- 老师页在你的电脑屏幕上字够不够大。不够的话告诉我，我可以把蓝色读音栏收窄或把中文页字号调大。
