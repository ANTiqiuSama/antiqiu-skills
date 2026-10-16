## 13. Dot Plot with CI — 点图+置信区间（按显著性渐变着色 + 汇总菱形）

**场景**: 多方法多指标对比。比柱状图信息密度更高——同时展示显著性、汇总估计和各自的置信区间。Nature/Cell 风格。

```python
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten; from _utils.vivid_config import palette_colors
setup_style(); scale_colors = palette_colors()
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

methods = ['Ours', 'BERT', 'GPT-4', 'LLaMA', 'T5']
metrics = ['Acc', 'F1', 'Prec', 'Rec']
scores = np.array([[0.92, 0.90, 0.91, 0.89],
                    [0.88, 0.86, 0.89, 0.84],
                    [0.90, 0.88, 0.87, 0.90],
                    [0.85, 0.83, 0.86, 0.81],
                    [0.87, 0.85, 0.88, 0.83]])
ci = np.random.uniform(0.01, 0.03, scores.shape)

# Compute p-values (simulated) for gradient coloring
np.random.seed(42)
pvals = np.random.uniform(0.001, 0.1, scores.shape)
pvals[0, :] = np.random.uniform(0.001, 0.01, 4)  # Ours is most significant

fig, ax = plt.subplots(figsize=(8, 5))

# Subtle grid
ax.grid(axis='x', alpha=0.15, linestyle='-', color=COLORS['grid'])
ax.set_axisbelow(True)

y_base = np.arange(len(methods))
offsets = np.linspace(-0.25, 0.25, len(metrics))

# Gradient colormap for significance
cmap_sig = mcolors.LinearSegmentedColormap.from_list('sig', [scale_colors[1], scale_colors[4] if len(scale_colors) > 4 else scale_colors[0], scale_colors[2] if len(scale_colors) > 2 else scale_colors[0]])

for j, metric in enumerate(metrics):
    for i in range(len(methods)):
        # Color by significance (lower p = greener)
        sig_norm = min(pvals[i, j] / 0.1, 1.0)
        dot_color = cmap_sig(1 - sig_norm)
        ax.errorbar(scores[i, j], y_base[i] + offsets[j], xerr=ci[i, j],
                     fmt='o', color=dot_color, markersize=8, capsize=3,
                     linewidth=1.5, markeredgecolor='white', markeredgewidth=0.8,
                     label=metric if i == 0 else '', zorder=3)

# Pooled estimate diamond for each method
pooled = np.mean(scores, axis=1)
pooled_ci = np.mean(ci, axis=1)
for i in range(len(methods)):
    diamond_x = [pooled[i] - pooled_ci[i], pooled[i], pooled[i] + pooled_ci[i], pooled[i]]
    diamond_y = [y_base[i] + 0.35, y_base[i] + 0.42, y_base[i] + 0.35, y_base[i] + 0.28]
    ax.fill(diamond_x, diamond_y, color=PALETTE[0] if i == 0 else COLORS['ref_line'],
            alpha=0.7, zorder=4)
    ax.text(pooled[i] + pooled_ci[i] + 0.008, y_base[i] + 0.35,
            f'{pooled[i]:.3f}', fontsize=7, va='center', color=COLORS['text'])

ax.set_yticks(y_base)
ax.set_yticklabels(methods, fontsize=10)
ax.set_xlabel('Score', fontsize=11)

# Custom legend
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=PALETTE[j],
                           markersize=8, label=metrics[j]) for j in range(len(metrics))]
legend_elements.append(Line2D([0], [0], marker='D', color='w', markerfacecolor=COLORS['ref_line'],
                               markersize=8, label='Pooled'))
ax.legend(handles=legend_elements, loc='lower right', frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=8, ncol=3)
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_dot_ci.pdf')
```

**⚠ 易踩的坑（Dot Plot with CI 专用）：**
```python
# 1. 数值标签统一放在 CI 右端再偏右：不要放在 CI 内部
# 2. pooled diamond 的标签放在 diamond 右侧：不要放在上方（避免与数据 CI 重叠）
# 3. 自适应高度：_fig_h = max(5, n_studies * 0.4 + 2)
# 4. 基线指标用虚线 axhline，不要用粗横线
```

---
