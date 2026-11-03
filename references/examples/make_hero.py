#!/usr/bin/env python3
"""16:9 hero image for the project front page.

Eight miniature charts drawn natively (not stitched from PNGs) so the banner
stays crisp, plus the palette strip.
"""
from __future__ import annotations
import os
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap

from _layout_common import (HERE, apply_style, TXT, BAR_EDGE,
                            PINK, BLUE, BEIGE, NEUTRAL, VIOLET, ROSE)

apply_style()
rng = np.random.default_rng(3)

P1 = ["#D5D7D6", "#F1C3C1", "#B7D5EC", "#FEDFB1", "#B9C3DC", "#EEB3C1"]
P2 = ["#385a75", "#6192b5", "#98b4ce", "#f4f6f1", "#f2d9be", "#eec0a3"]
P3 = ["#22BDD2", "#1B78B2", "#9368AB", "#F47F1E", "#2DA248"]
P5 = ["#C93735", "#F8AB61", "#78A9CD", "#333A8C"]
P6 = ["#E68600", "#2CA8A2", "#3E7EBF", "#C1272D", "#6E3FA3", "#4CAF50"]
P7 = ["#a4cde1", "#67a4cc", "#277fb8", "#549da3", "#96cb8f", "#4dae47"]
P8 = ["#f38989", "#ec5051", "#ef6a45", "#f9b769", "#f9a341"]
P9 = ["#af93c4", "#8660a8", "#d4a55b", "#b05a28"]
DIV = LinearSegmentedColormap.from_list(
    "bwo", ["#385a75", "#6192b5", "#98b4ce", "#f4f6f1", "#f2d9be", "#eec0a3", "#d2894f"])

fig = plt.figure(figsize=(12.8, 7.2))
fig.patch.set_facecolor("white")
gs = GridSpec(3, 4, figure=fig, height_ratios=[0.40, 1.0, 1.0],
              hspace=0.52, wspace=0.26,
              left=0.045, right=0.965, top=0.97, bottom=0.105)


def mini(ax, title):
    ax.set_title(title, fontsize=9, pad=4, color=TXT)
    ax.tick_params(labelsize=6.5, length=2)


# ── title band ────────────────────────────────────────────────────────────
axT = fig.add_subplot(gs[0, :]); axT.axis("off")
axT.text(0.0, 0.74, "figure-skill", fontsize=38, fontweight="bold",
         color="#1E1E1E", va="center", ha="left")
axT.text(0.0, 0.24,
         "Publication-quality figures for papers  ·  journal palettes, "
         "mandatory rcParams, chart-type selection",
         fontsize=12.5, color="#5A5A5A", va="center", ha="left")
axT.text(1.0, 0.74, "Nature  ·  Science  ·  Cell  ·  ICLR  ·  NeurIPS",
         fontsize=11, color="#8A8A8A", va="center", ha="right")
axT.text(1.0, 0.26, "apply_style()  —  one system, every panel",
         fontsize=10.5, color="#8A8A8A", va="center", ha="right",
         fontstyle="italic")

# ── 1: paired box + dots ──────────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 0])
a = rng.normal(95, 30, 22).clip(20); b = a + rng.normal(30, 28, 22)
bp = ax.boxplot([a, b], positions=[0, 1], widths=0.5, patch_artist=True,
                showfliers=False, medianprops=dict(color=TXT, lw=1.1),
                whiskerprops=dict(color=TXT, lw=0.8),
                capprops=dict(color=TXT, lw=0.8),
                boxprops=dict(edgecolor=TXT, lw=0.8))
bp["boxes"][0].set_facecolor(P1[2]); bp["boxes"][1].set_facecolor(P1[1])
for i in range(len(a)):
    ax.plot([0, 1], [a[i], b[i]], color="#D8D8D8", lw=0.5, zorder=1)
for p, d, c in zip([0, 1], [a, b], [P1[2], P1[1]]):
    ax.scatter(p + rng.uniform(-0.09, 0.09, len(d)), d, s=9, color=c,
               edgecolor=TXT, linewidth=0.4, zorder=3)
ax.set_xticks([0, 1]); ax.set_xticklabels(["Cond. A", "Cond. B"])
mini(ax, "Paired box + dots")

# ── 2: line + shaded CI ───────────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 1])
t = np.linspace(0, 30, 140)
for c, top in [(P5[0], 150), ("#9E9E9E", 48)]:
    m = top * (1 - np.exp(-t / (7 if top > 100 else 12)))
    sd = 5 + 0.22 * t
    ax.plot(t, m, color=c, lw=1.6)
    ax.fill_between(t, m - sd, m + sd, color=c, alpha=0.18, lw=0)
ax.set_xlim(0, 30); mini(ax, "Line + shaded CI")

# ── 3: diverging heatmap ──────────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 2])
M = np.linspace(1.6, -1.4, 12)[:, None] + rng.normal(0, 0.42, (12, 5))
im = ax.imshow(M, cmap=DIV, vmin=-2, vmax=2, aspect="auto")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
cb.outline.set_visible(False); cb.ax.tick_params(length=0, labelsize=6)
mini(ax, "Diverging heatmap")

# ── 4: radar ──────────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 3], polar=True)
ang = np.linspace(0, 2 * np.pi, 7, endpoint=False); angc = np.r_[ang, ang[:1]]
for v, c in [(np.array([.84, .85, .52, .90, .70, .65, .83]), "#0072B2"),
             (np.array([.60, .50, .80, .38, .85, .85, .92]), "#D55E00")]:
    vv = np.r_[v, v[:1]]
    ax.plot(angc, vv, color=c, lw=1.7); ax.fill(angc, vv, color=c, alpha=0.17)
ax.plot(angc, np.ones_like(angc), color="#666666", lw=0.8, ls=(0, (4, 2.5)))
ax.set_xticks(ang); ax.set_xticklabels([f"D{i}" for i in range(1, 8)], fontsize=6.5)
ax.set_yticks([0.5]); ax.set_yticklabels([]); ax.set_ylim(0, 1.05)
ax.grid(color="#DCDCDC", lw=0.55); ax.spines["polar"].set_visible(False)
ax.set_theta_offset(np.pi / 2)
ax.set_title("Radar profile", fontsize=9, pad=9, color=TXT)

# ── 5: projection scatter ─────────────────────────────────────────────────
def cloud(n, scale, seed, bend, aniso):
    """Anisotropic, rotated, slightly bent cluster - reads as a real projection."""
    r = np.random.default_rng(seed)
    sx, sy = aniso
    p = np.c_[r.normal(0, sx, n), r.normal(0, sy, n)]
    p[:, 1] += bend * (p[:, 0] ** 2 - sx ** 2) / sx
    k = n // 6
    t = r.uniform(0, 1, k)
    p[:k, 0] = p[:k, 0] * 0.3 + sx * 1.6 * t
    p[:k, 1] = p[:k, 1] * 0.3 + bend * sx * 1.4 * t ** 2
    th = r.uniform(0, 2 * np.pi)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return (p @ R.T) * scale


ax = fig.add_subplot(gs[2, 0])
cols = [P7[2], P9[1], P7[5], P8[2], P8[4], P3[0]]
cr = np.random.default_rng(77)
for i, c in enumerate(cols):
    ctr = np.array([np.cos(i * 1.05) * 3.3, np.sin(i * 1.05) * 2.7])
    pts = cloud(520, cr.uniform(0.85, 1.25), 500 + i,
                cr.uniform(0.15, 0.5) * cr.choice([-1, 1]),
                (cr.uniform(0.8, 1.3), cr.uniform(0.30, 0.55))) + ctr
    ax.scatter(pts[:, 0], pts[:, 1], s=1.5, color=c, alpha=0.55, linewidths=0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
mini(ax, "2-D projection")

# ── 6: beeswarm ───────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[2, 1])
for i, (m, c) in enumerate(zip([12, 27, 41, 70], P3[:4])):
    d = np.clip(rng.normal(m, 14, 75), 0, 100)
    order = np.argsort(d); xs = np.zeros_like(d); seen = defaultdict(int)
    for k, bb in enumerate(np.round(d[order] / 4)):
        q = seen[bb]; seen[bb] += 1
        xs[order[k]] = ((q % 7) - 3) * 0.030 * (1 if q % 2 else -1)
    ax.scatter(i + xs, d, s=6, facecolor="none", edgecolor=c, linewidths=0.5)
    ax.plot([i - 0.26, i + 0.26], [np.median(d)] * 2, color=TXT, lw=1.3, zorder=5)
ax.set_xticks(range(4)); ax.set_xticklabels([f"Cut {i}" for i in range(1, 5)])
ax.set_ylim(0, 105); mini(ax, "Beeswarm by group")

# ── 7: stacked bar + line, double axis ────────────────────────────────────
ax = fig.add_subplot(gs[2, 2])
x = np.arange(1, 9)
comp = rng.dirichlet([3, 2, 1.2], size=8).T
bottom = np.zeros(8)
for i, c in enumerate([P1[2], P1[3], P1[1]]):
    ax.bar(x, comp[i], bottom=bottom, color=c, width=0.72, **BAR_EDGE)
    bottom += comp[i]
ax.set_ylim(0, 1); ax.set_xticks(x); ax.set_yticks([0, 0.5, 1])
ax2 = ax.twinx()
ax2.plot(x, 52 + np.cumsum(rng.normal(0.35, 0.4, 8)), color=P5[3],
         marker="o", ms=3.4, lw=1.4)
ax2.tick_params(axis="y", colors=P5[3], labelsize=6.5)
ax2.spines["right"].set_visible(True); ax2.spines["right"].set_color(P5[3])
ax2.spines["top"].set_visible(False)
mini(ax, "Composition + result")

# ── 8: raster ─────────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[2, 3])
for row in range(9):
    for c, rate in [(P3[0], 1.4), (P5[0], 0.55)]:
        k = rng.poisson(rate * 13); xs_ = rng.uniform(0, 30, k)
        for xx, ww in zip(xs_, rng.uniform(0.15, 0.7, k)):
            ax.add_patch(plt.Rectangle((xx, row + 0.1), ww, 0.8, color=c, lw=0))
ax.set_xlim(0, 30); ax.set_ylim(0, 9.2); ax.set_yticks([])
ax.spines["left"].set_visible(False)
mini(ax, "Event raster")

# ── palette strip ─────────────────────────────────────────────────────────
strip = fig.add_axes([0.045, 0.028, 0.920, 0.040]); strip.axis("off")
chips = P1 + P2[:5] + P3 + P5 + P6 + P7[:5] + P8[:4] + P9
w = 1.0 / len(chips)
for i, c in enumerate(chips):
    strip.add_patch(plt.Rectangle((i * w, 0.30), w * 0.92, 0.70,
                                  color=c, transform=strip.transAxes, lw=0))
strip.text(0, 0.02, "9 journal palettes  ·  CVD-safe  ·  Times-metric serif  "
                    "·  300 dpi  ·  embedded fonts",
           transform=strip.transAxes, fontsize=8.5, color="#8A8A8A", va="top")

# apply_style() sets savefig.bbox="tight"; clear it so the banner keeps its
# exact 16:9 canvas instead of being trimmed to the drawn content.
plt.rcParams["savefig.bbox"] = None
fig.savefig(os.path.join(HERE, "hero.png"), dpi=150, facecolor="white")
print("wrote hero.png")
