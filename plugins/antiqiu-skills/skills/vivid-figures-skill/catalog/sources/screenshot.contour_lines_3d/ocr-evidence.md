# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 040

```text
BCG: —MeieRAR py @®
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,
to_hex
# PGA RRA BRE
rows, cols = 32, 22
X = np.linspace(-1, 1, cols)
y = np.linspace(-1.7, 1.3, rows)
X, Y = np.meshgrid(x, y)
Z = np.exp(-((X+0.5)**2 + (Y¥+0.5)**2) / @.7) * 1.5 +
np.exp(-((X-0.5)**2 + (¥-0.5)**2) / 0.3)
*#EXBEXMABR (BFLRM matplotlib colormap)
colors = [(6.0, "#2f648e"), (0.5, "#e9dlab"), (1.06,
"#c3476a") ]
cmap = LinearSegmentedColormap. from_lList("custom", [col for
pos, col in colors], N=256)
* RBS eAnaR (TREES EE)
num_levels = 20
levels = np.linspace(Z.min(), Z.max(), num_levels)
# FIFA matplotlib ERS BHR (RAFREMARE, FETA)
fig_contour = plt.figure()
CS = plt.contour(X, Y, Z, levels=levels)
plt.close(fig_contour) # KMIRR A&R
# 792 Plotly BW, KRARRMBRSER
fig = go.Figure()
for i, level in enumerate(CS. levels):
segs = CS.allsegs[i] # # level DWHRBASRSHBAR
for seg in segs:
# A-KS SEAM aE
norm_level = (level - Z.min()) / (Z.max(}) - Z.min())}
# REV -KEHRRE (SEX AAMH)
line_color = to_hex(cmap(norm_level))
1

```

## 截图 041

```text
BCG: =MeieRAR py @®
fig.add_trace(go.Scatter3d(
x=seg[:, 6],
y=seg[:, 1],
z=[level] * len(seg),
mode='Lines',
Line=dict(color=line_color, width=8),
showlegend=False
»)
fig.update_layout (
scene=dict(
xaxis_title='X',
yaxis_title='Y',
zaxis_title='Z'
)s
margin=dict(1=8, r=0, t=0, b=0)
)
fig.show()
2

```

