# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 107

```text
ae
BKB: HORA TORE py @
nous FA matplotlib #ml#RRERNHRAB
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from sklearn.svm import SVC
from matplotlib.colors import ListedColormap
def load_style():
try:
plt.style.use("chartlab.mplstyle")
except:
pass
plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.edgecolor"] = "#ffffff"
def create_chart(ax):
n = 80
np. random. seed(7)
X1 = np.random.normal(30, 8, n)
Y1 = np.random.normal(60, 18, n)
X2 = np.random.normal(70, 13, n)
Y2 = np.random.normal(90, 20, n)
X3 = np.random.normal(55, 15, n)
Y3 = np.random.normal(5@, 15, n)
# BHA
X = np.concatenate((np.column_stack((X1, Y1)),
np.column_stack((X2, ¥2)), np.column_stack((X3, Y3))))
y = np.array((6] * n + [1] * n + [2] * n)
# i —T svm Bae
model = SVC(kernel='linear',
decision_function_shape='ovo')
model. fit(x, y)
4 GUE Pe Lee il RR
x_min, x_max = X[:, 9].min() - 5, X[:, ©].max() +5
1

```

## 截图 108

```text
QO :

ae é
BKB: HORA TORE py [3/4]

y_min, y_max = X[:, 1].min() - 10, X[:, 1].max() + 10

XxX, yy = np.meshgrid(np.arange(-5, x_max, 0.5),
np.arange(-10, y_max, 0.5))

Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

Z = Z,.reshape(xx. shape)

#exXHe

colors = ["#e97a7a", "#5595d1", "#e5c679"]

cmap_background = ListedColormap(colors)

¢ Sa RRDA

ax.contourf(xx, yy, Z, alpha=@.2, cmap=cmap_background)

# $8 Bl AM Ra

ax.scatter(X1, Y1, s=100, c=colors[@], alpha=0.5,
label=" 36 @ 1")

ax.scatter(X1, [0] * len(X1), marker="|",
color=colors[@], alpha=0.5, s=300)}

ax.scatter((@] * len(X1), Y1, marker="_",
color=colors[0], alpha=0.5, s=300)

ax.scatter(X2, Y2, s=100, c=colors[1], alpha=0.5,
label=" 36 @ 2")

ax.scatter(X2, [0] * len(X2), marker="|",
color=colors[1], alpha=0.5, s=300)

ax.scatter([@] * len(X2), Y2, marker="_",
color=colors[1], alpha=0.5, s=300)

ax.scatter(X3, Y3, s=100, c=colors[2], alpha=0.5,
label=" 38 @ 3")

ax.scatter(X3, [0] * Len(X3), marker="|",
color=colors[2], alpha=0.5, s=300)

ax.scatter([@] * len(X3), Y3, marker="_",
color=colors[2], alpha=0.5, s=300)}

ax. xaxis.set_major_locator(ticker.MultipleLocator(5))

ax. xaxis.set_minor_Locator(ticker.MultipleLocator (1) )

ax. yaxis.set_major_locator (ticker.MultipleLocator (10) )

ax. yaxis.set_minor_locator(ticker.MultipleLocator(2))

ax. set_title ("4 33 82 TN Bim A")

2

```

## 截图 109

```text
BRB: HORE TORMEpy @
ax.set_xlabel ("Xx #4")
ax.set_ylabel("y #4")
ax. legend(loc="upper center", ncols=3)}
plt.tight_Layout()
if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
create_chart(ax)
plt.show()}
3

```

