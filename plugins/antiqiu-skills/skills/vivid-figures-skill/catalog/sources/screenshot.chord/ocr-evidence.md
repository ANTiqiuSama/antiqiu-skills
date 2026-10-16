# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 076

```text
WAC: HRM py @®
from pycirclize import Circos, sector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
try:
plt.style.use("robox.mplstyle")
except:
pass
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"] #
RAN
plt.rcParams["axes.unicode_minus"] = False # ERAS
def generate_random_matrix(size, min_value, max_value,
large_value_prob=0.1):
wie Ze oY — +S Be AL oe Be
matrix = np.zeros((size, size)) # @3a(i 3h
for i in range(size):
for j in range(size):
if its j: # EWRATR
+ RRM REEMA BR)
if np.random.rand({) < Large_value_prob:
matrixli][j] =
np.random.uniform(max_value * 6.95, max_value)
else:
matrix[i][j] =
np.random.uniform(min_value, max_value * 0.1)
return matrix.tolist()
# UB SAE fF oe Be RE
labels = [ "MEA a", "Be", "MAC, "SR", "BRE",
"SAF, "SAG, MAN, "BRI, ew I]
# CURA MB OR ST
color_map = ["#214e81", "#cO627a"] * 5
cmap = {}
link_cmap = {}
4

```

## 截图 077

```text
QO :
WAC: HRM py [3/3]

for i in range(len(labels)):

cmap[labels[i]] = color_map[i] + "77"
#iRBBRADAR EEE
size = 10 # HPA) (10 x 10)
min_value = 1 #4 ®/)\{
max_value = 500 # mRA‘A
# 4 5 Re WL 5B
np. random. seed (2)
interaction_data = generate_random_matrix(size, min_value,
max_value, @.2)
+ C12 BE
interaction_df = pd.DataFrame(interaction_data,
index=labels, columns=labels)
# MEM Circos
circos = Circos.initialize_from_matrix(

interaction_df,

space=3, # SKK Zs Milf

r_lim=(63, 70), # RRB W+@2w

cmap=cmap, # MARRAR

ticks_interval=500, # ZI1 Kialla

label_kws=dict(r=64, size=6, color="#ffffff",
fontweight="bold"), # ME BR

ticks_kws=dict(

Line_kws=dict (ec="#597cab") ,

text_kws=dict(weight="bold"), Label_size=6

)>

Link_kws=dict (alpha=0.4),
)
# REKARWA
for i, sector in enumerate(circos.sectors):

sector.tracks[0].axis(ec="#ffffff", lw=1.5)
fig = circos.plotfig(figsize=(8, 5), dpi=150)
fig.suptitle("MR MAR", x=0.22, y=0.57, fontsize=22)
fig.text(x=0.065, y=0.47, s="Chord Diagram of Gene
Expression", fontweight="bold")
plt.tight_layout()
plt.subplots_adjust(left=0.33, right=1, top=1, bottom=0)
plt.show()

2

```

