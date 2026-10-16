# 径向环形热图：来源与恢复说明

- 来源署名：小明的代码美学
- 来源状态：代码截图恢复与适配
- 效果图：截图 098
- 代码页：[99, 100, 101, 102]
- [原始效果截图](reference.jpg)
- [页序和原文件哈希](../../screenshot-source-manifest.json)

截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

## 明确修改与限制

- 显式align=edge统一环形单元角度边界与缺口；设置半径下界0保留中心空白。

## 输入与调用

有行列标签的二维数值矩阵。示例中的随机数与手工数值均为演示数据。

复制完整 [restored.py](restored.py) 后，替换数据定义块；存在 `read_custom_data` 的模板可设置为 True，并提供代码指定的 CSV。连续色标、透明度、轮廓和组合图层保持独立。

运行：`python restored.py`。Matplotlib 弹出图窗，Plotly 打开交互图。导出时使用该库的 `savefig` / `write_image`。

依赖：[统一依赖清单](../../screenshot-requirements.txt)。

## 项目配色适配

热图默认读取项目配色；连续插值、中性色、透明度及数据归一化保留，数值文字按实际底色选择对比色。在已运行 bootstrap 的任务工作区执行，依赖随工作区复制的 `_utils/palette_maps.py`。
