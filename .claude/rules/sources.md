---
paths:
  - "papers/**"
  - "docs/literature/**"
  - "validation/benchmarks/**"
---

# Sources and benchmark data — rules

- `papers/**` is **read-only** and hook-guarded, except the curated logs
  (`papers/sources.yaml`, the READMEs). Findings go to `docs/literature/<topic>.md`, never
  into the sources directory.
- Every source is registered in `papers/sources.yaml` with every identifier that exists for
  it, its role (primary / benchmark / method-reference / background), and the exact version
  consulted. A source used but unregistered is a provenance defect.
- PDFs are gitignored by default; the registry is committed. Whether to commit a publisher's
  PDF is the PI's call (`TEMPLATE_GUIDE.md` §4).
- Sources the PI drops in `papers/_drop/` are transient: register, move onward, and empty the
  folder. The session-start hook reports a non-empty drop folder.
- A source brought in from a local library (`scripts/library.py import`) is registered
  `verified: false`. Catalogue metadata can be wrong, so it stays unverified until its
  identifiers and file have been checked against the document's own first page.
  `make check-docs` counts the unverified ones.

## Reading a source

- **Read from the best form that exists: the `.tex` source first, then a shipped data or
  figure file, then the rendered page image, and never the extracted text layer** for
  anything with a fraction, stacked indices or columns. Say which you used. The order, and
  what the page is still for when a source exists, is stated once in
  `.claude/skills/literature-audit/reference/corpus.md`.
- Record the equation or table number and the version every time a number or equation enters
  this project. "As given in the paper" is not a citation.
- Quote the source's own words for anything contested, rather than paraphrasing it into the
  project's vocabulary — the paraphrase is where a discrepancy gets smoothed away.

## Benchmark data

- Benchmark tables go to `validation/benchmarks/<source><year>_<what>.csv` with a provenance
  header naming: the source and its identifier, the table/figure it came from, **the method
  the numbers were actually produced by** (read the source's own caption — never infer it
  from a previous header or the source's reputation), the units and conventions as printed,
  and the conversion needed to compare with this project.
- A provenance header that cites a column must cite one of that file's own columns
  (`make check-docs` enforces this).
- Same-method agreement and independent-method agreement are different evidence. Label which
  one a benchmark provides; a same-method check cannot validate the method.
