# Benchmark provenance — what a header must establish

A benchmark number is evidence only if a reader can tell where it came from. The reader must
also know what it means and what to do to compare it. The header answers five questions.

## 1. Which work, which version?

State the authors, the title, the venue, the identifier and the **version that you consulted**.
A preprint and its journal version can differ in exactly the equation or table that you use.

## 2. Where in that work?

State the table or figure number and the page. "From the paper" is not a location. If you read
the numbers from a figure and not from a table, say so and state the precision of the reading.
This is a much weaker benchmark. Do not report it as a tabulated benchmark.

## 3. Which method produced these numbers?

Read the caption and the method section of the source. Do **not** infer the method from these
items:

- an earlier header in this repository (this is how a wrong label spreads)
- the general reputation of the paper, or its title
- the method that made the paper known, when the table in question used another method

This matters because it decides what the comparison proves:

| Method of the benchmark and method of this project | What agreement establishes |
|---|---|
| different method | the method is validated (the strong case) |
| same method | the implementations are consistent. The method itself is untested. |
| an earlier run of the project | a regression check only |

If you cannot establish the method of a benchmark, record `method: unknown`. Do not use the
benchmark to validate anything until you establish the method.

## 4. Which units and conventions, as printed?

State the units, the sign conventions, the orientation, the definition of each quantity, and the
labelling and ordering of the results. Transcribe what the source prints. Do not transcribe what
you believe that it meant.

## 5. Which conversion do you need to compare?

Write the conversion explicitly, as a formula, in the header. "After the usual rescaling" is not
a conversion. The conversion is part of the evidence. You cannot check an agreement that someone
claims without it. A disagreement that you find without it is probably not a disagreement.

## Column citations

If a header mentions a column of the file, the column must exist in that file
(`make check-docs` enforces this). The project added this check because a benchmark once had its
columns labelled as one method while the text of the paper said another method. Nothing noticed.

## If a benchmark and the project disagree

1. Read the table of the source again. Use the `.tex` file or a shipped data file if one exists.
   Otherwise use the rendered page image (`reference/corpus.md`). Never use the text layer.
2. Check the conversion again, in both directions.
3. Check if the value of the source is consistent with its other tables.
4. Only then treat the difference as a discrepancy. Record it in the five-item form (CLAUDE.md
   §3).

Steps 1–3 resolve most apparent disagreements. If you skip to step 4, you make a discrepancy
record that someone must withdraw.
