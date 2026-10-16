# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 012

```text
QO :
WRU: 05-004-NAEE.py @®
import plotly.graph_objects as go
import pandas as pd
## BPRS
read_custom_data = False # ZERMAEXRE
if read_custom_data:
# GRENCSVR ER
data_df = pd.read_csv("data.csv")
else:
# OB MM RER
data = {
"labels': [
HAN, "BY, NCH MDH HEN HEY wBqH uBlM HBy-ae,
"B1-2", "B1-3", "C1", "C2", "D1", "D2", "EI",
"EQ", "E3", "Eq", "E2-1", "E1-2", "E1-3", "E3-1",
"E3-2", "FI", "F2", "3", "F1-1", "F1-2", "F1-3"
1;
'parents': [
mr MA MAN MAU, HAM NAM nBH BH mB pH MBIe
"BI", "CH, NCH, MD, NpM, MEM, HEN Hew nEH,
"EI", "£2", "EL", "ER", "EQ", "pH, upH nEH,
"EI", "EL", HFN
1;
'values': [
6, 8, 0, @, 6, 0, 0, 8, 4, 2,
2, 4, 4, 6, 6, 0, 7, 6, 3,
7, 2, 2, 2, 2, 0, 9, 8,
6, 5, 6
]
}
data_df = pd.DataFrame(data)
data_df.to_csv('data.csv', index=False)
fig = go.Figure(
go. Sunburst (
labels=data_df['labels'].tolist(),
parents=data_df['parents'].tolist(),
1

```

## 截图 013

```text
QO :
ae é
WR: 05-004-MAE.py @®
values=data_df['values'].tolist(),
textinfo='label+percent root’,
textfont=dict(color="white", size=14),
marker=dict(
colors=("#ffffff", "#f9b99e", "#f87F8&c",
"#e37e8e", "#a9758c", "#796b88"],
Line=dict(color="white", width=3)
)>
)
)
fig.update_layout(
margin=dict(t=0, 1=0, r=0, b=0),
width=860,
hei ght=500,
)
fig.show()
2

```

