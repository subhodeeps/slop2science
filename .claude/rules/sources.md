---
paths:
  - "papers/**"
  - "docs/literature/**"
  - "validation/benchmarks/**"
---

# Sources and benchmark data — rules

- `papers/**` is **read-only**, and a hook guards it. The curated logs are the exception
  (`papers/sources.yaml` and the READMEs). Put findings in `docs/literature/<topic>.md`. Never
  put them in the sources directory.
- Register each source in `papers/sources.yaml`. Give each identifier that exists for the source,
  its role (primary, benchmark, method-reference or background) and the exact version that you
  consulted. A source that the project uses and does not register is a provenance defect.
- Git ignores PDFs by default. Commit the registry. The PI decides whether to commit the PDF of a
  publisher (`TEMPLATE_GUIDE.md` §4).
- Sources that the PI drops in `papers/_drop/` are transient. Register each one, move it onward
  and empty the folder. The session-start hook reports a drop folder that is not empty.
- Register a source from a local library (`scripts/library.py import`) with `verified: false`.
  Catalogue metadata can be wrong. The entry stays unverified until someone checks its
  identifiers and its file against the first page of the document. `make check-docs` counts the
  unverified entries.

## Read a source

- **Read the best form that exists.** Use the `.tex` source first. Then use a shipped data file
  or figure file. Then use the rendered page image. **Never use the extracted text layer** for
  anything with a fraction, stacked indices or columns. State which form you used.
  `.claude/skills/literature-audit/reference/corpus.md` states the order one time. It also
  states what the page is still for when a source exists.
- Each time a number or an equation enters this project, record the equation or table number and
  the version. "As given in the paper" is not a citation.
- For a contested item, quote the own words of the source. Do not paraphrase them into the
  vocabulary of the project. A paraphrase is where a discrepancy disappears.

## Benchmark data

- Put benchmark tables in `validation/benchmarks/<source><year>_<what>.csv`. Start each file
  with a provenance header. The header names these items:
  - the source and its identifier
  - the table or figure that the numbers came from
  - **the method that produced the numbers.** Read the caption of the source. Never infer the
    method from an earlier header or from the reputation of the source.
  - the units and conventions as printed
  - the conversion that is necessary to compare with this project
- If a provenance header cites a column, it must cite a column of its own file
  (`make check-docs` enforces this).
- Agreement with the same method and agreement with an independent method are different kinds
  of evidence. Label which one a benchmark gives. A same-method check cannot validate the
  method.
