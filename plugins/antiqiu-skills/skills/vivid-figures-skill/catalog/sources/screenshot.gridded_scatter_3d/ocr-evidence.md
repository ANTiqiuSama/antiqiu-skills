# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 038

```text
QO :
ae é
BG: =P py @
import plotly.graph_objects as go
import numpy as np
+ WEMARB RM
rows, cols = 32, 22
Xx = np. linspace(-1, 1, cols)
y = np. linspace(-1.7, 1.3, rows)
X, Y = np.meshgrid(x, y)
Z = np.exp(-((X + 0.5) ** 2 + (¥ + 6.5) ** 2) / 0.7) * 1.5 +
np.exp(
-((X - 0.5) ** 2 + (¥ - 0.5) ** 2) / 0.3
)
# EXBEXRAAR
colorscale_custom = [[0.0, "#2f648e"], [0.5, "#e9dlab"],
(1.0, "#c3476a"]]
#iRset rine
color_vals = np.exp(-((X + 0.5) ** 2 + (¥ + 6.5) ** 2) /
®.7) * 1.5 + np.exp(
-((X - 6.5) ** 2 + (Y - 0.5) ¥* 2) / 0.3
)
# ik = Hnkaa
fig = go.Figure(
data=[
go.Scatter3d(
x=X.flatten(), y=¥.flatten(), z=Z.flatten(),
mode="markers",
marker=dict(
size=4,
color=color_vals.flatten(),
colorscale=colorscale_custom,
colorbar=dict(title="Color Scale")))])
fig.update_layout (
scene=dict(xaxis_title="X", yaxis_title="¥",
zaxis_title="2"),
margin=dict(1=0, r=0, t=0, b=6),
)
fig.show()
1

```

