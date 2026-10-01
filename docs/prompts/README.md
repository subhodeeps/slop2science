# docs/prompts — records of session prompts

You cannot derive a result again without the prompt that produced it. You also cannot check how
much the model chose and how much the prompt told it (CLAUDE.md §10). Rules:
`.claude/rules/research-sessions.md`.

There are three kinds of file, in **two separate places**. Then no filtering rule needs trust.

## Curated records — the citable records

`docs/prompts/<ID>_<topic>.md`. Write one **by hand** for each substantial session, before the
work starts. Fill in `## Outcome` at the close. Use `## Revisions for reuse` to note what to
change when you adapt the prompt.

`<ID>` is a short, stable handle. Use it in commit messages and in `docs/STATUS.md`. Then you
can find a result, its prompt and its commit from each other:

| Prefix | For |
|---|---|
| `A<n>` | source audit |
| `D<n>` | derivation stage |
| `I<n>` | implementation |
| `V<n>` | validation run |
| `R<n>` | report |
| `M<n>` | maintenance and configuration (not science) |

| ID | Topic | Outcome |
|---|---|---|
| | | |

## Machine captures — the safety net

`.claude/hooks/log_prompt.py` writes these files. Never write them by hand:

- `log/<session>.md` contains every prompt of a session, appended. It **includes false starts
  and harness traffic**. It is the raw record.
- `auto/<timestamp>_<session>_<hash>.md` contains any prompt of 600 characters or more, in its
  own file with an Outcome placeholder.

These files are a net. They are not the record. **Do not cite `auto/` as a curated record.** To
make a capture citable, promote it by hand to a curated record.

The two places are separate for this reason: one directory once held both kinds. At least 54 of
110 "captured prompts" were subagent hand-backs and task notifications. They sat beside the real
prompts (`docs/failure_modes.md` entry 12).

## Write a good prompt record

State what is in scope. State **what is out of scope**. State which files to read first. State
which subagent or skill the prompt expects. People often omit the out-of-scope field. It
prevents an agent from producing an artefact that nobody asked for.
