# 代码截图的辅助OCR转录（未经逐字校订，不可直接运行）

以原始截图为准；可运行恢复版见 restored.py。

## 截图 008

```text
def load_style():

Un pn Be RE shee

try:

plt.style.use("robox.mplstyle")
except:
pass

#iRRPRSH, LERERPM

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]

plt.rcParams["axes.unicode_minus"] = False

plt.rcParams["grid.color"] = "#fed2d2"
def generate_single_weighted_random(scale=1.5, lower=1,
upper=10):

SR Th BALK, BABY RE ee BN

- scale: HRD AHA, BRARAH TE

- lower: RMB

- upper: RATA

value = np.random.exponential(scale) + lower

value = np.clip(value, lower, upper) # 4 fA 0R BIZ
[lower, upper] st

return value
def create_smooth_peak_data(x, start, peak, end, max_value):

ERAT SORE, RA SM MERR RO Sm

- start: Asati

- peak: 3X 2 le ff BY ia]

— end: 4458 Bt ial

1

```

## 截图 088

```text
WKB: RE.py
- max_value: IA)
nie
y = np.zeros_like(x)
eR BLAME (B Mens)
rising = (x >= start) & (x <= peak)
sigma_rise = (peak - start) /3 # #3#ILAWEE
y[rising] = max_value * np.exp(-((x[rising] - peak} *«
2) / (2 * sigma_rise**2))
# FR PRRR (Se +i Rm)
falling = (x > peak) & (x <= end)
sigma_fall = (end - peak) / 3 # #2 FREE
y[falling] = max_value * np.exp(-((x[falling] - peak) **
2) / (2 * sigma_fall**2))
return y
def create_streamgraph_chart (ax):
Ce oe CS
def generate_data(
num_categories, start_base, peak_base, end_base,
interval, direction
):
for i in range(num_categories):
start = start_base + (
i * interval if direction == "forward" else
-i * interval
)
peak = peak_base + (
i * interval if direction == "forward" else
-i * interval
)
end = end_base + (i * interval if direction ==
"forward" else -i * interval)
max_value = generate_single_weighted_random(6,
1, 10000)
y_list. append (create_smooth_peak_data(x, start,
2

```

## 截图 089

```text
ae
CH: FIRE py @
peak, end, max_value))
color_list.append(assign_color (max_value) )
categories .append(f" # Bil {len(categories) + 1}")

def assign_color(value):

thresholds = [5, 7.5, 8, 12, 15, 20, 25]

‘idx = sum(value > t for t in thresholds) # it®@@it

BEDRMS IEA RSI

return hex_colors[idx]
np.random. seed (30)
x = np.linspace(@, 800, 806)
y_list, color_list, categories = [], [], [J
hex_colors = [

"#214e81",

"#456991",

"#6983a2",

"#8d9eb2",

"#dc9fbe",

"#cfBb9e",

"#02768b",

"#a55d75",
]
generate_data(72, 720, 746, 820, 16, “backward")
generate_data(72, 6, 20, 100, 10, "forward")
y_list = np.array(y_list)
polys = ax.stackplot(

Xy

y_list,

colors=color_list,

labels=categories,

zorder=16,

alpha=1,

baseline="wiggle",
)
for poly in polys:

3

```

## 截图 090

```text
QO :

MR: FUN py @®
verts = poly.get_paths()[@].vertices
ax.plot(verts[:, 0], verts[:, 1], color="#ffffff",

zorder=20, Linewidth=0.5)
# $32 colerbar
cmap = LinearSegmentedColormap. from_list("custom_cmap",
hex_colors)
norm = Normalize(vmin=y_list.min(), vmax=y_list.max())
# RMA
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) # BMIRB—-TSERAUERMAR
cbar = plt.colorbar(sm, ax=ax, orientation="vertical",
pad=0.01, fraction=0.05)
cbar.ax.tick_params(size=@)
4 2a
ax. grid(axis="x", which="major", linestyle="-",
linewidth=1, color="#ffffff")
ax. xaxis.set_major_locator(ticker.MultipleLocator (168) )
+ EMR
ax. set_xticks(
[O, 100, 200, 300, 400, 500, 600, 760, 800],
[2020, 2021, 2022, 2623, 2024, 2025, 2026, 2027,
2028],
)
ax.set(ylim=(-75, 75), yticks=[])
ax.set_title("7]7EM", x=0.015, y=0.95, ha="left",
va="top")
plt.tight_Layout()
if __name__ == "__main__":
load_style()
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
create_streamgraph_chart (ax)
plt.show()
4

```

