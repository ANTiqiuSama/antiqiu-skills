# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 085

```text
ae
HG: MARA py @®
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
def load_style():
try:
plt.style.use("robox.mplstyle")
except:
pass
#Pepesa, MERE REHX
plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
# ERR
plt.rcParams["xtick.major.size"] = 5
plt.rcParams["xtick.minor.size"] = 2
def create_chart(ax):
# RE
X = np.arange(1860, 2020)
np. random. seed (3)
yl = np.random.uniform(20, 30, size=len(x)) + 10 *
np.sin(
np.linspace(@, 3 * np.pi, len(x))
)
y2 = np.random.uniform(50, 55, size=len(x)) + 5 *
np.cos(
np.linspace(@, 3 * np.pi, Len(x))
)
y3 = np.random.uniform(8®, 85, size=len(x)) + 7 *
np.sin(
np.linspace(®, 3 * np.pi, len(x))
)
cil = np.random.uniform(4, 5, size=len(x))
ci2 = np.random.uniform(4, 7, size=len(x))
ci3 = np.random.uniform(5, 9, size=len(x))
# 2 iS Bl Be Ki
line_colors = ["#8e93af", "#d7a6b3", "#eac890"]
ax.step(x, yl, label="3¢% A", Linewidth=1, where="mid",
1

```

## 截图 086

```text
QO :
HACE: MALTS py [3/3]
color="#3f5laf", zorder=3)
ax. fill_between(
x, yl - cil, yl + cil, label="EE 4% Ki@ a",
alpha=0.4, step="mid", color=lLine_colors[®], zorder=3
)
ax.step(x, y2, label="28@ B", Linewidth=1, where="mid",
color="#d7667e", zorder=3)
ax. fill_between(
x, y2 - ci2, y2 + ci2, label="F fe Kia] B",
alpha=0.4, step="mid", color=line_colors[1], zorder=3
)
ax.step(x, y3, label="2¢@¢", Linewidth=1, where="mid",
color="#eab159", zorder=3)
ax. fill_between(
x, y3 - ci3, y3 + ci3, label="H fF Kid c",
alpha=0.4, step="mid", color=line_colors[2], zorder=2
)
# RMNMALR
ax. text(1940, 5, "FAS", ha="center",
color="#3fSlaf", fontweight="bold")
ax.text(2000, 80, "FP Mi", ha="center",
color="#eab159", fontweight="bold")
ax. set_xlim(1860, 2020)
ax.set_ylim(@, 120)
# ROA
ax. legend{Loc="upper right", ncols=3)
# RM TR: Bl
ax.grid(axis="y", which="major", linestyle="-",
linewidth=1, color="#ffffff", zorder=1)
ax.xaxis.set_major_locator(ticker.MultipleLocator (16) )
ax.set_title(" Hf fm & ia] $f #M", x=0.015, y=0.95,
ha="left", va="top")
plt.tight_lLayout()
if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
create_chart(ax)
plt.show()}
2

```

