# docs/prompts — session prompt records

A result without the prompt that produced it cannot be re-derived, and cannot be checked for
how much the model chose versus was told (CLAUDE.md §10). Rules:
`.claude/rules/research-sessions.md`.

Three kinds of file, in **two separate places**, so that no filtering rule has to be trusted.

## Curated records — the citable ones

`docs/prompts/<ID>_<topic>.md`, one per substantial session, **written by hand** before work
starts, with `## Outcome` filled in at the close and `## Revisions for reuse` noting what to
change when adapting it.

`<ID>` is a short stable handle reused in commit messages and in `docs/STATUS.md`, so a
result, its prompt and its commit are findable from each other:

| Prefix | For |
|---|---|
| `A<n>` | source audit |
| `D<n>` | derivation stage |
| `I<n>` | implementation |
| `V<n>` | validation run |
| `R<n>` | report |
| `M<n>` | maintenance / configuration (not science) |

| ID | Topic | Outcome |
|---|---|---|
| | | |

## Machine captures — the safety net

Written by `.claude/hooks/log_prompt.py`, never by hand:

- `log/<session>.md` — every prompt of a session, appended, **including false starts and
  harness traffic**. The raw record.
- `auto/<timestamp>_<session>_<hash>.md` — any prompt of 600 characters or more, in its own
  file with an Outcome placeholder.

These are a net, not the record. **Do not cite `auto/` as though it were curated.** To make
one citable, promote it by hand to a curated record above.

The separation exists because a single directory once held both, and at least 54 of 110
"captured prompts" turned out to be subagent hand-backs and task notifications, sitting
beside the real ones (`docs/failure_modes.md` entry 12).

## Writing a good prompt record

State what is in scope, **what is out of scope**, which files to read first, and which
subagent or skill the prompt expects. Out-of-scope is the field people leave out and the one
that prevents an agent from producing an artefact nobody asked for.
