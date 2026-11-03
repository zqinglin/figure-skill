#!/usr/bin/env python3
"""Generate the example gallery for figure-skill.

Each figure is original (synthetic data) and is drawn only with
figure_style.apply_style() + the named palettes, so the gallery doubles as a
worked reference for every chart family in references/chart-selection.md and
every palette in references/palettes.md.

    python3 make_examples.py           # writes *.png (+ gallery.png) here

Run from anywhere; it adds the repo root to sys.path to import figure_style.
"""
from __future__ import annotations
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
from figure_style import (apply_style, WIDTH_FULL, WIDTH_HALF,
                          CS_SUPPORT, BAR_EDGE)

apply_style()
rng = np.random.default_rng(11)

# ── palettes (mirrors references/palettes.md) ──────────────────────────────
P1 = {"grey": "#D5D7D6", "pink": "#F1C3C1", "blue": "#B7D5EC",
      "beige": "#FEDFB1", "violet": "#B9C3DC", "rose": "#EEB3C1"}
P2 = ["#385a75", "#6192b5", "#98b4ce", "#f4f6f1", "#f2d9be", "#eec0a3"]  # blue->white->orange
P3_DEEP = ["#22BDD2", "#1B78B2", "#9368AB", "#F47F1E", "#2DA248"]
P3_LITE = ["#D0F0F2", "#CDD9EC", "#E4D8F2", "#FCE1C9", "#D7FADB"]
P5 = {"red": "#C93735", "orange": "#F8AB61", "blue": "#78A9CD", "navy": "#333A8C"}
P6 = ["#E68600", "#2CA8A2", "#3E7EBF", "#C1272D", "#6E3FA3", "#4CAF50", "#CDBE91", "#9E9E9E"]
P7 = ["#a4cde1", "#67a4cc", "#277fb8", "#549da3", "#96cb8f", "#8bc96d", "#4dae47", "#5c9e43"]
P8 = ["#f38989", "#ec5051", "#e32427", "#ef6a45", "#f9b769", "#f9a341", "#f48521"]
P9 = ["#af93c4", "#8660a8", "#815e99", "#d4a6a8", "#d4a55b", "#b05a28"]

DIVERGING = LinearSegmentedColormap.from_list("blue_white_orange",
            ["#385a75", "#6192b5", "#98b4ce", "#f4f6f1", "#f2d9be", "#eec0a3", "#d2894f"])

TXT = CS_SUPPORT["text"]
saved = []


def _panel_letter(ax, s):
    ax.text(-0.18, 1.06, s, transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="top", ha="left")


def _sig_bracket(ax, x1, x2, y, text, h=None):
    h = h if h is not None else (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=0.8, c=TXT)
    ax.text((x1 + x2) / 2, y + h, text, ha="center", va="bottom", fontsize=7.5, color=TXT)


def save(fig, name):
    p = os.path.join(HERE, name)
    fig.savefig(p + ".png", dpi=200)
    plt.close(fig)
    saved.append(name + ".png")
    print("wrote", name + ".png")


# ── ex1: paired box + dots (ref 163A / 165d-k) — Palette 1 ─────────────────
def ex1():
    a = rng.normal(95, 32, 22).clip(20)
    b = a + rng.normal(28, 30, 22)                      # paired, shifted up
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 2.5))
    pos = [0, 1]
    bp = ax.boxplot([a, b], positions=pos, widths=0.5, patch_artist=True,
                    showfliers=False, medianprops=dict(color=TXT, lw=1.1),
                    whiskerprops=dict(color=TXT, lw=0.8),
                    capprops=dict(color=TXT, lw=0.8),
                    boxprops=dict(edgecolor=TXT, lw=0.8))
    for patch, c in zip(bp["boxes"], [P1["blue"], P1["pink"]]):
        patch.set_facecolor(c)
    for i in range(len(a)):                             # paired connecting lines
        ax.plot([0, 1], [a[i], b[i]], color=CS_SUPPORT["neutral_light"], lw=0.5, zorder=1)
    for p, d, c in zip(pos, [a, b], [P1["blue"], P1["pink"]]):
        jx = p + rng.uniform(-0.09, 0.09, len(d))
        ax.scatter(jx, d, s=10, color=c, edgecolor=TXT, linewidth=0.4, zorder=3)
    _sig_bracket(ax, 0, 1, max(a.max(), b.max()) * 1.04, "$P$ = 0.013")
    ax.set_xticks(pos); ax.set_xticklabels(["Saline", "Formalin"])
    ax.set_ylabel("Investigation (s)")
    _panel_letter(ax, "a")
    fig.tight_layout()
    save(fig, "ex1_paired_box_dots")


# ── ex2: diverging heatmap (ref 164 / 167k) — Palette 2 ────────────────────
def ex2():
    genes = [f"Gene {i+1}" for i in range(14)]
    cols = ["SPF+CD", "SPF+LPD", "GF+CD", "GF+LPD"]
    base = np.linspace(1.4, -1.2, 14)[:, None]
    M = base + rng.normal(0, 0.45, (14, 4)) + np.array([0.2, 0.9, -0.3, -0.6])
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 3.2))
    im = ax.imshow(M, cmap=DIVERGING, vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(4)); ax.set_xticklabels(cols, rotation=30, ha="right")
    ax.set_yticks(range(14)); ax.set_yticklabels(genes, fontstyle="italic", fontsize=6.5)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.09, pad=0.03)
    cb.set_label("$z$-score", fontsize=8); cb.outline.set_visible(False)
    cb.ax.tick_params(length=0, labelsize=7)
    _panel_letter(ax, "b")
    fig.tight_layout()
    save(fig, "ex2_diverging_heatmap")


# ── ex3: cumulative line + shaded CI (ref 165b / 166) — Palettes 4/5 ───────
def ex3():
    t = np.linspace(0, 30, 120)
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 2.5))
    series = [("Formalin", "#C93735", 150), ("Saline", CS_SUPPORT["neutral_mid"], 45)]
    for name, c, top in series:
        mean = top * (1 - np.exp(-t / (7 if top > 100 else 12))) + rng.normal(0, 1.2, t.size).cumsum() * 0.05
        sd = 6 + 0.25 * t
        ax.plot(t, mean, color=c, lw=1.4, label=name)
        ax.fill_between(t, mean - sd, mean + sd, color=c, alpha=0.18, lw=0)
    ax.set_xlabel("Time (min)"); ax.set_ylabel("Cumulative duration (s)")
    ax.set_xlim(0, 30)
    ax.legend(frameon=False, loc="upper left")
    _panel_letter(ax, "c")
    fig.tight_layout()
    save(fig, "ex3_line_shaded_ci")


# ── ex4: raster plot (ref 165a) — teal + coral ────────────────────────────
def ex4():
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 2.3))
    n_tr = 8
    for row in range(n_tr):
        for c, rate, col in [("groom", 0.9, "#22BDD2"), ("lick", 0.4, "#C93735")]:
            k = rng.poisson(rate * 18)
            xs = rng.uniform(0, 30, k)
            w = rng.uniform(0.15, 0.6, k)
            for x, wi in zip(xs, w):
                ax.add_patch(plt.Rectangle((x, row + (0 if c == "groom" else 0.45)),
                             wi, 0.4, color=col, lw=0))
    ax.set_xlim(0, 30); ax.set_ylim(0, n_tr + 0.5)
    ax.set_xlabel("Time (min)"); ax.set_yticks([]); ax.set_ylabel("Trials")
    ax.spines["left"].set_visible(False)
    leg = [Patch(facecolor="#22BDD2", label="General allogrooming"),
           Patch(facecolor="#C93735", label="Targeted allolicking")]
    ax.legend(handles=leg, frameon=False, ncol=1, loc="upper right", fontsize=7)
    _panel_letter(ax, "a")
    fig.tight_layout()
    save(fig, "ex4_raster")


# ── ex5: grouped bar + dots with n and P (ref 167) — Palette 6 ─────────────
def ex5():
    groups = ["Control", "Low\nprotein", "High\nfat", "Ketogenic"]
    means = [0.15, 0.95, 0.35, 0.08]
    cols = [P6[7], P6[0], P6[2], P6[5]]
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 2.6))
    for i, (m, c) in enumerate(zip(means, cols)):
        pts = (m + rng.normal(0, m * 0.5 + 0.05, 6)).clip(0)
        ax.bar(i, pts.mean(), width=0.62, color=c, **BAR_EDGE, zorder=2)
        ax.errorbar(i, pts.mean(), yerr=pts.std(), color=TXT, lw=0.8, capsize=2, zorder=3)
        ax.scatter(i + rng.uniform(-0.12, 0.12, 6), pts, s=9, color=TXT, zorder=4)
    _sig_bracket(ax, 0, 1, 1.62, "$P$ < 0.001")
    ax.text(0.98, 0.97, "$n$ = 6 per group", transform=ax.transAxes,
            fontsize=6.8, va="top", ha="right", color=TXT)
    ax.set_xticks(range(4)); ax.set_xticklabels(groups)
    ax.set_ylabel("Relative $Ucp1$ mRNA")
    ax.set_ylim(0, 1.9)
    _panel_letter(ax, "a")
    fig.tight_layout()
    save(fig, "ex5_bar_dots_pvalues")


# ── ex6: tone-pair box, hollow vs filled (ref 166 brain expression) — P3 ───
def ex6():
    grp = ["HAR", "HGE:FB", "HGE:AB", "HLE:AB"]
    base = [1.26, 1.26, 1.40, 1.37]
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 2.5))
    for i, (g, b) in enumerate(zip(grp, base)):
        pre = rng.normal(b, 0.03, 60)
        post = rng.normal(b + [-0.01, 0.0, 0.05, 0.02][i], 0.03, 60)
        for j, (d, filled) in enumerate([(pre, False), (post, True)]):
            x = i + (j - 0.5) * 0.36
            bp = ax.boxplot([d], positions=[x], widths=0.3, patch_artist=True,
                            showfliers=False, medianprops=dict(color=TXT, lw=1),
                            whiskerprops=dict(color=TXT, lw=0.7),
                            capprops=dict(color=TXT, lw=0.7),
                            boxprops=dict(edgecolor=P3_DEEP[2], lw=1))
            bp["boxes"][0].set_facecolor(P3_DEEP[2] if filled else "white")
        _sig_bracket(ax, i - 0.18, i + 0.18, max(pre.max(), post.max()) + 0.02,
                     ["$P$ = 0.02", "ns", "$P$ < 0.001", "$P$ = 0.01"][i])
    ax.set_xticks(range(4)); ax.set_xticklabels(grp)
    ax.set_ylabel("Normalized expression")
    leg = [Patch(facecolor="white", edgecolor=P3_DEEP[2], label="Prenatal"),
           Patch(facecolor=P3_DEEP[2], edgecolor=P3_DEEP[2], label="Postnatal")]
    ax.legend(handles=leg, frameon=False, loc="upper left", fontsize=7)
    _panel_letter(ax, "b")
    fig.tight_layout()
    save(fig, "ex6_tonepair_box")


# ── ex7: radar / spider, 2 series, 7 dims (ref 168) — CVD-safe pair ────────
def ex7():
    dims = ["Responsivity", "NEP", "Rise time", "3-dB\nbandwidth",
            "Yield\nstrength", "Impact\nstrength", "Torsional\nstrength"]
    ge = np.array([0.42, 6.8, 2.1, 360, 70, 5.2, 300])
    si = np.array([0.30, 4.0, 3.2, 150, 85, 6.8, 330])
    hi = np.array([0.5, 8, 4.0, 400, 100, 8.0, 360])
    lo = np.array([0, 0, 0, 0, 0, 0, 0])
    gi = (ge - lo) / (hi - lo); sv = (si - lo) / (hi - lo)
    ang = np.linspace(0, 2 * np.pi, len(dims), endpoint=False)
    ang = np.r_[ang, ang[:1]]
    fig, ax = plt.subplots(figsize=(WIDTH_HALF + 0.3, WIDTH_HALF + 0.3),
                           subplot_kw=dict(polar=True))
    for v, c, name in [(gi, "#3E7EBF", "Ge"), (sv, "#E68600", "Si")]:
        vv = np.r_[v, v[:1]]
        ax.plot(ang, vv, color=c, lw=1.6, label=name)
        ax.fill(ang, vv, color=c, alpha=0.18)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(dims, fontsize=7)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels([], fontsize=6)
    ax.set_ylim(0, 1); ax.grid(color=CS_SUPPORT["neutral_light"], lw=0.6)
    ax.spines["polar"].set_color(CS_SUPPORT["neutral_light"])
    ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1.18, 1.1), fontsize=8)
    fig.tight_layout()
    save(fig, "ex7_radar")


# ── ex8: UMAP scatter + in-place labels + count bar (ref 169) — P7/8/9 ─────
def ex8():
    names = ["Exc", "Inh", "Oli", "OPC", "Ast", "Immune", "Vasc"]
    cols = [P7[2], P9[1], P7[6], P8[3], P8[5], P3_DEEP[0], P9[3]]
    centers = rng.uniform(-6, 6, (len(names), 2))
    counts = (rng.uniform(0.3, 1.0, len(names)) ** 2 * 9000).astype(int)
    fig, (axu, axb) = plt.subplots(1, 2, figsize=(WIDTH_FULL, 2.8),
                                   gridspec_kw=dict(width_ratios=[2.1, 1]))
    for (cx, cy), c, nm, n in zip(centers, cols, names, counts):
        k = max(120, n // 25)
        pts = rng.normal([cx, cy], 0.9, (k, 2))
        axu.scatter(pts[:, 0], pts[:, 1], s=2, color=c, alpha=0.6, linewidths=0, rasterized=True)
        axu.text(cx, cy, nm, fontsize=8, fontweight="bold", ha="center", va="center", color=TXT)
    axu.set_xticks([]); axu.set_yticks([])
    for s in axu.spines.values(): s.set_visible(False)
    axu.set_title("UMAP of all cells", fontsize=8)
    axu.set_xlabel("UMAP1"); axu.set_ylabel("UMAP2")
    order = np.argsort(counts)[::-1]
    y = np.arange(len(names))
    axb.barh(y, counts[order], color=[cols[i] for i in order], **BAR_EDGE)
    axb.set_yticks(y); axb.set_yticklabels([names[i] for i in order], fontsize=7)
    axb.invert_yaxis(); axb.set_xlabel("Number of cells")
    for i, c in enumerate(counts[order]):
        axb.text(c, y[i], f" {c:,}", va="center", ha="left", fontsize=6.3, color=TXT)
    axb.set_xlim(0, counts.max() * 1.25)
    fig.tight_layout()
    save(fig, "ex8_umap_counts")


# ── ex9: stacked composition bar + result line, double Y (chart #15) ───────
def ex9():
    depth = np.arange(1, 9)
    comp = rng.dirichlet([3, 2, 1.2], size=8).T          # 3 stages, sums to 1
    comp = comp / comp.sum(0)
    result = 52 + np.cumsum(rng.normal(0.3, 0.4, 8))
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 2.5))
    bottom = np.zeros(8)
    for i, (c, lab) in enumerate(zip([P1["blue"], P1["beige"], P1["pink"]],
                                     ["Stage 1", "Stage 2", "Stage 3"])):
        ax.bar(depth, comp[i], bottom=bottom, color=c, width=0.7, label=lab, **BAR_EDGE)
        bottom += comp[i]
    ax.set_xlabel("Depth"); ax.set_ylabel("Composition")
    ax.set_ylim(0, 1)
    ax2 = ax.twinx()
    ax2.plot(depth, result, color=P5["navy"], marker="o", ms=3, lw=1.3)
    ax2.set_ylabel("Robust accuracy (%)", color=P5["navy"])
    ax2.tick_params(axis="y", colors=P5["navy"])
    ax2.spines["right"].set_visible(True); ax2.spines["right"].set_color(P5["navy"])
    ax2.spines["top"].set_visible(False)
    ax.legend(frameon=False, loc="lower center", ncol=3, fontsize=6.5,
              bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout()
    save(fig, "ex9_stacked_double_axis")


# ── ex10: beeswarm by group with median line (ref 163H / 166) ──────────────
def ex10():
    groups = ["5th", "15th", "25th", "50th"]
    centers = [10, 25, 40, 72]
    cols = [P3_DEEP[0], P3_DEEP[1], P3_DEEP[2], P3_DEEP[3]]
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 2.5))
    for i, (g, m, c) in enumerate(zip(groups, centers, cols)):
        d = rng.normal(m, 14, 80).clip(0, 100)
        # simple beeswarm: bin y, spread x within bin
        order = np.argsort(d)
        xs = np.zeros_like(d)
        bins = np.round(d[order] / 4)
        from collections import defaultdict
        seen = defaultdict(int)
        for j, b in enumerate(bins):
            k = seen[b]; seen[b] += 1
            xs[order[j]] = (k % 7 - 3) * 0.028 * (1 if k % 2 else -1)
        ax.scatter(i + xs, d, s=6, facecolor="none", edgecolor=c, linewidths=0.5)
        ax.plot([i - 0.25, i + 0.25], [np.median(d)] * 2, color=TXT, lw=1.3, zorder=5)
    ax.set_xticks(range(4)); ax.set_xticklabels(groups)
    ax.set_xlabel("Percentile cutoff"); ax.set_ylabel("Prediction precision (%)")
    ax.set_ylim(0, 105)
    _panel_letter(ax, "h")
    fig.tight_layout()
    save(fig, "ex10_beeswarm")


def contact_sheet():
    import matplotlib.image as mpimg
    imgs = [n for n in saved if n != "gallery.png"]
    ncol = 2; nrow = (len(imgs) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(WIDTH_FULL, 2.4 * nrow))
    for ax, name in zip(axes.ravel(), imgs):
        ax.imshow(mpimg.imread(os.path.join(HERE, name)))
        ax.set_title(name.replace(".png", ""), fontsize=7)
        ax.axis("off")
    for ax in axes.ravel()[len(imgs):]:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "gallery.png"), dpi=130)
    plt.close(fig)
    print("wrote gallery.png")


if __name__ == "__main__":
    for fn in (ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10):
        fn()
    contact_sheet()
    print("done:", len(saved), "figures")
