## 21. 极坐标径向柱状图

用途：径向条形、空心基座、三档颜色、旋转数值。

数据要求：非负类别值；类别角度等分。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：设置半径下界0，保留bottom=10的空心基座。

```python
"""极坐标径向柱状图
Restored/adapted from supplied screenshots [72, 73, 74].
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
from matplotlib.patches import Patch
values=[20,27,16,17,16,22,24,26,30,22,18,24,17,14,23,17,20,18,14,18,21,13,14,20]
count=len(values);angles=np.linspace(0,2*np.pi,count,endpoint=False)
colors=['#9dc1c5' if v<15 else '#d7a6b3' if v>25 else '#8e93af' for v in values]
fig,ax=plt.subplots(figsize=(8,5),subplot_kw={'projection':'polar'},dpi=150)
bars=ax.bar(angles,values,width=2*np.pi/count,bottom=10,color=colors,edgecolor='#f1f5f9',linewidth=1,zorder=2)
for bar,angle,value in zip(bars,angles,values):
    rotation=np.degrees(angle);flip=90<rotation<270
    ax.text(angle,value+7,str(value),ha='right' if flip else 'left',va='center',fontsize=8,fontweight='bold',rotation=rotation-180 if flip else rotation,rotation_mode='anchor',color='white',zorder=4)
handles=[Patch(color=c,label=l) for c,l in zip(['#9dc1c5','#8e93af','#d7a6b3'],['低值','中值','高值'])]
fig.legend(handles=handles,loc='center right',frameon=False)
ax.set_ylim(0,44);ax.set_yticks([]);ax.set_xticks(angles,np.arange(count))
ax.tick_params(axis='x',labelsize=8,pad=-5)
ax.grid(axis='x',linestyle='--',linewidth=.5,color='#8e93af',alpha=.5,zorder=1)
ax.spines['polar'].set_visible(False)
fig.text(.67,.72,'径向柱状图',fontsize=22,fontweight='bold',color='#515a85')
fig.subplots_adjust(left=.03,right=.67,top=.95,bottom=.05)
plt.show()
```
