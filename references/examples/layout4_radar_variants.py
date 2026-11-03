#!/usr/bin/env python3
"""Layout 4 - one radar, five palettes.

A hero radar over a 2x2 grid of palette variants, each in a titled box: the
standard "same chart, which palette" comparison layout. Two entities over seven
normalised dimensions.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from _layout_common import HERE, apply_style, TXT

apply_style()

DIMS = ["Dimension 1", "Dimension 2", "Dimension 3", "Dimension 4",
        "Dimension 5", "Dimension 6", "Dimension 7"]
TICKS = [[0.25, 0.5], [4, 8], [2, 4], [200, 400], [50, 100], [4, 8], [180, 360]]
HI = np.array([0.5, 8, 4.0, 400, 100, 8.0, 360])
A = np.array([0.42, 6.8, 2.1, 360, 70, 5.2, 300])   # Entity A
B = np.array([0.30, 4.0, 3.2, 150, 85, 6.8, 330])   # Entity B

VARIANTS = [
    ("Original palette",      "#2B2E6E", "#C2224B"),
    ("Journal standard",      "#22BDD2", "#F47F1E"),
    ("Purple / orange",       "#F38989", "#6E3FA3"),
    ("Perceptually uniform",  "#2CA8A2", "#6E9CC4"),
    ("CVD-safe",              "#0072B2", "#D55E00"),
]

ANG = np.linspace(0, 2 * np.pi, len(DIMS), endpoint=False)
ANG_C = np.r_[ANG, ANG[:1]]


def radar(ax, ca, cb, big):
    for v, c, name in [(A / HI, ca, "Entity A"), (B / HI, cb, "Entity B")]:
        vv = np.r_[v, v[:1]]
        ax.plot(ANG_C, vv, color=c, lw=1.9 if big else 1.1, label=name,
                solid_joinstyle="round")
        ax.fill(ANG_C, vv, color=c, alpha=0.17)
    ax.plot(ANG_C, np.ones_like(ANG_C), color="#555555", lw=1.0 if big else 0.7,
            ls=(0, (4, 2.5)))
    ax.set_xticks(ANG)
    ax.set_xticklabels(DIMS if big else ["" for _ in DIMS],
                       fontsize=8 if big else 5)
    ax.set_yticks([0.25, 0.5, 0.75]); ax.set_yticklabels([])
    ax.set_ylim(0, 1.0)
    ax.set_clip_on(False)
    ax.grid(color="#DCDCDC", lw=0.55)
    ax.spines["polar"].set_visible(False)
    ax.set_theta_offset(np.pi / 2)
    if big:
        for a, lab, hi in zip(ANG, DIMS, HI):
            ax.text(a, 0.94, f"{hi:g}", ha="center", va="center",
                    fontsize=7, fontweight="bold", color=TXT)
    else:
        for a, lab in zip(ANG, DIMS):
            ax.text(a, 1.15, lab.replace("Dimension ", "D"), ha="center",
                    va="center", fontsize=5.2, color=TXT)


def titled_box(fig, rect, title):
    """Light header bar + hairline frame, as in the comparison layout."""
    x0, y0, w, h = rect
    fig.patches.append(plt.Rectangle((x0, y0), w, h, transform=fig.transFigure,
                                     facecolor="none", edgecolor="#C8C8C8",
                                     lw=0.8, zorder=0))
    fig.patches.append(plt.Rectangle((x0, y0 + h - 0.028), w, 0.028,
                                     transform=fig.transFigure,
                                     facecolor="#EFEFEF", edgecolor="#C8C8C8",
                                     lw=0.8, zorder=0))
    fig.text(x0 + w / 2, y0 + h - 0.0145, title, ha="center", va="center",
             fontsize=7.6, color=TXT, zorder=1)


fig = plt.figure(figsize=(7.2, 8.4))

# hero radar
titled_box(fig, (0.055, 0.520, 0.890, 0.445), VARIANTS[0][0])
axh = fig.add_axes([0.285, 0.545, 0.430, 0.360], polar=True)
radar(axh, VARIANTS[0][1], VARIANTS[0][2], big=True)
axh.legend(frameon=False, fontsize=9, loc="upper right",
           bbox_to_anchor=(1.47, 1.12), handlelength=1.3)

# 2 x 2 variants
POS = [(0.055, 0.275), (0.505, 0.275), (0.055, 0.030), (0.505, 0.030)]
for (px, py), (title, ca, cb) in zip(POS, VARIANTS[1:]):
    titled_box(fig, (px, py, 0.440, 0.230), title)
    ax = fig.add_axes([px + 0.105, py + 0.028, 0.230, 0.160], polar=True)
    radar(ax, ca, cb, big=False)
    ax.legend(frameon=False, fontsize=5.6, loc="center left",
              bbox_to_anchor=(1.10, 0.50), handlelength=1.0,
              labelspacing=0.3)

fig.savefig(os.path.join(HERE, "layout4_radar_variants.png"), dpi=200)
print("wrote layout4_radar_variants.png")
