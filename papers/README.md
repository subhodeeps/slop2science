# papers — sources (read-only)

Edits here are blocked by a hook, except the curated logs (`sources.yaml` and the READMEs).
Findings about a source go to `docs/literature/<topic>.md` or the source audit, never into
this folder.

- `sources.yaml` — **the registry.** Every source used by this project, with every identifier
  that exists for it, its role, and the version consulted. Committed.
- `<identifier>.pdf` — the primary source and anything else fetched. **Gitignored by
  default**: whether to commit a publisher's PDF is the PI's call, not the template's
  (`TEMPLATE_GUIDE.md` §4). The registry keeps every source identifiable and re-fetchable
  either way.
- `background/` — secondary literature: works cited by the primary source, method references,
  benchmark sources. Fetched only against a stated need, never speculatively.
- `_drop/` — the PI's transient drop folder. Gitignored except this README. The session-start
  hook reports it when non-empty; intake empties it
  (`.claude/skills/literature-audit/SKILL.md`).

Fetching: `make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>`. arXiv is fetched; a DOI
or publisher URL is registered and left for the PI to place in `_drop/`.

**Read equations, tables and numbers from the rendered page, not the extracted text layer.**
This is where this project's ancestor's three most expensive documentation errors came from
(`docs/failure_modes.md` entry 2).
