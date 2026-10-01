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

# Eight palettes of four tones, 32 colours. Each palette has a deep ink for a reference curve
# or a label, a muted main colour, a light tone for fills, and a very light shade for
# background bands. The palettes go round the colour wheel: red, amber, olive, green, teal,
# blue, plum, and slate (a neutral blue-grey for reference data). Pairs that work together:
# red and green are complementary (a diverging map for a signed field); teal and amber are
# split-complementary (two quantities); teal, amber and plum are close to a triad (three
# quantities). tests/python/test_amore.py checks the lightness steps, the contrast of each
# ink and the distance between colours, so a new colour must pass the same rules.
PALETTES = {
    "blue": {"ink": "#2e1a6e", "main": "#5c9dc7", "light": "#b4d0e6", "shade": "#f4f4fa"},
    "green": {"ink": "#1e4d3b", "main": "#6fa98a", "light": "#bcdcc6", "shade": "#f2f7f3"},
    "red": {"ink": "#6b1d2a", "main": "#d2737f", "light": "#efc0c4", "shade": "#fbf3f4"},
    "teal": {"ink": "#164b4f", "main": "#4e9e9f", "light": "#a8d3d1", "shade": "#f0f7f7"},
    "amber": {"ink": "#6e4a12", "main": "#d39b3c", "light": "#efd39a", "shade": "#fbf6ec"},
    "plum": {"ink": "#4e2154", "main": "#9a6aa6", "light": "#d6bfdc", "shade": "#f7f2f8"},
    "olive": {"ink": "#3d4318", "main": "#97a04c", "light": "#d2d6a2", "shade": "#f7f8ee"},
    "slate": {"ink": "#28313d", "main": "#768594", "light": "#c2c9d1", "shade": "#f4f5f7"},
}
TONES = ("ink", "main", "light", "shade")

# A pastel version of the "fake parula" colour map: 9 points, sampled at indices 0, 32, ..., 255
# of cm_data in fake_parula.py of github.com/BIDS/colormap (commit bc54947, CC0, by Nathaniel
# Smith and Stefan van der Walt). MATLAB's own parula belongs to MathWorks and is not used.
# fakeparulapastel() blends each point 20 % towards white; its lightness rises from L* 36 to 95.
FAKE_PARULA = (
    (0.26711, 0.03311, 0.61882),
    (0.14991, 0.28893, 0.59137),
    (0.16690, 0.41028, 0.50959),
    (0.19159, 0.51638, 0.47598),
    (0.16400, 0.63147, 0.39450),
    (0.35846, 0.72348, 0.19466),
    (0.71771, 0.75615, 0.16388),
    (0.99137, 0.78177, 0.32816),
    (0.98681, 0.95698, 0.12662),
)
PARULA_PASTEL = 0.2


# Lines drawn on top of a colour map (flow lines, guides): a dark neutral grey at partial
# opacity. White vanishes on the light centre of a map, black competes with contour lines,
# and a coloured line reads as a quantity.
OVERLAY = "#3a3a3a"
OVERLAY_ALPHA = 0.55


def lab(colour):
    """CIELAB (L*, a*, b*) of a hex colour, for a D65 white. L* is the perceived lightness."""
    rgb = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    x = (0.4124 * rgb[0] + 0.3576 * rgb[1] + 0.1805 * rgb[2]) / 0.95047
    y = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    z = (0.0193 * rgb[0] + 0.1192 * rgb[1] + 0.9505 * rgb[2]) / 1.08883
    f = [t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116 for t in (x, y, z)]
    return 116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])


def contrast_on_white(colour):
    """WCAG contrast ratio of a hex colour against white (1 to 21)."""
    rgb = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 1.05 / (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2] + 0.05)


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


def fakeparulapastel(pastel=PARULA_PASTEL):
    """Return a sequential pastel colour map in the style of parula, from violet to yellow.

    Use it for a field with a wide range, where a single-hue map gives too few steps.
    """
    colours = [tuple(c + pastel * (1 - c) for c in rgb) for rgb in FAKE_PARULA]
    return LinearSegmentedColormap.from_list("amore_parula", colours)


# The plot area of every figure, in inches: the same for a line plot and for a map, so that
# figures side by side match. A figure with a colour bar is taller by COLORBAR_BAND only.
PLOT_AREA = dict(left=0.69, bottom=0.52, width=5.16, height=3.38)
FIGURE_SIZE = (6.0, 4.0)
COLORBAR_BAND = 0.68


def figure(colorbar=False):
    """Return (fig, ax) with the standard plot area. With colorbar=True the figure is taller by
    COLORBAR_BAND, and amore.colorbar() puts the bar in that band, above the plot."""
    width, height = FIGURE_SIZE[0], FIGURE_SIZE[1] + (COLORBAR_BAND if colorbar else 0.0)
    fig = plt.figure(figsize=(width, height))
    a = PLOT_AREA
    ax = fig.add_axes([a["left"] / width, a["bottom"] / height, a["width"] / width,
                       a["height"] / height])
    return fig, ax


def colorbar(ax, mappable, label, ticks=None, gap=0.15, thickness=0.11):
    """Draw a horizontal colour bar above the plot, as wide as the plot, outside the axes.

    The bar never covers data, and it does not take width from the plot. Make the figure with
    amore.figure(colorbar=True), so that the band above the plot has room for the bar, its tick
    labels and its label. gap and thickness are in inches.
    """
    fig = ax.figure
    height = fig.get_figheight()
    box = ax.get_position()
    cax = fig.add_axes([box.x0, box.y1 + gap / height, box.width, thickness / height])
    bar = fig.colorbar(mappable, cax=cax, orientation="horizontal", ticks=ticks)
    cax.xaxis.set_ticks_position("top")
    cax.xaxis.set_label_position("top")
    bar.set_label(label, fontsize=9, labelpad=6)
    cax.tick_params(labelsize=8, length=2.5, which="major")
    cax.minorticks_off()
    bar.outline.set_linewidth(1.0)
    return bar


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
