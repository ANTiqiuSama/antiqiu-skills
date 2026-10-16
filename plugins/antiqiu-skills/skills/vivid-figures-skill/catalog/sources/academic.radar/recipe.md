## 5. Architecture Comparison Radar — 架构对比雷达图

**Use case**: Multiple methods across multiple datasets. Main result figure.
**Upgrades**: Heatmap-style background coloring on bars, rank numbers on top, significance markers (bold = best).

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

datasets = ['CIFAR-10', 'CIFAR-100', 'ImageNet', 'STL-10']
methods = ['Ours', 'ViT', 'ResNet', 'DeiT']
scores = np.array([[95.2, 78.3, 82.1, 93.5], [93.1, 75.8, 80.5, 91.2],
                    [91.5, 73.2, 79.8, 89.8], [92.8, 76.1, 81.2, 90.5]])
stds = np.random.uniform(0.3, 0.8, scores.shape)

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(datasets))
width = 0.18

# Heatmap-style coloring: normalize scores per dataset
for j in range(len(datasets)):
    col_min, col_max = scores[:, j].min() - 2, scores[:, j].max() + 2
    cmap = plt.cm.YlGn
    norm = plt.Normalize(col_min, col_max)
    ranks = np.argsort(np.argsort(-scores[:, j])) + 1  # 1 = best

    for i, method in enumerate(methods):
        offset = (i - len(methods) / 2 + 0.5) * width
        color = cmap(norm(scores[i, j]))
        bar = ax.bar(x[j] + offset, scores[i, j], width, yerr=stds[i, j], capsize=3,
                      color=_lighten(color, 0.35), edgecolor=color, linewidth=1.0,
                      error_kw={'elinewidth': 0.8, 'capthick': 0.6})

        # Rank number on top
        rank = ranks[i]
        is_best = rank == 1
        ax.text(x[j] + offset, scores[i, j] + stds[i, j] + 0.4,
                f'{"★" if is_best else ""}{scores[i, j]:.1f}',
                ha='center', fontsize=7, fontweight='bold' if is_best else 'normal',
                color=COLORS['down'] if is_best else COLORS['text'])

# Method legend (manual)
for i, method in enumerate(methods):
    ax.bar([], [], color=_lighten(PALETTE[i], 0.4), label=method, edgecolor=PALETTE[i], linewidth=1.2)

ax.set_xticks(x)
ax.set_xticklabels(datasets, fontsize=10)
ax.set_ylabel('Accuracy (%)', fontsize=11)
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=9, ncol=len(methods))
ax.set_ylim(68, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.15, linestyle='--')
fig.tight_layout()
save_fig(fig, 'figures/fig_dataset_compare.pdf')
```

**★ 防遮挡技巧（Multi-Dataset Compare 专用）：**
```python
# 1. 排名数字放在柱子内部顶端：fontsize=7, color='white'（深色柱子）或 color=PALETTE[i]（浅色柱子）
# 2. 星号标记放在 error bar 上方：不要放在柱子顶部（会和排名数字重叠）
# 3. 数据集数 >5 时：x 轴标签 rotation=15
# 4. 图例放在图外上方：bbox_to_anchor=(0.5, 1.12), ncol=n_methods
```

---