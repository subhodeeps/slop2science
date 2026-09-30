# derivation — the human-readable derivations

**A primary deliverable, not a byproduct of the numerics** (CLAUDE.md §2). Each topic's
derivation must accumulate into a complete, self-contained, re-runnable reconstruction — from
the source's equations through the reduction to whatever the solver consumes — publishable as
an appendix or a standalone methods paper in its own right.

## Shape

One file per stage: `<topic>/NN_<stage>.md`, mirroring `symbolic/<topic>/stage_NN_<stage>.<ext>`.

Each states: the conventions and assumptions used, the displayed equations, and for **every**
displayed equation an evidence tag naming the verifying script and its exact check label:

    [E: `symbolic/<topic>/stage_04_reduce.wls`, "reduced system matches source Eq. (9)"]

Under the title, two lines:

    Kind:           REPRODUCTION | EXTENSION | CROSS-CHECK
    Judged against: <the source's Eq./Table N> | <benchmark/physics, named>

**Never display an equation that no script checks.** Algebra done by hand between two checked
expressions is allowed, stated once and marked as such.

## Retention

Write-ups and their scripts are the permanent record and are committed together. **Never
delete one.** Supersede by adding a new numbered stage and noting the change in the old
script's header and in `docs/decision_log.md`. A hook blocks overwriting an existing stage
script, because the write-ups cite these scripts by name.

Full rules: `.claude/rules/derivation.md`. Per-stage checklist:
`.claude/skills/derivation-workflow/reference/stage_checklist.md`.

## Topic index

| Topic | Stages | Status |
|---|---|---|
| | | |
