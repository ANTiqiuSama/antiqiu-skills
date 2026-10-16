## 4. 多层旭日图

用途：多层扇区、白色分界、标签与根节点百分比。

数据要求：labels、parents、values 树形表；节点唯一且无环。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：从012–013恢复树形演示数据和Plotly Sunburst；取消演示时向当前目录写出data.csv的副作用。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""多层旭日图
Restored/adapted from supplied screenshots [12, 13].
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
read_custom_data = False
if read_custom_data:
    data_df = pd.read_csv('data.csv')
else:
    data_df = pd.DataFrame({
        'labels':['A','B','C','D','E','F','B1','B2','B1-1','B1-2','B1-3','C1','C2','D1','D2','E1','E2','E3','E4','E1-1','E1-2','E1-3','E3-1','E3-2','F1','F2','F3','F1-1','F1-2','F1-3'],
        'parents':['','A','A','A','A','A','B','B','B1','B1','B1','C','C','D','D','E','E','E','E','E1','E1','E1','E3','E3','F','F','F','F1','F1','F1'],
        'values':[0,0,0,0,0,0,0,8,4,2,2,4,4,6,6,0,7,0,3,7,2,2,2,2,0,9,8,6,5,6]})
fig = go.Figure(go.Sunburst(labels=data_df.labels,parents=data_df.parents,values=data_df['values'],
    textinfo='label+percent root',textfont=dict(color='white',size=14),
    marker=dict(colors=['#ffffff','#f9b99e','#f87f8c','#e37e8e','#a9758c','#796b88'],line=dict(color='white',width=3))))
fig.update_layout(margin=dict(t=0,l=0,r=0,b=0),width=800,height=500)
fig.show()
```
