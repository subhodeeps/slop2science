# Reproduction matrix

**What of the source has actually been reproduced, claim by claim.** This is the table that
answers "how far along is this?" — and the reason to keep it is that without it, that question
is answered from memory and from whichever document was opened most recently.

One row per equation, table and figure the project intends to reproduce. Rows are added by
the source audit (`/source-audit`) and updated at every `/session-close`.

## Status values

| Status | Meaning |
|---|---|
| `not attempted` | in scope, not yet started |
| `in progress` | being worked on now; name the stage or run |
| `reproduced` | reproduced, with re-runnable evidence cited |
| `discrepant` | the project's result disagrees with the source; five-point record exists |
| `not reproducible` | cannot be reproduced from what the source provides; say what is missing |
| `out of scope` | deliberately excluded; say why |

`discrepant` is a **result**, not a failure — it is often the most valuable row in the table.
It requires a five-point record (CLAUDE.md §3) and a logged decision on what the project
adopts.

## Matrix

| Source item | What it states | Status | Evidence | Notes |
|---|---|---|---|---|
| | | | | |

<!-- Evidence is a citation, not a claim: a stage script and its check label, or a record.
     [E: `symbolic/<topic>/stage_04_reduce.wls`, "matches source Eq. (9)"]
     [E: `validation/<topic>/records/std_case1.json`, field `judged_against`]
     A row marked `reproduced` with no citable evidence is the exact thing this table is for
     preventing. `make check-evidence` checks that the cited label exists; whether the check
     behind it establishes the claim is a human's job. -->

## Extensions

Work beyond the source, listed separately so it can never be read as reproduction of it
(`docs/WORKFLOW.md` §5). Judged against independent benchmarks and physics, not against the
paper.

| Extension | What it establishes | Status | Evidence | Judged against |
|---|---|---|---|---|
| | | | | |

## Summary

Kept current by `/session-close`, so the PI can read one line instead of counting rows.

    Reproduction targets:  0 total — 0 reproduced, 0 in progress, 0 discrepant, 0 not attempted
    Extensions:            0 total — 0 validated, 0 in progress
    Last updated:          (never)
