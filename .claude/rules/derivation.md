---
paths:
  - "symbolic/**"
  - "derivation/**"
---

# Derivation work — rules

Derivations are a deliverable in their own right (CLAUDE.md §2). These rules keep each
derivation re-runnable and citable.

## Ownership

Tool ownership follows the registry in `docs/toolchain.md` (CLAUDE.md §5). Repeat the owner tool
in the header of each stage script. Label a derivation of the same result in another tool as a
cross-check, in its header and in `validation/`.

## One derivation in each file

- Use one script for each stage: `symbolic/<topic>/stage_NN_<what>.<ext>`. Never combine two
  stages. Never append a new derivation to an existing script. A `PreToolUse` hook blocks `Write`
  to an existing stage or export script. A new stage is a new numbered file.
- Use one write-up for each stage: `derivation/<topic>/NN_<what>.md`. It cites its script at each
  displayed equation.
- If a sub-derivation is long enough to stand alone, give it its own numbered stage and
  write-up. Do not make it a section of another stage.
- The order comes from `symbolic/<topic>/stages.txt`. Never use a shell glob for the order.

## Write-ups

- Give each displayed equation an evidence tag: the verifying script and the exact check label.
- You can do algebra by hand between two checked expressions. State it one time, briefly, and
  mark it: "by hand between <label 1> and <label 2>".
- If an equation has no check and no such mark, do not put it in the write-up.

## Each script

The header comment states these items, in this order:

    Topic:          <topic>
    Stage:          NN — <what this stage establishes>
    Owner tool:     <the tool that is the record for this topic>
    Kind:           REPRODUCTION | EXTENSION | CROSS-CHECK
    Judged against: <the source's Eq./Table N, or the named benchmark/physics>
    Inputs:         <previous stage outputs it loads>
    Outputs:        <what it writes, including its out/ record>

Rules for the body:

- Put shared helper code in `symbolic/common/`. Load it by path from `PROJECT_ROOT`. Never copy
  it between stages.
- **Print before you assert.** Each non-trivial step prints what it found and *then* checks it.
  If you assert an expected value and read the printout only when something looks wrong, a wrong
  assertion survives. The ancestor of this project caught exactly one such case. It caught it
  only because the printed invariant contradicted the assertion.
- Each check has a short, stable, quoted **label**. Write-ups cite labels. If you rename a
  label, you break a citation silently (`make check-evidence` catches the break).
- The script exits with a non-zero code on any failed check. A script that can fail silently is
  not a check.
- Save the results of a stage as text under `symbolic/<topic>/out/`. Never use a binary format
  that depends on a version.

## Retention

Scripts and write-ups are the permanent record. Commit them. **Never delete one.** To supersede
a script, add a new numbered stage. Note the change in the header of the old script and in
`docs/decision_log.md`.

## Export to another tool

- Always generate the hand-off by machine. `export_NN_<what>.<ext>` writes into
  `symbolic/generated/<lang>/`. `make codegen-check TOPIC=<topic>` must be clean.
- Each generated file has a banner with the generating script and its SHA-256.
- Never transcribe an expression by hand between tools, in either direction. This applies also
  to a short expression and to a temporary expression.
