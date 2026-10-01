"""Regenerate the three example figures of the amore style (shown in README.md).

Run: make plot-examples
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import amore  # noqa: E402

OUT = Path(__file__).resolve().parents[3] / "docs" / "figures"
README_DPI = 200          # small PNGs for the README; amore.save() without dpi gives 600
TAG = r"\textbf{Example} of the amore plot style"


def wave_packet():
    """Blue palette: a signal and a reference, a shaded transient, an inset and an arrow."""
    c = amore.palette("blue")
    t = np.linspace(0, 60, 6000)
    first = np.exp(-((t - 8) / 3) ** 2) * np.sin(2.2 * t)
    later = sum(0.35 * 0.6 ** k * np.exp(-((t - 8 - 14 * k) / 3.5) ** 2) * np.sin(2.2 * t + k)
                for k in range(1, 4))

    fig, ax = plt.subplots()
    ax.plot(t, first, color=c["ink"], ls="--", label="reference", zorder=3)
    ax.plot(t, first + later, color=c["main"], label="signal", zorder=2)
    ax.set_xlim(0, 60)
    ax.set_ylim(-1.2, 1.8)
    amore.shade(ax, 0, 15, "transient", y=1.3, palette="blue")
    ax.annotate("", xy=(22, -0.75), xytext=(36, -0.75),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color="black", shrinkA=0, shrinkB=0))
    ax.text(29, -0.82, r"$\Delta t$", ha="center", va="top", fontsize=10)
    ins = amore.inset(ax, [0.50, 0.55, 0.46, 0.40], xlim=(16, 60), ylim=(-0.3, 0.3))
    ins.plot(t, first + later, color=c["main"], lw=0.8)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$f(t)$")
    ax.legend(loc="lower right", bbox_to_anchor=(0.98, 0.08))
    amore.tag(ax, TAG)
    amore.save(fig, OUT / "amore_blue", dpi=README_DPI, formats=("png",))
    plt.close(fig)


def normal_distribution():
    """Red palette: a histogram against the density, a shaded band, a log-scale inset."""
    c = amore.palette("red")
    rng = np.random.default_rng(1)
    samples = rng.standard_normal(200_000)
    x = np.linspace(-4.5, 4.5, 2000)
    pdf = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    bins = np.linspace(-4.5, 4.5, 91)

    fig, ax = plt.subplots()
    ax.hist(samples, bins=bins, density=True, histtype="stepfilled", color=c["light"],
            edgecolor=c["main"], linewidth=0.8, label="samples")
    ax.plot(x, pdf, color=c["ink"], ls="--", label=r"$p(x) = e^{-x^2/2}/\sqrt{2\pi}$", zorder=3)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(0, 0.62)
    amore.shade(ax, -1, 1, "one sigma", y=0.5, palette="red")
    half = pdf.max() / 2
    xh = np.sqrt(2 * np.log(2))
    ax.annotate("", xy=(-xh, half), xytext=(xh, half),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color="black", shrinkA=0, shrinkB=0))
    ax.text(0, half - 0.012, r"FWHM", ha="center", va="top", fontsize=9)
    ins = amore.inset(ax, [0.71, 0.52, 0.26, 0.40], xlim=(2, 4.5), ylim=(1e-5, 0.1))
    ins.hist(samples, bins=bins, density=True, histtype="stepfilled", color=c["light"],
             edgecolor=c["main"], linewidth=0.6)
    ins.plot(x, pdf, color=c["ink"], ls="--", lw=0.8)
    ins.set_yscale("log")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$p(x)$")
    ax.legend(loc="upper left")
    amore.tag(ax, TAG)
    amore.save(fig, OUT / "amore_red", dpi=README_DPI, formats=("png",))
    plt.close(fig)


def signed_field():
    """Red and green palettes: a signed field with many extrema, a diverging map, labelled
    contours, a dashed zero line, flow lines of the gradient, and marked extrema."""
    c = amore.palette("green")
    x, y = np.meshgrid(np.linspace(-4, 4, 800), np.linspace(-3, 3, 600))
    bumps = ((1.2, -1.6, 1.0, 1.1), (-1.0, 1.4, 1.2, 1.0), (0.9, 2.3, 0.9, 0.7),
             (-0.8, -2.4, -1.1, 0.8), (-1.1, 0.6, -1.0, 0.9), (0.7, -0.3, 2.6, 0.6))
    f = 0.35 * np.sin(1.3 * x) * np.cos(1.1 * y) * np.exp(-(x ** 2 + y ** 2) / 18)
    for amp, x0, y0, w in bumps:
        f += amp * np.exp(-((x - x0) ** 2 + (y - y0) ** 2) / (2 * w ** 2))
    vmax = np.ceil(np.abs(f).max() * 10) / 10                    # round, so levels are round

    fig, ax = plt.subplots()
    levels = np.linspace(-vmax, vmax, int(round(20 * vmax)) + 1)   # steps of 0.1
    filled = ax.contourf(x, y, f, levels=levels, cmap=amore.diverging("red", "green"))
    steps = np.round(np.arange(-1.0, 1.01, 0.2), 1)
    lines = ax.contour(x, y, f, levels=steps[steps != 0], colors="black", linewidths=0.4,
                       alpha=0.6)                                 # the zero line is drawn apart
    ax.clabel(lines, levels=[v for v in lines.levels if abs(abs(v) - 0.4) < 1e-9
                             or abs(abs(v) - 0.8) < 1e-9], fmt=r"$%.1f$", fontsize=7, inline=True)
    ax.contour(x, y, f, levels=[0], colors="black", linewidths=1.0, linestyles="--")
    gy, gx = np.gradient(f)
    flow = ax.streamplot(x, y, gx, gy, color=amore.OVERLAY, linewidth=0.5, density=0.5,
                         arrowsize=0.6)
    flow.lines.set_alpha(amore.OVERLAY_ALPHA)
    flow.arrows.set_alpha(amore.OVERLAY_ALPHA)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.grid(False)
    for amp, x0, y0, w in bumps[:2] + bumps[3:5]:
        near = (x - x0) ** 2 + (y - y0) ** 2 < w ** 2          # the extremum near each bump
        k = np.unravel_index(np.where(near, f * np.sign(amp), -np.inf).argmax(), f.shape)
        name = "max" if amp > 0 else "min"
        ax.plot(x[k], y[k], marker="o", ms=4, color="white", mec="black", mew=0.8)
        ax.text(x[k] + 0.15, y[k] + 0.15, r"\texttt{%s}" % name, fontsize=9,
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.15"))
    bar = fig.colorbar(filled, ax=ax, pad=0.02, ticks=[-1, -0.5, 0, 0.5, 1])
    bar.set_label(r"$\phi(x, y)$")
    bar.outline.set_linewidth(1.5)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    amore.tag(ax, TAG)
    amore.save(fig, OUT / "amore_green", dpi=README_DPI, formats=("png",))
    plt.close(fig)


if __name__ == "__main__":
    amore.use()
    wave_packet()
    normal_distribution()
    signed_field()
    print(f"wrote {OUT}/amore_blue.png, amore_red.png and amore_green.png")
