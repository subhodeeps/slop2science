# validation — runs, records and benchmarks

    <topic>/              validation drivers for one topic
    <topic>/records/      one JSON record per candidate or accepted result (hook-protected)
    <topic>/accepted/     tables generated from records by a script (hook-protected)
    benchmarks/           published data, as CSV with a provenance header

## A result is not a number

A solver output is a **candidate** until it passes `docs/validation_protocol.md`. Acceptance
means: residual in the original problem, resolution and precision stability, solution-shape
convergence, boundary regularity, continuation where a parameter exists, and an
independent-method benchmark with its conversion written out.

Each run writes its own record, so the number and its provenance come from the same run.
Records are hook-protected against hand editing: **a changed number is a new run.** Scaffold
the first one with `make new-record`.

## Reproduction and extension live together, marked

Both kinds of work share drivers here — often one driver tests the source's own case and the
project's adopted case side by side. They are distinguished by the `kind` and
`judged_against` fields of every record and by the header of every script, not by directory
(`docs/WORKFLOW.md` §5).

## Benchmarks

`benchmarks/<source><year>_<what>.csv`, each with a provenance header naming the source, the
table it came from, **the method that actually produced the numbers**, the units and
conventions as printed, and the conversion needed to compare.

Same-method agreement is a consistency check; only independent-method agreement validates a
method. Label which one each benchmark provides.
Details: `.claude/skills/literature-audit/reference/benchmark_provenance.md`.
