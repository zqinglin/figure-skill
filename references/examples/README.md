# Example gallery

Ten worked example figures, all **original** — synthetic data drawn only with
`figure_style.apply_style()` and the named palettes. They are visual targets:
this is what "publication-quality" looks like for each chart family in
`../chart-selection.md`, in the palettes of `../palettes.md`.

Regenerate (or re-render as vector PDF) with:

```bash
python3 make_examples.py
```

![gallery](gallery.png)

| File | Chart family | Palette | Shows |
|---|---|---|---|
| `ex1_paired_box_dots.png` | Paired box + dots | P1 soft pastel | two groups, per-subject connecting lines, significance bracket |
| `ex2_diverging_heatmap.png` | Heatmap | P2 blue–white–orange | zero-centered expression matrix, minimal colorbar |
| `ex3_line_shaded_ci.png` | Line + shaded CI | P5 / neutral | cumulative curve with ±SD band, not error bars |
| `ex4_raster.png` | Raster | teal + coral | event spans across trials, two behaviors |
| `ex5_bar_dots_pvalues.png` | Bar + individual dots | P6 many-category | means with dots, `n =` and P-value on a bracket |
| `ex6_tonepair_box.png` | Tone-pair box | P3 deep/light | hollow (prenatal) vs filled (postnatal), P per group |
| `ex7_radar.png` | Radar / spider | CVD-safe pair | two entities over 7 normalized dimensions |
| `ex8_umap_counts.png` | UMAP + count bar | P7 / P8 / P9 | 2-D projection with in-place labels + sorted counts |
| `ex9_stacked_double_axis.png` | Stacked bar + line | P1 + P5 navy | composition drift (left) vs result metric (right) |
| `ex10_beeswarm.png` | Beeswarm | P3 deep | per-point distribution with median line, by group |

These replace redistributing third-party journal figures: the palettes and
layout conventions were learned from published top-journal panels, but every
pixel here is generated from `make_examples.py`, so the gallery is free to
share. Swap the synthetic data for yours and keep the styling.
