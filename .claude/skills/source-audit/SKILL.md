---
name: source-audit
description: Audit the primary source paper into the project - reconstruct what it states, what its equations imply, and where it is inconsistent - before any code is written. Produces docs/<topic>_source_audit.md and populates the conventions register and reproduction matrix.
when_to_use: 'Trigger phrases: source audit; audit the paper; read the paper; what does the source actually say; reconstruct the paper; before writing code'
---

# Source audit

The first real session of a project, and the one everything else depends on. Its output is
not a summary of the paper: it is a **structured reconstruction** of what the paper states,
what its displayed equations actually imply, and where the two differ.

No code is written during an audit. Deriving is a later stage; auditing is reading with a
template (`docs/source_audit_template.md`).

## Procedure

1. **State the scope**: which sections, equations, tables and figures are in scope. A whole
   paper at once produces a shallow audit; one chapter of a calculation at a time produces a
   usable one.
2. **Read the paper as rendered pages**, not as extracted text, for every equation, table and
   number (`.claude/rules/sources.md`). This is not optional and it is the single highest-
   yield rule in this skill.
3. **Fill `docs/source_audit_template.md`** into `docs/<topic>_source_audit.md`. Record, for
   every displayed equation in scope: its number, the section, its variables, its role, and
   what it depends on. Transcribe, do not paraphrase.
4. **Separate three things at every point**, and never merge them:
   - what the source **states** (its prose);
   - what its **displayed equations imply** (algebra on the equations themselves);
   - what is **assumed but unstated**.
   The prose and the equations disagree more often than one expects, and the audit's value is
   almost entirely in having kept them apart.
5. **Record every discrepancy in the five-point form** (CLAUDE.md §3), in the audit's open-
   issues section. Do not resolve one by picking the reading that seems more likely; that is a
   PI decision, and it gets logged in `docs/decision_log.md`.
6. **Populate `docs/conventions.md`**: one row per convention the source fixes, tagged
   SOURCE; one row per convention the source leaves ambiguous, tagged OPEN.
7. **Populate `docs/reproduction_and_extension.md`**: one row per equation, table and figure the
   project intends to reproduce, status `not attempted`.
8. **List what the source does not give you**: steps it calls standard, constants it states
   without derivation, numerical details it omits. This list is the derivation plan.
9. **List what the source does not do** — the regimes it excludes, the cases it leaves open,
   the generalizations it gestures at, the questions its own results raise. The PI decides
   which of these the project will pursue; this list is where the **extension** starts, and
   an audit that omits it has done half its job (CLAUDE.md §2).

## Output shape

- `docs/<topic>_source_audit.md` — the audit.
- Rows added to `docs/conventions.md`, and to **both** tables of
  `docs/reproduction_and_extension.md` — reproduction targets, and candidate extensions for
  the PI to rule in or out.
- Discrepancies in five-point form, each one either logged as a decision or left explicitly
  open with the validation that would decide it.
- A short "what to derive first" section: the dependency order of the stages to come.

## What makes an audit fail

- Summarising instead of transcribing. A summary cannot be checked against the paper later.
- Resolving an ambiguity to keep the narrative tidy.
- Recording a number without its equation/table number and the paper's version.
- Treating a single paper's stated equation as ground truth for something that would change a
  project convention, without a second independent source
  (`.claude/rules/sources.md`, `docs/failure_modes.md`).
