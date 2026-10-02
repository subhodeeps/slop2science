"""Tests of the physics behind the example figures in src/python/amore/examples.py.

black_hole_charges() draws the field of test charges near extremal black holes. These tests check
the function that it uses, mp_test_field(), in three dimensions and against separate formulas:

- for one hole it equals the closed form of Frolov and Zelnikov, Phys. Rev. D 85, 064032, Eq. (4.21);
- it solves Maxwell's equation d_a (U^2 d_a A_0) = 0 away from the sources;
- the flux of U^2 grad Phi gives the charge of the test charge, the charge at infinity, and zero
  change of the charge of each hole;
- the coefficients C_k = M_k / rho'_k that the paper prints for Eq. (4.14) do change the charges
  of the holes when there are several holes (this pins the correction that the code makes).
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "python"))
pytest.importorskip("matplotlib")
from amore import examples  # noqa: E402

THREE_HOLES = [(1.5, -0.5, 1 / 3, 1.0), (-1.0, 0.5, -0.25, 0.7), (0.2, 1.6, 0.9, 0.5)]   # x, y, z, M
CHARGE = (0.2, -1 / 3, 0.5, 1.0)                                                          # x', y', z', e'


def sphere_flux(field, centre, radius, nt=80, nph=160):
    """Flux of U^2 grad Phi through a sphere, divided by 4 pi (Gauss-Legendre in cos(theta))."""
    nodes, weights = np.polynomial.legendre.leggauss(nt)
    phi = (np.arange(nph) + 0.5) * 2 * np.pi / nph
    c, p = np.meshgrid(nodes, phi, indexing="ij")
    s = np.sqrt(1 - c ** 2)
    n = [s * np.cos(p), s * np.sin(p), c]
    point = [centre[a] + radius * n[a] for a in range(3)]
    _, grad, big_u = field(*point)
    integrand = big_u ** 2 * sum(grad[a] * n[a] for a in range(3))
    return float(np.sum(weights[:, None] * integrand) * (2 * np.pi / nph) * radius ** 2) / (4 * np.pi)


def paper_field(holes, charge):
    """The same field with the coefficients C_k = M_k / rho'_k of Eq. (4.14) of the paper."""
    holes = np.asarray(holes, float)
    pos, mass = holes[:, :3], holes[:, 3]
    cpos, e = np.array(charge[:3]), charge[3]
    rp = np.linalg.norm(pos - cpos, axis=1)
    up = 1 + np.sum(mass / rp)

    def field(x, y, z):
        pt = [x, y, z]
        rho = [np.sqrt(sum((pt[a] - pos[k, a]) ** 2 for a in range(3))) for k in range(len(mass))]
        big_u = 1 + sum(mass[k] / rho[k] for k in range(len(mass)))

        def phi_at(q):
            rq = [np.sqrt(sum((q[a] - pos[k, a]) ** 2 for a in range(3))) for k in range(len(mass))]
            uq = 1 + sum(mass[k] / rq[k] for k in range(len(mass)))
            rr = np.sqrt(sum((q[a] - cpos[a]) ** 2 for a in range(3)))
            return e * (1 / rr + sum(mass[k] / rp[k] / rq[k] for k in range(len(mass)))) / (uq * up)

        h = 1e-6
        grad = [(phi_at([pt[b] + h * (a == b) for b in range(3)]) - phi_at([pt[b] - h * (a == b) for b in range(3)]))
                / (2 * h) for a in range(3)]
        return phi_at(pt), grad, big_u
    return field


def test_one_hole_equals_the_closed_form_of_the_paper():
    hole, charge = (0.0, 0.0, 0.0, 1.3), (1.1, -0.4, 0.7, 1.0)
    field = examples.mp_test_field([hole], [charge])
    x, y, z = 0.6, 0.9, -0.5
    rho, rho_c = np.sqrt(x * x + y * y + z * z), np.sqrt(1.1 ** 2 + 0.4 ** 2 + 0.7 ** 2)
    big_u, big_u_c = 1 + 1.3 / rho, 1 + 1.3 / rho_c
    r = np.sqrt((x - 1.1) ** 2 + (y + 0.4) ** 2 + (z - 0.7) ** 2)
    expected = (1 / r + 1.3 / (rho * rho_c)) / (big_u * big_u_c)           # Eq. (4.21), D = 4
    assert field(x, y, z)[0] == pytest.approx(expected, rel=1e-12)


def test_the_potential_solves_maxwells_equation():
    field = examples.mp_test_field(THREE_HOLES, [CHARGE, (-2.0, -1.0, -0.4, -1.0)])

    def flux_density(x, y, z):
        _, grad, big_u = field(x, y, z)
        return [big_u ** 2 * g for g in grad]

    h = 1e-4
    for point in ((1.0, 1.0, 1.0), (-2.5, 0.3, 0.8), (0.4, -1.7, -1.2)):
        div = 0.0
        for a in range(3):
            up, dn = list(point), list(point)
            up[a] += h
            dn[a] -= h
            div += (flux_density(*up)[a] - flux_density(*dn)[a]) / (2 * h)
        assert abs(div) < 1e-5


def test_the_gradient_is_the_gradient_of_phi():
    field = examples.mp_test_field(THREE_HOLES, [CHARGE])
    point, h = np.array([0.7, 0.9, -0.6]), 1e-6
    _, grad, _ = field(*point)
    for a in range(3):
        step = np.zeros(3)
        step[a] = h
        numeric = (field(*(point + step))[0] - field(*(point - step))[0]) / (2 * h)
        assert grad[a] == pytest.approx(numeric, rel=1e-6)


def test_the_charge_is_e_and_no_horizon_changes_its_charge():
    field = examples.mp_test_field(THREE_HOLES, [CHARGE])
    assert sphere_flux(field, CHARGE[:3], 0.01) == pytest.approx(-1.0, abs=1e-6)       # the test charge
    assert sphere_flux(field, (0, 0, 0), 300.0) == pytest.approx(-1.0, abs=2e-3)        # at infinity
    for hole in THREE_HOLES:
        for radius in (0.02, 0.2):
            assert abs(sphere_flux(field, hole[:3], radius)) < 1e-6


def test_the_coefficients_printed_in_the_paper_change_the_horizon_charges():
    field = paper_field(THREE_HOLES, CHARGE)
    induced = [sphere_flux(field, h[:3], 0.02) for h in THREE_HOLES]
    assert max(abs(q) for q in induced) > 0.02                                        # 0.036 for hole 1
    assert sum(induced) == pytest.approx(0.0, abs=1e-6)                               # the total is kept
    # the formula dQ_k = -(M_k / U') sum_{j != k} (M_j / d_jk)(1 / rho'_j - 1 / rho'_k)
    pos, mass = np.array(THREE_HOLES)[:, :3], np.array(THREE_HOLES)[:, 3]
    rp = np.linalg.norm(pos - np.array(CHARGE[:3]), axis=1)
    up = 1 + np.sum(mass / rp)
    for k in range(3):
        predicted = -(mass[k] / up) * sum(mass[j] / np.linalg.norm(pos[j] - pos[k]) * (1 / rp[j] - 1 / rp[k])
                                          for j in range(3) if j != k)
        assert -induced[k] == pytest.approx(predicted, abs=2e-4)                     # flux = -(charge change)
