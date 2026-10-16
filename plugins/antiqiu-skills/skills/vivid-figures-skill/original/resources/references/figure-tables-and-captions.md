# 论文表格与引用

仅在交付包含表格或论文引用时读取；用户的格式要求优先。

### Step 5: Generate tables (LaTeX OR Markdown — pick by output mode)

**⛔ FIRST: detect output format mode**

```bash
echo "=== 检测输出格式 ==="
# 从统一项目配置读取输出格式
OUTPUT_FORMAT=$(python _utils/vivid_config.py get output_format)
OUTPUT_FORMAT=${OUTPUT_FORMAT:-pdf}
echo "Output format: $OUTPUT_FORMAT"

# 学术写作四大模板始终是 docx 模式（即使 output_format 没明写）
TEMPLATE=$(python _utils/vivid_config.py get template)
case "$TEMPLATE" in
    thesis_proposal|literature_review|course_paper|course_report)
        OUTPUT_FORMAT=docx
        echo "学术写作模板，强制 docx 模式"
        ;;
esac

if [ "$OUTPUT_FORMAT" = "docx" ]; then
    TABLE_EXT="md"
    echo "⛔ Word/DOCX 模式：表格输出 .md（Markdown 三线表）"
else
    TABLE_EXT="tex"
    echo "PDF 模式：表格输出 .tex（booktabs 三线表）"
fi
echo "TABLE_EXT=$TABLE_EXT (将用于 figures/TABLE_*.${TABLE_EXT})"
```

**⛔ At minimum: main results comparison table + descriptive statistics table.**
- PDF 模式 → Save as `figures/TABLE_xxx.tex`（booktabs 三线表）
- Word/DOCX 模式 → Save as `figures/TABLE_xxx.md`（Markdown 三线表）

**⛔ For Chinese papers: table captions and column headers MUST be in Chinese.** Check TOPIC_PLAN.md or PROBLEM_ANALYSIS.md to determine paper language. If Chinese (stats modeling / math modeling competition), all `\caption{}` and column headers must use Chinese.

**⛔⛔ 表注只写短标题（中文 ≤20 字 / 英文 ≤14 词）**：`\caption{}` 只写"这张表是什么"的名词短语，**统计口径（重复次数/置信区间/随机数种子）、结论、数据来源全部进正文**，一个字都别塞进表注。正例 `\caption{各体积分数下的导通概率}`；反例 `\caption{问题二四个题给体积分数下的导通概率（$T$=1000 次独立重复……数据来源：\texttt{results/xxx.json}。}`。详见本步末尾 `<table_sizing>` 的表注铁律与「为什么表注更容易写超」。

**⛔ DOCX 模式下 Markdown 三线表的标准格式（必须遵守）：**

```markdown
**表 1：模型性能对比**

| 模型 | RMSE | MAE | R² |
|---|---|---|---|
| LSTM | 0.023 | 0.018 | 0.94 |
| Transformer | 0.019 | 0.015 | 0.96 |
| XGBoost | 0.021 | 0.017 | 0.95 |

> 注：所有指标基于测试集；最优值已加粗。

<!-- label: tab:model_perf -->
```

铁律：
- 表标题：`**表 X：标题**`（不是 `\caption{}`）
- 表头单独一行 `| h1 | h2 |`，**接下来必须有分隔行** `|---|---|`
- 每行 `|` 数量必须一致（列数对齐）
- 单元格里的 `|` 必须转义为 `\|`
- 表注：`> 注：xxx`（引用块）
- ⛔ **不要**在 .md 里写 `\begin{table}` / `\begin{tabular}` / `\toprule` / `\midrule` / `\bottomrule`
- ⛔ **不要**输出 .tex 文件（Word 模式根本不读）

**调用 stats_utils 时按后缀输出对应格式：**

```python
from _utils.stats_utils import regression_table, descriptive_table

# 自动按后缀选格式（推荐）
ext = "md" if output_format == "docx" else "tex"
regression_table(results, ['OLS', 'Logit'],
                 output=f'figures/TABLE_regression.{ext}',
                 caption='回归结果')
descriptive_table(df, output=f'figures/TABLE_descriptive.{ext}')
```

<table_sizing>
**⛔⛔ 表注（`\caption`）只写短标题：中文 ≤20 字 / 英文 ≤14 词，与图注同一口径。**
表格本身就是数字载体，**不存在**「图内文字遮挡数据」那个刚需，所以**统计口径、结论、数据来源一律进正文**，不要塞进表注。

- ✅ `\caption{各体积分数下的导通概率}`（11 字）
- ❌ `\caption{问题二四个题给体积分数下的导通概率（$T$=1000 次独立重复，公共随机数）。$P$ 随 $f_A$ 严格单调上升，八点扫描的反序数为 0……数据来源：\texttt{results/problem\_2\_results.json}。}`（292 字）

**★ 为什么表注比图注更容易写超（必读）**：正文引**图**时是「复制 `figure` 块 → 改 caption」，caption 会被过一遍手、顺带精简；而**表**是 `\input{figures/TABLE_*.tex}` **直通 PDF**——你在这里写多长，论文里就是多长，**没有任何中间精简环节**。实测某工作区 6 张表因此平均 391 字、最长 546 字，表头下方糊成一整段。编译期 `writing_check.sh` 会递归跟随 `\input` 扫表注长度，超限判违规。

**LaTeX 模式（.tex）：**
- Narrow tables (≤4 columns): do not use `\resizebox` — it stretches text to full width, font becomes huge
- Wide tables (≥6 columns): wrap with `\resizebox{\textwidth}{!}{...}` to prevent overflow
- Use three-line style (booktabs): `\toprule`, `\midrule`, `\bottomrule`
- **⛔ Tall tables (>30 rows or multirow causing >35 visual rows)**: use `longtable` environment or split into multiple smaller tables. A single `tabular` that exceeds one page will be silently truncated.
- **⛔ Hyperparameter/config tables**: if models have very different parameter counts (e.g., Linear Reg 2 params vs LSTM 9 params), split into separate small tables per model or use `longtable`. Do not cram all models into one huge tabular.

**Markdown 模式（.md）：**
- 列数 ≤ 8（Word 渲染列数过多会挤压）；超过 8 列必须横向拆分
- 数据行 ≤ 25（超过 25 行的表格在 Word 里跨页效果差）；超过的拆为「正文摘要表 + 附录完整表」
- 单元格内不要换行（`<br>` Word 不一定渲染）
- 不要嵌套表格（Markdown 不支持）
- 数值精度统一：百分比保留 2 位小数（94.72%），系数保留 3-4 位（0.0234）
</table_sizing>

### Step 6: Generate LaTeX include snippets

Save to `figures/latex_includes.tex`. Figures use `[H]` float specifier (pinned in place to prevent multi-figure stacking); tables use `[H]` (requires `\usepackage{float}`).

**⛔ Captions must match paper language.** Check TOPIC_PLAN.md or PROBLEM_ANALYSIS.md:
- Chinese papers (stats modeling / math competition): `\caption{模型性能对比雷达图}` — Chinese caption
- English papers (MCM/ICM/APMCM): `\caption{Model Performance Comparison}` — English caption

**★★ 图注（figure caption）要承载结论，别只写一个图名**（实测常见毛病：图内塞满结论文字框、caption 却只有"随轨道相位的变化"这样一句，正好写反了）。图注是**图内文字的去处**——写长不占版面、不遮挡数据、还能被检索。推荐结构：

> ⛔ **本节只管图注，不要套用到表注。** 表注按 `<table_sizing>` 的铁律写短标题（≤20 字），结论进正文——表格是数字载体，没有「图内文字遮挡数据」这个前提，而且表是 `\input` 直通 PDF、没有精简环节。曾有工作区把这套长 caption 规范套到 6 张表上，平均 391 字、最长 546 字。

> **一句话讲图型与内容** → **多 panel 逐个说明 (a)(b)(c)** → **关键结论数值** → 必要的数据来源/口径

```latex
% ❌ 太干：结论无处安放，读者只能去图里挤着看
\caption{相对论钟速率随轨道相位的变化}

% ✅ 结论进图注：图内因此只需留极简锚点，两边都清爽
\caption{相对论钟速率沿轨道相位的变化。(a) 速度项 $v^2/2c^2$ 与引力项 $GM_E/rc^2$
分别随相位振荡，量级均为 $10^{-10}$；(b) 两项之和的单圈累积达 5473\,ns，
折合每日 83.4\,$\mu$s，远超 0.1\,$\mu$s 的定位精度需求，故该项不可忽略。
数据源：problem\_3\_results.json（轨道积分 1200 周期）。}
```

⛔ 图内被搬走的结论**必须在 caption 里出现**，否则是丢信息不是搬信息。

**⛔ Axis labels in gen_fig_*.py must also match paper language:**
- Chinese: `ax.set_xlabel('迭代次数')`, `ax.set_ylabel('目标函数值')`, `label='本文算法'`
- English: `ax.set_xlabel('Iterations')`, `ax.set_ylabel('Objective Value')`, `label='Ours'`
