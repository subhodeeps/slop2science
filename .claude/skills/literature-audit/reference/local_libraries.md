# Local reference libraries — search, read, import

The PI can keep a Zotero library, a Calibre library, or both, on this machine. This file explains
how to use them without damage to them and without overload from them.

    scripts/py scripts/library.py status
    scripts/py scripts/library.py search --author SURNAME [--title WORDS] [--doi DOI]
    scripts/py scripts/library.py show   --zotero ID | --calibre ID      # all metadata, read-only
    scripts/py scripts/library.py bibtex --zotero ID | --calibre ID      # print an entry, write nothing
    scripts/py scripts/library.py import --zotero ID | --calibre ID --dry-run
    scripts/py scripts/library.py import --zotero ID | --calibre ID [--label L] [--role R]
                                         [--max-mb 25] [--no-file] [--formats pdf,epub]

## Search. Never browse.

These libraries hold thousands of items. `search` requires a query. There is no mode that lists
everything, on purpose. If you enumerate a library, you use the context of the session and learn
nothing. Search for a specific work that you know you need. If two or three targeted queries find
nothing, stop and ask. If neither library exists on this machine, say so and continue. Do not
search the disk for one.

Search shows real, live works only. It hides trashed items, attachments and notes. If you give
more than one criterion, an item must match all of them.

## Read-only, always

The tool opens the database through a read-only connection. The application can lock the
database (Zotero keeps it locked while it runs). In that case the tool copies the database, with
any `-wal` file, to a scratch location and reads the copy. The output says so. The tool only
reads and copies a library file. It never moves, renames or edits one. The library is the
long-term store of the PI. This project does not own it.

## Read one item: `show`

`show` prints everything that the library knows about the item:

- every field
- full creator names and roles
- identifiers, tags and collections
- attachments, with their type and size
- for Calibre: the publisher, series, languages, formats and description

It also says what it did **not** read, for example a table that an older schema lacks, or
Calibre custom columns. An empty result and a failed query are different things.

The tool deliberately does **not** read these items:

- Zotero notes and annotations
- Calibre ratings
- absolute paths on the machine of the PI

They are personal, and a repository gets shared.

## Import one item: `import`

An import is a decision. Therefore the unit is exactly one item that you name explicitly. Never
import "all matches". Always run `--dry-run` first. It prints each file that it would copy or
skip, with the reason. It prints the BibTeX entry that it would add. It writes nothing.

An import does these steps:

1. **It copies the file into `papers/imported/<label>/`** if the file is small. The default limit
   is 25 MB for each file and three files for each item. The tool skips a larger file and records
   the reason. The tool records the metadata in all cases. Use `--no-file` for metadata only.
2. **It writes `papers/imported/<label>/metadata.json`.** This is the full record, with a sha256
   and a size for each copied file.
3. **It appends an entry to `papers/sources.yaml`.** The entry has the identifiers, the
   provenance (which library, which item key, which date) and `verified: false`.
4. **It appends a BibTeX entry to `papers/refs.bib`**, marked UNVERIFIED.

All of these steps happen, or none of them happens. If any step fails, the tool removes the
directory and restores both files to their exact earlier state.

The tool refuses, with a message, in these cases:

- The item is in the trash.
- The item is an attachment or a note.
- The item has no title.
- The label, the BibTeX key or the DOI is already in the bibliography.

Git ignores `papers/imported/`, as it ignores the PDFs. The PI decides whether to commit the
paper of another person. The project **does** commit the registry entry and `refs.bib`. They
carry the identifiers and the provenance.

### What the tool skips, and why

| File | Why the tool does not copy it |
|---|---|
| a saved web page (`text/html`) | It is a snapshot of an abstract page. It is not the paper. |
| catalogued as a PDF but does not start with `%PDF` | It is an attachment with the wrong label. |
| over the size limit | It is too large for a repository. The path is in the metadata. |
| missing on this machine | The catalogue knows it. The disk does not. |
| stored relative to the base directory of Zotero | That is a preference outside the database. |

The tool recognises a Zotero snapshot by its content type. It does not recognise it by
`linkMode`. A PDF that someone downloaded from a URL has the same `linkMode` as a saved web page.

## `verified: false` is the point

The import copies what the catalogue says. **A catalogue can be wrong.** An entry can have the
wrong label. An attachment can be a different paper or a different version. A DOI can be wrong
or missing. Therefore you write each import as unverified. `make check-docs` counts the entries
that are still unverified.

To verify an entry, open the copied file and read the first page of the document. Check the
title, the authors, the journal, the volume and the pages. Then check the DOI and each arXiv ID
against that page. Fix what is wrong. Fill in `role` and `notes` in `papers/sources.yaml`. Set
`verified: true`. Delete the UNVERIFIED marker above the entry in `papers/refs.bib`. If the entry
does not match, name the failure mode. Do not report "not found".

The importer does not do two things for you. It never guesses an identifier that you did not give
it. It never fills in `primaryClass` for an arXiv entry. If the catalogue lacks it, the entry
says so in a comment.

## When the library is not enough

Use this order of attempts for a work that the project needs:

1. `papers/`: is the work already here?
2. `papers/_drop/`: did the PI supply it?
3. **The arXiv source**: `make fetch-source ID=<id>`, if the work is on arXiv
   (`reference/corpus.md`).
4. **The local libraries**, which this file describes. This is the usual route for anything older
   than arXiv, and for books.
5. Ask the PI. Record what the project needed and why you did not find it.

## Known limits

- The tool does not read Calibre custom columns. `show` says so.
- The database does not give the path of a Zotero attachment that the library stores relative
  to a base directory. The tool cannot resolve it.
- The tool reads group libraries. The item records the library that it came from.
- The tool builds BibTeX from catalogue fields. It covers the common entry types. It writes
  anything else as `@misc`. It leaves Unicode as UTF-8, so use biber or a modern BibTeX setup.
- The tests use synthetic databases that follow the real table layouts. They do not use every
  Zotero or Calibre version. **On a real library, run `import --dry-run` first** and read what it
  says.
