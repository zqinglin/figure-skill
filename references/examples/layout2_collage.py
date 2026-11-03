#!/usr/bin/env python3
"""Layout 2 - eight-panel collage (A-H).

Distribution box, stacked proportion, three line-over-bar double-axis panels,
a two-tier diagnostic, a value-labelled horizontal bar and a wide multi-series
beeswarm, arranged as a standard journal collage. Synthetic, generic data.
"""
from __future__ import annotations
import os
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from _layout_common import (HERE, apply_style, TXT, BAR_EDGE, letter, stamp,
                            PINK, BLUE, BEIGE, NEUTRAL, VIOLET, ROSE,
                            DEEP_R, DEEP_B)

apply_style()
rng = np.random.default_rng(23)

BINS = [f"[{a}-{a+5}]" for a in range(95, -1, -5)]


def double_axis(ax, bins, seed, ymax, ylab, show_y2=True):
    """Stacked count bars (right axis) under three line series (left axis)."""
    r = np.random.default_rng(seed)
    n = len(bins); x = np.arange(n)
    lo = r.uniform(18, 55, n)
    hi = lo * r.uniform(0.5, 1.6, n)
    ax2 = ax.twinx()
    ax2.bar(x, lo, color=PINK, width=0.78, **BAR_EDGE, zorder=1)
    ax2.bar(x, hi, bottom=lo, color=BLUE, width=0.78, **BAR_EDGE, zorder=1)
    ax2.set_ylim(0, 200); ax2.set_yticks([0, 50, 100, 150, 200])
    ax2.tick_params(labelsize=6.5)
    ax2.spines["right"].set_visible(show_y2); ax2.spines["top"].set_visible(False)
    if not show_y2:
        ax2.set_yticklabels([])
    base = np.linspace(ymax * 0.55, ymax * 0.85, n) + r.normal(0, ymax * 0.07, n)
    for lab, c, off in [("Subset I", DEEP_R, ymax * 0.10),
                        ("Subset II", DEEP_B, -ymax * 0.12),
                        ("All", "#C9C9C9", 0.0)]:
        y = np.clip(base + off + r.normal(0, ymax * 0.05, n), 0, ymax)
        ax.plot(x, y, color=c, lw=0.9, marker="o", ms=2.6,
                markeredgecolor=TXT, markeredgewidth=0.3, label=lab, zorder=3)
    ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
    ax.set_ylim(0, ymax); ax.set_xlim(-0.7, n - 0.3)
    ax.set_xticks(x); ax.set_xticklabels(bins, rotation=90, fontsize=5.6)
    ax.set_ylabel(ylab, fontsize=7.2); ax.tick_params(axis="y", labelsize=6.5)
    ax.set_xlabel("Input bin (%)", fontsize=7)
    return ax2


fig = plt.figure(figsize=(7.2, 8.3))
gs = GridSpec(4, 24, figure=fig, height_ratios=[1.00, 1.00, 1.00, 1.08],
              hspace=0.92, wspace=3.0,
              left=0.075, right=0.955, top=0.955, bottom=0.055)

# ── A: two-group distribution ─────────────────────────────────────────────
axA = fig.add_subplot(gs[0, 0:4])
a = rng.lognormal(0.25, 0.45, 300).clip(0, 5)
b = rng.lognormal(0.05, 0.40, 300).clip(0, 5)
bp = axA.boxplot([a, b], positions=[0, 1], widths=0.55, patch_artist=True,
                 showfliers=False, medianprops=dict(color=TXT, lw=1.0),
                 whiskerprops=dict(color=TXT, lw=0.8),
                 capprops=dict(color=TXT, lw=0.8),
                 boxprops=dict(edgecolor=TXT, lw=0.8))
bp["boxes"][0].set_facecolor(PINK); bp["boxes"][1].set_facecolor(BLUE)
for p, d, c in zip([0, 1], [a, b], [DEEP_R, DEEP_B]):
    axA.scatter(p + rng.uniform(-0.2, 0.2, 110), rng.choice(d, 110),
                s=1.6, color=c, alpha=0.65, linewidths=0, zorder=3)
axA.axhline(1.0, ls="--", lw=0.8, color=TXT)
axA.set_ylim(0, 5); axA.set_xticks([0, 1])
axA.set_xticklabels(["Subset I", "Subset II"], fontsize=7)
axA.set_ylabel("Relative value\n(ratio to baseline)", fontsize=7.2)
axA.tick_params(labelsize=6.5)
letter(axA, "A", dx=-0.42)

# ── B: stacked proportion ─────────────────────────────────────────────────
axB = fig.add_subplot(gs[0, 5:8])
axB.bar([0], [0.03], color="white", edgecolor=TXT, lw=0.8)
axB.bar([0], [0.97], bottom=[0.03], color=PINK, **BAR_EDGE)
axB.bar([1], [1.0], color="white", edgecolor=TXT, lw=0.8)
axB.text(0, 0.50, "30", ha="center", va="center", fontsize=7.5, color=TXT)
axB.text(0, 0.015, "1", ha="center", va="center", fontsize=6.5, color=TXT)
axB.set_ylim(0, 1.12); axB.set_xticks([0, 1])
axB.set_xticklabels(["Observed", "Expected"], rotation=30, ha="right", fontsize=7)
axB.set_ylabel("Proportion of sources", fontsize=7.2)
axB.tick_params(labelsize=6.5)
axB.legend(handles=[Patch(facecolor="white", edgecolor=TXT, label="type I"),
                    Patch(facecolor=PINK, edgecolor=TXT, label="type II")],
           frameon=False, fontsize=6.2, loc="lower left",
           bbox_to_anchor=(-0.05, 1.04), handlelength=1.1)
letter(axB, "B", dx=-0.55)

# ── C, D, E: line-over-bar double axis ────────────────────────────────────
axC = fig.add_subplot(gs[0, 9:16])
double_axis(axC, BINS, 101, 25, "Response rate (%)", show_y2=False)
axC.text(0.03, 0.96, "Top 5% cut", transform=axC.transAxes, fontsize=6.8, va="top")
axC.legend(frameon=False, fontsize=6.2, loc="upper right", handlelength=1.2,
           bbox_to_anchor=(1.02, 1.05))
letter(axC, "C", dx=-0.17)

axD = fig.add_subplot(gs[0, 17:24])
ax2D = double_axis(axD, BINS[::2], 202, 15, "Relative rate (%)")
ax2D.set_ylabel("Count", fontsize=7, rotation=0, labelpad=2, va="bottom")
axD.axhline(5, ls="--", lw=0.8, color=DEEP_R)
letter(axD, "D", dx=-0.17)

axE = fig.add_subplot(gs[1, 0:11])
double_axis(axE, BINS, 303, 25, "Response rate (%)")
axE.text(0.03, 0.96, "Top 5% cut", transform=axE.transAxes, fontsize=6.8, va="top")
letter(axE, "E", dx=-0.11)

# ── F: two-tier diagnostic ────────────────────────────────────────────────
STAGES = ["Stage\n1", "Stage\n2", "Stage\n3", "Stage\n4"]
xs = np.arange(4)
subF = GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1, 13:19],
                               hspace=0.18)
axF1 = fig.add_subplot(subF[0])
axF1.plot(xs, [0.88, 1.0, 0.98, 1.0], color=DEEP_B, marker="o", ms=3.2, lw=0.9,
          markeredgecolor=TXT, markeredgewidth=0.3)
axF1.plot(xs, [1.0, 1.0, 0.80, 0.98], color="#C9C9C9", marker="o", ms=3.2, lw=0.9,
          markeredgecolor=TXT, markeredgewidth=0.3)
axF1.set_ylim(0.68, 1.06); axF1.set_xlim(-0.4, 3.4)
axF1.set_xticks(xs); axF1.set_xticklabels([])
axF1.set_ylabel("Detection rate", fontsize=7.2); axF1.tick_params(labelsize=6.5)
axF1.text(0.5, 1.055, "Upper tier", transform=axF1.transAxes, ha="center",
          fontsize=6.6)
letter(axF1, "F", dx=-0.26)

axF2 = fig.add_subplot(subF[1])
for i, m in enumerate([-0.22, -0.20, -0.12, -0.10]):
    d = rng.normal(m, 0.14, 55)
    c = DEEP_B if i < 2 else DEEP_R
    axF2.scatter(i + rng.uniform(-0.18, 0.18, 55), d, s=2.2, color=c,
                 alpha=0.7, linewidths=0)
    axF2.errorbar(i, d.mean(), yerr=d.std() / np.sqrt(55), color=TXT, lw=0.8,
                  capsize=2, marker="_", ms=8)
axF2.axhline(0, ls="--", lw=0.8, color=TXT); axF2.invert_yaxis()
axF2.set_xticks(xs); axF2.set_xticklabels(STAGES, fontsize=6.2)
axF2.set_ylabel("Difference\n(arb.)", fontsize=7.2); axF2.tick_params(labelsize=6.5)

# ── G: value-labelled horizontal bars ─────────────────────────────────────
axG = fig.add_subplot(gs[2, 0:9])
names = ["Method A", "Method B", "Method C", "Ensemble",
         "Method A (alone)", "Baseline I", "Baseline II", "Baseline III",
         "Combined"]
vals = [0.161, 0.172, 0.080, 0.160, 0.118, 0.084, 0.088, 0.112, 0.158]
cols = [PINK, BLUE, VIOLET, NEUTRAL, PINK, BEIGE, "#333A8C", ROSE, "#9E9E9E"]
y = np.arange(len(names))[::-1]
axG.barh(y, vals, color=cols, height=0.68, **BAR_EDGE)
for yy, v in zip(y, vals):
    axG.text(v + 0.004, yy, f"{v:.3f}", va="center", fontsize=6.0, color=TXT)
axG.set_yticks(y); axG.set_yticklabels(names, fontsize=6.4)
axG.set_xlim(0, 0.23); axG.set_xlabel("Score (arb. units)", fontsize=7)
axG.tick_params(axis="x", labelsize=6.5)
axG.axhline(y[4] + 0.5, color="#BBBBBB", lw=0.7, ls="--")
letter(axG, "G", dx=-0.28)

# ── H: four cuts x five methods beeswarm ──────────────────────────────────
axH = fig.add_subplot(gs[3, 0:24])
SER = [("Method A", PINK), ("Method B", BLUE), ("Baseline I", BEIGE),
       ("Baseline II", "#333A8C"), ("Baseline III", ROSE)]
CUTS = [("Cut 1", 11, 5), ("Cut 2", 28, 15), ("Cut 3", 41, 25), ("Cut 4", 72, 50)]
for gi, (cname, centre, hline) in enumerate(CUTS):
    for si, (sname, col) in enumerate(SER):
        x0 = gi * (len(SER) + 1.2) + si
        d = np.clip(rng.normal(centre + si * 2.0, 17, 90), 0, 100)
        order = np.argsort(d); xs_ = np.zeros_like(d)
        seen = defaultdict(int)
        for k, bb in enumerate(np.round(d[order] / 3.2)):
            c_ = seen[bb]; seen[bb] += 1
            xs_[order[k]] = ((c_ % 9) - 4) * 0.035 * (1 if c_ % 2 else -1)
        axH.scatter(x0 + xs_, d, s=3.4, facecolor="none", edgecolor=col,
                    linewidths=0.42)
        axH.plot([x0 - 0.33, x0 + 0.33], [np.median(d)] * 2, color=TXT, lw=1.1,
                 zorder=5)
    gx = gi * (len(SER) + 1.2)
    axH.plot([gx - 0.6, gx + len(SER) - 0.4], [hline] * 2, color=PINK, lw=0.9)
    axH.text(gx + len(SER) - 0.35, hline, f"{hline}%", fontsize=5.8,
             color=DEEP_R, va="center")
    if gi:
        axH.axvline(gx - 1.1, color="#BBBBBB", lw=0.7, ls="--")
axH.set_xticks([gi * (len(SER) + 1.2) + 2 for gi in range(4)])
axH.set_xticklabels([c[0] for c in CUTS], fontsize=7.5)
axH.set_ylim(0, 108)
axH.set_ylabel("Score (%)", fontsize=7.2); axH.tick_params(labelsize=6.5)
axH.legend(handles=[Line2D([], [], marker="o", ls="", mfc="none", mec=c,
                           label=n, ms=4) for n, c in SER],
           frameon=False, ncol=5, fontsize=6.4, loc="lower left",
           bbox_to_anchor=(0.0, 1.02), handlelength=1.0)
letter(axH, "H", dx=-0.055)

stamp(fig)
fig.savefig(os.path.join(HERE, "layout2_collage.png"), dpi=200)
print("wrote layout2_collage.png")
