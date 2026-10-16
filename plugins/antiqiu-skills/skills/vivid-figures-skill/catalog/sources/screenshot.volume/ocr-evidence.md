# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 036

```text
QO :
ae é
WRG: =RKBUE py @
import numpy as np
import plotly.graph_objects as go
from scipy import ndimage
# QUE GA AR
np. random. seed (0)
1 = 30
X, Y, Z = np.mgrid(:1, :1, :1]
vol = np.zeros((1l, lL, 1))
pts = (1 * np.random.rand(3, 15)).astype(int)
vol[tuple(indices for indices in pts)] =1
+ WARRERTEM ER, FRR
vol = ndimage.gaussian_filter(vol, 4)
vol /= vol.max()
# BHAA
fig = go.Figure(
data=go.Volume(
x=X.flatten(), y=Y¥.flatten(), z=Z.flatten(),
value=vol. flatten(),
isomin=0.2,
isomax=0.7,
opacity=0.1,
surface_count=25,
colorscale=[[6.0, "#3768be"], [0.5, “#e9dlab"],
[1.0, "#c3476a"]],
)
)
fig.update_layout (
scene=dict(
xaxis=dict(title="X", backgroundcolor="#f2e2e4") ,
yaxis=dict(title="¥", backgroundcolor="#f2e2e4") ,
zaxis=dict(title="Z2", backgroundcolor="#f2e2e4") ,
),
margin=dict(1=0, r=0, t=0, b=0),
)
fig.show()
1

```

