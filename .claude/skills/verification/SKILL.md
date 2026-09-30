---
name: verification
description: Independent audit of derivations, generated code, solvers, results, convergence, precision and benchmark comparisons, with a fixed failure taxonomy. Use after any derivation, export or solver change, and before any number is reported.
when_to_use: 'Trigger phrases: verify; audit; check this result; is this converged; is this right; before reporting; limit check; independent check; review the derivation'
---

# Scientific verification

The audit finds and classifies failures. It does **not** fix them: a bug quietly fixed is a
finding nobody recorded, and the `verification` agent is hook-blocked from writing project
files for that reason.

## Derivation checks

- substitution residual — put the result back into what it came from; identically zero;
- dimensional and scaling consistency;
- a limiting or special case with an independently known answer;
- constraint consistency — does the result satisfy relations not used in deriving it;
- back-substitution of every intermediate reduction;
- comparison with the source **coefficient by coefficient**, not visually, where the stage
  claims to reproduce something;
- an independent second route where feasible — a genuinely different derivation, not the same
  route retyped.

## Generated-code checks

- `make codegen-check TOPIC=<topic>` clean;
- banner SHA matches the current generating script;
- no hand edits (`git log`/`git blame` on `symbolic/generated/`);
- a round-trip test: the consuming tool evaluates the generated expression at reference
  points and matches the generating tool's own values.

## Numerical checks, per accepted result

- residual in the **original** problem, not the reformulation;
- resolution refinement: `N` and `2N`, with `Δ` recorded;
- precision refinement: a result that moves with precision is unresolved;
- boundary/asymptotic regularity of the computed solution;
- solution-shape convergence, not just the scalar (overlap or pointwise difference);
- parameter continuation where a parameter exists, matched by overlap and not by ordering;
- an independent-method benchmark with the conversion written out;
- the record exists and is complete (`docs/validation_protocol.md` §12).

## Failure taxonomy

Every finding gets exactly one class:

| Class | Meaning |
|---|---|
| `ALGEBRAIC` | a sign, factor or term is wrong in an otherwise correct formulation |
| `FORMULATION` | the problem being solved is not the intended problem |
| `DISCRETIZATION` | the approximation, grid or map is inadequate or wrongly imposed |
| `CONDITIONING` | the computation is ill-conditioned or precision-limited |
| `IDENTIFICATION` | a result is mislabelled, misordered, or is a solver artefact taken as real |
| `BENCHMARK` | the comparison is invalid — convention, method or provenance |
| `PHYSICAL` | a limit, symmetry or physical requirement is violated |
| `IMPLEMENTATION` | the code does not do what the formulation says |
| `REPRODUCIBILITY` | the result cannot be re-obtained from the repository as committed |
| `PROVENANCE` | a claim's cited evidence does not establish it, or does not exist |

`PROVENANCE` is the class the automated checks cannot find. `make check-evidence` verifies
that a cited label *exists*; whether the check behind that label actually establishes the
claim requires reading the script, and that is this audit's most valuable output.

## Report format

    ID | class | evidence (the command run and its actual output) | severity | suggested check

Rules:

- **Never report a pass you did not observe.** If a command could not be run, say so; do not
  infer the outcome from the code.
- Quote actual output. A paraphrase of a result is not evidence.
- Separate "this is wrong" from "this is unsupported". They need different fixes.
- Severity is about consequence, not confidence: a wrong sign in a coefficient everything
  depends on is high severity even if the fix is one character.

## When to stop

When an independent re-derivation confirms the result by a genuinely different route, **and**
either the literature agrees or there is a stated reason it cannot be checked against
literature — stop, and say the audit is complete. Chasing further confirmation of something
several independent routes already agree on is not rigour; it is not trusting the verification
loop (`docs/failure_modes.md`).
