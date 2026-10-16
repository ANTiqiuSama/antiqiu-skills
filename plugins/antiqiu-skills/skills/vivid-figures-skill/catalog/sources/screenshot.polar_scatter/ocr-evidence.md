# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 111

```text
ae
BRB: RHR. py @®

nous FA matplotlib RHRMARDARAB
import matplotlib.pyplot as plt
import numpy as np
def load_style():

try:

plt.style.use("chartlab.mplstyle")
except:
pass

plt.rcParams["font.sans-serif"] = ("Microsoft YaHei"]

plt.rcParams["axes.unicode_minus"] = False

plt.rcParams["axes.edgecolor"] = "#ffffff"
def create_polar_chart (ax):

# mE

n = 50

np. random. seed(7)

rl = np.random.uniform(30, 8@, n)

thetal = np.random.uniform(O, 8.75 * np.pi, n)

r2 = np.random.uniform(40, 70, 2 * n)

theta2 = np.random.uniform(0.5 * np.pi, 1.5 * np.pi, 2 *
n)

r3 = np.random.uniform(20, 60, n)

theta3 = np.random.uniform(1.25 * np.pi, 2 * np.pi, n)

colors = ["#e97a7a", "#5595d1", "#e5c679"]

# SBR S tr

ax.scatter(thetal, rl, s=100, c=colors[®], alpha=0.5,
label="26 #1", zorder=10)

ax. scatter (theta2, r2, s=100, c=colors[1], alpha=0.5,
label="26 ®@ 2", zorder=10)

ax. scatter (theta3, r3, s=100, c=colors[2], alpha=0.5,
label="26 # 3", zorder=10)

# RMAKER BE

1

```

## 截图 112

```text
BAB: RHR ARAL.py @®
theta = np.linspace(®, 2 * np.pi, 100)
for i in range(4):
ax.fill_between(theta, 20*i+10, 20*i + 20,

color=colors[0], alpha=0.15, zorder=1)

ax.set_title ("4 & #7 5) 48 BOA")

ax. legend(loc="center right", bbox_to_anchor=(1.4, 0.5))
if __name__ == "__main__":

load_style()

fig, ax = plt.subplots(figsize=(8, 5), dpi=150,
subplot_kw={"projection": "polar"})

create_polar_chart(ax)

plt.show(}

2

```

