#!/usr/bin/env python3
"""Shared publication-figure style for papers.

Import this and call ``apply_style()`` at the top of every plotting script,
then draw with the named palettes below so that one entity keeps one
(color, marker) across every figure in the paper.

    from figure_style import apply_style, WIDTH_FULL, CS_PEER_PALETTE
    apply_style()
    fig, ax = plt.subplots(figsize=(WIDTH_FULL, 3.0))

The palette system is Okabe-Ito-derived: muted, luminance-balanced, and safe
for the common colour-vision deficiencies. For the full journal-grade palette
set (pastel, diverging, tone-pairs, UMAP ramps, ...) see references/palettes.md.
"""
from __future__ import annotations
import matplotlib as mpl


def apply_style():
    """Apply the mandatory top-journal rcParams. Call once, at import time."""
    mpl.rcParams.update({
        # Serif throughout, so figure text sits with the body rather than
        # against it. Figure type also drops a point below the 10-11pt body:
        # type larger than the prose beside it is the fastest way a panel
        # reads as amateur.
        #
        # Liberation Serif is metric-compatible with Times New Roman and must
        # precede DejaVu in the chain: many machines that render these figures
        # do not ship Times, and matplotlib falls back silently, so without
        # this entry the panels quietly come out in DejaVu Serif.
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Liberation Serif", "Times",
                       "STIXGeneral", "DejaVu Serif", "serif"],
        "mathtext.fontset": "stix",
        "font.size": 8,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,     # embed TrueType, not Type-3 bitmaps
        "svg.fonttype": "none",
    })


# ── Figure widths in inches ──────────────────────────────────────────────
# These match a \textwidth of 5.5 in (ICLR/NeurIPS single-column on 8.5 in
# paper). Adjust to your journal (see the table in SKILL.md) and draw at these
# widths and nowhere else.
#
# This is not a style preference. \includegraphics[width=\textwidth] on a
# figure authored at 13 in scales it by ~0.42, and the font scales with it, so
# the 9pt labels set above reach the page at ~3.8pt, under the 6pt floor.
# Authoring at the final width makes the rcParams sizes mean what they say.
WIDTH_FULL = 5.5     # \textwidth: a full-width figure
WIDTH_HALF = 2.65    # a side-by-side pair inside \textwidth


# ── Equal-status categorical peers (Okabe-Ito, CVD-safe) ─────────────────
# One entity -> one (colour, marker), reused across every figure so a reader
# learns the mapping once.
CS_PEER_PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
CS_PEER_MARKERS = ["o", "s", "^", "D", "v", "P"]


# ── Support / neutral ink ────────────────────────────────────────────────
CS_SUPPORT = {
    "text": "#333333", "axis": "#4D4D4D", "edge": "#4D4D4D",
    "neutral_mid": "#767676", "neutral_light": "#D8D8D8",
}
BAR_EDGE = {"edgecolor": CS_SUPPORT["edge"], "linewidth": 0.8}


def sequential_blues(n, lo=0.40, hi=0.92):
    """Single-hue ramp for an ordered magnitude (low -> high, darker = larger).

    Use for an ordered quantity (stage, dose, time bin), never for unordered
    categories -- those get CS_PEER_PALETTE.
    """
    return mpl.cm.Blues([lo + (hi - lo) * i / max(1, n - 1) for i in range(n)])


def peer(i):
    """(colour, marker) for the i-th equal-status category, cycling if needed."""
    return (CS_PEER_PALETTE[i % len(CS_PEER_PALETTE)],
            CS_PEER_MARKERS[i % len(CS_PEER_MARKERS)])


if __name__ == "__main__":
    # Smoke test + a one-glance swatch of the peer palette.
    import matplotlib.pyplot as plt
    apply_style()
    fig, ax = plt.subplots(figsize=(WIDTH_HALF, 1.2))
    for i, (c, m) in enumerate(zip(CS_PEER_PALETTE, CS_PEER_MARKERS)):
        ax.scatter([i], [0], s=80, color=c, marker=m, edgecolor=CS_SUPPORT["edge"],
                   linewidth=0.8)
    ax.set_yticks([]); ax.set_xticks(range(len(CS_PEER_PALETTE)))
    ax.set_title("CS_PEER_PALETTE")
    fig.savefig("figure_style_swatch.pdf")
    print("wrote figure_style_swatch.pdf")
