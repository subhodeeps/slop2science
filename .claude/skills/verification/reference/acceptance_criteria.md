# Acceptance criteria — the gate a number passes to become a result

The project's own numerical thresholds live in one place in code (a single constants module
or its equivalent), never duplicated across drivers: duplicated tolerances drift, and then
two runs "pass" against different bars. This file says which criteria exist and how to choose
their values; `docs/validation_protocol.md` is the protocol they belong to.

## Status ladder

| Status | Meaning |
|---|---|
| `candidate` | produced by a solver. No claim is attached to it. |
| `accepted` | passed every applicable criterion below, at a stated resolution and precision, with a record. |
| `flagged` | reproducible but failing a criterion, or outside the regime where a criterion applies. **Not** a result; the reason is recorded in the record. |
| `rejected` | shown to be an artefact. Kept, with the diagnostic that rejected it. |

A record whose `status` is `accepted` while any of its own flags is true is a contradiction,
and `make check-docs` fails on it.

## Criteria

1. **Original-problem residual** below a stated, documented norm and threshold. State the
   norm; a scaled and an unscaled residual differ by orders of magnitude.
2. **Resolution stability**: `Δ = |x_2N − x_N|` below threshold. For near-zero quantities use
   absolute as well as relative.
3. **Precision stability**: the value moves by less than the threshold when the precision
   tier is raised. This is the criterion most often skipped and most often decisive.
4. **Solution-shape convergence**: overlap or pointwise difference of the normalized solution
   between resolutions, in the same variables and conventions.
5. **Boundary/asymptotic regularity**: the computed solution behaves as the formulation's
   factorization requires. A result that violates this has usually satisfied the wrong
   boundary condition.
6. **Continuation**: reachable continuously along a parameter path, matched by overlap.
7. **Independent benchmark**: agreement with a different-method source, to that source's
   printed precision, with the conversion written out. Same-method agreement does not satisfy
   this criterion.

## Choosing thresholds

- Derive them from the precision and resolution actually used, not from what the data happens
  to satisfy. A threshold set after seeing the numbers is not a criterion.
- Record where each threshold came from, next to its value.
- **Never widen a threshold to admit a result.** If a result needs a wider bar, either the
  formulation or the discretization is the problem, and the finding is a
  `DISCRETIZATION`/`CONDITIONING` one.
- A criterion that does not apply is recorded as not applicable, with the reason. It is never
  silently dropped.

## What no threshold can establish

Clean convergence of a wrong operator. Every criterion above tests whether the problem was
solved accurately; only criterion 7 and an exact known answer test whether it was the right
problem. Do not let 1–6 passing stand in for 7.
