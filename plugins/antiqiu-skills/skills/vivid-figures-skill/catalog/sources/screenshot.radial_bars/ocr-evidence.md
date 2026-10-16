# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 072

```text
ae
HCE: SPIER py @
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
style_file = "bar.mplstyle" # Hitxf#2 Mm
try:
plt.style.use(style_file)
except:
print(f" i SHRM A {style_file}l REAM—BRF")
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["legend.facecolor"] = "#ffffff"
plt.rcParams["legend.edgecolor"] = “#ffffff"
+ RRS
values = [20, 27, 16, 17, 16, 22, 24, 26, 30, 22, 18, 24,
17, 14, 23, 17, 20, 18, 14, 18, 21, 13, 14, 20 ]
count = len(values)
angles = np.linspace(®, 2 * np.pi, count, endpoint=False) #
STEFHAB
xticks = np.arange (count)
+ U#RARA
fig, ax = plt.subplots(figsize=(8, 5),
subplot_kw={"projection": "polar"}, dpi=150)
#RBRE
colors = []
for v in values:
ifv< 15:
colors.append("#9dc1c5") # KG
elif v > 25:
colors.append("#d7a6b3") # TEA
else:
colors.append("#8e93af") # EHE
4 SHBAEKEA
1

```

## 截图 073

```text
QO :
¢ a
ae é
MAB: SCERE.py [3/4]
bars = ax.bar{
angles,
values,
width=2 * np.pi / count,
bottom=10,
colorscolors,
edgecolor="#f1f5f9",
Linewidth=1,
zorder=2
)
# AR DD RE iE
for bar, angle, value in zip(bars, angles, values):
rotation = np.degrees(angle) # BURR RNAR
ha = "right" if rotation > 9@ and rotation < 270 else
"Left"
rotation = rotation - 180 if rotation > 90 and rotation
< 270 else rotation
ax. text (
angle,
value +7, # MFA: ABB
f"{int(value)}", # ERARFAR
ha=ha,
va="center",
fontsize=8,
fontweight="bold",
rotation=rotation,
rotation_mode="anchor",
color="#ffffff",
zorder=4,
)
# Bl
low_handle = mpatches.Patch(color="#9dc1c5", Label="id 4k ff")
normal_handle = mpatches.Patch(color="#8e93af", label="iE #%
fi")
high_handle = mpatches.Patch(color="#d7a6b3", label="3t Mi
fi")
handles = [low_handle, normal_handle, high_handle]
2

```

## 截图 074

```text
MARIS: HEM py @
fig. legend(handles=handles, loc="center right",
handleheight=1, handlelength=1, ncols=3)

# PERERA
ax,set_yticks([{]) # BR@AAMKR
ax.set_xticks(angles, xticks) # REABMHK
ax.tick_params(axis="x", labelsize=8, pad=-5)
fig.text(x=0.68, y=0.55, so"BAMHRKM", fontdict={"size":
32, “weight":"bold"})
ax.grid(axis="x", Linestyle="--", Linewidth=6.5,
color="#8e93af", alpha=.5, zorder=1)
plt.tight_lLayout()
plt.subplots_adjust(left=0, right=0.66, top=0.95,
bottom=6.05)
plt.show()

3

```

