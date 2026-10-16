## 7. Rain Cloud 图（淡色填充 + 原色边框 + 半小提琴 + 箱线 + 抖动散点 + 均值菱形）

**场景**：分组数据的分布对比，比箱线图更丰富——同时展示密度、统计量和原始数据。
**要点**：淡色填充+原色边框半小提琴、窄箱线图、抖动散点、均值菱形标记、渐变密度填充。

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import matplotlib.colors as mcolors
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

np.random.seed(42)
groups = ['组A', '组B', '组C', '组D']
data = [np.random.normal(loc, s, 80) for loc, s in [(80, 5), (85, 3), (78, 8), (90, 4)]]

# ★ 自适应高度
_fig_h = max(4, len(groups) * 1.2 + 1)
fig, ax = plt.subplots(figsize=(8, _fig_h))

for i, (name, d) in enumerate(zip(groups, data)):
    pos = i

    # 渐变半小提琴（右侧）
    kde = gaussian_kde(d, bw_method=0.3)
    yr = np.linspace(d.min() - 4, d.max() + 4, 300)
    density = kde(yr)
    density_norm = density / density.max() * 0.35

    for layer in range(6):
        frac = layer / 6
        alpha = 0.35 - frac * 0.05
        ax.fill_betweenx(yr, pos + frac * 0.02, pos + density_norm * (1 - frac * 0.12),
                         alpha=alpha, color=PALETTE[i], linewidth=0)
    # 原色边框轮廓
    ax.plot(pos + density_norm, yr, color=PALETTE[i], linewidth=1.2, alpha=0.8)

    # 箱线图（左侧，窄）
    bp = ax.boxplot(d, positions=[pos - 0.18], widths=0.12, vert=True, patch_artist=True,
                    boxprops=dict(facecolor=_lighten(PALETTE[i], 0.4),
                                  edgecolor=PALETTE[i], linewidth=1.2),
                    medianprops=dict(color=COLORS['text'], linewidth=1.8),
                    whiskerprops=dict(linewidth=1, color=PALETTE[i]),
                    capprops=dict(linewidth=1, color=COLORS['ref_line']),
                    flierprops=dict(marker='', markersize=0))

    # 抖动散点（最左侧）
    jitter = np.random.uniform(-0.08, 0.08, len(d))
    ax.scatter(pos - 0.38 + jitter, d, s=6, alpha=0.2, color=PALETTE[i], edgecolor='none')

    # 均值菱形
    ax.scatter(pos - 0.18, d.mean(), marker='D', s=45, color=PALETTE[i],
               edgecolor='white', linewidth=1.2, zorder=5)

    # 均值数值标注
    ax.text(pos - 0.32, d.mean(), f'{d.mean():.1f}', fontsize=7, color=PALETTE[i],
            ha='right', va='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                      edgecolor='none', alpha=0.7))

ax.set_xticks(range(len(groups)))
ax.set_xticklabels(groups, fontsize=10)
ax.set_ylabel('数值', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.12, linestyle='--', color=COLORS['grid'])
fig.tight_layout()
save_fig(fig, 'figures/fig_raincloud.pdf')
```

**★ 防遮挡技巧（Rain Cloud 图专用）：**
```python
# 1. 半小提琴只画右半：左侧留给箱线图和散点
# 2. 均值标注放在箱线图左侧：不要和小提琴重叠
# 3. 组数 >6 时：_fig_h 自动增高（每组 1.2 高度）
# 4. 散点用极小尺寸（s=6）和低 alpha（0.2）：不要遮挡箱线图
```

---