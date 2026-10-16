# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 017

```text
ae
Python Sry #i(t-Hi
import json
import random
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from scipy.signal import find_peaks
## APES
read_custom_data = False # ZH ERMRAENRE
if read_custom_data:
# HER csv ME
data = pd.read_csv("data.csv")
else:
# GBR RES
def create_data(x, size, n, max_value):
sigma = size / 30 # #H# FE
return max_value * np.exp(-0.5 * ((x - n) /
sigma) ** 2)
random. seed(16)
size, x_max = 300, 80
4/8

```

## 截图 018

```text
ae
Python Sry #i(t-Hi
xX = np.linspace(®, x_max, size)
peaks = [5, 15, 23, 30, 35, 40, 53, 60]
means = (2.5, 1.2, 3.0, 2.5, 1.0, 1.5, 2.0, 2.2]
data = {"x": x}
for i in range(4):
y = np.zeros_like(x)
for p, m in zip(peaks, means):
y += create_data(x, x_max, p, m *
random. random())
data([f" 38 BU {i+1}"] = y
data = pd.DataFrame(data)
#4 2 & RUE
x = data["x"].values # MARE
a MS TK Bl SR
categories = [c for c in data.columns if c != "x"]
# Ae
colors = ["#e7c2cb", "#daa2bo", "#cd8295", "#c0627a"]
fig = go.Figure() # #32 figure WR
## al REA
for cat, color in zip(categories, colors):
5/8

```

## 截图 019

```text
QO :
eo!
Python S27) #i(t-AAl ©
fig.add_trace(
go. Scatter (
X=X,
y=data[cat],
Fill="tonexty",
mode="none",
name=cat,
fillcolor=color,
stackgroup="one",
)
)
He BDA
y_matrix = data[categories].T.values
y_stack = np.cumsum(y_matrix, axis=0)
for ys in y_stack:
fig.add_trace(
go. Scatter (
X=X,
y=ys,
mode="lines",
Line=dict(width=2, color="#ffffff") ,
showlegend=False,
6/8

```

## 截图 020

```text
QO :
eo!
Python SGen 30 (t-MiB1 ©
)
)
ae 2 ill 1 fa
idx, _ = find_peaks(y_stack[-1])
fig.add_trace(
go.Scatter (
x=x[idx],
y=y_stack[-1] [idx],
mode="markers",
marker=dict(
symbol="circle",
size=8,
color="#ffffff" ,
Line=dict(width=2, color="#c0627a") ,
) ?
showLlegend=False,
)
)
## RO RBS
for px, py in zip(x[idx], y_stack[-1][idx]):
fig.add_annotation(x=px, y=py + 0.3,
7/8

```

## 截图 021

```text
QO :
e
Python SGenT 3 (t-MiB1E
text=f"{py:.2f}", showarrow=False)
H## REG. GHEE ARRT
fig.update_layout(
xaxis=dict(title="X Mi", range=[0, 70]),
yaxis=dict(title="& (i", range=[0, 10]),
width=800,
height=500,
)
fig.show() # #HETRAR
8/8

```

