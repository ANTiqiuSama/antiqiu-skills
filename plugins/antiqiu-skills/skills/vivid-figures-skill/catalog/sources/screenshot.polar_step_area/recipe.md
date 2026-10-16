## 31. 环形刻度阶梯面积图

用途：交替背景环、角度射线、描边径向刻度、阶梯填充与轮廓。

数据要求：按角度有序的非负半径；源码为随机阶梯面积，不是真正频数直方图。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：原标题称直方图，但代码绘制随机半径阶梯面积；按真实编码命名，不当作频数图。

```python
"""环形刻度阶梯面积图
Restored/adapted from supplied screenshots [113, 114, 115].
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
import matplotlib.patheffects as path_effects
bgcolor='#ebf0f5';edgecolor='#597cab'
plt.rcParams.update({'figure.facecolor':bgcolor,'axes.facecolor':bgcolor,'axes.edgecolor':edgecolor,'text.color':'#597cab'})
fig,ax=plt.subplots(figsize=(6,6),subplot_kw={'projection':'polar'},dpi=150)
ax.set(ylim=(0,1000),xticks=[],yticks=[])
radius=ax.get_rmax();length=.02*radius
for i in range(0,360,30):
    angle=np.pi*i/180
    ax.plot([angle,angle],[radius,100],linewidth=.5,color='white')
    ax.text(angle,radius+4*length,str(i),rotation=i-90,rotation_mode='anchor',va='top',ha='center')
def polar_to_cartesian(theta,radius):
    return np.array([radius*np.cos(theta),radius*np.sin(theta)])
def cartesian_to_polar(x,y):
    return np.array([np.arctan2(y,x),np.sqrt(x*x+y*y)])
for i in range(100,1000,100):
    p=cartesian_to_polar(*(polar_to_cartesian(0,i)+[0,-length]))
    text=ax.text(p[0],p[1],str(i),zorder=500,va='top',ha='center',size='x-small')
    text.set_path_effects([path_effects.Stroke(linewidth=2,foreground='white'),path_effects.Normal()])
T=np.linspace(0,2*np.pi,1000)
for i in range(0,1000,200):
    ax.fill_between(T,i,i+100,color='#597cab33',zorder=-50)
ax.scatter([0],[0],20,facecolor=bgcolor,edgecolor='#597cab',zorder=1000)
np.random.seed(1);n=100
T=2*np.pi/n+np.linspace(0,2*np.pi,n)
T[1::2]=T[0:-1:2]
R=np.random.uniform(500,800,n)
R[-1]=R[0];R[1:-1:2]=R[2::2]
ax.fill(T,R,color='#e6a6a5',zorder=150,alpha=.3)
ax.plot(T,R,color='#e6a6a5',zorder=250,linewidth=1)
plt.tight_layout();plt.show()
```
