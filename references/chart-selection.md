# 选图：什么数据用什么图

配色之外，更重要的是学会**恰到好处地选图**。下面是数据形状 → 图类型速查，
加 15 类图的何时用 / 何时不用 / 各自的坑。

## 数据形状 → 图类型速查

| 你要表达什么 | 推荐图 | 常见错用 |
|---|---|---|
| **单变量分布**（1 组数） | violin / box / hist / KDE | pie（除非明确比例分类）|
| **两组分布对比**（treatment vs control） | box+dots / paired box with connecting lines / swarm | 只画均值柱（丢分布信息） |
| **N (3-8) 组对比** | grouped box / swarm 多 panel / bar+error | 3D bar |
| **N (>8) 组对比** | horizontal bar / heatmap 排序 | 挤在一张图里 |
| **时间序列 + 误差** | line + shaded CI（不是 error bar）| error bar 密到看不清 |
| **事件时序**（spikes, behaviors） | raster plot | line plot 无法表达 |
| **累积效应** | cumulative curve | histogram 表达累积效应弱 |
| **双 Y 轴指标共变** | line (主) + bar (副) overlay | 分成两张图丢关联 |
| **相关矩阵 / expression map** | heatmap (diverging 蓝-白-橙) | rainbow color |
| **构成漂移 + 结果共变** | 成分堆叠柱 + 结果折线（双 Y） | 右轴量程掐太窄制造假趋势；写成因果 |
| **多维度 profile 对比**（3-8 维） | radar/spider chart | >8 维时读不出 |
| **配对前后对比**（每 subject 都有前后） | box+individual connecting lines | 只画两组 mean 差异 |
| **散点 + 密度** | scatter + marginal hist / hexbin | 100k+ 点还用 scatter → overplot 一片黑 |
| **占比分类**（部件总和 = 100%） | stacked bar (顶多 4-5 类) | pie（更看不出差异） |
| **不同 scale 数据 + 计数** | 双 Y 轴：主 % / count | 只挑一个 Y |
| **分布形状 + 异常值** | swarm / beeswarm | pure box（异常值淹在 whisker）|

---

## 各类图详细说明

### 1. Box plot（箱线图）
**何时用**：2-N 组数分布对比，样本量 20-1000 都能看。
**优先级**：分组对比第一选择。
**变体**：box + dots（叠加原始点，样本小时必加）；paired box with connecting
lines（same subject 前后 / paired design）。
**坑**：样本 < 15 时 box 会歪；此时改 dots 为主。

### 2. Violin plot（小提琴图）
**何时用**：分布**形状**重要（bimodal / skewed），n > 100。
**优先级**：box 说不完时的升级。
**坑**：小样本时 KDE 平滑会误导（造出假峰）。

### 3. Beeswarm / Swarm plot
**何时用**：中样本（20-200），想同时看**每个点 + 分布形状 + 中位数 line**。
**优先级**：想让 reviewer 看到"我没藏点"时的最佳选择。

### 4. Bar + individual dots
**何时用**：小样本（n < 10 每组），生物学/化学论文标配。
**必配**：`n = X` 直接标在柱上、P-value 直接标 comparison bracket。
**坑**：n ≥ 20 就该升级到 box/swarm。

### 5. Raster plot
**何时用**：event-based 时序（spikes、行为片段、trials 上的响应窗）。
**优先级**：只要有"事件 + 时间"就先想 raster。

### 6. Cumulative curve
**何时用**：累积效应（cumulative duration, cumulative reward, hazard function）。
**优先级**：想说"随时间某量在累积"时比 histogram 强。

### 7. Line + shaded CI
**何时用**：时间序列 + 误差（learning curve, time course, dose-response）。
**shaded 用 alpha ~0.2-0.3 的同色**，比 error bar 干净。
**坑**：n < 5 时 CI 太宽，画出来惨不忍睹，改画每个 sample 独立 line。

### 8. Heatmap
**何时用**：矩阵（相关系数、gene expression、attention map、confusion matrix）。
**配色**：diverging（蓝-白-橙）for zero-centered；sequential（浅到深单色）for
0-1 or 计数。
**坑**：rainbow color 不感知均匀；100×100 以上要 down-sample 或加 dendrogram；
别加太多注释 grid。

### 9. Radar/Spider chart
**何时用**：**3-8 维的 profile 对比**，很少用来对比 > 3 组（会重叠）。
**优先级**：多维度 tradeoff visualization 最直观。
**坑**：维度 > 8 → 换 parallel coordinates；组 > 3 → 换 line 或分开画；
维度 scale 不齐 → 归一化到 [0,1] 再画；顺序敏感：把相关维度放邻近。

### 10. Double-axis (line + bar) overlay
**何时用**：主指标（如 % 准确率）+ 参考量（如 sample count）同时展示。
**优先级**：想让读者一眼看到"这个数据点样本量小"时最好用。
**坑**：两根轴 scale 要在标题里说清避免误读。

### 11. Stacked / grouped bar
**何时用**：占比（stacked, 总和=100%）或多分组对比（grouped, 每组内多柱）。
**优先级**：绝对占比一目了然。
**坑**：stacked 超过 5 段就该考虑 heatmap；grouped 超过 4 组每组超过 4 柱就爆炸。

### 12. Scatter with density / hex / regression
**何时用**：两连续变量关系。n < 500 → scatter with alpha；n < 5000 →
scatter + marginal hist；n > 5000 → hexbin / 2D density。
**坑**：R² 直接标图角，趋势线用虚线不要用实线（避免误认为 y=x）。

### 13. UMAP / tSNE / PCA 2D projection
**何时用**：**高维数据降到 2D 看 cluster / population 结构**（RNA-seq、
embeddings、feature space、cell atlas）。
**必配**：主 UMAP（overall），每点一 sample，颜色 = category；细分 sub-panel
UMAP（挑关键 category 各画一张 zoom-in）；配 horizontal bar chart 列每个
category 的 count 和百分比。
**类别 >20 时**：主图 legend 塞不下，直接把 label 写在 cluster 中心；右侧另开
sorted horizontal bar 给准确 count。
**坑**：tSNE 的簇间距离**没意义**，只有簇内密度有意义；UMAP 参数
（n_neighbors / min_dist）会改变形状，要固定 seed；点数 > 100k 用
rasterize=True；类别多时用 24+ 色（见 palettes.md 的 Palette 7-9）；category
有顺序（stage/time）用 sequential 色 ramp 而不是 categorical。

### 14. Parallel coordinates
**何时用**：**>8 维 profile 对比**（radar chart 处理不了的高维）。
**优先级**：radar 的替代品，维度超 8 时用。
**坑**：轴顺序会影响视觉解读，把相关维度放邻近。

### 15. 成分堆叠柱 + 结果折线（共享 x，双 Y）
**何时用**：想说「**某成分构成随 x 漂移的同时，某结果指标跟着变**」。柱是加和
恒为 1 的构成（各阶段占比、各类别份额），折线是结果（准确率等），共享横轴。
**跟第 10 条的区别**：第 10 条折线为主、柱当样本量背景；这一条**构成为主、
折线是被解释的结果**，读者读的是两者共变。
**坑（最容易造假象的图型之一）**：
- **右轴量程会制造相关性**。定右轴范围前先问：从 0 或实际可能区间起画，这条线
  还动得明显吗。
- **双轴天然诱导因果读法**。共享 x 只能说共变，caption 必须写明 observational。
- **堆叠柱只有最底和最顶一段共享基线**，中间段变化肉眼读不出；要比中间段改分面
  折线或 100% 面积图。
- **成分段数超过 4-5 就该换热图**。
- 多 panel 时右轴含义不同，右轴颜色在承担编码任务，必须在图例/caption 点明。

## Axis 顺序 / dimension count 决策树

- 1 维分布 → box / violin / hist
- 2 维关系 → scatter / heatmap
- 3 维（x, y, z）→ 用 color 编码第 3 维；避免 3D
- 4-8 维 profile → radar
- >8 维 profile → parallel coordinates
- 高维 → UMAP/tSNE 降到 2D
- 时间为一维 → line / area / raster

## 顶刊图组常见"合成 pattern"

- **cumulative + 5-min binned + boxplot** 三件套：总体趋势 → 时间 chunk →
  subject 层面差异。
- **heatmap + summary bar** 双件套：全景 → 挑几个维度做定量对比。
- **raster + curve** 组合：原始事件 + 抽象曲线，同时给 raw 感和 summary。
- **主 Fig 大 hero panel + 4-8 supporting panels**（Nature 常规组图 8-12 panel）。
- **Ablation bar + CI ratio bar** 组合：先分方法看均值再看比例。

## 常见坑（跨图类型）

1. **Pie chart 学术论文别用**（除非明确 5 类以内的比例分类，且比例差 > 10%）。
2. **3D 图别用**（视觉扭曲）。
3. **Rainbow color 别用**（不感知均匀 + 色盲不友好）。
4. **Grid line 除非科学上需要（threshold），全去掉**。
5. **Legend 别塞图内挡数据** → 外置或贴数据点标。
6. **多 panel 字号要统一**。
7. **多 subplot y-axis 不同 scale 但视觉一样** → 读者会误读，加 note
   "note different y-scale"。
8. **数据点数 < axis label 数** → label 密度过高，需要 rotate 或简化。
