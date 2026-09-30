# Local reference libraries — search procedure

The PI may have a Zotero and/or Calibre library on this machine. **Read-only, and searched
with a targeted query — never listed, never browsed.**

    scripts/py scripts/library.py status
    scripts/py scripts/library.py search --author SURNAME [--title WORDS] [--limit N]
    scripts/py scripts/library.py search --title "words in the title"
    scripts/py scripts/library.py search --doi 10.1103/...
    scripts/py scripts/library.py attachments --item ITEMID          # Zotero

## Why there is no browse mode

These libraries hold **thousands of items**. A session that starts enumerating one has spent
its context before doing any work, and the enumeration answers nothing: the PI's library is
not this project's bibliography — `papers/sources.yaml` is. The tool therefore *requires* a
query and refuses to run without one. That refusal is the mechanism; treat it as the rule.

Corollaries:

- Search for a **specific work you already know you need**, by author surname, title words or
  DOI. Do not search for a topic and read whatever comes back.
- If the first query misses, try a name-order or diacritic variant, or title keywords — then
  stop. Two or three targeted queries, never a sweep.
- If neither library exists on this machine, say so plainly and move on. **Do not search the
  disk for one.** `status` checks the usual locations and stops; so should you.

## Never write to a library

The tool opens the live database through a read-only URI. If the application holds it locked
(Zotero running, mid-transaction) it copies the database to a scratch file, queries the copy,
and says which applied. Nothing else is acceptable:

- never open a library database read-write, for any reason;
- never edit, move, rename or delete a file inside the library's own folders;
- to read an attachment, **copy it out** and read the copy.

A library is the PI's long-term store, shared with other projects and other machines. A
project that corrupts it has destroyed something it does not own.

## Confirming a match — never trust the catalogue entry alone

Copy the attachment out and read the **document's own** first page — title, authors, journal,
volume, page range — against the catalogue entry before treating it as the cited work. Three
distinct failure modes, all real:

| What happened | How it looks | How to tell |
|---|---|---|
| **Mislabelled entry** | catalogue title/author/year right, attached file is a different paper or version | the document's own first page disagrees with the entry |
| **Wrong-file attachment** | item correctly catalogued, attachment is not the paper | `contentType` is not `application/pdf`, or the file has none of the paper's running text |
| **Snapshot, not the paper** | a saved web page of the abstract instead of the PDF | `linkMode` marks a snapshot; content is nav chrome and an abstract with a "Download PDF" link |

If one of these is what is there, **say which one by name.** Do not report "not found" — it
*is* in the library, just not usable as found — and never treat a snapshot's abstract as
though it were the paper.

## Where a found paper goes

The library is not this project's store. Copy the file into `papers/` (or
`papers/background/`), register it in `papers/sources.yaml` with its role, and record where
it came from:

    provenance: PI Zotero library, item key <key>
    provenance: PI Calibre library, book id <id>

If the work is also on arXiv, prefer the **source** (`reference/corpus.md`): `.tex` beats a
PDF for equations, and the tarball carries the figures and sometimes the data. A library PDF
is the right answer for a pre-arXiv paper or a book, and often the only one.

## Order of attempts

1. `papers/` — already fetched for this project?
2. `papers/_drop/` — has the PI supplied it by hand?
3. **arXiv source** (`make fetch-source ID=…`) — if it is on arXiv.
4. **Local libraries** — this file. The best route for pre-1991 papers, books and
   journal-only works.
5. Ask the PI. Record what was needed and why it could not be found, rather than silently
   dropping the reference or substituting a secondary source's restatement of it.
