# 立体方块相关性热图：来源、编码与调用

[参考图](reference.jpg) · [当前完整源码](original.py)

用途：展示多个变量两两之间的正负相关关系，并用浮雕方块突出矩阵结构。
输入：至少3行完整观测的数值表，或已计算的Pearson相关矩阵；2–40个变量及唯一标签。原始数据不允许缺失、非有限值或常数列；相关矩阵须对称、对角线为1、值域[-1,1]且在数值容差内半正定。不能把任意随机方阵当相关矩阵。
结构：完整N×N矩阵，固定斜投影，方形正面加两片阴影侧壁，密集细棱线、顶部阶梯轮廓、左侧行标签、底部竖排列标签与侧边Pearson r色条；PNG和PDF均由确定性矢量多边形绘制。
数据编码：正面颜色严格对应r，色条固定[-1,1]；凸起长度h=relief×(0.12+1.4×(r+1)/2)，随有符号r增加，非abs(r)。高度规则是本模板明确选定的约定，参考图未提供原高度定义。阴影侧面不用于读取相关系数；标签锚定原矩阵基座，正面随凸起向右上平移。
配色：常规调用读取当前主题的发散色阶，保留r=0中性中心；--reference-colors明确选择参考蓝色色阶。不会修改共享热图配色算法。可传入cmap覆盖，正面和色条必须同源。
来源：用户仅提供效果图，无原始代码和数据；按图重建立体结构，示例由固定种子潜在因子样本计算相关矩阵。领域标签沿用截图作版式演示，不代表该研究的实测相关关系。
局限：浮雕遮挡可能削弱逐格精确查值；需要精确读数时配合矩阵CSV或平面热图。布局不是可旋转的三维场景，也不含显著性或因果判断；不平滑、不重排、不填造缺失值。

## 调用

在初始化的Vivid工作区运行，也可从完整安装包直接执行：

```text
python original.py
python original.py --reference-colors --output figures/fig_reference_relief
python original.py --data observations.csv --output figures/fig_correlations
python original.py --matrix correlations.csv --relief 0.8
```

观测CSV首行为变量名，其余行为数值观测，不含样本ID列；矩阵CSV左上角为空或variable，首行和首列为顺序一致的变量名。输出PNG、矢量PDF、矩阵CSV与编码JSON，模拟演示另保存原始样本CSV。

Python接口：`plot_chart(matrix, labels, cmap=None, relief=1.0)`。正面保留单位正方形，`relief`只改变浮雕强度，颜色仍编码同一r。可以用`relief=0`查看平面布局。单位方形和阴影不可替换成连续光滑曲面；完整矩阵、变量顺序和色条值域须保留。

依赖NumPy、Matplotlib和随包Vivid工具。仅重建截图可见的设计；参考图作者未核验，不声称获得作者源码。
