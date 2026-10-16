# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 053

```text
ae
WCB: TWALRELpy @

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
style_file = "bar.mplstyle" # Hitxf#2 Mm
try:

plt.style.use(style_file)
except:

print(f" i SHARMA {style_filel RMEM—BRF")
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["legend.facecolor"] = "#ffffff"
plt.rcParams["legend.edgecolor"] = “#ffffff"
plt.rcParams["ytick.color"] = "#ffffff"
values = [11, 12, 12, 14, 15, 20, 22, 22, 24, 24, 26, 27] #
HWANG, RHSTAT RADA ESA
max_value = max(values)*1.1 #4 BRA, BFE
num_rings = len(values) # FR
categories = [f" LB{i}" for i in range(num_rings)] # 324i
&
* 2S
fig, ax = plt.subplots(figsize=(8, 5),
subpLlot_kw={"projection": "polar"}, dpi=150)
ax.set_theta_direction(-1) # Hatt
ax.set_theta_offset(np.pi / 2) # MIR®B 7AM
inner_radius_offset = 2
# RRS Hl
for i, (label, value) in enumerate(zip(categories, values)):

# STHHRETENEE

inner_radius = i + inner_radius_offset # #& SRM WA 2S
BY +E fe

ring_width = 0.8 # #7 HEE

#HvAAeth, RRBRERTHRARCA

1

```

## 截图 054

```text
QO :
¢ a
ae é
WCB: TWALRELpy [3/4]
theta_start = 0 # RAE
theta_end = (value / max_value) * 2 * np.pi # MiB (AOR
SAR
if np.degrees(theta_end) < 180:
rotation = -np.degrees((theta_start + theta_end) /
2)
else:
rotation = -186 - np.degrees((theta_start +
theta_end) / 2)
if value < 15:
color = "“#9dc1cs"
elif value > 25:
color = "#d7a6b3"
else:
color = "#8e93af"
# 2HMREREA
ax. bar (
x=(theta_start + theta_end) / 2, # &#¢MAB, BR
Ke
height=ring_width, # WARE
width=theta_end - theta_start, # KN MHSH
bottom=inner_radius, # At
color=color,
)
# RMMRS HEFL
ax. text(
x=(theta_start + theta_end) / 2, # AE
y=inner_radius + ring_width / 2, # #@EHA Pia)
s=f"{value}", # MEA
ha="center",
va="center",
color="white",
fontsize=6,
fontwei ght="bold",
rotation=rotation,
rotation_mode="anchor",
)
+ BG
2

```

## 截图 055

```text
WCB: TWALRELpy @
low_handle = mpatches.Patch(color="#9de1c5", Label="i {f fi")
normal_handle = mpatches.Patch(color="#8e93af", lLabel="iE #&
fi")
high_handle = mpatches.Patch(color="#d7a6b3", label="3t
fi")
handles = [low_handle, normal_handle, high_handle]
fig. legend(handles=handles, loc="center right",
handleheight=1, handlelength=1, ncols=1)

4 Diy id A
ax.set_xticks([])
ax. set_yticks(np.arange(num_rings) + inner_radius_offset,
categories)
ax.set_rlabel_position(@)
ax.tick_params(axis="y", Labelsize=6, color="#ffffff")
+ WAM
ax.grid(axis="y", Linestyle="-", Linewidth=1,
color="#ffffff")
fig.suptitle("HRH RE", x=0.015, y=0.975, ha="left",
va="top")
plt.tight_layout()
plt.show()

3

```

