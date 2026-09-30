# code — external and PI-supplied code

Not part of the production pipeline (`src/`, `symbolic/`). This tree holds code that enters
the project from outside it, so that it is neither lost nor allowed to drift into the pipeline
unattributed.

    reference/<topic>/    third-party code kept for reference. Committed. Never imported,
                          never run by the pipeline.
    pi/<topic>/           the PI's own code, as supplied, unmodified. Committed.
    unused/               supplied code that turned out not to fit, kept with the reason why.
                          "We tried this and it did not work" is information.
    _drop/                the PI's transient drop folder. Gitignored except its README.

Code adapted for actual use goes to its normal home (`src/`, `validation/`,
`symbolic/common/`), rewritten to this project's interfaces and carrying the attribution block
from `.claude/skills/external-code/SKILL.md` — **and** the original still moves to
`reference/` or `pi/`, so what the adaptation came from stays available.

## Two things this tree must never become

- **A source of physics.** An external solver's coefficient function is exactly as untrusted
  as a coefficient typed out of a paper. Equations enter through `symbolic/generated/` from
  this project's own derivation (CLAUDE.md §5).
- **A source of unattributed technique.** Consulting an implementation and then writing your
  own is still consulting it. The line to avoid crossing is not copying — it is failing to
  record what you looked at, which commit, and under what licence.

Intake procedure, and the questions to ask the PI before reading a dropped file closely:
`.claude/skills/external-code/reference/pi_code_intake.md`.
