# validation/benchmarks — published data with provenance

Use one CSV for each source table. Name it `<FirstAuthor><Year>_<what>.csv`.

Each file starts with a provenance header. `make check-docs` fails if the header cites a column
that the file does not have:

    # source:      <authors, title, venue, identifier, version consulted>
    # from:        Table N / Figure N, page N
    # method:      <the method that produced these numbers, per the OWN caption of the source>
    # evidence:    independent-method | same-method | regression
    # units:       <as printed>
    # conventions: <as printed>
    # conversion:  <the explicit conversion to the conventions of this project>
    # columns:     <name each column and its meaning>
    # retrieved:   <date, and by whom or which script>

## The `method` field is the field that people get wrong

Read the caption and the method section of the source. Do **not** infer the method from an
earlier header in this repository. Do not infer it from the title of the paper or from the
fame of the group. A table in a paper often comes from a method that is not the method of the paper's
fame. If you cannot establish the method of a benchmark, record `method: unknown`. The
benchmark validates nothing until you establish the method.

This field decides what agreement means:

| Method of the benchmark | Agreement establishes |
|---|---|
| different from the method of this project | the method is validated |
| the same as the method of this project | the implementations are consistent. The method is untested. |
| an earlier run of this project | a regression check only |

Transcribe numbers exactly as printed, to the printed precision. Never round, extend or
recompute a published value. Put a converted value in a separate column. Put the conversion in
the header.
