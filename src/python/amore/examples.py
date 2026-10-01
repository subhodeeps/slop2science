"""Regenerate the three example figures of the amore style (shown in README.md).

All three have the same size: constrained layout, saved with exact_size=True.

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

    fig, ax = plt.subplots(layout="constrained")
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
    amore.save(fig, OUT / "amore_blue", dpi=README_DPI, formats=("png",), exact_size=True)
    plt.close(fig)


def tortoise_to_r(rstar):
    """Invert r_* = r + log(r - 1) for r > 1 (units 2M = 1), by Newton steps in log(r - 1)."""
    u = np.where(rstar < 2, rstar - 1, np.log(np.maximum(rstar - 1, 1e-12)))
    for _ in range(60):
        u = u - (1 + np.exp(u) + u - rstar) / (np.exp(u) + 1)
    return 1 + np.exp(u)


def potential_with_bump():
    """Teal, amber and plum (close to a triad): the Regge-Wheeler potential, and the same
    potential with a small Poschl-Teller or Gaussian bump at a distance a from the peak."""
    teal, amber, plum = (amore.palette(n) for n in ("teal", "amber", "plum"))
    rstar = np.linspace(-10, 50, 6000)
    r = tortoise_to_r(rstar)
    v_rw = (1 - 1 / r) * (6 / r ** 2 - 3 / r ** 3)           # l = 2, spin 2, units 2M = 1
    a, eps_pt, w = 41.0, 0.0012, 0.6                          # Poschl-Teller bump
    b, eps_g, sigma = 40.0, 0.004, 2.3                        # Gaussian bump
    v_pt = v_rw + eps_pt / np.cosh((rstar - a) / w) ** 2
    v_g = v_rw + eps_g * np.exp(-((rstar - b) ** 2) / (2 * sigma ** 2))
    at = lambda xs, v: np.interp(xs, rstar, v)                # noqa: E731

    fig, ax = plt.subplots(layout="constrained")
    ax.set_xlim(-10, 50)
    ax.set_ylim(-0.17, 0.76)
    ax.fill_between(rstar, v_rw, color=teal["light"], alpha=0.55, lw=0)
    ax.plot(rstar, v_rw, color=teal["main"], lw=1.4, label=r"Regge--Wheeler, $\ell = 2$")
    ax.annotate("", xy=(0, -0.05), xytext=(b, -0.05),
                arrowprops=dict(arrowstyle="<->", lw=0.9, ls="--", color=teal["ink"],
                                shrinkA=0, shrinkB=0))
    ax.text(b / 2, -0.075, r"$a$", color=teal["ink"], ha="center", va="top", fontsize=11)

    window = (rstar >= 36) & (rstar <= 44)
    lo, hi = v_rw[window].min(), v_g[window].max()
    pad = 0.12 * (hi - lo)
    ins = amore.inset(ax, [0.43, 0.30, 0.54, 0.57], xlim=(36, 44), ylim=(lo - pad, hi + pad))
    ins.set_yticklabels([])
    ins.tick_params(axis="x", labeltop=True, labelbottom=False)   # keep the zoom lines clear
    ins.grid(False)
    ins.fill_between(rstar, lo - pad, v_rw, color=teal["shade"], lw=0)       # under the bare V
    ins.fill_between(rstar, v_rw, v_g, color=plum["light"], alpha=0.55, lw=0)  # Gaussian area
    ins.fill_between(rstar, v_rw, v_pt, color=amber["light"], alpha=0.9, lw=0)  # P-T area
    ins.plot(rstar, v_rw, color=teal["ink"], ls=":", lw=1.1)
    ins.plot(rstar, v_pt, color=amber["ink"], lw=1.2)
    ins.plot(rstar, v_g, color=plum["ink"], ls="-.", lw=1.2)
    arrow = dict(arrowstyle="<->", lw=0.8, ls="--", shrinkA=0, shrinkB=0)
    ins.annotate("", xy=(b, at(b, v_rw)), xytext=(b, at(b, v_g)),
                 arrowprops=dict(arrow, color=plum["ink"]))
    ins.text(b + 0.12, at(b, v_rw) + 0.3 * eps_g, r"$\epsilon$", color=plum["ink"], fontsize=11)
    ins.annotate("", xy=(a, at(a, v_rw)), xytext=(a, at(a, v_pt)),
                 arrowprops=dict(arrow, color=amber["ink"]))
    ins.text(a + 0.12, (at(a, v_rw) + at(a, v_pt)) / 2, r"$\epsilon$", color=amber["ink"],
             fontsize=11, va="center")
    ys = at(b, v_rw) + eps_g * np.exp(-0.5)
    near = np.flatnonzero(window)                         # the arrow ends on the curve, both sides
    top = near[v_g[near].argmax()]
    left = rstar[near[0]:top][np.argmin(np.abs(v_g[near[0]:top] - ys))]
    right = rstar[top:near[-1]][np.argmin(np.abs(v_g[top:near[-1]] - ys))]
    ins.annotate("", xy=(left, ys), xytext=(right, ys), arrowprops=dict(arrow, color=plum["ink"]))
    ins.text((left + b) / 2, ys + 0.03 * (hi - lo), r"$\sigma$", color=plum["ink"], ha="center",
             fontsize=11)

    def along(xs, v, dy):
        """Position and angle of a label that follows curve v at xs, offset dy in data units."""
        p0, p1 = ins.transData.transform([(xs - 0.3, at(xs - 0.3, v)), (xs + 0.3, at(xs + 0.3, v))])
        return (xs, at(xs, v) + dy), np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))

    fig.canvas.draw()                                       # fix the transforms before use
    (gx_, gy_), g_angle = along(37.35, v_g, 0.03 * (hi - lo))
    ins.text(gx_, gy_, r"\texttt{Gaussian}", color=plum["ink"], fontsize=8, rotation=g_angle,
             rotation_mode="anchor", ha="left", va="bottom")
    # The label spans about r_* = 36.4 to 38.6. Tilt it by the mean slope of the potential
    # under that span (here -14.4 degrees on the page). The angle is set in data units and
    # matplotlib converts it at draw time (transform_rotates_text), so it stays parallel to
    # the curve if the figure size or the axis limits change.
    slope = (at(38.6, v_pt) - at(36.4, v_pt)) / 2.2
    ins.text(37.5, at(37.5, v_pt) + 0.03 * (hi - lo), r"\texttt{P\"oschl-Teller}",
             color=amber["ink"], fontsize=8, rotation=np.degrees(np.arctan(slope)),
             transform_rotates_text=True, rotation_mode="anchor", ha="center", va="bottom")
    zoom = ax.indicate_inset_zoom(ins, edgecolor=teal["ink"], alpha=0.8, lw=0.9, ls=":")
    for line in getattr(zoom, "connectors", ()) or ():
        line.set(color=teal["ink"], linestyle=":", linewidth=0.9, alpha=0.8)

    ax.set_xlabel(r"$r_*$")
    ax.set_ylabel(r"$V^{\mathrm{RW}} + \epsilon\, V_{\mathrm{bump}}$")
    ax.legend(loc="upper left")
    amore.tag(ax, TAG, loc="lower right")
    amore.save(fig, OUT / "amore_teal", dpi=README_DPI, formats=("png",), exact_size=True)
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

    fig, ax = plt.subplots(layout="constrained")
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
    amore.save(fig, OUT / "amore_green", dpi=README_DPI, formats=("png",), exact_size=True)
    plt.close(fig)


if __name__ == "__main__":
    amore.use()
    wave_packet()
    potential_with_bump()
    signed_field()
    print(f"wrote {OUT}/amore_blue.png, amore_teal.png and amore_green.png")
