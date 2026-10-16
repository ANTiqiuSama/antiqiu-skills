# 小提琴 + Pearson 完整组合模板

来源：用户提供的 `02-SEM-violin-pearson-plots.zip` 中 `sem-violin-pearson-plots/scripts/plot_sem_violin_pearson.py`。脚本逐字复制，未修改。

用于问卷构念分数的残差分布与相关关系组合展示，或用户明确选择此原版组合图时。直接运行同目录的 `plot_sem_violin_pearson.py`，不要拆成现有配方重新设计。默认保留原版青蓝配色、字体、透明度、左右比例和矩阵结构；本模板不自动套用全局鲜艳/稳重配色。用户明确要求调整时再适配。

```text
python "<SKILL>/templates/sem-violin-pearson/plot_sem_violin_pearson.py" --data "<数据.csv>" --output-dir "<输出目录>" --construct-map-json "<mapping.json>" --order "A,B,C" --prefix sem
```

`mapping.json` 将构念名映射到题项列名，例如 `{"A":["A1","A2"],"B":["B1","B2"],"C":["C1","C2"]}`。已有构念分数也可每个构念映射到一列。按数据实际变量传 `--order`。依赖 numpy、pandas、scipy、matplotlib、seaborn、Pillow、openpyxl；读取 SAV 另需 pyreadstat。原版优先使用 Times New Roman。

交付 `*_violin_pearson_combined.png`，同时保留两张单图 PNG/SVG、计算审计 XLSX 和 JSON。实际打开组合图检查。

原版适用范围：默认按 1–7 分量表绘图，残差显示范围固定为 -2.8 到 2.8；残差来自每个构念对其余构念的 OLS 回归，不是 SEM 路径模型残差。原版直方图为计数、KDE 为密度且共轴；相关色条两端同色。这些行为原样保留，不应声称已修正；超出适用数据范围时说明所需适配。
