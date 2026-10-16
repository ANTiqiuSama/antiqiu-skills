## 28. 可行域图（约束满足分区 + 边界 + 最优点）

**场景**：约束优化 / 参数搜索里，在**两个决策变量**的平面上画出"哪些组合可行、哪些违反约束"，
并标出可行域边界与最优解。适用：线性规划可行域、参数扫描的达标区、
碰撞/干涉判定的安全区（如"(螺距, 盘入圈数) 平面上是否碰撞"）、多约束交集区。
**要点**：可行域是**离散的可行/不可行二分区**（不是连续目标值——那是等高线 #14）。
用 `contourf` 的两档色 或 `pcolormesh` 掩膜画可行/违反两片，叠约束边界线，标最优点。
⛔ 不要把可行域画成一堆散点或条形——那读不出"区域"和"边界"。

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

# ── 数据：两个决策变量网格 + 每点是否可行（真实项目从求解结果读；此处可复现演示）
# 例：x=螺距 pitch∈[0.35,0.55]m, y=盘入圈数 turns∈[1,16]，可行=不碰撞
px = np.linspace(0.35, 0.55, 120)
ty = np.linspace(1.0, 16.0, 120)
X, Y = np.meshgrid(px, ty)
# feasible[i,j]=1 表示该(pitch,turns)组合满足约束（真实项目用求解器逐点判定）
margin = (X - 0.44) * 40 - (Y - 8.0) * 0.6            # 演示用的约束裕度函数
feasible = (margin >= 0).astype(float)

fig, ax = plt.subplots(figsize=(6.6, 5.2))
# 两档填充：可行=主色浅版、违反=灰浅版（语义清晰，不用花哨渐变）
cmap2 = ListedColormap([_lighten(COLORS['down'], 0.72), _lighten(PALETTE[0], 0.55)])
ax.contourf(X, Y, feasible, levels=[-0.5, 0.5, 1.5], cmap=cmap2, zorder=2)
# 可行域边界线（margin=0 那条）
ax.contour(X, Y, margin, levels=[0], colors=[PALETTE[0]], linewidths=2.0, zorder=4)

# 关键阈值参考线（如题给的临界螺距）+ 线旁短标签（不写文字框）
p_crit = 0.44
ax.axvline(p_crit, ls='--', lw=1.4, color=PALETTE[1], zorder=5)
ax.text(p_crit + 0.003, ty.max(), f'临界螺距 {p_crit}', rotation=90, fontsize=8.4,
        ha='left', va='top', color=PALETTE[1], fontweight='bold')

# 最优点：白描边让它从填充里跳出来 + 一个短标签
opt_x, opt_y = 0.45, 11.5
ax.scatter([opt_x], [opt_y], s=150, marker='*', color=PALETTE[4], zorder=8,
           edgecolors='white', linewidths=1.2)
ax.text(opt_x + 0.004, opt_y, ' 最优', fontsize=8.6, va='center',
        color=PALETTE[4], fontweight='bold')

# 可行/违反用图例说明（不在图内写整句），图例去框
legend_items = [
    Line2D([], [], marker='s', ls='', markersize=10, markerfacecolor=_lighten(PALETTE[0], 0.55),
           markeredgecolor=PALETTE[0], label='可行域'),
    Line2D([], [], marker='s', ls='', markersize=10, markerfacecolor=_lighten(COLORS['down'], 0.72),
           markeredgecolor=COLORS['down'], label='违反约束'),
    Line2D([], [], color=PALETTE[0], lw=2.0, label='可行边界'),
]
ax.legend(handles=legend_items, frameon=False, fontsize=8.6, loc='lower left',
          handlelength=1.6, labelspacing=0.3, borderpad=0.25)

ax.set_xlabel('螺距 $p$ (m)', fontsize=10.4)
ax.set_ylabel('盘入圈数', fontsize=10.4)
ax.set_xticks([0.35, 0.40, 0.44, 0.50, 0.55])        # 临界值 0.44 进刻度
ax.set_yticks([1, 4, 8, 12, 16])
ax.tick_params(labelsize=9.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_title('(a) 参数平面可行域与最优解', fontsize=11.4, fontweight='bold', loc='left', pad=6)

fig.subplots_adjust(left=0.10, right=0.97, bottom=0.10, top=0.93)
save_fig(fig, 'figures/fig_feasible_region.pdf')
```

**注意事项**：
```python
# 1. ⛔ 可行域是"分区"不是"目标值"：用 contourf 两档色 或 pcolormesh 掩膜画可行/违反两片，
#    不要用连续 colormap（那读者分不清哪片可行）；更不要退化成散点/条形（读不出区域和边界）。
# 2. 结论（可行域面积占比、最优解坐标与目标值、临界约束是哪条）写进 LaTeX \caption{}，
#    图内只留：边界线 + 阈值线旁短标签 + 最优点一个短标签。不要在图内写多行结论框。
# 3. 边界线用 contour(margin, levels=[0]) 从裕度函数精确画，不要手描一条近似线。
# 4. 多条约束时：每条约束画一条边界线（不同线型），可行域是它们的交集；
#    约束多于 4 条时考虑只画"起决定作用"的活跃约束，其余进 caption 说明。
# 5. 真实项目的 feasible 矩阵必须来自求解器逐点判定（碰撞检测/约束校验），不要用演示裕度函数编造。
```