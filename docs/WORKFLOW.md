# Workflow — how to do a piece of work here

`docs/GUIDE.md` explains the mechanism. This file explains the practice. It is for the next
person who receives this repository. It also covers the failure modes that the repository
prevents (`docs/failure_modes.md` has the full account).

## 1. Write a session prompt

Use one phase-step for each session (CLAUDE.md §8). Record a substantial research prompt word
for word in `docs/prompts/<ID>_<topic>.md` **before** the work starts
(`.claude/rules/research-sessions.md`). Never paraphrase it.

State what is in scope. State **what is out of scope**. State which files to read first. State
which subagent or skill the prompt expects. A prompt that is vague about scope causes an agent
to produce an artefact that nobody asked for and nobody can explain later.

## 2. The cycle: derive, check, write up, commit

1. **Derive.** Use one script for each stage: `symbolic/<topic>/stage_NN_<what>.<ext>`. Use the
   tool that owns the topic. Never combine stages. Never overwrite an old stage (a hook blocks
   this).
2. **Check, inside the same script.** Give each non-trivial step an explicit, labelled
   assertion. **Print the value before you assert it.** A check that asserts without a printed
   value lets a false PASS survive a whole session.
3. **Write up** in `derivation/<topic>/NN_<what>.md`. For each displayed equation, cite the
   verifying script and the exact check label. If a displayed equation has no citable check, do
   not put it in the write-up.
4. **Commit** the script and the write-up together. Do not defer this to a cleanup pass.
5. **Export**, if the stage produces coefficients that another tool needs. Then run
   `make codegen-check`. Never transcribe by hand.

Implementation has the same shape in code (`src/`, tested by `make test`). It uses only
`symbolic/generated/`. If the export is missing, never invent a coefficient.

## 3. What "verified" means, and what it does not mean

**Verified** means one of two things. An explicit, printed, re-runnable assertion in a committed
script checked it. Or it is a numerical result that passed each applicable criterion in
`docs/validation_protocol.md`, at a stated resolution and precision. Always cite the script and
the check label.

**Not verified.** State this plainly. Do not soften it. Do not omit it. These items are not
verified:

- a result that is only plausible
- a spot check at a single resolution
- a solver output with no convergence or benchmark check (this is a *candidate*, CLAUDE.md §6)
- a comparison that agrees within a tolerance but did not pass the acceptance protocol. For
  this case, write "consistent with", not "verified".

**Never call something verified because it looks right.** A wrong asymptotic expression looks
right for three sessions. Then an independent derivation finds the dropped term.

## 3a. The ladder of rigour

"Verified" is not one thing. A claim has a place on a ladder. **To state the place is part of
the report** (adapted from *How to Train Your Slop Cannon*):

| Rung | What it means | Good for |
|---|---|---|
| 1. prose | an argument in paragraphs | orientation. Never a result. |
| 2. **structured proof** | a numbered hierarchy. Each step has a justification or an explicit gap (`.claude/skills/derivation-workflow/reference/structured_proofs.md`) | anything that a reviewer can question |
| 3. **adversarially verified** | rung 2, attacked by an independent agent that never saw the reasoning of the prover (`.claude/skills/verification/reference/adversarial_protocol.md`) | a claim that changes a convention or closes a discrepancy |
| 4. **script-checked** | a printed, labelled, re-runnable assertion in a committed script | algebra, identities, limits, reproductions |
| 5. **numerically accepted** | each applicable criterion in `docs/validation_protocol.md`, at a stated resolution and precision, with a record | a reported number |
| 6. machine-checked | a proof assistant decides | a load-bearing step that is worth the cost |

**No single rung is trustworthy alone. The rungs fail in different places.** This is the reason
to have several rungs. A script-checked identity can be the wrong identity. An adversarially
verified argument can rest on a premise that someone mis-transcribed. A converged number can
solve the wrong problem. Layers make the result solid. Therefore combine rungs. Do not pick the
highest rung that you reached.

Report the rung honestly. "Script-checked" and "adversarially verified" are different claims.
Neither is "machine-checked".

**What the automated checks can do and cannot do.** `make check` verifies that a reference
*resolves* to a file, a check label, a column or a commit. It cannot verify that the statement
is *true*. A citation can resolve cleanly to a real script. The check in
that script can fail to establish what the entry claims. Such a citation passes every
automated check. Only a person, or the `verification` agent that reads the script, closes this
gap.

## 4. Record a discrepancy

CLAUDE.md §3 states the five-item form one time. Use it exactly. Do not invent a shorter or
longer version for one write-up. Every file that needs the form points there.

## 5. Reproduction and extension — the same directories, marked where used

The project has two parts of equal standing. They have different standards of evidence
(CLAUDE.md §2):

- **REPRODUCTION** reconstructs the source itself: its equations, its own conventions and its
  tables. The standard is agreement with the source. This is the foundation.
- **EXTENSION** is the new work built on the foundation: new systems, new regimes, a more
  general or better method, and questions that the source left open. The standard is
  independent benchmarks and physics. **The source cannot validate an extension.** The source
  does not contain the result. This is the purpose of the project. It ends in a set of new
  calculations that can go into a future publication.

It is easy to get the asymmetry backwards. A reproduction that agrees with the source is
*evidence that the machinery works*. An extension that "looks consistent with the source" is
**not evidence of anything**.

The project does **not** split the two parts into separate directory trees. They share
derivation stages and asymptotic analysis. Often they share one validation driver that tests
both cases side by side. A split cuts across working scripts and gives no benefit. To fragment
a small topic costs more than a marker costs.

Instead, **each script, write-up and record states its kind and its standard of judgement**,
near the top:

    Kind:           REPRODUCTION | EXTENSION | CROSS-CHECK
    Judged against: <the source's Eq./Table N>  |  <benchmark/physics, named>

This rule exists because of a specific, easy mistake. In one write-up, a comparison with an
independent-method benchmark looked as if it validated the reproduction of the source. That
comparison is evidence of extension grade. One `Judged against:` line where the write-up reports
the number makes this misreading impossible.

Reports state the same fact in plain prose where it matters ("this reproduces Eq. (16) of the
source"). They do not use marker lines, because a human reader reads a report.

## 6. Read a validation record

The schema of `validation/<topic>/records/*.json` is in `docs/validation_protocol.md` §12. A
record contains these items:

- resolution and precision
- residuals
- the benchmark that the record compares against, **with its method and provenance**
- pass or fail for each criterion
- `kind` and `judged_against`
- tool versions and commit

A record with no benchmark provenance is incomplete. Ask where the comparison number came from
before you trust it. A benchmark provenance header names the *real* method behind a published
number. Read the caption of the source yourself. Do not infer the method from an earlier header
or from the reputation of the source.

## 7. When a check fails

Stop. Report the failing check, its exact output and its class
(`.claude/skills/verification/SKILL.md`). Do not change the check to make it pass. Do not change
an expected value silently. Do not widen a tolerance without a recorded reason. If you are not
sure that the fix is correct, record it as an open discrepancy. Do not guess.

## 8. Process problems

The project watches for these problems. It does not write rules against them, because people
read past a rule. `docs/failure_modes.md` has the full account and the cost of each problem.
In brief:

- **Audits that start audits.** Stop when an independent route confirms the result, and the
  literature agrees, or you cannot consult the literature.
- **Claims that someone asserted before checking them.** Print, then assert. Do this always,
  not only when you suspect a problem.
- **The same equation misread from a PDF twice.** If a `.tex` file exists, read it. If it does
  not exist, read the rendered page. Never read the text layer
  (`.claude/skills/literature-audit/reference/corpus.md`). Require a second source before the
  equation of one paper changes a convention of the project.
- **Scope creep during an interruption.** Under pressure, the scope gets smaller. It never gets
  larger. The orphan check of the session close is the backstop.
- **Long agent outputs that stall silently.** Write in chunks. Check the line count of the file
  and the transcript before you declare that an agent is stuck. A restart of a working agent
  discards its work.
- **Parallel authors do not make one document.** Split the reading and the checking. Never
  split a narrative.
- **A brief that an agent follows faithfully can still produce the wrong thing.** Start a brief
  with the reader and with what the reader must be able to do.
- **Working notes against the settled record.** The decision log and the audit rows outrank the
  notes that they came from. If they disagree, record the inconsistency. Do not pick one
  silently.
- **STATUS drifts.** If a session changes a fact that STATUS states, the session updates that
  line.
