"""Reproduce the supplied chart using NumPy and Matplotlib.
Values transcribed from image labels; error bars are illustrative, NOT measured.
Run: python reproduce.py. Outputs: PNG and vector PDF beside this script.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm, to_rgb
from matplotlib.colorbar import ColorbarBase
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parent
with (ROOT / 'data.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.reader(f))
samples = [r[0] for r in rows[1:]]
ss = rows[0][1:]
values = np.array([[float(v) for v in r[1:]] for r in rows[1:]])
assert values.shape == (6, 11) and np.isfinite(values).all() and (values > 0).all()

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
                     'font.weight': 'bold', 'axes.labelweight': 'bold', 'font.size': 12,
                     'pdf.fonttype': 42, 'axes.linewidth': 1.2})
colors = ['#202124', '#3b1425', '#702335', '#92083d', '#c70043',
          '#e63c59', '#f28b59', '#f8b282', '#ffe3cf', '#7bdc75', '#00a99f']
bounds = np.array([.21, .35, .58, .97, 1.6, 2.7, 4.5, 7.4, 12.4, 20.6, 34.3, 57.14])
cmap = ListedColormap(colors)
norm = BoundaryNorm(bounds, cmap.N, clip=True)
fig = plt.figure(figsize=(14.4, 12.8), facecolor='white')
ax = fig.add_axes([.015, .055, .81, .90], projection='3d', computed_zorder=False)
ax.view_init(elev=27, azim=-56)
ax.set_proj_type('ortho')
ax.set_box_aspect((6.6, 10.5, 8))

# Side faces fade from near-white at the foot to the bin color at the top.
faces, facecolors = [], []
w, d = .62, .62
for i in range(6):
    for j in range(11):
        h = values[i,j]
        base = np.array(to_rgb(colors[int(norm(h))]))
        x0, x1, y0, y1 = i-w/2, i+w/2, j-d/2, j+d/2
        n = 40 if h > 1.5 else 1
        levels = np.linspace(0, h, n+1)
        for k in range(n):
            z0, z1 = levels[k:k+2]
            t = (k+.5)/n
            c = base if h <= 1.5 else np.ones(3)*(1-t**.65)+base*t**.65
            for points, shade in [([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],.98),
                                  ([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],.88),
                                  ([(x1,y1,z0),(x0,y1,z0),(x0,y1,z1),(x1,y1,z1)],.92),
                                  ([(x0,y1,z0),(x0,y0,z0),(x0,y0,z1),(x0,y1,z1)],1.)]:
                faces.append(points)
                facecolors.append(np.clip(c*shade,0,1))
        faces.append([(x0,y0,h),(x1,y0,h),(x1,y1,h),(x0,y1,h)])
        facecolors.append(np.clip(base*1.04,0,1))
ax.add_collection3d(Poly3DCollection(faces, facecolors=facecolors, edgecolors='none',
                                    linewidths=0, antialiased=False, zsort='average', zorder=3))
# The reference does not provide uncertainty values. These marks approximate appearance only.
for i in range(6):
    for j in range(11):
        h = values[i,j]
        err = max(.10, .025*h)
        ax.plot([i,i], [j,j], [h-.35*err,h+err], c='black', lw=1.25, zorder=5)
        ax.plot([i-.10,i+.10], [j,j], [h+err,h+err], c='black', lw=1.25, zorder=5)
        ax.text(i, j, h+err+1.15, f'{h:.2f}', ha='center', va='bottom',
                fontsize=10, zorder=6, bbox=dict(facecolor='white', edgecolor='none', alpha=.87, pad=.15))
ax.set(xlim=(-.65,5.65), ylim=(-.65,10.65), zlim=(0,60))
ax.set_xticks(range(6), samples, rotation=-15)
ax.set_yticks(range(11), ss, rotation=18)
ax.set_zticks(np.arange(0,61,5))
ax.set_xlabel('Sample', labelpad=22, fontsize=19)
ax.set_ylabel('SS Content', labelpad=24, fontsize=19)
ax.set_zlabel('Compressive strength /MPa', labelpad=20, fontsize=18)
ax.zaxis._axinfo['juggled'] = (1,2,0)
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_pane_color((1,1,1,1))
    axis.pane.set_edgecolor('black')
    axis._axinfo['grid'].update(color=(.68,.68,.68,1), linestyle='--', linewidth=.8)
ax.tick_params(axis='both', labelsize=12, pad=3)
cax = fig.add_axes([.865,.205,.024,.63])
cb = ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds, spacing='uniform')
cb.ax.set_yticklabels(['0.21','0.35','0.58','0.97','1.6','2.7','4.5','7.4','12.4','20.6','34.3','57.1'])
cb.ax.tick_params(labelsize=14, pad=6)
cb.set_label('Compressive strength /MPa', fontsize=18, labelpad=17)
for suffix in ('png','pdf'):
    fig.savefig(ROOT / f'reproduced_chart.{suffix}', dpi=220, facecolor='white', bbox_inches='tight', pad_inches=.25)
print('Saved PNG and PDF to', ROOT)
