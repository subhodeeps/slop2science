# validation/benchmarks — published data with provenance

One CSV per source table. Naming: `<FirstAuthor><Year>_<what>.csv`.

Every file starts with a provenance header, and `make check-docs` fails if the header cites a
column the file does not have:

    # source:      <authors, title, venue, identifier, version consulted>
    # from:        Table N / Figure N, page N
    # method:      <the method that produced these numbers, per the source's OWN caption>
    # evidence:    independent-method | same-method | regression
    # units:       <as printed>
    # conventions: <as printed>
    # conversion:  <the explicit conversion to this project's conventions>
    # columns:     <name each column and its meaning>
    # retrieved:   <date, and by whom or which script>

## The `method` field is the one that gets it wrong

Read the source's own caption and method section. Do **not** infer the method from a previous
header in this repository, from the paper's title, or from what the group is best known for —
a paper's table is often produced by a different method than the one it is famous for. A
benchmark whose method you cannot establish is recorded as `method: unknown` and validates
nothing until it is established.

This field decides what agreement means:

| Benchmark's method | Agreement establishes |
|---|---|
| different from this project's | the method is validated |
| the same as this project's | implementations are consistent; the method is untested |
| this project's own earlier run | a regression check only |

Numbers are transcribed exactly as printed, to the printed precision. Never round, extend, or
recompute a published value — a converted value goes in a separate column with the conversion
in the header.
