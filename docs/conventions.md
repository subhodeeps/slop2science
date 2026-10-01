# Conventions register

This file is short on purpose, because it loads into every session. It has one row for each
convention, with the place where the project fixes it. Put longer text in the source audit or
in a derivation write-up.

**Status legend**

| Status | Meaning |
|---|---|
| `SOURCE` | as the primary source states it |
| `ADOPTED` | a PI decision, logged in `docs/decision_log.md` |
| `OPEN` | not settled yet. The source audit or a validation decides it. |
| `DERIVED` | fixed by a recorded, re-runnable script |

`OPEN` is a valid and useful status. Do not guess a convention to fill an empty cell. A guessed
convention is the most expensive kind of entry in this file, because all later work inherits it
silently.

## Register

| Item | Value | Status | Fixed by |
|---|---|---|---|
| | | | |

<!-- Rows to expect, for a typical reproduction project. Delete what does not apply.
     units and normalization          | SOURCE/ADOPTED
     independent/dependent variables  | SOURCE
     sign and orientation conventions | SOURCE — and check the prose against the equations
     definition of each reported quantity | SOURCE
     labelling and ordering of results   | SOURCE
     parameter ranges and regime          | SOURCE
     the production method vs. what is only a benchmark | ADOPTED
     numerical units for reporting        | ADOPTED
     benchmark conversions, one row per benchmark source | per source
-->

## Adding a convention

Add a row. Cite the place where the project fixes the convention. If the convention is a
decision, log the decision. A convention that exists only in a chat reply does not exist. The
next session does not have it.

## When the prose and the equations of the source disagree

They disagree often. This disagreement is the most valuable result of an audit. Do not resolve
it in this file. Record both readings in the five-item form (CLAUDE.md §3). Put `OPEN` in the
table. A logged PI decision or a validation settles it.
