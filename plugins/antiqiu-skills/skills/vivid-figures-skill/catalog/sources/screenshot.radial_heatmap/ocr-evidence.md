# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 099

```text
ae
MAB: SADE py @®
nous FA matplotlib ##l#@mAAA
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
def load_style():
try:
plt.style.use("chartlab.mplstyle")
except:
pass
#iBpesea, WERE KHX
plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
# eM et
plt.rcParams["axes.edgecolor"] = "#ffffff"
plt.rcParams["xtick.major.size"] = @
plt.rcParams["ytick.major.size"] = ®
def create_2d_gaussian(center, shape, amplitude, sigma_x,
sigma_y):
nr gl — SLi center AP OMB BMA A"
X = np.linspace(@, shape[1] - 1, shape[1])
y = np.linspace(®, shape[0] - 1, shape[0])
xX, y = np.meshgrid(x, y)
gauss = amplitude * np.exp(
-¢
({x - center[@]) ** 2) / (2 * sigma_x**2)
+ ((y - center[1]) ** 2) / (2 * sigma_y**2)
)
)
return gauss
def create_chart(ax):
4 eT WR
1

```

## 截图 100

```text
ae
BD: VANE py @®
np. random. seed (6)
# data = np.random.uniform(@, 100, (12, 48)) # BRALRGE
1
data = [] #4 RAMdE 2
for i in range(12):
data.append(np.random.uniform(5 * 1, 5 * (i + 1),
48))
data = np.array(data)
noise = np.random.normal(
loc=0, scale=15, size=data.shape
) + FRAO MEEAS HRA
4 4508 OR On Bl Bede
data = data + noise
#EXMEWNRHURAEKMERH
colors = ["#747b9d", "#87b4b9", "#ffTfFFFF", "#e9dlab",
"#cd8195"]
cmap = LinearSegmentedColormap. from_list("custom_cmap",
colors, N=256)
# BHA 485), HRSTREFHAR, SHIORTS
num_columns = data.shape[1]
gap_angle =- 10 # BHUMSAAE
theta = np. linspace(
®, 2 * np.pi * (360 - gap_angle) / 368, num_columns,
endpoint=False
)
tRAPRHASCaR )\GNRAE, AFRERH
vmin, vmax = data.min(}), data.max()
4 S@—-HBMRE, SMR BRRAK IZA
labels = ["1", "2", "3", "qt, n5H, Wen, v7 mgy ongy,
"ie", "21", 12")
4 RESTA (17)
for i, (row, label) in enumerate(zip(data, labels)):
2

```

## 截图 101

```text
QO :
ae é
BD: VANE py @
URS THE
height = 2
radius = height * i + 10
# BHP AT
for j, value in enumerate(row):
4 SRERN EAS
color = cmap((value - vmin) / (vmax - vmin))
ax.bar(
theta[jl],
height,
bottom=radius,
width=2 * np.pi / num_columns * (360 -
gap_angle) / 360,
color=color,
edgecolor="white",
linewidth=0.5,
)
* PME RE
ax.text(
theta[-1] + np.radians(gap_angle / 2),
radius,
label,
ha="left",
va="center",
fontsize=6,
rotation=-10,
transform=ax.transData,
)
# RBA ett
ax.set_yticklabels([]) #4 RHE ERE
ax,set_xticks(theta) # REABRREUE
ax.set_xticklabels([]) # MEM 1 348
# REBMHINAR TS
angle_labels = range(1, num_columns + 1)
for angle, label in zip(theta, angle_labels):
rotation = np.degrees(angle) # BIBRAKE
3

```

## 截图 102

```text
QO :
HUG: MALL py @®
ha = “right" if rotation > 90 and rotation < 270
else "left"
rotation = rotation - 180 if rotation > 96 and
rotation < 270 else rotation
ax. text(
angle,
radius + 3,
f"{label}",
hatha,
va="center",
rotation=rotation,
rotation_mode="anchor",
fontsize=8,
)
ax.spines["polar"].set_visible(False) # BRB ACiOtE
ax.grid(False) # RMR
# RMR
sm = plt.cm,ScalarMappable(cmap=cmap,
norm=plt.Normalize(vmin=vmin, vmax=vmax) )
sm.set_array([])
char = fig.colorbar(sm, ax=ax, orientation="vertical",
pad=0.2, fraction=0.1)
cbar.ax.tick_params(labelsize=8)
ax, text(
0, 0, "MIAZ HB", ha="center", va="center",
fontsize=10, fontweight="bold"
)
plt.tight_layout()
if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(figsize=(8, 5), dpi=150,
subpLot_kw=dict(polar=True))
create_chart(ax)
plt.show()
4

```

