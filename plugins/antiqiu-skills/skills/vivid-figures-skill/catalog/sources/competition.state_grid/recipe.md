## 29. 离散状态栅格图（仿真逐帧/逐时隙状态热图）

**场景**：把离散事件仿真、排队/调度、重传轮次、设备状态机的**逐帧逐单元状态**铺成栅格，
一眼看出"什么时候谁在什么状态"。适用：CSMA/CA 时隙占用、机器加工甘特栅格、
病床/车位占用、重传轮次分布、元胞自动机时空快照。
**要点**：状态是**离散类别**（不是连续值），所以必须用 `ListedColormap` + `BoundaryNorm`
配离散色带，`colorbar` 的刻度标签写成人话（"首传成功/1轮重传/..."）；格子间加白描边分隔。
⛔ 不要用连续 colormap（viridis 之类）画离散状态 —— 读者无法判断色深对应哪一档。

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

# ── 数据：n_unit 行(单元/槽位) × n_frame 列(帧/时隙)，值 = 离散状态编码
#    真实项目里从仿真结果 JSON 读；此处用可复现的随机演示
rng = np.random.default_rng(7)
n_unit, n_frame = 16, 40
Z = rng.choice([0, 1, 2, 3], size=(n_unit, n_frame), p=[0.70, 0.18, 0.09, 0.03])
Z = Z.astype(float)
Z[rng.random(Z.shape) < 0.05] = np.nan          # 空缺单元用 nan，画成空白不画死0

STATE_NAMES = ['0（首传成功）', '1 轮重传', '2 轮', '3 轮']
# 离散色带：低档用浅色、高档用醒目色（语义递进），一律走 PALETTE 派生
CMAP = ListedColormap([_lighten(PALETTE[2], 0.42), _lighten(PALETTE[5], 0.20),
                       PALETTE[1], PALETTE[4]])
BOUNDS = [-0.5, 0.5, 1.5, 2.5, 3.5]            # 每档一个区间，边界卡在半整数
NORM = BoundaryNorm(BOUNDS, CMAP.N)

fig, ax = plt.subplots(figsize=(7.2, 4.4))
pc = ax.pcolormesh(np.arange(n_frame + 1) - 0.5, np.arange(n_unit + 1) - 0.5,
                   np.ma.masked_invalid(Z), cmap=CMAP, norm=NORM,
                   edgecolors='white', linewidth=0.30, zorder=3)

cb = fig.colorbar(pc, ax=ax, shrink=0.82, aspect=16, pad=0.03, ticks=[0, 1, 2, 3])
cb.set_ticklabels(STATE_NAMES)                  # ★ 离散标签写人话，不写 0/1/2/3
cb.set_label('该单元的状态档位', fontsize=10)
cb.ax.tick_params(labelsize=8.4)

ax.set_xlabel('帧 / 时隙序号 $k$', fontsize=10)
ax.set_ylabel('单元 / 槽位序号', fontsize=10)
ax.set_xticks([0, 9, 19, 29, 39]); ax.set_xticklabels(['1', '10', '20', '30', '40'])
ax.set_yticks([0, 3, 7, 11, 15]);  ax.set_yticklabels(['1', '4', '8', '12', '16'])
ax.tick_params(labelsize=9)
ax.set_title('(a) 仿真逐帧状态栅格', fontsize=11, fontweight='bold', loc='left', pad=6)

fig.tight_layout()
save_fig(fig, 'figures/fig_state_grid.pdf')
```

**注意事项**：
```python
# 1. ⛔ 栅格铺满坐标区，图内没有空白可放文字 —— 统计结论（首传成功率/最大重传轮次/丢包数/
#    仿真总帧数）一律写进 LaTeX \caption{}，不要用 ax.text 压在格子上（会盖住首行数据）。
# 2. 展示帧数控制在 30-60 列：真实仿真跑几千帧时取前 N 帧展示，并在 caption 说明
#    "取前 40 帧展示，共运行 1200 帧"，不要把几千列硬塞进一张图（格子细成条纹看不清）。
# 3. 空缺/未定义单元用 np.nan + masked_invalid 画成空白，不要填 0 —— 填 0 会被误读成"状态0"。
# 4. 状态超过 5 档时考虑合并语义相近的档（如"3轮及以上"归一档），离散色带超过 5 色难分辨。
# 5. 若要同时看"状态"和"数值"（如重传轮次+时长），拆成上下两个 panel 共享 x 轴，
#    不要在一个格子里塞两种编码。
```