# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 047

```text
QO :
ae é
BB: =A. py @
import plotly.graph_objects as go
import numpy as np
# PiGARRA BRE
rows, cols = 32, 22
x = np.linspace(-1, 1, cols)
y = np.linspace(-1.7, 1.3, rows)
X, Y = np.meshgrid(x, y)
Z = np.exp(-((X+O.5)**2 + (Y¥+0.5)**2) / @.7) * 1.5 +
np.exp(-((X-0.5)**2 + (¥-0.5)**2) / 0.3)
# EXBEXRAAR
colorscale_custom = [
(0.0, "#2f648e"],[6.5, "#e9dlab"], [1.6, "#c3476a"]
]
*# RRARBABE: BWW start. end M1 size BH ABA
fig = go.Figure(data=[go.Surface(
x=X, y=Y, Z=Z,
colorscale=colorscale_custom,
contours={
"x": {"show": True, "color": "white", "width": 1,
"start": x.min(), "end": x.max(), "size": 0.1},
"y": {"show": True, "color": "white", "width": 1,
"start": y.min(), "end": y.max(), "size": @.1}
}
v1)
fig.update_lLayout (
scene=dict(
xaxis_title='X',
yaxis_title='yY',
zaxis_title='Z'
),
margin=dict(1=0, r=0, t=0, b=0)
)
fig.show()
1

```

