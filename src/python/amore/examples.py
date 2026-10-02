"""Regenerate the four example figures and the palette chart of the amore style (in README.md).

The four example figures have one plot area (amore.figure), saved with exact_size=True.

Run: make plot-examples
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
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
    amore.save(fig, OUT / "amore_blue", dpi=README_DPI, formats=("pdf", "png"), exact_size=True)
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
    amore.save(fig, OUT / "amore_teal", dpi=README_DPI, formats=("pdf", "png"), exact_size=True)
    plt.close(fig)


def mp_test_field(holes, charges):
    """Field of test charges in a Majumdar-Papapetrou background of extremal black holes (D = 4).

    holes: rows (x, y, z, M). charges: rows (x', y', z', e'). Returns field(x, y, z), which gives
    Phi (per unit e', so Phi = -A_0 of a charge e' = 1 for each charge, summed with the signs),
    its gradient (three arrays) and U. The formula is Eqs. (4.9) and (4.17) of Frolov and Zelnikov,
    Phys. Rev. D 85, 064032 (2012), with the coefficients C_k of the pole terms taken from the
    condition that no horizon changes its charge. That condition differs from Eq. (4.14) of the
    paper. This result contradicts Eq. (4.14) of the paper. Someone must check it again.

    Derivation of the correction. Use e' = 1, D = 4, G = c = 1. Let rho_k = |x - x_k|,
    rho'_k = |x' - x_k|, d_jk = |x_j - x_k|, R = |x - x'|.

    1. Background: U = 1 + sum_k M_k / rho_k, and A_0 = 1/U. Static Maxwell equation in the
       background, away from the sources: d_a (U^2 d_a A_0) = 0 (a = 1, 2, 3, flat derivatives).
    2. Ansatz of the paper (Eqs. 4.9, 4.17): A_0 = -psi / (U(x) U(x')), with
       psi = 1/R + sum_k C_k / rho_k. This solves step 1 for all C_k. With A_0 = -psi / (U U'),
       U^2 d_a (psi/U) = U d_a psi - psi d_a U, so the divergence is U lap(psi) - psi lap(U).
       Both U and psi are harmonic away from their poles, so it is zero.
    3. Charge of hole k: Q_k = (1/4 pi) * (flux of U^2 d_n A_0 through a sphere rho = r0 around
       x_k), with r0 -> 0. The divergence of step 1 is zero, so the flux does not depend on r0.
       Check with the background A_0 = 1/U: U^2 d_rho (1/U) = -d_rho U = M_k / rho^2, so Q_k = M_k.
    4. Local expansion near hole k (rho = rho_k -> 0):
           U   = M_k / rho + u_k + O(rho),          u_k = 1 + sum_{j != k} M_j / d_jk,
           psi = C_k / rho + s_k + O(rho),          s_k = 1/rho'_k + sum_{j != k} C_j / d_jk.
       Then psi / U = (C_k + rho s_k) / (M_k + rho u_k) = (1/M_k) [C_k + rho (s_k - C_k u_k / M_k)]
       + O(rho^2). The terms that depend on angle enter at order rho^2 and add nothing to the
       flux. Put A_0 = -psi / (U U') and U^2 rho^2 -> M_k^2, and the flux gives
           Q_k = - (M_k s_k - C_k u_k) / U'.
       The background charge M_k stays, so the change of charge of hole k is
           dQ_k = - (M_k s_k - C_k u_k) / U',   U' = U(x') = 1 + sum_k M_k / rho'_k.
    5. Eq. (4.14) of the paper: C_k = M_k / rho'_k. Put it in step 4:
           M_k s_k - C_k u_k = M_k sum_{j != k} (M_j / d_jk) (1/rho'_j - 1/rho'_k),
           dQ_k = - (M_k / U') sum_{j != k} (M_j / d_jk) (1/rho'_j - 1/rho'_k).
       This is zero for one hole, and when all rho'_k are equal. Otherwise it is not zero. The
       dQ_k sum to zero, because the terms for (j, k) and (k, j) cancel in pairs (that is why the
       total charge is right).
    6. Hand check with two holes, M_1 = 1 and M_2 = 0.7, at x_1 = (1.5, -0.5, 1/3) and
       x_2 = (-1.0, 0.5, -0.25), charge at x' = (0.2, -1/3, 0.5). Then rho'_1 = 1.32119,
       rho'_2 = 1.64224, d_12 = 2.75505, U' = 1 + 1/1.32119 + 0.7/1.64224 = 2.18314, and
           dQ_1 = - (1 * 0.7 / (2.18314 * 2.75505)) * (1/1.64224 - 1/1.32119) = +0.01722.
    7. Condition dQ_k = 0 for every k, with general C_k (step 4: M_k s_k = C_k u_k):
           u_i C_i - M_i sum_{j != i} C_j / d_ij = M_i / rho'_i       (i = 1 ... N).
       For N = 1 it gives C_1 = M_1 / rho'_1, the paper's value. Sum the N equations. The
       terms M_j C_i / d_ij and M_i C_j / d_ij cancel in pairs, so sum_k C_k = sum_k M_k / rho'_k
       = U' - 1. Then psi -> U' / r at infinity, A_0 -> -1/r, and the charge at infinity is
       exactly e' = 1. That is the check that the paper's other equations also hold.
    8. Numbers for three holes (the test in tests/python/test_examples_physics.py uses them):
       M = (1, 0.7, 0.5) at x_1 = (1.5, -0.5, 1/3), x_2 = (-1.0, 0.5, -0.25), x_3 = (0.2, 1.6, 0.9),
       charge at x' = (0.2, -1/3, 0.5).
           rho'     = 1.32119  1.64224  1.97428        d_12, d_13, d_23 = 2.7550  2.5340  1.9931
           u        = 1.4514   1.61383  1.74584        U' = 2.43640
           C paper  = 0.75689  0.42625  0.25326        (sum 1.43640 = U' - 1)
           dQ paper = +0.03571 -0.00805 -0.02766       (sum 0)
           C fixed  = 0.70955  0.43857  0.28828        (sum 1.43640; dQ = 0 for all three)
    9. Numerical check of the flux, independent of steps 3 to 5. Take the field of this
       function (the same code as the figure). For each hole, sum U^2 d_n A_0 over a sphere of
       radius r0 around x_k (Gauss-Legendre in cos(theta), 80 points; uniform in phi, 160 points),
       divide by 4 pi, and subtract M_k. The result is the dQ_k of step 8 for the C paper values
       and zero for the C fixed values, with the same digits for r0 = 0.002 to 0.2.

    Script that reproduces steps 5 to 8 (numpy only; run it after the import below):

        import numpy as np
        M = np.array([1.0, 0.7, 0.5])
        X = np.array([[1.5, -0.5, 1/3], [-1.0, 0.5, -0.25], [0.2, 1.6, 0.9]])
        Y = np.array([0.2, -1/3, 0.5])
        rp = np.linalg.norm(X - Y, axis=1)                       # rho'_k
        d = np.linalg.norm(X[:, None] - X[None], axis=2); np.fill_diagonal(d, np.inf)
        Up = 1 + np.sum(M / rp)                                  # U'
        u = 1 + (M[None, :] / d).sum(axis=1)                     # u_k
        dQ = lambda C: -(M * (1 / rp + (C[None, :] / d).sum(axis=1)) - C * u) / Up
        C_paper = M / rp                                         # Eq. (4.14)
        A = np.diag(u) - M[:, None] / d                          # step 7
        C_fixed = np.linalg.solve(A, M / rp)
        print(rp, d[0, 1], d[0, 2], d[1, 2], u, Up)
        print(C_paper, dQ(C_paper), dQ(C_paper).sum())
        print(C_fixed, dQ(C_fixed))

    The function below solves the system of step 7 for each charge.
    """
    holes = np.asarray(holes, float)
    pos, mass = holes[:, :3], holes[:, 3]
    n = len(holes)
    d = np.array([[np.linalg.norm(pos[i] - pos[j]) if i != j else np.inf for j in range(n)]
                  for i in range(n)])
    u = 1 + np.array([sum(mass[j] / d[i, j] for j in range(n) if j != i) for i in range(n)])
    system = np.diag(u) - np.array([[mass[i] / d[i, j] if i != j else 0 for j in range(n)]
                                    for i in range(n)])
    terms = []                                       # (position, e', C_k, U(x')) of each charge
    for cx, cy, cz, e in np.asarray(charges, float):
        rp = np.linalg.norm(pos - np.array([cx, cy, cz]), axis=1)
        terms.append((np.array([cx, cy, cz]), e, np.linalg.solve(system, mass / rp),
                      1 + np.sum(mass / rp)))

    def field(x, y, z):
        pt = [x, y, z]
        rho = [np.sqrt(sum((pt[a] - pos[k, a]) ** 2 for a in range(3))) for k in range(n)]
        big_u = 1 + sum(mass[k] / rho[k] for k in range(n))
        du = [-sum(mass[k] * (pt[a] - pos[k, a]) / rho[k] ** 3 for k in range(n)) for a in range(3)]
        phi, grad = 0 * big_u, [0 * big_u for _ in range(3)]
        for c_pos, e, c, up in terms:
            r = np.sqrt(sum((pt[a] - c_pos[a]) ** 2 for a in range(3)))
            s = 1 / r + sum(c[k] / rho[k] for k in range(n))
            ds = [-(pt[a] - c_pos[a]) / r ** 3
                  - sum(c[k] * (pt[a] - pos[k, a]) / rho[k] ** 3 for k in range(n))
                  for a in range(3)]
            phi = phi + e * s / (big_u * up)
            for a in range(3):
                grad[a] = grad[a] + e / up * (ds[a] / big_u - s * du[a] / big_u ** 2)
        return phi, grad, big_u
    return field


def black_hole_charges():
    """Red and green palettes: test charges near two extremal black holes, from closed forms.

    V. P. Frolov and A. Zelnikov, "Scalar and electromagnetic fields of static sources in higher
    dimensional Majumdar-Papapetrou spacetimes", Phys. Rev. D 85, 064032 (2012). Units G = c = 1,
    D = 4 (n = 1). Extremal charged black holes (charge = mass) rest in equilibrium, with
    ds^2 = -U^-2 dt^2 + U^2 dx^2 and U = 1 + sum_k M_k / rho_k, where rho_k = |x - x_k| (Eqs. 2.2,
    2.7). Here there are two holes with M_k = M = 1. Each horizon is a point x_k in these
    isotropic coordinates, so the black dots are not to scale. A test charge e' at x' (e' much
    smaller than M, so there is no back-reaction) has the potential A_0 = -e' [1/R + sum_k C_k /
    rho_k] / (U(x) U(x')) with R = |x - x'| (Eqs. 4.9, 4.17). This figure draws Phi = -A_0 per
    unit test charge, for two charges + e' and two charges - e'. It leaves out the potential of
    the holes, 1 - 1/U, which is positive everywhere and would hide the sign. A static observer
    measures E_i = d_i A_0 (the metric factors cancel), so the lines drawn here are the lines of
    force of the test charges. Each line starts on a + charge and ends on a - charge or leaves
    the plot. The dashed line is Phi = 0, the cross is a point where E = 0 (a saddle of Phi), and
    the contours are labelled in units of e' / M.

    A correction to the paper. Eq. (4.14) gives C_k = M_k / rho'_k and states that then the
    charges of the holes do not change. That holds for one hole, or when all the rho'_k are equal.
    For several holes the printed C_k give hole k the extra charge
        dQ_k = - (M_k / U(x')) sum_{j != k} (M_j / d_jk) (1 / rho'_j - 1 / rho'_k)  (units of e'),
    and these dQ_k sum to zero. For three holes with M = 1, 0.7 and 0.5 and a charge at
    (0.2, -1/3, 0.5), the flux of U^2 grad A_0 through a small sphere gives +0.036, -0.008 and
    -0.028 (both from the flux and from this formula, and the same at every radius). This code
    takes the C_k that make every dQ_k zero. They solve the linear system
        u_i C_i - M_i sum_{j != i} C_j / d_ij = M_i / rho'_i,   u_i = 1 + sum_{j != i} M_j / d_ij.
    For one hole it gives the paper's C_k. The C_k then sum to U(x') - 1, which gives exactly the
    charge e' at infinity. The full derivation, the numbers, and a script that reproduces them
    are in the docstring of mp_test_field().

    This result contradicts Eq. (4.14) of the paper. Someone must check it again.

    Checked independently, with sympy and not with the code below: the metric and A_0 = 1/U
    solve the Einstein-Maxwell equations (residual 6e-32 at 6 points); the potential above solves
    d_a (U^2 d_a A_0) = 0 (residual 6e-32 at 8 points); the flux of U^2 grad A_0 is 4 pi e'
    through a small sphere around the charge and at infinity, and zero through each hole.
    tests/python/test_examples_physics.py repeats the Maxwell and flux checks, in three
    dimensions, on the function that this figure uses.
    """
    ink = amore.palette("slate")["ink"]
    holes = np.array([(-2.1, -1.1, 0.0, 1.0), (2.1, -1.1, 0.0, 1.0)])         # x, y, z, M
    charges = [(-1.0, 0.0, 0.0, 1.0), (1.2, 0.4, 0.0, -1.0), (0.2, -1.8, 0.0, 1.0),
               (-3.2, 1.5, 0.0, -1.0)]                                        # x', y', z', e'
    hx = holes[:, :2]
    field = mp_test_field(holes, charges)

    def potential(x, y):
        """Phi and its in-plane gradient in the plane z = 0 (the holes and charges lie in it)."""
        phi, grad, _ = field(x, y, 0 * x)
        return phi, grad[:2]

    half_x, half_y = 4.5, 2.95                                     # the plot area has aspect 1.527
    x, y = np.meshgrid(np.linspace(-half_x, half_x, 900), np.linspace(-half_y, half_y, 590))
    phi, grad = potential(x, y)
    vmax = 0.5                                                     # the range is clipped, see below

    fig, ax = amore.figure(colorbar=True)
    filled = ax.contourf(x, y, np.clip(phi, -0.999 * vmax, 0.999 * vmax),
                         levels=np.linspace(-vmax, vmax, 41), cmap=amore.diverging("red", "green"))
    steps = [-1.0, -0.8, -0.6, -0.5, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05,
             0.1, 0.2, 0.3, 0.4]
    lines = ax.contour(x, y, phi, levels=steps, colors="black", alpha=0.6,   # dotted below zero
                       linewidths=[0.6 if v < 0 else 0.4 for v in steps],
                       linestyles=[":" if v < 0 else "solid" for v in steps])
    ax.clabel(lines, levels=[-0.2, 0.2], fmt=r"$%.1f$", fontsize=7, inline=True)
    zero = ax.contour(x, y, phi, levels=[0], colors="black", linewidths=1.0, linestyles="--")

    # Lines of force: E = -grad Phi, from the + charges to the - charges (fourth-order steps).
    def direction(p):
        gx, gy = potential(p[0], p[1])[1]
        return -np.array([gx, gy]) / max(np.hypot(gx, gy), 1e-300)

    sinks = [(c[0], c[1]) for c in charges if c[3] < 0]
    for cx, cy, _, e in charges:
        if e < 0:
            continue
        for angle in np.linspace(0, 2 * np.pi, 16, endpoint=False) + 0.3:
            p = np.array([cx + 0.06 * np.cos(angle), cy + 0.06 * np.sin(angle)])
            path = [p]
            for _ in range(6000):
                k1 = direction(p)
                k2 = direction(p + 0.01 * k1)
                k3 = direction(p + 0.01 * k2)
                k4 = direction(p + 0.02 * k3)
                p = p + 0.02 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
                path.append(p)
                if abs(p[0]) > half_x or abs(p[1]) > half_y:
                    break
                if any(np.hypot(*(p - s)) < 0.06 for s in sinks):
                    break
            path = np.array(path)
            ax.plot(path[:, 0], path[:, 1], color=amore.OVERLAY, lw=0.6, alpha=amore.OVERLAY_ALPHA)
            arc = np.r_[0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))]
            for s0 in np.arange(0.8, arc[-1] - 0.3, 1.4):          # several arrowheads on each line
                k = np.searchsorted(arc, s0)
                if abs(path[k, 0]) < half_x - 0.2 and abs(path[k, 1]) < half_y - 0.2:
                    ax.add_patch(FancyArrowPatch(
                        path[k], path[min(k + 8, len(path) - 1)], arrowstyle="-|>",
                        mutation_scale=6, lw=0, color=amore.OVERLAY, alpha=0.85, shrinkA=0,
                        shrinkB=0))
    ax.set_xlim(-half_x, half_x)
    ax.set_ylim(-half_y, half_y)
    ax.grid(False)
    note = dict(facecolor="white", alpha=0.78, edgecolor="none", boxstyle="round,pad=0.15")
    pointer = dict(arrowstyle="->", lw=0.7, color=ink, shrinkA=2, shrinkB=0)

    # The points where E = 0: the minima of |grad Phi| on the grid, refined by Newton steps.
    gmag = np.hypot(*grad)
    rows, cols = gmag.shape
    window = np.stack([gmag[2 + i:rows - 2 + i, 2 + j:cols - 2 + j]
                       for i in range(-2, 3) for j in range(-2, 3)])
    found = (gmag[2:-2, 2:-2] <= window.min(axis=0)) & (gmag[2:-2, 2:-2] < 0.05)
    saddles = []
    for px, py in zip(x[2:-2, 2:-2][found], y[2:-2, 2:-2][found]):
        p = np.array([px, py])
        for _ in range(12):
            g0 = np.array(potential(*p)[1])
            jac = np.array([(np.array(potential(p[0] + 1e-5 * (a == 0),
                                                p[1] + 1e-5 * (a == 1))[1]) - g0) / 1e-5
                            for a in range(2)]).T
            p = p - np.linalg.solve(jac, g0)
        near_source = min(np.hypot(*(p - np.array(q))) for q in [c[:2] for c in charges] + list(hx))
        if (np.hypot(*potential(*p)[1]) < 1e-8 and np.linalg.det(jac) < 0 and near_source > 0.4
                and abs(p[0]) < half_x - 0.1 and abs(p[1]) < half_y - 0.1
                and all(np.hypot(*(p - q)) > 1e-3 for q in saddles)):
            saddles.append(p)
    saddles = np.array(saddles)
    ax.plot(saddles[:, 0], saddles[:, 1], ls="none", marker="x", ms=6, mew=1.4, color=ink, zorder=7)
    ax.plot(hx[:, 0], hx[:, 1], ls="none", marker="o", ms=8, color=ink, mec="white", mew=0.9,
            zorder=6)
    for cx, cy, _, e in charges:
        ax.plot(cx, cy, ls="none", marker="o", ms=6, color="white", mec=ink, mew=0.9, zorder=6)
        ax.text(cx, cy - 0.01, r"$+$" if e > 0 else r"$-$", fontsize=6, ha="center", va="center",
                color=ink, zorder=7)
    ax.annotate(r"\texttt{extremal black hole}", xy=(hx[0, 0], hx[0, 1]), xytext=(-4.4, -2.55),
                fontsize=8, bbox=note, arrowprops=pointer, zorder=8)
    ax.annotate(r"\texttt{test charge}", xy=(charges[1][0], charges[1][1]), xytext=(2.0, 1.9),
                fontsize=8, bbox=note, arrowprops=pointer, zorder=8)
    on_zero = max(zero.allsegs[0], key=len)                # a point of the dashed line, x near -3.4
    on_zero = on_zero[np.argmin(np.abs(on_zero[:, 0] + 3.4))]
    ax.annotate(r"$\Phi = 0$", xy=on_zero, xytext=(-4.35, 0.15), fontsize=8, bbox=note,
                arrowprops=pointer, zorder=8)
    ax.annotate(r"$\mathbf{E} = 0$", xy=saddles[0], xytext=(-1.9, -2.45), fontsize=8, bbox=note,
                arrowprops=pointer, zorder=8)
    amore.colorbar(ax, filled, r"$\Phi M / e'$ (clipped at $\pm 0.5$)",
                   ticks=[-0.5, -0.25, 0, 0.25, 0.5])
    ax.set_xlabel(r"$x/M$")
    ax.set_ylabel(r"$y/M$")
    amore.tag(ax, TAG)
    amore.save(fig, OUT / "amore_green", dpi=README_DPI, formats=("pdf", "png"), exact_size=True)
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
    amore.save(fig, OUT / "amore_parula", dpi=README_DPI, formats=("pdf", "png"), exact_size=True)
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
    amore.save(fig, OUT / "amore_palettes", dpi=README_DPI, formats=("pdf", "png"), exact_size=True)
    plt.close(fig)


if __name__ == "__main__":
    amore.use()
    wave_packet()
    potential_with_bump()
    black_hole_charges()
    kerr_curvature()
    palette_chart()
    print(f"wrote {OUT}/amore_blue.png, amore_teal.png, amore_green.png, amore_parula.png and amore_palettes.png")
