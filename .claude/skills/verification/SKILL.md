---
name: verification
description: Independent audit of derivations, generated code, solvers, results, convergence, precision and benchmark comparisons, with a fixed failure taxonomy. Use it after any derivation, export or solver change, and before you report any number.
when_to_use: 'Trigger phrases: verify, audit, check this result, is this converged, is this right, before reporting, limit check, independent check, review the derivation'
---

# Scientific verification

The audit finds failures and classifies them. It does **not** fix them. A bug that someone fixes
quietly is a finding that nobody recorded. A hook blocks the `verification` agent from writing
project files for this reason.

## Derivation checks

- the substitution residual: put the result back into what it came from. It must be identically
  zero.
- dimensional and scaling consistency
- a limiting or special case with an independently known answer
- consistency with constraints: does the result satisfy relations that the derivation did not use?
- back-substitution of each intermediate reduction
- where the stage claims to reproduce something, a comparison with the source **coefficient by
  coefficient**, not a visual comparison
- where it is feasible, an independent second route. This is a different derivation. It is not
  the same route typed again.

## Checks of generated code

- `make codegen-check TOPIC=<topic>` is clean
- the SHA in the banner matches the current generating script
- no hand edits (`git log` and `git blame` on `symbolic/generated/`)
- a round-trip test: the consuming tool evaluates the generated expression at reference points
  and matches the values of the generating tool

## Numerical checks, for each accepted result

- the residual in the **original** problem, not in the reformulation
- resolution refinement: `N` and `2N`, with `Δ` recorded
- precision refinement: a result that changes with precision has not converged
- regularity of the computed solution at the boundary and in the asymptotic region
- convergence of the solution shape, not only of the scalar (overlap or pointwise difference)
- parameter continuation where a parameter exists, matched by overlap and not by ordering
- an independent-method benchmark with the conversion written out
- the record exists and is complete (`docs/validation_protocol.md` §12)

## Adversarial verification

If a claim carries real weight, do not "check" it. **Attack it.** One agent proves. A second agent
attacks the proof. The second agent sees **only the numbered artifact.** It never sees the
reasoning of the prover or the expectation of the dispatcher. `reference/adversarial_protocol.md`
gives the protocol. It also states when the two dispatches are worth it and when the script is
the better verifier.

Two points decide if it works:

- **Do not tell the verifier what you hope that it finds.** "Check that this is right" and
  "attack this" produce different behaviour from the same model. The first is sycophancy that
  waits to happen (`docs/failure_modes/model.md` 0c).
- **Two runs of the same model on the same input are not independent.** Where a claim
  matters, a verifier from a different model family shares fewer failure modes. Never report two
  runs of one model as independent confirmation.

## Failure taxonomy

Give each finding exactly one class:

| Class | Meaning |
|---|---|
| `ALGEBRAIC` | A sign, factor or term is wrong in an otherwise correct formulation. |
| `FORMULATION` | The problem that the work solves is not the intended problem. |
| `DISCRETIZATION` | The approximation, grid or map is inadequate, or the work imposes it wrongly. |
| `CONDITIONING` | The computation is ill-conditioned or limited by precision. |
| `IDENTIFICATION` | A result has the wrong label or order, or someone took a solver artefact as real. |
| `BENCHMARK` | The comparison is not valid: convention, method or provenance. |
| `PHYSICAL` | The result violates a limit, a symmetry or a physical requirement. |
| `IMPLEMENTATION` | The code does not do what the formulation says. |
| `REPRODUCIBILITY` | You cannot obtain the result again from the repository as committed. |
| `PROVENANCE` | The cited evidence of a claim does not establish it, or does not exist. |

`PROVENANCE` is the class that the automated checks cannot find. `make check-evidence` verifies
that a cited label *exists*. To decide if the check behind that label establishes the claim, you
must read the script. This is the most valuable output of the audit.

## Report format

    ID | class | evidence (the command run and its actual output) | severity | suggested check

A hook blocks the Edit and Write tools of the verifier on project files. It records its report as a new file
`docs/audits/<YYYYMMDD>_<topic>.md` (see `docs/audits/README.md`) and returns the same text.

Rules:

- **Never report a pass that you did not observe.** If you did not run a command, say so. Do not
  infer the outcome from the code.
- Quote the actual output. A paraphrase of a result is not evidence.
- Separate "this is wrong" from "this is not supported". The fixes are different.
- Severity is about consequence. It is not about confidence. A wrong sign in a coefficient that
  everything depends on is high severity, even if the fix is one character.

## When to stop

Stop when an independent derivation confirms the result by a different route. Also, the
literature must agree, or you must have a stated reason why you cannot check the result against
the literature. Then say that the audit is complete. More confirmation of a result that several
independent routes already agree on is not rigour. It shows a lack of trust in the verification
loop (`docs/failure_modes.md`).
