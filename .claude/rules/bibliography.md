---
paths:
  - "papers/sources.yaml"
  - "papers/refs.bib"
  - "docs/literature/**"
  - "reports/**"
---

# Bibliography — rules

Every entry carries every identifier that exists for that work:

- `doi` — required for anything that has one. Preprints are excepted only when no DOI
  genuinely exists, not because looking it up is inconvenient.
- `eprint` + `archivePrefix` + `primaryClass` — all three together, for anything on arXiv.
  An `eprint` without its siblings is an incomplete entry, not a complete one.
- `url` — only when neither a DOI nor a preprint ID identifies the work.
- Works predating both: record `publisher`, `edition`, `isbn`, and a comment stating why no
  DOI or eprint is given.

## Verification, not construction

- Identifiers are **verified against the actual source** before being recorded, never
  guessed and never assembled from a publisher's URL pattern.
- A DOI that resolves to a *different* work than the one cited is worse than a missing DOI.
  Check what it resolves to.
- If an identifier cannot be found, record that it could not be found. Do not leave the field
  out silently, and do not invent one.
- Cite the version actually consulted. Preprint and journal versions differ, sometimes in the
  equation the project depends on.
