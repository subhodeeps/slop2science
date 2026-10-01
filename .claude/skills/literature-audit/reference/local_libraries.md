# Local reference libraries — search, read, import

The PI may keep a Zotero and/or a Calibre library on this machine. This is how to use them
without damaging them and without drowning in them.

    scripts/py scripts/library.py status
    scripts/py scripts/library.py search --author SURNAME [--title WORDS] [--doi DOI]
    scripts/py scripts/library.py show   --zotero ID | --calibre ID      # all metadata, read-only
    scripts/py scripts/library.py bibtex --zotero ID | --calibre ID      # print an entry, write nothing
    scripts/py scripts/library.py import --zotero ID | --calibre ID --dry-run
    scripts/py scripts/library.py import --zotero ID | --calibre ID [--label L] [--role R]
                                         [--max-mb 25] [--no-file] [--formats pdf,epub]

## Search, never browse

These libraries hold thousands of items. `search` requires a query and there is no
list-everything mode, on purpose: enumerating a library spends the session's context and
answers nothing. Search for a specific work you already know you need. If two or three
targeted queries miss, stop and ask. If neither library exists on this machine, say so and
move on; do not search the disk for one.

Search shows real, live works only. Trashed items, attachments and notes are hidden, and when
you give more than one criterion all of them must match.

## Read-only, always

The database is opened through a read-only connection. If the application holds it locked
(Zotero keeps it locked while it runs), the database, with any `-wal` file, is copied to a
scratch location and the copy is read; the output says so. A library file is only ever read
and copied, never moved, renamed or edited. The library is the PI's own long-term store and
this project does not own it.

## Reading one item: `show`

`show` prints everything bibliographic the library knows: every field, full creator names and
roles, identifiers, tags, collections, attachments with their type and size, and for Calibre
the publisher, series, languages, formats and description. It also says what it could **not**
read (a table missing from an older schema, Calibre custom columns), because an empty result
and a failed query are different things.

Deliberately **not** read, because it is personal and a repository gets shared: Zotero notes
and annotations, Calibre ratings, and absolute paths on the PI's machine.

## Importing one item: `import`

Import is a decision, so the unit is exactly one explicitly named item, never "all matches".
Always run `--dry-run` first: it prints every file it would copy or skip, with the reason,
and the BibTeX entry it would add, and writes nothing.

An import:

1. **copies the file into `papers/imported/<label>/`** if it is small. The default limit is
   25 MB per file and three files per item; anything larger is skipped, and the reason is
   recorded. Metadata is recorded regardless. Use `--no-file` for metadata only;
2. **writes `papers/imported/<label>/metadata.json`**, the full record, with a sha256 and size
   for each copied file;
3. **appends an entry to `papers/sources.yaml`** with the identifiers, the provenance (which
   library, which item key, which date) and `verified: false`;
4. **appends a BibTeX entry to `papers/refs.bib`**, marked UNVERIFIED.

Either all of that happens or none of it does: on any failure the directory is removed and
both files are restored to exactly what they were.

It refuses, with a message, when: the item is in the trash, is an attachment or a note, has no
title, or the label, BibTeX key or DOI is already in the bibliography.

`papers/imported/` is gitignored, as the PDFs are: whether to commit someone else's paper is
the PI's call. What **is** committed is the registry entry and `refs.bib`, which carry the
identifiers and provenance.

### What is skipped, and why

| File | Why it is not copied |
|---|---|
| a saved web page (`text/html`) | a snapshot of an abstract page, not the paper |
| catalogued as a PDF but does not start with `%PDF` | a mislabelled attachment |
| over the size limit | too large for a repository; the path is in the metadata |
| missing on this machine | the catalogue knows it, the disk does not |
| stored relative to Zotero's base directory | that is a preference outside the database |

A Zotero snapshot is recognised by its content type. It is not recognised by `linkMode`: a PDF
downloaded from a URL has the same `linkMode` as a saved web page.

## `verified: false` is the point

The import copies what the catalogue says, and **a catalogue can be wrong**: a mislabelled
entry, an attachment that is a different paper or a different version, a wrong or missing DOI.
So every import is written unverified, and `make check-docs` counts the ones that still are.

To verify an entry, open the copied file and read the document's own first page: title,
authors, journal, volume, pages. Then check the DOI and any arXiv ID against that. Fix what is
wrong, fill in `role` and `notes` in `papers/sources.yaml`, set `verified: true`, and delete
the UNVERIFIED marker above the entry in `papers/refs.bib`. If it does not match, say which of
the failure modes it is, by name, rather than reporting "not found".

Two things the importer will not do for you: it never guesses an identifier it was not given,
and it never fills in `primaryClass` for an arXiv entry. Where the catalogue lacks it, the
entry says so in a comment.

## When the library is not enough

Order of attempts for a work the project needs:

1. `papers/`: already here?
2. `papers/_drop/`: has the PI supplied it?
3. **arXiv source**: `make fetch-source ID=<id>`, if it is on arXiv (`reference/corpus.md`).
4. **The local libraries**, this file. The usual route for anything older than arXiv, and for
   books.
5. Ask the PI, and record what was needed and why it could not be found.

## Known limits

- Calibre custom columns are not read, and `show` says so.
- Zotero attachments stored relative to a base directory cannot be resolved from the database.
- Group libraries are read, and the item records which library it came from.
- BibTeX is built from catalogue fields and covers the common entry types. Anything else
  becomes `@misc`. Unicode is left as UTF-8, so use biber or a modern BibTeX setup.
- The tools are tested against synthetic databases that follow the real table layouts, not
  against every Zotero or Calibre version. **On a real library, run `import --dry-run` first**
  and read what it says.
