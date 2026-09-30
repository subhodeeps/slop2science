#!/usr/bin/env python3
"""Query the PI's local reference libraries (Zotero, Calibre). Read-only, query-required.

    scripts/py scripts/library.py status [--fast]
    scripts/py scripts/library.py search --author SURNAME [--title WORDS] [--limit N]
    scripts/py scripts/library.py search --title "words in title"
    scripts/py scripts/library.py search --doi 10.1103/...
    scripts/py scripts/library.py attachments --item ITEMID      (Zotero)

**These libraries hold thousands of items. Search them; never browse them.** A query is
required and there is no "list everything" mode, deliberately: a session that starts
enumerating a ten-thousand-item library has spent its context before doing any work, and the
enumeration is not useful anyway — the PI's library is not this project's bibliography.
`papers/sources.yaml` is.

**Never writes to a library.** Each query opens the live database through a read-only URI
(`file:...?mode=ro&immutable=0`). If the application holds it locked — Zotero running, mid
transaction — the database is copied to a scratch file and the copy is queried, and the
output says which applied. The library's own files are never edited, moved or renamed; to
read an attachment, copy it out.

Paths: ZOTERO_DIR (default ~/Zotero), CALIBRE_DIR (default: a short list of common
locations; if none has a database, report absent and stop — do not search the disk).

Uses only the standard library, so it works wherever Python does, with no sqlite3 CLI.
"""
import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = Path(os.environ.get("RESEARCH_RECORDS_DIR")
               or Path.home() / ".claude-research-records")
CACHE = RECORDS / "library_status.json"

CALIBRE_CANDIDATES = ["Calibre Library", "Documents/Calibre Library",
                      "Books/Calibre Library", "Calibre", "Books"]


def zotero_db():
    path = Path(os.environ.get("ZOTERO_DIR") or Path.home() / "Zotero") / "zotero.sqlite"
    return path if path.is_file() else None


def calibre_db():
    explicit = os.environ.get("CALIBRE_DIR")
    if explicit:
        path = Path(explicit) / "metadata.db"
        return path if path.is_file() else None
    for candidate in CALIBRE_CANDIDATES:
        path = Path.home() / candidate / "metadata.db"
        if path.is_file():
            return path
    return None


class ReadOnly:
    """Read-only connection to a live database, falling back to a scratch copy if locked."""

    def __init__(self, path):
        self.path = Path(path)
        self.copied = False
        self._tmp = None
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(f"file:{self.path}?mode=ro", uri=True, timeout=2.0)
            self.conn.execute("SELECT 1").fetchone()
            return self
        except sqlite3.Error:
            if self.conn:
                self.conn.close()
            handle, tmp = tempfile.mkstemp(prefix="libread.", suffix=".sqlite")
            os.close(handle)
            self._tmp = Path(tmp)
            shutil.copy2(self.path, self._tmp)
            self.conn = sqlite3.connect(f"file:{self._tmp}?mode=ro", uri=True)
            self.copied = True
            return self

    def __exit__(self, *exc):
        if self.conn:
            self.conn.close()
        if self._tmp and self._tmp.exists():
            self._tmp.unlink(missing_ok=True)
        return False

    def rows(self, sql, params=()):
        try:
            return self.conn.execute(sql, params).fetchall()
        except sqlite3.Error as exc:
            print(f"  query failed ({exc}) — schema may differ in this version", file=sys.stderr)
            return []


def count(path, table):
    with ReadOnly(path) as db:
        rows = db.rows(f"SELECT COUNT(*) FROM {table}")
        return (rows[0][0] if rows else None), db.copied


# --------------------------------------------------------------------------- status

def cmd_status(args):
    zot, cal = zotero_db(), calibre_db()
    if args.fast:
        cache = {}
        try:
            cache = json.loads(CACHE.read_text())
        except Exception:
            pass
        changed = False
        for name, path, table in (("zotero", zot, "items"), ("calibre", cal, "books")):
            if not path:
                continue                              # silent: most machines have neither
            mtime = str(int(path.stat().st_mtime))
            entry = cache.get(name, {})
            if entry.get("mtime") == mtime and entry.get("count"):
                print(f"[libraries] {name}: {entry['count']} items, unchanged since last "
                      f"session — search it (scripts/library.py), never browse it")
                continue
            n, copied = count(path, table)
            if n is None:
                print(f"[libraries] {name}: present but locked and uncopyable")
                continue
            was = f" (was {entry.get('count')})" if entry.get("count") not in (None, str(n)) else ""
            cache[name] = {"mtime": mtime, "count": str(n)}
            changed = True
            print(f"[libraries] {name}: {n} items{was} — search it "
                  f"(scripts/library.py), never browse it"
                  + ("  [read from a scratch copy; the live db was locked]" if copied else ""))
        if changed:
            try:
                CACHE.parent.mkdir(parents=True, exist_ok=True)
                CACHE.write_text(json.dumps(cache))
            except Exception:
                pass
        return 0

    for name, path, tables, override in (
            ("Zotero", zot, [("items", "items"), ("attachments", "itemAttachments")], "ZOTERO_DIR"),
            ("Calibre", cal, [("books", "books")], "CALIBRE_DIR")):
        print(f"{name}:")
        if not path:
            print(f"  db:   NOT FOUND (override: {override}; checked the usual locations and "
                  f"searched no further)")
            continue
        print(f"  db:   {path}")
        for label, table in tables:
            n, copied = count(path, table)
            print(f"  {label:<12} {n if n is not None else 'unreadable'}"
                  + ("   [live db locked; queried a scratch copy]" if copied else ""))
    print("\nThousands of items. Use a targeted query; there is no browse mode, on purpose.")
    return 0


# --------------------------------------------------------------------------- search

ZOTERO_FIELDS = ("title", "date", "publicationTitle", "DOI", "volume", "pages", "url")


def zotero_search(path, author, title, doi, limit):
    with ReadOnly(path) as db:
        if db.copied:
            print("  [live Zotero db was locked; queried a scratch copy]")
        ids, why = set(), []
        if author:
            rows = db.rows(
                "SELECT DISTINCT i.itemID FROM items i "
                "JOIN itemCreators ic ON ic.itemID = i.itemID "
                "JOIN creators c ON c.creatorID = ic.creatorID "
                "WHERE c.lastName LIKE ?", (f"%{author}%",))
            ids |= {r[0] for r in rows}
            why.append(f"author~{author}")
        if title or doi:
            needle, field = (title, "title") if title else (doi, "DOI")
            rows = db.rows(
                "SELECT DISTINCT id.itemID FROM itemData id "
                "JOIN itemDataValues v ON v.valueID = id.valueID "
                "JOIN fields f ON f.fieldID = id.fieldID "
                "WHERE f.fieldName = ? AND v.value LIKE ?", (field, f"%{needle}%"))
            matched = {r[0] for r in rows}
            ids = (ids & matched) if (author and ids) else (ids | matched)
            why.append(f"{field}~{needle}")

        if not ids:
            print(f"  Zotero: no match ({', '.join(why)})")
            return
        total = len(ids)
        print(f"  Zotero: {total} match(es) for {', '.join(why)}"
              + (f", showing {limit}" if total > limit else ""))
        for item_id in sorted(ids)[:limit]:
            data = {}
            for row in db.rows(
                    "SELECT f.fieldName, v.value FROM itemData id "
                    "JOIN itemDataValues v ON v.valueID = id.valueID "
                    "JOIN fields f ON f.fieldID = id.fieldID "
                    "WHERE id.itemID = ?", (item_id,)):
                if row[0] in ZOTERO_FIELDS:
                    data[row[0]] = row[1]
            creators = db.rows(
                "SELECT c.lastName FROM itemCreators ic "
                "JOIN creators c ON c.creatorID = ic.creatorID "
                "WHERE ic.itemID = ? ORDER BY ic.orderIndex", (item_id,))
            names = ", ".join(r[0] for r in creators[:4]) or "?"
            print(f"    [{item_id}] {names} ({str(data.get('date', '?'))[:4]}) "
                  f"{data.get('title', '?')}")
            if data.get("publicationTitle") or data.get("DOI"):
                print(f"           {data.get('publicationTitle', '')} "
                      f"{data.get('DOI', '')}".rstrip())
        if total > limit:
            print(f"    … {total - limit} more. Narrow the query rather than raising --limit.")
        print("    Attachment paths: scripts/library.py attachments --item <ID>")


def calibre_search(path, author, title, limit):
    with ReadOnly(path) as db:
        if db.copied:
            print("  [live Calibre db was locked; queried a scratch copy]")
        clauses, params = [], []
        if author:
            clauses.append("a.name LIKE ?")
            params.append(f"%{author}%")
        if title:
            clauses.append("b.title LIKE ?")
            params.append(f"%{title}%")
        rows = db.rows(
            "SELECT b.id, b.title, b.pubdate, a.name, b.path FROM books b "
            "LEFT JOIN books_authors_link bal ON bal.book = b.id "
            "LEFT JOIN authors a ON a.id = bal.author "
            f"WHERE {' AND '.join(clauses)} LIMIT ?", (*params, limit + 1))
        if not rows:
            print("  Calibre: no match")
            return
        print(f"  Calibre: {min(len(rows), limit)} match(es)"
              + (" (more exist; narrow the query)" if len(rows) > limit else ""))
        for book_id, book_title, pubdate, name, rel in rows[:limit]:
            print(f"    [{book_id}] {name or '?'} ({str(pubdate or '?')[:4]}) {book_title}")
            print(f"           dir: {rel}")


def cmd_search(args):
    if not (args.author or args.title or args.doi):
        print("A query is required: --author, --title or --doi.\n"
              "There is no browse mode. These libraries hold thousands of items, and "
              "enumerating one spends a session's context without answering anything.",
              file=sys.stderr)
        return 64
    zot, cal = zotero_db(), calibre_db()
    if not zot and not cal:
        print("Neither a Zotero nor a Calibre library was found on this machine "
              "(ZOTERO_DIR / CALIBRE_DIR). Say so and move on — do not search the disk.")
        return 0
    print(f"searching local libraries (read-only) — limit {args.limit} per library")
    if zot:
        zotero_search(zot, args.author, args.title, args.doi, args.limit)
    if cal:
        calibre_search(cal, args.author, args.title, args.limit)
    print("\nBefore treating any hit as the cited work: copy the attachment out and check the\n"
          "document's OWN first page against the catalogue entry. A catalogue entry can be\n"
          "mislabelled, its attachment can be a different paper, or it can be a web snapshot\n"
          "of an abstract rather than the paper "
          "(.claude/skills/literature-audit/reference/local_libraries.md).")
    return 0


def cmd_attachments(args):
    path = zotero_db()
    if not path:
        print("No Zotero library found (ZOTERO_DIR).", file=sys.stderr)
        return 66
    zdir = path.parent
    with ReadOnly(path) as db:
        rows = db.rows(
            "SELECT i2.key, ia.path, ia.contentType, ia.linkMode FROM itemAttachments ia "
            "JOIN items i2 ON i2.itemID = ia.itemID WHERE ia.parentItemID = ?", (args.item,))
        if not rows:
            print(f"  item {args.item}: no attachments")
            return 0
        for key, apath, ctype, linkmode in rows:
            print(f"  key={key}  type={ctype or '?'}  linkMode={linkmode}")
            if apath and str(apath).startswith("storage:"):
                filename = str(apath).split("storage:", 1)[1]
                print(f"    file: {zdir / 'storage' / key / filename}")
            elif apath:
                print(f"    path: {apath}")
            if ctype and ctype != "application/pdf":
                print(f"    NOTE: contentType is {ctype}, not application/pdf — this may be a "
                      f"web snapshot of an abstract, not the paper itself.")
    print("\n  Copy the file out to read it. Never open, edit or move a file inside the library.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="report which libraries exist, and their size")
    p_status.add_argument("--fast", action="store_true", help="one cached line per library")

    p_search = sub.add_parser("search", help="targeted search (a query is required)")
    p_search.add_argument("--author", help="surname, substring match")
    p_search.add_argument("--title", help="words in the title, substring match")
    p_search.add_argument("--doi", help="DOI, substring match")
    p_search.add_argument("--limit", type=int, default=15)

    p_att = sub.add_parser("attachments", help="attachment paths for one Zotero item")
    p_att.add_argument("--item", type=int, required=True)

    args = parser.parse_args()
    return {"status": cmd_status, "search": cmd_search, "attachments": cmd_attachments}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
