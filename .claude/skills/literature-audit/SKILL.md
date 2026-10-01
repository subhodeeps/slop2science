---
name: literature-audit
description: Audit primary literature, conventions, equations, benchmark data and claims. Reconcile notation, unit and sign conventions before any comparison. Use it each time an external equation, number or citation enters the project.
when_to_use: 'Trigger phrases: benchmark, published values, compare with the literature, convention conversion, citation, DOI, arXiv, what does that paper say, provenance, intake a source'
---

# Literature audit

## Procedure

1. State the exact claim that you investigate. State the claim, not the topic.
2. Locate the **primary** source. A review is acceptable only if the review *is* the claim.
3. Read the relevant sections. Record the section, equation and table numbers, and the exact
   version (preprint vN or journal). They differ, sometimes in the equation that you need.
4. Record the identifiers (DOI, arXiv ID with `archivePrefix` and `primaryClass`) and **verify**
   them against the source itself. Then add them to `papers/sources.yaml`
   (`.claude/rules/bibliography.md`). Never construct an identifier from a pattern.
5. Record the notation, assumptions and parameter regime of the source.
6. Record its conventions: units, signs, orientation, the definition of each reported quantity,
   and how it labels and orders results.
7. **Convert conventions explicitly, in writing, before you compare anything.** Two datasets are
   never "inconsistent" until you write out the conversion and apply it.
8. Identify the disagreements. Cross-check anything important against an independent source
   before it changes a convention of the project.

## Prefer the source to the PDF

Before you read a PDF, check if the LaTeX source exists:

    make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>

This command fetches the arXiv **e-print tarball** and the PDF. The source gives the equation as
the authors wrote it. It gives the figure files behind each plot. It sometimes gives the
`.dat` or `.csv` file behind a table. That file is a benchmark with real provenance. It is not
digits that someone read from a figure.

**The order is: the `.tex` file first, then a shipped data file or figure file, then the
rendered page, and never the text layer.** `reference/corpus.md` states the order one time. It
also gives the reasons, the narrow remaining job of the page and the rules for version pinning.

The PI can also have the work in a local Zotero or Calibre library. This is the usual route for
papers from before arXiv, books and works that only a journal published. These libraries hold
thousands of items. **Search them with a targeted query. Never browse them.** When you have the
item, `library.py show` reads all of its metadata. `library.py import` brings one item in: a
small file, the full record, and entries for `sources.yaml` and `refs.bib`, marked unverified.
`reference/local_libraries.md` gives the procedure, the read-only discipline, and the ways in
which a catalogue entry can be wrong.

## When there is no source

Some works have no source: older papers, books, works that only a journal published, and
submissions that only exist as a PDF. In that case **read the rendered page as an image.** Do
not rely on the extracted text layer for anything with a fraction, a stacked subscript or
superscript, a matrix, or tabulated columns. (A figure is a different case. If a source exists,
use its figure file. Do not use the page.)

This is slow, and it is worth it. In the project that this template came from, three
documentation errors had the most consequence. They were a dropped term in an asymptotic
expression, a sign convention with the wrong attribution, and a benchmark column with the wrong
label. All three came from the text or OCR layer of a nested structure, and not from the page.
Text extraction reorders nested structure silently. The result looks plausible. The order and
the reasons are in `reference/corpus.md`.

## Benchmark data

Put tables in `validation/benchmarks/<source><year>_<what>.csv` with a provenance header:

    # source:      <authors, title, journal/preprint, identifier, version>
    # from:        Table N / Figure N, page N
    # method:      <the method that actually produced these numbers, per the source's own
    #               caption — NOT inferred from a previous header or the source's reputation>
    # units:       <as printed>
    # conventions: <as printed>
    # conversion:  <what must be done to compare with this project, explicitly>
    # columns:     <name each column>

Then label the kind of evidence:

- **independent-method.** A method that is different from the method of this project produced
  the numbers. This evidence validates a method.
- **same-method.** The same method produced the numbers. This is a consistency check. It cannot
  validate the method. To report it as validation is a real and easy error.

## Intake of a source that the PI dropped in

`papers/_drop/` is transient, and the session-start hook reports it. For each file, do these
steps:

1. Identify the file.
2. Verify its identifiers.
3. Register it in `papers/sources.yaml` with its role.
4. Move it to `papers/` or `papers/background/`.
5. Leave the drop folder empty.

Never leave a source in the drop folder "for now". An unregistered source that someone cites
later has no provenance.

## Quote before you cite

**Quote the passage word for word from the local file before you cite it.** Do not paraphrase
from memory. Do not summarize. Use the actual words, from the actual file on disk, in the
record. A citation that you make without a new reading of the source is a recalled citation.
Recall is where a plausible and wrong equation number, page or attribution comes from.

This costs little, because the source is in `papers/` or `papers/source/`. It is the most
effective guard against a fabricated reference. A quote exists in the file, or it does not.

## Never

- Invent a citation, DOI, page, equation number or value. If you cannot find it, say so.
- Report agreement without a statement of the conversion and the tolerance.
- Treat the stated equation of one paper as ground truth for a discrepancy that would change a
  convention of the project, without a second independent source.
