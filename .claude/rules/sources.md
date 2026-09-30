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

## Reading a source

- **Read equations, tables and numbers from the rendered page image**, not the extracted text
  layer, whenever fractions, stacked sub/superscripts or tabulated columns are involved.
  Text-layer extraction reorders nested structure silently and confidently.
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
