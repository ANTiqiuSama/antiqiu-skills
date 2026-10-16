# 按需参考

选定模板后的适配以完整源码和卡片保留要点为准；以下示例仅在确有需要时使用，不作为重写已选模板的理由。

<figure_selection_guide>
## Data → Figure Type Decision Table

Before choosing a figure type, analyze the data characteristics, then match using this table. Read the full code from the corresponding recipes file.

<selection_priority>
### Selection priority: match data shape, not visual novelty

Choose the figure type that best communicates your data, not the fanciest one available. The decision order is:

1. **First check the "By data shape" table below** — match your data characteristics to the recommended figure type
2. **If multiple options fit**, prefer the one your target audience (competition judges, reviewers) will instantly understand
3. **Use advanced recipes** (Lollipop, Dumbbell, Waterfall, SHAP, etc.) when they genuinely add information that basic charts cannot show — e.g., Waterfall shows incremental contribution, SHAP shows feature direction
4. **Use basic recipes** (grouped bar, line, scatter) when they are the clearest way to present the data — a well-made grouped bar chart is better than a confusing Bump chart

A paper needs visual variety — mix basic and advanced charts. A paper with ALL advanced charts looks like it's trying too hard. A paper with ALL bar charts looks monotonous. Balance is key.

Repeated chart types are appropriate for consistent comparisons; no fixed type quota applies.
</selection_priority>

### By data shape

| Data characteristic | Best figure type | Recipes file | Avoid |
|---|---|---|---|
| ≤3 methods × 1-2 metrics | Three-line table | — | Any chart — too few data points for a meaningful figure |
| 4+ methods × 1 metric | Lollipop Chart or Grouped Bar | recipe:advanced.lollipop, recipe:basic.grouped_bar | — |
| A vs B (2 methods, multiple metrics) | Dumbbell Chart | recipe:advanced.dumbbell | heatmap — 2 rows looks like a traffic light |
| A vs B vs C (3-5 methods, multiple metrics) | Grouped Bar Chart or Radar chart | recipe:basic.grouped_bar, recipe:competition.radar | — |
| Methods × Metrics matrix (≤5×5) | Method Comparison Heatmap or Grouped Bar | recipe:advanced.method_heatmap, recipe:basic.grouped_bar | — |
| Methods × Metrics (show trends across metrics) | Parallel Coordinates | recipe:advanced.parallel_coordinates | multiple separate charts |
| Methods × Metrics matrix (>5×5) | Heatmap with values | recipe:basic.heatmap | — |
| Methods × Datasets ranking | Bump Chart or Grouped Bar | recipe:advanced.bump, recipe:basic.grouped_bar | — |
| Before/after comparison | Dumbbell Chart or Grouped Bar | recipe:advanced.dumbbell, recipe:basic.grouped_bar | — |
| Before/after (paired samples) | Paired Dot Plot | recipe:advanced.paired_dot | grouped bar (hides individual variation) |
| Relative to baseline (±%) | Diverging Bar Chart | recipe:advanced.diverging_bar | grouped bar (doesn't show direction clearly) |
| Two-group mirror comparison | Back-to-Back Bar Chart | recipe:advanced.back_to_back_bar | — |
| Multi-model statistical comparison | Taylor Diagram | recipe:advanced.taylor | separate RMSE/R²/StdDev bar charts |
| Distribution comparison (5-15 groups) | Ridgeline Plot | recipe:advanced.ridgeline | multiple histograms (wastes space) |
| Distribution comparison (2-4 groups × categories) | Grouped Violin Plot | recipe:advanced.grouped_violin | box plot (hides distribution shape) |
| Module contribution (ablation) | Waterfall Chart | recipe:advanced.waterfall | bar chart |
| Time series (1-3 lines) | Line plot with CI band | recipe:basic.line | — |
| Time series (4+ lines) | Small multiples (subplot grid) | recipe:basic.multipanel | spaghetti plot |
| Distribution (1 group) | Violin + strip | recipe:basic.raincloud_violin | histogram |
| Distribution (2-5 groups) | Rain Cloud Plot | recipe:basic.raincloud | box plot |
| Proportion/composition | Donut Chart or Stacked Area | recipe:basic.donut, recipe:basic.area | pie chart |
| Correlation matrix | Heatmap + dendrogram | recipe:advanced.cluster_heatmap | plain heatmap |
| 2D scatter + relationship | Scatter + regression + R² | recipe:basic.scatter_regression | — |
| 2D joint distribution (large N) | Hexbin + marginal histograms | recipe:competition.hexbin_joint | plain scatter (overplotting) |
| 2D joint distribution (small N, clusters) | KDE contour + marginal density | recipe:competition.kde_joint | plain scatter |
| 2D relationship + distribution | Scatter + regression + marginal density | recipe:competition.scatter_regression_marginals | scatter without marginals |
| High-dim features | t-SNE/UMAP scatter | recipe:academic.tsne_umap | — |
| 3D clustering results (3 features) | 3D scatter + centroids | recipe:competition.cluster_3d | 2D scatter (loses dimension) |
| Multi-criteria evaluation | Radar chart | recipe:competition.radar | — |
| Feature importance | SHAP Summary Plot | recipe:advanced.shap_summary | horizontal bar |
| Classification result | Confusion matrix | recipe:competition.confusion_matrix | — |
| Binary classifier comparison | ROC + AUC | recipe:competition.roc | — |
| Probability reliability | Calibration Plot | recipe:advanced.calibration | — |
| Sensitivity (single-param sweep, rank drivers) | Tornado Chart (barh sorted by range) | recipe:competition.tornado | grouped bar (loses ranking) |
| Throughput/flow loss per stage | Sankey Diagram | recipe:advanced.sankey | stacked bar (hides chain) |
| Two-factor response / error propagation | 3D Surface + projected contour | recipe:competition.surface_3d | heatmap (loses magnitude) |

### By problem domain (competition)

| Problem type | Recommended figures | Recipes |
|---|---|---|
| Optimization (GA/PSO/SA) | Convergence curve + 3D surface + Pareto front | recipe:competition.convergence, recipe:competition.surface_3d, recipe:competition.pareto_front |
| Scheduling/routing | Gantt chart + Network path | recipe:competition.gantt, recipe:competition.network_path |
| Classification/clustering | Confusion matrix + ROC + 3D cluster scatter | recipe:competition.confusion_matrix, recipe:competition.roc, recipe:competition.cluster_3d |
| Regression/prediction | Prediction vs Actual with CI band + Error Rain Cloud + Multi-step decay + Model accuracy heatmap | recipe:empirical.prediction_ci, recipe:empirical.prediction_error_raincloud, recipe:empirical.multistep_decay, recipe:empirical.prediction_accuracy_heatmap |
| Sensitivity analysis | Tornado chart + Contour + 3D surface | recipe:competition.tornado, recipe:competition.contour, recipe:competition.surface_3d |
| Spatial data | China province choropleth + Spatiotemporal matrix | recipe:competition.china_choropleth, recipe:competition.spatiotemporal_heatmap |
| Multi-objective | 2D Pareto + 3D Pareto surface | recipe:competition.pareto_front, recipe:competition.pareto_surface_3d |
| Factor decomposition | Waterfall chart | recipe:competition.waterfall, recipe:advanced.waterfall |

### By problem domain (academic/empirical)

| Paper type | Recommended figures | Recipes |
|---|---|---|
| DID/causal inference | Parallel trends + Event study + Placebo | recipe:empirical.parallel_trends, recipe:empirical.event_study, recipe:empirical.placebo |
| Regression analysis | Forest plot + Heterogeneity forest + Marginal effects | recipe:empirical.forest, recipe:empirical.subgroup_forest, recipe:empirical.marginal_effects |
| Prediction/forecasting | Prediction with CI band + Error Rain Cloud + Multi-step decay + Model heatmap | recipe:empirical.prediction_ci, recipe:empirical.prediction_error_raincloud, recipe:empirical.multistep_decay, recipe:empirical.prediction_accuracy_heatmap |
| Deep learning | Training curves + Attention map + t-SNE | recipe:academic.training_curves, recipe:academic.attention_heatmap, recipe:academic.tsne_umap |
| Model comparison | Grouped Bar + Method Comparison Heatmap + Radar | recipe:basic.grouped_bar, recipe:advanced.method_heatmap, recipe:competition.radar |
| Hyperparameter tuning | Sensitivity grid + 3D loss landscape | recipe:academic.hyperparameter_sensitivity, recipe:competition.surface_3d |
| Meta-analysis | Forest plot + Funnel plot | recipe:empirical.forest, recipe:advanced.funnel |
| Survival analysis | Kaplan-Meier curve | recipe:advanced.kaplan_meier |
| Genomics/omics | Volcano plot + Cluster heatmap | recipe:advanced.volcano, recipe:advanced.cluster_heatmap |
| Method agreement | Bland-Altman plot | recipe:advanced.bland_altman |

### Anti-patterns (check before generating — but use judgment)

Not every "upgrade" is appropriate. Check this table, but choose based on clarity for your audience.

| ❌ If you were going to use... | ✅ Consider this instead | Why | When to upgrade |
|---|---|---|---|
| Single-metric bar chart for ranking | Lollipop Chart | Less visual noise for pure ranking | When showing 5+ items ranked by one metric |
| Horizontal bar for feature importance | SHAP Summary Plot | Shows direction + magnitude | When you have SHAP values available |
| Bar chart for ablation | Waterfall Chart | Shows additive incremental contributions | Only when differences form a meaningful additive sequence; independent ablations may use comparison plots |
| Bar chart for before/after (2 groups) | Dumbbell Chart | Shows direction and magnitude of change | When comparing exactly 2 conditions |
| Plain box plot | Rain Cloud Plot | Distribution shape + box stats + raw data | When sample size > 20 and distribution shape matters |
| Pie chart | Donut Chart | Leaves a center for a meaningful total | Optional; compare readability and preserve the selected template |
| Plain heatmap | Heatmap + dendrogram | Adds clustering structure | When row/column ordering matters |
| Stacked bar (non-temporal) | Sankey Diagram | Shows flow direction | When data represents flow/routing |
| RdYlGn colormap | palette_cmap | Use the project continuous palette | Select sequential/diverging from data meaning |

**Keep using grouped bar chart when:**
- Comparing 3-5 methods across 2-5 metrics (this is what grouped bar charts are designed for)
- Your audience is competition judges or non-specialist reviewers who expect familiar chart types
- The data has clear, discrete categories on the x-axis
- You already have too many advanced charts in the paper and need visual variety

**Keep using line chart when:**
- Showing trends over time or continuous x-axis
- Comparing convergence curves or training progress
</figure_selection_guide>

<bar_chart_alternatives>
### 柱状图使用指南

柱状图是最通用、最易读的图表类型之一。不要回避使用它。

**适合用柱状图的场景（直接用，不需要替代）：**
- 3-5 个方法在 2-5 个指标上的对比 → 分组柱状图
- 类别数据的频次/计数对比 → 普通柱状图
- 需要评委/读者一眼看懂的核心结果 → 分组柱状图
- 论文中已经有多个高级图表，需要平衡 → 柱状图

**适合用替代方案的场景：**

| 场景 | 替代方案 | 原因 |
|------|---------|------|
| 单指标排名（5+项） | Lollipop Chart | 纯排名场景，棒棒糖更简洁 |
| 消融实验 | Waterfall Chart | 展示增量贡献，柱状图做不到 |
| 前后两组对比 | Dumbbell Chart | 展示变化方向和幅度 |
| 特征重要性（有SHAP值） | SHAP Summary Plot | 同时展示重要性和方向 |
| 多数据集排名变化 | Bump Chart | 展示排名交叉 |

**图集一致性：** 按数据和表达收益选择；需要一致比较时可重复图型，不设数量配额。
</bar_chart_alternatives>

不同图表类型有不同的最佳配色策略，不能一刀切：
