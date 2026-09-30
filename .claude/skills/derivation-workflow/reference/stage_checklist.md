# Per-stage checklist

Work through this before calling a derivation stage done. It is deliberately mechanical: the
failures it catches are the ones that look fine at the time.

## Before writing the script

- [ ] Does this stage do exactly one thing? If the name needs "and", split it.
- [ ] Is the owning tool for this topic declared in `docs/toolchain.md`?
- [ ] Which previous stage's output does it load? Does that output exist and is it committed?
- [ ] Is it REPRODUCTION, EXTENSION, or CROSS-CHECK, and judged against what exactly?
- [ ] Is there a prompt record for this session (`docs/prompts/<ID>_<topic>.md`)?

## While writing it

- [ ] Header complete: Topic / Stage / Owner tool / Kind / Judged against / Inputs / Outputs.
- [ ] Shared helpers loaded from `symbolic/common/`, not copy-pasted.
- [ ] Every non-trivial step **prints** its result, and then checks it.
- [ ] Every check has a short, stable, quoted label that a write-up can cite.
- [ ] Assumptions stated where they are used, not only at the top.
- [ ] Any simplification that could divide by something records the assumption that it is
      nonzero — and the stage checks it where the check is cheap.
- [ ] The script exits non-zero if any check fails.
- [ ] Results persisted as text under `out/`, not a binary format.

## Checks the stage should contain

- [ ] Back-substitution residual, identically zero.
- [ ] A limiting or special case with an independently known answer.
- [ ] Dimensional or scaling consistency.
- [ ] An invariant not used in the derivation.
- [ ] For a reproduction: coefficient-by-coefficient comparison against the source's
      displayed equation. Not a visual comparison, not "same up to notation".
- [ ] For an extension: the reduction to the already-verified case, run as a check.

## After running it

- [ ] Every check passed, and the printed output was actually read — not only the exit code.
- [ ] Check count recorded, so a later rerun can be compared against it.
- [ ] Write-up written, citing script and label at every displayed equation.
- [ ] Any discrepancy with the source recorded in the five-point form.
- [ ] `stages.txt` updated; `make stages TOPIC=<topic>` reruns the whole topic cleanly from a
      fresh checkout.
- [ ] `make check` clean (references and evidence labels resolve).
- [ ] Script and write-up committed together.
- [ ] `docs/STATUS.md` and `docs/reproduction_and_extension.md` updated with evidence.

## Smells

- A check that passes the first time you write it, on a step you expected to be hard.
- A tolerance that had to be widened to get a pass.
- A stage that needed its own earlier output edited to work.
- "It matches the paper" with no coefficient-level comparison.
- A write-up whose equation you cannot point to a labelled check for.
