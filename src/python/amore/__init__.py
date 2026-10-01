"""amore: the plot style of this project.

Use it for every matplotlib figure:

    import amore
    amore.use()
    c = amore.palette("blue")           # or "green" or "red"
    ax.plot(x, y, color=c["main"])
    amore.shade(ax, x0, x1, "transient", palette="blue")
    amore.save(fig, "path/without/suffix")

amore.mplstyle sets the fonts, the default colour cycle, the frame, the ticks and the grid.
The functions below add what a style file cannot set: named palettes, a colour map for each
palette (and a diverging map for a signed field), a shaded band with a monospace label, an inset, a provenance tag, and saving to PDF
and PNG together.
The style needs LaTeX (latex and dvipng) for the text. `make check-env` reports them.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

STYLE = Path(__file__).with_name("amore.mplstyle")

# Each palette has four tones: a deep ink for a reference curve, a muted main colour, a light
# tone for fills, and a very light shade for background bands. Pairs that work together:
# red and green are complementary (a diverging map for a signed field); teal and amber are
# split-complementary (two quantities in one figure); teal, amber and plum are close to a
# triad, about 120 degrees apart (three quantities); blue stands alone.
PALETTES = {
    "blue": {"ink": "#2e1a6e", "main": "#5c9dc7", "light": "#b4d0e6", "shade": "#f4f4fa"},
    "green": {"ink": "#1e4d3b", "main": "#6fa98a", "light": "#bcdcc6", "shade": "#f2f7f3"},
    "red": {"ink": "#6b1d2a", "main": "#d2737f", "light": "#efc0c4", "shade": "#fbf3f4"},
    "teal": {"ink": "#164b4f", "main": "#4e9e9f", "light": "#a8d3d1", "shade": "#f0f7f7"},
    "amber": {"ink": "#6e4a12", "main": "#d39b3c", "light": "#efd39a", "shade": "#fbf6ec"},
    "plum": {"ink": "#4e2154", "main": "#9a6aa6", "light": "#d6bfdc", "shade": "#f7f2f8"},
}


# Lines drawn on top of a colour map (flow lines, guides): a dark neutral grey at partial
# opacity. White vanishes on the light centre of a map, black competes with contour lines,
# and a coloured line reads as a quantity.
OVERLAY = "#3a3a3a"
OVERLAY_ALPHA = 0.55


def use():
    """Apply the amore style to all figures made after this call."""
    plt.style.use(STYLE)


def palette(name="blue"):
    """Return the four tones of a named palette: ink, main, light and shade."""
    return PALETTES[name]


def cmap(name="green", reverse=False):
    """Return a sequential colour map from shade to ink in a named palette (for contours)."""
    tones = PALETTES[name]
    colours = [tones["shade"], tones["light"], tones["main"], tones["ink"]]
    return LinearSegmentedColormap.from_list(f"amore_{name}", colours[::-1] if reverse else colours)


def diverging(low="red", high="green"):
    """Return a diverging colour map: the low palette, then near white at zero, then the high one.

    Use it for a signed field, with vmin = -vmax so that zero is at the centre of the map.
    """
    lo, hi = PALETTES[low], PALETTES[high]
    colours = [lo["ink"], lo["main"], lo["light"], "#f7f7f5", hi["light"], hi["main"], hi["ink"]]
    return LinearSegmentedColormap.from_list(f"amore_{low}_{high}", colours)


def shade(ax, x0, x1, label=None, y=None, palette="blue"):
    """Shade the band x0 < x < x1 and write a vertical monospace label at its right edge.

    Set the axis limits first. Choose y (data units) so that the label does not touch a
    curve. By default the label sits in the upper part of the band.
    """
    ax.axvspan(x0, x1, facecolor=PALETTES[palette]["shade"], zorder=0)
    if label:
        ymin, ymax = ax.get_ylim()
        ax.text(x1 - 0.03 * (x1 - x0), ymin + 0.72 * (ymax - ymin) if y is None else y,
                r"\texttt{%s}" % label, rotation=90, va="center", ha="right", fontsize=9)


def inset(ax, bounds, xlim, ylim):
    """Add an inset at bounds = [left, bottom, width, height], in axes fractions."""
    ins = ax.inset_axes(bounds)
    ins.set_xlim(*xlim)
    ins.set_ylim(*ylim)
    ins.tick_params(which="both", labelsize=8)
    return ins


def tag(ax, text, loc="lower right"):
    """Write a provenance tag in a corner ("lower right", "upper right", "lower left" or
    "upper left"), on a translucent box. Choose the corner where it hides no data."""
    vert, horiz = loc.split()
    x, ha = (0.98, "right") if horiz == "right" else (0.02, "left")
    y, va = (0.98, "top") if vert == "upper" else (0.02, "bottom")
    ax.text(x, y, text, transform=ax.transAxes, fontsize=8, va=va, ha=ha,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.2"))


def save(fig, path, dpi=None, formats=("pdf", "png"), exact_size=False):
    """Save the figure as PDF (for the paper) and PNG (for previews), side by side.

    The style crops each figure to its content. For figures that must have one exact size
    (side by side in a document), make each with `plt.subplots(layout="constrained")` and
    pass exact_size=True. Then each file has the size of the figure, without cropping.
    The PNG has the same bytes for the same input. The PDF does not: TeX font subsets get a
    random name prefix. Commit a PNG when a byte comparison matters.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({"savefig.bbox": "standard"} if exact_size else {}):
        if "pdf" in formats:
            fig.savefig(path.with_suffix(".pdf"), metadata={"CreationDate": None})
        if "png" in formats:
            fig.savefig(path.with_suffix(".png"), **({"dpi": dpi} if dpi else {}))
