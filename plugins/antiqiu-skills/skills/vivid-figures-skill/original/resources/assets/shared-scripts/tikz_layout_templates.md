# 按需参考

选定模板后的适配以完整源码和卡片保留要点为准；以下示例仅在确有需要时使用，不作为重写已选模板的理由。

## TikZ 技术路线图/架构图模板

TikZ 画出来丑的根本原因：没有颜色分层、没有分阶段色块、节点样式太朴素。好的技术路线图应该是分阶段分色、自上而下清晰流动的。

### 设计原则

1. **分阶段着色**：每个研究阶段用不同的背景色块（浅色填充 + 深色边框），一眼看出层次
2. **圆角矩形**：所有节点用 `rounded corners=4pt`，不要直角方框
3. **箭头统一**：用 `-{Stealth[length=6pt]}`，粗细 `line width=0.8pt`
4. **留白充足**：节点间距 ≥1cm，不要挤在一起
5. **字体统一**：节点内文字用 `\small` 或 `\footnotesize`，不要太大
6. **阴影可选**：`drop shadow` 增加层次感，但不要过度

### 模板 1/2/3：已废弃（被模板 4/9/10/11 替代）

模板 1（纵向路线图）、模板 2（问题关系图）、模板 3（模型架构图）是早期简单版本，存在左侧文字重叠、线穿过节点等问题。**⛔ 不要使用模板 1/2/3，改用模板 4/9/10/11。**

- 模板 1 的场景 → 用模板 4 或模板 9
- 模板 2 的场景 → 用模板 10（管道式）
- 模板 3 的场景 → 助手 自由画架构图，遵守防遮挡规则即可

### 模板 4：通用研究技术路线图（所有论文类型通用）

白底 + 浅灰虚线框分阶段 + 蓝色主节点（微阴影）+ 白色子节点 + 蓝色粗箭头。简洁专业，适合所有论文类型。不依赖 `backgrounds` 和 `fit` 库。

**完整代码**：
- 通用版：见 `demo_roadmap_template4.tex`
- 竞赛专用版（多问题双行+星号标注）：见 `demo_roadmap_competition.tex`

**竞赛论文必须参考 `demo_roadmap_competition.tex`**：每个问题可有 2 行主节点+子节点，子节点 4 个一排，用 `$^{\bigstar}$` 标注最优方法。

**使用规则：复制下面的完整代码，只改节点文字和数量。**

**核心样式定义**（直接复制到 tikzpicture 参数）：
```latex
\begin{tikzpicture}[scale=1.0,
    main/.style={rectangle, rounded corners=3pt,
        minimum width=5.5cm, minimum height=0.7cm,
        draw=blue!80, line width=0.7pt, fill=blue!6,
        font=\small\bfseries, align=center,
        drop shadow={opacity=0.15, shadow xshift=0.5pt, shadow yshift=-0.5pt}},
    sub/.style={rectangle, rounded corners=2pt,
        minimum width=2.4cm, minimum height=0.6cm,
        draw=teal!70, line width=0.5pt, fill=white,
        font=\footnotesize, align=center},
    dashbox/.style={rectangle, rounded corners=4pt,
        draw=gray!40, dashed, line width=0.7pt, fill=gray!2},
    bigarrow/.style={-stealth, line width=1.4pt, color=blue!70},
    smarrow/.style={-stealth, line width=0.5pt, color=gray!50},
    label/.style={font=\small\bfseries, color=black!70},
]
```

**每个阶段的结构模式**（重复此模式，改文字和子节点数量）：
```latex
% === 阶段 N ===
% 1. 虚线框（先画，节点覆盖在上面）
\node[dashbox, minimum width=13cm, minimum height=2cm] (boxN) at (0, Y) {};
\node[label, anchor=north west] at (boxN.north west) {\scriptsize 阶段名称};

% 2. 主节点（蓝色，居中）
\node[main] (mN) at (0, Y+0.35) {主步骤名称};

% 3. 子节点（白色，一行排列，间距 2.8cm）
\node[sub] (sNa) at (-4.2, Y-0.65) {方法A};
\node[sub] (sNb) at (-1.4, Y-0.65) {方法B};
\node[sub] (sNc) at (1.4, Y-0.65) {方法C};
\node[sub] (sNd) at (4.2, Y-0.65) {方法D};
\foreach \x in {sNa,sNb,sNc,sNd} {\draw[smarrow] (mN) -- (\x);}

% 4. 阶段间粗箭头
\draw[bigarrow] (0, Y-1.4) -- (0, Y-2.0);
```

**双层阶段**（一个阶段有两行主节点时，虚线框高度改为 4.2cm）：
```latex
\node[dashbox, minimum width=13cm, minimum height=4.2cm] (boxN) at (0, Y) {};
% 第一行主节点 + 子节点
\node[main] (mN) at (0, Y+1.7) {第一步};
\node[sub] ... % 子节点
% 第二行主节点 + 子节点
\node[main] (mNb) at (0, Y-0.5) {第二步};
\node[sub] ... % 子节点
```

**关键参数**：
- 虚线框宽度统一 13cm，单层高度 2cm，双层高度 4.2cm
- 子节点 x 坐标：4 个时用 -4.2, -1.4, 1.4, 4.2；3 个时用 -2.8, 0, 2.8
- 阶段间粗箭头间距 0.6cm
- 标注最佳方法用 `$^{\bigstar}$` 上标

**使用规则：复制下面的完整代码，只改节点文字和数量。从下方 5 套配色中选一套替换 main/.style 和 sub/.style 的颜色值。**

<tikz_color_schemes>
#### TikZ 架构图配色方案（5 套，按论文类型选择）

**方案 A：低饱和蓝灰+淡青（★ 默认，适合经管/统计/社科/竞赛）**
```latex
main/.style={fill={rgb,255:red,200;green,218;blue,235},
    draw={rgb,255:red,140;green,170;blue,200}, ...},
sub/.style={fill={rgb,255:red,218;green,232;blue,220},
    draw={rgb,255:red,165;green,200;blue,175}, ...},
bigarrow: color={rgb,255:red,74;green,144;blue,184}
```

**方案 B：钢蓝+浅灰蓝（适合 CS/AI/工程类）**
```latex
main/.style={fill={rgb,255:red,180;green,210;blue,235},
    draw={rgb,255:red,120;green,160;blue,200}, ...},
sub/.style={fill={rgb,255:red,220;green,230;blue,240},
    draw={rgb,255:red,170;green,190;blue,210}, ...},
bigarrow: color={rgb,255:red,70;green,100;blue,150}
```

**方案 C：薰衣草紫+淡粉（适合医学/生物/心理学）**
```latex
main/.style={fill={rgb,255:red,210;green,195;blue,230},
    draw={rgb,255:red,170;green,150;blue,200}, ...},
sub/.style={fill={rgb,255:red,235;green,215;blue,225},
    draw={rgb,255:red,200;green,175;blue,195}, ...},
bigarrow: color={rgb,255:red,130;green,100;blue,160}
```

**方案 D：青绿+薄荷（适合环境/地理/生态）**
```latex
main/.style={fill={rgb,255:red,175;green,220;blue,210},
    draw={rgb,255:red,120;green,185;blue,170}, ...},
sub/.style={fill={rgb,255:red,215;green,235;blue,225},
    draw={rgb,255:red,170;green,205;blue,190}, ...},
bigarrow: color={rgb,255:red,60;green,130;blue,120}
```

**方案 E：暖灰+赭石（适合人文/历史/法学，低调沉稳）**
```latex
main/.style={fill={rgb,255:red,225;green,210;blue,195},
    draw={rgb,255:red,190;green,170;blue,150}, ...},
sub/.style={fill={rgb,255:red,235;green,230;blue,220},
    draw={rgb,255:red,200;green,195;blue,180}, ...},
bigarrow: color={rgb,255:red,140;green,120;blue,100}
```

**选择建议**：
| 论文类型 | 推荐方案 |
|---------|---------|
| 经管/统计/社科/竞赛 | A（低饱和蓝灰+淡青）★ 默认 |
| CS/AI/电子/通信 | B（钢蓝+浅灰蓝） |
| 医学/生物/心理 | C（薰衣草紫+淡粉） |
| 环境/地理/生态/农学 | D（青绿+薄荷） |
| 人文/历史/法学/哲学 | E（暖灰+赭石） |

All schemes share the same structural rules: white background, dashed boxes, rounded corners, draw-order layering. Only the fill/draw colors differ.
</tikz_color_schemes>

```latex
\begin{figure}[H]
\centering
\begin{tikzpicture}[scale=0.85, every node/.style={scale=0.85},
    main/.style={fill={rgb,255:red,200;green,218;blue,235},
        draw={rgb,255:red,140;green,170;blue,200}, rounded corners=3pt,
        minimum width=4.5cm, minimum height=0.6cm, align=center,
        font=\small, line width=0.4pt},
    sub/.style={fill={rgb,255:red,218;green,232;blue,220},
        draw={rgb,255:red,165;green,200;blue,175}, rounded corners=2pt,
        minimum width=2cm, minimum height=0.5cm, align=center,
        font=\footnotesize, line width=0.3pt},
    bigarrow/.style={-{Stealth[length=7pt,width=5pt]}, line width=1.8pt,
        color={rgb,255:red,74;green,144;blue,184}},
    smarrow/.style={-{Stealth[length=3pt]}, line width=0.3pt, color=gray!40},
    lbl/.style={font=\small\bfseries, color=black},
    dashbox/.style={draw=gray!40, dashed, rounded corners=4pt,
        fill={rgb,255:red,248;green,249;blue,250}},
]

% 第一步：虚线框（先画，节点覆盖在上面）
\node[dashbox, minimum width=10.5cm, minimum height=1.6cm] (b1) at (0, -0.3) {};
\node[lbl, anchor=east] at ([xshift=-6pt]b1.west) {综述};
\node[dashbox, minimum width=10.5cm, minimum height=5.2cm] (b2) at (0, -3.15) {};
\node[lbl, anchor=east] at ([xshift=-6pt]b2.west) {模型构建};
\node[dashbox, minimum width=10.5cm, minimum height=2.2cm] (b3) at (0, -6.65) {};
\node[lbl, anchor=east] at ([xshift=-6pt]b3.west) {实证分析};
\node[dashbox, minimum width=10.5cm, minimum height=2.2cm] (b4) at (0, -9.35) {};
\node[lbl, anchor=east] at ([xshift=-6pt]b4.west) {策略应用};
\node[dashbox, minimum width=10.5cm, minimum height=2.2cm] (b5) at (0, -12.05) {};
\node[lbl, anchor=east] at ([xshift=-6pt]b5.west) {结论};

% 第二步：节点和箭头
% 阶段1
\node[main] (m1) at (0, 0) {绪论};
\draw[bigarrow] (0,-0.7) -- (0,-1.3);

% 阶段2
\node[main] (m2) at (0,-1.8) {理论基础};
\node[sub] (s2a) at (-2.8,-2.7) {文献回顾};
\node[sub] (s2b) at (-0.9,-2.7) {概念界定};
\node[sub] (s2c) at (0.9,-2.7) {理论框架};
\node[sub] (s2d) at (2.8,-2.7) {研究假设};
\foreach \x in {s2a,s2b,s2c,s2d} {\draw[smarrow] (m2) -- (\x);}
\node[main] (m2b) at (0,-3.6) {模型设定};
\foreach \x in {s2b,s2c} {\draw[smarrow] (\x) -- (m2b);}
\node[sub] (s2e) at (-2.2,-4.5) {变量定义};
\node[sub] (s2f) at (0,-4.5) {计量模型};
\node[sub] (s2g) at (2.2,-4.5) {识别策略};
\foreach \x in {s2e,s2f,s2g} {\draw[smarrow] (m2b) -- (\x);}
\draw[bigarrow] (0,-5.2) -- (0,-5.8);

% 阶段3
% 阶段3 — 以下节点文字仅为示例，根据实际研究内容替换
% Example nodes shown below. Replace with actual research content:
% 预测类：数据预处理/模型构建/模型对比/预测应用
% 分类类：特征工程/模型训练/分类评估/模型解释
% 评价类：指标构建/权重确定/综合评价/结果分析
% 因果推断类：描述统计/回归分析/稳健检验/异质分析
\node[main] (m3) at (0,-6.3) {模型构建与分析};
\node[sub] (s3a) at (-3.2,-7.2) {数据预处理};
\node[sub] (s3b) at (-1.1,-7.2) {模型构建};
\node[sub] (s3c) at (1.1,-7.2) {模型对比};
\node[sub] (s3d) at (3.2,-7.2) {结果分析};
\foreach \x in {s3a,s3b,s3c,s3d} {\draw[smarrow] (m3) -- (\x);}
\draw[bigarrow] (0,-7.9) -- (0,-8.5);

% 阶段4
\node[main] (m4) at (0,-9) {策略应用};
\node[sub] (s4a) at (-2.2,-9.9) {制度优化};
\node[sub] (s4b) at (0,-9.9) {实施路径};
\node[sub] (s4c) at (2.2,-9.9) {保障措施};
\foreach \x in {s4a,s4b,s4c} {\draw[smarrow] (m4) -- (\x);}
\draw[bigarrow] (0,-10.6) -- (0,-11.2);

% 阶段5
\node[main] (m5) at (0,-11.7) {结论};
\node[sub] (s5a) at (-2.2,-12.6) {主要结论};
\node[sub] (s5b) at (0,-12.6) {创新点};
\node[sub] (s5c) at (2.2,-12.6) {研究展望};
\foreach \x in {s5a,s5b,s5c} {\draw[smarrow] (m5) -- (\x);}

\end{tikzpicture}
\caption{研究技术路线图}
\label{fig:research-roadmap}
\end{figure}
```

**架构要点（助手 画技术路线图时必须遵循）：**
1. **不依赖 `backgrounds` 和 `fit` 库**——只用 `tikz` + `arrows.meta` + `positioning` + `shapes.geometric` + `calc`
2. **不要灰色大背景 `\fill`**——白底最安全，不会出现黑色外围
3. 虚线框用 `dashbox` 样式（手动坐标 + minimum width/height），极浅灰填充 `rgb(248,249,250)`
4. **先画虚线框，再画节点**——利用绘制顺序，节点的 fill 自然覆盖虚线框
5. 左侧标签用 `lbl` 样式，**颜色必须是 `color=black`**，不要蓝色
6. 主节点统一橙色（`rgb(240,195,150)`），子节点统一绿色（`rgb(185,215,180)`）
7. 阶段间用蓝色粗箭头 `bigarrow`，节点间用灰色细箭头 `smarrow`
8. `scale=0.85` 确保一页放得下，阶段控制在 4-5 个
9. 子节点间距至少 1.5cm，超过 4 个分两行
10. **禁止用 `on background layer`、`fit=()`、灰色大背景 `\fill`**

#### 虚线框坐标计算规则（⛔ 防止框重叠）

虚线框用手动坐标，必须按以下规则计算，不能靠猜：

**单层阶段**（1 个主节点 + 1 行子节点）：
- 主节点 y 坐标 = `Y`
- 子节点 y 坐标 = `Y - 0.9`
- 虚线框中心 y = `(Y + Y-0.9) / 2 = Y - 0.45`
- 虚线框高度 = `1.6cm`
- 粗箭头从 `Y - 1.6` 到 `Y - 2.2`（间距 0.6）
- 下一阶段主节点 y = `Y - 2.7`（间距 = 上一阶段底部 + 0.5）

**双层阶段**（2 个主节点 + 2 行子节点）：
- 第一主节点 y = `Y`，第一行子节点 y = `Y - 0.9`
- 第二主节点 y = `Y - 1.8`，第二行子节点 y = `Y - 2.7`
- 虚线框中心 y = `(Y + Y-2.7) / 2 = Y - 1.35`
- 虚线框高度 = `3.4cm`
- 粗箭头从 `Y - 3.4` 到 `Y - 4.0`
- 下一阶段主节点 y = `Y - 4.5`

**三层阶段**（主节点 + 子节点 + 第二主节点 + 第二行子节点 + 第三行子节点）：
- 虚线框高度 = `5.2cm`，按实际内容范围计算

**关键公式**：
```
dashbox_center_y = (最高节点y + 最低节点y) / 2
dashbox_height = (最高节点y - 最低节点y) + 1.4cm  (上下各留 0.7cm padding)
bigarrow_start_y = 最低节点y - 0.7
bigarrow_end_y = bigarrow_start_y - 0.6
next_stage_main_y = bigarrow_end_y - 0.5
```

**验证方法**：每个虚线框的底边 y = `center_y - height/2`，下一个虚线框的顶边 y = `next_center_y + next_height/2`。两者之间必须有 ≥ 0.3cm 的间距，否则会重叠。
    % 阶段间粗箭头（灰蓝色，和竖条同色系）
    bigarrow/.style={-{Stealth[length=8pt, width=6pt]}, line width=2pt,
        color={rgb,255:red,90;green,120;blue,150}},
    % 节点间细箭头
    arrow/.style={-{Stealth[length=4pt]}, line width=0.5pt, color=gray!60},
]

% ========== 阶段一：研究设计 ==========
\node[stagelabel, rotate=90] (L1) at (-6.5, 0) {研究设计};
\node[stagebox] (B1) at (0, 0) {};
\node[main] (m1) at (0, 0.8) {研究问题确定};
\node[sub] (s1a) at (-3, -0.3) {文献梳理};
\node[sub] (s1b) at (-1, -0.3) {理论分析};
\node[sub] (s1c) at (1, -0.3) {假设提出};
\node[sub] (s1d) at (3, -0.3) {研究设计};
\draw[arrow] (m1) -- (s1a); \draw[arrow] (m1) -- (s1b);
\draw[arrow] (m1) -- (s1c); \draw[arrow] (m1) -- (s1d);

% 阶段间箭头
\draw[bigarrow] (0, -1.8) -- (0, -2.5);

% ========== 阶段二：数据与变量 ==========
\node[stagelabel, rotate=90] (L2) at (-6.5, -4.2) {数据与变量};
\node[stagebox] (B2) at (0, -4.2) {};
\node[main] (m2) at (0, -3.4) {数据收集与处理};
\node[sub] (s2a) at (-3.5, -4.5) {数据来源};
\node[sub] (s2b) at (-1.2, -4.5) {变量构建};
\node[sub] (s2c) at (1.2, -4.5) {描述性统计};
\node[sub] (s2d) at (3.5, -4.5) {相关性分析};
\draw[arrow] (m2) -- (s2a); \draw[arrow] (m2) -- (s2b);
\draw[arrow] (m2) -- (s2c); \draw[arrow] (m2) -- (s2d);

% 阶段间箭头
\draw[bigarrow] (0, -6) -- (0, -6.7);

% ========== 阶段三：实证分析 ==========
\node[stagelabel, rotate=90] (L3) at (-6.5, -8.8) {实证分析};
\node[stagebox, minimum height=3.8cm] (B3) at (0, -8.8) {};
\node[main] (m3) at (0, -7.6) {模型构建};
% 子节点分两行 — 以下节点文字仅为示例，根据实际研究内容替换
\node[sub] (s3a) at (-3.5, -8.8) {数据预处理};
\node[sub] (s3b) at (-1.2, -8.8) {模型构建};
\node[sub] (s3c) at (1.2, -8.8) {模型对比};
\node[sub] (s3d) at (3.5, -8.8) {结果分析};
\draw[arrow] (m3) -- (s3a); \draw[arrow] (m3) -- (s3b);
\draw[arrow] (m3) -- (s3c); \draw[arrow] (m3) -- (s3d);
\node[main] (m3b) at (0, -10.1) {模型诊断与检验};

% 阶段间箭头
\draw[bigarrow] (0, -11) -- (0, -11.7);

% ========== 阶段四：结论 ==========
\node[stagelabel, rotate=90] (L4) at (-6.5, -12.8) {结论建议};
\node[stagebox, minimum height=2cm] (B4) at (0, -12.8) {};
\node[main] (m4) at (0, -12.4) {研究结论};
\node[sub] (s4a) at (-2, -13.4) {政策建议};
\node[sub] (s4b) at (0, -13.4) {研究局限};
\node[sub] (s4c) at (2, -13.4) {未来展望};
\draw[arrow] (m4) -- (s4a); \draw[arrow] (m4) -- (s4b); \draw[arrow] (m4) -- (s4c);

\end{tikzpicture}
\caption{研究技术路线图}
\label{fig:research-roadmap}
\end{figure}
```

**架构要点（模板 4 通用规则）：**
1. **绘制顺序决定层级**：先画灰色大背景 → 再画白色虚线框 → 最后画节点和箭头。Do not use `on background layer` or `fit` library
2. 虚线框用 `dashbox` 样式（手动坐标，白色填充），不用 `fit`
3. 左侧阶段标签水平书写，放在虚线框外面左侧
4. 从上方 5 套配色方案中选一套，整张图统一使用。Do not mix schemes or use a different color per stage
5. 阶段之间用粗箭头（`bigarrow`），节点之间用灰色细箭头（`smarrow`）
6. 纵向布局，从上到下流动
7. 配色必须低饱和协调，禁止纯蓝/纯绿/纯红高饱和色
8. 子节点间距至少 1.2cm，超过 4 个分两行

### 常见丑图 vs 好图对比

| 丑图特征 | 改进方法 |
|----------|---------|
| 每个阶段不同颜色 | 选一套配色方案，整张图统一 main+sub 两色 |
| 用了 `on background layer` 导致黑底 | 用绘制顺序控制层级 |
| 直角方框 | `rounded corners=3pt` |
| 箭头太细看不清 | 阶段间用 `bigarrow`（1.8pt） |
| 节点挤在一起 | 子节点间距至少 1.2cm |
| 没有层次感 | 灰色大背景 + 白色虚线框 |
| 箭头交叉乱 | 用 `|-` 和 `-|` 走直角路径，避免斜线交叉 |
| 字体太大 | 节点内用 `\small`，标签用 `\footnotesize` |


### 模板 9：圆形编号 + 卡片分层（高级经管/实证风格）

**视觉特征**：左侧圆形编号+阶段名称 + 浅色卡片区域 + 方法节点/工具节点双层信息 + 右侧胶囊输出标签。适合方法论丰富的实证研究。

**完整代码**（复制后只改节点文字和阶段数量）：

```latex
\begin{figure}[H]
\centering
\begin{tikzpicture}[
    phasenum/.style={circle, fill={rgb,255:red,#1}, minimum size=22pt,
        font=\footnotesize\bfseries, text=white, inner sep=0pt},
    phasename/.style={font=\small\bfseries, color={rgb,255:red,#1}, anchor=west},
    method/.style={fill={rgb,255:red,#1}, draw={rgb,255:red,#2},
        rounded corners=4pt, minimum width=3.4cm, minimum height=0.85cm,
        align=center, font=\small, line width=0.5pt},
    tool/.style={fill={rgb,255:red,248;green,248;blue,248},
        draw={rgb,255:red,210;green,210;blue,210}, rounded corners=2pt,
        minimum width=1.8cm, minimum height=0.5cm, align=center,
        font=\scriptsize, line width=0.3pt},
    outputtag/.style={fill={rgb,255:red,#1}, rounded corners=10pt,
        minimum width=1.6cm, minimum height=0.4cm, align=center,
        font=\tiny\bfseries, text=white, inner sep=2pt},
    pipe/.style={-{Stealth[length=7pt, width=5pt]}, line width=1.8pt,
        color={rgb,255:red,200;green,210;blue,225}},
    inner/.style={-{Stealth[length=3pt]}, line width=0.4pt, color=gray!45},
    card/.style={fill={rgb,255:red,#1}, rounded corners=6pt, line width=0pt},
]
% Phase 1: 研究设计（蓝色）
\fill[card={245;green,250;blue,255}] (-1, 2.3) rectangle (15.5, -0.8);
\node[phasenum={100;green,160;blue,210}] at (-0.2, 1.7) {1};
\node[phasename={80;green,140;blue,190}] at (0.4, 1.7) {研究设计};
\node[method={232;green,243;blue,252}{165;green,200;blue,230}] (rq) at (3.2, 1.0) {研究问题提出};
\node[method={232;green,243;blue,252}{165;green,200;blue,230}] (lit) at (7.2, 1.0) {系统文献综述};
\node[method={232;green,243;blue,252}{165;green,200;blue,230}] (hypo) at (11.2, 1.0) {假设与框架构建};
\draw[inner] (rq) -- (lit); \draw[inner] (lit) -- (hypo);
\node[tool] at (3.2, -0.05) {文献计量}; \node[tool] at (5.5, -0.05) {知识图谱};
\node[tool] at (8.2, -0.05) {理论推演}; \node[tool] at (11.2, -0.05) {概念模型};
\node[outputtag={100;green,160;blue,210}] at (14.2, 1.0) {理论模型};
\draw[pipe] (7.2, -0.8) -- (7.2, -1.6);
% Phase 2: 数据准备（绿色）— 同样结构，换色
% Phase 3: 实证分析（橙色）— 三行：模型设定→机制检验→稳健性
% Phase 4: 结论建议（紫色）
% 每阶段重复：卡片背景 → 编号+名称 → 方法节点行 → 工具节点行 → 输出标签 → 管道箭头
\end{tikzpicture}
\caption{研究技术路线图}
\end{figure}
```

**四阶段配色**（蓝→绿→橙→紫）：
- 研究设计：编号 `rgb(100,160,210)`，卡片 `rgb(245,250,255)`，方法节点 `rgb(232,243,252)`
- 数据准备：编号 `rgb(80,170,130)`，卡片 `rgb(245,252,248)`，方法节点 `rgb(230,246,237)`
- 实证分析：编号 `rgb(215,155,75)`，卡片 `rgb(255,251,243)`，方法节点 `rgb(255,244,228)`
- 结论建议：编号 `rgb(150,120,180)`，卡片 `rgb(250,247,255)`，方法节点 `rgb(242,237,252)`

**架构要点**：
1. 不依赖 `backgrounds`/`fit` 库，用绘制顺序控制层级
2. 左侧圆形编号 + 阶段名称文字（不要用色带竖条）
3. 方法节点和工具节点形成双层信息，方法节点 y 间距 ≥ 1.0cm
4. 工具节点间距 ≥ 2.2cm，一行最多 5 个
5. 右侧胶囊标签标注每阶段输出物
6. 完整示例见 `demo_roadmap_research_premium.tex`

---

### 模板 10：管道分段 + 并行分支 + 汇聚（数据科学/竞赛风格）

**视觉特征**：5段管道色块 + 白色卡片带顶部彩色装饰条 + 并行三分支建模 + 汇聚节点 + 圆角胶囊方法标签 + 左侧圆形编号。适合多模型对比、数据驱动研究。

**完整代码**：见 `demo_roadmap_research_pipeline.tex`

**五阶段配色**（蓝→绿→橙→紫→灰绿）：
- 问题定义：标题 `rgb(85,155,210)`，背景 `rgb(244,249,255)`
- 特征工程：标题 `rgb(75,162,125)`，背景 `rgb(242,251,244)`
- 模型构建：标题 `rgb(212,158,75)`，背景 `rgb(255,250,240)`
- 评估验证：标题 `rgb(142,115,182)`，背景 `rgb(249,244,255)`
- 结论建议：标题 `rgb(102,132,112)`，背景 `rgb(246,249,246)`

**架构要点**：
1. 每个 Stage 是一个大圆角色块（`draw=none` 无边框），内含白色卡片
2. 卡片顶部有 0.15cm 彩色装饰条
3. Stage 3 用并行三分支 + Σ 汇聚节点，展示多模型对比
4. 方法标签用圆角胶囊样式，标签间距 ≥ 2cm
5. 汇聚节点和下方卡片间距 ≥ 0.8cm

---

### 模板 5：算法流程图（带判断分支）

```latex
\begin{figure}[H]
\centering
\begin{tikzpicture}[
    node distance=0.8cm,
    process/.style={fill=blue!10, draw=blue!50, rounded corners=4pt,
        minimum width=3.5cm, minimum height=0.8cm, align=center,
        font=\small, line width=0.6pt},
    decision/.style={fill=orange!12, draw=orange!50, diamond, aspect=2.5,
        minimum width=2cm, align=center, font=\small, line width=0.6pt,
        inner sep=1pt},
    io/.style={fill=gray!8, draw=gray!50, rounded corners=3pt,
        minimum width=3cm, minimum height=0.7cm, align=center, font=\small},
    arrow/.style={-{Stealth[length=5pt]}, line width=0.7pt, color=gray!70},
    yesno/.style={font=\footnotesize, color=gray!60},
]
\node[io] (start) {输入数据 $D$};
\node[process, below=of start] (init) {初始化参数 $\theta_0$};
\node[process, below=of init] (compute) {计算目标函数 $f(\theta)$};
\node[process, below=of compute] (update) {更新参数 $\theta \leftarrow \theta - \alpha\nabla f$};
\node[decision, below=of update] (conv) {收敛?};
\node[io, below=of conv] (output) {输出最优解 $\theta^*$};
\draw[arrow] (start) -- (init);
\draw[arrow] (init) -- (compute);
\draw[arrow] (compute) -- (update);
\draw[arrow] (update) -- (conv);
\draw[arrow] (conv) -- node[yesno, right] {是} (output);
\draw[arrow] (conv.west) -- ++(-1.5,0) node[yesno, above] {否} |- (compute.west);
\end{tikzpicture}
\caption{优化算法流程图}
\label{fig:algorithm-flow}
\end{figure}
```

### 模板 6：数据处理 Pipeline（横向多阶段）

```latex
\begin{figure}[H]
\centering
\begin{tikzpicture}[
    node distance=0.3cm,
    stage/.style={fill=#1!12, draw=#1!50, rounded corners=5pt,
        minimum width=2.2cm, minimum height=2.2cm, align=center,
        font=\small, line width=0.6pt},
    detail/.style={font=\tiny, color=gray!40, align=center, text width=2cm},
    arrow/.style={-{Stealth[length=6pt]}, line width=1pt, color=gray!50},
]
\node[stage=blue] (raw) {\textbf{原始数据}\\[2pt]\footnotesize 多源采集};
\node[stage=blue, right=1cm of raw] (clean) {\textbf{数据清洗}\\[2pt]\footnotesize 缺失值/异常值};
\node[stage=teal, right=1cm of clean] (feat) {\textbf{特征工程}\\[2pt]\footnotesize 变量构建};
\node[stage=teal, right=1cm of feat] (model) {\textbf{模型训练}\\[2pt]\footnotesize 参数优化};
\node[stage=blue, right=1cm of model] (eval) {\textbf{评估验证}\\[2pt]\footnotesize 交叉验证};
\node[detail, below=0.3cm of raw] {CSV/API/\\数据库};
\node[detail, below=0.3cm of clean] {插值/IQR/\\标准化};
\node[detail, below=0.3cm of feat] {PCA/交互项/\\时序特征};
\node[detail, below=0.3cm of model] {XGBoost/\\DNN/SVM};
\node[detail, below=0.3cm of eval] {RMSE/AUC/\\$R^2$};
\draw[arrow] (raw) -- (clean);
\draw[arrow] (clean) -- (feat);
\draw[arrow] (feat) -- (model);
\draw[arrow] (model) -- (eval);
\draw[arrow, dashed, color=red!40] (eval.north) -- ++(0,0.8) -| (feat.north)
    node[pos=0.25, above, font=\tiny, color=red!50] {特征调优};
\end{tikzpicture}
\caption{数据处理与建模流程}
\label{fig:pipeline}
\end{figure}
```

### 模板 7：经管/统计 — 变量关系路径图（中介效应）

```latex
\begin{figure}[H]
\centering
\begin{tikzpicture}[
    node distance=2cm and 3cm,
    var/.style={fill=#1!12, draw=#1!50, rounded corners=5pt,
        minimum width=3cm, minimum height=1cm, align=center,
        font=\small, line width=0.7pt},
    arrow/.style={-{Stealth[length=5pt]}, line width=0.8pt},
    coef/.style={font=\footnotesize, fill=white, inner sep=2pt},
]
\node[var=blue] (x) {\textbf{自变量}\\数字化转型};
\node[var=orange, above right=1.5cm and 3.5cm of x] (m) {\textbf{中介变量}\\创新能力};
\node[var=red, below right=1.5cm and 3.5cm of x] (y) {\textbf{因变量}\\企业绩效};
\draw[arrow, color=blue!60] (x) -- node[coef, below] {$c'$ (直接效应)} (y);
\draw[arrow, color=orange!60] (x) -- node[coef, above left] {$a$ (H1)} (m);
\draw[arrow, color=red!60] (m) -- node[coef, above right] {$b$ (H2)} (y);
\node[fill=gray!8, draw=gray!40, rounded corners=3pt,
    minimum width=2.5cm, minimum height=0.7cm, align=center,
    font=\footnotesize, below=1.5cm of y] (ctrl) {控制变量\\企业规模/行业/年份};
\draw[-{Stealth[length=4pt]}, dashed, color=gray!40, line width=0.5pt] (ctrl) -- (y);
\node[font=\footnotesize\itshape, color=gray!50, below=0.3cm of x] {H3: $a \times b$ 中介效应};
\end{tikzpicture}
\caption{理论模型与研究假设}
\label{fig:theoretical-model}
\end{figure}
```

### 模板 8：竞赛 — 单问题求解流程图（带分支+判断+并行对比）

```latex
\begin{figure}[H]
\centering
\begin{tikzpicture}[
    node distance=0.7cm and 1.2cm,
    step/.style={fill=#1!10, draw=#1!45, rounded corners=4pt,
        minimum width=3.5cm, minimum height=0.75cm, align=center,
        font=\small, line width=0.5pt},
    substep/.style={fill=gray!6, draw=gray!35, rounded corners=3pt,
        minimum width=2.6cm, minimum height=0.6cm, align=center,
        font=\footnotesize, line width=0.4pt},
    decision/.style={fill=orange!10, draw=orange!45, diamond, aspect=2.8,
        minimum width=1.5cm, align=center, font=\small, line width=0.5pt, inner sep=1pt},
    note/.style={font=\tiny, color=gray!40, text width=3cm, align=left},
    arrow/.style={-{Stealth[length=4pt]}, line width=0.5pt, color=gray!55},
    yesno/.style={font=\tiny, color=gray!50},
    phaselabel/.style={font=\tiny\bfseries, color=#1!50, rounded corners=2pt,
        fill=#1!6, inner sep=2pt},
]
% 阶段一：数据准备
\node[phaselabel=blue] (L1) at (-3.5, 0) {数据准备};
\node[step=blue] (input) at (0, 0) {读取附件数据};
\node[step=blue, below=of input] (eda) {数据探索与可视化};
\node[decision, below=0.8cm of eda] (missing) {有缺失值?};
\node[substep, right=1.5cm of missing] (fill) {插值/删除处理};
\node[step=blue, below=0.8cm of missing] (clean) {清洗后数据集};
\draw[arrow] (input) -- (eda); \draw[arrow] (eda) -- (missing);
\draw[arrow] (missing) -- node[yesno, above] {是} (fill);
\draw[arrow] (fill.south) |- (clean);
\draw[arrow] (missing) -- node[yesno, right] {否} (clean);
% 阶段二：建模（并行两种方法）
\node[phaselabel=teal] (L2) at (-3.5, -4.5) {模型构建};
\node[step=teal, below=0.8cm of clean] (formulate) {建立数学模型};
\node[substep, below left=0.8cm and 0.8cm of formulate] (method1) {方法A：精确求解};
\node[substep, below right=0.8cm and 0.8cm of formulate] (method2) {方法B：启发式};
\draw[arrow] (clean) -- (formulate);
\draw[arrow] (formulate.south) -- ++(0,-0.3) -| (method1.north);
\draw[arrow] (formulate.south) -- ++(0,-0.3) -| (method2.north);
\node[note, right=0.3cm of formulate] {目标函数\\约束条件\\决策变量};
% 阶段三：对比选优
\node[substep, below=0.7cm of method1] (result1) {结果A};
\node[substep, below=0.7cm of method2] (result2) {结果B};
\node[step=orange, below=1.2cm of formulate] at (0, -8.5) (compare) {方法对比与选优};
\draw[arrow] (method1) -- (result1); \draw[arrow] (method2) -- (result2);
\draw[arrow] (result1.south) |- (compare.west);
\draw[arrow] (result2.south) |- (compare.east);
% 阶段四：验证
\node[step=orange, below=0.7cm of compare] (verify) {结果验证与分析};
\node[step=red, below=0.7cm of verify] (sense) {灵敏度/稳健性分析};
\node[step=red, below=0.7cm of sense] (output) {输出最终方案};
\draw[arrow] (compare) -- (verify); \draw[arrow] (verify) -- (sense); \draw[arrow] (sense) -- (output);
\end{tikzpicture}
\caption{问题一求解流程}
\label{fig:solve-flow-q1}
\end{figure}
```

### TikZ 通用样式速查

```latex
% 在 tikzpicture 外部定义（放在 preamble 或 figure 环境开头）
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, calc, decorations.pathreplacing, shadows}

% 常用颜色搭配（按阶段）
% 阶段一：blue    阶段二：teal    阶段三：orange    阶段四：red
% 辅助/数据：gray  高亮/核心：purple

% 节点间距参考
% 紧凑型：node distance=0.5cm and 0.8cm
% 标准型：node distance=0.8cm and 1.2cm
% 宽松型：node distance=1.2cm and 2cm

% 箭头样式
% 主流程：-{Stealth[length=5pt]}, line width=0.7pt, color=gray!70
% 数据流：-{Stealth[length=4pt]}, line width=0.5pt, dashed, color=gray!40
% 反馈：-{Stealth[length=4pt]}, line width=0.5pt, dashed, color=red!40
```
