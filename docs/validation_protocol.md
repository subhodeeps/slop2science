# Validation protocol

## 1. The general rule

A computed output is a **candidate**. It becomes an accepted result only after it passes each
applicable check below. The check must state the resolution and the precision. A record must
say that the output passed.

Until then, say "candidate" in code comments, in logs, in reports and in conversation.

## 2. Algebraic checks

For each newly derived operator or equation, do these checks:

- Substitute the result back into what it came from.
- Check the dimensions and the scaling.
- Check a limiting or special case with an independently known answer.
- Check consistency with constraints that the derivation did not use.
- Where it is feasible, make an independent derivation or formulation check.

## 3. Residuals

Evaluate the residual **in the original problem**. Do not evaluate it only in the reformulation
that the solver uses internally (companion linearization, shifted system, preconditioned form).
A small residual in the reformulation proves only that the solver solved the reformulation.

Use a documented, scaled norm. State the scaling. A scaled and an unscaled residual for the
same solution can differ by many orders of magnitude.

## 4. Resolution

Compute at $N$ and $2N$. Record

$$
\Delta_N = |x_{2N} - x_N|.
$$

For quantities near zero, also record the absolute change. A relative measure has no meaning
there, and it reports success.

## 5. Solution shape

Compare the normalized solutions at different resolutions. Use the same variables and
conventions. Compare these items: overlap, pointwise difference, boundary and asymptotic
coefficients, and each derived observable. A scalar can converge while the solution that it
came from does not converge.

## 6. Precision

Repeat representative cases at higher precision. Run **the same generic code path**. Do not use
a separate implementation. If a result changes appreciably with precision, it has not converged,
whatever its residual says. Teams skip this check most often. It is also the most often
decisive check.

## 7. Parameter continuation

If the problem has a parameter, do these steps:

- Solve along a sequence in that parameter.
- Match by proximity **and** by solution overlap. Never match by ordering. The ordering swaps
  at near-degeneracies and gives all later results the wrong labels.
- Flag near-degenerate cases explicitly.
- Keep the whole continuation path. Do not keep only the end point.

## 8. Independent benchmarks

Use the benchmarks that apply. Examples: published tables, the results of an independent
method, a standard solver, a time-domain or direct simulation, or the implementation of
another group.

**State each convention conversion explicitly.** State the *method* of the benchmark.
Agreement with the same method is a consistency check. It cannot validate the method. To report
it as validation is a real and easy error.

**An extension has no source table to check against.** This raises the standard. It does not
lower it (CLAUDE.md §2). The project accepts an extension result on these grounds:

- an exact limiting case that the project already verified
- an independent-method benchmark, where one exists
- internal consistency across resolution, precision and continuation
- a physical requirement that the result must satisfy

If none of these is available, say so explicitly in the record and in the report. An extension
that rests only on its own convergence is a *candidate*, however clean the convergence looks
(`docs/failure_modes.md` entry 4).

## 9. Required limits

State each limit that the results of the project must satisfy. Test it where the project makes
the claim.
Do not test it only at the start. A limit that held for the first topic is not evidence for the
third topic.

## 10. Spurious outputs

Flag these outputs: resolution-sensitive, precision-sensitive, poor-residual,
boundary-irregular and non-continuable outputs, and obvious discretization artefacts.

**Do not remove an unusual result without a diagnostic.** It is an artefact that you can name.
Or it is a result that you did not expect. The difference matters. Record which one it is, and
why.

## 11. Reproducibility

A script generates each table and figure. Each one records these items: parameters, resolution,
precision, solver, tool versions, git commit and benchmark source. Never edit a generated table
or a record by hand. A hook blocks this. A changed number is a new run.

## 12. Result records

Each candidate or accepted result is one JSON object at
`validation/<topic>/records/<run-id>.json`. Use `make new-record` (`scripts/new_record.py`) to
create the first record. After that, the driver writes the records. Then the same run produces
the number and its provenance.

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

`make check-docs` requires the fields `status`, `kind`, `judged_against` and `git`. It fails
without them. It also fails on a record that has `status` equal to `accepted` while one of its
own `*flag` fields is true.

A script produces the accepted tables in `validation/<topic>/accepted/` from the records. A
hook protects them against manual editing.

## 13. Project-specific criteria

<!-- After /init-paper: add the thresholds of this project, the precision tiers that it uses,
     the benchmarks that will judge it, and each criterion above that does not apply, with the
     reason that it does not apply. Never drop a criterion silently.
     Put the numerical thresholds in ONE place in the code. Do not duplicate them across
     drivers. Duplicated tolerances drift. Then two runs "pass" against different bars. -->

(`/init-paper` fills this section. Refine it when the methods of the project settle.)
