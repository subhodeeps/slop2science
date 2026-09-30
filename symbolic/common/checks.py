"""checks.py — print-before-assert check helpers for derivation stages.

Import with::

    import sys, os
    sys.path.insert(0, os.path.join(os.environ["PROJECT_ROOT"], "symbolic", "common"))
    from checks import check_zero, check_equal, check_true, check_numeric, report_checks

Semantics, identical across checks.wl / checks.py / checks.jl:

- a check **prints** what it found, and **then** asserts it;
- every check carries a short, stable label that a write-up cites;
- ``report_checks()`` prints a labelled tally and exits non-zero if anything failed.

Print-before-assert is not decoration. A check that asserts without ever printing what it
found is how a false PASS survives a whole session (``docs/failure_modes.md`` entry 1).
"""
from __future__ import annotations

import sys

_passed: int = 0
_failed: int = 0
_failures: list[str] = []


def _record(label: str, ok: bool, shown: object) -> bool:
    global _passed, _failed
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}  ->  {shown}")
    if ok:
        _passed += 1
    else:
        _failed += 1
        _failures.append(label)
    return ok


def _simplify(expr):
    """Simplify with sympy if the expression is symbolic; otherwise pass through."""
    try:
        import sympy
        if isinstance(expr, sympy.Basic):
            return sympy.simplify(expr)
    except ImportError:
        pass
    return expr


def check_zero(label: str, expr) -> bool:
    """Print `expr` and check it is identically zero."""
    value = _simplify(expr)
    return _record(label, value == 0, value)


def check_equal(label: str, got, want) -> bool:
    """Print both sides and their difference, and check they are equal."""
    difference = _simplify(got - want) if hasattr(got, "__sub__") else None
    ok = (difference == 0) if difference is not None else (got == want)
    return _record(label, bool(ok), f"{got} vs {want}  difference: {difference}")


def check_true(label: str, condition) -> bool:
    """Print `condition` and check it is true."""
    return _record(label, bool(condition), condition)


def check_numeric(label: str, got, want, tol: float = 1e-10) -> bool:
    """Print both values and their absolute difference, and check |got - want| <= tol."""
    difference = abs(got - want)
    return _record(label, difference <= tol,
                   f"{got} vs {want}  |diff|: {difference}  tol: {tol}")


def report_checks(exit_on_failure: bool = True) -> int:
    """Print the tally; exit non-zero if any check failed."""
    print(f"--- checks: {_passed} passed, {_failed} failed")
    if _failed:
        print(f"--- failed labels: {_failures}")
        if exit_on_failure:
            sys.exit(1)
    return _passed
