# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 104

```text
ae
BC: AIRE py @®
nous FA matplotlib #AWHRAAA
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
def load_style():
try:
plt.style.use("chartlab.mplstyle")
except:
pass
plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.edgecolor"] = "#ffffff"
plt.rcParams["xtick.major.size"] = ©
plt.rcParams["ytick.major.size"] = @
def create_gaussian_points(center, amplitude, sigma_x,
sigma_y, num_points):
wun de BY — HE BT 9) 7p BD a oe SHE"
xX = np.random.normal(center[0], sigma_x, num_points)
y = np.random.normal(center[1], sigma_y, num_points)
Z = amplitude * np.exp(
-(
(x - center[@]) ** 2 / (2 * sigma_x**2)
+ (y - center[1]) ** 2 / (2 * sigma_y**2)
)
)
return x, y, Z
def create_hexbin_chart (ax):
+ ERAT SM AY me BE
np. random. seed (2)
num_points = 5600
xl, yl, zl = create_gaussian_points(
center=(10, 7), amplitude=-50, sigma_x=28,
sigma_y=25, num_points=num_points
)
x2, y2, z2 = create_gaussian_points(
1

```

## 截图 105

```text
QO :
ae é
BC: AIRE py @®
center=(25, 12), amplitude=50, sigma_x=27,
sigma_y=26, num_points=num_points
)
# SHAE
X = np.concatenate([x1, x2])
y = np.concatenate([y1, y2])
zZ = np.concatenate([zl, z2]) + np.random.uniform(
-25, 25, 2 * num_points
) # MARNE
#BEXReRH
colors = ["#747b9d", "#87b4b9", "#ffffff", "#e9dlab",
"#cd8195"]
cmap = LinearSegmentedColormap. from_list("custom_cmap",
colors, N=256)}
# (8A hexbin SH AWHAAA
hb = ax.hexbin(
x, y, C=z, gridsize=50, cmap=cmap,
reduce_C_function=np.mean,
edgecolors="white", Linewidths=@.5,
)
# RMRARK
cb = fig.colorbar(hb, ax=ax, orientation="vertical",
pad=0.01, fraction=0.05)
ax.set_title("AW# AM")
ax.set_xlim(-60, 90)
ax.set_ylim(-40, 50)
ax.set_xlabel ("Xx #4")
ax.set_ylabel("Y $4")
plt.tight_layout()
if __name_. == "__main__":
load_style()
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
create_hexbin_chart(ax)}
plt.show()
2

```

