---
name: source-audit
description: Audit the primary source paper into the project. Reconstruct what it states, what its equations imply, and where it is inconsistent. Do this before you write any code. The audit produces docs/<topic>_source_audit.md and fills the conventions register and the reproduction matrix.
when_to_use: 'Trigger phrases: source audit, audit the paper, read the paper, what does the source say, reconstruct the paper, before writing code'
---

# Source audit

This is the first real session of a project. Everything else depends on it. Its output is not a
summary of the paper. It is a **structured reconstruction** of what the paper states, what its
displayed equations imply, and where the two differ.

Do not write code during an audit. Derivation is a later stage. An audit is reading with a
template (`docs/source_audit_template.md`).

## Procedure

1. **State the scope.** State which sections, equations, tables and figures are in scope. If you
   audit a whole paper at once, the audit is shallow. If you audit one chapter of a calculation
   at a time, the audit is usable.
2. **Read the paper in its best form** for each equation, table and number. Use the `.tex` file
   from `make fetch-source` if the paper is on arXiv. Otherwise use the rendered pages. Never use
   the extracted text. The printed equation numbers come from the page. A `.tex` file has labels,
   not numbers. This step is not optional.
   `.claude/skills/literature-audit/reference/corpus.md` gives the order. It also states what to
   do when the `.tex` and the page disagree.
3. **Fill `docs/source_audit_template.md`** into `docs/<topic>_source_audit.md`. For each
   displayed equation in scope, record its number, the section, its variables, its role and what
   it depends on. Transcribe. Do not paraphrase.
4. **Separate three things at each point, and never merge them:**
   - what the source **states** (its prose)
   - what its **displayed equations imply** (algebra on the equations themselves)
   - what the source **assumes and does not state**

   The prose and the equations disagree more often than you expect. The value of the audit is
   almost entirely in the separation of the two.
5. **Record each discrepancy in the five-item form** (CLAUDE.md §3), in the open-issues section
   of the audit. Do not resolve a discrepancy by choosing the reading that seems more likely.
   That is a PI decision. Log it in `docs/decision_log.md`.
6. **Fill `docs/conventions.md`.** Add one row for each convention that the source fixes, with
   the tag SOURCE. Add one row for each convention that the source leaves ambiguous, with the
   tag OPEN.
7. **Fill `docs/reproduction_and_extension.md`.** Add one row for each equation, table and figure
   that the project intends to reproduce, with the status `not attempted`.
8. **List what the source does not give you.** This includes steps that it calls standard,
   constants that it states without derivation, and numerical details that it omits. This list
   is the derivation plan.
9. **List what the source does not do.** This includes the regimes that it excludes, the cases
   that it leaves open, the generalizations that it suggests, and the questions that its own
   results raise. The PI decides which of these the project pursues. The **extension** starts
   from this list. An audit that omits it did half of its job (CLAUDE.md §2).

## Output

- `docs/<topic>_source_audit.md` — the audit.
- Rows in `docs/conventions.md`, and in **both** tables of `docs/reproduction_and_extension.md`.
  These are the reproduction targets and the candidate extensions, for the PI to rule in or out.
- Discrepancies in the five-item form. Each one is either logged as a decision, or left open
  explicitly with the validation that would decide it.
- A short section "what to derive first": the order of dependency of the stages to come.

## What makes an audit fail

- A summary in place of a transcription. You cannot check a summary against the paper later.
- Resolving an ambiguity to keep the narrative tidy.
- Recording a number without its equation or table number and the version of the paper.
- Treating the stated equation of one paper as ground truth for something that would change a
  convention of the project, without a second independent source (`.claude/rules/sources.md`,
  `docs/failure_modes.md`).
