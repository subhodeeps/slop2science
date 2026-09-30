"""Known-answer test of the FULL solver chain. Copy into tests/python/ per topic.

This is the most important test in the project. Unit tests of each stage are necessary and
not sufficient: a chain can be correct piece by piece and wrong end to end. This test runs
the *same* path the real solver uses — assembly, solve, refinement, acceptance — against a
problem whose answer is known in closed form, in every precision tier the project uses.

Pick the known-answer problem so that it exercises the real chain and nothing is stubbed:
same assembly code, same solver call, same refinement and acceptance logic, only the
coefficients replaced by ones whose exact solution is known.
"""
import math

import pytest

# from <project_package> import assemble, solve, refine, accept


EXACT = [
    # (parameters, exact answer). Use a problem with a closed-form answer: the zeros of a
    # standard special function, an exactly solvable limit, an analytically diagonalizable
    # operator. Cite the source of the exact values in a comment.
]

TIERS = ["working"]          # extend to the project's extended-precision tiers


@pytest.mark.parametrize("params,exact", EXACT)
@pytest.mark.parametrize("tier", TIERS)
def test_full_chain_reproduces_known_answer(params, exact, tier):
    """The complete chain, not a stubbed version of it."""
    pytest.skip("fill in for this project's chain")

    # got = accept(refine(solve(assemble(params, precision=tier))))
    # assert math.isclose(got, exact, rel_tol=1e-10), f"{got} != {exact}"


@pytest.mark.parametrize("params,exact", EXACT)
def test_resolution_refinement_converges(params, exact):
    """Delta between N and 2N shrinks, and toward the exact answer — not merely to
    something stable. A wrong formulation converges cleanly to the wrong number."""
    pytest.skip("fill in for this project's chain")


def test_wrong_coefficient_is_detected():
    """Deliberately perturb one coefficient and assert the chain does NOT report success.

    This is the test that establishes the chain has any diagnostic power at all. In the
    project this template came from, a deliberately sign-flipped recurrence converged
    beautifully and gave confidently wrong answers (docs/failure_modes.md entry 4) — which is
    exactly what this test exists to make visible.
    """
    pytest.skip("fill in for this project's chain")
