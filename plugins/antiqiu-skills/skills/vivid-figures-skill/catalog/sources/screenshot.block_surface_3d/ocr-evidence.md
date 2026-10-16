# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 043

```text
ae
BiG: =REABL py @®
import plotly.graph_objects as go
import numpy as np
def hex_to_rgb(hex_color):
wire +S oF fl Bi f RGB"
hex_color = hex_color.\Istrip('#')
return tuple(int(hex_color[i:i+2], 16) for i in (®, 2,
4))
def rgb_to_hex (rgb):
mwRGR FE-PE
return f'#{rgb[0] :02x}{rgb[1] :02x}{rgb[2]:02x}'
def interpolate_color(value, color_list):
weet re a BA fn
if value <= 0:
return color_list[0]
if value >= 1:
return color_list[-1]
n = len(color_list) - 1
segment = min(int(value * n), n - 1)
local_t = (value - segment / n) *n
rgb1, rgb2 = hex_to_rgb(color_list[segment]),
hex_to_rgb(color_list[segment + 1])
interpolated_rgb = tuple(int({1 - local_t) * cl +
local_t * ¢2) for cl, c2 in zip(rgbl, rgb2))
return rgb_to_hex(interpolated_rgb)
def towers(fig, a, e, pos_x, pos_y, color_list, global_min,
global_max) ;
wun ge il oF Fy GR BE
x_vals, y_vals = np.linspace(pos_x - a / 2, pos_x +a /
2, 2), np.linspace(pos_y - a / 2, pos_y + a / 2, 2)
xX, Y, Z = np.meshgrid(x_vals, y_vals, [0, e]}
normalized_e = (e - global_min) / (global_max -
1

```

## 截图 044

```text
ae
BiG: =REABL py @
global_min) if global_max > global_min else @
color = interpolate_color(normalized_e, color_list)
fig.add_trace(go.Mesh3d(x=x.flatten(), y=y.flatten(),
z=z.flatten(), alphahull=1, flatshading=True, color=color))
vertices = np.array([[pos_x - a / 2, pos_y - a / 2, 6],
[pos_x + a / 2, pos_y - a / 2, 9],
[pos_x + a / 2, pos_y + a / 2, 0],
[pos_x - a / 2, pos_y + a / 2, O],
[pos_x - a / 2, pos_y - a / 2, e],
[pos_x + a / 2, pos_y - a / 2, e],
[pos_x + a / 2, pos_y + a / 2, e],
[pos_x - a / 2, pos_y + a / 2, e]])
edges = [[0, 12], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6],
(6, 7], [7, 4], (6, 4], [1, 5], [2, 6], (3, 7]]
edge_x, edge_y, edge_z = [], [], []
for edge in edges:
edge_x += [vertices[edge[@], ©], vertices[edge[1],
6], None]
edge_y += [vertices[edge[6], 1], vertices[edge[1],
1], None]
edge_z += [vertices[edge[@], 2], vertices[edge[1],
2], None]
fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z,
mode='lines', Line=dict(color='white', width=3)))
4 ERR
rows, cols = 16, 11
X, y = np.linspace(-1, 1, cols), np.linspace(-1.7, 1.3,
rows)
X, Y = np.meshgrid(x, y)
Z = np.exp(-((X+0.5) **2 + (¥#0.5)**2) / 0.7) * 1.5 +
np.exp(-((X-0.5)**2 + (¥-0.5)**2) / 0.3)
xx, yy, 2Z = X.flatten(), Y.flatten(), Z.flatten()
2

```

## 截图 045

```text
BiG: =REABL py @®
global_min, global_max = np.min(zz), np.max(zz)
fig = go.Figure()
color_list = ["#214e81", "#e9dlab", "#c2768b"]
color_list = ["#214e81", "#8d9eb2","#cecccc", "“#dc9fbo",
"#c2768b"]
for x_val, y_val, z_val in zip(xx, yy, zz):
towers(fig, 6.15, z_val, x_val, y_val, color_list,
global_min, global_max)
fig.update_layout (
showlegend=False,
autosize=True,
margin=dict(1=0, r=0, t=0, b=@),
scene=dict(
xaxis=dict(title="X", backgroundcolor="#f8f1f1") ,
yaxis=dict(title="¥", backgroundcolor="#f8f1fl") ,
zaxis=dict(title="Z", backgroundcolor="#f8f1fl") ,
aspectmode="data",
ys
)
fig.show()
3

```

