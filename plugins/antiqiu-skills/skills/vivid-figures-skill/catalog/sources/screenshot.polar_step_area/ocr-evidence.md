# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 113

```text
QO :
e
caazg @
Python Sal Bin eA e
BR Het RX SR
» .
ay oo
8: " ce ee, ie
\¥ e/ a
UN ~. . | _ &
oz
TRAE
import numpy as np
import matpLlotlib.pyplot as plt
import matplotlib.patheffects as path_effects
#8 BMS
bgcolor = "#ebfefs"
1

```

## 截图 114

```text
QO :

edgecolor = “#didid1" 2/3)
plt.rcParams["figure.facecolor"] = bgcolor
plt.rcParams["axes.facecolor"] = "#ebfefs"
plt.rcParams["axes.edgecolor"] = edgecolor
plt.rcParams["font.sans-sertf"] = ["Microsoft YaHei"] #¢ BRAM
plt.rcParams("axes.unicode_minus"] = False # BRAS
plt.rcParams["text.color"] = "#597?cab" #¢ BAS
fig = plt.figure(figsize=(6, 6))
ax = plt.subplot(1, 1, 1, projection="polar", frameon=True)
ax.set_rlim(@, 1006)
ax. set_xticks([])
ax. set_yticks([])
# BHARWE
radius = ax.get_rmax(}
length = @.@2 * radius
for i in range(®, 360, 30):

angle = np.pi * i / 180

ax.plot([angle, angle], [radius, 1¢0],

Linewidth=@.5, color="#e5c5c5")
ax.text(angle, radius + 4 * length, "*d" % i, rotation=i - 98,
rotation_mode="anchor", va="top", ha="center"™)

a BEADS
def polar_to_cartesian(theta, radius):

x = radius * np.cos(theta)

y = radius * np.sin(theta)

return np.array([x, y])
def cartesian_to_polar(x, y):

radius = np.sqrt(xss2 + yx*2)

theta = np.arctan2(y, x)

return np.array([theta, radius])

2

```

## 截图 115

```text
QO :
for i in range(166, 1060, 108):
Pe = 0, i
Pl = cartesian_to_polar(
*(polar_to_cartesian(*«P9) + [6, -1.6 * length]))
text = ax.text(
P1[e], P1[1], “%d" % i, zorder=see,
va="top", ha="center”, size="x-small")
text.set_path_effects([path_effects.Stroke(Linewidth=2,
foreground="white"), path_effects.Normal()])
ae RAE
n= 10¢6
T = np.linspace(6, 2 * np.pi, n)
for i in range(®, 1080, 200):
ax. fill_between(T, i, i+106, color="#597cab33", zorder=-56)
ax.scatter((@], [0], 26, facecolor="#ebfefs", edgecolor="#597cab",
zorder=1008)
# RRA
np. random. seed(1)
n= 106
T=2* np.pi / n+ np.tinspace(@, 2 * np.pi, n)
T(a::2] = T[@:-1:2]
R = np.random.uniform(508, 880, n)}
R[-1] = R[@]
R[2:-1:2) = R[2::2]
ax. fill(T, R, color="se6a6a5", zorder=156, alpha=@.3)
ax.plot(T, R, color="#e6a6a05", zorder=256, Linewidth=1)
plt.tight_layout()
Plt. show()
3

```

