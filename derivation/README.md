# derivation — the human-readable derivations

**This is a primary deliverable. It is not a byproduct of the numerics** (CLAUDE.md §2). The
derivation of each topic must grow into a complete, self-contained, re-runnable reconstruction.
It starts with the equations of the source. It continues through the reduction to the form that
the solver uses. It must be publishable as an appendix or as a separate methods paper.

## Shape

Use one file for each stage: `<topic>/NN_<stage>.md`. It mirrors
`symbolic/<topic>/stage_NN_<stage>.<ext>`.

Each file states the conventions and assumptions that it uses and the displayed equations. For
**each** displayed equation, it gives an evidence tag. The tag names the script that verifies
the equation. It also names the exact label of the check:

    [E: `symbolic/<topic>/stage_04_reduce.wls`, "reduced system matches source Eq. (9)"]

Put two lines under the title:

    Kind:           REPRODUCTION | EXTENSION | CROSS-CHECK
    Judged against: <the source's Eq./Table N> | <benchmark/physics, named>

**Never display an equation that no script checks.** You can do algebra by hand between two
checked expressions. State it one time and mark it.

## Retention

The write-ups and their scripts are the permanent record. Commit them together. **Never delete
one.** To supersede a stage, add a new numbered stage. Note the change in the header of the old
script and in `docs/decision_log.md`. A hook blocks the overwrite of an existing stage script,
because the write-ups cite these scripts by name.

Full rules: `.claude/rules/derivation.md`. Checklist for each stage:
`.claude/skills/derivation-workflow/reference/stage_checklist.md`.

## Topic index

| Topic | Stages | Status |
|---|---|---|
| | | |
