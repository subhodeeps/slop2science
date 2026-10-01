# papers — sources (read-only)

A hook blocks edits here, except edits to the curated logs (`sources.yaml` and the READMEs).
Put findings about a source in `docs/literature/<topic>.md` or in the source audit. Never put
them in this folder.

- `sources.yaml` — **the registry.** It lists each source that this project uses, with each
  identifier that exists for the source, its role and the version that you consulted. Commit it.
- `<identifier>.pdf` — the primary source and each other file that you fetch. **Git ignores
  these files by default.** The PI decides whether to commit the PDF of a publisher. The
  template does not decide this (`TEMPLATE_GUIDE.md` §4). The registry keeps each source
  identifiable and possible to fetch again, whichever the PI decides.
- `imported/` — items that `scripts/library.py import` brings in from the Zotero or Calibre
  library of the PI. It contains the file, if the file is small, and a `metadata.json`. Git
  ignores it. The registry entry and `refs.bib` (committed) carry the identifiers and the
  provenance.
- `background/` — secondary literature: works that the primary source cites, method
  references and benchmark sources. Fetch a work only if a stated need exists. Never fetch
  speculatively.
- `_drop/` — the transient drop folder of the PI. Git ignores it, except this README. The
  session-start hook reports the folder when it is not empty. The intake empties it
  (`.claude/skills/literature-audit/SKILL.md`).

To fetch a source: `make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>`. The command
fetches an arXiv paper. It registers a DOI or a publisher URL and leaves the file for the PI to
put in `_drop/`.

**If the paper is on arXiv, read the `.tex` file (`papers/source/<id>/`). If it is not, read
the rendered page. Never read the extracted text layer.** The text layer caused the three most
expensive documentation errors in the ancestor of this project (`docs/failure_modes/inherited.md` entry 2). `.claude/skills/literature-audit/reference/corpus.md` states the order one time.
