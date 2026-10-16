## 2. 三维分层面积图

用途：透明层叠面积、平滑曲线、三维轴与深色轮廓。

数据要求：有序 x 和多个情景数值序列。

来源：小明的代码美学；部分代码恢复，缺失段按图补全。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：仅有007的CSV读取和函数起始页；保留可见读取函数，绘图部分按009效果图重建。；原CSV未附带，示例水位为手工合成；统一900m基座、六层透明填充与独立轮廓。

```python
"""三维分层面积图
Restored/adapted from supplied screenshots [7].
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
# Only CSV-reader code page 007 was supplied; plotting section reconstructed from 009.
import csv
from matplotlib.collections import PolyCollection
from scipy.interpolate import make_interp_spline
def polygon_under_graph(x,y):
    return [(x[0],0.),*zip(x,y),(x[-1],0.)]
def read_csv(csv_path):
    categories=[];x_vals=[];y_cols=None
    with open(csv_path,'r',newline='',encoding='utf-8') as f:
        reader=csv.reader(f);header=next(reader);categories=header[1:]
        y_cols=[[] for _ in categories]
        for row in reader:
            if not row:continue
            x_vals.append(float(row[0]))
            for i in range(len(categories)):y_cols[i].append(float(row[i+1]))
    return np.array(x_vals,dtype=float),categories,[np.array(col,dtype=float) for col in y_cols]
read_custom_data=False
if read_custom_data:
    x,categories,y_list=read_csv('data.csv')
else:
    x=np.arange(1,13)
    categories=[f'Scenario {i+1}' for i in range(6)]
    y_list=[np.array(v) for v in [
      [1000,1006,1009,1005,995,980,964,965,1000,1020,1040,1000],
      [995,1006,1000,985,976,975,966,1002,1015,1025,1030,970],
      [990,1003,1008,1002,981,970,975,990,1010,1040,1000,1050],
      [998,1003,1012,1009,991,982,980,982,990,1004,1035,1026],
      [1000,1003,1005,1007,1000,994,990,995,1024,1033,1028,1034],
      [1014,1015,1020,1024,1020,1004,994,992,1050,992,1054,1000]]]
BASE=900
colors=['#dc6bc8','#f19a42','#f1d63e','#40cb6b','#398dd7','#7f61cc']
fig=plt.figure(figsize=(8,7),dpi=150);ax=fig.add_subplot(projection='3d')
x_smooth=np.linspace(x.min(),x.max(),300)
for i,(values,color) in enumerate(zip(y_list,colors)):
    y_smooth=make_interp_spline(x,values)(x_smooth)
    vertices=[(x_smooth[0],BASE),*zip(x_smooth,y_smooth),(x_smooth[-1],BASE)]
    poly=PolyCollection([vertices],facecolors=color,alpha=.32,edgecolors='none')
    ax.add_collection3d(poly,zs=i+1,zdir='y')
    ax.plot(x_smooth,np.full(len(x_smooth),i+1),y_smooth,color=color,linewidth=2.5)
ax.set(xlim=(x.min(),x.max()),ylim=(1,6),zlim=(BASE,1080),xlabel='Month',ylabel='Scenario',zlabel='Water level (m)')
ax.set_yticks(range(1,7));ax.view_init(elev=25,azim=-75)
ax.set_box_aspect((1.25,1.5,1))
for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
    axis.pane.fill=False;axis._axinfo['grid'].update(linestyle='--',color='#999999')
plt.tight_layout();plt.show()
```
