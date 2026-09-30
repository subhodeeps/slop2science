---
name: solver-workflow
description: Design, implement and audit a production solver from generated coefficients - discretization, assembly, eigen/root solving, residuals, resolution and precision studies, spurious-result filtering, parameter continuation. Use when building or debugging anything in src/ or validation/.
when_to_use: 'Trigger phrases: solver; implement the numerics; discretization; collocation; eigenvalues; root finding; residual; convergence; N vs 2N; precision study; spurious modes; parameter continuation; mode tracking'
paths:
  - "src/**"
  - "tests/**"
  - "validation/**"
---

# Solver workflow

Execution details: the `toolchain` skill. Rules a checker enforces:
`.claude/rules/implementation.md`. Acceptance gates:
`docs/validation_protocol.md`. Formulation checklist before writing code:
`reference/formulation_checklist.md`.

## Order of work

The order is the point. Each step is cheap to do now and expensive to retrofit.

1. **Formulation, on paper and in the derivation** — the problem the solver will actually
   solve, including the boundary/asymptotic factors pulled out, the variable the domain is
   mapped to, and the structure the unknown parameter enters with. This belongs in
   `derivation/`, verified by a stage script, *before* any code exists. Writing the solver
   first and inferring the formulation from what makes it converge is how a wrong
   formulation gets validated by its own artefacts.
2. **Coefficients exported** — `symbolic/generated/<lang>/`, with `make codegen-check` clean.
   Nothing in the solver is written by hand from a paper.
3. **Known-answer test first** — a problem with an exact closed-form solution, run through
   **the full chain the real solver uses** (assembly, solve, refinement, acceptance), in every
   precision the project will use. Not a unit test of each piece: a chain can be correct
   piece by piece and wrong end to end, and this test is the only thing that catches that.
4. **The real problem, at small size, densely and simply.** Print the whole computed
   spectrum/solution set, not the part you expected.
5. **Residuals in the original problem.** A residual computed in the reformulation the solver
   uses internally proves only that the reformulation was solved.
6. **Resolution study** — solve at `N` and `2N`; record `Δ = |x_2N − x_N|`. For
   near-zero quantities record absolute as well as relative change.
7. **Precision study** — repeat representative cases at higher precision. A result that moves
   with precision is unresolved, whatever its residual says.
8. **Filtering with a diagnostic, never by eye.** Flag resolution-sensitive,
   precision-sensitive, poor-residual, boundary-irregular and non-continuable outputs. Record
   why each was discarded. Never discard an unusual result without a diagnostic — it is
   either an artefact you can name or a result you did not expect.
9. **Parameter continuation** — follow a solution along a parameter path and match by
   proximity *and* eigenvector/solution overlap, not by ordering. Ordering swaps at
   near-degeneracies and mislabels everything downstream.
10. **Independent benchmark, with the conversion written out.** State the benchmark's method:
    same-method agreement cannot validate the method.
11. **Record** — the run writes its own record (`docs/validation_protocol.md` §12). Then, and
    only then, is the output a result rather than a candidate.

## Things that look like success and are not

- **Clean convergence of a wrong recurrence or wrong operator.** A wrong formulation can
  converge beautifully to the wrong answer; convergence alone catches nothing about
  correctness. Only an independent benchmark or an exact known answer does.
- **A small residual in the linearized or companion problem.** See step 5.
- **Agreement to a tolerance nobody stated.** State the tolerance and where it came from
  before comparing.
- **A result that matches a published table** when the published table was produced by the
  same method. That is a consistency check, not validation.
- **A spectrum that looks right.** Print it all; the artefacts are usually visible and
  usually ignored.

## Generic-precision code

Write every numerical routine generic in its element type, so the identical code path runs at
working and extended precision. A precision study that runs different code at each precision
is a comparison of two implementations, not a convergence study.
