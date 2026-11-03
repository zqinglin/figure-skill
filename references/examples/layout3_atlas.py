#!/usr/bin/env python3
"""Layout 3 - 2-D projection atlas.

Main projection + sorted count bar + two zoomed sub-population projections with
long labelled count lists + three small projections: the standard atlas layout.
Synthetic point clouds, generic cluster names.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.lines import Line2D

from _layout_common import (HERE, apply_style, TXT, BAR_EDGE, letter, stamp)

apply_style()
rng = np.random.default_rng(5)

# Palettes 7 / 8 / 9 (see ../palettes.md)
P7 = ["#a4cde1", "#67a4cc", "#277fb8", "#549da3", "#96cb8f", "#8bc96d",
      "#4dae47", "#5c9e43"]
P8 = ["#f38989", "#ec5051", "#e32427", "#ef6a45", "#f9b769", "#f9a341",
      "#f48521", "#b79973"]
P9 = ["#d4a6a8", "#af93c4", "#8660a8", "#815e99", "#c6b598", "#d4a55b",
      "#b05a28", "#f6f28f"]

TOP = ["Type A", "Type B", "Type C", "Type D", "Type E", "Type F", "Type G"]
TOP_COL = [P7[2], P9[2], P7[6], P8[3], P8[5], "#22BDD2", P9[5]]
TOP_N = [1043230, 528699, 92502, 88558, 83689, 45142, 17974]


def blob(ax, centre, n, col, spread=0.9, label=None, rot=0):
    pts = rng.normal(centre, spread, (n, 2))
    ax.scatter(pts[:, 0], pts[:, 1], s=1.6, color=col, alpha=0.55,
               linewidths=0, rasterized=True)
    if label:
        ax.text(centre[0], centre[1] + spread * 2.1, label, fontsize=6.0,
                ha="center", va="bottom", color=TXT, rotation=rot)


def grid_centres(k, half=4.0, jitter=0.35, seed=0, cols=None):
    """Jittered grid so cluster labels never land on top of each other."""
    r = np.random.default_rng(seed)
    cols = cols or int(np.ceil(np.sqrt(k)))
    rows = int(np.ceil(k / cols))
    xs = np.linspace(-half, half, cols)
    ys = np.linspace(half, -half, rows)
    pts = [(xs[i % cols], ys[i // cols]) for i in range(k)]
    return np.array(pts) + r.uniform(-jitter, jitter, (k, 2))


def clean(ax, title=None):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if title:
        ax.set_title(title, fontsize=7, pad=2,
                     bbox=dict(facecolor="#EFEFEF", edgecolor="none",
                               boxstyle="round,pad=0.25"))


def count_list(ax, names, counts, cols, xlabel="Number of points"):
    y = np.arange(len(names))[::-1]
    total = sum(counts)
    ax.barh(y, counts, color=cols, height=0.72, **BAR_EDGE)
    for yy, c in zip(y, counts):
        ax.text(c + max(counts) * 0.02, yy, f"{c:,} ({c/total*100:.1f}%)",
                va="center", fontsize=5.2, color=TXT)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=5.4)
    ax.set_xlim(0, max(counts) * 1.55)
    ax.set_xlabel(xlabel, fontsize=6.4)
    ax.tick_params(axis="x", labelsize=5.8)
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax.xaxis.get_offset_text().set_fontsize(5.4)


fig = plt.figure(figsize=(7.2, 6.4))
gs = GridSpec(3, 12, figure=fig, height_ratios=[1.25, 0.95, 0.95],
              hspace=0.55, wspace=1.5,
              left=0.055, right=0.985, top=0.94, bottom=0.07)

# ── D: main projection ────────────────────────────────────────────────────
axD = fig.add_subplot(gs[0, 0:5])
cent = np.array([[-3.2, 2.4], [1.8, -2.6], [-1.0, 4.6], [3.4, 2.0],
                 [4.6, -0.4], [-4.4, -1.8], [0.4, 0.6]])
for c, col, nm, n in zip(cent, TOP_COL, TOP, TOP_N):
    blob(axD, c, max(150, n // 1800), col, spread=1.15, label=nm)
clean(axD, "Projection of all points (2,359,994)")
axD.legend(handles=[Line2D([], [], marker="o", ls="", color=c, label=n, ms=3.4)
                    for n, c in zip(TOP, TOP_COL)],
           frameon=False, fontsize=5.6, loc="center left",
           bbox_to_anchor=(1.0, 0.5), handlelength=0.8, labelspacing=0.35)
letter(axD, "D", dx=-0.07, dy=1.10)

# ── F: sub-population I projection + long count list ──────────────────────
axF = fig.add_subplot(gs[0, 6:9])
SUB1 = [f"Group {i}" for i in range(1, 13)]
SUB1_COL = (P7 + P8)[:12]
SUB1_N = sorted((rng.uniform(0.1, 1.0, 12) ** 2 * 300000).astype(int))[::-1]
sc = grid_centres(12, half=3.0, seed=31, cols=3)
for c, col, nm in zip(sc, SUB1_COL, SUB1):
    blob(axF, c, 200, col, spread=0.40, label=nm)
clean(axF, "Sub-population I")
letter(axF, "F", dx=-0.12, dy=1.10)

axFb = fig.add_subplot(gs[0, 9:12])
count_list(axFb, SUB1, SUB1_N, SUB1_COL)

# ── E: sorted count bar for the main types ────────────────────────────────
axE = fig.add_subplot(gs[1, 0:4])
count_list(axE, TOP, TOP_N, TOP_COL)
letter(axE, "E", dx=-0.30, dy=1.16)

# ── G: sub-population II projection + long count list ─────────────────────
axG = fig.add_subplot(gs[1:3, 5:8])
SUB2 = [f"Group {i}" for i in range(13, 27)]
SUB2_COL = (P9 + P8)[:14]
SUB2_N = sorted((rng.uniform(0.1, 1.0, 14) ** 2 * 60000).astype(int))[::-1]
sc2 = grid_centres(14, half=3.1, seed=32, cols=3)
for c, col, nm in zip(sc2, SUB2_COL, SUB2):
    blob(axG, c, 130, col, spread=0.34, label=nm)
clean(axG, "Sub-population II")
letter(axG, "G", dx=-0.12, dy=1.07)

axGb = fig.add_subplot(gs[1:3, 8:12])
count_list(axGb, SUB2, SUB2_N, SUB2_COL)

# ── H, I, J: small projections ────────────────────────────────────────────
subHIJ = GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[2, 0:5], wspace=0.45)
DETAILS = [("H", ["Sub 1", "Sub 2", "Sub 3"], [P7[4], P7[6], P7[1]]),
           ("I", ["Sub 4", "Sub 5", "Sub 6"], [P8[1], P8[4], P9[2]]),
           ("J", ["Sub 7", "Sub 8", "Sub 9"], [P9[1], P9[5], P7[3]])]
for k, (lab, names, cols) in enumerate(DETAILS):
    ax = fig.add_subplot(subHIJ[k])
    for c, (nm, col) in zip(grid_centres(3, half=1.6, seed=40 + k, cols=2),
                            zip(names, cols)):
        blob(ax, c, 150, col, spread=0.42, label=nm)
    clean(ax, f"Detail {lab}")
    letter(ax, lab, dx=-0.18, dy=1.14)

stamp(fig)
fig.savefig(os.path.join(HERE, "layout3_atlas.png"), dpi=200)
print("wrote layout3_atlas.png")
