# Conventions register

Short by design: this file loads into every session. One row per convention, with where it is
fixed. Anything longer than a row belongs in the source audit or a derivation write-up.

**Status legend**

| Status | Meaning |
|---|---|
| `SOURCE` | as stated in the primary source |
| `ADOPTED` | a PI decision, logged in `docs/decision_log.md` |
| `OPEN` | not yet settled — to be decided by the source audit or a validation |
| `DERIVED` | fixed by a recorded, re-runnable script |

`OPEN` is a legitimate and useful state. A convention guessed to avoid an empty cell is the
single most expensive kind of entry in this file, because everything downstream inherits it
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

Add a row, cite where it is fixed, and log the decision if it is a decision. A convention that
exists only in a chat reply does not exist: the next session will not have it.

## When the source's prose and its equations disagree

They do, more often than one expects, and that disagreement is the most valuable thing an
audit finds. Do not resolve it here. Record both readings in the five-point form
(CLAUDE.md §3), put `OPEN` in this table, and let a logged PI decision or a validation settle
it.
