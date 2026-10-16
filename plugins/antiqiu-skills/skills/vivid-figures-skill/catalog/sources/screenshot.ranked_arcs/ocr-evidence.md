# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 064

```text
ae
BV: C13-FVEEREE py @
import numpy as np
import matplotlib.pyplot as plt
from faker import Faker
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
## ER ERPXSAS
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
an BORE
bgcolor = "#ffffff"
plt.rcParams.update(
{
"Legend. facecolor": bgcolor,
"Legend.edgecolor": bgcolor,
"figure.facecolor": bgcolor,
"axes. facecolor": bgcolor,
“axes.edgecolor": bgcolor,
"text.color": "#575864",
}
)
def create_colors(hex_colors, data):
"OAR HE RIE CS A Re"
cmap =
plt.cm.colors.LinearSegmentedColormap. from_list ("custom_cmap",
hex_colors)
norm = Normalize(vmin=min(data), vmax=max (data) )
sm = ScalarMappable(cmap=cmap, norm=norm)
return [sm.to_rgba(val)(:3] for val in data]
#¢ ERRIURE: GASH SE KK
Faker .seed(6)
np. random. seed (6)
fake = Faker()
company_name = [fake.company() for _ in range(16)]
growth_data = np.sort(np.random.uniform(®, 100, 16))
1

```

## 截图 065

```text
QO :
a
ae é
MCB: 613-7 py [3/4]
4 BERS
fig, ax = plt.subplots(figsize=(8, 7),
subpLlot_kw={"projection": "polar"}, dpi=150)
max_value = max(growth_data) * 2.75 # RAH, AF MME
colors = create_colors(["#214e81", "#a55d75"], growth_data)
inner_radius = 15 # MSMuAR+E
for i, (label, value) in enumerate(zip(company_name,
growth_data)):
# EMS NRMtEBARE
inner_radius = 1.7 + inner_radius
ring_width = 1.5
#HUSASBE, RRERERBHNKE
theta_start = 0 # RAE
theta_end = (value / max_value) * 2 * np.pi # RAE
# RHR BREKE
ax. bar(
x=(theta_start + theta_end) / 2, # &R#@MRAB, BR
height=ring_width, # FREE
width=theta_end - theta_start, # RA MRHAIA
bottom=inner_radius, # A
color=colors[i],
alpha=0.85,
)
# RMS
if theta_end < np.pi / 2:
text_attr = {
"color": colors[il],
"rotation": np.degrees(theta_end) + 5,
"hat: "left",
3
else:
text_attr = {
"color": "#ftfffff",
"rotation": np.degrees(theta_end - np.pi) ~- 5,
"ha": "Left",
3
ax. text (
x=(theta_start + theta_end), # AEB
y=inner_radius + ring_width / 2, # ##@0 8 ia
2

```

## 截图 066

```text
QO :
e
MCB: 613-7 py @
s=f" {value:.1f}%", # MEAS
va="center"™,
fontsize=8,
fontwei ght="bold",
rotation_mode="anchor",
*xetext_attr,
)
4 Balas Mis
ax. text (
x=0- 0.01, # AB
y=inner_radius + ring_width / 2, # #@#@0 4 hig
s=company_name[i], # H2AR
ha="right”",
va="center",
color=colors[i],
fontsize=8,
fontweight="bold",
rotation=0,
rotation_mode="anchor",
)
at BRIE MTR: Binh, QE. ma
ax.set_xticks([])
ax.set_yticks(np.arange(len(growth_data)) + inner_radius,
01)
ax.grid(False) # XFIMS
ax.set_theta_direction(1) # #h## BG ot 4 fll
ax.set_theta_offset(np.pi * 1.5) # RAMAN MBAS
text_attr = {"ha": "left", "va": "top", "fontweight":
“bold"}
fig.text(@.1, 0.80, "Python REAR", fontsize=24,
extext_attr)
fig.text(@.1, 0.72, "Pik AER MIRA ML", fontsize=32,
x«text_attr)
#4 12 BBW
plt.subplots_adjust(left=-0.35, right=1.1, top=1.35,
bottom=-0.15)
plt.savefig("C13- 7% RB. png")
plt.show()
3

```

