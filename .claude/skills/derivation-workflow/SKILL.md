---
name: derivation-workflow
description: The reproducible derivation cycle: one stage for each script, print-before-assert checks with stable labels, a write-up that cites each equation, then export. Use it for any symbolic derivation stage, source reconstruction, asymptotic analysis or limit check.
when_to_use: 'Trigger phrases: derive, derivation stage, reconstruct the equations, linearize, reduce the system, indicial exponents, asymptotic analysis, series expansion, limiting case, export coefficients'
paths:
  - "symbolic/**"
  - "derivation/**"
---

# Derivation workflow

For execution details for each tool, see the `toolchain` skill. For the rules that a hook or a
checker enforces, see `.claude/rules/derivation.md`. The stage template is
`templates/stage_template.wls` (adapt the header for `.py` or `.jl`). The checklist for each
stage is `reference/stage_checklist.md`.

## The cycle

**1. Derive.** Use one stage and one script: `symbolic/<topic>/stage_NN_<what>.<ext>`. Use the
tool that owns the topic. Add the script to `symbolic/<topic>/stages.txt`.

**2. Check, inside the same script.** Give each non-trivial step an explicit check with a short,
quoted label. **Print the value before you assert it.** The order matters: print, then assert. If
you assert first and read the output only when something looks wrong, a wrong assertion survives
a whole session.

Make these checks at each stage:

- Substitute the result back into what it came from. The residual must be identically zero.
- Check a limiting or special case with an independently known answer.
- Check dimensions or scaling.
- Check an invariant that the result must satisfy and that you did not use in the derivation.
- Where the stage reproduces the source, compare coefficient by coefficient against the displayed
  equation of the source. A visual comparison is not enough.

**3. Write up** in `derivation/<topic>/NN_<what>.md`. State the conventions that you use, the
assumptions and the displayed equations. For each displayed equation, give an evidence tag that
names the script and the exact check label.

If an argument is **not** a mechanical computation, write it as a **structured proof**. Examples
are an argument of uniqueness, exhaustiveness, a limit, a gauge or regularity. A structured proof
is a numbered hierarchy. A cited result, earlier steps or child steps justify each step. A step
with neither children nor justification is an explicit, labelled gap
(`reference/structured_proofs.md`). Prose hides exactly the step that is wrong. "After some
algebra it follows that" is not falsifiable at the level of the step. If a script checks algebra
coefficient by coefficient, the script is the proof. Cite its label. Do not add a hierarchy.

Evidence tags look like this:

    [E: `symbolic/<topic>/stage_04_reduce.wls`, "reduced system matches source Eq. (9)"]

If a displayed equation has no citable check, do not put it in the write-up. You can do algebra by hand
between two checked expressions. State it one time, briefly, and mark it.

**4. Commit** the script and the write-up together. Do not defer this to a cleanup pass. A
write-up that you commit a week after its script is how a stale citation appears.

**5. Export, if the stage produces coefficients that another tool needs.** Write
`export_NN_<what>.<ext>` to `symbolic/generated/<lang>/`. Then run
`make codegen-check TOPIC=<topic>`. Never transcribe by hand.

## The header of each stage

    Topic / Stage / Owner tool / Kind (REPRODUCTION|EXTENSION|CROSS-CHECK) /
    Judged against / Inputs / Outputs

`Kind:` and `Judged against:` are not bookkeeping. Reproduction evidence and extension evidence
have different weight. A write-up can let a benchmark comparison read as if it validated the
reproduction of the source. This is a real and easy mistake (`docs/WORKFLOW.md` §5).

## When a check fails

Stop. Report the failing check, its exact output and its class
(`.claude/skills/verification/SKILL.md`). Do not change the check to make it pass. Do not change
an expected value. Do not widen a tolerance without a recorded reason in the script and in the
write-up. If you are not sure that the fix is correct, record an open discrepancy in the
five-item form. Do not guess (CLAUDE.md §3).

## When to stop auditing

Stop when an independent derivation confirms a result by a different route. The same
script run again does not count. The same route typed again does not count. Also, the literature
must agree, or you must have a stated reason why you cannot check the result against the
literature. A fifth confirmation of a result that four independent routes confirm is not rigour
(`docs/failure_modes.md`).
