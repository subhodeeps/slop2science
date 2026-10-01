---
paths:
  - "papers/sources.yaml"
  - "papers/refs.bib"
  - "docs/literature/**"
  - "reports/**"
---

# Bibliography — rules

Each entry carries each identifier that exists for the work:

- `doi`: required for any work that has a DOI. A preprint is an exception only if no DOI exists.
  It is not an exception because the lookup is inconvenient.
- `eprint`, `archivePrefix` and `primaryClass`: give all three together for any work on arXiv.
  An `eprint` without the other two is an incomplete entry.
- `url`: use it only if neither a DOI nor a preprint ID identifies the work.
- Works that are older than both: record `publisher`, `edition` and `isbn`. Add a comment that
  states why the entry has no DOI or eprint.

## Verify. Do not construct.

- **Verify identifiers against the actual source** before you record them. Never guess an
  identifier. Never build one from the URL pattern of a publisher.
- A DOI that resolves to a *different* work than the cited work is worse than a missing DOI.
  Check what the DOI resolves to.
- If you cannot find an identifier, record that you did not find it. Do not omit the field
  silently. Do not invent an identifier.
- Cite the version that you consulted. The preprint and the journal version differ, sometimes
  in the equation that the project depends on.
