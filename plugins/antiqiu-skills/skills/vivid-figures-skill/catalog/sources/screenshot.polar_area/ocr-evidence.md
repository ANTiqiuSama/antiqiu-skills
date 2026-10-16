# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 118

```text
a bee!
4 £
3/6
—
er - 1
Polar Area Chart - Code
2H: Matplotlib 1D:02-005-01
1 import pandas as pd
2 import numpy as np
3 import matplotlib.pyplot as plt
4 from scipy.interpolate import make_interp_spline
5
6 # Hx
7 try:
8 plt.style.use("area.mplstyle")
9 except:
1@ pass
11
12 BASE_RADIUS = 5@ # PORK
13 SMOOTHING_POINTS = 300 # Fis} (B ma ok
14
15 # &#MB
16 COLORS = ["#529a9f", "#d36a87", "#ee8dSa")
17
18 # PRSMBAT
19 plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "Simei",
"Arial" ]
2@ plt.rcParams["axes.unicode_minus"] = False
21
22 # ik PRUE
23 df = pd.read_csv("data.csv")
24
25 series_cols = [col for col in df.columns if “value” in col]
26
27 # RR ‘angle' WHRRAME
28 original_angles = df["angle"].values
29 original_theta = np.deg2rad(original_angles)
38
31 # Hea
32 fig, ax = plt.subplots(figsize=(8, 6), dpi=150,
subplot_kw={"projection": "“polar"})

```

## 截图 119

```text
QO :
a 5
4 £

33 4/6
34 # BREE
35 ax.grid(color="gray", linestyle=":", linewidth=@.8, alpha=0.5)
36 ax.spines["polar"].set_visible(False)
37
38 max_data_value = df[series_cols].max().max()
39 LIMIT_RADIUS = BASE_RADIUS + max_data_value + 2.8
40
41 # MAH
42 for idx, col in enumerate(series_cols):
43 values = df[col). values
44 theta_closed = np.concatenate([original_theta,

{original_theta[@] + 2 * np.piJ])
45 values_closed = np.concatenate([values, [values[@]]])
46 # Feith a
47 spl = make_interp_spline(theta_closed, values_closed, k=3)
48 theta_smooth = np.linspace(@, 2 * np.pi, SMOOTHING_POINTS)
49 values_smooth = spl(theta_smooth)
50 values_smooth = np.maximum(values_smooth, @)
51 # BMBR+E
52 r_values = values_smooth + BASE_RADIUS
$3 color = COLORS[idx % Len(COLORS))
54 # 2 Hl
ss ax. fill_between(
56 theta_smooth,
S7 BASE_RADIUS,
58 r_values,
S9 color=color,
68 alpha=@.3,
61 label=f" 818 RA) {idx+1}",
62 )
63 ax.plot(theta_smooth, r_values, color=color, lLinewidth=2,

alpha=@.9)
64
65 # ik BYi
66 ax.set_ylim(@, LIMIT_RADIUS)
67 ax.set_yticks(np.linspace(BASE_RADIUS, LIMIT_RADIUS, 4)[1:])
68 ax.set_yticklabels([])
69 # ik BXhh
7@ labels_deg = np.arange(@, 360, 45)

```

## 截图 120

```text
QO :
¢ a
ae é
71 labels_rad = np.deg2rad(labels_deg) 5/6
72
73 ax.set_xticks(labels_rad)
74 ax.set_xticklabels([f"{d}°" for d in labels_deg], fontsize=9,
color="#555555")
75 ax.tick_params(axis="x", pad=12)
76
77 # 28h OB
78 center_circle = plt.Circle(
79 (®, @), BASE_RADIUS, transform=ax.transData._b,
color="white", zorder=18
8a )
81
82 # Bl
83 plt.legend(
84 loc="upper center", bbox_to_anchor=(@.5, -@.1),
frameon=False, fontsize=10, ncol=3
8s )
86
87 plt.tight_lLayout()
88 plt.show()
89

```

