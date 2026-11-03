# 顶刊配图配色 palette 参考

9 组可直接复用的顶刊（Nature / Science / Cell）配色 + 通用 style 原则。
配色之外更重要的选图判断见 `chart-selection.md`。

## Palette 1 — 柔和粉/蓝/米（最通用，适合 mixed 组图）

```
#D5D7D6  R:213 G:215 B:214  (中性灰)
#F1C3C1  R:241 G:195 B:193  (柔粉)
#B7D5EC  R:183 G:213 B:236  (柔蓝)
#FEDFB1  R:254 G:223 B:177  (米黄)
#B9C3DC  R:185 G:195 B:220  (灰紫)
#EEB3C1  R:238 G:179 B:193  (灰粉)
```
配对：粉+蓝对照最标准；米+紫做次要 arm。

## Palette 2 — 蓝橘 diverging（热图必备）

```
#385a75  rgb(56, 90, 117)   深蓝
#6192b5  rgb(97, 146, 181)  中蓝
#98b4ce  rgb(152, 180, 206) 浅蓝
#eec0a3  rgb(238, 192, 163) 浅橙
#d2d0dc  rgb(210, 208, 220) 中性紫灰
#f2d9be  rgb(242, 217, 190) 米黄
#f0e4d2  rgb(240, 228, 210) 米白
#f4f6f1  rgb(244, 246, 241) 灰白
```
用途：correlation matrix / attention map / expression heatmap。

## Palette 3 — 亮色+浅色 tone-pair（每类一深一浅，配对使用）

深色：
```
#22BDD2  cyan
#1B78B2  blue
#9368AB  purple
#F47F1E  orange
#2DA248  green
#A2D94D  lime
#72D3D4  teal
#859ED7  slate
#8F69C5  violet
```
浅色（同色系 20% opacity 效果）：
```
#D0F0F2  #CDD9EC  #E4D8F2  #FCE1C9  #D7FADB
#EBF6DC  #E4F5F8  #E8ECF8  #E7E2F2
```

## Palette 4 — Nature medicine / genetics 风（严格科研色）

```
#009E74  绿  #C0E7DA (浅)
#0073B1  深蓝 #BEDCED (浅)
#57B4E9  中蓝 #D2ECFA (浅)
#D26101  深橙 #E5B893 (浅)
#E59F05  中橙 #F6E3BA (浅)
#F3C80D  金黄 #F9F0C6 (浅)
```

## Palette 5 — 红/橙/蓝/深蓝（bar plot 分组）

```
#C93735  红   #E59693 (浅)
#F8AB61  橙   #FCD7AF (浅)
#78A9CD  蓝   #BBD5E7 (浅)
#333A8C  深蓝 #989CC8 (浅)
```

## Palette 6 — 大类彩色（8 个明显区分色，多类比较）

```
#E68600  橙    #2CA8A2  青
#3E7EBF  蓝    #C1272D  红
#6E3FA3  紫    #4CAF50  绿
#CDBE91  卡其  #9E9E9E  灰
```

## Palette 7 — UMAP/tSNE 蓝绿色系（8 色，可用于 excitatory neuron 等主类）

```
#a4cde1  浅蓝    #67a4cc  中蓝
#277fb8  深蓝    #549da3  蓝绿
#96cb8f  中绿    #8bc96d  黄绿
#4dae47  深绿    #5c9e43  橄榄绿
```

## Palette 8 — UMAP/tSNE 红橙系（9 色，可用于 inhibitory 或 warm-tone 类别）

```
#b79973  卡其    #f38989  柔红    #ec5051  中红
#e32427  深红    #ef6a45  橙红    #f9b769  柔橙
#f9a341  深橙    #f48521  火橙    #ee8e46  砖橙
```

## Palette 9 — UMAP/tSNE 紫土系（8 色，第三类主色）

```
#d4a6a8  灰粉    #af93c4  柔紫    #8660a8  中紫
#815e99  深紫    #c6b598  卡其    #f6f28f  奶黄
#d4a55b  金土    #b05a28  棕土
```

**UMAP/tSNE 用色建议**：3 组（Palette 7+8+9）共 25 色，能覆盖大多数
single-cell atlas 的类别数。每主类用同色系（7 excitatory / 8 inhibitory /
9 vasculature 等），亚型内深浅区分。

---

## 硬规矩

### 1. 字体：一律 Times New Roman（serif）

```python
import matplotlib as mpl
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = ["Times New Roman", "Liberation Serif", "Times",
                              "STIXGeneral", "DejaVu Serif", "serif"]
mpl.rcParams["mathtext.fontset"] = "stix"   # 数学符号也用 Times 风
```

不用 Arial / Helvetica / DejaVu Sans。渲染机器常常没有 Times，matplotlib 会
**静默回退**，所以 `Liberation Serif`（与 Times 度量兼容）必须排在 DejaVu 前面。

### 2. 单栏 vs 双栏尺寸

| Journal | Single column | Double column |
|---|---|---|
| Nature | 89 mm (3.5 in) | 183 mm (7.2 in) |
| Science | 55 mm (2.17 in) | 111 mm (4.37 in) |
| Cell | 85 mm (3.35 in) | 174 mm (6.85 in) |
| ICLR/NeurIPS | ≈ 5.5 in | ≈ 7.0 in（跨栏 full-width）|

设图尺寸时**先决定放单栏还是双栏**，并且**在最终打印宽度上作图**，字号才能配得上。

### 3. 字号：接近正文或略小

正文常 10-11pt。图内字号：
- axes label / tick label / legend text：**8-9pt**
- panel letter (A/B/C)：**10-11pt bold**
- caption：正文字号即可

**避免**：图内字号大于正文（视觉粗糙）；或小于 6pt（印刷读不清）。

### 4. 组合口径（顶刊底 rcParams）

见根目录 `figure_style.py` 的 `apply_style()`，它就是下面这套：

```python
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "Times",
                   "STIXGeneral", "DejaVu Serif", "serif"],
    "mathtext.fontset": "stix",
    "font.size": 8, "axes.labelsize": 9, "axes.titlesize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "figure.dpi": 300, "savefig.dpi": 300,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,       # embed truetype
    "svg.fonttype": "none",
})
```

## 通用 style 原则（顶刊图共性）

1. **低饱和优先**：avoid neon / pure primary，用 muted 或 pastel，saturation
   约 40-60% 最舒服。
2. **一 finding 一 panel**：不要合并太多；顶刊图常见 8-12 panel，每 panel 极简。
3. **数字直接标在数据点上**：柱顶写值、`n=X`，别让读者去 legend 查。
4. **P-value 直接标在 comparison bracket 上**（`P = 0.010` / `P < 0.001`），
   不用 `*/**/***`，除非 space 紧。
5. **Error bar 用 shaded region**（时间序列）或 whisker（分类）；均值用实线。
6. **legend 极简**：外置色 chip + 名字，不加 box。
7. **字号 7-9pt 统一**；不同 panel 之间字号一致。
8. **grid line 去掉**：只留 axes；除非科学上需要（threshold line 用 dashed）。
9. **Hollow marker with fill** 用于两 tone 对比（如 before hollow vs after filled）。
10. **Diverging heatmap 用蓝-白-橙**（zero-centered），不要蓝-黑-红那种老 style。
11. **marker 序列**：`o`(圆) `s`(方) `^`(三角) `D`(菱形) `v`(倒三角) `P`(填十字)
    —— 圆最优先，形状按视觉重量降级。
12. **每个 panel 单独 sub-caption**：`(a)` `(b)` 用 bold + 简短短语。
