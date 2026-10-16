# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 049

```text
ae
C17-sa i SR-"WALOn HST IBS @
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def load_style():
we hy ey Re oe
#REBPRSR, VERE
plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
#BExXeat
plt.rcParams["grid.color"] = "#fed2d2"
plt.rcParams["figure.facecolor"] = "#ffffff"
plt.rcParams["axes.facecolor"] = "#f1f5f9"
plt.rcParams["axes.edgecolor"] = "#ffffff"
plt.rcParams["axes.labelcolor"] = "#515a85"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["text.color"] = %#515a85"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["xtick.color"] = "#515a85"
plt.rcParams["ytick.color"] = "#515a85"
plt.rcParams["legend.edgecolor"] = "#f1f5f9"
def load_data(file_path):
we dy ye ‘KA Ree
data = pd.read_csv(file_path)
return data
def create_stacked_area_chart(ax, data):
1

```

## 截图 050

```text
C17-sa i SR-"WALOn HST IBS [3/4]
wie Ql) 22 tt RRA Ae
# RB: pASRBSEFOERAH EH TK
age_groups = data.groupby(["Model", "Yas"])["Fiyat
($)"] .mean(). reset_index()
#RRMATAN MHS
models = age_groups["Model"] .unique()
# EMM BTR
colors = ["#214e81", "#6983a2", "#8d9eb2", "#b59fb1",
“#dc9fbe", "#c2768b"]
# TREN PA A SF ot ER
ages = age_groups["Yas"].unique()
# DBL -TSWRERES TD He RE
y_list = []
bottom = np.zeros(len(ages)) # MM#BR HEN O
# BASTARD, HRSTER RN TOS
for model in models:
model_data = age_groups[age_groups["Model"] == model]
y_values = (
model_data. set_index ("Yas") . reindex (ages) ["Fiyat
($)"]. fil1na(9). values
)
y_list.append( (model, y_values))
t+ RRSTRP ATA RHTHE, MEAN MER SB
y_list.sort(key=Lambda x: np.sum(x[1]), reverse=True)
2

```

## 截图 051

```text
QO :
C17-sa i SR-"WALOn HST IBS @
4 Sale SHRE
for i, (model, y_values) in enumerate(y_list):
ax. fill_between(
ages, bottom, bottom + y_values,
label=model, color=colors[i], alpha=0.6,
edgecolor="white", Linewidth=1,
)
bottom += y_values # BMHENRR US
ax.set_xlabel(" GALS we ()")
ax.set_ylabel(" 6 #LF 39 tH ($)")
ax.set_xlim(ages.min(), ages.max())
ax.set_ylim(@, 2e9)
# Ere ol
ax. legend(loc="upper right", bbox_to_anchor=(0.95, 60.95),
ncol=2)
plt.tight_layout()
if __name__ == "__main__":
load_style()
data = load_data("airplane_price_dataset.csv")
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
create_stacked_area_chart(ax, data)
plt.show(}
3

```

