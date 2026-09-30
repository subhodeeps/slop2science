# Reproduction and extension

**The two halves of this project, tracked side by side** (CLAUDE.md §2). Reproduction
establishes that the machinery is sound; extension is the new work built on it. Neither table
below is subordinate to the other, and the third exists because the extension is meant to
become a paper.

Without this file, "how far along is this?" gets answered from memory and from whichever
document was opened most recently. Rows are created by the source audit (`/source-audit`) and
by the PI's scope decisions, and updated at every `/session-close`.

## Status values

| Status | Meaning |
|---|---|
| `not attempted` | in scope, not yet started |
| `in progress` | being worked on now; name the stage or run |
| `established` | done, with re-runnable evidence cited (`reproduced` for §1 rows) |
| `discrepant` | the project's result disagrees with the source; five-point record exists |
| `not reproducible` | cannot be obtained from what the source provides; say what is missing |
| `negative` | the extension was attempted and did not work. **A result. Keep it.** |
| `out of scope` | deliberately excluded by the PI; say why and cite the decision |

`discrepant` is a **result**, not a failure — often the most valuable row in §1. It requires a
five-point record (CLAUDE.md §3) and a logged PI decision on what the project adopts.

`negative` matters for the same reason: an extension that was tried and failed is the kind of
thing nobody writes down and everybody re-attempts. Record what was tried, how far it got, and
why it stopped.

## 1. Reproduction — the source's own claims

Judged against **the source**. One row per equation, table and figure the PI has put in scope.

| Source item | What it states | Status | Evidence | Notes |
|---|---|---|---|---|
| | | | | |

## 2. Extension — this project's new results

Judged against **physics and independent benchmarks**, never against the source: the source
does not contain these results and therefore cannot validate them
(`docs/WORKFLOW.md` §5). Scope is the PI's decision.

| Extension | The question it answers | Status | Evidence | Judged against | Decision |
|---|---|---|---|---|---|
| | | | | | |

`Judged against` names the actual standard — an independent-method benchmark, an exact
limiting case, a physical requirement, a convergence-plus-continuation argument. "Consistent
with the source" is not an entry here; if it were, it would belong in §1.

## 3. New work — what becomes the paper

The manuscript the extension is for. Kept here so the deliverable stays visible while the
derivations and runs accumulate, rather than being assembled from memory at the end.

| Deliverable | Depends on | Status | Where |
|---|---|---|---|
| Result / figure / table for the manuscript | §2 rows it rests on | `not attempted` | `reports/`, `figures/` |

The PI decides what goes in, what is claimed, the ordering, and authorship (CLAUDE.md §1).
Claude drafts and never decides a claim.

<!-- Evidence is a citation, not a claim: a stage script and its check label, or a record.
     [E: `symbolic/<topic>/stage_04_reduce.wls`, "matches source Eq. (9)"]
     [E: `validation/<topic>/records/std_case1.json`, field `judged_against`]
     A row marked established/reproduced with no citable evidence is the exact thing this
     table prevents. `make check-evidence` checks that the cited label exists; whether the
     check behind it establishes the claim is a human's job. -->

## Summary

Kept current by `/session-close`, so the PI reads one block instead of counting rows.

    Reproduction:  0 in scope — 0 reproduced, 0 in progress, 0 discrepant, 0 not attempted
    Extension:     0 in scope — 0 established, 0 in progress, 0 negative, 0 not attempted
    New work:      0 deliverables — 0 done
    Last updated:  (never)
