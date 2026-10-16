# 数据图尺寸预计算

完整尺寸规则唯一维护在 [figure_layout_reference.md](../resources/assets/shared-scripts/figure_layout_reference.md) 的 `figsize` 与最终引用尺寸章节，绘制前读取该部分，不另存一套尺寸表。

在写每张新图的 figsize 前，代入本次实际引用宽度与高度限制，计算“上页字号 = 代码字号 × 引用宽 ÷ 原生宽”，并记在现有规划或脚本说明中。原文示例宽度不是所有任务的固定尺寸；不固定所有图为 136 mm，也不新增字号门槛。按实际显示比例与可读性调整字号、线宽和画布，避免画布远大于显示宽度造成整体缩小。
