# Acceptance criteria — the gate that a number passes to become a result

The numerical thresholds of the project live in one place in code (a single constants module or
its equivalent). Never duplicate them across drivers. Duplicated tolerances drift. Then two runs
"pass" against different bars. This file states which criteria exist and how to choose their
values. `docs/validation_protocol.md` is the protocol that the criteria belong to.

## Status ladder

| Status | Meaning |
|---|---|
| `candidate` | A solver produced it. No claim is attached to it. |
| `accepted` | It passed each applicable criterion below, at a stated resolution and precision, with a record. |
| `flagged` | You can reproduce it, but it fails a criterion, or it is outside the regime where a criterion applies. It is **not** a result. The record states the reason. |
| `rejected` | Someone showed that it is an artefact. Keep it, with the diagnostic that rejected it. |

A record with `status` equal to `accepted` and one of its own flags set to true is a
contradiction. `make check-docs` fails on it.

## Criteria

1. **Residual in the original problem.** The residual is below a stated, documented norm and
   threshold. State the norm. A scaled and an unscaled residual differ by orders of magnitude.
2. **Resolution stability.** `Δ = |x_2N − x_N|` is below the threshold. For quantities near
   zero, use the absolute change and the relative change.
3. **Precision stability.** The value changes by less than the threshold when you raise the
   precision tier. Teams skip this criterion most often. It is also the most often decisive.
4. **Convergence of the solution shape.** Compare the overlap or the pointwise difference of the
   normalized solution between resolutions. Use the same variables and conventions.
5. **Regularity at the boundary and in the asymptotic region.** The computed solution behaves as
   the factorization of the formulation requires. A result that violates this has usually
   satisfied the wrong boundary condition.
6. **Continuation.** You can reach the result continuously along a parameter path, matched by
   overlap.
7. **Independent benchmark.** The result agrees with a source that uses a different method, to
   the printed precision of that source, with the conversion written out. Agreement with the
   same method does not satisfy this criterion.

## Choose thresholds

- Derive the thresholds from the precision and resolution that you use. Do not derive
  them from what the data happens to satisfy. A threshold that you set after you see the numbers
  is not a criterion.
- Record the origin of each threshold next to its value.
- **Never widen a threshold to admit a result.** If a result needs a wider bar, the problem is
  the formulation or the discretization. The finding is then a `DISCRETIZATION` or
  `CONDITIONING` finding.
- If a criterion does not apply, record it as not applicable, with the reason. Never drop it
  silently.

## What no threshold can establish

A wrong operator can converge cleanly. Each criterion above tests if the solver solved the
problem accurately. Only criterion 7 and an exact known answer test if it was the right
problem. Do not let criteria 1–6 stand in for criterion 7.
