# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 031

```text
ae
BC: =e py @
import plotly.graph_objects as go
import numpy as np
X, Y, Z = np.mgrid[-5:5:40j, -5:5:40j, -5:5:40j]
values = X*X*O0.5+Y*x#Y+Z4 72% 2
fig = go.Figure(
data=go.Isosurface(
x=X.flatten(),
y=Y.flatten(),
z=Z.flatten(),
value=values. flatten(),
isomin=10,
isomax=56,
colorscale=[
[0.0, "#2f648e"],
[0.5, "#e9dlab"],
(1.0, "#c3476a"],
1;
surface_count=5,
colorbar_nticks=5,
caps=dict(x_show=False, y_show=False) ,
)
)
fig.update_lLayout (
scene=dict(
xaxisedict(title="X", backgroundcolor="#f2e2e4") ,
yaxis=dict(title="¥", backgroundcolor="#f2e2e4") ,
zaxis=dict(title="Z", backgroundcolor="#f2e2e4") ,
),
margin=dict(1=8, r=0, t=0, b=@),
)
fig.show()
1

```

