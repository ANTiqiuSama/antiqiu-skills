# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 060

```text
AS: RINE py @

import matplotlib.pyplot as plt
import numpy as np
def load_style():

# RAH RFE), HREP RS ARH

try:

plt.style.use("pie.mplstyle")
except:
pass

plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]

plt.rcParams["axes.unicode_minus"] = False
def create_chart(ax):

# RERENDRAM

color = ["#dc9eb5", "#b8b2b9", “#bOa3cO", “#e3ded7",
"Hebesfo"]

bgcolor = "#ffffff"

main_name = ("SUH A", “RGB, "RSE Ct]

sub_name = ["SRHB A-1", "SHB A-2", "HIE B-1", "HE
C-1", "BB C-2", "SHB c-3")

value_list = [[100.0, 120.0], [37.0], [29.0, 10.6, 20]]
# ERRRF RRR

size = 06.2 # RREASERE

# PERS, BRA

ax.set_ylim(0, 0.6)

ax.set_axis_off()

tT RaRBASTHRARH AL (HB)

sum_vals = sum(map(sum, value_list)) # #28 M

main_divided = [sum(sublist) / sum_vals * 2 * np.pi for
sublist in value_list] # DRAB

main_x = np.cumsum([@] + main_divided[:-1]) # #*+2
XORMAE

# $2 fl ER

main_colors = color[:len(value_list)]

1

```

## 截图 061

```text
QO :
ae é
AS: RINE py [3/4]
main_bars = ax.bar(
x=main_x, width=main_divided, bottom=size,
height=size,
color=main_colors, edgecolor=bgcolor, Linewidth=1,
align="edge"
)
REF RRRE, WASFDRHARD EB
sub_values = [val for sublist in value_list for val in
sublist]
sub_divided = [x / sum_vals * 2 * np.pi for x in
sub_values]
sub_x = np.cumsum([@] + sub_divided[:-1])
sub_colors = [main_colors[i] for i, sublist in
enumerate(value_list} for _ in sublist]
4 BaF DRAKA
sub_bars = ax.bar(
x=sub_x, width=sub_divided, bottom=2 * size,
height=size * 0.5,
color=sub_colors, alpha=@.5, edgecolor=bgcolor,
linewidth=2, align="edge"
)
#AEDRRMHSE
text_attr = {"ha": "center", "va": "center",
“fontweight": "bold"}
for bar, label, val in zip(main_bars, main_name,
map(sum, value_lList)):
angle = bar.get_x() + bar.get_width() / 2 # itBam
SBR (Pi tw)
distance = bar.get_height() + bar.get_y() # ita
SHE (RH MBB)
percentage = f"{label}\n{val / sum_vals * 100:.1f}%
| {val:.0f}" # ETMADIARBE
ax.text(angle, distance - 0.1, percentage,
color="#ffffff", fontsize=8, **xtext_attr) .set_bbox(
dict(facecolor="#75879655", edgecolor="none",
boxstyle="round, pad=0.5")
2

```

## 截图 062

```text
QO :
ae é
AS: RINE py @
)
# AF DRAMAS
for bar, label, val in zip(sub_bars, sub_name,
sub_values):
angle = bar.get_x() + bar.get_width() / 2
distance = bar.get_height() + bar.get_y()
percentage = f"{label}\n{val / sum_vals * 100:.1f}%
| {val:.of}"
ax.text(angle, distance + 0.1, percentage,
color="#ffffff", fontsize=8, **xtext_attr) .set_bbox(
dict(facecolor="#75879677", edgecolor="none",
boxstyle="round,pad=@.5")
)
# ROMA RTD
fig.text(0.15, 0.5, "RRA", fontsize=24,
*etext_attr)
plt.subplots_adjust(left=0.3, right=1.0, top=1.0,
bottom=0.05)
if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(subplot_kw={"projection":
"“polar"}, figsize=(8, 5), dpi=150)
create_chart(ax)
plt.show()
3

```

