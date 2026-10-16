## 8. 面积图（渐变填充 + 事件标记线 + 端点标注）

**场景**：时序数据的构成变化趋势，如渠道占比变迁、能源结构演变、市场份额变化。
**要点**：渐变填充层叠、事件标记竖线+标注、端点数值标注、顶部轮廓线。

```python
import numpy as np
import matplotlib.pyplot as plt
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

years = np.arange(2015, 2025)
data = {
    '线上渠道': np.array([15, 20, 28, 35, 42, 48, 55, 60, 65, 68]),
    '线下门店': np.array([60, 55, 48, 42, 38, 35, 30, 28, 25, 22]),
    '其他渠道': np.array([25, 25, 24, 23, 20, 17, 15, 12, 10, 10]),
}

fig, ax = plt.subplots(figsize=(8, 5))

# 渐变填充层叠
cumsum = np.zeros(len(years))
for i, (name, vals) in enumerate(data.items()):
    # 多层渐变填充
    for layer, alpha in enumerate([0.35, 0.20, 0.10]):
        ax.fill_between(years, cumsum + layer * 0.3, cumsum + vals - layer * 0.3,
                        alpha=alpha, color=PALETTE[i], linewidth=0)
    # 原色边框轮廓线
    ax.plot(years, cumsum + vals, color=PALETTE[i], linewidth=1.5, alpha=0.8, label=name)
    cumsum += vals

# 事件标记线
events = {2020: '疫情爆发', 2022: '政策调整'}
for year, event in events.items():
    ax.axvline(x=year, color=COLORS['ref_line'], linestyle=':', linewidth=1, alpha=0.6)
    ax.text(year + 0.1, cumsum.max() * 0.95, event, fontsize=8, color=COLORS['ref_line'],
            rotation=90, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=COLORS['ref_line'], alpha=0.8, linewidth=0.5))

# 端点数值标注
cumsum_end = np.zeros(1)
for i, (name, vals) in enumerate(data.items()):
    y_pos = cumsum_end + vals[-1] / 2
    ax.text(years[-1] + 0.3, y_pos[0], f'{vals[-1]}%',
            fontsize=8, color=PALETTE[i], fontweight='bold', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                      edgecolor=PALETTE[i], alpha=0.8, linewidth=0.5))
    cumsum_end += vals[-1]

ax.set_xlabel('年份', fontsize=11)
ax.set_ylabel('占比 (%)', fontsize=11)
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=9, loc='best')
ax.set_xlim(years[0], years[-1] + 0.8)
ax.grid(alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_area.pdf')
```

**★ 防遮挡技巧（面积图专用）：**
```python
# 1. 事件标记线标签用 rotation=90：竖排文字不会和面积重叠
# 2. 端点标注放在最右侧外：x = years[-1] + 0.3
# 3. 渐变填充 3 层：最内层 alpha=0.35，最外层 alpha=0.10
# 4. xlim 右侧留余量：给端点标注留空间
```

---