# 多Y轴渐变直方图与正态拟合：来源与调用

[用户效果截图](reference.jpg) · [当前完整代码](original.py)

用途：比较多个方法或样本群体在共同测量变量上的分布位置、离散程度与形状。
数据：1–3组同一物理量、同单位的原始观测；长表CSV列为group,value。频数由实际样本分箱统计，不能输入已经汇总的频数冒充原始样本。
结构：共享X轴；第一组左Y轴，其余组右Y轴并外移；组别同色刻度、柱体和虚线；每根柱体从透明底部到有色顶部渐变；白底图例列出样本量及正态拟合参数。
保真：保留64层矢量透明渐变、三组重叠、同色轴关联、正态虚线和独立图层顺序。所有曲线置于柱体上方，双轴的数据变换分别绑定，不把第三组曲线错误放到主轴刻度上。
配色：使用当前项目categorical_colors()固定分类顺序，支持七套主题和自定义配色；不同组至少需要同数量的颜色；--reference-colors明确使用参考图红蓝青颜色，其余调用遵循当前项目配色。
统计：组内等宽分箱，允许各组宽度与边界不同；每组拟合mu=mean、sigma=std(ddof=0)，曲线高度为N×箱宽×正态密度，频数仅为箱计数，曲线是预期频数的近似。正态拟合不等于正态性检验；非正态或零方差数据可用fit=False/--no-fit保留直方图。非有限值、缺失组名和不覆盖样本的分箱报错，不静默删除或截断。
注意：独立Y轴的柱高不能直接跨组比较频数；对绝对频数的比较优先使用共Y轴直方图，比较概率形状可用归一化密度。此模板中的Y轴均为频数，不为多种单位的趋势图。
来源：只有用户效果截图，无原始代码、样本数据与可核验作者；按视觉结构重建。演示为固定种子模拟数据，图中明确标注，不冒充截图研究数据。

## 调用

在初始化的Vivid工作区运行，也可从完整安装包目录运行：

```text
python original.py
python original.py --data samples.csv --bins 14 --xlabel "Residual (um)" --output figures/fig_residual
python original.py --data samples.csv --no-fit
python original.py --reference-colors --output figures/fig_reference
```

CSV格式示例：

```csv
group,value
Method A,-2.1
Method A,3.4
Method B,5.8
Method B,-1.9
```

Python入口 `plot_chart(groups, bins=14, fit=True, ylimits=None)` 返回图对象和逐组统计记录。`groups`为名称到样本数组的字典；`bins`可为统一箱数/边界，或组名到等宽边界数组的字典；每条拟合曲线使用自己那一组的箱宽。`ylimits`可指定每组从0开始且不截断数据的刻度范围。输出PNG、矢量PDF及JSON统计，演示另保存模拟CSV。依赖NumPy、Matplotlib和随包Vivid工具。

相对参考图：保留渐变重叠、正态虚线、左1右2的彩色轴及图例；恢复错位分箱与各组不同柱宽，采用一个Frequency标题和颜色关联轴刻度，外侧轴偏移0.12；图例紧凑排列，删除无对应面板的(a)字样。图形为单面板；没有额外添加装饰子图。
