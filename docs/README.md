# docs — what lives where

One owner per fact. If two files would say the same thing, one of them links instead
(`docs/failure_modes.md` entry 11 is why).

## Loaded into every session

| File | Holds | Size discipline |
|---|---|---|
| `../CLAUDE.md` | the charter: authority, objective, source-first discipline, the five-point form, toolchain rules, session protocol | under ~200 lines |
| `STATUS.md` | **current state only** — phase, next task, derived, validated, open, blockers, last validation | under ~100 lines |
| `conventions.md` | the conventions register, one row each, with status and where fixed | short by design |

## Read when needed

| File | Holds |
|---|---|
| `GUIDE.md` | the mechanism: what each configuration piece is and when it fires |
| `WORKFLOW.md` | the practice: how to do a piece of work, what "verified" means |
| `failure_modes.md` | what has actually gone wrong, what it cost, what changed because of it |
| `toolchain.md` | tool ownership registry, per-tool execution notes, hand-off conventions |
| `validation_protocol.md` | the acceptance gates and the result-record schema |
| `reproduction_matrix.md` | what of the source has been reproduced, claim by claim |
| `source_audit_template.md` | the skeleton for auditing a source paper |
| `implementation_checklist.md` | item-by-item progress, ticked only with evidence |
| `decision_log.md` | PI decisions, `D-NNN`, append-only |
| `status_history.md` | the session-by-session record (not auto-loaded) |
| `literature/` | per-topic literature notes and convention reconciliations |
| `prompts/` | session prompt records — curated, plus machine captures |

## Where a new document goes

Before adding one, check whether it belongs in an existing file. A new document that restates
an existing one is the failure mode this structure is built against.

- A procedure for a category of work → a **skill**, not a doc.
- A constraint on a set of paths → a **rule**, not a doc.
- Something that must hold regardless of what the model decides → a **hook**.
- A per-topic scientific record → `derivation/<topic>/` or `validation/<topic>/`.
- Working notes and dead ends → `notes/`. Real, worth keeping, and not the record.
