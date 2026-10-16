## 5. Sankey Diagram — 桑基图（D3 风格，矩形节点 + 贝塞尔流带）

**场景**: 资源分配、数据流向、能量流、用户路径。矩形节点（高度=流量）+ 半透明贝塞尔曲线连接带（按 source 分色）。

⛔ **不要用 `matplotlib.sankey.Sankey`**——它出来是"动物形状/箭头风格"，标签重叠、比例失真、整体丑。下面这套用 path + Bezier 手写，是 D3.js / Plotly 风格的现代 Sankey。

```python
import shutil, os
os.makedirs('_utils', exist_ok=True)
for f in ['plot_utils.py']:
    src = os.path.join(os.path.dirname(__file__), f)
    if os.path.exists(src):
        shutil.copy2(src, f'_utils/{f}')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()


def draw_sankey(ax, source_nodes, target_nodes, flows,
                source_colors=None, target_colors=None,
                left_x=0.10, right_x=0.90,
                node_width=0.025, node_gap=0.03,
                title_top=None):
    """D3 风格 Sankey 图（矩形节点 + 贝塞尔流带）。

    Args:
        source_nodes: list of (name, total_value)，例如 [('国产', 1473), ('俄罗斯', 1500)]
        target_nodes: list of (name, total_value)，例如 [('总供给', 3000)]
        flows: list of dict {source_idx: int, target_idx: int, value: float}
        source_colors / target_colors: 可选，None 时自动按 PALETTE 分色
        node_width: 矩形宽度（相对坐标 0-1）
        node_gap: 同侧节点间垂直间距
        title_top: 顶部副标题（如"流量守恒 (万 m³)"）
    """
    total_src = sum(v for _, v in source_nodes)
    total_tgt = sum(v for _, v in target_nodes)
    if abs(total_src - total_tgt) > 1e-3:
        raise ValueError(f'流量不守恒：source 合计 {total_src} ≠ target 合计 {total_tgt}')

    Y_MARGIN = 0.08
    avail_h_src = (1 - 2 * Y_MARGIN) - node_gap * max(0, len(source_nodes) - 1)
    avail_h_tgt = (1 - 2 * Y_MARGIN) - node_gap * max(0, len(target_nodes) - 1)

    src_ranges = []
    y = 1 - Y_MARGIN
    for _, v in source_nodes:
        h = v / total_src * avail_h_src
        src_ranges.append((y - h, y))
        y = y - h - node_gap

    tgt_ranges = []
    y = 1 - Y_MARGIN
    for _, v in target_nodes:
        h = v / total_tgt * avail_h_tgt
        tgt_ranges.append((y - h, y))
        y = y - h - node_gap

    if source_colors is None:
        source_colors = [PALETTE[i % len(PALETTE)] for i in range(len(source_nodes))]
    if target_colors is None:
        target_colors = [COLORS.get('text', '#444444')] * len(target_nodes)

    # 左侧节点矩形 + 标签
    for i, ((name, v), (y0, y1)) in enumerate(zip(source_nodes, src_ranges)):
        rect = Rectangle((left_x - node_width / 2, y0), node_width, y1 - y0,
                         facecolor=source_colors[i], edgecolor='none', alpha=0.92, zorder=3)
        ax.add_patch(rect)
        ax.text(left_x - node_width / 2 - 0.012, (y0 + y1) / 2,
                f'{name}\n{v:g}',
                ha='right', va='center', fontsize=9,
                color=COLORS.get('text', '#222'), fontweight='bold')

    # 右侧节点矩形 + 标签
    for i, ((name, v), (y0, y1)) in enumerate(zip(target_nodes, tgt_ranges)):
        rect = Rectangle((right_x - node_width / 2, y0), node_width, y1 - y0,
                         facecolor=target_colors[i], edgecolor='none', alpha=0.92, zorder=3)
        ax.add_patch(rect)
        ax.text(right_x + node_width / 2 + 0.012, (y0 + y1) / 2,
                f'{name}\n{v:g}',
                ha='left', va='center', fontsize=9,
                color=COLORS.get('text', '#222'), fontweight='bold')

    # 贝塞尔流带
    src_top_used = [r[1] for r in src_ranges]
    tgt_top_used = [r[1] for r in tgt_ranges]

    for flow in flows:
        si, ti, val = flow['source_idx'], flow['target_idx'], flow['value']
        s_h = val / total_src * avail_h_src
        t_h = val / total_tgt * avail_h_tgt
        s_y_top = src_top_used[si]; s_y_bot = s_y_top - s_h; src_top_used[si] = s_y_bot
        t_y_top = tgt_top_used[ti]; t_y_bot = t_y_top - t_h; tgt_top_used[ti] = t_y_bot

        mid_x = (left_x + right_x) / 2
        path_data = [
            (Path.MOVETO,    (left_x + node_width / 2, s_y_top)),
            (Path.CURVE4,    (mid_x, s_y_top)),
            (Path.CURVE4,    (mid_x, t_y_top)),
            (Path.CURVE4,    (right_x - node_width / 2, t_y_top)),
            (Path.LINETO,    (right_x - node_width / 2, t_y_bot)),
            (Path.CURVE4,    (mid_x, t_y_bot)),
            (Path.CURVE4,    (mid_x, s_y_bot)),
            (Path.CURVE4,    (left_x + node_width / 2, s_y_bot)),
            (Path.CLOSEPOLY, (left_x + node_width / 2, s_y_top)),
        ]
        codes, verts = zip(*path_data)
        flow_color = flow.get('color', source_colors[si])
        patch = PathPatch(Path(verts, codes),
                          facecolor=flow_color, edgecolor='none', alpha=0.42, zorder=2)
        ax.add_patch(patch)

    if title_top:
        ax.text(0.5, 0.98, title_top, ha='center', va='top',
                fontsize=10, color=COLORS.get('text', '#444'), fontweight='bold')

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_aspect('auto'); ax.axis('off')


# ── 示例 1: 多 source → 单 target（资源分配场景）
fig, ax = plt.subplots(figsize=(9, 5))
source_nodes = [('国产', 1473), ('俄罗斯', 1500), ('卡塔尔', 27)]
target_nodes = [('总供给 = 需求 (万 m³)', 3000)]
flows = [
    {'source_idx': 0, 'target_idx': 0, 'value': 1473},
    {'source_idx': 1, 'target_idx': 0, 'value': 1500},
    {'source_idx': 2, 'target_idx': 0, 'value': 27},
]
draw_sankey(ax, source_nodes, target_nodes, flows,
            title_top='问题一 最优供应量分配（流量守恒，万 m³）')

auto_rate = 1473 / 3000 * 100
import_rate = (1500 + 27) / 3000 * 100
ax.text(0.05, 0.04,
        f'自给率 = {auto_rate:.1f}%   进口依赖 = {import_rate:.1f}%',
        ha='left', va='bottom', fontsize=8.5,
        color=COLORS.get('text', '#444'),
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor='#cccccc', linewidth=0.5))

fig.tight_layout()
save_fig(fig, 'figures/fig_sankey_supply.pdf')


# ── 示例 2: 单 source → 多 target（数据分流场景）
fig, ax = plt.subplots(figsize=(10, 5.5))
source_nodes = [('原始数据', 1000)]
target_nodes = [('训练集', 600), ('测试集', 300), ('验证集', 100)]
flows = [
    {'source_idx': 0, 'target_idx': 0, 'value': 600, 'color': PALETTE[0]},
    {'source_idx': 0, 'target_idx': 1, 'value': 300, 'color': PALETTE[1]},
    {'source_idx': 0, 'target_idx': 2, 'value': 100, 'color': PALETTE[2]},
]
draw_sankey(ax, source_nodes, target_nodes, flows,
            target_colors=[PALETTE[0], PALETTE[1], PALETTE[2]],
            title_top='数据集划分')
fig.tight_layout()
save_fig(fig, 'figures/fig_sankey_split.pdf')


# ── 示例 3: 多对多
fig, ax = plt.subplots(figsize=(10.5, 6))
source_nodes = [('来源A', 500), ('来源B', 300), ('来源C', 200)]
target_nodes = [('去向X', 400), ('去向Y', 350), ('去向Z', 150), ('去向W', 100)]
flows = [
    {'source_idx': 0, 'target_idx': 0, 'value': 300},
    {'source_idx': 0, 'target_idx': 1, 'value': 150},
    {'source_idx': 0, 'target_idx': 2, 'value':  50},
    {'source_idx': 1, 'target_idx': 0, 'value': 100},
    {'source_idx': 1, 'target_idx': 1, 'value': 150},
    {'source_idx': 1, 'target_idx': 3, 'value':  50},
    {'source_idx': 2, 'target_idx': 1, 'value':  50},
    {'source_idx': 2, 'target_idx': 2, 'value': 100},
    {'source_idx': 2, 'target_idx': 3, 'value':  50},
]
draw_sankey(ax, source_nodes, target_nodes, flows,
            title_top='多对多流向分析')
fig.tight_layout()
save_fig(fig, 'figures/fig_sankey_many.pdf')
```

**⛔ 易踩的坑（Sankey Diagram 专用）：**

1. **流量必须守恒**：source 总和 = target 总和（函数已加 `raise ValueError` 校验，超 1e-3 报错）
2. **节点 ≤ 8 个**：每侧超过 8 节点 → 矩形太薄看不清，改用桑基图 + 滚动条（plotly）或拆成多张图
3. **流 ≤ 15 条**：超过 15 条流 → 视觉混乱，用 Sankey 不合适，改成饼图嵌套或矩阵热力图
4. **图例颜色**：每个 source 用同一颜色，target 矩形可以中性色（灰）或承袭 source 色
5. **数值单位写在 `title_top` 里**（如 "（流量守恒，万 m³）"），不要在每个节点重复
6. **不要用 `matplotlib.sankey.Sankey`**：那个 API 出来是"箭头形状"，标签重叠、比例失真

**⛔ 反例（用户实际踩过的坑）：**

```python
# ❌ 错误：matplotlib.sankey.Sankey 出来是"动物形状"
from matplotlib.sankey import Sankey
sankey = Sankey(ax=ax, scale=0.008, ...)
sankey.add(flows=[1473, 1500, 27, -3000], orientations=[1, 0, -1, 0], ...)
# 结果：3 个 source 从 3 个方向汇聚到 1 个 target → 形状像箭头 / 鱼，不是 Sankey

# ✅ 正确：用上面的 draw_sankey 函数，矩形 + 贝塞尔流带
draw_sankey(ax, source_nodes, target_nodes, flows, title_top='...')
```


---