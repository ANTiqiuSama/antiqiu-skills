## 22. Paired Dot Plot — 配对点图（个体变化连线 + 均值偏移箭头 + 显著性）

**场景**: 展示配对观测（同一受试者/样本在两种条件下的值）。每条线连接同一实体的前后值，揭示分组柱状图隐藏的个体差异。常见于医学、A/B 测试和实验设计论文。

```python
import numpy as np
import matplotlib.pyplot as plt
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS
setup_style()

np.random.seed(42)
n = 20
labels = ['Before', 'After']
before = np.random.normal(75, 8, n)
after = before + np.random.normal(5, 4, n)  # general improvement with variance

fig, ax = plt.subplots(figsize=(5, 6))

# Individual paired lines
for i in range(n):
    color = PALETTE[0] if after[i] > before[i] else PALETTE[1]
    ax.plot([0, 1], [before[i], after[i]], color=color, alpha=0.35,
            linewidth=1.2, zorder=2)
    ax.scatter([0, 1], [before[i], after[i]], color=color, s=30,
               edgecolors='white', linewidths=0.5, zorder=3, alpha=0.6)

# Mean markers (large, prominent)
mean_before, mean_after = before.mean(), after.mean()
ax.scatter(0, mean_before, s=200, color=PALETTE[1], marker='D',
           edgecolors='white', linewidths=2, zorder=5, label=f'Mean Before: {mean_before:.1f}')
ax.scatter(1, mean_after, s=200, color=PALETTE[0], marker='D',
           edgecolors='white', linewidths=2, zorder=5, label=f'Mean After: {mean_after:.1f}')

# Mean shift arrow
ax.annotate('', xy=(1, mean_after), xytext=(0, mean_before),
            arrowprops=dict(arrowstyle='->', color=COLORS['text'], lw=2.5,
                            connectionstyle='arc3,rad=0.15'))
delta = mean_after - mean_before
ax.text(0.5, (mean_before + mean_after) / 2 + 2,
        f'Δ = +{delta:.1f}', ha='center', fontsize=10, fontweight='bold',
        color=PALETTE[0],
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor=PALETTE[0], alpha=0.9))

# Significance annotation
from scipy import stats
t_stat, p_val = stats.ttest_rel(after, before)
sig_text = f'p = {p_val:.4f}' if p_val >= 0.001 else 'p < 0.001'
ax.text(0.5, max(max(before), max(after)) + 4, sig_text,
        ha='center', fontsize=9, fontstyle='italic', color=COLORS['text'])

ax.set_xticks([0, 1])
ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
ax.set_ylabel('Score', fontsize=11)
ax.set_xlim(-0.4, 1.4)
ax.legend(loc='lower right', fontsize=8, frameon=False, edgecolor=COLORS['grid'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.1, linestyle='--')
fig.tight_layout()
save_fig(fig, 'figures/fig_paired_dot.pdf')
```

**⚠ 易踩的坑（Paired Dot Plot 专用）：**
```python
# 1. 显著性标注不要与数据点重叠：放在 y 位置 = max(data) + offset
# 2. 均值偏移箭头放在图右侧空白区域，不要穿过数据点之间
# 3. 个体变化线用低 alpha（0.3），不要遮挡均值标记
# 4. p 值标注放在数据上方（fontsize=8），不要太大
```

---