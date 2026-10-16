# SHAP排名双层贡献环与蜂群组合：来源与调用

用户仅提供效果图，未提供原始代码、模型或数据；按截图完整组合结构重建。演示为320个模拟样本、12个变量及含非线性和交互的合成模型，使用解析interventional SHAP，不是原研究结果。

[参考图](reference.jpg) · [共享源码快照](../shap-composites/original.py) · [当前完整调用说明](../../../templates/shap-composites/TEMPLATE.md)

```text
python "<SKILL>/templates/shap-composites/plot_shap_composites.py" --mode contribution --demo --output figures/fig_shap_contribution
```

真实数据用`--features`与`--shap`替代`--demo`；contribution模式另需`--groups-json`。完整格式、统计口径、阈值与分组规则见专用说明。默认随项目配色，`--reference-colors`可选择截图近似色。

连续颜色在每个变量内部按min/max归一化，重要性为平均绝对SHAP。模型归因不是因果效应。变量分组必须有实际含义；占比分母和环图均覆盖全部输入变量，top筛选不改变归一化。组贡献采用各变量mean(abs(SHAP))之和，不与有符号组归因混淆。

原图作者未核验。截图中无法确定的数据定义不凭空复刻；这是保留主要结构的可复用重建，并非原研究的逐像素/数值复现。共享渲染代码仅维护一份，两张卡分别固定调用模式。
