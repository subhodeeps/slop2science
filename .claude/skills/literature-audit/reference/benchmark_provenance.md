# Benchmark provenance — what a header must establish

A benchmark number is evidence only if a reader can tell where it came from, what it means,
and what had to be done to compare it. The header answers five questions.

## 1. Which work, which version?

Authors, title, venue, identifier, and the **version consulted**. A preprint and its journal
version can differ in exactly the equation or table being used.

## 2. Where in that work?

Table or figure number and page. "From the paper" is not a location. If the numbers were read
off a figure rather than a table, say so and state the read precision — that is a much weaker
benchmark and must not be reported as a tabulated one.

## 3. By what method were these numbers produced?

Read the source's own caption and method section. Do **not** infer the method from:

- a previous header in this repository (that is how a mislabelling propagates);
- the paper's general reputation or its title;
- the method the paper is best known for, when the table in question used another.

This matters because it determines what the comparison proves:

| Benchmark's method vs. this project's | What agreement establishes |
|---|---|
| different method | the method is validated (the strong case) |
| same method | implementations are consistent; the method itself is untested |
| the project's own earlier run | a regression check only |

A benchmark whose method you cannot establish is recorded as `method: unknown` and is not
used to validate anything until it is established.

## 4. In what units and conventions, as printed?

Units, sign conventions, orientation, the definition of every quantity, the labelling and
ordering of results. Transcribe what is printed, not what you believe was meant.

## 5. What conversion is needed to compare?

Written out explicitly, as a formula, in the header. Not "after the usual rescaling". The
conversion is part of the evidence: an agreement claimed without it cannot be checked, and a
disagreement found without it is probably not a disagreement.

## Column citations

A header that mentions one of the file's columns must name a real column of that file —
`make check-docs` enforces this. It was added because a benchmark's columns were once
mislabelled as one method while the paper's own text said another, and nothing noticed.

## When a benchmark and the project disagree

1. Re-read the source's table from the `.tex` or a shipped data file if there is one, else
   as a rendered page image (`reference/corpus.md`) — never the text layer.
2. Re-check the conversion, in both directions.
3. Check whether the source's own value is internally consistent with its other tables.
4. Only then treat it as a discrepancy, and record it in the five-point form (CLAUDE.md §3).

Steps 1–3 resolve most apparent disagreements. Skipping to step 4 produces a discrepancy
record that has to be withdrawn.
