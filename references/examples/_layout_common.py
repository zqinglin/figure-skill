"""Shared helpers for the layout-demonstration figures."""
from __future__ import annotations
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))

from figure_style import apply_style, CS_SUPPORT, BAR_EDGE  # noqa: E402

TXT = CS_SUPPORT["text"]
GREY = "#9E9E9E"

# Palette 1 (soft pastel) + Palette 6 (many-category), see ../palettes.md
PINK, BLUE, BEIGE = "#F1C3C1", "#B7D5EC", "#FEDFB1"
NEUTRAL, VIOLET, ROSE = "#D5D7D6", "#B9C3DC", "#EEB3C1"
DEEP_R, DEEP_B = "#C4716D", "#6E9CC4"
P6 = ["#E68600", "#2CA8A2", "#3E7EBF", "#C1272D", "#6E3FA3",
      "#4CAF50", "#CDBE91", "#9E9E9E"]





def letter(ax, s, dx=-0.20, dy=1.14, size=10.5):
    ax.text(dx, dy, s, transform=ax.transAxes, fontsize=size,
            fontweight="bold", va="top", ha="left")


def bracket(ax, x1, x2, y, text, size=7.5):
    h = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.035
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=0.8, c=TXT)
    ax.text((x1 + x2) / 2, y + h * 0.9, text, ha="center", va="bottom",
            fontsize=size, color=TXT)
