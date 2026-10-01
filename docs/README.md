# docs — what lives where

Each fact has one owner. If two files would state the same fact, one of them links to the
other (`docs/failure_modes.md` entry 11 explains why).

## Loaded into every session

| File | Contents | Size rule |
|---|---|---|
| `../CLAUDE.md` | the charter: **authority of the PI**, the two parts of the objective, source-first discipline, the five-item form, the rules for toolchain and language ownership, the session protocol | `make check-docs` checks the budget |
| `STATUS.md` | **current state only**: phase, next task, derived, validated, reproduction, extension/new work, open questions, blockers, last validation | budget checked |
| `conventions.md` | the conventions register: one row for each convention, with status and the place where the project fixes it | budget checked |

## Read when needed

| File | Contents |
|---|---|
| `GUIDE.md` | the mechanism: what each piece of configuration is, and when it acts |
| `WORKFLOW.md` | the practice: how to do a piece of work, and what "verified" means |
| `failure_modes.md` | what went wrong, what it cost, and what changed |
| `toolchain.md` | the ownership registry, the notes on execution for each tool, the hand-off conventions |
| `validation_protocol.md` | the acceptance gates and the schema of the result record |
| `reproduction_and_extension.md` | both parts, claim by claim: what of the source the project reproduced, what new work it established, and what the paper needs |
| `source_audit_template.md` | the skeleton for the audit of a source paper |
| `implementation_checklist.md` | progress for each item. Tick an item only with evidence. |
| `decision_log.md` | PI decisions, `D-NNN`, append-only |
| `status_history.md` | the record of each session (does not load automatically) |
| `literature/` | literature notes for each topic, and reconciliations of conventions |
| `prompts/` | records of session prompts: curated records and machine captures |
| `handoff_guide.md` | how to write `handoff.md`: the four headings, worked examples, what to never put in it |

The handoff (`../handoff.md`) is at the repository root, not here. A hook reads it into the
opening context of each session. It is prose for the next session. It is not a record. If it
disagrees with the files above, **those files win**. If something in the handoff is worth
relying on, move it into a record and delete it from the handoff.

## Where a new document goes

First check if the content belongs in an existing file. A new document that restates an
existing document causes the failure that this structure prevents.

- A procedure for a category of work goes in a **skill**. It does not go in a document.
- A constraint on a set of paths goes in a **rule**. It does not go in a document.
- A requirement that must hold whatever the model decides goes in a **hook**.
- A scientific record for one topic goes in `derivation/<topic>/` or `validation/<topic>/`.
- Working notes and dead ends go in `notes/`. They are real and worth keeping. They are not the
  record.
