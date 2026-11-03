#!/usr/bin/env python3
"""Layout 1 - full-page time-course panel.

Panel geometry matches the canonical full-page journal layout one-for-one:
  a      two framed raster panels, shared legend centred above
  b      five cumulative-curve panels, coloured two-line titles
  c      five binned-area panels
  d-k    eight paired-box panels; f and j are four-box grouped panels with
         sub-group rules and three brackets, the rest are two-box
Axis limits, tick sets, label line counts and label lengths follow the
reference; the series are synthetic.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch, Rectangle

from _layout_common import HERE, apply_style, TXT, GREY

apply_style()
rng = np.random.default_rng(7)

EV1, EV2 = "#2FC4D8", "#B33A32"          # the two event types
GROUPS = ("Control", "Treated")
SUBSITES = ("Treated site", "Control site")

# (title, colour, y-max, y-ticks) - five series, titles wrap exactly as the
# reference does: short, short, two-line, two-line, two-line
SERIES = [
    ("Exploration",                   "#4C9BD5", 150, [0, 50, 100, 150]),
    ("General behaviour",             "#2FC4D8", 200, [0, 50, 100, 150, 200]),
    ("Targeted behaviour\nat site A",  "#9E2B25",  40, [0, 10, 20, 30, 40]),
    ("Behaviour at\ncontrol site B",   "#E8A33D",  10, [0, 5, 10]),
    ("General and targeted\nbehaviour","#6B4C9A", 250, [0, 50, 100, 150, 200, 250]),
]
# binned-area panel ranges, panel for panel
AREA = [(80, [0, 20, 40, 60, 80]), (50, [0, 10, 20, 30, 40, 50]),
        (20, [0, 5, 10, 15, 20]), (50, [0, 10, 20, 30, 40, 50]),
        (60, [0, 20, 40, 60])]


def letter(ax, s, dx, dy=1.14):
    ax.text(dx, dy, s, transform=ax.transAxes, fontsize=10.5,
            fontweight="bold", va="top", ha="left")


def letter_fig(fig, ax, s, pad_x=0.048, pad_y=0.013):
    """Panel letter anchored to the axes box, in figure coordinates."""
    fig.canvas.draw()
    bb = ax.get_position()
    fig.text(bb.x0 - pad_x, bb.y1 + pad_y, s, fontsize=10.5,
             fontweight="bold", va="bottom", ha="left")


def bracket(ax, x1, x2, y, text, size=8.0):
    h = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.030
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=0.8, c=TXT)
    ax.text((x1 + x2) / 2, y + h * 0.85, text, ha="center", va="bottom",
            fontsize=size, color=TXT)


def paired_box(ax, pos, lo, hi, face, n=20):
    v = np.maximum(0, rng.normal(lo, lo * 0.45, n))
    w = np.maximum(0, v * hi + rng.normal(0, lo * 0.5, n))
    bp = ax.boxplot([v, w], positions=pos, widths=0.52, patch_artist=True,
                    showfliers=False, medianprops=dict(color=TXT, lw=1.1),
                    whiskerprops=dict(color=TXT, lw=0.8),
                    capprops=dict(color=TXT, lw=0.8),
                    boxprops=dict(edgecolor=TXT, lw=0.8))
    bp["boxes"][0].set_facecolor(GREY); bp["boxes"][1].set_facecolor(face)
    for i in range(n):
        ax.plot(pos, [v[i], w[i]], color="#C9C9C9", lw=0.45, zorder=1)


fig = plt.figure(figsize=(7.2, 8.9))
gs = GridSpec(5, 20, figure=fig, height_ratios=[0.92, 1.00, 1.00, 1.16, 1.16],
              hspace=0.95, wspace=3.1,
              left=0.085, right=0.985, top=0.935, bottom=0.072)

# ── a: two framed raster panels ───────────────────────────────────────────
for k, (gname, dens) in enumerate([(GROUPS[0], 0.28), (GROUPS[1], 1.0)]):
    ax = fig.add_subplot(gs[0, (0 if k == 0 else 10):(9 if k == 0 else 19)])
    for row in range(6):
        for col, rate in [(EV1, 1.6 * dens), (EV2, 0.62 * dens)]:
            n = rng.poisson(rate * 9)
            for x, w in zip(rng.uniform(0, 30, n),
                            rng.uniform(0.12, 0.8, n) * (1.4 if dens > .5 else .8)):
                ax.add_patch(Rectangle((x, row + 0.08), w, 0.84, color=col, lw=0))
    ax.set_xlim(0, 30); ax.set_ylim(0, 6)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30]); ax.set_yticks([])
    ax.set_xlabel("Time (min)")
    ax.set_ylabel(gname, fontsize=8.5)
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_linewidth(0.8)
    if k == 0:
        letter(ax, "a", dx=-0.115, dy=1.22)
        ax.legend(handles=[Patch(facecolor=EV1, label="General behaviour I"),
                           Patch(facecolor=EV2, label="Targeted behaviour II")],
                  frameon=False, ncol=2, fontsize=8, handlelength=1.2,
                  columnspacing=1.6, loc="lower left", bbox_to_anchor=(0.30, 1.06))

# ── b: five cumulative-curve panels ───────────────────────────────────────
t = np.linspace(0, 30, 160)
for i, (name, col, ymax, yt) in enumerate(SERIES):
    ax = fig.add_subplot(gs[1, i * 4:i * 4 + 4])
    for c, top in [(col, ymax * 0.80), (GREY, ymax * 0.80 * 0.28)]:
        tau = 7.5 if ymax > 80 else 11
        m = top * (1 - np.exp(-t / tau))
        m = m + np.r_[0, np.cumsum(rng.normal(0, 0.45, t.size - 1))] * 0.35
        sd = np.maximum(ymax * 0.012, 0.12 * m + ymax * 0.012)
        ax.plot(t, m, color=c, lw=1.3)
        ax.fill_between(t, m - sd, m + sd, color=c, alpha=0.20, lw=0)
    ax.set_xlim(0, 30); ax.set_ylim(0, ymax)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_xticklabels(["0", "", "10", "", "20", "", "30"])
    ax.set_yticks(yt); ax.tick_params(labelsize=7)
    ax.set_title(name, color=col, fontsize=7.8, fontweight="bold", pad=3)
    if i == 0:
        ax.set_ylabel("Cumulative duration (s)", fontsize=7.8)
        letter(ax, "b", dx=-0.52, dy=1.30)

# ── c: five binned-area panels ────────────────────────────────────────────
tb = np.linspace(0, 30, 60)
for i, ((name, col, _, _), (ymax, yt)) in enumerate(zip(SERIES, AREA)):
    ax = fig.add_subplot(gs[2, i * 4:i * 4 + 4])
    peak = ymax * 0.56
    y1 = peak * (np.exp(-((tb - 8) / 4.5) ** 2) + 0.86 * np.exp(-((tb - 23) / 3.8) ** 2))
    y1 = np.maximum(0, y1 + rng.normal(0, peak * 0.07, tb.size))
    y0 = np.maximum(0, y1 * rng.uniform(0.15, 0.32) + rng.normal(0, peak * 0.03, tb.size))
    ax.fill_between(tb, 0, y1, color=col, alpha=0.55, lw=0.8, edgecolor=col)
    ax.fill_between(tb, 0, y0, color=GREY, alpha=0.55, lw=0.8, edgecolor=GREY)
    ax.set_xlim(0, 30); ax.set_ylim(0, ymax)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_xticklabels(["0", "", "10", "", "20", "", "30"])
    ax.set_yticks(yt); ax.tick_params(labelsize=7)
    ax.set_xlabel("Time (min)", fontsize=7.5)
    if i == 0:
        ax.set_ylabel("Behaviour time (s)\nper 5 min", fontsize=7.8)
        letter(ax, "c", dx=-0.52, dy=1.16)

# ── d-k: eight paired-box panels (f and j are four-box grouped) ───────────
#   label, y-max, y-ticks, colour, effect, star(s), grouped?
PANELS = [
    ("Exploration (s)",                      250, [0, 50, 100, 150, 200, 250],
     "#4C9BD5", 1.35, "*",   False),
    ("General behaviour (s)",                500, [0, 100, 200, 300, 400, 500],
     "#2FC4D8", 3.10, "**",  False),
    ("Targeted behaviour (s)",               150, [0, 50, 100, 150],
     "#E86A60", 3.40, "**",  True),
    ("General + targeted\nbehaviour (s)",    600, [0, 200, 400, 600],
     "#6B4C9A", 3.00, "***", False),
    ("Bouts of exploration",                 100, [0, 50, 100],
     "#4C9BD5", 1.50, "***", False),
    ("Bouts of general behaviour",            60, [0, 20, 40, 60],
     "#2FC4D8", 2.60, "**",  False),
    ("Bouts of targeted behaviour",           15, [0, 5, 10, 15],
     "#E86A60", 3.00, "***", True),
    ("Bouts of general + targeted\nbehaviour", 80, [0, 20, 40, 60, 80],
     "#6B4C9A", 2.70, "***", False),
]
for j, (ylab, ymax, yt, col, fold, star, grouped) in enumerate(PANELS):
    r, c = divmod(j, 4)
    SPAN = [(0, 4), (4, 8), (8, 14), (14, 20)]      # d/e narrow, f wide, g wide
    ax = fig.add_subplot(gs[3 + r, SPAN[c][0]:SPAN[c][1]])
    if grouped:
        paired_box(ax, [0, 1], ymax * 0.10, fold, col)
        paired_box(ax, [2.4, 3.4], ymax * 0.055, fold * 0.55, "#F5C98E")
        ax.set_xlim(-0.75, 4.15)
        ax.set_xticks([0, 1, 2.4, 3.4])
        ax.set_xticklabels(list(GROUPS) * 2, fontsize=6.6)
        ax.set_ylim(0, ymax * 1.72)
        bracket(ax, 0, 1, ymax * 1.03, star, size=7.5)
        bracket(ax, 2.4, 3.4, ymax * 1.03, "ns", size=6.8)
        bracket(ax, 0.5, 2.9, ymax * 1.34, "ns", size=6.8)
        # sub-group rules under each pair, as the reference draws them
        for (x0, x1), lab, cc in zip([(0, 1), (2.4, 3.4)], SUBSITES,
                                     [col, "#D79A4A"]):
            tr = ax.get_xaxis_transform()      # x in data, y in axes fraction
            ax.plot([x0 - 0.35, x1 + 0.35], [-0.215] * 2, color=cc, lw=1.4,
                    transform=tr, clip_on=False)
            ax.text((x0 + x1) / 2, -0.245, lab, ha="center", va="top",
                    fontsize=6.2, color=cc, transform=tr, clip_on=False)
    else:
        paired_box(ax, [0, 1], ymax * 0.17, fold, col)
        ax.set_xlim(-0.7, 1.7)
        ax.set_xticks([0, 1]); ax.set_xticklabels(GROUPS, fontsize=7.0)
        ax.set_ylim(0, ymax * 1.30)
        bracket(ax, 0, 1, ymax * 1.03, star)
    ax.set_yticks(yt)
    ax.set_ylabel(ylab, fontsize=7.4)
    ax.tick_params(labelsize=7)
    letter_fig(fig, ax, "defghijk"[j])

fig.savefig(os.path.join(HERE, "layout1_timecourse_panel.png"), dpi=200)
print("wrote layout1_timecourse_panel.png")
