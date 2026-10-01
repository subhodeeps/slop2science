"""Tests of the amore plot style in src/python/amore/.

The rendering test needs LaTeX. Without latex and dvipng it is a skip, not a pass.
"""
import re
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "python"))
matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import amore as ps  # noqa: E402

HEX = re.compile(r"^#[0-9a-f]{6}$")


def test_there_are_at_least_30_colours():
    assert sum(len(t) for t in ps.PALETTES.values()) >= 30


def test_each_palette_has_four_hex_tones():
    for name, tones in ps.PALETTES.items():
        assert sorted(tones) == sorted(ps.TONES), name
        assert all(HEX.match(v) for v in tones.values()), name


def test_each_palette_gives_a_colour_map():
    for name in ps.PALETTES:
        assert ps.cmap(name).N > 2


def test_the_tones_step_up_in_lightness():
    """ink -> main -> light -> shade, with steps large enough that no two tones look alike."""
    for name, tones in ps.PALETTES.items():
        ink, main, light, shade = (ps.lab(tones[t])[0] for t in ps.TONES)
        assert main - ink >= 25, name
        assert light - main >= 15, name
        assert shade - light >= 10, name
        assert shade >= 95, name                     # a background band stays nearly white


def test_each_ink_is_dark_enough_for_text():
    """Ink colours label curves, so each must pass WCAG AAA (7:1) against white."""
    for name, tones in ps.PALETTES.items():
        assert ps.contrast_on_white(tones["ink"]) >= 7, name


def test_the_palettes_are_distinct():
    """Two palettes must not look alike: CIE76 colour difference between each pair."""
    import itertools
    limits = {"main": 15, "ink": 10, "light": 8}
    for tone, limit in limits.items():
        for a, b in itertools.combinations(ps.PALETTES, 2):
            la, lb = ps.lab(ps.PALETTES[a][tone]), ps.lab(ps.PALETTES[b][tone])
            assert sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5 >= limit, (tone, a, b)


def test_the_fakeparulapastel_map_rises_in_lightness():
    """A sequential map must rise in lightness at every step, or it shows false features."""
    import numpy as np
    cm = ps.fakeparulapastel()
    hexes = ["#%02x%02x%02x" % tuple(int(round(v * 255)) for v in cm(t)[:3])
             for t in np.linspace(0, 1, 64)]
    lightness = [ps.lab(h)[0] for h in hexes]
    assert all(b > a for a, b in zip(lightness, lightness[1:]))
    assert lightness[0] < 40 and lightness[-1] > 90       # it uses most of the lightness range


def test_the_colour_bar_sits_above_the_plot_and_keeps_its_size():
    """amore.figure(colorbar=True) adds a band above the plot. The plot area, in inches, stays
    the same as without a colour bar, and the bar sits in the band, outside the axes."""
    import numpy as np
    with plt.style.context(ps.STYLE), plt.rc_context({"text.usetex": False}):
        def inches(ax):
            box = ax.get_window_extent()
            return round(box.width / ax.figure.dpi, 3), round(box.height / ax.figure.dpi, 3)
        fig0, ax0 = ps.figure()
        fig1, ax1 = ps.figure(colorbar=True)
        image = ax1.imshow(np.random.default_rng(0).random((4, 4)), cmap=ps.fakeparulapastel(),
                           aspect="auto")
        bar = ps.colorbar(ax1, image, "z")
        assert inches(ax0) == inches(ax1)
        assert bar.ax.get_position().y0 > ax1.get_position().y1      # above the plot, no overlap
        plt.close(fig0)
        plt.close(fig1)


def test_the_overlay_grey_has_no_hue():
    _, a, b = ps.lab(ps.OVERLAY)
    assert (a * a + b * b) ** 0.5 < 3


def test_the_colour_helpers_give_known_values():
    assert abs(ps.lab("#ffffff")[0] - 100) < 0.01
    assert abs(ps.lab("#000000")[0]) < 0.01
    assert abs(ps.contrast_on_white("#000000") - 21) < 0.01
    assert abs(ps.contrast_on_white("#ffffff") - 1) < 0.01


def test_the_diverging_map_is_near_white_at_zero():
    r, g, b, _ = ps.diverging("red", "green")(0.5)
    assert min(r, g, b) > 0.9


@pytest.mark.skipif(not (shutil.which("latex") and shutil.which("dvipng")),
                    reason="LaTeX (latex, dvipng) is not installed: make check-env")
def test_exact_size_gives_the_figure_size(tmp_path):
    from PIL import Image
    with plt.style.context(ps.STYLE):
        fig, ax = plt.subplots(figsize=(3, 2), layout="constrained")
        ax.set_xlabel(r"$x$")
        ps.save(fig, tmp_path / "f", dpi=100, formats=("png",), exact_size=True)
        plt.close(fig)
    assert Image.open(tmp_path / "f.png").size == (300, 200)


def test_style_file_sets_latex_and_the_frame():
    with plt.style.context(ps.STYLE):
        assert plt.rcParams["text.usetex"] is True
        assert plt.rcParams["axes.linewidth"] == 1.5
        assert plt.rcParams["xtick.direction"] == "in"


@pytest.mark.skipif(not (shutil.which("latex") and shutil.which("dvipng")),
                    reason="LaTeX (latex, dvipng) is not installed: make check-env")
def test_a_figure_renders_and_saves_pdf_and_png(tmp_path):
    with plt.style.context(ps.STYLE):
        c = ps.palette("green")
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 0], color=c["main"], label=r"$f(x)$")
        ax.set_ylim(-0.5, 1.5)
        ps.shade(ax, 0, 1, "band", palette="green")
        ps.inset(ax, [0.6, 0.6, 0.3, 0.3], xlim=(0, 1), ylim=(0, 1))
        ps.tag(ax, r"\textbf{Test}")
        ax.legend()
        ps.save(fig, tmp_path / "fig", dpi=50)
        plt.close(fig)
    assert (tmp_path / "fig.pdf").stat().st_size > 0
    assert (tmp_path / "fig.png").stat().st_size > 0
