# Validation protocol

## 1. The general rule

A computed output is a **candidate**. It becomes an accepted result only after passing every
applicable check below, at a stated resolution and precision, with a record that says so.

Say "candidate" until then — in code comments, in logs, in reports, and in conversation.

## 2. Algebraic checks

For every newly derived operator or equation:

- direct substitution back into what it came from;
- dimensional and scaling consistency;
- a limiting or special case whose answer is known independently;
- consistency with constraints not used in the derivation;
- an independent derivation or formulation check where feasible.

## 3. Residuals

Evaluate the residual **in the original problem**, not only in the reformulation the solver
uses internally (companion linearization, shifted system, preconditioned form). A small
residual in the reformulation proves the reformulation was solved.

Use a documented, scaled norm, and state the scaling. An unscaled and a scaled residual for
the same solution can differ by many orders of magnitude.

## 4. Resolution

Compute at $N$ and $2N$, and record

$$
\Delta_N = |x_{2N} - x_N|.
$$

For near-zero quantities record the absolute change as well — a relative measure is
meaningless there and will report success.

## 5. Solution shape

Compare normalized solutions between resolutions, in the same variables and conventions:
overlap, pointwise difference, boundary/asymptotic coefficients, and any derived observable.
A scalar can be converged while the solution it came from is not.

## 6. Precision

Repeat representative cases at higher precision, running **the same generic code path** — not
a separate implementation. A result that moves appreciably with precision is unresolved,
whatever its residual says. This check is the one most often skipped and most often decisive.

## 7. Parameter continuation

Where the problem has a parameter:

- solve along a sequence in that parameter;
- match by proximity **and** by solution overlap, never by ordering — ordering swaps at
  near-degeneracies and mislabels everything downstream;
- flag near-degenerate cases explicitly;
- keep the whole continuation path, not just the endpoint.

## 8. Independent benchmarks

As applicable: published tables; an independent method's results; a standard solver; a
time-domain or direct simulation; another group's implementation.

**State every convention conversion explicitly**, and state the benchmark's *method*.
Same-method agreement is a consistency check and cannot validate the method — reporting it as
though it can is a real and easy error.

**For an extension there is no source table to check against**, and that raises the bar rather
than lowering it (CLAUDE.md §2). An extension result is accepted on: an exact limiting case
the project has already verified; an independent-method benchmark where one exists; internal
consistency across resolution, precision and continuation; and a physical requirement it must
satisfy. Where none of those is available, say so explicitly in the record and in the report —
an extension resting only on its own convergence is a *candidate*, however clean that
convergence looks (`docs/failure_modes.md` entry 4).

## 9. Required limits

State each limit the project's results must satisfy, and test it where the claim is made —
not once at the start. A limit that held for the first topic is not evidence for the third.

## 10. Spurious outputs

Flag: resolution-sensitive, precision-sensitive, poor-residual, boundary-irregular,
non-continuable outputs, and obvious discretization artefacts.

**Do not remove an unusual result without a diagnostic.** It is either an artefact you can
name or a result you did not expect, and the difference matters. Record which, and why.

## 11. Reproducibility

Every table and figure is generated from a script and records: parameters, resolution,
precision, solver, tool versions, git commit, benchmark source. Never edit a generated table
or a record by hand — a hook blocks it, and a changed number is a new run.

## 12. Result records

Each candidate or accepted result is one JSON object at
`validation/<topic>/records/<run-id>.json`. Scaffold the first one with
`make new-record` (`scripts/new_record.py`); after that the driver writes them itself, so the
number and its provenance are produced by the same run.

    {
      "topic": "...", "run_id": "...",
      "kind": "reproduction|extension",
      "judged_against": "the source's Eq./Table N, or the named benchmark/physics",
      "params": {...},
      "resolution": [N, 2N], "eltype": ["working", "extended"],
      "result": {"value": "...", "units": "..."},
      "residual": ..., "delta_resolution": ..., "delta_precision": ..., "overlap": ...,
      "status": "candidate|accepted|flagged|rejected", "reject_reason": null,
      "benchmark": {"file": "validation/benchmarks/...", "method": "...",
                    "converted": true, "conversion": "..."},
      "generated_code": {"file": "symbolic/generated/...", "source_sha256": "..."},
      "tools": {"mathematica": "...", "julia": "...", "python": "..."},
      "script": "validation/<topic>/run_....jl",
      "prompt_record": "docs/prompts/<ID>_<topic>.md",
      "created": "...", "git": "<commit>"
    }

`status`, `kind`, `judged_against` and `git` are required; `make check-docs` fails without
them, and fails on a record whose `status` is `accepted` while any of its own `*flag` fields
is true.

Accepted tables in `validation/<topic>/accepted/` are produced from records by a script, and
are hook-protected against manual editing.

## 13. Project-specific criteria

<!-- After /init-paper: add this project's thresholds, the precision tiers it uses, the
     benchmarks it will be judged against, and any criterion above that does not apply —
     with the reason it does not. A criterion is never silently dropped.
     Numerical thresholds live in ONE place in code, not duplicated across drivers:
     duplicated tolerances drift, and then two runs "pass" against different bars. -->

(to be filled in by `/init-paper` and refined as the project's methods settle)
