# validation — runs, records and benchmarks

    <topic>/              validation drivers for one topic
    <topic>/records/      one JSON record for each candidate or accepted result (hook-protected)
    <topic>/accepted/     tables that a script generates from records (hook-protected)
    benchmarks/           published data, as CSV with a provenance header

## A result is not a number

A solver output is a **candidate** until it passes `docs/validation_protocol.md`. To accept it,
you need these items:

- the residual in the original problem
- stability in resolution and precision
- convergence of the solution shape
- boundary regularity
- continuation, where a parameter exists
- a benchmark from an independent method, with its conversion written out

Each run writes its own record. Therefore the number and its provenance come from the same
run. A hook protects records against hand edits: **a changed number is a new run.** Use
`make new-record` to create the first record.

## Reproduction and extension live together, marked

Both kinds of work share drivers here. Often one driver tests the case of the source and the
adopted case of the project side by side. The fields `kind` and `judged_against` of each record
mark the difference. The header of each script marks it too. Directories do not mark it
(`docs/WORKFLOW.md` §5).

## Benchmarks

Name each file `benchmarks/<source><year>_<what>.csv`. Each file has a provenance header with
these items:

- the source
- the table that the numbers came from
- **the method that produced the numbers**
- the units and conventions as printed
- the conversion that is necessary to compare

Agreement with the same method is a consistency check. Only agreement with an independent
method validates a method. Label which one each benchmark provides. For details, see
`.claude/skills/literature-audit/reference/benchmark_provenance.md`.
