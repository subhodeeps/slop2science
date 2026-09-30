---
name: report-writing
description: How to write a topic's report (reports/<topic>_report.md) as a paper a physicist can follow and redo by hand, from already-verified stages, audits and records. Use when writing or regenerating a report, never mid-derivation.
when_to_use: 'Trigger phrases: write the report; assemble the report; methods section; write it up as a paper; regenerate the report'
paths:
  - "reports/**"
---

# Report writing

Two documents can come out of a topic, and they are not the same document:

- a **methods report** — the full verified derivation and validation chain, for the PI and
  for whoever continues the work;
- a **manuscript** — the project's own new work, written for publication, in which the
  reproduction is background and the extension is the contribution (CLAUDE.md §2).

The rules below apply to both. What differs is the weighting: a methods report shows every
verified step; a manuscript states the reproduction compactly ("the source's Eqs. (1)–(9) were
reconstructed independently; see the methods appendix") and spends its length on what is new.
**The PI decides which document is being written, what it claims, its scope and its
authorship** — ask if the brief does not say, and never decide a claim.

**The reader is a researcher in the field, not an auditor.** They must be able to (a) follow
and redo the algebra by hand and (b) reproduce the results. They do not know this project's
internal vocabulary and should not have to learn it.

A report written for an auditor instead of that reader fails even when it satisfies every
mechanical requirement it was given. The project this template came from produced exactly
that — a provenance block after every equation, an internal classification line on every
section, session codes in running text — and it had to be thrown away and rewritten. It did
what its brief said. The brief was wrong (`docs/failure_modes.md`).

**So start every brief with who the reader is and what they must be able to do**, and put
mechanical requirements where they serve that reader: in an appendix.

## Structure

1. **Introduction** — the problem, what this document establishes, what is reproduction of the
   source and what is new here. Say which is which plainly, in prose.
2. **Setup** — conventions, notation, definitions. Every symbol defined at first use, one
   notation throughout the document, even where sources differ. State the conversions.
3. **The derivation**, stage by stage. For each: the goal, the operation, the result, and the
   connecting algebra. Where the source says "standard techniques" or states a result without
   derivation, **supply the derivation** — that is the main thing this document adds.
4. **Method** — the production method, in enough detail to reimplement: formulation, boundary
   treatment, discretization, solution structure, acceptance criteria.
5. **Results** — with resolution, precision, convergence measure, and benchmark comparisons
   naming each benchmark's *method*.
6. **Discrepancies with the source** — a short paragraph each in the text, saying what the
   source states, what its equations imply, what this project derives, and what was adopted.
   The full five-point form goes in the appendix.
7. **Appendix: verification record** — the provenance. Script, check label and result for
   every equation presented as a result; record for every number. This is where the ledger
   belongs, and it is genuinely valuable *here*.
8. **Appendix: discrepancies in full**, five-point form each (CLAUDE.md §3).

## Hard constraints

- **Only verified results as results.** An equation is either established by a cited script
  check or derived by hand between two checked expressions — and if the latter, say so, once,
  briefly. Never invent, "clean up" or silently alter an equation or convention.
- **Only recorded numbers.** Every digit traces to a record. No unsupported precision.
- **Nothing softened.** Open issues stay open. Discrepancies are stated, not smoothed. Never
  attribute the project's extensions to the source, or the source's results to this project —
  in a manuscript this is not a bookkeeping slip but a misattribution.
- **Novelty is the PI's to claim.** State plainly what is new and what is reproduction; do
  not write significance, priority or novelty claims of your own. Where the extension rests
  on something weaker than an independent benchmark, say what it rests on
  (`docs/validation_protocol.md` §8).
- **Never "after some algebra"** in place of the algebra. If it is long, put it in an appendix
  and point there.
- **One author, in order.** Do not split the narrative across parallel writers: ten parallel
  authors produce ten voices, drifting notation and repeated framing, and the result has to be
  rewritten by one person anyway. Split *reading* and *checking*, never the prose.
- **Write in chunks** of roughly 250 lines per tool call. A whole-document write hits the
  output-token limit and produces nothing while appearing to work — the file's line count
  stops changing and the agent looks alive.

## Precedence between sources

When the settled record and a working note disagree, the settled record wins:
`docs/decision_log.md` and the source audit's discrepancy rows outrank the per-leg notes they
were synthesized from. Where the two disagree, **record the inconsistency** as an open
question rather than quietly picking one — a report writer once copied a claim from a working
note that the settled record contradicted, and it shipped.
