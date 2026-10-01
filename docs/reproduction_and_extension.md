# Reproduction and extension

**This file tracks the two parts of the project side by side** (CLAUDE.md §2). Reproduction
shows that the machinery is sound. The extension is the new work built on it. Neither table
below is subordinate to the other. The third table exists because the extension can become a
future publication.

Without this file, people answer the question "how far along is this?" from memory and from the
document that they opened last. The source audit (`/source-audit`) and the scope decisions of
the PI create the rows. Each `/session-close` updates them.

## Status values

| Status | Meaning |
|---|---|
| `not attempted` | in scope, not yet started |
| `in progress` | work is in progress now. Name the stage or the run. |
| `established` | done, with re-runnable evidence cited (`reproduced` for §1 rows) |
| `discrepant` | the result of the project disagrees with the source. A five-item record exists. |
| `not reproducible` | cannot be obtained from what the source provides. State what is missing. |
| `negative` | the project tried the extension and it did not work. **This is a result. Keep it.** |
| `out of scope` | the PI excluded it deliberately. State why and cite the decision. |

`discrepant` is a **result**. It is not a failure. It is often the most valuable row in §1. It
needs a five-item record (CLAUDE.md §3) and a logged PI decision about what the project adopts.

`negative` matters for the same reason. Nobody writes down an extension that failed, and
everybody tries it again. Record what you tried, how far it went and why it stopped.

## 1. Reproduction — the claims of the source

The source is the standard here. Use one row for each equation, table and figure that the PI
puts in scope.

| Source item | What it states | Status | Evidence | Notes |
|---|---|---|---|---|
| | | | | |

## 2. Extension — the new results of this project

**Physics and independent benchmarks** are the standard here. The source is never the standard.
The source does not contain these results, and therefore it cannot validate them
(`docs/WORKFLOW.md` §5). The PI decides the scope.

| Extension | The question it answers | Status | Evidence | Judged against | Decision |
|---|---|---|---|---|---|
| | | | | | |

`Judged against` names the real standard: an independent-method benchmark, an exact limiting
case, a physical requirement, or an argument from convergence and continuation. "Consistent with
the source" is not an entry here. That entry belongs in §1.

## 3. New work — what becomes the paper

This section lists the manuscript that the extension serves. It keeps the deliverable visible
while the derivations and runs accumulate. Then nobody assembles the deliverable from memory at
the end.

| Deliverable | Depends on | Status | Where |
|---|---|---|---|
| Result / figure / table for the manuscript | §2 rows it rests on | `not attempted` | `reports/`, `figures/` |

The PI decides what goes in, what the project claims, the order and the authorship (CLAUDE.md
§1). Claude drafts. Claude never decides a claim.

<!-- Evidence is a citation. It is not a claim. Cite a stage script and its check label, or a
     record:
     [E: `symbolic/<topic>/stage_04_reduce.wls`, "matches source Eq. (9)"]
     [E: `validation/<topic>/records/std_case1.json`, field `judged_against`]
     A row marked established or reproduced with no citable evidence is what this table
     prevents. `make check-evidence` checks that the cited label exists. A person must decide
     if the check behind the label establishes the claim. -->

## Summary

`/session-close` keeps this block current. Then the PI reads one block and does not count rows.

    Reproduction:  0 in scope — 0 reproduced, 0 in progress, 0 discrepant, 0 not attempted
    Extension:     0 in scope — 0 established, 0 in progress, 0 negative, 0 not attempted
    New work:      0 deliverables — 0 done
    Last updated:  (never)
