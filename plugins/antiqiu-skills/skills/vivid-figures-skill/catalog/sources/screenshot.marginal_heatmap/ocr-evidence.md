# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 079

```text
QO :
SH: RADE py @

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
try:

plt.style.use("robox.mplstyle")
except:

print("i# robox.mplstyle M#RKEA—ARE")

pass
#RRPRSAURHEKET
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
#ikBBRAD
plt.rcParams["axes.edgecolor"] = "#ffffff"
plt.rcParams["axes.facecolor"] = "#ffffff"
plt.rcParams["xtick.major.size"] = 0
plt.rcParams["ytick.major.size"] = 0
plt.rcParams["xtick. labelsize"] = 6
plt.rcParams["ytick.labelsize"] = 6
plt.rcParams["text.color"] = "#3680ae"
plt.rcParams["xtick.color"] = "#3680ae99"
plt.rcParams["ytick.color"] = "#368Gae99"
def load_colormap():

colors = ["#368@ae","#82b8cb", "#ffFFFF", "#e98184",
"#e04c50"]

n_bins = 300 #4 RADAR

cmap_name = “custom_cmap"

return LinearSegmentedColormap. from_list(cmap_name,
colors, N=n_bins)
cmap = load_colormap{)
# EMAAR
years = np.arange(1985, 2021) # xX: i
months = [

1

```

## 截图 080

```text
SH: RADE py [3/6]

"Jan", "Feb", “Mar", "Apr", "May", "Jun",

"Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]
# FREMRBUOLRAABRH
np. random. seed (10)
data = np.random.uniform(-1, 1, (len(months), len(years)))
for i in range(len(months) ):

data[i] += np.linspace(-1.0, 2, len(years)) # PAE (38
$8 09 8 BR
data = data + np.random.uniform(-1.5, 1.5, data.shape) # i&
moa
bar_data_year = data.sum(axis=0) # #FGRA, $RABHRK
eke
bar_data_month = data.sum(axis=1) # RA@RA, kAMeH
KRERE
+ U2ARNAA
fig = plt.figure(figsize=(8, 5), dpi=150)
gs = GridSpec(

2, 2, width_ratios=[10, 1], height_ratios=[1, 2],
wspace=0.03, hspace=@.05
)
* ADE
ax_heatmap = fig.add_subplot(gs[1, 9])
heatmap = ax_heatmap. imshow(

data,

cmap=cmap ,

aspect="auto",

vmin=-np.max(np.abs(data)),

vmax=np.max(np.abs(data)),
)
# GRABLE TKE
for i in range(data.shape[0]): # MAT

for j in range(data.shape[1]): # 18/7

2

```

## 截图 081

```text
QO :
ae é
SH: RADE py @
if data[i, j] > © and data [i, j] < 1:
color="#e04c50"
elif data[i, j] < © and data [i, j] > -1:
color="#3680ae"
else:
color="#ffffff"
ax_heatmap.text(
j, # Whe
i, #¢ 7k
f"{datali, j]:.1f}", # BROXAAS
ha="center", # K#BA
va="center", # £ZAEP
fontsize=6, # FRA
color=color,
fontweight="bold",
)
4 Em RMA
for i in range(data.shape[6] + 1): # S##m&
ax_heatmap.plot(
[-0.5, data.shape[1] - 0.5],
[i - 6.5, i - 0.5],
color="white",
lLinewidth=1,
)
for j in range(data.shape[1] +1): # HAA
ax_heatmap. plot (
(j - 9.5, j - 0.5],
[-0.5, data.shape[9] - 0.5],
color="white",
Linewidth=1,
)
# REARS
ax_heatmap. set_xticks(np.arange(len(years)))
ax_heatmap.set_xticklabels(years, rotation=90,
fontweight="bold")
3

```

## 截图 082

```text
QO :
ae é
SH: RADE py @®
ax_heatmap.set_yticks (np.arange(len(months) ))
ax_heatmap.set_yticklabels(months, fontweight="bold")
# TR ABE tt eK
ax_top = fig.add_subplot(gs[®, @], sharex=ax_heatmap)
top_colors = ["#81b7d9" if v < © else "#e98184" for v in
bar_data_year]
ax_top.bar(np.arange(len(years)), bar_data_year,
color=top_colors)
ax_top.tick_params(axis="x", bottom=False,
labelbottom=False) # #& Rx WinS
ax_top.tick_params(axis="y", Left=False, labelleft=False) #
BER y thin S
ax_top.grid(False)
# GNAGHEKEA
ax_right = fig.add_subplot(gs[1, 1], sharey=ax_heatmap)
right_colors = ["#81b7d9" if v < © else "#e98184" for v in
bar_data_month]
ax_right.barh(np.arange(len(months)), bar_data_month,
color=right_colors)
ax_right.tick_params(axis="y", left=False, labelleft=False)
# BR y HiRS
ax_right.tick_params(axis="x", bottom=False,
labelbottom=False) # Rx Wir
ax_right.grid(False)
# 7D TW ER EK BR 0 RH i
for i, v in enumerate(bar_data_year):
ax_top. text(

7 ,

vt (@.2 if v > @ else -0.8), # MEME, ERmt
RE, ABA T HS

f"{vi.1f}",

ha="center",

va="bottom" if v > @ else "top", # H2BWHA

fontsize=6,

color="#e98184" if v > © else "#81b7d9",

4

```

## 截图 083

```text
ae
SH: RADE py @
fontwei ght="bold",
)
# AB MK AR RE
for i, v in enumerate(bar_data_month):
ax_right. text (

v-1l, # M88, EBERKARE, ABER KARA

i,

f"{vi.1f}",

ha="right" if v > @ else "left", # *MEWARAD

va="center",

fontsize=6,

color="white",

fontweight="bold",

)
fig.suptitle(
"HEA RIANA", x=0.05, y=0.93, ha="left", va="top",
fontsize=22, color="#3680ae"
)
fig.text(x=@.05, y=@.83, s="Heatmap of Annual Profits",
fontweight="bold", fontsize=12)
plt.subplots_adjust(left=0.05, bottom=@.12, right=1,
top=0.875)
plt.show()
5

```

