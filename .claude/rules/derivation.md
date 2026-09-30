---
paths:
  - "symbolic/**"
  - "derivation/**"
---

# Derivation work — rules

Derivations are a deliverable in their own right (CLAUDE.md §2); these rules are what keeps
each one re-runnable and citable.

## Ownership

- Every topic has exactly one tool that is the **record** for it, declared in
  `docs/toolchain.md` and repeated in each stage script's header. Undeclared ownership is a
  defect. Two records for one fact is a defect.
- A derivation of the same result in another tool is a **cross-check**, labelled as such in
  its header and in `validation/`, and it never becomes the record.

## One derivation per file

- One stage, one script: `symbolic/<topic>/stage_NN_<what>.<ext>`. Never combine two stages;
  never append a new derivation to an existing script. A `PreToolUse` hook blocks `Write` to
  an existing stage or export script — a new stage is a new numbered file.
- One write-up per stage: `derivation/<topic>/NN_<what>.md`, citing its script at every
  displayed equation.
- A sub-derivation long enough to stand alone gets its own numbered stage and write-up, not a
  section inside another one's.
- Order comes from `symbolic/<topic>/stages.txt`, never from a shell glob.

## Every script

Header comment states, in this order:

    Topic:          <topic>
    Stage:          NN — <what this stage establishes>
    Owner tool:     <the tool that is the record for this topic>
    Kind:           REPRODUCTION | EXTENSION | CROSS-CHECK
    Judged against: <the source's Eq./Table N, or the named benchmark/physics>
    Inputs:         <previous stage outputs it loads>
    Outputs:        <what it writes, including its out/ record>

Body rules:

- Shared helper code lives in `symbolic/common/`, loaded by path from `PROJECT_ROOT`, never
  copy-pasted between stages.
- **Print before asserting.** Every non-trivial step prints what it found and *then* checks
  it. Asserting an expected value and reading the printout only when something looks wrong is
  how a wrong assertion survives; this project's ancestor caught exactly one such case, and
  only because the printed invariant contradicted the assertion.
- Every check carries a short, stable, quoted **label**. Write-ups cite labels, so renaming
  one silently breaks a citation (`make check-evidence` catches the break).
- The script exits non-zero on any failed check. A script that can fail silently is not a
  check.
- Persist stage results as text under `symbolic/<topic>/out/`, never as a version-specific
  binary format.

## Retention

Scripts and write-ups are the permanent record and are committed. **Never delete one.**
Supersede by adding a new numbered stage and noting the change in the old script's header and
in `docs/decision_log.md`.

## Exporting to another tool

- Hand-off is always machine-generated: `export_NN_<what>.<ext>` writes into
  `symbolic/generated/<lang>/`, and `make codegen-check TOPIC=<topic>` must be clean.
- Generated files carry a banner with the generating script and its SHA-256.
- Never hand-transcribe an expression between tools, in either direction, not even a short
  one, not even temporarily.
