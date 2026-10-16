## 29. Hovmöller — 时空双轴图（时间纵 + 空间横 + 偏离均值色阶 + 事件标注）

**场景**: 气候 / 海洋 / 水文（厄尔尼诺、海温、降水带迁移）。两个连续轴上的二维量纲。X 轴=空间（如经度、纬度），Y 轴=时间（自上而下递增）。

⛔ **不要画反 Y 轴方向**：Hovmöller 约定时间从上往下（即 `ax.invert_yaxis()` 或直接 `extent` 反过来）。

```python
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import matplotlib.pyplot as plt
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten

setup_style()
np.random.seed(42)

# === 模拟数据：60 个月 × 40 个经度 ===
n_time = 60; n_space = 40
months = np.arange(n_time)
lons = np.linspace(120, 280, n_space)  # 太平洋经度
# 季节波动 + 空间波形 + ENSO 信号 + 噪声
seasonal = 0.6 * np.sin(2 * np.pi * months[:, None] / 12)
spatial = 0.3 * np.cos(2 * np.pi * (lons - 180) / 80)[None, :]
enso = np.zeros((n_time, n_space))
# 模拟两个事件
enso[15:25, 10:30] += 1.8 * np.exp(-((np.arange(10)[:, None] - 5)**2 + (np.arange(20)[None, :] - 10)**2) / 30)
enso[40:48, 20:35] -= 1.3 * np.exp(-((np.arange(8)[:, None] - 4)**2 + (np.arange(15)[None, :] - 7)**2) / 25)
data = seasonal + spatial + enso + np.random.normal(0, 0.18, (n_time, n_space))

fig, ax = plt.subplots(figsize=(7, 5))

# ★ 双向色阶（偏离零）— 用 coolwarm 但反转让暖色=正
v = np.nanmax(np.abs(data))
im = ax.imshow(data, aspect='auto', cmap=palette_cmap('diverging'), vmin=-v, vmax=v,
               extent=[lons[0], lons[-1], months[-1], months[0]],
               interpolation='bilinear')

# ★ 零线等高线（可选，帮助读者定位"基线")
cs = ax.contour(lons, months, data, levels=[0], colors=[COLORS['ref_line']],
                linewidths=0.6, alpha=0.5, linestyles='--')

# ★ 事件标注：用半透明矩形圈出
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((lons[10], 15), lons[30] - lons[10], 10,
                        fill=False, edgecolor=COLORS['highlight'],
                        linewidth=1.4, linestyle='-', zorder=5))
ax.text(lons[20], 12, 'El Niño 期', fontsize=8, ha='center',
        color=COLORS['highlight'], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                  edgecolor=COLORS['highlight'], alpha=0.9, linewidth=0.6))

ax.add_patch(Rectangle((lons[20], 40), lons[35] - lons[20], 8,
                        fill=False, edgecolor=PALETTE[0],
                        linewidth=1.4, linestyle='-', zorder=5))
ax.text(lons[27], 53, 'La Niña 期', fontsize=8, ha='center',
        color=PALETTE[0], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                  edgecolor=PALETTE[0], alpha=0.9, linewidth=0.6))

ax.set_xlabel('经度 (°E)', fontsize=10)
ax.set_ylabel('时间（月）', fontsize=10)
ax.tick_params(labelsize=9)

# ★ 右侧 colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.04, aspect=20)
cbar.set_label('SST 距平 (°C)', fontsize=9)
cbar.ax.tick_params(labelsize=8)
cbar.outline.set_linewidth(0.4)
cbar.outline.set_edgecolor(COLORS['grid'])

# 顶部加经度参考标记
ax.axvline(180, color=COLORS['ref_line'], linewidth=0.5, alpha=0.4, linestyle=':')
ax.text(180, -1.5, '日期变更线', fontsize=7, ha='center',
        color=COLORS['ref_line'], style='italic')

fig.tight_layout()
save_fig(fig, 'figures/fig_hovmoller.pdf')
```

**★ 设计要点：**
- **双向 cmap（RdBu_r / coolwarm）+ `vmin=-v, vmax=v`** 让零自动落在中性色
- **时间轴 extent 反向**：让最新数据在底部（约定）
- **事件用矩形框**：不要直接在数据上叠加标签，会遮挡

---
