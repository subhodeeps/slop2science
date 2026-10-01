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


def test_each_palette_has_four_hex_tones():
    for name in ("blue", "green", "red", "teal", "amber", "plum"):
        tones = ps.palette(name)
        assert sorted(tones) == ["ink", "light", "main", "shade"]
        assert all(HEX.match(v) for v in tones.values()), name


def test_each_palette_gives_a_colour_map():
    for name in ("blue", "green", "red"):
        assert ps.cmap(name).N > 2


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
