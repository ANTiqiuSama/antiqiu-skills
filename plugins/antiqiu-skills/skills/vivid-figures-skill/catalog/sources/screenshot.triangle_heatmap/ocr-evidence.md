# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 023

```text
QO :
WER: LEHR EL py @®
"0" A Matplotlib al MHA A
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import pandas as pd
plt.rcParams.update(
{
"font.sans-serif": ["Microsoft YaHei"],
"axes.unicode_minus": False,
“axes.edgecolor": "#ffffff",
"axes. linewidth": 0.3,
“"xtick.major.size": 6,
"ytick.major.size": 0,
“"figure.figsize": (8, 5),
"figure.dpi": 150,
"xtick.color": "#c0627a",
"ytick.color": "#c0627a",
"axes.titleweight": "bold",
"text.color": "#c®627a",
"font.size": 8,
}
)
#4 EM
# PRRMAEMRER
read_custom_data = False
+ RRB
upper_path = "upper_data.csv"
lower_path = “lLower_data.csv"
# EXH AR
upper_color_list = ["#f48b7f", "#e4c696", "#eeeeee",
"#69ala7", "#5d7a94"]
lower_color_list = ["#515a85", "#eeeeee", "#cO627a"]
color_alpha = 0.75 # M@BAE
# 872 colormap
def create_colormap(color_list, num_colors=256) :
1

```

## 截图 024

```text
QO :
ae é
WER: LEHR EL py @®
return mcolors.LinearSegmentedColormap. from_list(
"custom_cmap", color_list, N=num_colors
)
# DSMERAE
def get_text_color(value, vmax, color_list):
norm_val = value / vmax
if norm_val >= -@.4 and norm_val <= 0:
return color_list[0]
elif norm_val >= © and norm_val <= 0.4:
return color_list[-1]
else:
return “#ffffff"
# RAR OBR
if read_custom_data:
#4 ik csv XA. ANRB RSMAS
upper_df = pd.read_csv(upper_path, index_col=@)
lower_df = pd.read_csv(lower_path, index_col=0)
¢ MRBPRRTSMERES
row_labels = List(upper_df. index)
col_labels = list (upper_df.columns)
num_rows, num_cols = len(row_labels), len(col_labels)
# fe Rk (a A
upper_data = upper_df.values.astype(int)
lower_data = lower_df.values.astype(int)
else:
# O12 MMR
np. random. seed (2)
row_labels = [f"#M{chr(65 + i1)}" for i in range(s8)]
col_labels = (f"#EBE{i}" for i in range(1, 19)]
num_rows, num_cols = len(row_labels), len(col_labels)
upper_data = np.random.randint(-100, 101,
size=(num_rows, num_cols))
lower_data = np.random.randint(-10e, 101,
size=(num_rows, num_cols))
pd.DataFrame(upper_data, index=row_labels,
columns=col_labels) . to_csv(upper_path)
pd.DataFrame(lower_data, index=row_labels,
2

```

## 截图 025

```text
QO :
ae é
WER: LEHR EL py @
columns=col_labels) . to_csv(lLower_path)
+ SARE
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(@, num_cols)
ax.set_ylim(®, num_rows)
norm = plt.Normalize(-100, 100)
upper_cmap = create_colormap(upper_color_lList)
lower_cmap = create_colormap(lower_color_List)
for i in range(num_rows):
for j in range(num_cols):
# REA
color_upper = upper_cmap(norm(upper_data[i, j])})
triangle_upper = [[j, i], [i +2, i], Tj, i+ 17]
ax.add_patch(
plt.Polygon(
triangle_upper, facecolor=color_upper,
edgecolor="#ffffff" ,
linewidth=0.5, alpha=color_alpha,
)
)
ax. text(
j+6.1, 7 + 0.4,
f"{upper_data[i, j]:d}",
fontsize=8, fontweight="bold",
color=get_text_color(upper_data[i, j], 100,
upper_color_list),
)
# GPA
color_lower = lower_cmap(norm(lower_data[i, j]})
triangle_lower = [[j + 1, i], (j +1, i+ 1], [j, i
+17]
ax.add_patch(
plt.Polygon(
triangle_lower, facecolor=color_lower,
edgecolor="#ffffff",
linewidth=0.5, alpha=color_alpha,
3

```

## 截图 026

```text
QO :
ae é
WER: LEHR EL py @®
)
)
ax. text(
j + 0.5, i + 0.8,
f"{lower_datali, j]:d}",
fontsize=8, fontweight="bold",
color=get_text_color(lower_data[i, j], 100,
lower_color_list),
)
a Dip
ax.set_xticks(np.arange(num_cols) + 0.5)
ax.set_yticks(np.arange(num_rows) + 0.5)
ax.set_xticklabels(col_labels, rotation=90,
fontwei ght="bold")
ax.set_yticklabels(row_Labels, fontweight="bold")
ax. invert_yaxis()
ax.set_aspect ("equal")
# FRMIAB RM colorbar (L= Mist)
cax2 = fig.add_axes([@.1, 9.9, 0.4, 0.03])
sm2 = cm.ScalarMappable(cmap=upper_cmap, norm=norm)
sm2.set_array([])
cbar2 = plt.colorbar(sm2, cax=cax2,
orientation="horizontal", alpha=color_alpha)
cbar2.ax.set_title("2 EA Hi", fontsize=10)
# GROOT SBR colorbar (F= Mis tr)
caxl = fig.add_axes([0.55, 6.9, 0.4, ©.03]) # [left,
bottom, width, height]
sml = cm.ScalarMappable(cmap=lower_cmap, norm=norm)
sml.set_array([])
cbarl = plt.colorbar(sml, cax=cax1,
orientation="horizontal", alpha=color_alpha)
cbarl.ax.set_title("4& FA tea", fontsize=10)
plt.tight_layout()
plt.show()
4

```

