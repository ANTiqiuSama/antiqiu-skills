# 按需参考

选定模板后的适配以完整源码和卡片保留要点为准；以下示例仅在确有需要时使用，不作为重写已选模板的理由。

### 15. ★★ 版面精调六件套（"看起来专业"的直接来源，实测差距最大的一组）

对 94 张真实竞赛图统计：高分图集和平庸图集在这六项上的差距是**压倒性**的（前者 46%-82% 都做，
后者 0%-17%）。**图型选对了但还是显得"业余"，八成是这六项没做。**
⛔ 下面给的数值是精调后的参考量级，**按你的图实际调整，不要当死数照抄**。

**① 手动指定刻度位置（差距最大：82% vs 7%）**
matplotlib 默认刻度经常给出 `0 / 2.5 / 5.0 / 7.5` 这种无意义分割，或者密到糊掉。
自己按**数据语义**挑刻度，尤其**把关键阈值/上限/范围端点塞进刻度**——读者能直接从轴上读出结论：

```python
ax.set_xticks([4, 8, 12, 16, 21])        # 21 是题给硬上限 → 进刻度，一眼看出实测顶到上限
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0])   # 0.9 是 Q90 判据线 → 单独加一个刻度
# 数据范围很窄时（如 0.41~0.44）别让 matplotlib 给 0/0.2/0.4，那样细节全糊：
ax.set_yticks([0.41, 0.42, 0.43, 0.44])
# 刻度本身无意义时（状态矩阵、类别条形的位置轴）主动清空，别留一排没用的数字：
ax.set_yticks([])
```

**② 保留一致的字号层次**
沿用模板中不同角色的字号。需要统一调整时可以提取为常量，不因代码中有多个字号就重设整图：

```python
FS_ANNO, FS_TICK, FS_LAB, FS_TITLE, FS_LEG = 8.4, 9.0, 10.4, 11.4, 8.6
#         标注    刻度    轴标签   面板标题  图例
ax.set_xlabel('...', fontsize=FS_LAB)
ax.tick_params(labelsize=FS_TICK)
ax.set_title('(a) ...', fontsize=FS_TITLE, fontweight='bold', loc='left', pad=5)
```
层级关系（**标注 < 刻度 < 轴标签 < 面板标题**）比具体数值更重要。

#### figsize 与最终显示尺寸

以所选模板的画布比例、面板结构和字号层次为起点，再按实际交付宽度、高度限制与数据量局部适配。
论文单栏、通栏、独立 PNG 和屏幕展示的显示尺寸不同，不能从图的长宽比推定一个通用引用宽度。

绘制前计算：

```text
缩放比 = 最终显示宽度 ÷ 原生画布宽度
显示字号 = 代码字号 × 缩放比
显示线宽 = 代码线宽 × 缩放比
```

若最终高度也有限制，使用宽、高限制共同决定的实际缩放比。`fig_include_size.py` 的排版默认值
只适用于实际使用该排版方案的文稿，不是所有绘图任务的原生尺寸要求。

- 显示尺寸已知时，在该尺寸下检查文字、线条与间距；未知时沿用模板并说明适合的显示方式。
- 不固定原生宽度、原生高度、缩放比或最小字号。原生画布较大不等于图不合格，数值示例也不是全库阈值。
- 拥挤时在原代码上调整必要的画布、面板间距、标签位置和字号；同时核对最终显示效果。
  不为满足固定尺寸机械收窄画布，也不只放大画布而忽略缩放后文字是否清楚。
- 同轴单位和数量级应适合比较；确需拆分面板或减少展示项时，依据分析目的处理并说明范围。
  不按固定条目数自动换图、截取 Top N 或删除模板信息层。

#### 多 panel 共用 colorbar：按布局选择 `ax=axes` 或独立 `cax`

**当前保存行为：** `save_fig` 保留已有画布和布局，不自动调用 `tight_layout`、收缩画布或移动标注。
若绘图代码显式调用 `tight_layout`，需留意它是否重算 `fig.colorbar(sm, ax=axes)` 预留的空间。
出现面板与色条重叠时，统一调整所需空间，再检查实际渲染。
`fraction`、`pad` 或独立 `cax` 均可按具体布局使用；优先保留模板已有方案。
需要时可以显式使用 `constrained_layout=True`；样式默认关闭它，不代表禁止使用。
同一张图选用相容的布局方式，避免再叠加 `tight_layout` 重排。

**一种可选写法 —— 把 cax 做成 gridspec 的一列，为色条明确留位：**
```python
fig = plt.figure(figsize=(5.4, 4.9))                      # 示例尺寸；按模板比例和实际交付尺寸适配
gs  = fig.add_gridspec(2, 3, width_ratios=[1, 1, 0.055],  # 第3列留给 colorbar
                       wspace=0.30, hspace=0.34)
axes = np.array([[fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])],
                 [fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])]])
cax  = fig.add_subplot(gs[:, 2])                          # 跨两行
cbar = fig.colorbar(sm, cax=cax)                          # 此布局显式使用独立色条轴
cbar.set_label('...', fontsize=9.5, labelpad=8)           # 标签长了会撞自己的刻度 → 加 labelpad
cbar.ax.tick_params(labelsize=8.5)
```
- 单 panel 也可用 `fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.03)`；仍需检查色条、标签与主图的实际间距。
- colorbar 标签**宁短勿长**：`把手序号（龙头→龙尾）` 就够，详细口径写进 `\caption{}`
  （实测长标签 `把手节号（0=龙头 → 223=龙尾后把手）` 会横跨过去压到自己的刻度数字上）

#### 共享坐标的多 panel 可减少重复轴标签
若各面板含义和单位一致，可只在外侧保留共同轴标签；不同指标的面板应保留各自标签。以下为共享坐标示例：
```python
for i, ax in enumerate(axes.flat):
    if i >= 2:      ax.set_xlabel('x (m)', fontsize=9.5)   # 只下排
    if i % 2 == 0:  ax.set_ylabel('y (m)', fontsize=9.5)   # 只左列
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))       # 画布小了刻度会挤 → 限档数
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
```

**③ 按模板安排图例**
保留模板的图例位置、边框和间距。需要更紧凑的无框图例时可参考下例；不因 `frameon=True` 就自动去框：

```python
ax.legend(frameon=False,          # ★ 去掉那个灰框
          fontsize=FS_LEG,
          handlelength=1.7,       # 默认 2.0 偏长
          labelspacing=0.28,      # 默认 0.5 偏松
          handletextpad=0.36,
          borderpad=0.2,
          loc='upper right')      # 位置按数据空白区挑，挤就 bbox_to_anchor 移轴外
```

**④ 浅色填充 + 主色描边（`_lighten` 用了 113 次 vs 0 次）**
这是"层次感"最廉价也最有效的来源：**填充用同色浅版、边线用主色**，而不是整块实色。
比"每个系列换一个色相"高级得多，也不会让图变成调色盘：

```python
ax.stairs(counts, edges, fill=True,
          color=_lighten(PALETTE[0], 0.50),   # 填充：主色的浅版（0.4~0.6 最常用）
          edgecolor=PALETTE[0], lw=1.5)       # 描边：主色本身
ax.bar(x, y, color=_lighten(PALETTE[1], 0.44), edgecolor=PALETTE[1], linewidth=1.4)
ax.fill_between(x, lo, hi, color=_lighten(PALETTE[2], 0.60), alpha=0.42)  # 置信带更浅
```
`_lighten` 系数经验值：**主体填充 0.4~0.5**、**背景带/次要元素 0.55~0.7**、**渐变起点 0.6~0.8**。

**⑤ `zorder` 分层 + 关键点白描边（95% / 86%）**
不设 `zorder` 时数据可能被网格线或填充压住；关键标记点加白描边能从密集背景里"跳出来"：

```python
# 层次约定：参考带/网格 0-2 → 填充 3 → 数据主体 4-6 → 关键标记 7-9
ax.fill_between(x, lo, hi, color=..., alpha=0.2, zorder=2)
ax.plot(x, y, lw=2.0, color=PALETTE[0], zorder=6)
ax.scatter(x_key, y_key, s=86, color=PALETTE[2], zorder=8,
           edgecolors='white', linewidths=1.1)      # ★ 白描边=从背景里跳出来
ax.plot(x, y, '-o', markersize=4.4, markeredgecolor='white', markeredgewidth=0.7)
```

**⑥ 多 panel 用 `subplots_adjust` 手动抠边距（46% vs 0%）**
显式调用 `tight_layout()` 后若留白或标签位置不合适，可手动调整多 panel 布局；保存本身不会自动重排：

```python
gs = gridspec.GridSpec(2, 2, hspace=0.44, wspace=0.24,   # 子图间距：0.24~0.52 常用
                       height_ratios=[1.0, 1.06])        # 行高微调（下排放长标签就给多点）
# ... 画完所有 panel 后 ...
fig.subplots_adjust(left=0.075, right=0.985, bottom=0.062, top=0.945)
```
判据：**打开图看四周白边是否均匀、有没有标签被裁**。`hspace` 不足时下排 panel 的 x 轴标签会
顶到上排 panel 的底部——这是多 panel 图最常见的挤压。

## 避免的常见丑图

- ❌ 默认蓝色单色（用多色配色方案）
- ❌ 图内加 `plt.title()`（标题只在 LaTeX caption 中）
- ❌ 默认灰色网格线（去掉或用极淡的虚线）
- ❌ 图例遮挡数据（放在空白区域或图外）
- ❌ 坐标轴标签用变量名（如 `col_1`，应改为有意义的中文/英文标签）
- ❌ 字体太小（打印后看不清）
- ❌ 连续色图绕过项目配色（按数据语义使用 `palette_cmap`）

## ⛔ 防遮挡规则（文字/数据/曲线互相遮挡是最常见的图表质量问题）

### 注释沿用模板，长解释放图外

保留原模板已有的指标框、代表点说明、引线和数值标签，按真实数据更新内容与位置。
注释是否合适取决于作用、占用空间和实际遮挡，不按行数、数量、白底或圆角统一判错。

- 新增的方法解释、统计口径和长结论优先放图注或随图说明；独立图片交付也可附简短文字说明。
- 确需新增图内注释时，沿用模板的字体、边框、背景与引线样式，为它安排空白空间。
  不把长说明塞进原来的小指标框；内容增加后重新检查框的位置、大小与数据层级。
- 坐标轴标签、单位、图例、色条及直接数据标注承载读图所需信息，不能为了少写字删掉。
- 出现遮挡时优先在源码上局部调整位置、引线、间距或文字长度。仅提高 `zorder` 把数据盖住不算解决。

### 图例位置
- 沿用模板已有的位置。`loc='best'`、手动位置和轴外图例均可，按数据空白和最终画布边界选择。
- 不凭系列数量自动移动图例，不要求把正常工作的图例改成 `auto_legend`。
- 自动选位也可能遮挡数据，仍需打开成图检查。

### 数值与点标注
- 模板的 `ax.text`、`annotate`、`bar_label` 或直接数据标签均可保留；标签在柱内或柱外由模板与可读性决定。
- 数据更新后若发生重叠，可手动调整偏移，或按需使用 `smart_labels` / `adjustText`；这些工具不保证无重叠。
- 森林图的文字列、热图数值、多个代表点和短指标框可包含多项信息，不套用统一数量配额。
- 多条参考线的标签应错开或使用短代号配合图例，不能因模板留有参考线就补造没有依据的阈值。

### 曲线/数据点重叠
- **多条折线重叠**：用不同线型（实线/虚线/点线/点划线）+ 不同标记（o/s/^/D）区分
- **散点图数据密集**：降低 `alpha=0.5-0.7`，或用 hexbin/KDE 等高线代替
- **多组箱线图/小提琴图**：按类别间距和模板布局调整琴体/箱体宽度，避免相邻组互相遮挡。

### 坐标轴标签
- **长标签**：用 `rotation=45, ha='right'` 斜着显示，或换行 `'第一行\n第二行'`
- **长中文标签**：按可用空间换行、调整间距或采用不损失含义的简称，不设置统一字数上限。
- **刻度太密**：用 `ax.xaxis.set_major_locator(MaxNLocator(nbins=6))` 减少刻度数

### 通用技巧
```python
# 布局需要时显式调整；不与其他布局方案机械叠加
fig.tight_layout()

# 散点标注防重叠（需要 pip install adjustText）
from adjustText import adjust_text
texts = [ax.text(x[i], y[i], labels[i], fontsize=8) for i in range(len(x))]
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

# 先检查标签和边界，再保存；保存函数本身不调整布局
save_fig(fig, 'xxx.pdf')
```
