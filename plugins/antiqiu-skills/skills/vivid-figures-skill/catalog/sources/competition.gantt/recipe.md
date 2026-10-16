## 15. 甘特图（彩色条形 + 原色边框 + 里程碑/排斥标记）

**场景**：项目调度/排程问题的时间线展示，如车间调度、任务分配。
**要点**：彩色条形按资源/机器分组、里程碑菱形标记、Makespan 标注线。

```python
import numpy as np, matplotlib.pyplot as plt
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

tasks = ['任务A', '任务B', '任务C', '任务D', '任务E', '任务F', '任务G', '任务H']
starts = [0, 2, 1, 5, 3, 7, 6, 9]
durations = [3, 4, 2, 3, 5, 2, 4, 3]
machines = [0, 1, 0, 2, 1, 0, 2, 1]
machine_names = ['机器M1', '机器M2', '机器M3']

n = len(tasks)
_fig_h = max(5, n * 0.35 + 1)
fig, ax = plt.subplots(figsize=(10, _fig_h))
ax.grid(axis='x', alpha=0.12, linestyle='--', color=COLORS['grid']); ax.set_axisbelow(True)

for i in range(n):
    c = PALETTE[machines[i] % len(PALETTE)]
    ax.barh(i, durations[i], left=starts[i], height=0.6,
            color=_lighten(c, 0.3), edgecolor=c, linewidth=1.3, zorder=3)
    ax.text(starts[i] + durations[i]/2, i, f'J{i+1}', ha='center', va='center',
            fontsize=8, fontweight='bold', color=c)

# Makespan 标注（放在 axes 内部顶端，避免 tight_layout 压缩导致标注飘远）
makespan = max(s+d for s, d in zip(starts, durations))
ax.axvline(makespan, color=COLORS['down'], linewidth=1.5, linestyle='--', zorder=4)
# ⛔ 不要用 y=1.02 + transform=ax.get_xaxis_transform()（会被 tight_layout 压缩导致标注飘远）
# 改用 axes 内部坐标：放在第一个任务条的上方
ax.text(makespan, -0.8, f'Makespan={makespan}h',
        ha='center', va='center', fontsize=9, fontweight='bold', color=COLORS['down'],
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLORS['down'], alpha=0.9))

# 图例
legend_elements = [plt.Rectangle((0,0), 1, 1, facecolor=_lighten(PALETTE[j], 0.3), edgecolor=PALETTE[j], linewidth=1.3)
                   for j, name in enumerate(machine_names)]
ax.legend(handles=legend_elements, labels=machine_names, frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=8, ncol=len(machine_names), loc='best')
ax.set_yticks(range(n)); ax.set_yticklabels(tasks, fontsize=10)
ax.set_xlabel('时间 (h)', fontsize=11)
ax.invert_yaxis()
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_gantt.pdf')
```

**⚠ 甘特图定制生成注意事项：**
```python
# 1. 任务标签在条形内部居中（y 轴标签位置），不要放在条形外部导致重叠
# 2. 里程碑用菱形标记（marker='D'），不要用圆点（容易和任务条位置混淆）
# 3. 任务数 >15 时自适应高度 _fig_h = max(5, n_tasks * 0.35 + 1)
# 4. ⛔ Makespan 标注不要用 y=1.02 + transform=ax.get_xaxis_transform()
#    tight_layout() 会为轴外文本压缩绘图区域，导致标注"飘"在图表上方很远
#    正确做法：放在 axes 内部（如 y=-0.8，第一个任务条上方），用数据坐标
# 5. ⛔ 离群任务检测：如果某个任务的结束时间远大于其他任务（如 10 倍以上），
#    说明调度结果可能有问题。此时应该：
#    a) 先检查数据是否合理（打印最大/最小任务时间，看是否有异常值）
#    b) 如果数据确实如此（如某个任务等待时间很长），用断轴（broken axis）展示
#    c) 或者只展示主要任务区间，离群任务单独标注
#    d) 绝对不要让一个离群任务把整个图压缩到角落
# 6. 生成甘特图前先做数据摘要：
#    max_end = max(end times); p90_end = np.percentile(end times, 90)
#    if max_end > p90_end * 3: print("⚠ 离群任务检测：最大结束时间远大于 P90")
```

---