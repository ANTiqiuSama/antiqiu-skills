# 新增图表的完整恢复配方

按用户提供的效果图顺序存储；编号仅用于定位，统一在全库检索。

## 1. 扇形小提琴与热图

用途：半圆热图、小提琴分布、外圈刻度与色标。

数据要求：各类别的样本分布，以及类别×指标数值矩阵。

来源：滚筒洗衣机；仅效果图，按图重建。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：仅有截图006效果图，未提供代码；按图重建扇形热图、KDE小提琴与四分位线，附可重复合成数据。；径向年份隔项显示并旋转，避免重叠；保留每一个热图环。

```python
"""扇形小提琴与热图
Restored/adapted from supplied screenshots [6].
Source: 滚筒洗衣机 (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
# Image-only reference (page 006, 滚筒洗衣机). Entire implementation reconstructed.
from scipy.stats import gaussian_kde
rng=np.random.default_rng(6)
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
years=np.arange(2000,2028,4)
means=.44+.16*np.sin(np.linspace(-np.pi/2,3*np.pi/2,12))
samples=[np.clip(rng.normal(m,.035,100),.2,.7) for m in means]
heat=np.vstack([np.clip(means+rng.normal(0,.025,12)+(i-3)*.008,.2,.7) for i in range(7)])
cmap=LinearSegmentedColormap.from_list('fan',palette_stops('diverging',center='#f4e5e9',reverse=True))
norm=Normalize(.2,.7)
fig,ax=plt.subplots(figsize=(10,5.5),subplot_kw={'projection':'polar'},dpi=150)
ax.set_theta_zero_location('E');ax.set_theta_direction(1)
ax.set_thetamin(0);ax.set_thetamax(180)
theta_edges=np.linspace(0,np.pi,13)
r_edges=np.linspace(.22,.7,8)
ax.pcolormesh(theta_edges,r_edges,heat[:,::-1],cmap=cmap,norm=norm,edgecolors='#ffffff88',linewidth=.5,shading='flat',alpha=.85)
centers=np.pi-(theta_edges[:-1]+theta_edges[1:])/2
for j,(theta,values) in enumerate(zip(centers,samples)):
    grid=np.linspace(values.min(),values.max(),120)
    density=gaussian_kde(values)(grid)
    halfwidth=density/density.max()*(np.pi/12)*.18
    radial=.83+(grid-.2)/.5*.35
    ax.fill(np.r_[theta-halfwidth,(theta+halfwidth)[::-1]],np.r_[radial,radial[::-1]],color=cmap(norm(np.median(values))),alpha=.85,edgecolor='#ffffff',linewidth=.6)
    for q in np.quantile(values,[.25,.5,.75]):
        w=float(np.interp(q,grid,halfwidth))*.8
        ax.plot([theta-w,theta+w],[.83+(q-.2)/.5*.35]*2,color='white',linestyle='--',linewidth=1.1)
    ax.plot([theta,theta],[.2,1.24],color='#dddddd',linestyle=':',linewidth=.5,zorder=0)
ax.set_xticks(centers,months,fontsize=10,color='#777777')
ax.set_yticks([])
for i in range(0,len(years),2):
    ax.text(np.pi+.05,(r_edges[i]+r_edges[i+1])/2,str(years[i]),fontsize=8,color='#777777',rotation=55,ha='right',va='top',clip_on=False)
ax.set_ylim(0,1.27);ax.grid(False);ax.spines['polar'].set_color('#bbbbbb')
ax.set_title('扇形热图与分布小提琴',pad=24,color='#515a85')
cb=fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),ax=ax,orientation='vertical',fraction=.035,pad=.07,shrink=.65)
cb.set_label('测量值（合成数据）')
plt.tight_layout();plt.show()
```

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

## 3. 三维分层热图

用途：多层热图平面、共享发散色标、单元格与三维轴。

数据要求：同形状的多层数值矩阵。

来源：@Doc mm；仅效果图，按图重建。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：仅有010效果图（署名 @Doc mm），整段实现按视觉结构重建；矩阵是固定种子的合成数据。

```python
"""三维分层热图
Restored/adapted from supplied screenshots [10].
Source: @Doc mm (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
# Image-only page 010 (@Doc mm); reconstructed layered heatmap with synthetic inputs.
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
rng=np.random.default_rng(10)
n_layers,n_rows,n_cols=4,5,10
base=np.sin(np.linspace(-np.pi,np.pi,n_cols))[None,:]*.55
matrices=np.clip(base+rng.normal(0,.25,(n_layers,n_rows,n_cols)),-1,1)
cmap=LinearSegmentedColormap.from_list('rc2',palette_stops('diverging',center='#f5f3ed'))
norm=Normalize(-1,1)
fig=plt.figure(figsize=(10,7),dpi=150);ax=fig.add_subplot(projection='3d')
for layer in range(n_layers):
    verts=[];facecolors=[]
    for row in range(n_rows):
        for col in range(n_cols):
            verts.append([(col,row,layer+1),(col+1,row,layer+1),(col+1,row+1,layer+1),(col,row+1,layer+1)])
            facecolors.append(cmap(norm(matrices[layer,row,col])))
    slab=Poly3DCollection(verts,facecolors=facecolors,edgecolors='#dddddd',linewidths=.4,alpha=.86)
    ax.add_collection3d(slab)
ax.set(xlim=(0,n_cols),ylim=(0,n_rows),zlim=(1,n_layers),xlabel='Gene',ylabel='Gradient tier')
ax.set_xticks(np.arange(n_cols)+.5,np.arange(1,n_cols+1));ax.set_yticks(np.arange(n_rows)+.5,np.arange(n_rows));ax.set_zticks(range(1,n_layers+1))
ax.view_init(elev=23,azim=-120);ax.set_box_aspect((1.5,1,1))
for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:axis.pane.fill=False
cb=fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),ax=ax,fraction=.035,pad=.06,shrink=.7)
cb.ax.set_title('RC2')
plt.tight_layout();plt.show()
```

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

## 5. 峰值标注堆叠面积图

用途：累计面积、白色边界、顶层峰值空心标记及数值。

数据要求：有序 x 和多条非负序列。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复多峰合成、累计面积、白边、空心峰值点和注释。；显式设定效果图的白色背景；演示图例移至上方。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""峰值标注堆叠面积图
Restored/adapted from supplied screenshots [17, 18, 19, 20, 21].
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
import random
from scipy.signal import find_peaks
read_custom_data = False
def create_data(x,size,n,max_value):
    sigma = size/30
    return max_value*np.exp(-.5*((x-n)/sigma)**2)
if read_custom_data:
    data = pd.read_csv('data.csv')
else:
    random.seed(16)
    size,x_max = 300,80
    x = np.linspace(0,x_max,size)
    peaks = [5,15,23,38,35,48,53,68]
    means = [2.5,1.2,3.,2.5,1.,1.5,2.,2.2]
    data = {'x':x}
    for i in range(4):
        y=np.zeros_like(x)
        for p,m in zip(peaks,means):
            y += create_data(x,x_max,p,m*random.random())
        data[f'类别{i+1}']=y
    data=pd.DataFrame(data)
x=data['x'].values
categories=[c for c in data.columns if c!='x']
colors=['#e7c2cb','#daa2b0','#cd8295','#c0627a']
fig=go.Figure()
for cat,color in zip(categories,colors):
    fig.add_trace(go.Scatter(x=x,y=data[cat],fill='tonexty',mode='none',name=cat,fillcolor=color,stackgroup='one'))
y_stack=np.cumsum(data[categories].T.values,axis=0)
for ys in y_stack:
    fig.add_trace(go.Scatter(x=x,y=ys,mode='lines',line=dict(width=2,color='#ffffff'),showlegend=False))
idx,_=find_peaks(y_stack[-1])
fig.add_trace(go.Scatter(x=x[idx],y=y_stack[-1][idx],mode='markers',marker=dict(symbol='circle',size=8,color='#ffffff',line=dict(width=2,color='#c0627a')),showlegend=False))
for px,py in zip(x[idx],y_stack[-1][idx]):
    fig.add_annotation(x=px,y=py+.3,text=f'{py:.2f}',showarrow=False)
fig.update_layout(xaxis=dict(title='X 轴',range=[0,70]),yaxis=dict(title='值',range=[0,10]),width=800,height=500,
                  legend=dict(orientation='h',y=1.08,x=.5,xanchor='center'))
# Match reference's white plot background; leave room for annotations.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',font=dict(color='#a65c70'),xaxis=dict(showgrid=False,showline=True,linecolor='#c99baa'),yaxis=dict(showgrid=False,showline=True,linecolor='#c99baa'))
fig.show()
```

## 6. 双指标三角热图

用途：每格双三角、独立色标、数值文本、透明填充和白边。

数据要求：形状及行列标签一致的两张矩阵。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""双指标三角热图
Restored/adapted from supplied screenshots [23, 24, 25, 26].
Source: 小明的代码美学 (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
from matplotlib.patches import Polygon
plt.rcParams.update({'axes.edgecolor':'white','axes.linewidth':.3,'xtick.major.size':0,'ytick.major.size':0,'xtick.color':'#c0627a','ytick.color':'#c0627a','text.color':'#c0627a','font.size':8})
read_custom_data=False
upper_color_list=palette_stops('diverging',count=5,center='#eeeeee',reverse=True)
lower_color_list=palette_stops('diverging',center='#eeeeee')
color_alpha=.75
def create_colormap(colors):
    return LinearSegmentedColormap.from_list('custom',colors,N=256)
def get_text_color(value,vmax,colors):
    n=value/vmax
    return contrast_text(create_colormap(colors)((n+1)/2),alpha=color_alpha)
if read_custom_data:
    upper_df=pd.read_csv('upper_data.csv',index_col=0)
    lower_df=pd.read_csv('lower_data.csv',index_col=0)
    if not upper_df.index.equals(lower_df.index) or not upper_df.columns.equals(lower_df.columns):
        raise ValueError('Upper/lower matrix labels must match')
    upper_data,lower_data=upper_df.values,lower_df.values
    row_labels,col_labels=list(upper_df.index),list(upper_df.columns)
else:
    np.random.seed(2)
    row_labels=[f'类别{chr(65+i)}' for i in range(8)]
    col_labels=[f'指标{i}' for i in range(1,19)]
    upper_data=np.random.randint(-100,101,(8,18))
    lower_data=np.random.randint(-100,101,(8,18))
num_rows,num_cols=upper_data.shape
fig,ax=plt.subplots(figsize=(11,5.5),dpi=150)
ax.set(xlim=(0,num_cols),ylim=(0,num_rows))
norm=Normalize(-100,100)
upper_cmap,lower_cmap=map(create_colormap,[upper_color_list,lower_color_list])
for i in range(num_rows):
    for j in range(num_cols):
        ax.add_patch(Polygon([[j,i],[j+1,i],[j,i+1]],facecolor=upper_cmap(norm(upper_data[i,j])),edgecolor='white',linewidth=.5,alpha=color_alpha))
        ax.text(j+.1,i+.4,f'{upper_data[i,j]:g}',fontsize=7,fontweight='bold',color=get_text_color(upper_data[i,j],100,upper_color_list))
        ax.add_patch(Polygon([[j+1,i],[j+1,i+1],[j,i+1]],facecolor=lower_cmap(norm(lower_data[i,j])),edgecolor='white',linewidth=.5,alpha=color_alpha))
        ax.text(j+.5,i+.8,f'{lower_data[i,j]:g}',fontsize=7,fontweight='bold',color=get_text_color(lower_data[i,j],100,lower_color_list))
ax.set_xticks(np.arange(num_cols)+.5,col_labels,rotation=90,fontweight='bold')
ax.set_yticks(np.arange(num_rows)+.5,row_labels,fontweight='bold')
ax.invert_yaxis();ax.set_aspect('equal')
fig.subplots_adjust(left=.08,right=.98,bottom=.18,top=.79)
for bounds,cmap,label in [([.1,.88,.38,.03],upper_cmap,'上三角指标'),([.57,.88,.38,.03],lower_cmap,'下三角指标')]:
    cb=fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),cax=fig.add_axes(bounds),orientation='horizontal',alpha=color_alpha)
    cb.ax.set_title(label,fontsize=10)
plt.show()
```

## 7. 三维涡旋向量图

用途：三维锥体方向、速度色阶、场景背景与长宽比。

数据要求：x、y、z、u、v、w 六列；坐标和向量单位明确。

来源：小明的代码美学；代码截图恢复，原数据缺失。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：vortex.csv未提供，005/029只是部分数值截图；默认改用明确标注的解析涡旋合成场。；原代码sizeref=60依赖原向量单位；演示场用1.3。真实数据须按单位调整。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维涡旋向量图
Restored/adapted from supplied screenshots [28].
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
# vortex.csv is absent from the archive. This analytic demo is explicitly synthetic.
read_custom_data=False
if read_custom_data:
    df=pd.read_csv('vortex.csv')
else:
    a=np.linspace(-4,4,9);b=np.linspace(-4,4,9);c=np.linspace(0,5,5)
    X,Y,Z=np.meshgrid(a,b,c,indexing='ij')
    df=pd.DataFrame(dict(x=X.ravel(),y=Y.ravel(),z=Z.ravel(),u=(-Y).ravel(),v=X.ravel(),w=np.full(X.size,1.5)))
fig=go.Figure(go.Cone(x=df.x,y=df.y,z=df.z,u=df.u,v=df.v,w=df.w,
    colorscale=['#ffffff','#e9d1ab','#c3476a'],sizemode='absolute',sizeref=1.3))
# The screenshot uses sizeref=60 for its unavailable dataset; 1.3 fits demo vector units.
fig.update_layout(margin=dict(l=0,r=0,t=0,b=0),scene=dict(
    xaxis=dict(title='X',backgroundcolor='#f7eff0'),yaxis=dict(title='Y',backgroundcolor='#f7eff0'),
    zaxis=dict(title='Z',backgroundcolor='#f7eff0'),aspectratio=dict(x=.7,y=1,z=.5)))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```

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

## 9. 三维螺旋气泡

用途：半透明气泡、大小与连续色彩编码、三维轨迹。

数据要求：x、y、z 与非负气泡大小变量。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维螺旋气泡
Restored/adapted from supplied screenshots [33, 34].
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
np.random.seed(42)
n_bubbles=100
t=np.linspace(0,4*np.pi,n_bubbles)
x=np.cos(t)+np.random.normal(scale=.2,size=n_bubbles)
y=np.sin(t)+np.random.normal(scale=.2,size=n_bubbles)
z=t+np.random.normal(scale=.2,size=n_bubbles)
z_normalized=z-z.min()
bubble_sizes=2*z_normalized+10
fig=go.Figure(go.Scatter3d(x=x,y=y,z=z,mode='markers',marker=dict(size=bubble_sizes,color=z,
    colorscale=[[0.,'#2f648e'],[.5,'#e9d1ab'],[1.,'#c3476a']],opacity=.7,colorbar=dict(title='Z 值'))))
fig.update_layout(scene=dict(xaxis_title='X',yaxis_title='Y',zaxis_title='Z'))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```

## 10. 三维体绘制

用途：低透明度多层体表面、连续色阶与深度叠加。

数据要求：三维网格上的标量场。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维体绘制
Restored/adapted from supplied screenshots [36].
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
from scipy import ndimage
np.random.seed(0)
l=30
X,Y,Z=np.mgrid[:l,:l,:l]
vol=np.zeros((l,l,l))
pts=(l*np.random.rand(3,15)).astype(int)
vol[tuple(indices for indices in pts)]=1
vol=ndimage.gaussian_filter(vol,4)
vol/=vol.max()
fig=go.Figure(go.Volume(x=X.flatten(),y=Y.flatten(),z=Z.flatten(),value=vol.flatten(),
    isomin=.2,isomax=.7,opacity=.1,surface_count=25,colorscale=[[0.,'#3768b0'],[.5,'#e9d1ab'],[1.,'#c3476a']] ))
fig.update_layout(scene={a:dict(title=a[0].upper(),backgroundcolor='#f2e2e4') for a in ['xaxis','yaxis','zaxis']},margin=dict(l=0,r=0,t=0,b=0))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```

## 11. 三维网格散点场

用途：规则点阵、位置高度与色阶双重编码、色标。

数据要求：规则 x/y 网格上的高度 z。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维网格散点场
Restored/adapted from supplied screenshots [38].
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
rows, cols = 32, 22
x = np.linspace(-1, 1, cols)
y = np.linspace(-1.7, 1.3, rows)
X, Y = np.meshgrid(x, y)
Z = np.exp(-((X+.5)**2+(Y+.5)**2)/.7)*1.5 + np.exp(-((X-.5)**2+(Y-.5)**2)/.3)
colorscale_custom = [[0., '#2f648e'], [.5, '#e9d1ab'], [1., '#c3476a']]

fig=go.Figure(go.Scatter3d(x=X.flatten(),y=Y.flatten(),z=Z.flatten(),mode='markers',marker=dict(size=4,color=Z.flatten(),colorscale=colorscale_custom,colorbar=dict(title='Color Scale'))))
fig.update_layout(scene=dict(xaxis_title='X',yaxis_title='Y',zaxis_title='Z'),margin=dict(l=0,r=0,t=0,b=0))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```

## 12. 三维等高线

用途：多高度等值曲线、逐层连续颜色与三维轴。

数据要求：规则 x/y 网格和连续高度矩阵。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维等高线
Restored/adapted from supplied screenshots [40, 41].
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
rows, cols = 32, 22
x = np.linspace(-1, 1, cols)
y = np.linspace(-1.7, 1.3, rows)
X, Y = np.meshgrid(x, y)
Z = np.exp(-((X+.5)**2+(Y+.5)**2)/.7)*1.5 + np.exp(-((X-.5)**2+(Y-.5)**2)/.3)
colorscale_custom = [[0., '#2f648e'], [.5, '#e9d1ab'], [1., '#c3476a']]

cmap=LinearSegmentedColormap.from_list('custom',[col for pos,col in colorscale_custom],N=256)
levels=np.linspace(Z.min(),Z.max(),20)
fig_contour=plt.figure()
cs=plt.contour(X,Y,Z,levels=levels)
plt.close(fig_contour)
fig=go.Figure()
for i,level in enumerate(cs.levels):
    for seg in cs.allsegs[i]:
        if len(seg)==0: continue
        color=to_hex(cmap((level-Z.min())/(Z.max()-Z.min())))
        fig.add_trace(go.Scatter3d(x=seg[:,0],y=seg[:,1],z=[level]*len(seg),mode='lines',line=dict(color=color,width=8),showlegend=False))
fig.update_layout(scene=dict(xaxis_title='X',yaxis_title='Y',zaxis_title='Z'),margin=dict(l=0,r=0,t=0,b=0))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```

## 13. 三维方柱曲面

用途：独立网格方柱、全局高度色阶、十二条白色立方体棱线。

数据要求：二维网格及每格非负高度；本例高度并非频数。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：原标题称三维直方图，但高度来自连续合成曲面；卡片称方柱曲面，真实频数需先分箱计数。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维方柱曲面
Restored/adapted from supplied screenshots [43, 44, 45].
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
def hex_to_rgb(hex_color):
    h=hex_color.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))
def rgb_to_hex(rgb):
    return '#%02x%02x%02x'%tuple(rgb)
def interpolate_color(value,color_list):
    if value<=0:return color_list[0]
    if value>=1:return color_list[-1]
    n=len(color_list)-1
    segment=min(int(value*n),n-1)
    local_t=(value-segment/n)*n
    rgb1,rgb2=map(hex_to_rgb,color_list[segment:segment+2])
    return rgb_to_hex(tuple(int((1-local_t)*a+local_t*b) for a,b in zip(rgb1,rgb2)))
def towers(fig,a,e,pos_x,pos_y,color_list,global_min,global_max):
    x_vals=np.linspace(pos_x-a/2,pos_x+a/2,2)
    y_vals=np.linspace(pos_y-a/2,pos_y+a/2,2)
    x,y,z=np.meshgrid(x_vals,y_vals,[0,e])
    color=interpolate_color((e-global_min)/(global_max-global_min) if global_max!=global_min else 0,color_list)
    fig.add_trace(go.Mesh3d(x=x.flatten(),y=y.flatten(),z=z.flatten(),alphahull=1,flatshading=True,color=color))
    vertices=np.array([[pos_x-a/2,pos_y-a/2,0],[pos_x+a/2,pos_y-a/2,0],
      [pos_x+a/2,pos_y+a/2,0],[pos_x-a/2,pos_y+a/2,0],
      [pos_x-a/2,pos_y-a/2,e],[pos_x+a/2,pos_y-a/2,e],
      [pos_x+a/2,pos_y+a/2,e],[pos_x-a/2,pos_y+a/2,e]])
    edges=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
    edge_x,edge_y,edge_z=[],[],[]
    for a,b in edges:
        edge_x.extend([vertices[a,0],vertices[b,0],None])
        edge_y.extend([vertices[a,1],vertices[b,1],None])
        edge_z.extend([vertices[a,2],vertices[b,2],None])
    fig.add_trace(go.Scatter3d(x=edge_x,y=edge_y,z=edge_z,mode='lines',line=dict(color='white',width=3)))
rows,cols=16,11
x,y=np.linspace(-1,1,cols),np.linspace(-1.7,1.3,rows)
X,Y=np.meshgrid(x,y)
Z=np.exp(-((X+.5)**2+(Y+.5)**2)/.7)*1.5+np.exp(-((X-.5)**2+(Y-.5)**2)/.3)
color_list=['#214e81','#8d9eb2','#cccccc','#dc9fb0','#c2768b']
fig=go.Figure()
for xv,yv,zv in zip(X.flatten(),Y.flatten(),Z.flatten()):
    towers(fig,.15,zv,xv,yv,color_list,Z.min(),Z.max())
fig.update_layout(showlegend=False,margin=dict(l=0,r=0,t=0,b=0),scene=dict(
    xaxis=dict(title='X',backgroundcolor='#f8f1f1'),yaxis=dict(title='Y',backgroundcolor='#f8f1f1'),
    zaxis=dict(title='Z',backgroundcolor='#f8f1f1'),aspectmode='data'))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```

## 14. 三维网格曲面

用途：连续曲面色阶、白色横纵等值网格、三维坐标。

数据要求：规则网格 X、Y、Z。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。；使用Plotly交互显示；预览通过Kaleido导出，画布和边距适配截图检查。3D PDF内部仍含栅格渲染。

```python
"""三维网格曲面
Restored/adapted from supplied screenshots [47].
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
rows, cols = 32, 22
x = np.linspace(-1, 1, cols)
y = np.linspace(-1.7, 1.3, rows)
X, Y = np.meshgrid(x, y)
Z = np.exp(-((X+.5)**2+(Y+.5)**2)/.7)*1.5 + np.exp(-((X-.5)**2+(Y-.5)**2)/.3)
colorscale_custom = [[0., '#2f648e'], [.5, '#e9d1ab'], [1., '#c3476a']]

fig=go.Figure(go.Surface(x=X,y=Y,z=Z,colorscale=colorscale_custom,contours={
 'x':dict(show=True,color='white',width=1,start=x.min(),end=x.max(),size=.1),
 'y':dict(show=True,color='white',width=1,start=y.min(),end=y.max(),size=.1)}))
fig.update_layout(scene=dict(xaxis_title='X',yaxis_title='Y',zaxis_title='Z'),margin=dict(l=0,r=0,t=0,b=0))
# Export-safe frame leaves room for outer 3D ticks.
fig.update_layout(margin=dict(l=30,r=30,t=30,b=35))
fig.update_layout(scene_camera=dict(eye=dict(x=1.65,y=1.65,z=1.5)))
fig.show()
```

## 15. 多型号价格堆叠面积

用途：按总量排序、透明面积、白色分界和两列图例。

数据要求：Model、Yas、Fiyat ($) 长表；同一年龄覆盖全部型号。

来源：小明的代码美学；代码截图恢复，原数据缺失。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：原airplane_price_dataset.csv未提供，补充同字段固定种子的合成长表。；年龄排序后再绘制；缺失型号×年龄单元报错而非静默补零。图轴明确是型号均价的累计值，不代表市场总额。

```python
"""多型号价格堆叠面积
Restored/adapted from supplied screenshots [49, 50, 51].
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
def load_data(file_path):
    return pd.read_csv(file_path)
read_custom_data=False
if read_custom_data:
    data=load_data('airplane_price_dataset.csv')
else:
    # The archive does not include aircraft price data. This is a synthetic schema demo.
    rng=np.random.default_rng(48)
    models=['Boeing 777','Boeing 737','Airbus A350','Airbus A330','Bombardier CRJ900','Cessna 172']
    records=[]
    for i,model in enumerate(models):
        for age in range(46):
            for k in range(5):
                price=(4.8e8-i*5.5e7)*(.4+.6*np.exp(-age/12))*rng.uniform(.95,1.05)
                records.append((model,age,price))
    data=pd.DataFrame(records,columns=['Model','Yas','Fiyat ($)'])
plt.rcParams.update({'axes.facecolor':'#f1f5f9','axes.edgecolor':'white','axes.labelcolor':'#515a85','text.color':'#515a85','xtick.color':'#515a85','ytick.color':'#515a85'})
def create_stacked_area_chart(ax,data):
    age_groups=data.groupby(['Model','Yas'])['Fiyat ($)'].mean().reset_index()
    models=age_groups['Model'].unique()
    colors=['#214e81','#6983a2','#8d9eb2','#b59fb1','#dc9fb0','#c2768b']
    ages=np.sort(age_groups['Yas'].unique())
    y_list=[]
    for model in models:
        model_data=age_groups[age_groups.Model==model]
        y_values=model_data.set_index('Yas').reindex(ages)['Fiyat ($)'].values
        if np.isnan(y_values).any():raise ValueError('Missing age/model cells need explicit treatment; not zero filling')
        y_list.append((model,y_values))
    y_list.sort(key=lambda x:np.sum(x[1]),reverse=True)
    bottom=np.zeros(len(ages))
    for i,(model,y_values) in enumerate(y_list):
        ax.fill_between(ages,bottom,bottom+y_values,label=model,color=colors[i],alpha=.6,edgecolor='white',linewidth=1)
        bottom+=y_values
    ax.set(xlabel='使用年限（年）',ylabel='各型号均价的累计值（$）',xlim=(ages.min(),ages.max()),ylim=(0,max(2e9,bottom.max()*1.1)))
    ax.legend(loc='upper right',bbox_to_anchor=(.98,.98),ncol=2,fontsize=8)
fig,ax=plt.subplots(figsize=(8,5),dpi=150)
create_stacked_area_chart(ax,data)
plt.tight_layout();plt.show()
```

## 16. 同心环形柱状图

用途：同心圆弧、三档颜色、圆弧内数值和径向标签。

数据要求：类别及非负数值；所有环共享角度尺度。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""同心环形柱状图
Restored/adapted from supplied screenshots [53, 54, 55].
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
values=[11,12,12,14,15,20,22,22,24,24,26,27]
max_value=max(values)*1.1
num_rings=len(values)
categories=[f'类别{i+1}' for i in range(num_rings)]
fig,ax=plt.subplots(figsize=(8,5),subplot_kw={'projection':'polar'},dpi=150)
ax.set_theta_direction(-1);ax.set_theta_offset(np.pi/2)
inner_radius_offset=2
for i,(label,value) in enumerate(zip(categories,values)):
    inner_radius=i+inner_radius_offset
    ring_width=.8
    theta_start=0;theta_end=value/max_value*2*np.pi
    rotation=-np.degrees((theta_start+theta_end)/2) if np.degrees(theta_end)<180 else 180-np.degrees((theta_start+theta_end)/2)
    color='#9dc1c5' if value<15 else '#d7a6b3' if value>25 else '#8e93af'
    ax.bar(x=(theta_start+theta_end)/2,height=ring_width,width=theta_end-theta_start,bottom=inner_radius,color=color)
    ax.text((theta_start+theta_end)/2,inner_radius+ring_width/2,f'{value}',ha='center',va='center',color='white',fontsize=6,fontweight='bold',rotation=rotation,rotation_mode='anchor')
handles=[Patch(color=c,label=l) for c,l in zip(['#9dc1c5','#8e93af','#d7a6b3'],['低值','中值','高值'])]
fig.legend(handles=handles,loc='center right',frameon=False)
ax.set_xticks([]);ax.set_yticks(np.arange(num_rings)+inner_radius_offset,categories,fontsize=6)
ax.set_rlabel_position(0)
ax.grid(axis='y',linestyle='-',linewidth=1,color='white')
ax.spines['polar'].set_visible(False)
fig.suptitle('环形柱状图',x=.02,ha='left')
plt.tight_layout();plt.show()
```

## 17. 南丁格尔玫瑰图

用途：变角宽扇柱、中心留白、白色分隔和标签框。

数据要求：正值类别表；角宽与半径都编码值，不按面积读比例。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：原百分比公式width/pi*100会合计200%；改为value/sum(values)*100。；设置半径下界0以显示源码bottom=10的中心留白，微调前两个标签位置避免碰撞。

```python
"""南丁格尔玫瑰图
Restored/adapted from supplied screenshots [57, 58].
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
values=np.array([30,35,40,45,50,55,60,65,70])
labels=[f'类别{i+1}' for i in range(len(values))]
width=2*np.pi*values/sum(values)
colors=['#dc9eb5','#e3d0d7','#b0a3c0']*3
fig,ax=plt.subplots(subplot_kw={'projection':'polar'},figsize=(8,5),dpi=150)
start_x=0
for i,value in enumerate(values):
    start_x+=.5*width[i]
    ax.bar(start_x,value,width=width[i],bottom=10.,linewidth=2,edgecolor='white',color=colors[i])
    # Correct the screenshot's percentage formula (width / 2pi, not width / pi).
    label=f'{labels[i]}\n{value/values.sum()*100:.1f}% | {value}'
    offset=[12,-4,0,0,0,0,0,0,0][i]
    ax.text(start_x,value*.75+10+offset,label,color='white',fontsize=7,ha='center',va='center',fontweight='bold',
            bbox=dict(facecolor='#75879655',edgecolor='none',boxstyle='round,pad=.5'))
    start_x+=.5*width[i]
ax.set(xticks=[],yticks=[],ylim=(0,85))
ax.spines['polar'].set_visible(False)
ax.set_theta_direction(1);ax.set_theta_offset(np.pi*.5)
fig.text(.18,.5,'南丁格尔\n玫瑰图',fontsize=24,ha='center',va='center',fontweight='bold',color='#515a85')
fig.subplots_adjust(left=.32,right=.98,top=.98,bottom=.02)
plt.show()
```

## 18. 嵌套环形图

用途：内外两层圆环、外圈半透明、内外注释框。

数据要求：父类别和子类别的非负数值，父值等于子值之和。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""嵌套环形图
Restored/adapted from supplied screenshots [60, 61, 62].
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
colors=['#dc9eb5','#b8b2b9','#b0a3c0','#e3d0d7','#ebe8f0']
main_name=['类别A','类别B','类别C']
sub_name=['子类A-1','子类A-2','子类B-1','子类C-1','子类C-2','子类C-3']
value_list=[[100.,120.],[37.],[29.,10.,20.]]
fig,ax=plt.subplots(subplot_kw={'projection':'polar'},figsize=(8,5),dpi=150)
size=.2
ax.set_ylim(0,.8);ax.set_axis_off()
sum_vals=sum(map(sum,value_list))
main_divided=[sum(v)/sum_vals*2*np.pi for v in value_list]
main_x=np.cumsum([0]+main_divided[:-1])
main_colors=colors[:len(value_list)]
main_bars=ax.bar(main_x,width=main_divided,bottom=size,height=size,color=main_colors,edgecolor='white',linewidth=1,align='edge')
sub_values=[v for group in value_list for v in group]
sub_divided=[v/sum_vals*2*np.pi for v in sub_values]
sub_x=np.cumsum([0]+sub_divided[:-1])
sub_colors=[main_colors[i] for i,group in enumerate(value_list) for _ in group]
sub_bars=ax.bar(sub_x,width=sub_divided,bottom=2*size,height=size*.5,color=sub_colors,alpha=.5,edgecolor='white',linewidth=2,align='edge')
for bars,names,values,offset,face in [(main_bars,main_name,list(map(sum,value_list)),-.1,'#75879655'),(sub_bars,sub_name,sub_values,.1,'#75879677')]:
    for bar,label,val in zip(bars,names,values):
        angle=bar.get_x()+bar.get_width()/2
        distance=bar.get_height()+bar.get_y()+offset
        ax.text(angle,distance,f'{label}\n{val/sum_vals*100:.1f}% | {val:.0f}',color='white',fontsize=8,ha='center',va='center',fontweight='bold',bbox=dict(facecolor=face,edgecolor='none',boxstyle='round,pad=.5'))
fig.text(.16,.5,'嵌套环形图',fontsize=23,ha='center',va='center',fontweight='bold',color='#515a85')
fig.subplots_adjust(left=.28,right=1,top=1,bottom=.02)
plt.show()
```

## 19. 排名圆弧条形图

用途：按值排序圆弧、连续色阶、起点名称和端点值。

数据要求：类别及可排序的非负百分比。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：保留Faker公司名、共享角度尺度和渐变圆弧；适度扩大画布与文字布局。

```python
"""排名圆弧条形图
Restored/adapted from supplied screenshots [64, 65, 66].
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
from faker import Faker
Faker.seed(6);np.random.seed(6)
fake=Faker()
company_name=[fake.company() for _ in range(16)]
growth_data=np.sort(np.random.uniform(0,100,16))
def create_colors(hex_colors,data):
    cmap=LinearSegmentedColormap.from_list('custom',hex_colors)
    sm=ScalarMappable(norm=Normalize(min(data),max(data)),cmap=cmap)
    return [sm.to_rgba(v)[:3] for v in data]
fig,ax=plt.subplots(figsize=(10,8),subplot_kw={'projection':'polar'},dpi=150)
max_value=max(growth_data)*2.75
colors=create_colors(['#214e81','#a55d75'],growth_data)
inner_radius=15
for i,(label,value) in enumerate(zip(company_name,growth_data)):
    inner_radius+=1.7;ring_width=1.5
    theta_start=0;theta_end=value/max_value*2*np.pi
    ax.bar((theta_start+theta_end)/2,height=ring_width,width=theta_end-theta_start,bottom=inner_radius,color=colors[i],alpha=.85)
    attr=dict(color=colors[i],rotation=np.degrees(theta_end)+5,ha='left') if theta_end<np.pi/2 else dict(color='white',rotation=np.degrees(theta_end-np.pi)-5,ha='left')
    ax.text(theta_end,inner_radius+ring_width/2,f' {value:.1f}%',va='center',fontsize=8,fontweight='bold',rotation_mode='anchor',**attr)
    ax.text(-.01,inner_radius+ring_width/2,label,ha='right',va='center',color=colors[i],fontsize=8,fontweight='bold')
ax.set(xticks=[],yticks=[],ylim=(0,inner_radius+3))
ax.grid(False);ax.spines['polar'].set_visible(False)
ax.set_theta_direction(1);ax.set_theta_offset(np.pi*1.5)
fig.text(.06,.91,'公司增长率排名',fontsize=24,fontweight='bold',color='#575864')
fig.text(.06,.86,'合成数据 · 共享角度尺度',fontsize=12,color='#575864')
fig.subplots_adjust(left=.12,right=.99,top=.9,bottom=.06)
plt.show()
```

## 20. 正负折叠地平线图

用途：正负色彩、四层透明折叠、白边与多行偏移。

数据要求：同一 x 上多条有符号序列，统一折叠层宽。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""正负折叠地平线图
Restored/adapted from supplied screenshots [68, 69, 70].
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
from scipy.interpolate import make_interp_spline
from matplotlib.patches import Patch
def create_data(x,size,n,max_value):
    sigma=size/30
    return max_value*np.exp(-.5*((x-n)/sigma)**2)
np.random.seed(3)
x=np.linspace(0,80,300)
y_list=[]
for i in range(20):
    peaks=np.sort(np.random.uniform(0,80,size=200))
    means=np.random.uniform(-.25,.3,200)
    temp_y=sum(create_data(x,80,p,m) for p,m in zip(peaks,means))
    y_list.append(temp_y)
fig,ax=plt.subplots(figsize=(10,6),dpi=150)
y_offset=.6
for i,y in enumerate(y_list):
    x_smooth=np.linspace(x.min(),x.max(),500)
    y_smooth=make_interp_spline(x,y)(x_smooth)
    for sign,color in [(1,'#e98184'),(-1,'#81b7d9')]:
        y_pos=np.maximum(sign*y_smooth,0)
        for j in range(4):
            y_plot=np.maximum(np.minimum(y_pos,y_offset*(j+1)),y_offset*j)
            y_bottom=y_offset*i
            y_top=y_plot-j*y_offset+y_offset*i
            ax.fill_between(x_smooth,y_bottom,y_top,color=color,alpha=.5)
            ax.plot(x_smooth,y_top,color='white',linewidth=.5)
ax.set(xlim=(0,70),ylim=(0,13))
ax.set_xticks([1.5,10,20,30,40,50,60,68.5],range(2020,2028),fontweight='bold',color='#81b7d9')
ax.set_yticks([.3+i*.6 for i in range(20)],[chr(i) for i in range(65,85)],fontweight='bold',color='#81b7d9')
ax.legend(handles=[Patch(color='#e98184',label='正向偏差'),Patch(color='#81b7d9',label='负向偏差')],loc='upper right',ncols=2,frameon=False)
ax.set_title('正负折叠地平线图',loc='left',color='#3680ae',fontweight='bold')
plt.tight_layout();plt.show()
```

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

## 22. 透明弦图

用途：扇区轨道、透明弦带、刻度和白色轨道边界。

数据要求：非负方阵，行列类别顺序一致；明确方向语义。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""透明弦图
Restored/adapted from supplied screenshots [76, 77].
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
from pycirclize import Circos
def generate_random_matrix(size,min_value,max_value,large_value_prob=.1):
    matrix=np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            if i!=j:
                matrix[i,j]=np.random.uniform(max_value*.95,max_value) if np.random.rand()<large_value_prob else np.random.uniform(min_value,max_value*.1)
    return matrix.tolist()
labels=[f'基因{chr(65+i)}' for i in range(10)]
color_map=['#214e81','#c0627a']*5
cmap={label:color+'77' for label,color in zip(labels,color_map)}
np.random.seed(2)
interaction_df=pd.DataFrame(generate_random_matrix(10,1,500,.2),index=labels,columns=labels)
circos=Circos.initialize_from_matrix(interaction_df,space=3,r_lim=(63,70),cmap=cmap,ticks_interval=500,
    label_kws=dict(r=64,size=6,color='white',fontweight='bold'),
    ticks_kws=dict(line_kws=dict(ec='#597cab'),text_kws=dict(weight='bold'),label_size=6),link_kws=dict(alpha=.4))
for sector in circos.sectors:
    sector.tracks[0].axis(ec='white',lw=1.5)
fig=circos.plotfig(figsize=(8,5),dpi=150)
fig.text(.04,.57,'基因关联弦图',fontsize=21,fontweight='bold',color='#515a85')
fig.text(.04,.48,'Synthetic interactions',fontsize=11,fontweight='bold')
fig.subplots_adjust(left=.32,right=1,top=1,bottom=0)
plt.show()
```

## 23. 带边际柱形的表格热图

用途：热图文本、白格线、上方列和、右方行和及数值。

数据要求：有行列标签的数值矩阵，边际求和有意义。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""带边际柱形的表格热图
Restored/adapted from supplied screenshots [79, 80, 81, 82, 83].
Source: 小明的代码美学 (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'axes.edgecolor':'white','xtick.major.size':0,'ytick.major.size':0,'xtick.labelsize':7,'ytick.labelsize':7,'text.color':'#3680ae','xtick.color':'#3680ae','ytick.color':'#3680ae'})
cmap=LinearSegmentedColormap.from_list('custom',palette_stops('diverging',count=5),N=300)
years=np.arange(1985,2021)
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
np.random.seed(10)
data=np.random.uniform(-1,1,(len(months),len(years)))
for i in range(len(months)):data[i]+=np.linspace(-1,2,len(years))
data+=np.random.uniform(-1.5,1.5,data.shape)
bar_data_year=data.sum(axis=0);bar_data_month=data.sum(axis=1)
fig=plt.figure(figsize=(12,6),dpi=150)
gs=GridSpec(2,2,width_ratios=[10,1.5],height_ratios=[1,2],wspace=.04,hspace=.05)
ax_heatmap=fig.add_subplot(gs[1,0])
ax_heatmap.imshow(data,cmap=cmap,aspect='auto',vmin=-np.max(np.abs(data)),vmax=np.max(np.abs(data)))
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        v=data[i,j];color=contrast_text(cmap((v/np.max(np.abs(data))+1)/2))
        ax_heatmap.text(j,i,f'{v:.1f}',ha='center',va='center',fontsize=6,color=color,fontweight='bold')
for i in range(data.shape[0]+1):ax_heatmap.plot([-.5,data.shape[1]-.5],[i-.5]*2,color='white',linewidth=1)
for j in range(data.shape[1]+1):ax_heatmap.plot([j-.5]*2,[-.5,data.shape[0]-.5],color='white',linewidth=1)
ax_heatmap.set_xticks(np.arange(len(years)),years,rotation=90,fontweight='bold')
ax_heatmap.set_yticks(np.arange(len(months)),months,fontweight='bold')
ax_top=fig.add_subplot(gs[0,0],sharex=ax_heatmap)
ax_top.bar(np.arange(len(years)),bar_data_year,color=[palette_stops('diverging')[0] if v<0 else palette_stops('diverging')[-1] for v in bar_data_year])
ax_top.tick_params(axis='both',bottom=False,left=False,labelbottom=False,labelleft=False)
ax_top.grid(False)
ax_right=fig.add_subplot(gs[1,1],sharey=ax_heatmap)
ax_right.barh(np.arange(len(months)),bar_data_month,color=[palette_stops('diverging')[0] if v<0 else palette_stops('diverging')[-1] for v in bar_data_month])
ax_right.tick_params(axis='both',bottom=False,left=False,labelbottom=False,labelleft=False)
ax_right.grid(False)
for i,v in enumerate(bar_data_year):
    ax_top.text(i,v+(.2 if v>0 else -.8),f'{v:.1f}',ha='center',va='bottom' if v>0 else 'top',fontsize=6,color=palette_stops('diverging')[-1] if v>0 else palette_stops('diverging')[0],fontweight='bold')
ax_top.margins(y=.25)
for i,v in enumerate(bar_data_month):
    ax_right.text(v-1 if v>0 else v+1,i,f'{v:.1f}',ha='right' if v>0 else 'left',va='center',fontsize=7,color='white',fontweight='bold')
fig.suptitle('表格热图与边际汇总',x=.06,y=.98,ha='left',fontsize=22,color='#3680ae')
fig.subplots_adjust(left=.06,bottom=.14,right=.97,top=.88)
plt.show()
```

## 24. 阶梯折线与区间带

用途：阶梯曲线、阶梯透明区间、双色层次和注释。

数据要求：x、各组估计值及上下界；真实区间必须来自计算。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：原区间宽度随机生成，卡片与示例明确标为示意区间；真实置信区间必须由真实统计估计替换。

```python
"""阶梯折线与区间带
Restored/adapted from supplied screenshots [85, 86].
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
import matplotlib.ticker as ticker
x=np.arange(1860,2020)
np.random.seed(3)
y1=np.random.uniform(20,30,len(x))+10*np.sin(np.linspace(0,3*np.pi,len(x)))
y2=np.random.uniform(50,55,len(x))+5*np.sin(np.linspace(0,3*np.pi,len(x)))
y3=np.random.uniform(80,85,len(x))+7*np.sin(np.linspace(0,3*np.pi,len(x)))
# Widths are synthetic illustration intervals, not estimated confidence intervals.
ci1=np.random.uniform(4,5,len(x));ci2=np.random.uniform(4,7,len(x));ci3=np.random.uniform(5,9,len(x))
line_colors=['#8e93af','#d7a6b3','#eac890'];edge_colors=['#3f51af','#d7607e','#eab159']
fig,ax=plt.subplots(figsize=(10,5),dpi=150)
ax.set_facecolor('#f4f6f8')
for i,(y,ci,fill_color,line_color) in enumerate(zip([y1,y2,y3],[ci1,ci2,ci3],line_colors,edge_colors)):
    ax.step(x,y,label=f'类别{chr(65+i)}',linewidth=1,where='mid',color=line_color,zorder=3)
    ax.fill_between(x,y-ci,y+ci,label=f'示意区间{chr(65+i)}',alpha=.4,step='mid',color=fill_color,zorder=3 if i<2 else 2)
ax.text(1940,5,'低值期',ha='center',color='#3f51af',fontweight='bold')
ax.text(2000,80,'高值期',ha='center',color='#eab159',fontweight='bold')
ax.set(xlim=(1860,2020),ylim=(0,120))
ax.legend(loc='upper right',ncols=3,frameon=False)
ax.grid(axis='y',which='major',linestyle='-',linewidth=1,color='white',zorder=1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.set_title('阶梯趋势及区间带（合成数据）',loc='left')
plt.tight_layout();plt.show()
```

## 25. 双向峰形河流图

用途：wiggle 基线、144条峰形带、白色边界和分档颜色。

数据要求：同一 x 上的非负序列。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：合并008（第一代码页）与088–090，恢复144条双向峰形和wiggle基线。；原颜色按峰值分档但色条为连续映射；色条改为同一组阈值和颜色，使图例与实际颜色一致。

```python
"""双向峰形河流图
Restored/adapted from supplied screenshots [8, 88, 89, 90].
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
import matplotlib.ticker as ticker
from matplotlib.colors import ListedColormap, BoundaryNorm
def generate_single_weighted_random(scale=1.5,lower=1,upper=10):
    return np.clip(np.random.exponential(scale)+lower,lower,upper)
def create_smooth_peak_data(x,start,peak,end,max_value):
    y=np.zeros_like(x)
    rising=(x>=start)&(x<=peak);sigma_rise=(peak-start)/3
    y[rising]=max_value*np.exp(-((x[rising]-peak)**2)/(2*sigma_rise**2))
    falling=(x>peak)&(x<=end);sigma_fall=(end-peak)/3
    y[falling]=max_value*np.exp(-((x[falling]-peak)**2)/(2*sigma_fall**2))
    return y
hex_colors=['#214e81','#456991','#6983a2','#8d9eb2','#dc9fb0','#cf8b9e','#c2768b','#a55d75']
thresholds=[5,7.5,8,12,15,20,25]
def assign_color(value):return hex_colors[sum(value>t for t in thresholds)]
np.random.seed(30)
x=np.linspace(0,800,800)
y_list,color_list,categories=[],[],[]
def generate_data(num_categories,start_base,peak_base,end_base,interval,direction):
    for i in range(num_categories):
        offset=i*interval if direction=='forward' else -i*interval
        max_value=generate_single_weighted_random(6,1,10000)
        y_list.append(create_smooth_peak_data(x,start_base+offset,peak_base+offset,end_base+offset,max_value))
        color_list.append(assign_color(max_value));categories.append(f'类别{len(categories)+1}')
generate_data(72,720,740,820,10,'backward');generate_data(72,0,20,100,10,'forward')
y_list=np.array(y_list)
fig,ax=plt.subplots(figsize=(10,5),dpi=150)
polys=ax.stackplot(x,y_list,colors=color_list,labels=categories,zorder=10,alpha=1,baseline='wiggle')
for poly in polys:
    verts=poly.get_paths()[0].vertices
    ax.plot(verts[:,0],verts[:,1],color='white',zorder=20,linewidth=.5)
# Colors are discrete peak-amplitude bins in the original; show matching bin boundaries.
cmap=ListedColormap(hex_colors);norm=BoundaryNorm([0,*thresholds,40],cmap.N)
cb=fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),ax=ax,orientation='vertical',pad=.01,fraction=.05,extend='max')
cb.set_label('序列峰值分档');cb.ax.tick_params(size=0)
ax.grid(axis='x',which='major',linestyle='-',linewidth=1,color='white')
ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
ax.set_xticks(range(0,801,100),range(2020,2029));ax.set(ylim=(-75,75),yticks=[])
ax.set_title('双向峰形河流图',loc='left')
plt.tight_layout();plt.show()
```

## 26. 相关矩阵与连线网络

用途：三角矩阵、方块大小及发散色、连线宽度颜色、三种图例。

数据要求：相关矩阵及每个网络节点到特征的 r/p 表。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：原示例随机方阵并非有效相关矩阵；演示改由合成样本计算对称Pearson矩阵。；原方块宽高直接使用带符号r；改为abs(r)，颜色保留符号。线宽按abs(r)分档。；修正连续颜色插值和标签与矩阵坐标的对应。网络r/p仍为演示输入，不声称做了Mantel检验；真实任务需提供实际检验结果。

```python
"""相关矩阵与连线网络
Restored/adapted from supplied screenshots [92, 93, 94, 95, 96, 97].
Source: 小明的代码美学 (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
from matplotlib import patches,lines
# Original uses arbitrary random matrix and network statistics. Demo below uses a real
# sample correlation matrix; the r/p network table remains explicitly illustrative.
feature_labels='N P K Ca Mg S Al Fe Mn Zn Mo pH'.split()
feature_count=len(feature_labels);spec_labels=['spec1','spec2','spec3']
np.random.seed(10)
latent=np.random.normal(size=(100,3))
observations=latent@np.random.normal(size=(3,feature_count))+np.random.normal(size=(100,feature_count))*.8
pearson_data=np.corrcoef(observations,rowvar=False)
p_data=np.random.beta(.8,5,(len(spec_labels),feature_count))
r_data=np.random.uniform(-1,1,(len(spec_labels),feature_count))
def calc_p_color(value):return palette_stops('diverging')[-1] if value<.01 else palette_stops('diverging')[0] if value<.05 else '#c7c7c7'
def calc_r_width(value):return 1. if abs(value)<.2 else 2. if abs(value)<.4 else 4.
def gradient_color(min_value,max_value,hex_colors,value):
    if max_value==min_value:return hex_colors[len(hex_colors)//2]
    n=np.clip((value-min_value)/(max_value-min_value),0,1)
    cmap=LinearSegmentedColormap.from_list('corr',hex_colors)
    return to_hex(cmap(float(n)))
fig,ax=plt.subplots(figsize=(10,7),dpi=150)
spec_pos_y=np.linspace(0,feature_count,len(spec_labels)+2).tolist()
for i,spec in enumerate(spec_labels):
    ax.text(spec_pos_y[i+1]-4.5,spec_pos_y[-2-i]-3.5,spec,ha='center',va='center')
    for j in range(feature_count):
        ax.plot([spec_pos_y[i+1]-4,-.5+j],[spec_pos_y[-2-i]-3,feature_count-j-.5],linestyle='-',linewidth=calc_r_width(r_data[i,j]),color=calc_p_color(p_data[i,j]),zorder=1-p_data[i,j],marker='o',markersize=4)
pearson_colors=palette_stops('diverging',center='#ecf4f8')
for i in range(feature_count):
    for j in range(i,feature_count):
        value=pearson_data[i,j];size=abs(value)
        color=gradient_color(-1,1,pearson_colors,value)
        ax.add_patch(patches.Rectangle((feature_count-i-1,j),1,1,linewidth=.25,edgecolor='#999999',facecolor='white'))
        ax.add_patch(patches.Rectangle((feature_count-i-.5-size/2,j+.5-size/2),size,size,linewidth=.5,edgecolor='#999999',facecolor=color))
# Matrix coordinates are reversed in x; labels follow matrix indices.
for i,label in enumerate(feature_labels):
    ax.text(feature_count-i-.5,feature_count+.5,label,ha='center',va='center',fontsize=8)
    ax.text(feature_count+.5,i+.5,label,ha='center',va='center',fontsize=8)
p_handles=[patches.Patch(color=c,label=l) for c,l in zip([palette_stops('diverging')[-1],palette_stops('diverging')[0],'#c7c7c7'],['< 0.01','0.01–0.05','≥ 0.05'])]
leg=ax.legend(handles=p_handles,title='示例关联 p',bbox_to_anchor=(1,.99),frameon=False);ax.add_artist(leg)
r_handles=[lines.Line2D([],[],color='#a9a9a9',linewidth=w,label=l) for w,l in zip([1,2,4],['< 0.2','0.2–0.4','≥ 0.4'])]
leg=ax.legend(handles=r_handles,title='示例 |r|',bbox_to_anchor=(1,.67),frameon=False);ax.add_artist(leg)
cmap=LinearSegmentedColormap.from_list('pearson',pearson_colors)
cb=fig.colorbar(ScalarMappable(norm=Normalize(-1,1),cmap=cmap),cax=fig.add_axes([.81,.13,.025,.19]))
cb.ax.set_title("Pearson's r",fontsize=9)
ax.set(xticks=[],yticks=[],xlim=(-2,feature_count+8),ylim=(-1,feature_count+1));ax.set_aspect('equal')
for s in ax.spines.values():s.set_visible(False)
ax.set_title('相关矩阵与关联网络（合成示例）',pad=20)
fig.subplots_adjust(left=.04,right=.96,top=.9,bottom=.06)
plt.show()
```

## 27. 径向环形热图

用途：分层环形单元、白边、缺口行标签、外圈列标签与色标。

数据要求：有行列标签的二维数值矩阵。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：显式align=edge统一环形单元角度边界与缺口；设置半径下界0保留中心空白。

```python
"""径向环形热图
Restored/adapted from supplied screenshots [99, 100, 101, 102].
Source: 小明的代码美学 (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
np.random.seed(6)
data=np.array([np.random.uniform(5*i,5*(i+1),48) for i in range(12)])
data+=np.random.normal(0,15,data.shape)
colors=palette_stops('diverging',count=5)
cmap=LinearSegmentedColormap.from_list('custom',colors,N=256)
num_columns=data.shape[1];gap_angle=10
width=2*np.pi/num_columns*(360-gap_angle)/360
theta=np.arange(num_columns)*width
vmin,vmax=data.min(),data.max()
fig,ax=plt.subplots(figsize=(8,6),dpi=150,subplot_kw={'polar':True})
for i,row in enumerate(data):
    height=2;radius=height*i+10
    for j,value in enumerate(row):
        ax.bar(theta[j],height,bottom=radius,width=width,color=cmap((value-vmin)/(vmax-vmin)),edgecolor='white',linewidth=.5,align='edge')
    ax.text(theta[-1]+width+np.radians(gap_angle/2),radius+height/2,str(i+1),ha='center',va='center',fontsize=6,rotation=-10)
for angle,label in zip(theta+width/2,range(1,num_columns+1)):
    rotation=np.degrees(angle);flip=90<rotation<270
    ax.text(angle,radius+3,str(label),ha='right' if flip else 'left',va='center',rotation=rotation-180 if flip else rotation,rotation_mode='anchor',fontsize=8)
ax.set(xticks=[],yticks=[],ylim=(0,radius+5));ax.spines['polar'].set_visible(False);ax.grid(False)
cb=fig.colorbar(ScalarMappable(norm=Normalize(vmin,vmax),cmap=cmap),ax=ax,orientation='vertical',pad=.15,fraction=.05)
cb.ax.tick_params(labelsize=8)
ax.text(0,0,'径向热图',ha='center',va='center',fontsize=12,fontweight='bold',color='#c0627a')
plt.tight_layout();plt.show()
```

## 28. 六边形空间热图

用途：六边形网格、白色细边、发散色阶和共享色标。

数据要求：x、y 和测量值 z；按六边形内均值聚合。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""六边形空间热图
Restored/adapted from supplied screenshots [104, 105].
Source: 小明的代码美学 (as shown in supplied screenshots).
This is a runnable restoration, not a byte-for-byte original source file.
See SOURCE.md for missing inputs and documented corrections.
"""
import numpy as np; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib.cm import ScalarMappable
from pathlib import Path
# Missing .mplstyle files are replaced only by explicit, portable display defaults.
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
 'axes.unicode_minus':False,'figure.facecolor':'white','axes.facecolor':'white',
 'axes.spines.top':False,'axes.spines.right':False,'font.size':9})
def create_gaussian_points(center,amplitude,sigma_x,sigma_y,num_points):
    x=np.random.normal(center[0],sigma_x,num_points)
    y=np.random.normal(center[1],sigma_y,num_points)
    z=amplitude*np.exp(-((x-center[0])**2/(2*sigma_x**2)+(y-center[1])**2/(2*sigma_y**2)))
    return x,y,z
np.random.seed(2);num_points=5000
x1,y1,z1=create_gaussian_points((10,7),-50,28,25,num_points)
x2,y2,z2=create_gaussian_points((25,12),50,27,26,num_points)
x=np.concatenate([x1,x2]);y=np.concatenate([y1,y2])
z=np.concatenate([z1,z2])+np.random.uniform(-25,25,2*num_points)
cmap=LinearSegmentedColormap.from_list('custom',palette_stops('diverging',count=5),N=256)
fig,ax=plt.subplots(figsize=(10,6),dpi=150)
hb=ax.hexbin(x,y,C=z,gridsize=50,cmap=cmap,reduce_C_function=np.mean,edgecolors='white',linewidths=.5)
cb=fig.colorbar(hb,ax=ax,orientation='vertical',pad=.01,fraction=.05)
cb.set_label('格内测量值均值')
ax.set(title='六边形空间热图',xlim=(-60,90),ylim=(-40,50),xlabel='X 轴',ylabel='Y 轴')
plt.tight_layout();plt.show()
```

## 29. 分类散点与决策区域

用途：半透明散点、淡色决策背景、横纵 rug 边际标记。

数据要求：两个数值特征和类别标签；背景为拟合模型预测。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""分类散点与决策区域
Restored/adapted from supplied screenshots [107, 108, 109].
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
from sklearn.svm import SVC
from matplotlib.colors import ListedColormap
import matplotlib.ticker as ticker
n=80;np.random.seed(7)
X1=np.random.normal(30,8,n);Y1=np.random.normal(60,18,n)
X2=np.random.normal(70,13,n);Y2=np.random.normal(90,20,n)
X3=np.random.normal(55,15,n);Y3=np.random.normal(50,15,n)
X=np.concatenate([np.column_stack((a,b)) for a,b in [(X1,Y1),(X2,Y2),(X3,Y3)]])
y=np.array([0]*n+[1]*n+[2]*n)
model=SVC(kernel='linear',decision_function_shape='ovo').fit(X,y)
x_max=X[:,0].max()+5;y_max=X[:,1].max()+10
xx,yy=np.meshgrid(np.arange(-5,x_max,.5),np.arange(-10,y_max,.5))
Z=model.predict(np.c_[xx.ravel(),yy.ravel()]).reshape(xx.shape)
colors=['#e97a7a','#5595d1','#e5c679']
fig,ax=plt.subplots(figsize=(9,5.5),dpi=150)
ax.contourf(xx,yy,Z,levels=[-.5,.5,1.5,2.5],alpha=.2,cmap=ListedColormap(colors))
for i,(a,b,c) in enumerate(zip([X1,X2,X3],[Y1,Y2,Y3],colors)):
    ax.scatter(a,b,s=100,c=c,alpha=.5,label=f'类别{i+1}')
    ax.scatter(a,np.zeros(len(a)),marker='|',color=c,alpha=.5,s=300)
    ax.scatter(np.zeros(len(a)),b,marker='_',color=c,alpha=.5,s=300)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10));ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20));ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
ax.set(title='分类散点与拟合决策区域',xlabel='X 轴',ylabel='Y 轴')
ax.legend(loc='upper center',ncols=3,frameon=False)
plt.tight_layout();plt.show()
```

## 30. 带背景圆环的极坐标散点

用途：三组透明散点、交替浅色背景圆环、角度轴和图例。

数据要求：角度（弧度）和非负半径，以及分组。

来源：小明的代码美学；代码截图恢复与适配。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：恢复全部可见绘图层与示例数据；调整导入、缩进、标签或输出边距以兼容当前运行环境。

```python
"""带背景圆环的极坐标散点
Restored/adapted from supplied screenshots [111, 112].
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
np.random.seed(7);n=50
r1=np.random.uniform(30,80,n);theta1=np.random.uniform(0,.75*np.pi,n)
r2=np.random.uniform(40,70,2*n);theta2=np.random.uniform(.5*np.pi,1.5*np.pi,2*n)
r3=np.random.uniform(20,60,n);theta3=np.random.uniform(1.25*np.pi,2*np.pi,n)
colors=['#e97a7a','#5595d1','#e5c679']
fig,ax=plt.subplots(figsize=(8,5),dpi=150,subplot_kw={'projection':'polar'})
for i,(theta,r,color) in enumerate(zip([theta1,theta2,theta3],[r1,r2,r3],colors)):
    ax.scatter(theta,r,s=100,c=color,alpha=.5,label=f'类别{i+1}',zorder=10)
theta=np.linspace(0,2*np.pi,100)
for i in range(4):
    ax.fill_between(theta,20*i+10,20*i+20,color=colors[0],alpha=.15,zorder=1)
ax.set_title('极坐标分组散点图')
ax.legend(loc='center right',bbox_to_anchor=(1.4,.5),frameon=False)
ax.spines['polar'].set_visible(False)
plt.tight_layout();plt.show()
```

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

## 32. 平滑极坐标面积叠加

用途：闭合平滑曲线、半透明重叠、深轮廓、空心基座和外置图例。

数据要求：angle（度）和多个 value 列；角度严格递增且不重复360°。

来源：小明的代码美学；代码截图恢复，原数据缺失。截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

适配记录：原data.csv缺失，补充angle及三个value列的周期合成示例。；增加角度顺序及端点检查，周期样条在0/360处同时闭合值和斜率。；原中心Circle仅创建且使用私有变换；改为实际绘制的白色中心覆盖，保留空心基座。

```python
"""平滑极坐标面积叠加
Restored/adapted from supplied screenshots [118, 119, 120].
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
from scipy.interpolate import make_interp_spline
BASE_RADIUS=50;SMOOTHING_POINTS=300
COLORS=['#529a9f','#d36a87','#ee8d5e']
read_custom_data=False
if read_custom_data:
    df=pd.read_csv('data.csv')
else:
    # Synthetic cyclic series: the original data.csv is not supplied.
    angles=np.arange(0,360,30);theta=np.deg2rad(angles)
    df=pd.DataFrame({'angle':angles})
    for i in range(3):
        df[f'value_{i+1}']=14+8*np.sin(theta*2+i*.9)+4*np.cos(theta*3-i*.7)
series_cols=[col for col in df.columns if 'value' in col]
original_angles=df['angle'].values
if len(original_angles)<4 or np.any(np.diff(original_angles)<=0) or original_angles[0]!=0 or original_angles[-1]>=360:
    raise ValueError('Angles must start at zero, strictly increase, and exclude 360 degrees')
original_theta=np.deg2rad(original_angles)
fig,ax=plt.subplots(figsize=(8,6),dpi=150,subplot_kw={'projection':'polar'})
ax.grid(color='gray',linestyle=':',linewidth=.8,alpha=.5)
ax.spines['polar'].set_visible(False)
LIMIT_RADIUS=BASE_RADIUS+df[series_cols].max().max()*2
for idx,col in enumerate(series_cols):
    values=df[col].values
    theta_closed=np.concatenate([original_theta,[original_theta[0]+2*np.pi]])
    values_closed=np.concatenate([values,[values[0]]])
    # Periodic boundary also matches slope at 0/360 (original only duplicated endpoint).
    spl=make_interp_spline(theta_closed,values_closed,k=3,bc_type='periodic')
    theta_smooth=np.linspace(0,2*np.pi,SMOOTHING_POINTS)
    values_smooth=np.maximum(spl(theta_smooth),0)
    r_values=values_smooth+BASE_RADIUS;color=COLORS[idx%len(COLORS)]
    ax.fill_between(theta_smooth,BASE_RADIUS,r_values,color=color,alpha=.3,label=f'数据系列{idx+1}')
    ax.plot(theta_smooth,r_values,color=color,linewidth=2,alpha=.9)
ax.set_ylim(0,LIMIT_RADIUS)
ax.set_yticks(np.linspace(BASE_RADIUS,LIMIT_RADIUS,4)[1:]);ax.set_yticklabels([])
labels_deg=np.arange(0,360,45)
ax.set_xticks(np.deg2rad(labels_deg),[f'{d}°' for d in labels_deg],fontsize=9,color='#555555')
ax.tick_params(axis='x',pad=12)
# Cover the center using public polar coordinates rather than unused private-transform Circle.
ax.fill_between(np.linspace(0,2*np.pi,300),0,BASE_RADIUS,color='white',zorder=10)
ax.legend(loc='upper center',bbox_to_anchor=(.5,-.1),frameon=False,fontsize=10,ncol=3)
plt.tight_layout();plt.show()
```
