## 10. 混淆矩阵热力图

**场景**：分类模型的混淆矩阵可视化，展示各类别的预测准确率。
**要点**：热力图+数值标注、颜色深浅自适应文字颜色、归一化百分比。

```python
import numpy as np, matplotlib.pyplot as plt; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import seaborn as sns
from _utils.plot_utils import setup_style, save_fig, PALETTE
setup_style()

classes = ['类别A', '类别B', '类别C', '类别D']
cm = np.array([[85, 5, 7, 3], [4, 90, 3, 3], [6, 4, 82, 8], [2, 3, 5, 90]])
cm_norm = cm / cm.sum(axis=1, keepdims=True) * 100

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm_norm, annot=True, fmt='.1f', cmap=palette_cmap('sequential'), xticklabels=classes,
            yticklabels=classes, linewidths=0.5, linecolor='white',
            cbar_kws={'label': '预测准确率 (%)'}, ax=ax)
ax.set_xlabel('预测类别', fontsize=11); ax.set_ylabel('真实类别', fontsize=11)
ax.set_xticklabels(classes, fontsize=10); ax.set_yticklabels(classes, fontsize=10, rotation=0)
[t.set_color(contrast_text(ax.collections[0].cmap(ax.collections[0].norm(float(t.get_text()))))) for t in ax.texts]; fig.tight_layout()
save_fig(fig, 'figures/fig_confusion_matrix.pdf')
```

**⚠ 混淆矩阵定制生成注意事项：**
```python
# 1. 数值标注颜色自适应底色深浅：深色格子用白色文字，浅色格子用深色文字
#    color = 'white' if val > threshold else COLORS['text']（threshold 取 colormap 中间值）
# 2. 类别名过长时：rotation=45, ha='right'（x 轴），fontsize=8
# 3. 类别数 >6 时减小字号，>10 时考虑只标注对角线数值
```

---
