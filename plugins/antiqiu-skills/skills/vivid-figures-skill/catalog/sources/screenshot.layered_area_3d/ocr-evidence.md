# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 007

```text
im) 49
—
— -
a" .y
3D Layered Area Chart - Code
SE: Matplotlib 1D:02-006-01
1 import csv
2 import numpy as np
3 import matplotlib.pyplot as plt
4 from matplotlib.collections import PolyCollection
S from scipy.interpolate import make_interp_spline
6
7 def polygon_under_graph(x, y):
8 “on Bll 2 62 Hy Sk HE RK te wy Sie Te
9 return ((x(@], @.0), *zip(x, y), (x[-1], @.6)]
16
11 def read_csv(csv_path):
12 wena By CSV, aE] x AL RA ZWR. URSPRNHOH y
WAR BI sen
13 categories = []
14 x_vals = []
1s y_cols = None
16
17 with open(csv_path, “r", newline="", encoding="utf-8") as f:
18 reader = csv.reader(f)
19 header = next(reader)
20 categories = header(1:] # HEMRA— 5 x
21 y_cols = [[] for _ in categories]
22 for row in reader:
23 if not row:
24 continue
25 x_vals.append(float(row[@]))
26 for i in range(len(categories)):
27 y_cols[i].append(float(row[i + 1]))
28
29 xX_arr = np.array{x_vals, dtype=float)
30 y_list = [np.array(col, dtype=float) for col in y_cols]
31 return x_arr, categories, y_list
32
33 def create_3d_ridgeline_plot(ax, x, categories, y_list):

```

