## 12. 多面板子图（淡色填充 + 原色边框 + 带背景框标签 + 统一风格）

**场景**：多个相关图表组合成一张大图，如同一实验的不同视角、多数据集结果并排展示。
**要点**：(a)(b)(c)(d) 带背景框子图标签、淡色填充+原色边框统一风格、tight_layout 自动对齐。

```python
import numpy as np
import matplotlib.pyplot as plt
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

np.random.seed(42)
fig, axes = plt.subplots(2, 2, figsize=(5.0, 4.9))   # 示例尺寸；保留模板比例，按实际显示尺寸检查字号与布局

# (a) 折线图 — 渐变填充
ax = axes[0, 0]
for i in range(3):
    y = np.cumsum(np.random.randn(10))
    ax.plot(range(10), y, 'o-', color=PALETTE[i], linewidth=1.8, markersize=5,
            markeredgecolor='white', markeredgewidth=0.8, label=f'系列{i + 1}')
    ax.fill_between(range(10), y - 1, y + 1, alpha=0.08, color=PALETTE[i])
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=8)
ax.set_ylabel('累计值', fontsize=10)
ax.grid(alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# (b) 分组柱状图 — 淡色填充 + 原色边框
ax = axes[0, 1]
x = np.arange(5)
for i, label in enumerate(['方法A', '方法B']):
    vals = np.random.uniform(60, 95, 5)
    offset = (i - 0.5) * 0.3
    ax.bar(x + offset, vals, 0.28, color=_lighten(PALETTE[i], 0.4),
           edgecolor=PALETTE[i], linewidth=1.2, label=label)
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=8)
ax.set_ylabel('得分', fontsize=10)
ax.grid(axis='y', alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# (c) 散点图 — KDE 等高线背景
ax = axes[1, 0]
for i in range(3):
    pts = np.random.randn(30, 2)
    ax.scatter(pts[:, 0], pts[:, 1], s=25, alpha=0.6, color=PALETTE[i],
               edgecolor='white', linewidth=0.5, label=f'类{i + 1}')
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=8)
ax.grid(alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# (d) 直方图 — 淡色填充 + 原色边框
ax = axes[1, 1]
for i in range(3):
    vals = np.random.normal(i * 2, 1, 200)
    ax.hist(vals, bins=20, alpha=0.5, color=_lighten(PALETTE[i], 0.4),
            edgecolor=PALETTE[i], linewidth=0.8, label=f'分布{i + 1}')
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=8)
ax.set_ylabel('频次', fontsize=10)
ax.grid(axis='y', alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# ★ 带背景框子图标签（用 set_title 紧贴子图顶部）
for i, ax in enumerate(axes.flat):
    ax.set_title(f'({chr(97 + i)})', fontsize=12, fontweight='bold', loc='left', pad=3)

fig.tight_layout(pad=0.5)
save_fig(fig, 'figures/fig_subplots.pdf')
```

**★ 防遮挡技巧（多面板子图专用）：**
```python
# 1. 子图标签 (a)(b)(c)(d) 用 ax.set_title(loc='left', pad=3) 紧贴子图顶部
#    ⛔ 不要用 ax.text(transAxes) — set_aspect('equal') 时标注会远离子图
# 2. tight_layout(pad=0.5)：紧凑布局，子图不会被压缩
#    ⛔ 不要用 pad=2.0 — 紧凑布局下会导致子图极小
# 3. 每个子图的图例放在各自内部：不要用全局图例
# 4. 统一 fontsize：标题 10pt，标签 8pt，刻度 8pt
# 5. 统一配色：所有子图使用相同的 PALETTE 序列
```