## 3. Pareto 前沿图

**场景**：多目标优化的非支配解集展示，标注极端点、膝点解；可行域与非可行解。多目标优化问题必备。
**要点**：可行域浅色填充、Pareto 前沿粗实线、极端解用不同 marker、方向箭头+"优化方向"标识。

```python
import numpy as np, matplotlib.pyplot as plt
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()
np.random.seed(42)

# Pareto 前沿数据
t = np.linspace(0, 1, 80)
pareto_f1 = 0.8 + 4.8 * t          # 目标1：农业产量（标准化）
pareto_f2 = 4.5 - 4.0 * t**0.7     # 目标2：缺水缺口

fig, ax = plt.subplots(figsize=(7, 6))

# 可行域填充（Pareto 前沿上方）
ax.fill_between(pareto_f1, pareto_f2, 5.5, alpha=0.12, color=PALETTE[0], zorder=0)
ax.text(3.2, 3.5, '可行域', fontsize=13, color=PALETTE[0], fontweight='bold', alpha=0.5)
ax.text(1.5, 1.2, '非可行域', fontsize=11, color=COLORS['ref_line'], alpha=0.5)

# Pareto 前沿线（粗实线）
ax.plot(pareto_f1, pareto_f2, '-', color=COLORS['text'], linewidth=3, zorder=5, label='Pareto 最优前沿')

# 极端解标注 — 不同 marker + 颜色标注框
# 缺水最小极端解（左上）
ax.scatter(pareto_f1[0], pareto_f2[0], marker='s', s=150, color=COLORS['up'],
           edgecolor='white', linewidth=1.5, zorder=6)
ax.annotate('缺水最小极端解\n(min$G_t$，$Z_1$ 最小)',
            xy=(pareto_f1[0], pareto_f2[0]),
            xytext=(pareto_f1[0] + 0.3, pareto_f2[0] + 0.3),
            fontsize=8.5, color=COLORS['up'], fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=COLORS['up'], lw=1.2),
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=COLORS['up'], alpha=0.9))

# 均衡折中解（中间，五角星）
knee_idx = len(t) // 2 + 5
ax.scatter(pareto_f1[knee_idx], pareto_f2[knee_idx], marker='*', s=300,
           color=COLORS['highlight'], edgecolor='white', linewidth=1.5, zorder=6)
ax.annotate('均衡折中解（膝点）\n$\\omega_1 Z_1 + \\omega_2 G_t$ 最优',
            xy=(pareto_f1[knee_idx], pareto_f2[knee_idx]),
            xytext=(pareto_f1[knee_idx] + 0.5, pareto_f2[knee_idx] + 0.6),
            fontsize=8.5, color=COLORS['highlight'], fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=COLORS['highlight'], lw=1.2),
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=COLORS['highlight'], alpha=0.9))

# 产量最大化极端解（右下，菱形）
ax.scatter(pareto_f1[-1], pareto_f2[-1], marker='D', s=120, color=COLORS['down'],
           edgecolor='white', linewidth=1.5, zorder=6)
ax.annotate('产量最大化极端解\n(max$Z_1$，$G_t$ 较大)',
            xy=(pareto_f1[-1], pareto_f2[-1]),
            xytext=(pareto_f1[-1] - 1.5, pareto_f2[-1] - 0.5),
            fontsize=8.5, color=COLORS['down'], fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=COLORS['down'], lw=1.2),
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=COLORS['down'], alpha=0.9))

# 方向箭头
ax.annotate('', xy=(2.0, 0.15), xytext=(0.5, 0.15),
            arrowprops=dict(arrowstyle='->', color=COLORS['ref_line'], lw=1.2, linestyle='--'))
ax.text(1.25, 0.0, '$Z_1$ 增大方向', fontsize=8, color=COLORS['ref_line'], ha='center')
ax.annotate('', xy=(0.3, 1.8), xytext=(0.3, 0.5),
            arrowprops=dict(arrowstyle='->', color=COLORS['ref_line'], lw=1.2, linestyle='--'))
ax.text(0.15, 1.15, '$G_t$ 减小方向', fontsize=8, color=COLORS['ref_line'],
        ha='center', rotation=90)

ax.set_xlabel('农业产量 $Z_1$（标准化值）', fontsize=11)
ax.set_ylabel('缺水缺口 $G_t$（标准化值）', fontsize=11)
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=9, loc='best')
ax.set_xlim(0, 6.2)
ax.set_ylim(0, 5.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_pareto.pdf')
```

**⚠ Pareto 前沿图定制生成注意事项：**
```python
# 1. 极端解标注不要互相重叠（3 个标注分别在不同方向：左上/右上/右下）
# 2. 方向标注箭头放在图边缘空白处，不要和 Pareto 前沿线或数据重叠
# 3. 方向箭头放在图边缘空白处，不要让标注超出图表边界
# 4. 非支配解用小圆点（s=20），支配解用更小的点（s=8, alpha=0.3）
# 5. 实际查看 xytext 标注与边界和数据的关系；plot_utils 不会自动解决遮挡或裁切
```

---
