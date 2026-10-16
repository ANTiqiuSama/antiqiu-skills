# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 033

```text
ae
RG: =O py @®
import numpy as np
import plotly.graph_objects as go
*# eet t, TARE
np. random, seed (42)
# See
num_bubbles = 100
#2XSK t, RF ERRRLARE
t = np.linspace(®, 4 * np.pi, num_bubbles)
# ER xX, y ARR (#5 BS BY BR He)
R=1 4 Rie+E
noise_scale = 0.2 #4 BARE
x = R * np.cos(t) + np.random.normal(scale=noise_scale,
size=num_bubbles)
y = R * np.sin(t) + np.random.normal (scale=noise_scale,
size=num_bubbles)
z = t + np.random.normal(scale=noise_scale,
size=num_bubbles) #z fA t LA, MbLBA
#2 2 8, SRA o
Z_normalized = z - z.min()
bubble_sizes = 2 * z normalized + 10 # BmA\RUA 10, z t@
mA Bex
# (EFA Plotly #l 3p TA
fig = go.Figure(
data=[
go.Scatter3d(
x=X,
y=Ys
Z=Z,
mode="markers",
marker=dict(
size=bubble_sizes,
color=z, # RIGA z A
1

```

## 截图 034

```text
BB: =H py @®
colorscale=[[0.0, "#2f648e"], [0.5,
“"#e9dlab"], [1.0, "#c3476a"]],
opacity=0.7,
colorbar=dict(title="Z ff"),
)s
)
]
)
fig.update_lLayout (
title="RRLA RH",
scene=dict (xaxis_title="X", yaxis_title="¥",
zaxis_title="2"),
)
fig.show()
2

```

