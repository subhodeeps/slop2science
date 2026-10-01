"""Regenerate the four example figures and the palette chart of the amore style (in README.md).

The four example figures have one plot area (amore.figure), saved with exact_size=True.

Run: make plot-examples
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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

    fig, ax = amore.figure()
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
    potential with a small Poschl-Teller or Gaussian bump at a distance a from the peak.

    The barrier has a vertical gradient fill. The dashed curve is the effective potential of
    null geodesics, V_null = (1 - 2M/r) L^2 / r^2, from the radial equation
    (dr/dlambda)^2 + V_null = E^2. A null ray depends only on b = L/E, so the scale of V_null is
    free; the plot scales it to the peak height of the Regge-Wheeler potential, to compare the
    shapes. The peak of V_null is the photon sphere r = 3M (r = 1.5 in units 2M = 1,
    r_* = 1.5 + log 0.5), marked with a dot. The Regge-Wheeler peak is at r = 1.64 for l = 2;
    for large l the potential tends to V_null with L^2 = l (l + 1). The labels at the two ends
    show that r_* -> -inf at the horizon r = 2M and r_* -> +inf at spatial infinity."""
    teal, amber, plum = (amore.palette(n) for n in ("teal", "amber", "plum"))
    rstar = np.linspace(-10, 50, 6000)
    r = tortoise_to_r(rstar)
    v_rw = (1 - 1 / r) * (6 / r ** 2 - 3 / r ** 3)           # l = 2, spin 2, units 2M = 1
    r_photon = 1.5                                            # r = 3M, units 2M = 1
    shape = lambda r_: (1 - 1 / r_) / r_ ** 2                 # noqa: E731  V_null / L^2
    v_null = v_rw.max() * shape(r) / shape(r_photon)          # same peak height as V_RW
    a, eps_pt, w = 41.0, 0.0012, 0.6                          # Poschl-Teller bump
    b, eps_g, sigma = 40.0, 0.004, 2.3                        # Gaussian bump
    v_pt = v_rw + eps_pt / np.cosh((rstar - a) / w) ** 2
    v_g = v_rw + eps_g * np.exp(-((rstar - b) ** 2) / (2 * sigma ** 2))
    at = lambda xs, v: np.interp(xs, rstar, v)                # noqa: E731

    fig, ax = amore.figure()
    ax.set_xlim(-10, 50)
    ax.set_ylim(-0.17, 0.82)
    # The gradient fill: a vertical ramp from the shade tone at V = 0 to the light tone at the
    # peak, clipped to the area under the potential.
    under = ax.fill_between(rstar, v_rw, color="none", lw=0)
    ramp = LinearSegmentedColormap.from_list("ramp", [teal["shade"], teal["light"], teal["main"]])
    fill = ax.imshow(np.linspace(0, 1, 256)[:, None], extent=(-10, 50, 0, v_rw.max()),
                     origin="lower", aspect="auto", cmap=ramp, vmin=0, vmax=1.35, zorder=1)
    fill.set_clip_path(under.get_paths()[0], transform=ax.transData)
    ax.plot(rstar, v_null, color=teal["ink"], lw=1.0, ls="--", zorder=4,
            label=r"null geodesic")
    x_ps, y_ps = r_photon + np.log(r_photon - 1), v_rw.max()
    ax.plot([x_ps], [y_ps], ls="none", marker="o", ms=4.5, color=teal["ink"], mec="white",
            mew=0.9, zorder=5)
    ax.text(3.6, 0.555, r"$r = 3M$", color=teal["ink"], fontsize=9)
    ax.annotate(r"\texttt{photon sphere}", xy=(x_ps, y_ps), xytext=(3.6, 0.615),
                fontsize=8, color=teal["ink"],
                arrowprops=dict(arrowstyle="->", lw=0.7, color=teal["ink"], shrinkA=2, shrinkB=3))
    ax.text(-8.9, -0.025, r"$r \to 2M$", color=teal["ink"], fontsize=9, va="top")
    ax.text(48.9, -0.025, r"$r \to \infty$", color=teal["ink"], fontsize=9, va="top", ha="right")
    ax.plot(rstar, v_rw, color=teal["main"], lw=1.4, zorder=4, label=r"Regge--Wheeler, $\ell = 2$")
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

    fig, ax = amore.figure(colorbar=True)
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
    amore.colorbar(ax, filled, r"$\phi(x, y)$", ticks=[-1, -0.5, 0, 0.5, 1])
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    amore.tag(ax, TAG)
    amore.save(fig, OUT / "amore_green", dpi=README_DPI, formats=("png",), exact_size=True)
    plt.close(fig)


def kerr_curvature():
    """fakeparulapastel: the Kretschmann scalar K = R_abcd R^abcd of a Kerr black hole, from its
    closed form (units M = 1, spin a = 0.9), with no numerical solution:

        K = 48 (r^2 - c^2) ((r^2 + c^2)^2 - 16 r^2 c^2) / (r^2 + c^2)^6,   c = a cos(theta),

    in Boyer-Lindquist r and theta. The meridional plane uses x = sqrt(r^2 + a^2) sin(theta) and
    z = r cos(theta). K diverges at the ring singularity (r = 0, theta = pi/2), at x = +-a, z = 0,
    and changes sign across the dashed curves K = 0. The density is log10 |K| normalised to
    n = (log10 |K| + 1) / 6, clipped to [0, 1]: n = 0 at |K| = 10^-1 and n = 1 at |K| = 10^5. The
    colour bar has the label log10(M^4 |R_abcd R^abcd|) and the range 0 to 1; the range shows
    that the scale is normalised. The main map and the inset (a zoom on the right ring point)
    share this scale, so one colour bar reads both. The thin contour lines are at n = 0.1 to 0.6
    in the main map and n = 0.5 to 0.8 in the inset, without numbers. The pale red curves are the
    event horizon (solid) and the inner horizon (dotted). The segment between
    the two ring points (|x| < a, z = 0) is the disk r = 0, where the spacetime continues to the
    sheet r < 0; the plot shows the sheet r >= 0 above and below it, so contours end on the disk.

    Source: R. C. Henry, "Kretschmann scalar for a Kerr-Newman black hole", ApJ 535, 350 (2000),
    arXiv:astro-ph/9912320, p. 6, with charge Q = 0; the factor (r^2 - c^2)(...) expands to his
    r^6 - 15 r^4 c^2 + 15 r^2 c^4 - c^6. Checked independently: K from the Riemann tensor of the
    Kerr metric agrees with this form to 2e-11 (relative) at 80 points, inside and outside the
    horizons, for a = 0, 0.5, 0.9 and 0.99.
    """
    spin = 0.9
    ink = amore.palette("slate")["ink"]
    # The horizons: the lightest amore red. Red is the one hue that parula does not contain.
    horizon = dict(color=amore.palette("red")["light"])

    def kretschmann_at(x, z):
        big = x ** 2 + z ** 2 - spin ** 2
        r2 = 0.5 * (big + np.sqrt(big ** 2 + 4 * spin ** 2 * z ** 2))
        c2 = np.where(r2 > 0, spin ** 2 * z ** 2 / np.maximum(r2, 1e-30), spin ** 2)  # a^2 cos^2
        sigma = r2 + c2
        return 48 * (r2 - c2) * (sigma ** 2 - 16 * r2 * c2) / sigma ** 6

    def normalised(k):                         # log10 |K| from -1 to 5, mapped to 0 to 1
        return np.clip((np.log10(np.abs(k) + 1e-30) + 1) / 6, 0, 1)

    x, z = np.meshgrid(np.linspace(-3.0, 3.0, 1000), np.linspace(-1.96, 1.96, 654))
    kretschmann = kretschmann_at(x, z)
    field = normalised(kretschmann)

    fig, ax = amore.figure(colorbar=True)
    image = ax.imshow(field, extent=(-3.0, 3.0, -1.96, 1.96), origin="lower", aspect="auto",
                      cmap=amore.fakeparulapastel(), vmin=0, vmax=1, interpolation="bilinear")
    ax.contour(x, z, field, levels=np.arange(0.1, 0.65, 0.1), colors=amore.OVERLAY,
                       linewidths=0.5, alpha=amore.OVERLAY_ALPHA, linestyles="solid")
    ax.contour(x, z, kretschmann, levels=[0], colors=ink, linewidths=0.9, linestyles="--")
    theta = np.linspace(0, 2 * np.pi, 400)
    for radius, style in ((1 + np.sqrt(1 - spin ** 2), "-"), (1 - np.sqrt(1 - spin ** 2), ":")):
        ax.plot(np.sqrt(radius ** 2 + spin ** 2) * np.sin(theta), radius * np.cos(theta),
                ls=style, lw=1.3, **horizon)
    ax.plot([-spin, spin], [0, 0], color=ink, lw=1.3, solid_capstyle="butt")      # the disk r = 0
    ax.plot([-spin, spin], [0, 0], ls="none", marker="o", ms=4.5, color=ink, mec="white", mew=0.9)
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-1.96, 1.96)
    ax.grid(False)
    note = dict(facecolor="white", alpha=0.78, edgecolor="none", boxstyle="round,pad=0.15")
    pointer = dict(arrowstyle="->", lw=0.7, color=ink, shrinkA=2, shrinkB=0)
    # Each arrow ends exactly on its feature. On the spin axis (theta = 0, so z = r and c = a),
    # K = 0 at r = a and r = a (2 +- sqrt 3); the arrow points at z = a.
    x_h = -1.2
    z_h = (1 + np.sqrt(1 - spin ** 2)) * np.sqrt(1 - x_h ** 2 / (2 + 2 * np.sqrt(1 - spin ** 2)))
    ax.annotate(r"\texttt{ring singularity}", xy=(-spin, 0), xytext=(-2.85, -0.95), fontsize=8,
                bbox=note, arrowprops=pointer)
    ax.annotate(r"\texttt{event horizon}", xy=(x_h, z_h), xytext=(-2.85, 1.65), fontsize=8,
                bbox=note, arrowprops=pointer)
    ax.annotate(r"$K = 0$", xy=(0.0, spin), xytext=(0.9, 1.55), fontsize=9, bbox=note,
                arrowprops=pointer)
    r_minus = 1 - np.sqrt(1 - spin ** 2)                       # the inner (Cauchy) horizon
    x_i = 0.3
    z_i = -r_minus * np.sqrt(1 - x_i ** 2 / (r_minus ** 2 + spin ** 2))
    ax.annotate(r"\texttt{inner horizon}", xy=(x_i, z_i), xytext=(0.55, -1.32), fontsize=8,
                bbox=note, arrowprops=pointer)
    ax.text(-2.85, -1.82, r"$a = 0.9\,M$", fontsize=9, bbox=note)

    # Zoom on the flower at the right ring point: a filled contour plot of n on the same colour
    # scale as the main map, so the colour bar reads both. Its bands, 0.05 apart, show the
    # gradients inside the petals.
    zoom_x, zoom_z = (spin - 0.3, spin + 0.3), (-0.3, 0.3)
    xi, zi = np.meshgrid(np.linspace(*zoom_x, 650), np.linspace(*zoom_z, 650))
    k_zoom = kretschmann_at(xi, zi)
    f_zoom = normalised(k_zoom)
    # The inset spans x = 1.4 to 2.9 and z = -0.75 to 0.75.
    ins = amore.inset(ax, [0.7333, 0.3087, 0.25, 0.3827], zoom_x, zoom_z)
    ins.contourf(xi, zi, f_zoom, levels=np.linspace(0, 1, 21), cmap=amore.fakeparulapastel())
    ins.contour(xi, zi, f_zoom, levels=[0.5, 0.6, 0.7, 0.8], colors=amore.OVERLAY,
                linewidths=0.4, alpha=amore.OVERLAY_ALPHA, linestyles="solid")
    ins.contour(xi, zi, k_zoom, levels=[0], colors=ink, linewidths=0.7, linestyles="--")
    ins.plot(np.sqrt(r_minus ** 2 + spin ** 2) * np.sin(theta), r_minus * np.cos(theta),
             ls=":", lw=1.3, **horizon)
    ins.plot([zoom_x[0], spin], [0, 0], color=ink, lw=1.1, solid_capstyle="butt")
    ins.plot([spin], [0], ls="none", marker="o", ms=3.5, color=ink, mec="white", mew=0.8)
    ins.set_xticks([])
    ins.set_yticks([])
    ins.grid(False)
    box = dict(color="white", lw=0.7)
    link = dict(color="white", lw=0.8, ls=":")
    ax.plot([zoom_x[0], zoom_x[1], zoom_x[1], zoom_x[0], zoom_x[0]],
            [zoom_z[0], zoom_z[0], zoom_z[1], zoom_z[1], zoom_z[0]], **box)
    for sign in (1, -1):                       # box corners to the inset corners at x = 1.4
        ax.plot([zoom_x[1], 1.4], [sign * zoom_z[1], sign * 0.75], **link)
    ax.set_xlabel(r"$x/M$")
    ax.set_ylabel(r"$z/M$")
    ticks = [0, 0.25, 0.5, 0.75, 1]
    bar = amore.colorbar(ax, image, r"$\log_{10}\bigl(M^4\,|R_{abcd}R^{abcd}|\bigr)$",
                         ticks=ticks)
    bar.set_ticklabels([f"{t:g}" for t in ticks])
    amore.tag(ax, TAG, loc="lower right")
    amore.save(fig, OUT / "amore_parula", dpi=README_DPI, formats=("png",), exact_size=True)
    plt.close(fig)


def palette_chart():
    """Every colour of amore: one row for each palette, one swatch for each tone with its hex
    code and its lightness L*, and the colour map of the palette. Shown in README.md."""
    from matplotlib.patches import FancyBboxPatch
    order = ("red", "amber", "olive", "green", "teal", "blue", "plum", "slate")
    fig, ax = plt.subplots(figsize=(7.2, 5.5), layout="constrained")
    ax.set_xlim(0, 7.2)
    ax.set_ylim(-2.25, len(order) + 0.15)
    ax.axis("off")
    for j, tone in enumerate(amore.TONES):
        ax.text(1.55 + 1.05 * j, len(order) - 0.15, r"\texttt{%s}" % tone, ha="center", fontsize=9)
    ax.text(6.25, len(order) - 0.15, r"\texttt{cmap}", ha="center", fontsize=9)
    for i, name in enumerate(order):
        y = len(order) - 1 - i
        tones = amore.palette(name)
        ax.text(0.92, y + 0.38, r"\texttt{%s}" % name, ha="right", va="center", fontsize=9,
                color=tones["ink"])
        for j, tone in enumerate(amore.TONES):
            colour = tones[tone]
            x = 1.05 + 1.05 * j
            ax.add_patch(FancyBboxPatch((x, y + 0.08), 1.0, 0.62, boxstyle="round,pad=0,rounding_size=0.08",
                                        facecolor=colour, edgecolor="0.82", lw=0.4))
            # The text colour with the higher contrast on this swatch: white or the ink.
            # contrast_on_white(c) = 1.05 / (Y_c + 0.05), so Y_c = 1.05 / ratio - 0.05.
            y_sw, y_ink = (1.05 / amore.contrast_on_white(c) - 0.05 for c in (colour, tones["ink"]))
            on_white = 1.05 / (y_sw + 0.05)
            on_ink = (max(y_sw, y_ink) + 0.05) / (min(y_sw, y_ink) + 0.05)
            text = "white" if on_white > on_ink else tones["ink"]
            ax.text(x + 0.5, y + 0.47, r"\texttt{%s}" % colour.lstrip("#"), ha="center",
                    va="center", fontsize=7.5, color=text)
            ax.text(x + 0.5, y + 0.24, r"$L^* = %.0f$" % amore.lab(colour)[0], ha="center",
                    va="center", fontsize=6.5, color=text)
        ax.imshow(np.linspace(0, 1, 256)[None, :], cmap=amore.cmap(name), aspect="auto",
                  extent=(5.35, 7.15, y + 0.08, y + 0.70))
    # The diverging map and the overlay grey, below the palettes.
    ax.text(0.92, -0.62, r"\texttt{diverging}", ha="right", va="center", fontsize=9)
    ax.imshow(np.linspace(0, 1, 256)[None, :], cmap=amore.diverging("red", "green"), aspect="auto",
              extent=(1.05, 5.20, -0.93, -0.31))
    ax.text(0.92, -1.32, r"\texttt{fakeparulapastel}", ha="right", va="center", fontsize=9)
    ax.imshow(np.linspace(0, 1, 256)[None, :], cmap=amore.fakeparulapastel(), aspect="auto",
              extent=(1.05, 5.20, -1.63, -1.01))
    ax.text(0.92, -1.95, r"\texttt{overlay}", ha="right", va="center", fontsize=9)
    ax.add_patch(FancyBboxPatch((1.05, -2.17), 1.0, 0.42, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=amore.OVERLAY, alpha=amore.OVERLAY_ALPHA, edgecolor="none"))
    ax.text(2.2, -1.96, r"\texttt{%s} at %.0f\,\%% opacity, for lines on a colour map"
            % (amore.OVERLAY.lstrip("#"), 100 * amore.OVERLAY_ALPHA), va="center", fontsize=8)
    ax.text(7.15, -1.96, r"\textbf{%d colours}" % (len(order) * len(amore.TONES)), ha="right",
            va="center", fontsize=9)
    amore.save(fig, OUT / "amore_palettes", dpi=README_DPI, formats=("png",), exact_size=True)
    plt.close(fig)


if __name__ == "__main__":
    amore.use()
    wave_packet()
    potential_with_bump()
    signed_field()
    kerr_curvature()
    palette_chart()
    print(f"wrote {OUT}/amore_blue.png, amore_teal.png, amore_green.png, amore_parula.png and amore_palettes.png")
