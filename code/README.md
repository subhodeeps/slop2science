# code — external and PI-supplied code

This tree is not part of the production pipeline (`src/`, `symbolic/`). It holds code that
enters the project from outside. The tree keeps this code safe. It also keeps this code out of
the pipeline unless someone attributes it.

    reference/<topic>/    third-party code kept for reference. Committed. The pipeline never
                          imports it and never runs it.
    pi/<topic>/           the PI's own code, as supplied, unchanged. Committed.
    unused/               supplied code that did not fit, kept with the reason.
                          "We tried this and it did not work" is information.
    _drop/                the transient drop folder of the PI. Gitignored, except its README.

Adapted code goes to its normal place (`src/`, `validation/`, `symbolic/common/`). Rewrite it
to the interfaces of this project. Add the attribution block from
`.claude/skills/external-code/SKILL.md`. The original must also move to `reference/` or
`pi/`. Then the source of the adaptation stays available.

## Two things this tree must never become

- **A source of physics.** The coefficient function of an external solver is as untrusted as a
  coefficient that someone types from a paper. Equations enter through `symbolic/generated/`,
  from the derivation that this project makes (CLAUDE.md §5).
- **A source of unattributed technique.** If you consult an implementation and then write your
  own, you still consulted it. Copying is not the line to avoid. The line to avoid is failing
  to record what you looked at, which commit, and under which licence.

For the intake procedure, and the questions to ask the PI before you read a dropped file
closely, see `.claude/skills/external-code/reference/pi_code_intake.md`.
