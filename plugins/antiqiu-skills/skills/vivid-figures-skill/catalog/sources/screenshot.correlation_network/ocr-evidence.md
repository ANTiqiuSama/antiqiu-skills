# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 092

```text
ae
HG: REALIA py @
"0" A Matplotlib RHAAKMAAR
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
from matplotlib.font_manager import FontProperties
def load_style():
“NRA AAN, RBPMFANBARRSR,
try:
plt.style.use("chartlab.mplstyle")
except:
pass
plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.edgecolor"] = "#ffffffoo”"
plt.rcParams["xtick.major.size"] = 0
plt.rcParams["ytick.major.size"] = 0
def gradient_color(min_value, max_value, hex_colors, value):
wa YE value f€[min_value, max_value] CHAM UB,
+B SMe
if max_value == min_value:
return
mcolors.to_hex (mcolors.hex2color (hex_colors[Len(hex_colors) //
27))
normalized_value = np.clip((value - min_value) /
(max_value - min_value), ®, 1)
color_idx = int(normalized_value * (len({hex_colors) -
1))
color_start, color_end = map(
mcolors.hex2color,
(hex_colors[color_idx], hex_colors[min(color_idx +
1, len(hex_colors) - 1)]),
)
1

```

## 截图 093

```text
ae
HG: REALIA py @
interpolated_color = [
(1 - (normalized_value % 1)) * s + (normalized_value
%1)*e
for s, e in zip(color_start, color_end)
]
return mcolors.to_hex(interpolated_color)
def calc_p_color(value):
wie ff fe p fxkB UMA Me. re
return "#e4c696" if value < 0.01 else "#69ala7" if value
< @.05 else "#c7c7Tc7"
def calc_r_width(value):
"CRG r PRA RARE
return 1.0 if value < 0.2 else 2.0 if value < 6.4 else
4.0
def create_chart(ax):
"ABH REMBMA, ROEM NHAE. MHRA EN
EEtS5XRAE.
feature_labels = "N P K Ca Mg S Al Fe Mn Zn Mo
pH".split()
feature_count, spec_labels = len(feature_labels),
["specl", “spec2", “spec3"]
4 FPR
np. random. seed (10)
pearson_data = np.random.uniform(-1, 1, (feature_count,
feature_count})
np. fill_diagonal(pearson_data, 1)
p_data = np.random.beta(®.8, 5, (len(spec_labels),
feature_count))
r_data = np.random.uniform(-1, 1, (len(spec_labels),
feature_count})
4 Sal -BENRRAM SE
2

```

## 截图 094

```text
QO :
ae é
HG: REALIA py @
spec_pos_y = np.linspace(@, feature_count,
len(spec_labels) + 2).tolist()
for i, spec in enumerate(spec_labels):
ax.text(
spec_pos_y[i + 1] - 4.5,
spec_pos_y[-2 - i] - 3.5,
spec,
va="center",
ha="center",
)
for j in range(feature_count):
ax. plot(
[spec_pos_y[i + 1] - 4, -0.5 + jl],
(spec_pos_y[-2 - i] - 3, feature_count - j -
9.5],
linestyle="-",
linewidth=calc_r_width(r_data[i, j]),
color=calc_p_color(p_datali, j]),
zorder=1 / p_data[i, jl,
marker="o",
markersize=4,
)
a 22 GAD EER
pearson_colors = ["#515a85", "#ecf4f8", “#c0627a"]
for i in range(feature_count):
for j in range(i, feature_count):
size = pearson_data[i, j] «1 # #BARAA
color = gradient_color(-1, 1, pearson_colors,
pearson_data[i, jl)
ax.add_patch(
patches. Rectangle(
{feature_count - i- 1, j),
1,
1,
Linewidth=0.25,
edgecolor="#999999",
facecolor="#ffffff",
)
3

```

## 截图 095

```text
QO :
ae é
MCG: HAS NSIARE py @
)
ax.add_patch(
patches. Rectangle(
{(feature_count - i - 6.5 - size / 2, j +
0.5 - size / 2),
size,
size,
linewidth=0.5,
edgecolor="#999999" ,
facecolor=color,
)
)
4 Sal ime
for i, label in enumerate(feature_Labels):
ax.text(@.5 + i, 0.5 + feature_count, label,
va="center", ha="center")
ax. text(
feature_count + 0.5,
feature_count ~ 0.5 - i,
label,
va="center",
ha="center",
)
font_prop = FontProperties(weight="bold")
# 424 Mantel's p Bl
mantel_p_handles = [
patches.Patch(color="#e4c696", Label="< 6.61"),
patches.Patch(color="#69ala7", Label="6.01 - 0.05"),
patches.Patch(color="lightgrey", lLabel=">= 6.05"),
]
mantel_p_legend = ax.legend(
handles=mantel_p_handles,
title="Mantel's p",
bbox_to_anchor=(®.875, 1.6),
handleheight=1.0,
handlelength=1.0,
)
mantel_p_lLegend. get_frame() .set_edgecolor ("#ffffff")
4

```

## 截图 096

```text
HARE: HACIA py @
mantel_p_legend.get_title().set_font_properties (font_prop)
ax, add_artist (mantel_p_legend)
# #4) Mantel's r BG
mantel_r_handles = [
mlines.Line2D([], [], color="#a9a9a9", Linewidth=1,
label="< 6.2"),
mlines.Line2D([], [], color="#a9a9a9", Linewidth=2,
label="0.2 - 9.4"),
mlines.Line2D([], [], color="#a9a9a9", Linewidth=4,
label=">= 6.4"),
]
mantel_r_legend = ax.legend(
handles=mantel_r_handles, title="Mantel's r",
bbox_to_anchor=(@.875, 0.7)
)
mantel_r_legend. get_frame() .set_edgecolor ("#ffffff")
mantel_r_legend.get_title().set_font_properties(font_prop)
ax.add_artist(mantel_r_legend)
4 SAMAR ER ARNAER
cmap, norm = mcolors.LinearSegmentedColormap. from_list(
*custom_cmap*, pearson_colors
), mcolors.Normalize(vmin=-1.0, vmax=1.@)
cbar = fig.colorbar(
plt.cm.ScalarMappable(norm=norm, cmap=cmap) ,
cax=fig.add_axes([@.775, 0.1, 0.03, @.2]),
)
cbar.ax.set_title("Pearson's r", fontdict={"fontsize":
10}, loc="center", pad=10)
4 2B ia tt
ax. set_xticklabels([])
ax.set_yticklabels([])
ax.xaxis.tick_top()
ax. yaxis.tick_right()
ax. axis ("equal")
5

```

## 截图 097

```text
UCB: HARAEANLBIA py @
ax.set_xlim(-2, feature_count + 8)
ax.set_ylim(-1, feature_count + 1)
ax. set_title(" #4 % tt i $4 RAB", pad=20)
plt.tight_Layout()

if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
create_chart (ax)
plt.show()
6

```

