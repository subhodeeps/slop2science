---
name: report-writing
description: How to write the report of a topic (reports/<topic>_report.md) as a paper that a physicist can follow and redo by hand. The sources are stages, audits and records that you already verified. Use it when you write or regenerate a report. Never use it in the middle of a derivation.
when_to_use: 'Trigger phrases: write the report, assemble the report, methods section, write it up as a paper, regenerate the report'
paths:
  - "reports/**"
---

# Report writing

A topic can produce two documents. They are not the same document:

- a **methods report**: the full verified derivation and validation chain, for the PI and for
  the people who continue the work
- a **manuscript**: the new work of the project, written for possible publication. The
  reproduction is background and the extension is the contribution (CLAUDE.md §2).

The rules below apply to both. The weighting is different. A methods report shows each verified
step. A manuscript states the reproduction compactly ("we reconstructed Eqs. (1)–(9) of the
source independently. See the methods appendix") and spends its length on what is new. **The PI
decides which document you write, what it claims, its scope and its authorship.** Ask if the
brief does not say. Never decide a claim.

**The reader is a researcher in the field. The reader is not an auditor.** The reader must be
able to (a) follow and redo the algebra by hand and (b) reproduce the results. The reader does
not know the internal vocabulary of this project and must not have to learn it.

A report for an auditor fails, even if it satisfies each mechanical requirement of its brief.
The project that this template came from produced such a report. It had a provenance block after
each equation, an internal classification line on each section and session codes in the running
text. The project threw it away and rewrote it. The report did what its brief said. The brief was
wrong (`docs/failure_modes.md`).

**So start each brief with the reader and with what the reader must be able to do.** Put the
mechanical requirements where they serve that reader: in an appendix.

## Structure

1. **Introduction.** State the problem and what this document establishes. State what is
   reproduction of the source and what is new here. Say which is which, plainly, in prose.
2. **Setup.** State the conventions, the notation and the definitions. Define each symbol at its
   first use. Use one notation in the whole document, also where sources differ. State the
   conversions.
3. **The derivation**, stage by stage. For each stage, give the goal, the operation, the result
   and the connecting algebra. If the source says "standard techniques" or states a result
   without derivation, **supply the derivation.** This is the main addition of this document.
4. **Method.** Describe the production method in enough detail to implement it again: the
   formulation, the treatment of the boundary, the discretization, the solution structure and the
   acceptance criteria.
5. **Results.** Give the resolution, the precision, the convergence measure and the benchmark
   comparisons. Name the *method* of each benchmark.
6. **Discrepancies with the source.** Write a short paragraph for each one in the text. State
   what the source states, what its equations imply, what this project derives and what the
   project adopted. The appendix has the full five-item form.
7. **Appendix: verification record.** This is the provenance. Give the script, the check label
   and the result for each equation that the report presents as a result. Give a record for each
   number. The ledger belongs here, and here it is valuable.
8. **Appendix: discrepancies in full**, each in the five-item form (CLAUDE.md §3).

## Hard constraints

- **Use only verified results as results.** A cited script check establishes an equation, or you
  derive it by hand between two checked expressions. In the second case, say so one time,
  briefly. Never invent, "clean up" or alter silently an equation, convention or interpretation.
- **Use only recorded numbers.** Each digit traces to a record. Give its resolution, precision,
  convergence measure, benchmark, the *method* of that benchmark, and the type of comparison
  (independent-method, same-method or self-consistency). Do not write unsupported precision.
- **Keep the running text for the reader.** Do not put these items in it: session codes,
  decision numbers, process history, provenance blocks after each equation, or narration about
  the repository. Put provenance in the verification appendix.
- **Soften nothing.** Open issues stay open. State the discrepancies. Do not smooth them. Never
  attribute the extensions of the project to the source. Never attribute the results of the
  source to this project. In a manuscript this is a misattribution. It is not a bookkeeping slip.
- **The PI claims novelty.** State plainly what is new and what is reproduction. Do not write
  your own claims of significance, priority or novelty. If the extension rests on something
  weaker than an independent benchmark, say what it rests on (`docs/validation_protocol.md` §8).
- **Never write "after some algebra"** in place of the algebra. If the algebra is long, put it in
  an appendix and point there.
- **Use one author, in order.** Do not split the narrative across parallel writers. Ten parallel
  authors produce ten voices, drifting notation and repeated framing. One person must rewrite the
  result. Split the *reading* and the *checking*. Never split the prose.
- **Write in chunks** of about 250 lines for each tool call. A write of the whole document hits
  the output-token limit and produces nothing while it appears to work. The line count of the
  file stops changing, and the agent looks alive.

## Precedence between sources

If the settled record and a working note disagree, the settled record wins. `docs/decision_log.md`
and the discrepancy rows of the source audit outrank the notes that they came from. If they
disagree, **record the inconsistency** as an open question. Do not pick one silently. A report
writer once copied a claim from a working note that the settled record contradicted. The claim
shipped.
