"""Render reproducible, comparable palette posters for the GitHub gallery.

Custom poster composition inspired by the user's four-panel reference.
Scatter is an illustrative cluster plot; other panels adapt the archived
grouped_violin/stacked_bar/ridgeline recipes archived in sources/.
All posters share samples, KDEs, category order, coordinates and alpha values.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb, to_hex
from matplotlib.font_manager import fontManager
from matplotlib.patches import FancyBboxPatch
import numpy as np
from scipy.stats import gaussian_kde

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / 'original/resources/assets/shared-scripts'))
import plot_utils as pu
import vivid_config as vc

OPTIONS = [('coral-teal', '珊瑚青绿', 'CORAL & TEAL'),
           ('olive-apricot', '橄榄杏棕', 'OLIVE & APRICOT'),
           ('blue-pink', '蓝粉浅彩', 'BLUE & LILAC'),
           ('blue-sky', '蓝天绿地', 'BLUE SKY & GREEN LAND'),
           ('soft-forest', '柔绿森林', 'SOFT FOREST'),
           ('pastel-girl', '粉彩少女', 'PASTEL BLOSSOM'),
           ('ocean-breeze', '海洋清风', 'OCEAN BREEZE')]
INK = '#34404A'
MUTED = '#78818B'


def prepare_data():
    rng = np.random.default_rng(20260915)
    centers = np.array([[3.0, 3.8], [3.7, 10.7], [8.0, 2.8], [8.9, 7.7],
                        [13.7, 5.5], [14.0, 12.0], [19.4, 8.3]])
    scatter = []
    for i, center in enumerate(centers):
        angle = [-.5, .35, -.3, -.55, .45, -.5, .3][i]
        rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        points = rng.normal(size=(200, 2)) * [0.78, 1.30]
        scatter.append(points @ rotation.T + center)
    distribution = [np.r_[rng.normal(34+i*6, 4.8+i*.3, 160),
                           rng.normal(45+i*5, 2.8+i*.4, 80)] for i in range(7)]
    composition = rng.dirichlet([2.8, 2.4, 3.5, 2.6, 2.8, 2.2, 2.7], size=5).T*100
    np.testing.assert_allclose(composition.sum(axis=0), 100)
    data = dict(scatter=np.array(scatter), distributions=np.array(distribution), composition=composition)
    # Plain JSON is portable and inspectable without a binary viewer.
    payload=json.dumps({k:v.tolist() for k,v in data.items()},separators=(',',':'))
    (HERE/'demo-data.json').write_text(payload,encoding='utf-8')
    return data, hashlib.sha256(payload.encode()).hexdigest()


def extend_data(data):
    """Add an eighth group without changing the original seven sample groups."""
    rng=np.random.default_rng(20260916)
    points=rng.normal(size=(200,2))*[.8,.65]+[19.4,2.4]
    scores=np.r_[rng.normal(76,5.2,160),rng.normal(83,2.8,80)]
    composition=np.vstack([data['composition']*.88,np.full((1,5),12.)])
    extended=dict(scatter=np.concatenate([data['scatter'],points[None]],axis=0),
                  distributions=np.concatenate([data['distributions'],scores[None]],axis=0),
                  composition=composition)
    payload=json.dumps({k:v.tolist() for k,v in extended.items()},separators=(',',':'))
    (HERE/'demo-data-8.json').write_text(payload,encoding='utf-8')
    return extended,hashlib.sha256(payload.encode()).hexdigest()


def style_axis(ax):
    ax.spines[['top','right']].set_visible(False)
    for spine in ['left','bottom']:
        ax.spines[spine].set_color('#A6ADB4')
        ax.spines[spine].set_linewidth(.65)
    ax.tick_params(length=2.5, width=.65, colors=MUTED, labelsize=7)
    ax.set_axisbelow(True)
    ax.grid(False)


def panel_heading(fig, x, y, letter, title, subtitle):
    fig.text(x,y,letter,fontsize=9,fontweight='bold',color=MUTED)
    fig.text(x+.029,y,title,fontsize=11,fontweight='bold',color=INK)
    fig.text(x,y-.023,subtitle,fontsize=7.1,color=MUTED)


def readable_tones(color, lighten, enabled):
    """Local pale-palette adaptation; preserve hue and the template's alpha."""
    rgb=np.array(to_rgb(color))
    brightness=float(rgb @ np.array([.2126,.7152,.0722]))
    if enabled and brightness>.70:
        fill=to_hex(rgb*.96) if brightness>.88 else color
        edge=to_hex(rgb*min(1.,.62/brightness))
        return fill,edge
    return pu._lighten(color,lighten),color


def scatter_panel(ax, data, colors, readable=False):
    for i, points in enumerate(data):
        fill,edge=readable_tones(colors[i],0,readable)
        ax.scatter(points[:,0],points[:,1],s=9,color=fill,alpha=.83,
                   edgecolors=edge,linewidths=.3 if readable else 0,rasterized=False)
        center=points.mean(axis=0)
        ax.text(*center,chr(65+i),ha='center',va='center',fontsize=8.5,
                color=INK,fontweight='bold',bbox=dict(boxstyle='circle,pad=.28',
                facecolor='white',edgecolor='none',alpha=.88))
    ax.set(xlim=(-.3,23),ylim=(-1,16.5),xticks=[0,5,10,15,20],yticks=[0,5,10,15])
    ax.set_xlabel('Feature 1',fontsize=8,color=INK,labelpad=4)
    ax.set_ylabel('Feature 2',fontsize=8,color=INK,labelpad=4)


def violin_panel(ax, data, colors, readable=False):
    # Preserve the original independent light body / colored edge / median / IQR layers.
    for i,d in enumerate(data[:5]):
        color=colors[i]
        fill,edge=readable_tones(color,.4,readable)
        parts=ax.violinplot([d],positions=[i],widths=.76,
                            showmeans=False,showmedians=False,showextrema=False)
        for pc in parts['bodies']:
            pc.set_facecolor(fill)
            pc.set_edgecolor(edge)
            pc.set_linewidth(1.2)
            pc.set_alpha(.8)
        q1,med,q3=np.percentile(d,[25,50,75])
        ax.scatter(i,med,color=edge,s=23,zorder=5,edgecolors='white',linewidths=.8)
        ax.vlines(i,q1,q3,color=edge,linewidth=2.5,zorder=4)
    ax.set(xticks=range(5),xticklabels=list('ABCDE'),ylim=(15,83),yticks=[20,40,60,80])
    ax.set_xlabel('Group',fontsize=8,color=INK,labelpad=4)
    ax.set_ylabel('Score',fontsize=8,color=INK,labelpad=4)
    ax.grid(axis='y',color='#D7DCE1',alpha=.35,lw=.55,ls='--')


def ridge_panel(ax, data, colors, readable=False):
    # Current recipe: a single translucent pale fill, independent colored outline,
    # and back-to-front layering. No additional image or gradient covers the fill.
    n=len(data)
    x_grid=np.linspace(15,95,600)
    for i in range(n-1,-1,-1):
        kde=gaussian_kde(data[i],bw_method=.3)
        raw=kde(x_grid); peak=raw.max(); density=raw/peak*.94
        baseline=i*.61; color=colors[i]; z=n-i
        fill,edge=readable_tones(color,.5,readable)
        ax.fill_between(x_grid,baseline,baseline+density,
                        color=fill,alpha=.85,zorder=z)
        ax.plot(x_grid,baseline+density,color=edge,lw=1.2,zorder=z+.5)
        median=np.median(data[i]); med_height=float(kde(median)[0]/peak*.94)
        ax.plot([median,median],[baseline,baseline+med_height],color=edge,
                lw=.85,ls=(0,(2.5,2)),zorder=z+.8)
        ax.scatter([median],[baseline+med_height],s=11,color=edge,edgecolor='white',
                   lw=.5,zorder=n+2)
    ax.set_yticks(np.arange(n)*.61+.15,[chr(65+i) for i in range(n)])
    for tick,color in zip(ax.get_yticklabels(),colors):
        tick.set_color(readable_tones(color,0,readable)[1])
    ax.tick_params(axis='y',length=0,pad=5)
    ax.spines['left'].set_visible(False)
    ax.set(xlim=(15,95),ylim=(-.05,(n-1)*.61+1.12),xticks=[20,40,60,80])
    ax.set_xlabel('Score',fontsize=8,color=INK,labelpad=4)


def stacked_panel(ax, data, colors, readable=False):
    x=np.arange(data.shape[1]);bottom=np.zeros(len(x))
    # Palette demonstration uses 100% composition. A constant total line carries no
    # additional information here; retain the layer accumulation and fill/edge pairing.
    for i,vals in enumerate(data):
        fill,edge=readable_tones(colors[i],.12,readable)
        ax.bar(x,vals,.67,bottom=bottom,color=fill,
               edgecolor=edge,linewidth=.75,zorder=2)
        bottom+=vals
    ax.set(xticks=x,xticklabels=['S1','S2','S3','S4','S5'],ylim=(0,101),
           yticks=[0,25,50,75,100])
    ax.set_xlabel('Sample',fontsize=8,color=INK,labelpad=4)
    ax.set_ylabel('Composition (%)',fontsize=8,color=INK,labelpad=4)
    ax.grid(axis='y',color='#D7DCE1',alpha=.35,lw=.55,ls='--')


def render(output, selected=None):
    output.mkdir(parents=True,exist_ok=True)
    data7,hash7=prepare_data()
    data8,hash8=extend_data(data7)
    # Preserve complete current source examples alongside the adaptations.
    for path in (HERE/'sources').glob('*.md'):
        source=re.findall(r'```python\s*\n(.*?)```',path.read_text(encoding='utf-8'),re.S)[0]
        path.with_suffix('.py').write_text(source,encoding='utf-8')
    palettes=vc.registry()["palettes"]
    fonts={f.name for f in fontManager.ttflist}
    cjk=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','PingFang SC','SimHei'] if f in fonts),None)
    if not cjk: raise RuntimeError('Install a CJK font before rendering these Chinese posters.')
    original_cwd=Path.cwd()
    existing=output/'render-info.json'
    audit=json.loads(existing.read_text(encoding='utf-8')) if selected and existing.exists() else []
    with tempfile.TemporaryDirectory(prefix='vivid-palette-posters-') as tmp:
        try:
            os.chdir(tmp)
            for slug,name,english in OPTIONS:
                if selected and slug not in selected: continue
                base=list(palettes[slug]['colors'])
                assert len(base) in (5,7,8)
                data,data_hash=(data8,hash8) if len(base)==8 else (data7,hash7)
                n=len(data['scatter'])
                vc.write_config(tmp, palette=slug, style='clean_open')
                pu.setup_style()
                assert pu.PALETTE==base
                colors=list(pu.PALETTE)
                if len(colors)==5:
                    colors.extend([to_hex(pu._lighten(base[0],.42)),to_hex(pu._lighten(base[2],.42))])
                plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':[cjk,'DejaVu Sans'],
                    'font.size':8,'axes.labelsize':8,'axes.labelcolor':INK,'text.color':INK,
                    'savefig.bbox':None,'svg.fonttype':'path','pdf.fonttype':42})
                fig=plt.figure(figsize=(8,9.6))
                back=fig.add_axes([0,0,1,1],zorder=-10)
                back.imshow(np.linspace(0,1,256).reshape(-1,1),
                    cmap=LinearSegmentedColormap.from_list('background',[pu._lighten(base[2],.94),pu._lighten(base[0],.82)]),
                    origin='lower',extent=(0,1,0,1),aspect='auto')
                back.axis('off')
                fig.add_artist(FancyBboxPatch((.037,.064),.926,.721,boxstyle='round,pad=0.012,rounding_size=0.025',
                    facecolor='white',edgecolor='none',transform=fig.transFigure,zorder=-5))
                headline=to_hex(np.array(to_rgb(base[0]))*.67)
                fig.text(.063,.942,'VIVID FIGURES  /  COLOR STUDY',fontsize=9.5,fontweight='bold',color=headline)
                fig.text(.06,.882,'配色方案',fontsize=32,fontweight='bold',color=headline)
                fig.text(.395,.887,name,fontsize=22,fontweight='bold',color=headline)
                fig.text(.064,.849,english,fontsize=8.7,color=MUTED)
                fig.text(.934,.849,f'{len(base)} 个原色',fontsize=8.3,color=MUTED,ha='right')
                sw=.87/len(base)
                for i,color in enumerate(base):
                    xx=.063+i*sw
                    fig.add_artist(FancyBboxPatch((xx,.818),sw-.012,.014,boxstyle='round,pad=0,rounding_size=0.004',
                        facecolor=color,edgecolor='none',transform=fig.transFigure))
                    fig.text(xx,.802,color.upper(),fontsize=6.9,color=INK)
                axes=[fig.add_axes(rect) for rect in [[.10,.476,.342,.236],[.572,.476,.342,.236],
                                                    [.10,.141,.342,.236],[.572,.141,.342,.236]]]
                panel_heading(fig,.075,.752,'A','散点簇',f'点色与透明叠加 / {n} groups')
                panel_heading(fig,.548,.752,'B','小提琴分布','浅填充与原色轮廓 / 5 groups')
                panel_heading(fig,.075,.417,'C','层叠山脊',f'浅色透明填充与轮廓 / {n} groups')
                panel_heading(fig,.548,.417,'D','堆叠色块',f'相邻颜色与面积对比 / {n} components')
                for ax in axes: style_axis(ax)
                readable=slug in ('blue-sky','pastel-girl')
                scatter_panel(axes[0],data['scatter'],colors,readable)
                violin_panel(axes[1],data['distributions'],colors,readable)
                ridge_panel(axes[2],data['distributions'],colors,readable)
                stacked_panel(axes[3],data['composition'],colors,readable)
                # A consistent compact key makes repeated colors/tints explicit.
                for i,color in enumerate(colors):
                    xx=.135+i*(.77/n)
                    fig.add_artist(plt.Rectangle((xx,.089),.018,.008,transform=fig.transFigure,facecolor=color,edgecolor='none'))
                    fig.text(xx+.026,.088,chr(65+i),fontsize=7,color=MUTED)
                note='模拟数据 · 同组数配色共用数据与布局'
                if readable: note='模拟数据 · 浅色减少提亮，轮廓使用同色深色派生'
                if len(base)==5: note+=' · F/G 为 A/C 的浅色派生'
                fig.text(.06,.032,note,fontsize=6.8,color=INK)
                fig.text(.94,.032,'vivid-figures-skill',fontsize=7,color=MUTED,ha='right')
                for ext in ['png','svg','pdf']:
                    fig.savefig(output/f'{slug}.{ext}',dpi=300,facecolor='white')
                plt.close(fig)
                audit=[item for item in audit if item['slug']!=slug]
                audit.append(dict(slug=slug,name=name,base_colors=base,display_colors=colors,
                    data_sha256=data_hash,png_pixels=[2400,2880],dpi=300,
                    groups=n,data_file='demo-data-8.json' if n==8 else 'demo-data.json',
                    pale_color_readability_adjustment=readable,
                    scatter_samples_per_group=200,distribution_samples_per_group=240,
                    extra_tints=(['A lightened 42%','C lightened 42%'] if len(base)==5 else [])))
                print('Rendered',name)
        finally: os.chdir(original_cwd)
    (output/'render-info.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    cards=''.join(f'<section><h2>{name}</h2><a href="{slug}.png"><img src="{slug}.png" alt="{name}配色示意图"></a><p><a href="{slug}.png" download>高清 PNG</a> · <a href="{slug}.svg">矢量 SVG</a> · <a href="{slug}.pdf">PDF</a></p></section>' for slug,name,_ in OPTIONS)
    (output/'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vivid 七套配色预览</title><style>body{margin:0;padding:28px;background:#f2f4f7;font:15px/1.7 "Microsoft YaHei",sans-serif;color:#34404a}h1{font-size:26px}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}section{background:white;padding:16px;border-radius:14px}h2{font-size:18px}img{width:100%;display:block}a{color:#5879a0}header{margin-bottom:24px}p{font-size:13px;color:#78818b}@media(max-width:900px){main{grid-template-columns:1fr}}</style><header><h1>七套配色 · 色彩对照</h1><p>散点簇 / 小提琴 / 层叠山脊 / 堆叠色块。新增四套完整八色配色，共用八组模拟数据；原三套示意保留。点击图片查看高清原图。可下载高清图片与矢量文件。</p></header><main>'+cards+'</main></html>',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=REPO/'docs/images/palettes')
    parser.add_argument('--palettes',nargs='+',choices=[x[0] for x in OPTIONS])
    args=parser.parse_args()
    render(args.output.resolve(),args.palettes)
