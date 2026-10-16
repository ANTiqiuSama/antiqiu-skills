# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 057

```text
QO :
ae é
HAC: MET AREREE py @®
import matplotlib.pyplot as plt
import numpy as np
def load_style():
try:
plt.style.use("pie.mplstyle")
except:
pass
#RBPRSh, WER RRPK
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
def create_chart(ax):
a4 RUB
labels = ("AEM 1", "REM 2s, eM Wa", eM Mar, AM se,
"3 6", 3 7, "3 38", Or) 9",]
values = [30, 35, 40, 45, 50, 55, 60, 65, 70]
#TSetaeon AB ee (0° Sl 180°)
values = np.array(values)
width = 2 * np.pi * values / sum(values)
color = ["#dc9eb5", "#e3ded7", "#bGa3ce"]
color += color
color += color
start_x = 0
for i in range(values.shape[0]):
start_x += 0.5 * width[i]
ax.bar(
start_x, values[i], width=width[i],
bottom=10.06,
Linewidth=2, edgecolor="#ffffff",
color=color[i],
)
label = f"{labels[i]}\n{width[i]/np.pix100: .1f}% |
{values[i]}"
r_offset = (5.0, -5.0, 0.0, 0, 8, 0, 6, 0, 0] # Tia
Ree
text_attr = {"ha": "center", "va": "center",
“fontweight": "bold"}
1

```

## 截图 058

```text
ae
AG: MAT REE py @®
text = ax.text(
start_x, values[i] * 6.75 + 10 + r_offset[i],
label, color="#ffffff", fontsize=8, x*xtext_attr,
)
text. set_bbox (
dict(facecolor="#75879655", edgecolor="none",
boxstyle="round, pad=6@.5")
)
4 RE MS Si
start_x += 0.5 * width[i]
# PERSE, ARB
ax.set_yticklabels([]) # Raia 44
ax.set_xticklabels([]) # BRARRS
ax.set_rticks([]) # mt @4emRAE
ax.set_xticks([]}) # BR¥B@4HAE
a4 RM ha
text_attr = {"ha": "center", "va": "center",
“fontweight": "bold"}
fig.text(0.23, 0.5, "BT RRARB", fontsize=24,
x«text_attr)
ax.set_theta_direction(1) # R4ARAAERHSH
ax.set_theta_offset(np.pi * 6.5) # ARAM MBAS
plt.subplots_adjust(left=0.3, right=1.0, top=1,
bottom=-0.1)
if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(subplot_kw={"projection":
“polar"}, figsize=(8, 5), dpi=15e)
create_chart (ax)
plt.show()
2

```

