## 8. 三维等值面

用途：五层等值面、开口截面、连续色标与坐标壁。

数据要求：三维规则网格与每个网格点的标量。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维等值面
Restored/adapted from supplied screenshots [31].
Source: 小明的代码美学 (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
import plotly.graph_objects as go
X,Y,Z=np.mgrid[-5:5:40j,-5:5:40j,-5:5:40j]
values=X*X*.5+Y*Y+Z*Z*2
fig=go.Figure(go.Isosurface(x=X.flatten(),y=Y.flatten(),z=Z.flatten(),value=values.flatten(),
    isomin=10,isomax=50,colorscale=[[0.,'#2f648e'],[.5,'#e9d1ab'],[1.,'#c3476a']],
    surface_count=5,colorbar_nticks=5,caps=dict(x_show=False,y_show=False)))
fig.update_layout(scene={a:dict(title=a[0].upper(),backgroundcolor='#f2e2e4') for a in ['xaxis','yaxis','zaxis']},margin=dict(l=0,r=0,t=0,b=0))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```
