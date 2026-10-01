---
paths:
  - "src/**"
  - "tests/**"
  - "validation/**"
---

# Production code — rules

- Put production code in `src/<lang>/`, tests in `tests/<lang>/` and validation drivers in
  `validation/<topic>/`. Run everything through `scripts/run`. Run tests through `make test`.
- **The PI decides the language of a solver and the route by which it receives coefficients**
  (`docs/toolchain.md`). The decision is a registry row, or the default profile and its default
  routes. Do not choose either yourself. Do not add a hand-off that neither the registry nor the
  default routes describe.
- **Coefficients and equations come only from `symbolic/generated/`.** If something that you
  need is missing, stop and report it. Never write it by hand. Never copy it from a paper. Never
  inline it "temporarily".
- Do not guess results. Do not put known answers in production code. A documented automated rule
  must give each shift, target, bracket or initial iterate. If the rule needs a scale, derive the
  scale.
- Write numerics that are generic in the element type. Then the identical code runs at working
  precision and at extended precision. Record the precisions at which you confirmed a result.
- Evaluate residuals in the **original** problem. Do not evaluate them only in the reformulation
  that the solver uses internally. A small residual in a linearization proves only that the
  solver solved the linearization.
- Use a dense method first, at small size, when the correctness of the method is easy to see. Move to an iterative or
  structured method only with a size estimate in the relevant document.
- Each run that produces a reportable number writes its own record (JSON). The record has the
  parameters, resolution, precision, residuals, benchmark and its method, tool versions and git
  commit (`docs/validation_protocol.md` §12). A hook protects records against hand edits. A
  changed number is a new run.
- Each module has a test file. For each topic, at least one test is a **known-answer** test. It
  uses a problem with an exact closed-form solution. It exercises the full chain that the real
  solver uses. It is not a separate unit test of each piece. A chain can be correct piece by
  piece and wrong from end to end.
- A solver output is a **candidate** until it passes the validation protocol. Use the word
  "candidate" in code comments, logs and reports until then.
