# Research status

**Current state only.** This file loads into every session, so it has a line budget that
`make check-docs` enforces.
The session-by-session record and the evidence behind each line below go in
`docs/status_history.md`, which is *not* auto-loaded.

When a session changes a fact this file states, it updates **that line** — not only the
history. A STATUS that describes last month is worse than no STATUS, because it is believed.

## Current phase

Phase 0 — not initialized. Run `/init-paper`, then the source audit.

## Immediate next task

1. **`/init-paper`** — fill the project's placeholders, ownership registry and conventions.
2. **Source audit [PI + literature]** — `docs/prompts/A1_source_audit.md` once written.
   No code before the audit.

## Toolchain

Not yet recorded. After `/init-paper`, state here: which tools this project uses, their
versions, and which of them are available on which machine. Ownership per topic is in
`docs/toolchain.md`.

## Established decisions

None yet. `docs/decision_log.md`.

## Derived

Nothing yet. One line per completed derivation stage, each naming its script, its check count
and its write-up. A line here without a re-runnable script does not belong here.

## Validated

Nothing yet. One line per accepted result, each naming its record, resolution, precision and
the benchmark it was judged against — with that benchmark's *method*.

## Reproduction

Nothing yet. What of the source is reproduced, in one line. Judged against the source.

## Extension / new work

Nothing yet. What has been established **beyond** the source, in one line, and what the
current new-work target is. Judged against physics and independent benchmarks, never against
the source (CLAUDE.md §2).

This section is not an afterthought to the one above it: the extension is half the project,
and a STATUS that only tracks reproduction will quietly turn the project into a reproduction
project.

Both, claim by claim, with evidence: `docs/reproduction_and_extension.md`.

## Open questions

Nothing yet. Each entry says what is unknown, what would resolve it, and who it waits on:
**[PI]** a decision, **[tool]** a computation, **[lit]** a source.

## Current blockers

None.

## Last validation

None yet. Record: date, machine, commit, the exact commands run, and their outcome.
