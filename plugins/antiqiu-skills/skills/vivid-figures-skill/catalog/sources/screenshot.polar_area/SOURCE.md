# 平滑极坐标面积叠加：来源与恢复说明

- 来源署名：小明的代码美学
- 来源状态：代码截图恢复，原数据缺失
- 效果图：截图 116
- 代码页：[118, 119, 120]
- [原始效果截图](reference.jpg)
- [页序和原文件哈希](../../screenshot-source-manifest.json)

截图中的若干 .mplstyle 文件未附带；使用源码可见色值、透明度和描边，加上可移植字体/白背景默认值。代码通过视觉读取及OCR辅助恢复，并局部适配，不是作者原始文件的逐字副本。

## 明确修改与限制

- 原data.csv缺失，补充angle及三个value列的周期合成示例。
- 增加角度顺序及端点检查，周期样条在0/360处同时闭合值和斜率。
- 原中心Circle仅创建且使用私有变换；改为实际绘制的白色中心覆盖，保留空心基座。

## 输入与调用

angle（度）和多个 value 列；角度严格递增且不重复360°。示例中的随机数与手工数值均为演示数据。

复制完整 [restored.py](restored.py) 后，替换数据定义块；存在 `read_custom_data` 的模板可设置为 True，并提供代码指定的 CSV。连续色标、透明度、轮廓和组合图层保持独立。

运行：`python restored.py`。Matplotlib 弹出图窗，Plotly 打开交互图。导出时使用该库的 `savefig` / `write_image`。

依赖：[统一依赖清单](../../screenshot-requirements.txt)。
