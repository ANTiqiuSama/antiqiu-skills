## 9. 特征重要性排序图（渐变柱状图）

**场景**：机器学习模型的特征重要性排序展示，如随机森林、XGBoost 的 feature importance。
**要点**：水平柱状图、按重要性降序排列、渐变色映射重要性、数值标签右对齐。

```python
import numpy as np, matplotlib.pyplot as plt
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

features = ['人均GDP', '城镇化率', '教育支出', '医疗投入', '交通密度',
            '产业结构', '人口密度', '绿化覆盖', '科技投入', '能源消耗']
importance = np.array([0.182, 0.156, 0.134, 0.112, 0.098, 0.087, 0.076, 0.065, 0.054, 0.036])
sort_idx = np.argsort(importance)
features = [features[i] for i in sort_idx]
importance = importance[sort_idx]

n = len(features)
fig, ax = plt.subplots(figsize=(7, max(4, n*0.45)))
y = np.arange(n)
max_val = importance.max()

for i in range(n):
    ratio = importance[i] / max_val
    c = _lighten(PALETTE[0], 0.5 * (1 - ratio))
    ax.barh(y[i], importance[i], height=0.6,
            color=_lighten(c, 0.3), edgecolor=c, linewidth=1.2, zorder=3)
    ax.text(importance[i] + max_val*0.02, y[i], f'{importance[i]:.3f}',
            va='center', ha='left', fontsize=9, fontweight='bold', color=c)

ax.set_yticks(y); ax.set_yticklabels(features, fontsize=10)
ax.set_xlabel('特征重要性', fontsize=11)
ax.set_xlim(0, max_val * 1.2)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.12, linestyle='--')
fig.tight_layout()
save_fig(fig, 'figures/fig_feature_importance.pdf')
```

**⚠ 特征重要性图定制生成注意事项：**
```python
# 1. 数值标签紧贴条形右端（x=val+margin, ha='left'）
# 2. xlim 右侧留 20% 空间给数值标签
# 3. 特征名如果过长（>6 字），用 fontsize=8.5 或缩写
# 4. 特征数 >15 时自适应高度 _fig_h = max(4, n * 0.45)
```

---