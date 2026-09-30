---
paths:
  - "src/**"
  - "tests/**"
  - "validation/**"
---

# Production code — rules

- Production code lives in `src/<lang>/`; tests in `tests/<lang>/`; validation drivers in
  `validation/<topic>/`. Run everything through `scripts/run`; tests through `make test`.
- **Coefficients and equations come only from `symbolic/generated/`.** If something you need
  is missing, stop and report it. Never hand-write it, never copy it from a paper, never
  "temporarily" inline it.
- No result guesses and no known answers in production code. A shift, target, bracket or
  initial iterate comes from a documented automated rule; if the rule needs a scale, derive
  the scale.
- Write numerics generic in the element type so the identical code runs at working and at
  extended precision. Record which precisions a result was confirmed at.
- Evaluate residuals in the **original** problem, not only in the reformulation the solver
  uses internally. A small residual in a linearization proves the linearization was solved.
- Prefer a dense, obviously-correct method at small size first; move to an iterative or
  structured method only with a size estimate recorded in the relevant doc.
- Every run that produces a reportable number writes its own record (JSON) with parameters,
  resolution, precision, residuals, benchmark and its method, tool versions and git commit
  (`docs/validation_protocol.md` §12). Records are hook-protected against hand editing: a
  changed number is a new run.
- Every module has a test file. At least one test per topic is a **known-answer** test
  against a problem with an exact closed-form solution, exercising the full chain the real
  solver uses — not a unit test of each piece separately. A chain can be correct piecewise
  and wrong end to end.
- A solver output is a **candidate** until it passes the validation protocol. Use the word
  "candidate" in code comments, logs and reports until it does.
