# Workflow — how to do a piece of work here

`docs/GUIDE.md` explains the mechanism; this is the practice. Written for whoever is handed
this repository next, including the failure modes it is built to avoid
(`docs/failure_modes.md` has the full account).

## 1. Writing a session prompt

One phase-step per session (CLAUDE.md §8). A substantial research prompt is recorded verbatim
in `docs/prompts/<ID>_<topic>.md` **before** work starts
(`.claude/rules/research-sessions.md`), never paraphrased.

State explicitly: what is in scope, **what is out of scope**, which files to read first, and
which subagent or skill the prompt expects. A prompt that is vague about scope is how an
agent ends up producing an artefact nobody asked for and nobody can account for later.

## 2. The derive → check → write up → commit cycle

1. **Derive** — one stage per script, `symbolic/<topic>/stage_NN_<what>.<ext>`, in the tool
   that owns the topic. Never combine stages; never overwrite an old one (a hook blocks it).
2. **Check, inside the same script** — every non-trivial step gets an explicit labelled
   assertion, and **the value is printed before it is asserted.** A check that asserts without
   ever printing what it found is how a false PASS survives a whole session.
3. **Write up** in `derivation/<topic>/NN_<what>.md`, citing the verifying script and exact
   check label for every displayed equation. A displayed equation with no citable check does
   not go in the write-up.
4. **Commit** script and write-up together, not deferred to a cleanup pass.
5. **Export**, if the stage produces coefficients another tool needs — then
   `make codegen-check`. Never hand-transcribe.

Implementation follows the same shape in code (`src/`, tested by `make test`), consuming only
`symbolic/generated/` — never inventing a coefficient because the export is missing.

## 3. What "verified" means, and what it does not

**Verified**: checked by an explicit, printed, re-runnable assertion in a committed script;
or a numerical result that passed every applicable criterion in `docs/validation_protocol.md`
at a stated resolution and precision. Cite the script and the check label, always.

**Not verified** — say so plainly, do not soften and do not omit: a result that is merely
plausible; a single-resolution spot check; a solver output with no convergence or benchmark
check yet (that is a *candidate*, CLAUDE.md §6); a comparison that agrees within some
tolerance but has not been through the acceptance protocol. For that last case the phrase is
"consistent with", not "verified".

**Never call something verified because it looks right.** "Looks right" is what a wrong
asymptotic expression looks like for three sessions before an independent re-derivation
catches the dropped term.

## 3a. The ladder of rigour

"Verified" is not one thing. A claim sits somewhere on a ladder, and **saying where is part of
reporting it** (adapted from *How to Train Your Slop Cannon*):

| Rung | What it means | Good for |
|---|---|---|
| 1. prose | an argument in paragraphs | orientation; never a result |
| 2. **structured proof** | numbered hierarchy, each step justified or an explicit gap (`.claude/skills/derivation-workflow/reference/structured_proofs.md`) | anything a reviewer would question |
| 3. **adversarially verified** | rung 2, attacked by an independent agent that never saw the prover's reasoning (`.claude/skills/verification/reference/adversarial_protocol.md`) | a claim that changes a convention or closes a discrepancy |
| 4. **script-checked** | a printed, labelled, re-runnable assertion in a committed script | algebra, identities, limits, reproductions |
| 5. **numerically accepted** | every applicable criterion in `docs/validation_protocol.md`, at stated resolution and precision, with a record | a reported number |
| 6. machine-checked | a proof assistant decides | a load-bearing step worth the cost |

**No single rung is trustworthy alone, and they fail in different places** — which is the
point of having several. A script-checked identity can be the wrong identity; an
adversarially verified argument can rest on a mis-transcribed premise; a converged number can
solve the wrong problem. Layering them is what makes the result solid, so compose rungs rather
than picking the highest one reached.

Report the rung honestly. "Script-checked" and "adversarially verified" are different claims,
and neither is "machine-checked".

**What the automated checks can and cannot do.** `make check` verifies that a reference
*resolves* — to a file, a check label, a column, a commit. It cannot verify that the
statement built on it is *true*. A citation that resolves cleanly to a real script whose
check does not establish what the entry claims passes every automated check in full. That
gap is closed only by a human, or the `verification` agent, reading the script.

## 4. Recording a discrepancy

The five-point form, stated once in CLAUDE.md §3. Use it verbatim; do not invent a shorter or
longer version for a particular write-up. Every file that needs it points there.

## 5. Reproduction vs. extension — same directories, marked at the point of use

Two halves of equal standing, with different standards of evidence (CLAUDE.md §2):

- **REPRODUCTION** — reconstructing the source itself: its equations, its own conventions,
  its tables. Judged against: agreement with the source. This is the foundation.
- **EXTENSION** — the new work built on it: new systems, new regimes, a more general or
  better method, questions the source left open. Judged against: independent benchmarks and
  physics. **The source cannot validate an extension** — it does not contain the result.
  This is what the project is for, and it ends in a paper of its own.

The asymmetry is worth stating plainly, because it is the easiest thing in the project to get
backwards: a reproduction that agrees with the source is *evidence the machinery works*; an
extension that "looks consistent with the source" is **not evidence of anything**.

They are **not** split into separate directory trees. They share derivation stages, share
asymptotic analysis, and often share a single validation driver that tests both cases side by
side; splitting the tree would cut across working scripts for no benefit, and fragmenting a
small topic costs more than a marker does.

Instead, **every script, write-up and record states which kind it is and what it is judged
against**, near its top:

    Kind:           REPRODUCTION | EXTENSION | CROSS-CHECK
    Judged against: <the source's Eq./Table N>  |  <benchmark/physics, named>

This exists because of a specific, easy mistake: a write-up let an independent-method
benchmark comparison — extension-grade evidence — read as though it validated the source's own
reproduction. One `Judged against:` line at the point where the number is reported makes that
impossible to misread.

Reports say the same thing in plain prose where it matters ("this reproduces the source's
Eq. (16)"), not as marker lines: reports are written for a human reader.

## 6. Reading a validation record

`validation/<topic>/records/*.json`, schema in `docs/validation_protocol.md` §12: resolution,
precision, residuals, the benchmark compared against **with its method and provenance**,
pass/fail per criterion, `kind`, `judged_against`, tool versions, commit.

A record with no benchmark provenance is incomplete — ask where the comparison number came
from before trusting it. Benchmark provenance headers name the *actual* method behind a
published number: read the source's own caption yourself, rather than inferring it from a
previous header or the source's reputation.

## 7. When a check fails

Stop. Report the failing check, its exact output, and its class
(`.claude/skills/verification/SKILL.md`). Do not adjust the check to pass, silently change an
expected value, or widen a tolerance without recording why. If the fix is not obviously
correct, record it as an open discrepancy rather than guessing.

## 8. Process problems

These are watched for, not ruled against — a rule that gets read past does not help. The full
account, with what each one cost, is `docs/failure_modes.md`. In brief:

- **Audits spawning audits.** Stop when an independent route confirms the result and the
  literature agrees or demonstrably cannot be consulted.
- **Claims asserted before being checked.** Print, then assert. Always, not only when
  suspicious.
- **The same equation misread from a PDF twice.** Read the rendered page, not the text layer.
  Require a second source before a single paper's equation changes a project convention.
- **Scope creep under interruption.** Scope shrinks under pressure; it never expands. The
  session-close orphan check is the backstop.
- **Long agent outputs stalling silently.** Write in chunks; check the file's line count and
  the transcript before declaring an agent stuck, because restarting a working agent throws
  its work away.
- **Parallel authors do not make one document.** Split reading and checking, never a
  narrative.
- **A brief followed faithfully can still produce the wrong thing.** Start a brief with who
  the reader is and what they must be able to do.
- **Working notes versus the settled record.** The decision log and the audit rows outrank
  the notes they were synthesized from. Where they disagree, record the inconsistency; do not
  quietly pick one.
- **STATUS drifts.** When a session changes a fact STATUS states, it updates that line.
