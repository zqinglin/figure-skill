---
name: figure-skill
description: "Make publication-quality figures for papers (Nature / Science / Cell / ICLR / NeurIPS). Use whenever drawing a chart, plot, or figure panel for a paper, or choosing its colors, size, fonts, or chart type. Supplies journal-grade color palettes, the mandatory matplotlib rcParams (Times serif, 8-9pt type, column widths, 300 dpi, embedded fonts), a data-shape to chart-type decision guide across 15 chart families, and a ready-to-import matplotlib style module."
---

# figure-skill — publication figures that read as one system

A figure reads as amateur or professional before a reviewer parses a single
number: the font, the type size relative to the body text, the color choices,
and whether the chart type fits the data. This skill fixes all four so every
panel in a paper looks like it came from the same lab.

Three things live here:

1. **`figure_style.py`** — import it and call `apply_style()` at the top of
   every plotting script. It sets the mandatory rcParams and gives you named,
   CVD-safe palettes and the correct figure widths.
2. **`references/palettes.md`** — 9 journal-grade color palettes (soft
   pastel, blue-orange diverging, tone-pairs, Nature-genetics, bar groups,
   many-category, and three UMAP/tSNE ramps) plus the universal style rules.
3. **`references/chart-selection.md`** — "what data uses what chart": a
   data-shape cheat sheet and 15 chart families, each with when to use it,
   when not to, and the specific trap that breaks it.
4. **`references/examples/`** — the gallery: four full-page layout
   reproductions (time-course page, eight-panel collage, projection atlas,
   one-chart-five-palettes), ten single-chart examples, and the 16:9 banner.
   All original, synthetic data, regenerable. Use them as visual targets —
   match the panel structure, then swap in your data.

## The hard rules (do these every time)

These are non-negotiable; they are what separates a top-journal figure from a
default-matplotlib one.

### 1. Font: serif, Times-compatible, always

```python
import matplotlib as mpl
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = ["Times New Roman", "Liberation Serif", "Times",
                              "STIXGeneral", "DejaVu Serif", "serif"]
mpl.rcParams["mathtext.fontset"] = "stix"   # math symbols in a Times-like face
```

Never Arial / Helvetica / DejaVu Sans. On machines without Times installed,
matplotlib falls back **silently** — `Liberation Serif` (metric-compatible)
must precede `DejaVu` in the chain or your panels quietly ship in the wrong
font.

### 2. Decide single- vs double-column *first*, then size

| Journal | Single column | Double column |
|---|---|---|
| Nature | 89 mm (3.5 in) | 183 mm (7.2 in) |
| Science | 55 mm (2.17 in) | 111 mm (4.37 in) |
| Cell | 85 mm (3.35 in) | 174 mm (6.85 in) |
| ICLR / NeurIPS | ≈ 5.5 in (\textwidth) | ≈ 7.0 in (full-width) |

Author the figure **at its final printed width**. `\includegraphics[width=\textwidth]`
on a figure drawn at 13 in scales it — and its fonts — down by ~0.42, so your
9pt labels reach the page at under 4pt. Drawing at the final width makes the
type sizes below mean what they say.

### 3. Type size: at or just below body text

Body is usually 10-11pt. Inside the figure:
- axis labels / ticks / legend text: **8-9pt**
- panel letters (A/B/C): **10-11pt bold**
- never larger than body text (reads coarse), never below 6pt (prints illegibly)

### 4. The combined rcParams "top-journal base"

`figure_style.apply_style()` applies exactly this:

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
    "pdf.fonttype": 42,     # embed TrueType, not Type-3 bitmaps
    "svg.fonttype": "none",
})
```

## Universal style principles

1. **Low saturation first** — avoid neon / pure primaries; muted or pastel
   (~40-60% saturation) reads best.
2. **One finding, one panel** — top-journal figures run 8-12 minimal panels,
   not a few crowded ones.
3. **Write values on the data** — put the number on the bar top, `n = X` on
   the point; don't send the reader to the legend.
4. **P-values on the comparison bracket** (`P = 0.010` / `P < 0.001`), not
   `*/**/***`, unless space is tight.
5. **Error as shaded region** (time series) or whisker (categorical); mean as
   a solid line.
6. **Minimal legend** — color chip + name, no box; prefer labelling data in place.
7. **Consistent type sizes across panels** — 7-9pt everywhere.
8. **Kill grid lines** — keep only the axes, unless a threshold line is
   scientifically needed (then dashed).
9. **Hollow-vs-filled markers** for two-tone contrast (e.g. before/after).
10. **Diverging heatmaps blue-white-orange** (zero-centered), never blue-black-red.
11. **Marker priority** `o s ^ D v P` — circle first, shapes degrade by
    visual weight.
12. **Per-panel sub-captions** `(a) (b)` in bold + a short phrase.

## Workflow

1. `from figure_style import apply_style, WIDTH_FULL, CS_PEER_PALETTE, ...`
2. `apply_style()` once at the top.
3. Pick the chart type from `references/chart-selection.md` by your data shape.
4. Pick colors from `references/palettes.md` (or the named palettes in the module).
5. Draw at `WIDTH_FULL` / `WIDTH_HALF`.
6. Save as PDF (vector). **Then rasterize and eyeball it** before shipping —
   silent font fallback and clipped labels only show up in the rendered page.

## Rules of thumb for what *not* to do

- No pie charts in papers (unless ≤5 clear proportions differing by >10%).
- No 3D charts (visual distortion).
- No rainbow colormaps (not perceptually uniform, CVD-hostile).
- Don't let a narrow secondary-axis range manufacture a fake trend — set the
  range from zero or the real possible span and ask if the line still moves.
