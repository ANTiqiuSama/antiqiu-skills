# 七套配色示意图

仓库配色展示素材。参照四宫格海报的形式重新设计，使用散点簇、小提琴分布、层叠山脊和堆叠色块展示点色、轮廓、透明度、同色深浅与相邻色效果。

## 查看图片

| 配色 | 高清 PNG | SVG | PDF |
|---|---|---|---|
| 珊瑚青绿 | [PNG](../../docs/images/palettes/coral-teal.png) | [SVG](../../docs/images/palettes/coral-teal.svg) | [PDF](../../docs/images/palettes/coral-teal.pdf) |
| 橄榄杏棕 | [PNG](../../docs/images/palettes/olive-apricot.png) | [SVG](../../docs/images/palettes/olive-apricot.svg) | [PDF](../../docs/images/palettes/olive-apricot.pdf) |
| 蓝粉浅彩 | [PNG](../../docs/images/palettes/blue-pink.png) | [SVG](../../docs/images/palettes/blue-pink.svg) | [PDF](../../docs/images/palettes/blue-pink.pdf) |
| 蓝天绿地 | [PNG](../../docs/images/palettes/blue-sky.png) | [SVG](../../docs/images/palettes/blue-sky.svg) | [PDF](../../docs/images/palettes/blue-sky.pdf) |
| 柔绿森林 | [PNG](../../docs/images/palettes/soft-forest.png) | [SVG](../../docs/images/palettes/soft-forest.svg) | [PDF](../../docs/images/palettes/soft-forest.pdf) |
| 粉彩少女 | [PNG](../../docs/images/palettes/pastel-girl.png) | [SVG](../../docs/images/palettes/pastel-girl.svg) | [PDF](../../docs/images/palettes/pastel-girl.pdf) |
| 海洋清风 | [PNG](../../docs/images/palettes/ocean-breeze.png) | [SVG](../../docs/images/palettes/ocean-breeze.svg) | [PDF](../../docs/images/palettes/ocean-breeze.pdf) |

本地浏览器打开 [index.html](../../docs/images/palettes/index.html) 可并排比较。PNG 为 2400 × 2880 像素、300dpi。SVG 与 PDF 保留文本轮廓/嵌入字体及矢量图形；海报背景渐变是内嵌栅格层，山脊为矢量半透明填充。

## 复现

从仓库根目录运行：

```bash
python examples/palette-posters/render.py
```

可使用 `--output <目录>` 更改输出位置。需要仓库 Python 绘图依赖及微软雅黑、Noto Sans CJK SC、苹方或黑体之一。颜色直接读取 [palettes.json](../../original/resources/assets/shared-scripts/palettes.json)，通过临时项目的统一配置传入 `setup_style()`，不修改默认配色或已安装的 Skill。

原三张图共用固定种子 `20260915` 生成的 [demo-data.json](demo-data.json)，与本次充电调度实测数据无关：

- 散点簇：7 组，每组 200 个二维模拟点；直接生成坐标，未声称执行聚类或降维。
- 小提琴：前 5 组模拟得分，每组 240 个样本；点为中位数，粗线为四分位范围。
- 山脊：7 组模拟得分，核密度曲线各自等高归一化；虚线和白边点标出中位数。峰高不代表样本量。
- 堆叠柱：5 个样本、7 种成分，每根柱子的比例合计 100%。

珊瑚青绿与橄榄杏棕各有 7 个原色。蓝粉浅彩有 5 个原色，七组对照中的 F/G 分别为 A/C 与白色混合 42% 的派生色。海报上方仅列原色和原始色值，下方图例与脚注说明派生色。

新增四套按用户截图的 HEX 标签逐项录入，每套 8 色，来源记录见 [palette-sources.json](palette-sources.json)。新四张共用 [demo-data-8.json](demo-data-8.json)：在原七组样本之外，用固定种子 `20260916` 增加第八组散点与得分；堆叠图原七项等比缩至88%，第八项为12%。原三张示意图及其数据保留。

只生成新增四张：

```bash
python examples/palette-posters/render.py --palettes blue-sky soft-forest pastel-girl ocean-breeze
```

## 源码与适配

[render.py](render.py) 为可编辑绘图源码；[sources/](sources/) 保留当前完整配方章节和首个完整 Python 示例。海报不是图库中单张配方的原样截图：

- 自定义散点示意图与海报布局。
- 小提琴由 `advanced.grouped_violin` 的浅琴体、独立轮廓、中位数点及四分位线适配。
- 山脊沿用 `advanced.ridgeline` 的 `_lighten(color, 0.5)` 单层浅填充、`alpha=0.85`、独立原色轮廓和由后到前的遮叠顺序，不添加连续渐变。保留原始峰值进行归一化，中位数线高度与曲线一致。
- 堆叠色块由 `basic.stacked_bar` 适配：保留累计堆叠与浅填色/原色边界。为突出配色，省去各块数值、固定为 100% 的总量折线和同比文字。

首稿错误复用了旧 `palette-showcase/render.py` 的不透明渐变层，盖住了山脊的半透明填充。用户指出后完成第1轮修复：移除该覆盖层，按当前配方恢复浅色透明填充，并重新查看三种配色。之前的“无需修复”结论不作为模板保真通过记录。数据一致性、原色色值、PNG尺寸、SVG可解析性及PDF页数已检查；详见输出目录的 `verification.json` 与 `render-info.json`。

## 仓库首页引用

以下相对路径可直接用于仓库根目录的 README；首页已使用这些图片：

```markdown
### 珊瑚青绿
![珊瑚青绿：散点、小提琴、山脊与堆叠柱配色示意](docs/images/palettes/coral-teal.png)

### 橄榄杏棕
![橄榄杏棕：散点、小提琴、山脊与堆叠柱配色示意](docs/images/palettes/olive-apricot.png)

### 蓝粉浅彩
![蓝粉浅彩：散点、小提琴、山脊与堆叠柱配色示意](docs/images/palettes/blue-pink.png)
```

新增四张已逐张查看，未追加修复；每张输出PNG、SVG和PDF，可在仓库中下载。

### 浅色可读性修正

蓝天绿地、粉彩少女完成1轮局部修正：浅色图元减少额外提亮，较深的同色派生用于轮廓、散点细边和统计标记。原始色值与顶部色卡不变，山脊alpha=0.85、小提琴alpha=0.8、散点alpha=0.83不变，无额外渐变层。该适配仅用于这两张海报，未修改全局配色或原配方。两张修正版已实际查看。

本轮色板调整：蓝天绿地、柔绿森林、粉彩少女和海洋清风中过浅的原始 HEX 已适度调深，海报沿用现有生成脚本重新输出。此次仅调整色板源，未改变海报或数据图模板的提白、透明度及绘图流程。
