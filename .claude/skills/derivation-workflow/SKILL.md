---
name: derivation-workflow
description: The reproducible derivation cycle - one stage per script, print-before-assert checks with stable labels, a write-up citing every equation, then export. Use for any symbolic derivation stage, source reconstruction, asymptotic analysis or limit check.
when_to_use: 'Trigger phrases: derive; derivation stage; reconstruct the equations; linearize; reduce the system; indicial exponents; asymptotic analysis; series expansion; limiting case; export coefficients'
paths:
  - "symbolic/**"
  - "derivation/**"
---

# Derivation workflow

Execution details for each tool: the `toolchain` skill. Rules that a hook or a checker
enforces: `.claude/rules/derivation.md`. Stage template:
`templates/stage_template.wls` (adapt the header for `.py`/`.jl`). Per-stage checklist:
`reference/stage_checklist.md`.

## The cycle

**1. Derive** — one stage, one script, `symbolic/<topic>/stage_NN_<what>.<ext>`, in the tool
that owns the topic. Add it to `symbolic/<topic>/stages.txt`.

**2. Check, inside the same script** — every non-trivial step gets an explicit check with a
short quoted label, and **the value is printed before it is asserted**. Order matters: print,
then assert. Asserting first and reading the output only when something looks wrong is how a
wrong assertion survives a whole session.

Checks worth having at every stage:

- substitute the result back into what it came from; the residual should be identically zero;
- a limiting or special case whose answer is known independently;
- dimensional or scaling consistency;
- an invariant the result must satisfy that was not used in deriving it;
- where the stage reproduces the source: a coefficient-by-coefficient comparison against the
  source's displayed equation, not a visual one.

**3. Write up** — `derivation/<topic>/NN_<what>.md`: conventions used, assumptions, the
displayed equations, and for every displayed equation an evidence tag naming the script and
the exact check label:

    [E: `symbolic/<topic>/stage_04_reduce.wls`, "reduced system matches source Eq. (9)"]

A displayed equation with no citable check does not go in the write-up. Algebra done by hand
between two checked expressions is allowed, stated once, briefly, and marked as such.

**4. Commit** script and write-up together. Not deferred to a cleanup pass — a write-up
committed a week after its script is how a stale citation appears.

**5. Export, if the stage produces coefficients another tool needs** —
`export_NN_<what>.<ext>` writing to `symbolic/generated/<lang>/`, then
`make codegen-check TOPIC=<topic>`. Never hand-transcribe.

## Each stage's header

    Topic / Stage / Owner tool / Kind (REPRODUCTION|EXTENSION|CROSS-CHECK) /
    Judged against / Inputs / Outputs

`Kind:` and `Judged against:` are not bookkeeping. Reproduction evidence and extension
evidence carry different weight, and a write-up that lets a benchmark comparison read as if
it validated the source's own reproduction is a real and easy mistake
(`docs/WORKFLOW.md` §5).

## When a check fails

Stop. Report the failing check, its exact output, and its class
(`.claude/skills/verification/SKILL.md`). Do not adjust the check to pass, change an expected
value, or widen a tolerance without recording why in the script and the write-up. If the fix
is not obviously correct, record an open discrepancy in the five-point form instead of
guessing (CLAUDE.md §3).

## When to stop auditing

Once an independent re-derivation confirms a result by a genuinely different route — not the
same script rerun, not the same route retyped — and either the literature agrees or there is a
stated reason it cannot be checked against literature, **stop**. A fifth confirmation of
something four independent routes agree on is not rigour (`docs/failure_modes.md`).
