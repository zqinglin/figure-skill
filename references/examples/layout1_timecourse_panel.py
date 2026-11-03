#!/usr/bin/env python3
"""Layout 1 - full-page time-course panel.

Panel structure (raster pair -> cumulative curves -> binned area -> paired
boxes) follows the standard full-page journal layout. All series are synthetic
and generically named: this is a style template, not a result.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch, Rectangle

from _layout_common import (HERE, apply_style, TXT, GREY, letter, bracket, stamp)

apply_style()
rng = np.random.default_rng(7)

SERIES = [("Series 1", "#3E7EBF", 130, 150),
          ("Series 2", "#22BDD2", 170, 200),
          ("Series 3", "#A4342B", 36, 40),
          ("Series 4", "#E8A33D", 10, 12),
          ("Series 5", "#6E3FA3", 195, 250)]
GROUPS = ("Condition A", "Condition B")

fig = plt.figure(figsize=(7.2, 8.6))
gs = GridSpec(5, 20, figure=fig,
              height_ratios=[1.00, 1.05, 1.05, 1.15, 1.15],
              hspace=1.05, wspace=3.4,
              left=0.075, right=0.985, top=0.945, bottom=0.055)

# ── a: paired raster panels ───────────────────────────────────────────────
for k, (gname, dens) in enumerate([(GROUPS[0], 0.30), (GROUPS[1], 1.0)]):
    ax = fig.add_subplot(gs[0, (0 if k == 0 else 10):(9 if k == 0 else 19)])
    for row in range(6):
        for col, rate in [("#22BDD2", 1.5 * dens), ("#A4342B", 0.6 * dens)]:
            n = rng.poisson(rate * 9)
            xs = rng.uniform(0, 30, n)
            ws = rng.uniform(0.12, 0.75, n) * (1.4 if dens > 0.5 else 0.8)
            for x, w in zip(xs, ws):
                ax.add_patch(Rectangle((x, row + 0.08), w, 0.84, color=col, lw=0))
    ax.set_xlim(0, 30); ax.set_ylim(0, 6)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30]); ax.set_yticks([])
    ax.set_xlabel("Time (arb. units)")
    ax.set_ylabel(gname, fontsize=8.5)
    for sp in ("top", "right"): ax.spines[sp].set_visible(True)
    for sp in ax.spines.values(): sp.set_linewidth(0.8)
    if k == 0:
        letter(ax, "a", dx=-0.13)
        ax.legend(handles=[Patch(facecolor="#22BDD2", label="Event type I"),
                           Patch(facecolor="#A4342B", label="Event type II")],
                  frameon=False, ncol=2, fontsize=7.5,
                  loc="lower left", bbox_to_anchor=(0.26, 1.04))

# ── b: cumulative curves + CI band, one per series ────────────────────────
t = np.linspace(0, 30, 160)
for i, (name, col, top_t, ymax) in enumerate(SERIES):
    ax = fig.add_subplot(gs[1, i * 4:i * 4 + 4])
    for c, top in [(col, top_t), (GREY, top_t * 0.30)]:
        tau = 7.5 if top > 80 else 11
        m = top * (1 - np.exp(-t / tau))
        m = m + np.r_[0, np.cumsum(rng.normal(0, 0.45, t.size - 1))] * 0.35
        sd = np.maximum(2.0, 0.12 * m + 2)
        ax.plot(t, m, color=c, lw=1.3)
        ax.fill_between(t, m - sd, m + sd, color=c, alpha=0.20, lw=0)
    ax.set_xlim(0, 30); ax.set_ylim(0, ymax)
    ax.set_xticks([0, 10, 20, 30]); ax.tick_params(labelsize=7)
    ax.set_title(name, color=col, fontsize=7.8, fontweight="bold", pad=3)
    if i == 0:
        ax.set_ylabel("Cumulative\nvalue (arb.)", fontsize=8)
        letter(ax, "b", dx=-0.46)

# ── c: binned area, one per series ────────────────────────────────────────
tb = np.linspace(0, 30, 60)
for i, (name, col, top_t, ymax) in enumerate(SERIES):
    ax = fig.add_subplot(gs[2, i * 4:i * 4 + 4])
    peak = ymax * 0.28
    y1 = peak * (np.exp(-((tb - 8) / 4.5) ** 2) + 0.85 * np.exp(-((tb - 23) / 3.8) ** 2))
    y1 = np.maximum(0, y1 + rng.normal(0, peak * 0.07, tb.size))
    y0 = np.maximum(0, y1 * rng.uniform(0.15, 0.35) + rng.normal(0, peak * 0.03, tb.size))
    ax.fill_between(tb, 0, y1, color=col, alpha=0.55, lw=0.8, edgecolor=col)
    ax.fill_between(tb, 0, y0, color=GREY, alpha=0.55, lw=0.8, edgecolor=GREY)
    ax.set_xlim(0, 30); ax.set_ylim(0, peak * 1.9)
    ax.set_xticks([0, 10, 20, 30]); ax.tick_params(labelsize=7)
    ax.set_xlabel("Time (arb. units)", fontsize=7.5)
    if i == 0:
        ax.set_ylabel("Value per bin\n(arb.)", fontsize=8)
        letter(ax, "c", dx=-0.46)

# ── d-k: paired boxes with per-unit connecting lines ──────────────────────
PANELS = [("Metric 1 (arb.)", 110, 1.35, "#3E7EBF"),
          ("Metric 2 (arb.)",  95, 3.10, "#22BDD2"),
          ("Metric 3 (arb.)",  26, 3.40, "#A4342B"),
          ("Metric 4 (arb.)", 140, 3.00, "#6E3FA3"),
          ("Count 1",          26, 1.50, "#3E7EBF"),
          ("Count 2",           8, 2.60, "#22BDD2"),
          ("Count 3",         2.2, 3.00, "#A4342B"),
          ("Count 4",          10, 2.70, "#6E3FA3")]
for j, (ylab, base, fold, col) in enumerate(PANELS):
    r, c = divmod(j, 4)
    ax = fig.add_subplot(gs[3 + r, c * 5:c * 5 + 5])
    n = 20
    v = np.maximum(0, rng.normal(base, base * 0.45, n))
    w = np.maximum(0, v * fold + rng.normal(0, base * 0.55, n))
    bp = ax.boxplot([v, w], positions=[0, 1], widths=0.52, patch_artist=True,
                    showfliers=False, medianprops=dict(color=TXT, lw=1.1),
                    whiskerprops=dict(color=TXT, lw=0.8),
                    capprops=dict(color=TXT, lw=0.8),
                    boxprops=dict(edgecolor=TXT, lw=0.8))
    bp["boxes"][0].set_facecolor(GREY); bp["boxes"][1].set_facecolor(col)
    for i in range(n):
        ax.plot([0, 1], [v[i], w[i]], color="#C9C9C9", lw=0.45, zorder=1)
    top = max(np.percentile(v, 95), np.percentile(w, 95))
    ax.set_ylim(0, top * 1.42)
    bracket(ax, 0, 1, top * 1.12, "comparison", size=6.4)
    ax.set_xticks([0, 1]); ax.set_xticklabels(GROUPS, fontsize=7.2)
    ax.set_ylabel(ylab, fontsize=7.6); ax.tick_params(labelsize=7)
    letter(ax, "defghijk"[j], dx=-0.26)

stamp(fig)
fig.savefig(os.path.join(HERE, "layout1_timecourse_panel.png"), dpi=200)
print("wrote layout1_timecourse_panel.png")
