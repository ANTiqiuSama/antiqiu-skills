# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 068

```text
ae
BRB: WS SMR py @
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.patches as mpatches
def load_style():
ware hy ay BE hee
try:
plt.style.use("robox.mplstyle")
except:
pass
4x a, UERERHX
plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.facecolor"] = "#ffffff"
plt.rcParams["xtick.major.size"] = @
plt.rcParams["ytick.major.size"] = 0
def create_data(x, size, n, max_value):
wore io i A be Be EK — 48 i den
sigma = size / 30 #4 BH ESE
values = max_value * np.exp(-@.5 * ((x - n) / sigma) «*
2)
return values
def create_ridgeline_plot (ax):
“UN eoE RRA
a4 1.4 PRE IB
np. random. seed (3)
size = 300
xX_max = 80
xX = np.linspace(@®, x_max, size)
y_list = []
for i in range(2@):
temp_y = 0
1

```

## 截图 069

```text
QO :
ae é
SRE: GTO MRE py [3/4]
peaks = np.sort(np.random.randint(®, 88, size=200))
means = np.random.uniform(-9.25, 0.3, 20@)
for j in range(len(peaks) ):
temp_y += create_data(x, x_max, peaks[j],
means[j])
y_list. append (temp_y)
#4 2.28 D RRA
y_offset = 0.6 # 8-BNBARBE
for i, y in enumerate(y_list):
y_spline = make_interp_spline(x, y) # @A#RBE
Fie ah
x_smooth = np.linspace(x.min(), x.max(), 5006)
y_smooth = y_spline(x_smooth)
4 £2 fill IE fa
y_pos = np.maximum(y_smooth, 6)
for j in range(4):
y_plot = np.minimum(y_pos, y_offset * (j + 1))
y_plot = op.maximum(y_plot, y_offset * j)
y_bottom = © + y_offset * 7
y_top = y_plot - j * y_offset + y_offset * i
ax. fill_between(x_smooth, y_bottom, y_top,
color="#e98184", alpha=0.5)
ax.plot(x_smooth, y_top, color="#ffffff",
Linewidth=0.5)
# REIN
y_pos = np.maximum(-y_smooth, 6)
for j in range(4):
y_plot = np.minimum(y_pos, y_offset * (j + 1))
y_plot = np.maximum(y_plot, y_offset * j)
y_bottom = © + y_offset * 7
y_top = y_plot - j * y_offset + y_offset * 7
ax. fill_between(x_smooth, y_bottom, y_top,
color="#81b7d9", alpha=0.5)
ax.plot(x_smooth, y_top, color="#ffffff",
Linewidth=0.5)
ax.set_xlim(6, 70) # 38H
2

```

## 截图 070

```text
QO :
BRB: WS SMR py @
ax.set_ylim(@, 13) # RIEBRAB YH
ax. set_xticks(
[1.5, 10, 20, 30, 40, 50, 60, 68.5],
[2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027],
fontweight="bold",
color="#81b7d9",
)
ax. set_yticks(
[o.3 + i * 0.6 for 7 in range(20)],
[chr(i) for i in range(65, 65 + 20)], # YHPFaRS
fontweight="bold",
color="#81b7d9",
)
pos_handle = mpatches.Patch(color="#e98184", label="iE
i")
neg_handle = mpatches.Patch(color="#81b7d9", label="ft fl
Si")
handles = [pos_handle, neg_handle]
legend = ax.legend(
handles=handles, loc="upper right", handleheight=1,
handlelength=3, ncols=3
)
legend. get_frame().set_edgecolor ("#ffffff") # Afi
ax.set_title(
"SRR REAR: FMB",
x=0.0,
y=0.97,
ha="left",
va="top",
fontsize=16,
color="#3680ae",
)
plt.tight_layout()
if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
create_ridgeline_plot (ax)
plt.show()
3

```

