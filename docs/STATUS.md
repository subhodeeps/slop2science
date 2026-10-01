# Research status

**This file contains the current state only.** It loads into every session. It has a line
budget, and `make check-docs` enforces the budget.
Put the history of the sessions, and the evidence for each line below, in
`docs/status_history.md`. That file does not load automatically.

If a session changes a fact that this file states, update **that line**. Do not update only
the history. A STATUS that describes last month is worse than no STATUS, because people
believe it.

## Current phase

Phase 0: not initialized. Run `/init-paper`. Then do the source audit.

## Immediate next task

1. **`/init-paper`**: fill in the placeholders, the ownership registry and the conventions of
   the project.
2. **Source audit [PI + literature]**: use `docs/prompts/A1_source_audit.md` after someone
   writes it. Do not write code before the audit.

## Toolchain

Not recorded yet. After `/init-paper`, state these items here:

- the tools that this project uses
- the version of each tool
- the tools that each machine has

`docs/toolchain.md` records the owner of each topic.

## Established decisions

None yet. See `docs/decision_log.md`.

## Derived

Nothing yet. Write one line for each completed derivation stage. Each line names the script,
the number of checks and the write-up. Do not write a line here if no re-runnable script
supports it.

## Validated

Nothing yet. Write one line for each accepted result. Each line names the record, the
resolution, the precision and the benchmark that judged the result. Name the *method* of that
benchmark.

## Reproduction

Nothing yet. Write one line that states what of the source the project reproduced. The source
judges this part.

## Extension / new work

Nothing yet. Write one line that states what the project established **beyond** the source.
Write one line for the current target of the new work. Physics and independent benchmarks
judge this part. The source never judges it (CLAUDE.md §2).

This section is as important as the section above it. The extension is half of the project.
If STATUS tracks only the reproduction, the project quietly becomes a reproduction project.

`docs/reproduction_and_extension.md` has both parts, claim by claim, with the evidence.

## Open questions

Nothing yet. Each entry states what is unknown, what resolves it and who it waits for:
**[PI]** a decision, **[tool]** a computation, **[lit]** a source.

## Current blockers

None.

## Last validation

None yet. Record these items: the date, the machine, the commit, the exact commands that ran
and their results.
