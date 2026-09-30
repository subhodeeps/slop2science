"""
    checks.jl — print-before-assert check helpers for derivation stages.

Include with:

    include(joinpath(ENV["PROJECT_ROOT"], "symbolic", "common", "checks.jl"))
    using .Checks

Semantics, identical across `checks.wl` / `checks.py` / `checks.jl`:

- a check **prints** what it found, and **then** asserts it;
- every check carries a short, stable label that a write-up cites;
- `report_checks()` prints a labelled tally and exits non-zero if anything failed.

Print-before-assert is not decoration. A check that asserts without ever printing what it
found is how a false PASS survives a whole session (`docs/failure_modes.md` entry 1).
"""
module Checks

export check_zero, check_equal, check_true, check_numeric, report_checks

const PASSED   = Ref(0)
const FAILED   = Ref(0)
const FAILURES = String[]

function _record(label::AbstractString, ok::Bool, shown)
    println("  [", ok ? "PASS" : "FAIL", "] ", label, "  ->  ", shown)
    if ok
        PASSED[] += 1
    else
        FAILED[] += 1
        push!(FAILURES, String(label))
    end
    return ok
end

"Print `expr` and check it is (numerically) zero."
check_zero(label::AbstractString, expr; tol = 1e-12) =
    _record(label, abs(expr) <= tol, expr)

"Print both sides and their difference, and check they agree."
function check_equal(label::AbstractString, got, want; tol = 1e-12)
    d = got - want
    _record(label, abs(d) <= tol, "$got vs $want  difference: $d")
end

"Print `condition` and check it is true."
check_true(label::AbstractString, condition) =
    _record(label, Bool(condition), condition)

"Print both values and their absolute difference, and check |got - want| <= tol."
function check_numeric(label::AbstractString, got, want, tol = 1e-10)
    d = abs(got - want)
    _record(label, d <= tol, "$got vs $want  |diff|: $d  tol: $tol")
end

"Print the tally; exit non-zero if any check failed."
function report_checks(; exit_on_failure::Bool = true)
    println("--- checks: ", PASSED[], " passed, ", FAILED[], " failed")
    if FAILED[] > 0
        println("--- failed labels: ", FAILURES)
        exit_on_failure && exit(1)
    end
    return PASSED[]
end

end # module
