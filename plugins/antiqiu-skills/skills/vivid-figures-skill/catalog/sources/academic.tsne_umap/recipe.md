## 3. t-SNE / UMAP Visualization — 降维可视化

**Use case**: High-dimensional feature visualization showing cluster quality.
**Upgrades**: Per-class KDE contour backgrounds, 95% confidence ellipses, class center labels in white boxes.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Ellipse
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()

np.random.seed(42)
classes = ['Class A', 'Class B', 'Class C', 'Class D']
n_per = 150
embeddings, labels = [], []
for i, cls in enumerate(classes):
    center = np.random.randn(2) * 4
    pts = center + np.random.randn(n_per, 2) * 0.8
    embeddings.append(pts)
    labels.extend([cls] * n_per)
embeddings = np.vstack(embeddings)

fig, ax = plt.subplots(figsize=(7, 6))

for i, cls in enumerate(classes):
    mask = np.array(labels) == cls
    pts = embeddings[mask]

    # KDE contour background
    xy = pts.T
    kde = gaussian_kde(xy, bw_method=0.4)
    xg = np.linspace(pts[:, 0].min() - 2, pts[:, 0].max() + 2, 80)
    yg = np.linspace(pts[:, 1].min() - 2, pts[:, 1].max() + 2, 80)
    Xg, Yg = np.meshgrid(xg, yg)
    Z = kde(np.vstack([Xg.ravel(), Yg.ravel()])).reshape(Xg.shape)
    ax.contourf(Xg, Yg, Z, levels=5, cmap=plt.cm.Blues if i == 0 else
                plt.cm.Oranges if i == 1 else plt.cm.Greens if i == 2 else plt.cm.Purples,
                alpha=0.15)
    ax.contour(Xg, Yg, Z, levels=3, colors=PALETTE[i], alpha=0.3, linewidths=0.5)

    # 95% confidence ellipse
    cov = np.cov(pts.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 1], eigenvectors[0, 1]))
    width, height = 2 * np.sqrt(eigenvalues * 5.991)  # chi2 95%
    ellipse = Ellipse(xy=pts.mean(axis=0), width=width, height=height, angle=angle,
                      facecolor='none', edgecolor=PALETTE[i], linewidth=1.2,
                      linestyle='--', alpha=0.6)
    ax.add_patch(ellipse)

    # Scatter points
    ax.scatter(pts[:, 0], pts[:, 1], s=10, alpha=0.45, color=PALETTE[i],
               label=cls, edgecolor='none')

    # Class center label in white box
    cx, cy = pts.mean(axis=0)
    ax.annotate(cls, xy=(cx, cy), fontsize=9, fontweight='bold', color=PALETTE[i],
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                          edgecolor=PALETTE[i], alpha=0.9, linewidth=1))

ax.set_xlabel('Dimension 1', fontsize=11)
ax.set_ylabel('Dimension 2', fontsize=11)
ax.legend(frameon=False, labelspacing=0.35, handlelength=1.6, fontsize=9, markerscale=3, loc='best')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.15, linestyle='--')
fig.tight_layout()
save_fig(fig, 'figures/fig_tsne.pdf')
```

**★ 防遮挡技巧（t-SNE / UMAP 专用）：**
```python
# 1. 类别中心标签用 bbox 白底 + 粗边框：确保在散点云上可读
# 2. 置信椭圆用低 alpha（0.08）：不要遮挡散点
# 3. 类别数 >6 时：只标注最大的 3-4 个簇，其余用图例
# 4. 散点用小尺寸（s=8-15）和低 alpha（0.4）：给标签让出视觉空间
```

---