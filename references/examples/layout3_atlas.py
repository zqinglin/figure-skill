#!/usr/bin/env python3
"""Layout 3 - 2-D projection atlas.

Main projection + sorted count bar + two sub-population projections with
labelled count lists + three detail projections.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

from _layout_common import HERE, apply_style, TXT, BAR_EDGE, letter

apply_style()
rng = np.random.default_rng(5)

P7 = ["#a4cde1", "#67a4cc", "#277fb8", "#549da3", "#96cb8f", "#8bc96d",
      "#4dae47", "#5c9e43"]
P8 = ["#f38989", "#ec5051", "#e32427", "#ef6a45", "#f9b769", "#f9a341",
      "#f48521", "#b79973"]
P9 = ["#d4a6a8", "#af93c4", "#8660a8", "#815e99", "#c6b598", "#d4a55b",
      "#b05a28", "#f6f28f"]

TOP = ["Type A", "Type B", "Type C", "Type D", "Type E", "Type F", "Type G"]
TOP_COL = [P7[2], P9[2], P7[6], P8[3], P8[5], "#22BDD2", P9[5]]
TOP_N = [1043230, 528699, 92502, 88558, 83689, 45142, 17974]


def cloud(n, scale, seed, bend=0.35, aniso=(1.0, 0.45)):
    """An organic cluster: anisotropic, rotated, slightly bent."""
    r = np.random.default_rng(seed)
    sx, sy = aniso
    p = np.c_[r.normal(0, sx, n), r.normal(0, sy, n)]
    # bend along the long axis so the shape is not a plain ellipse
    p[:, 1] += bend * (p[:, 0] ** 2 - sx ** 2) / max(sx, 1e-6)
    # a thin tail on some clusters, which is what makes projections look real
    k = n // 6
    if k:
        t = r.uniform(0, 1, k)
        p[:k, 0] = p[:k, 0] * 0.3 + sx * 1.6 * t
        p[:k, 1] = p[:k, 1] * 0.3 + bend * sx * 1.4 * t ** 2
    th = r.uniform(0, 2 * np.pi)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return (p @ R.T) * scale


def scatter_layout(k, half, seed, min_sep):
    """Non-grid placement: random with a minimum-separation rejection."""
    r = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < k and tries < 20000:
        tries += 1
        c = r.uniform(-half, half, 2)
        if all(np.hypot(*(c - q)) >= min_sep for q in pts):
            pts.append(c)
    while len(pts) < k:                       # relax if packing was too tight
        pts.append(r.uniform(-half, half, 2))
    return np.array(pts)


def draw(ax, centres, cols, names, n_pts, scale, seed0, label_size=6.0,
         point_size=1.5, bend_rng=(0.15, 0.5)):
    r = np.random.default_rng(seed0 + 999)
    for i, (c, col, nm) in enumerate(zip(centres, cols, names)):
        bend = r.uniform(*bend_rng) * r.choice([-1, 1])
        aniso = (r.uniform(0.8, 1.3), r.uniform(0.30, 0.60))
        p = cloud(n_pts, scale * r.uniform(0.75, 1.25), seed0 + i,
                  bend=bend, aniso=aniso) + c
        ax.scatter(p[:, 0], p[:, 1], s=point_size, color=col, alpha=0.55,
                   linewidths=0, rasterized=True)
        # label sits on the cluster with a white halo, as atlas figures do,
        # so neighbouring labels can never collide into unreadable mush
        ax.text(np.median(p[:, 0]), np.median(p[:, 1]), nm,
                fontsize=label_size, ha="center", va="center", color="#1E1E1E",
                zorder=5,
                path_effects=[pe.withStroke(linewidth=1.8, foreground="white")])


def clean(ax, title=None):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.margins(0.08)
    if title:
        ax.set_title(title, fontsize=7, pad=2,
                     bbox=dict(facecolor="#EFEFEF", edgecolor="none",
                               boxstyle="round,pad=0.25"))


def count_list(ax, names, counts, cols, fs=5.4):
    y = np.arange(len(names))[::-1]
    total = sum(counts)
    ax.barh(y, counts, color=cols, height=0.74, **BAR_EDGE)
    for yy, c in zip(y, counts):
        ax.text(c + max(counts) * 0.02, yy, f"{c:,} ({c/total*100:.1f}%)",
                va="center", fontsize=fs - 0.2, color=TXT)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=fs)
    ax.set_xlim(0, max(counts) * 1.52)
    ax.set_xlabel("Number of points", fontsize=6.4)
    ax.tick_params(axis="x", labelsize=5.8)
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax.xaxis.get_offset_text().set_fontsize(5.4)


fig = plt.figure(figsize=(7.2, 5.9))
gs = GridSpec(3, 12, figure=fig, height_ratios=[1.30, 0.86, 0.86],
              hspace=0.42, wspace=1.25,
              left=0.050, right=0.985, top=0.945, bottom=0.075)

# ── D: main projection ────────────────────────────────────────────────────
axD = fig.add_subplot(gs[0, 0:5])
draw(axD, scatter_layout(7, 3.1, 11, 2.5), TOP_COL, TOP,
     n_pts=1400, scale=1.05, seed0=100, label_size=6.6, point_size=1.1)
clean(axD, "Projection of all points (2,359,994)")
axD.legend(handles=[Line2D([], [], marker="o", ls="", color=c, label=n, ms=3.2)
                    for n, c in zip(TOP, TOP_COL)],
           frameon=False, fontsize=5.6, loc="center left",
           bbox_to_anchor=(0.99, 0.5), handlelength=0.8, labelspacing=0.30)
letter(axD, "D", dx=-0.06, dy=1.10)

# ── F: sub-population I + count list ──────────────────────────────────────
SUB1 = [f"Group {i}" for i in range(1, 13)]
SUB1_COL = (P7 + P8)[:12]
SUB1_N = sorted((rng.uniform(0.1, 1.0, 12) ** 2 * 300000).astype(int))[::-1]
axF = fig.add_subplot(gs[0, 6:9])
draw(axF, scatter_layout(12, 3.3, 12, 1.75), SUB1_COL, SUB1,
     n_pts=420, scale=0.52, seed0=200, label_size=5.2, point_size=1.0)
clean(axF, "Sub-population I")
letter(axF, "F", dx=-0.11, dy=1.10)
count_list(fig.add_subplot(gs[0, 9:12]), SUB1, SUB1_N, SUB1_COL)

# ── E: sorted counts for the main types ───────────────────────────────────
axE = fig.add_subplot(gs[1, 0:4])
count_list(axE, TOP, TOP_N, TOP_COL, fs=6.0)
letter(axE, "E", dx=-0.28, dy=1.18)

# ── G: sub-population II + count list ─────────────────────────────────────
SUB2 = [f"Group {i}" for i in range(13, 27)]
SUB2_COL = (P9 + P8)[:14]
SUB2_N = sorted((rng.uniform(0.1, 1.0, 14) ** 2 * 60000).astype(int))[::-1]
axG = fig.add_subplot(gs[1:3, 5:8])
draw(axG, scatter_layout(14, 3.5, 13, 1.60), SUB2_COL, SUB2,
     n_pts=330, scale=0.46, seed0=300, label_size=5.0, point_size=0.9)
clean(axG, "Sub-population II")
letter(axG, "G", dx=-0.11, dy=1.06)
count_list(fig.add_subplot(gs[1:3, 8:12]), SUB2, SUB2_N, SUB2_COL)

# ── H, I, J: detail projections ───────────────────────────────────────────
subHIJ = GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[2, 0:5], wspace=0.40)
DETAILS = [("H", ["Sub 1", "Sub 2", "Sub 3"], [P7[4], P7[6], P7[1]]),
           ("I", ["Sub 4", "Sub 5", "Sub 6"], [P8[1], P8[4], P9[2]]),
           ("J", ["Sub 7", "Sub 8", "Sub 9"], [P9[1], P9[5], P7[3]])]
for k, (lab, names, cols) in enumerate(DETAILS):
    ax = fig.add_subplot(subHIJ[k])
    draw(ax, scatter_layout(3, 1.5, 40 + k, 1.7), cols, names,
         n_pts=300, scale=0.44, seed0=400 + 10 * k, label_size=5.4,
         point_size=1.1)
    clean(ax, f"Detail {lab}")
    letter(ax, lab, dx=-0.16, dy=1.14)

fig.savefig(os.path.join(HERE, "layout3_atlas.png"), dpi=200)
print("wrote layout3_atlas.png")
