---
name: literature-audit
description: Audit primary literature, conventions, equations, benchmark data and claims; reconcile notation, unit and sign conventions before any comparison. Use whenever an external equation, number or citation enters the project.
when_to_use: 'Trigger phrases: benchmark; published values; compare with the literature; convention conversion; citation; DOI; arXiv; what does that paper say; provenance; intake a source'
---

# Literature audit

## Procedure

1. State the exact claim under investigation. Not the topic — the claim.
2. Locate the **primary** source (not a review, unless the review *is* the claim).
3. Read the relevant sections; record section, equation and table numbers, and the exact
   version (preprint vN vs. journal — they differ, sometimes in the equation you need).
4. Record and **verify** the identifiers (DOI, arXiv ID with `archivePrefix` and
   `primaryClass`) against the source itself, then add them to `papers/sources.yaml`
   (`.claude/rules/bibliography.md`). Never construct an identifier from a pattern.
5. Record the source's notation, assumptions and parameter regime.
6. Record its conventions: units, signs, orientation, the definition of every reported
   quantity, how results are labelled and ordered.
7. **Convert conventions explicitly, in writing, before comparing anything.** Two datasets
   are never "inconsistent" until the conversion has been written out and applied.
8. Identify disagreements. Cross-check anything important against an independent source
   before it changes a project convention.

## Prefer the source over the PDF

Before reading a PDF at all, check whether the LaTeX source exists:

    make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>

fetches the arXiv **e-print tarball** as well as the PDF. The source gives the equation as
the authors wrote it, the figure files behind every plot, and sometimes the `.dat`/`.csv`
behind a table — which is a benchmark with real provenance rather than digits read off a
figure.

**The order is: `.tex` first, then a shipped data or figure file, then the rendered page, and
never the text layer.** It is stated once, with the reasons, the page's narrow remaining job
and the version-pinning rules, in `reference/corpus.md`.

The PI may also have the work in a local Zotero or Calibre library — the usual route for
pre-arXiv papers, books and journal-only works. Those hold thousands of items, so they are
**searched with a targeted query and never browsed**. Once you have the item, `library.py
show` reads all its metadata and `library.py import` brings one item in (a small file, the
full record, and `sources.yaml` / `refs.bib` entries, marked unverified). Procedure, the
read-only discipline, and the ways a catalogue entry can lie: `reference/local_libraries.md`.

## When there is no source

Not every work has one: older papers, books, journal-only works, PDF-only submissions. Then
**read the rendered page as an image.** Do not rely on the extracted text layer for anything
with a fraction, a stacked sub/superscript, a matrix, or tabulated columns. (A figure is a
different case: if there is a source, use its figure file rather than the page.)

Why this is worth the slowness: in the project this template came from, the three most
consequential documentation errors — a dropped term in an asymptotic expression, a
misattributed sign convention, and a mislabelled benchmark column — all traced to reading a
text/OCR layer of a nested structure instead of the page. Text extraction reorders nested
structure silently, and the result reads as perfectly plausible. The order and the reasons:
`reference/corpus.md`.

## Benchmark data

Tables go to `validation/benchmarks/<source><year>_<what>.csv` with a provenance header:

    # source:      <authors, title, journal/preprint, identifier, version>
    # from:        Table N / Figure N, page N
    # method:      <the method that actually produced these numbers, per the source's own
    #               caption — NOT inferred from a previous header or the source's reputation>
    # units:       <as printed>
    # conventions: <as printed>
    # conversion:  <what must be done to compare with this project, explicitly>
    # columns:     <name each column>

Then label what kind of evidence it is:

- **independent-method** — produced by a different method than this project's. This is the
  evidence that validates a method.
- **same-method** — produced by the same method. A consistency check; it cannot validate the
  method, and reporting it as though it does is a real and easy error.

## Intake of a source the PI dropped in

`papers/_drop/` is transient and reported by the session-start hook. For each file: identify
it, verify its identifiers, register it in `papers/sources.yaml` with its role, move it to
`papers/` or `papers/background/`, and leave the drop folder empty. Never leave a source in
the drop folder "for now" — an unregistered source that gets cited later has no provenance.

## Quote before you cite

**Quote the passage verbatim from the local file before citing it.** Not a paraphrase from
memory of having read it, and not a summary: the actual words, from the actual file on disk,
in the record. A citation produced without re-reading the source is a recalled citation, and
recall is where a plausible-but-wrong equation number, page or attribution comes from.

This is cheap — the source is in `papers/` or `papers/source/` — and it is the single most
effective guard against a fabricated reference, because a quote either exists in the file or
it does not.

## Never

- Invent a citation, DOI, page, equation number or value. If you cannot find it, say so.
- Report agreement without stating the conversion and the tolerance.
- Treat one paper's stated equation as ground truth for a discrepancy that would change a
  project convention, without a second independent source.
