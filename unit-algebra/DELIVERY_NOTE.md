# L2 Algebra 单元 · 第 1 课（草稿）· 交付说明

NCEA Level 2 Mathematics · Apply algebraic methods（91261）· 每节 100 分钟 · 一对一投到电视 · 考前冲刺，目标 M/E

按规范 v20 §3.6，先把第 1 课完整做完发给你看；风格确认后再做第 2–4 课。

## 一句话假设

学生 Year 11 的代数（index laws、单括号展开、简单因式分解、数字分数）已经会，所以第 1 课不从定义讲起，而是从 Do Now 诊断开始，重点放在 M/E 题型和失分点。

## 参数

| 参数 | 取值 | 来源 |
|---|---|---|
| 教学方式 | slide-led（没有白板） | 规范默认 |
| 观看距离 | far（投电视），字号按 §5.4 far 一栏 | 你的回答“和 Light 一样” |
| 学生活动 | 打印 Handout、Classwork、Practice set、Homework；前三份下课收回 | 同上 |
| 语言 | 学生看到的全部英文；演讲者备注中文、术语英文 | 同上 |
| 深度 | exam sprint，目标 M/E | 你的回答 |
| 真题 | 2021、2022 进课；2023 整套不动，留作模考 | 你的回答 |
| 讲义 | 每节一份自己做的 Handout | 你的回答 |
| 答案文件 | 同版面红色答案（`\withanswers`） | 你的回答 |
| 评分标注 | 每小题 [A] / [M] / [E]；答案版写出 u、r、t 的要求和 N0–E8 换算 | 你的回答 |
| 作业长度 | 约 60 分钟（三题小卷子 + Quick review） | 你的回答 |

## 四节课的划分

| 课 | 内容 | 2021/2022 真题 |
|---|---|---|
| **1（本次）** | 指数（负指数、分数指数、根式）、展开（含三括号）、因式分解（HCF、a≠1、平方差、完全分解）、代数分式（化简、乘除、加减、分式方程、换主元） | 2021 Q1(a)、Q2(a)(b)、Q3(a)(b)(c)；2022 Q1(a)(b)、Q3(a)(i) |
| 2 | 指数方程与对数（log laws、解方程、增长衰减应用题，含 e 和 ln） | 2021 Q2(c)；2022 Q3(a)(ii)(b)(c) |
| 3 | 二次方程：三种解法、由根反推方程、判别式与求 k | 2021 Q1(b)(c)；2022 Q2(a)(b) |
| 4 | M/E 综合：代数证明、直线与曲线联立、根式方程、建模 | 2021 Q1(d)、Q3(d)；2022 Q1(c)(d)、Q2(c)(d) |

模考：2023 整套（合并 PDF 第 53–63 页）加评分表（第 47–52 页），建议第 4 课之后限时 60 分钟。

## 文件（`unit-algebra/`）

| 文件 | 内容 | 页数 |
|---|---|---|
| `slides1.pptx` | 课件：每页一张全屏图片，备注是中文文字 + 原生公式（298 个） | 48 张，7.2 MB |
| `slides1.pdf` | 双宽 PDF（左幻灯片、右备注），PPTX 的来源，也是备用放映文件 | 48 页 |
| `handout1.pdf` | 讲义：核心思想、评分方式、四块内容的 Write it in this order、12 个完整例题（标 u/r）、marker won't accept 表、失分点 L1–L10、Quick review 页 | 5 页 |
| `classwork1.pdf` / `classwork1_answers.pdf` | 课堂练习约 20 分钟：Part A（A 级 5 题）、Part B（M 级 3 题）、Part C（E 级 show that，带词框和句子开头）、Extension | 2 / 2 页 |
| `practice1.pdf` / `practice1_answers.pdf` | 真题练习纸：2021、2022 的第 1 课相关题，原卷截图、原尺寸、保留答题线；答案版最后两页是官方评分表截图（红色标题，注明 official assessment schedule extract） | 6 / 8 页 |
| `hw1.pdf` / `hw1_answers.pdf` | 作业约 60 分钟：Quick review 4 题 + Question One–Three，每题 (a)–(e)，(e) 是 E 级；含一道 Spot the error | 4 / 4 页 |

重新生成：`./build.sh 1`（sheets → slides → `check.py 1 --tex` → `export_pptx.py 1` → `check.py 1 --pptx`），约 75 秒。`python3 test_checks.py`（约 4 分钟，后台跑）对每一项检查植入错误，确认都能抓到。

## 课堂时间表（也写在第 1 页备注里）

| 时间 | 内容 | 幻灯片 |
|---|---|---|
| 0:00–0:05 | Do Now（5 题，备注里有 Diagnostic） | 2 |
| 0:05–0:07 | 核心思想：factorise first | 3 |
| 0:07–0:20 | Block 1 指数 + Spot the error (1) + Practice | 4–12 |
| 0:20–0:35 | Block 2 展开和因式分解 + Spot the error (2) + Practice | 13–22 |
| 0:35–0:55 | Block 3 代数分式、分式方程、换主元 + Spot the error (3) + 两组 Practice | 23–34 |
| 0:55–1:15 | Classwork 1 | 35 |
| 1:15–1:35 | 真题演练（学生写在 Practice set 1 上） | 36–45 |
| 1:35–1:40 | Ways to lose marks、Summary、Homework | 46–48 |

时间不够时：真题演练只做前 6 页，其余放到第 2 课开头。

## 生成的图

- **TikZ 重画（4 个）**：2021 Q3 的正方体和三个长方体（`\Cuboid` 宏，等轴测坐标由边长计算，标签和原题一致：p；p/2、2p、p；p−4、p+5、p−3；p−a、p+a、p）。原图是深灰实心填充，按 §3.3 改成线框 + 不超过 10% 灰的浅填充。
- **原卷截图（`fig/ppfull/q1–q7`）**：Practice set 用，原尺寸，300 dpi。切割位置来自 PDF 文字层的题号坐标，不是目测。页眉页脚（带试卷编号）都在切割范围外。
- **评分表截图（`fig/ms/q1, q2, q3, q6, q7`）**：Practice set 答案版用。上下边界由像素扫描找到表格横线，每块从表头行切到下一小题前的横线。

## 题目删改与偏离规范的地方

1. **课件上的真题是重新排版的，不是截图**（§3.4）。计算：原卷正文 12 pt，上标 6.9–9 pt；截图放在 160 mm 宽的幻灯片上，上标要放大约 1.9 倍才到 13 pt 下限，也就是截图宽度不能超过约 85 mm 原尺寸，几乎每道题都更宽。所以课件上逐字重排，原卷截图只放在打印的 Practice set 上。
2. **2021 Q3 的题干和 (a) 拆成两页**（幻灯片 42、43）：题干加两张图放一页会溢出 6.7 pt，题干文字不能删。(b)(c) 本来就各占一页，所以和题干分开。
3. **作业和练习标 [A]/[M]/[E]，不标 [n] 分**（你的要求）。答案版每题下面写 u/r/t 各要写到哪一步，再写 N1–E8 换算。
4. **学生看到的材料不印标准号 91261**（§3.1 不出现试卷编号），只写 “NCEA Level 2 Mathematics · Algebra”。
5. **Cut scores 按年份不同**（2021：0–7 / 8–13 / 14–19 / 20–24；2022：0–6 / 7–12 / 13–18 / 19–24），所以讲义和答案只写“大约 7–8、13–14、19–20 起”，不写某一年的数字。
6. **Practice set 答案版比空白版多 2 页**（官方评分表截图），这是 §6.3 允许的唯一例外，check 14 会先去掉这两页再比较。
7. Quick review 的来源：没有学生自己考过的卷子，所以用的是本课依赖的 Year 11 内容（index laws、数字分数）。

## 发现的问题（影响了制作）

- **2022 Q1(b)(i) 文字层丢了根号**：文字层是 “6x³y − 15x²y”，实际印的是 **6x³y − 15x²√y**（放大渲染核对过，评分表也是这样）。课件和讲义都按印刷版写。所有重排的题干都对照了高分辨率渲染，不是只看文字层。
- 2023 Q1(c) 出现 $e^{-0.5t}$，公式表也给了 ln：第 2 课会讲 e 和 ln。

## Spot the error（三页，每页 2 个错误）

| 页 | Sam 的题 | 错误 → L 编号 |
|---|---|---|
| 11 | $(3x^2)^3 / 9x^{-1}$ | 数字没立方 → L2；$6-(-1)$ 算成 5 → L1 |
| 21 | $6x^2+7x-20$；$5x^3-45x$ | 提 −4 后符号没变 → L5（Sam 因此得出“不能分解”的错误结论）；平方差没继续分 → L4 |
| 29 | $\frac{2x}{x+3}-\frac{x-1}{x-2}$ | 第二个分子只变了第一项的符号 → L7；约掉 $x^2$ → L6 |

作业 Q1(d) 另有一道（L2、L5）。所有错误都来自失分点清单 L1–L10，清单来源是评分表的措辞（如 “correct simplified fraction (not bashed)”、“positive index”、2022 Q1(b)(i) 只给 u 的不完全分解）加教学观察；没有考官报告，所以没有引用考官报告。

## 真题对照表（仅老师用）

| 幻灯片 | Practice set 页 | 原题 |
|---|---|---|
| 36 | p.1 | 2021 Q1(a)(i)(ii) |
| 37 | p.1 | 2022 Q3(a)(i) |
| 38 | p.2 | 2022 Q1(b)(i)(ii) |
| 39 | p.3 | 2021 Q2(a) |
| 40 | p.3 | 2021 Q2(b) |
| 41 | p.2 | 2022 Q1(a) |
| 42–43 | p.4 | 2021 Q3 题干、(a) |
| 44 | p.5 | 2021 Q3(b) |
| 45 | p.6 | 2021 Q3(c) |

其余题目（Do Now、讲解例题、Practice、Classwork、作业）都是原创，数字互不重复，也不和真题重复。

## 版权说明

- NZQA 试卷和评分表：页面上写着 “© New Zealand Qualifications Authority … All rights reserved. No part of this publication may be reproduced by any means without the prior permission of the New Zealand Qualifications Authority.” 本课在 Practice set 里用了原卷截图和评分表截图，仅限课堂内使用；如果要对外分发，需要考虑这一条。
- StudyTime 指南：© Inspiration Education Limited 2022, All rights reserved。本课只采用了它的方法顺序（FOIL、a≠1 的拆中间项、换主元时提出 x），没有复制它的文字或图。

## 机器检查（§10.2）

`check.py 1`：第 1–6、10–16 项全部为 0；PPTX 第 7–11 项全部为 0。`test_checks.py`：干净的测试样本先通过全部检查，然后逐项植入 29 个错误，全部被抓到。

第一次跑时第 13 项漏了 2 个，查下来是测试样本本身错了（植入的词在 Say it 之后才出现；“indices” 和 “index” 词干不同，不算重复），修正样本后两个都被抓到。

检查过程中修正了三项检查本身（先查检查，再改文件，§10.3.2）：

- **1c**：pdftotext 按内容流顺序输出，页眉的 “n / N” 排在 “end of notes” 之后，导致 47 页全部误报；改成按位置找最后三个词。
- **14**：“Official” 被提取成连字 “Oﬀicial”，评分表页没有被识别；改成先做 NFKC 规范化。
- **12**：粗体句子 “Sam's answer has 2 errors.” 末尾有句号，正则没匹配到；放宽了标点。

## 还需要在真机上检查

- PowerPoint presenter view（Microsoft 365）里备注的中文显示和备用字体（备注写了 Microsoft YaHei 作为 East Asian 字体）。
- 备注里的原生公式在 presenter view 里显示是否正常。

## 请你看完后告诉我

1. 课件节奏（48 页、每页一个问题）和备注的详细程度合不合适。
2. 作业 60 分钟三题小卷的难度和长度。
3. Practice set 用原卷截图（带原答题线）这种形式可不可以。

确认后我按同样的风格做第 2–4 课。
