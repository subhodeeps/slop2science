# Checklist for each stage

Work through this checklist before you call a derivation stage done. It is mechanical on
purpose. The failures that it finds look fine at the time.

## Before you write the script

- [ ] Does this stage do exactly one thing? If the name needs "and", split the stage.
- [ ] Does `docs/toolchain.md` declare the owning tool for this topic?
- [ ] Which output of a previous stage does the stage load? Does that output exist? Did someone
      commit it?
- [ ] Is the stage REPRODUCTION, EXTENSION or CROSS-CHECK? What exactly judges it?
- [ ] Is there a prompt record for this session (`docs/prompts/<ID>_<topic>.md`)?

## While you write it

- [ ] The header is complete: Topic, Stage, Owner tool, Kind, Judged against, Inputs, Outputs.
- [ ] The script loads shared helpers from `symbolic/common/`. It does not use a copy.
- [ ] Each non-trivial step **prints** its result and then checks it.
- [ ] Each check has a short, stable, quoted label that a write-up can cite.
- [ ] The script states assumptions where it uses them, not only at the top.
- [ ] A simplification that can divide by something records the assumption that the divisor is
      not zero. The stage checks the assumption where the check is cheap.
- [ ] The script exits with a non-zero code if any check fails.
- [ ] The script saves results as text under `out/`. It does not use a binary format.

## Checks that the stage must contain

- [ ] A back-substitution residual that is identically zero.
- [ ] A limiting or special case with an independently known answer.
- [ ] A check of dimensions or scaling.
- [ ] An invariant that the derivation did not use.
- [ ] For a reproduction: a comparison with the displayed equation of the source, coefficient by
      coefficient. A visual comparison is not enough. "The same up to notation" is not enough.
- [ ] For an extension: the reduction to the already-verified case, run as a check.

## After you run it

- [ ] Each check passed. Someone read the printed output. The exit code alone is not enough.
- [ ] The project recorded the check count. Then a later rerun can compare against it.
- [ ] A write-up exists. It cites the script and the label at each displayed equation.
- [ ] The five-item form records each discrepancy with the source.
- [ ] `stages.txt` is current. `make stages TOPIC=<topic>` runs the whole topic cleanly from a
      fresh checkout.
- [ ] `make check` is clean (references and evidence labels resolve).
- [ ] You committed the script and the write-up together.
- [ ] `docs/STATUS.md` and `docs/reproduction_and_extension.md` have the update, with evidence.

## Warning signs

- A check passes the first time you write it, on a step that you expected to be hard.
- You had to widen a tolerance to get a pass.
- A stage needed an edit of its own earlier output to work.
- "It matches the paper", with no comparison at the level of the coefficients.
- A write-up has an equation, and you cannot point to a labelled check for it.
