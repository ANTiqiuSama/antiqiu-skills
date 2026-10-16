# 南丁格尔玫瑰图：来源与恢复说明

- 来源署名：小明的代码美学
- 来源状态：代码截图恢复与适配
- 效果图：截图 056
- 代码页：[57, 58]
- [原始效果截图](reference.jpg)
- [页序和原文件哈希](../../screenshot-source-manifest.json)

截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

## 明确修改与限制

- 原百分比公式width/pi*100会合计200%；改为value/sum(values)*100。
- 设置半径下界0以显示源码bottom=10的中心留白，微调前两个标签位置避免碰撞。

## 输入与调用

正值类别表；角宽与半径都编码值，不按面积读比例。示例中的随机数与手工数值均为演示数据。

复制完整 [restored.py](restored.py) 后，替换数据定义块；存在 `read_custom_data` 的模板可设置为 True，并提供代码指定的 CSV。连续色标、透明度、轮廓和组合图层保持独立。

运行：`python restored.py`。Matplotlib 弹出图窗，Plotly 打开交互图。导出时使用该库的 `savefig` / `write_image`。

依赖：[统一依赖清单](../../screenshot-requirements.txt)。
