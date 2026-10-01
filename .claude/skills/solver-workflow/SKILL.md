---
name: solver-workflow
description: Design, implement and audit a production solver from generated coefficients: discretization, assembly, eigen/root solving, residuals, resolution and precision studies, filtering of spurious results, parameter continuation. Use it when you build or debug anything in src/ or validation/.
when_to_use: 'Trigger phrases: solver, implement the numerics, discretization, collocation, eigenvalues, root finding, residual, convergence, N vs 2N, precision study, spurious modes, parameter continuation, mode tracking'
paths:
  - "src/**"
  - "tests/**"
  - "validation/**"
---

# Solver workflow

For execution details, see the `toolchain` skill. For the rules that a checker enforces, see
`.claude/rules/implementation.md`. For the acceptance gates, see `docs/validation_protocol.md`.
For the formulation checklist before you write code, see `reference/formulation_checklist.md`.

## Order of work

The order is the point. Each step is cheap now and expensive to add later.

1. **Formulation, on paper and in the derivation.** State the problem that the solver solves.
   Include the boundary and asymptotic factors that you pull out. Include the variable to which
   you map the domain. Include the structure in which the unknown parameter enters. This belongs in
   `derivation/`, verified by a stage script, *before* any code exists. If you write the solver
   first and infer the formulation from what makes it converge, the artefacts of the solver
   validate a wrong formulation.
2. **Export the coefficients** to `symbolic/generated/<lang>/`, with `make codegen-check` clean.
   Nothing in the solver comes by hand from a paper.
3. **Write the known-answer test first.** Use a problem with an exact closed-form solution. Run
   it through **the full chain that the real solver uses** (assembly, solve, refinement,
   acceptance), in each precision that the project uses. Do not write a unit test of each piece.
   A chain can be correct piece by piece and wrong from end to end. Only this test finds that
   fault.
4. **Run the real problem at small size, with a dense and simple method.** Print the whole computed
   spectrum or solution set. Do not print only the part that you expected.
5. **Evaluate residuals in the original problem.** A residual in the reformulation that the
   solver uses internally proves only that the solver solved the reformulation.
6. **Do the resolution study.** Solve at `N` and `2N`. Record `Δ = |x_2N − x_N|`. For quantities
   near zero, record the absolute change and the relative change.
7. **Do the precision study.** Repeat representative cases at higher precision. If a result
   changes with precision, it has not converged, whatever its residual says.
8. **Filter with a diagnostic. Never filter by eye.** Flag outputs that are sensitive to
   resolution or precision, outputs with a poor residual, outputs that are irregular at the
   boundary, and outputs that you cannot continue. Record why you discarded each one. Never
   discard an unusual result without a diagnostic. It is an artefact that you can name, or it is
   a result that you did not expect.
9. **Do the parameter continuation.** Follow a solution along a parameter path. Match by
   proximity *and* by overlap of the eigenvector or solution. Do not match by ordering. The
   ordering swaps at near-degeneracies and gives all later results the wrong labels.
10. **Compare with an independent benchmark, with the conversion written out.** State the method
    of the benchmark. Agreement with the same method cannot validate the method.
11. **Record.** The run writes its own record (`docs/validation_protocol.md` §12). Only then is
    the output a result and not a candidate.

## Things that look like success and are not success

- **Clean convergence of a wrong recurrence or a wrong operator.** A wrong formulation can
  converge beautifully to the wrong answer. Convergence alone says nothing about correctness.
  Only an independent benchmark or an exact known answer does.
- **A small residual in the linearized or companion problem.** See step 5.
- **Agreement to a tolerance that nobody stated.** State the tolerance and its origin before you
  compare.
- **A result that matches a published table** when the same method produced the table. That is a
  consistency check. It is not validation.
- **A spectrum that looks right.** Print all of it. The artefacts are usually visible, and
  people usually ignore them.

## Code that is generic in precision

Write each numerical routine generic in its element type. Then the identical code path runs at
working precision and at extended precision. A precision study that runs different code at each
precision compares two implementations. It is not a convergence study.
