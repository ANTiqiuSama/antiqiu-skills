# 按需参考

选定模板后的适配以完整源码和卡片保留要点为准；以下示例仅在确有需要时使用，不作为重写已选模板的理由。

## 字体与排版

优先沿用模板的字号层次与项目字体。以下为需要自定义时的示例，不要求覆盖模板现有设置：

```python
plt.rcParams.update({
    'font.size': 11,                    # 正文字号
    'axes.labelsize': 12,               # 坐标轴标签稍大
    'axes.titlesize': 13,               # 标题再大一号
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'font.family': 'sans-serif',
    'mathtext.fontset': 'stix',         # 数学字体用 STIX（接近 Times）
})
```

## 让图表更高级的技巧

下列为按需使用的局部技法。已选完整模板时保留其实现，不把这些示例逐项叠加到每张图上。

### 1. 去掉顶部和右侧边框（已在 plot_utils 中默认）
```python
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### 2. 柱状图加数值标注
```python
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9)
```

### 3. 折线图加标记点 + 置信带
```python
ax.plot(x, y, 'o-', markersize=5, linewidth=1.5, color=PALETTE[0])
ax.fill_between(x, y_low, y_high, alpha=0.15, color=PALETTE[0])
```

### 4. 热力图用 mask 只显示下三角
```python
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
from _utils.palette_maps import palette_cmap
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap=palette_cmap('diverging'), center=0)
```

### 5. 回归系数森林图（实证论文核心图）
```python
ax.errorbar(coefs, y_pos, xerr=[coefs-ci_low, ci_high-coefs],
            fmt='o', color=PALETTE[3], ecolor=COLORS['ref_line'], capsize=4, markersize=6)
ax.axvline(x=0, color=PALETTE[0], linestyle='--', linewidth=0.8, alpha=0.7)
```

### 6. 分组柱状图加误差棒
```python
bars = ax.bar(x + offset, vals, width, yerr=errs, capsize=3,
              color=PALETTE[i], edgecolor='white', linewidth=0.5)
```

### 7. 多面板子图对齐
```python
fig, axes = plt.subplots(2, 2, figsize=(5.0, 4.9))   # 示例尺寸；实际保留模板比例并按最终显示尺寸适配
fig.tight_layout(pad=0.5)
# 每个子图加 (a) (b) (c) (d) 标签 — 用 set_title 紧贴子图顶部
for i, ax in enumerate(axes.flat):
    ax.set_title(f'({chr(97+i)})', fontsize=11, fontweight='bold', loc='left', pad=3)
```

> `tight_layout` 的 `pad` 按模板和实际布局选择，不设统一上限。
> 可从模板原值开始；`pad=0.3`、`0.5` 或 `1.2` 均需结合面板、标签、色条与图例空间判断，避免不必要地重排。
> 如果需要子图间距更大，用 `hspace`/`wspace` 参数而不是增大 pad。

> 子图角标沿用模板已有方法。若 `ax.text(transAxes)` 在等比例坐标或布局调整后离面板过远，
> 可局部调整位置或使用 `set_title(loc='left', pad=3)`，修改后检查实际渲染。

### 8. 保存时确保高质量
```python
save_fig(fig, 'figures/fig_xxx.pdf')
```

### 9. 分布图的可选阶梯轮廓
需要连续阶梯轮廓时可用 `ax.stairs`。原模板的 `hist`、`bar`、渐变柱体或分层密度有各自用途，
不为统一外观替换其绘制方法：

```python
counts, edges = np.histogram(vals, bins=np.arange(3.5, 22.5, 1.0))
ax.stairs(counts, edges, fill=True,
          color=_lighten(PALETTE[0], 0.50),   # 浅色填充
          edgecolor=PALETTE[0], lw=1.5, zorder=4)
```
需要上下对镜像对照（如"真实分布 vs 预测分布"）时，把一侧取负即可，比并排双色柱更直观：
```python
ax.stairs(share_true * 100, edges, fill=True, color=_lighten(PALETTE[2], 0.48), edgecolor=PALETTE[2])
ax.stairs(-share_pred * 100, edges, fill=True, color=_lighten(PALETTE[0], 0.48), edgecolor=PALETTE[0])
ax.axhline(0, lw=1.2, color=COLORS['text'])          # 镜像轴
# 负半轴标成正数（读者看的是"占比"不是负值）；⛔ 必须先 set_yticks 再 set_yticklabels，
# 否则 matplotlib 会报 FixedFormatter 警告、且换版本后标签可能对不上刻度
_yt = ax.get_yticks()
ax.set_yticks(_yt)
ax.set_yticklabels([f'{abs(t):.0f}' for t in _yt])
```

### 10. 量化两个值的差距：可选双向箭头（保留所选模板的注释设计）
要说明"A 比 B 高多少"时，**别写一句话塞进图内**——在两点之间画双向箭头 + 一个短标签，
需要强调两点之间的差异时，可以按模板风格增加简短引线与差值标注：

```python
ax.annotate('', xy=(q_high, y), xytext=(q_low, y),
            arrowprops=dict(arrowstyle='<->', color=PALETTE[4], lw=1.5))
ax.text((q_low + q_high) / 2, y - 0.05, f'差 {(q_high - q_low) * 100:.1f} pp',
        ha='center', va='top', fontsize=8.5, fontweight='bold', color=PALETTE[4])
```
适用：两条 ECDF 在某分位处的差距、改进前后的提升量、上限与实测的余量、两方案的间隔。

### 11. 对数轴的零值地板：`0` 会被静默丢掉，必须显式处理 —— 但**地板要贴近数据，不能"远低于"**
`set_yscale('log')` / `set_xscale('log')` 时，值为 `0` 的点会被 matplotlib **无声丢弃**——
图上少了点却没有任何提示，这是很隐蔽的数据不诚实。所以要用地板值占位 + 单独标注。

⛔⛔ **但地板值必须【贴近真实数据下界】，绝不能设成"远低于数据量级"的极小值。**
（实测翻车：某 ECDF 图真实数据主体在 $10^1\sim10^2$ nm、1% 分位才 3.7nm，地板却设 `1e-3` →
对数轴被撑到 **6.1 个数量级**，左边约 **40% 的图宽是纯空白**，曲线在那段只是一条平线，
图看着"左边空一大片"。地板改到 0.5nm 后轴跨降到 3.5 个数量级，空白基本消失。）

**定地板的方法（三步）**：
```python
nz = vals[vals > 0]
# ⛔ 相交/重合等情形会产出 1e-15 量级的浮点残差，那不是真实数据，要和 0 一起归为"零"
EPS = 1e-6
real = nz[nz > EPS]
LOG_FLOOR = 10 ** (np.floor(np.log10(real.min())) - 0.5)   # ① 贴着真实最小值下方半个数量级
plot_v = np.where(vals > EPS, vals, LOG_FLOOR)
ax.set_yscale('log')
ax.set_ylim(LOG_FLOOR * 0.7, real.max() * 1.3)             # ② 轴界贴着地板给，别再往下留空
ax.scatter(x, plot_v, color=PALETTE[0])
n_zero = int((vals <= EPS).sum())
if n_zero:                                                 # ③ 地板并了多少点，必须写出来
    ax.scatter(x[vals <= EPS], np.full(n_zero, LOG_FLOOR),
               marker='v', color=COLORS['down'], zorder=6)
    ax.text(LOG_FLOOR * 0.8, ax.get_ylim()[1], f'← {n_zero} 个 = 0 并入左端',
            fontsize=7.2, ha='left', va='top')
```
**自检**：算一下 `log10(轴上界/轴下界)`。**超过 4 个数量级就要警觉**——除非数据真的横跨那么多量级，
否则就是地板设太低。真实数据只跨 2 个量级时，别让轴跨 6 个。

#### ⛔⛔ 更上位的原则：**轴只覆盖「有数据的区间」，别为极少数极端点留一大段空轴**

上面的地板技巧治的是"地板设太低"，但**真正的病根常常是"为了把某个东西画进轴内，让轴覆盖了没有数据的一大段"**。
调地板治不了这种（实测踩过完整一轮，三版数据在此）：

| 做法 | 轴跨 | 曲线真正在变化的横向占比 |
|---|---|---|
| 地板 `1e-3`、左界 8e-4 | 6.10 | 11% / 21% / 20% |
| 地板抬到 `0.5`、左界 0.35（"贴近数据下界"） | 3.46 | 12% / 31% / 29% |
| **左界直接设 10（砍掉无数据段）** | **2.00** | **12% / 44% / 36%** |

那张 ECDF 图：判据线 δ=1.8nm 想画进轴内，但 90.8% 的点在 100nm 以上、0.5–13nm 只有 **1.24%** 的点，
δ 处的纵截距几乎全由 d=0 的相交对贡献 —— **δ 附近本来就没数据**。于是：
- 左界拉到 0.35 → 左边 64% 图宽是平线；抬到 10nm 仍有 43%
- 连**断轴双 panel 也没用**：左 panel 曲线只上升 0.016–0.038、有变化占比仅 1–19%，还是平线

**⛔⛔ 第 0 步（比下面所有事都靠前）：定轴范围前，先打印数据真实 min/max。**
不是"心里大概有数"，是**真的打印出来看一眼**。实测踩过的坑：主胞边长常量 `L = 10000`，
而数据坐标系其实以原点为中心（`[-L/2, +L/2]`），脚本却写了 `set_xlim(0, L)` ——
负坐标那一半（实测 46%~79% 的点）被静默裁到轴外，图上只剩挤在角落的一小撮。
matplotlib 不报错、静态检查也扫不出来，就这么进了成品 PDF。

```python
A = np.vstack([P, Q])            # 或任何即将画上去的数组
for k, nm in enumerate('xyz'[:A.shape[1]]):
    print(f'{nm}: {A[:, k].min():.1f} .. {A[:, k].max():.1f}')
```

**常量名会骗人**：`L` / `SIZE` / `LENGTH` 到底是「边长」还是「坐标上界」？去常量定义处
确认，别猜——本例 `code/params.py` 里写得很清楚：`HALF = L / 2  # 半边长，坐标上下界`。
`save_fig` 里有运行时兜底闸（>20% 的点落在轴外就打警告），但那是最后一道网，别指望它。

**然后才是：先问「这段轴上有数据吗」，再谈地板怎么设。**
1. 看分位数/直方计数定出"数据真正密集的起点"，**轴界就设在那里**（如 `set_xlim(10, 1000)`）；
2. 落在轴外的极少数点、以及关键判据值，**用图例标签或一行注记承载数值**，不要为它们留一段空轴。
   例：`label=f"{组名}（{n} 对；δ 处 {frac:.2%}）"` —— 图例既标识曲线又给关键数值，比图内再塞
   一个文字框干净；再补一行"`d<10nm` 的点占 1.24%（其中 187 对已相交），贡献已计入曲线左端起始高度"。
3. ⛔ 但**必须写明轴外还有多少点、去哪了**，否则是数据不诚实。

**ECDF 尤其不需要地板**：`F(x)=P(X≤x)` 已把 `d=0` 的点算进任意 `x>0` 处的高度，
用全量算 ECDF、只在显示上裁 x 范围即可，`d=0` 体现为"曲线左端的起始高度"，零信息损失。

### 12. 同一物理量两种口径并列：加第二坐标轴（`twiny`/`twinx`）做换算刻度
当一个量有两种等价表述（时长↔效率、原值↔百分比、绝对量↔归一化），不要画两张图、也不要
只标一种让读者自己换算——在**同一根轴的对面**加换算刻度，一张图读两种口径：

```python
ax.set_xlabel(r'PPDU 时长 $T$ (ms)')
axt = ax.twiny()                       # 上方第二 x 轴
axt.set_xlim(ax.get_xlim())            # ⛔ 必须同步范围，否则刻度对不上
ticks = np.array([1.0, 2.0, 3.0, 4.5])
axt.set_xticks(ticks)
axt.set_xticklabels([f'{t / (t + 0.144):.3f}' for t in ticks])   # 换算成占空效率
axt.set_xlabel(r'对应占空效率 $\varsigma = T/(T+144\,\mu s)$', labelpad=3)
axt.tick_params(axis='x', length=2.5)
```
⛔ 注意与「异量纲隔离」的区别：这里是**同一个量的两种口径**（可换算）才用；两个**不同物理量**
（时间 vs 百分比）挤一根轴是错的，那种情况要用 `twinx` 各自标单位、或干脆拆 panel。

### 13. QQ 图加 95% 逐点包络（比一根参考线专业得多）
只画一条正态参考线，读者无法判断"偏离多少才算显著"。用 Beta 序统计量算出逐点置信包络，
越出包络的才是真尾部偏离：

```python
from scipy import stats
(osm, osr), (slope, icpt, r) = stats.probplot(resid, dist='norm')
ax.scatter(osm, osr, s=10, color=PALETTE[0], alpha=0.55, rasterized=True)
ax.plot([osm.min(), osm.max()], [slope * osm.min() + icpt, slope * osm.max() + icpt],
        '--', color=PALETTE[1], lw=1.6, label=f'正态参考线（$R^2$={r**2:.4f}）')
n = resid.size; k = np.arange(1, n + 1)          # 第 k 个序统计量服从 Beta(k, n-k+1)
lo = stats.norm.ppf(stats.beta.ppf(0.025, k, n - k + 1)) * slope + icpt
hi = stats.norm.ppf(stats.beta.ppf(0.975, k, n - k + 1)) * slope + icpt
ax.fill_between(np.sort(osm), lo, hi, color=PALETTE[3], alpha=0.22, label='95% 逐点包络')
```

### 14. 大量散点加 `rasterized=True`（控制 PDF 体积，不牺牲文字清晰度）
上千个散点写进矢量 PDF 会让文件膨胀到几 MB、打开卡顿。给**数据层**开栅格化，
坐标轴/文字仍是矢量（缩放不虚）：

```python
ax.scatter(x, y, s=9, color=PALETTE[0], alpha=0.34, linewidths=0,
           rasterized=True)          # 只栅格化点，标签文字仍矢量
```
适用：散点云 > 500 点、蜂群图、密集轨迹。热力图/柱状图不需要。
