#!/usr/bin/env python3
"""Read full bibliographic metadata from the PI's Zotero / Calibre libraries, build BibTeX,
and import one item (small file + metadata + bibliography entries) into this project.

Used by scripts/library.py (`show`, `bibtex`, `import`). Standard library only.

Guarantees, each pinned by scripts/test_library.py:

  * READ-ONLY. The live database is opened through a read-only URI; if the application holds
    it locked, the database (and any -wal/-shm) is copied to scratch and the copy is read.
    Library files are opened for reading and COPIED, never moved, renamed or edited.
  * ONE ITEM, EXPLICITLY. Nothing here imports "all matches". Reading a library is cheap and
    importing is a decision, so the unit is a single named item.
  * SMALL FILES ONLY. A file over --max-mb is not copied; the metadata is still recorded and
    the reason is written down, so the decision is visible rather than silent.
  * NOTHING PERSONAL TRAVELS. Zotero notes and annotations, Calibre ratings, and absolute
    paths on the PI's machine are deliberately not recorded: a repository gets shared and the
    library is the PI's own.
  * NOTHING IS TRUSTED. A catalogue entry can be mislabelled; its identifiers are not checked
    against the document, so every import is written `verified: false`.
"""
import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import registry

DEFAULT_MAX_MB = 25
MAX_FILES_PER_ITEM = 3
EXCLUDED_BY_DESIGN = ["Zotero notes", "Zotero annotations", "Calibre ratings",
                      "absolute paths on the PI's machine"]


class LibraryError(Exception):
    """A refusal the caller should show to the PI, not a bug."""


# --------------------------------------------------------------------------- database access

class ReadOnly:
    """Read-only connection to a live database; falls back to a scratch copy if it is locked."""

    def __init__(self, path):
        self.path = Path(path)
        self.copied = False
        self._tmpdir = None
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(f"file:{self.path}?mode=ro", uri=True, timeout=2.0)
            self.conn.execute("SELECT 1").fetchone()
            self.conn.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
            return self
        except sqlite3.Error:
            if self.conn:
                self.conn.close()
            self._tmpdir = Path(tempfile.mkdtemp(prefix="libread."))
            for suffix in ("", "-wal", "-shm"):          # a WAL holds recent, uncheckpointed rows
                source = Path(str(self.path) + suffix)
                if source.exists():
                    shutil.copy2(source, self._tmpdir / (self.path.name + suffix))
            self.conn = sqlite3.connect(f"file:{self._tmpdir / self.path.name}?mode=ro", uri=True)
            self.copied = True
            return self

    def __exit__(self, *exc):
        if self.conn:
            self.conn.close()
        if self._tmpdir and self._tmpdir.exists():
            shutil.rmtree(self._tmpdir, ignore_errors=True)
        return False

    def rows(self, sql, params=()):
        try:
            return self.conn.execute(sql, params).fetchall()
        except sqlite3.Error:
            return []

    def try_rows(self, sql, params, gaps, what):
        """Like rows(), but a failed query is RECORDED as a gap rather than read as 'empty'."""
        try:
            return self.conn.execute(sql, params).fetchall()
        except sqlite3.Error as exc:
            gaps.append(f"{what}: {exc}")
            return []

    def dicts(self, sql, params=(), gaps=None, what="query"):
        try:
            cur = self.conn.execute(sql, params)
        except sqlite3.Error as exc:
            if gaps is not None:
                gaps.append(f"{what}: {exc}")
            return []
        names = [d[0] for d in cur.description]
        return [dict(zip(names, row)) for row in cur.fetchall()]


def _iso(ts):
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="seconds")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --------------------------------------------------------------------------- Zotero

def read_zotero(db, zdir, ref):
    """Everything bibliographic about one regular Zotero item, as a plain dict."""
    gaps = []
    ref = str(ref).strip()
    where, param = ("i.itemID = ?", int(ref)) if ref.isdigit() else ("i.key = ?", ref)
    base = db.dicts(
        "SELECT i.itemID, i.key, i.libraryID, i.dateAdded, i.dateModified, t.typeName AS itemType "
        f"FROM items i JOIN itemTypes t ON t.itemTypeID = i.itemTypeID WHERE {where}",
        (param,), gaps, "items")
    if not base:
        raise LibraryError(f"no Zotero item {ref!r}")
    base = base[0]
    item_id = base["itemID"]

    if db.rows("SELECT 1 FROM deletedItems WHERE itemID = ?", (item_id,)):
        raise LibraryError(f"item {item_id} is in the Zotero trash; restore it there first")
    child = db.rows("SELECT parentItemID FROM itemAttachments WHERE itemID = ?", (item_id,))
    if child:
        raise LibraryError(f"item {item_id} is an attachment, not a work; "
                           f"use its parent, item {child[0][0]}")
    if db.rows("SELECT 1 FROM itemNotes WHERE itemID = ?", (item_id,)):
        raise LibraryError(f"item {item_id} is a note, not a work")

    fields = {}
    for name, value in db.try_rows(
            "SELECT f.fieldName, v.value FROM itemData d "
            "JOIN itemDataValues v ON v.valueID = d.valueID "
            "JOIN fields f ON f.fieldID = d.fieldID WHERE d.itemID = ?", (item_id,), gaps, "fields"):
        fields[name] = value

    creators = [
        {"type": r["creatorType"], "first": r["firstName"] or "", "last": r["lastName"] or "",
         "single_field": bool(r["fieldMode"])}
        for r in db.dicts(
            "SELECT c.firstName, c.lastName, c.fieldMode, ct.creatorType FROM itemCreators ic "
            "JOIN creators c ON c.creatorID = ic.creatorID "
            "JOIN creatorTypes ct ON ct.creatorTypeID = ic.creatorTypeID "
            "WHERE ic.itemID = ? ORDER BY ic.orderIndex", (item_id,), gaps, "creators")]

    tags = [r[0] for r in db.try_rows(
        "SELECT t.name FROM itemTags it JOIN tags t ON t.tagID = it.tagID WHERE it.itemID = ?",
        (item_id,), gaps, "tags")]

    all_cols = {r[0]: (r[1], r[2]) for r in db.try_rows(
        "SELECT collectionID, collectionName, parentCollectionID FROM collections", (), gaps,
        "collections")}

    def collection_path(cid):
        parts, seen = [], set()
        while cid in all_cols and cid not in seen:
            seen.add(cid)
            name, parent = all_cols[cid]
            parts.append(name)
            cid = parent
        return " / ".join(reversed(parts))

    collections = [collection_path(r[0]) for r in db.try_rows(
        "SELECT collectionID FROM collectionItems WHERE itemID = ?", (item_id,), gaps,
        "collection membership")]

    attachments = []
    for r in db.dicts(
            "SELECT i2.itemID AS attachmentID, i2.key, ia.path, ia.contentType, ia.linkMode "
            "FROM itemAttachments ia JOIN items i2 ON i2.itemID = ia.itemID "
            "WHERE ia.parentItemID = ? AND ia.itemID NOT IN (SELECT itemID FROM deletedItems)",
            (item_id,), gaps, "attachments"):
        raw = r["path"] or ""
        if raw.startswith("storage:"):
            kind, filename = "storage", raw.split("storage:", 1)[1]
            real = zdir / "storage" / r["key"] / filename
        elif raw.startswith("attachments:"):
            kind, filename, real = "relative-to-base-dir", raw.split("attachments:", 1)[1], None
        elif raw:
            kind, filename, real = "linked", os.path.basename(raw), Path(raw)
        else:
            kind, filename, real = "none", "", None
        info = {"key": r["key"], "content_type": r["contentType"], "link_mode": r["linkMode"],
                "path_kind": kind, "filename": filename,
                "exists": bool(real and real.is_file()),
                "size_bytes": real.stat().st_size if real and real.is_file() else None}
        info["_real_path"] = str(real) if real else None      # stripped before anything is recorded
        attachments.append(info)

    lib = db.dicts("SELECT type FROM libraries WHERE libraryID = ?", (base["libraryID"],))
    group = db.rows("SELECT name FROM groups WHERE libraryID = ?", (base["libraryID"],))

    return {
        "source": {"app": "zotero", "item_id": item_id, "item_key": base["key"],
                   "library_id": base["libraryID"],
                   "library_type": lib[0]["type"] if lib else None,
                   "group_name": group[0][0] if group else None,
                   "item_type": base["itemType"],
                   "date_added": base["dateAdded"], "date_modified": base["dateModified"]},
        "fields": fields, "creators": creators, "tags": tags, "collections": collections,
        "attachments": attachments, "schema_gaps": gaps,
    }


# --------------------------------------------------------------------------- Calibre

def read_calibre(db, cdir, book_id):
    gaps = []
    books = db.dicts("SELECT * FROM books WHERE id = ?", (int(book_id),), gaps, "books")
    if not books:
        raise LibraryError(f"no Calibre book {book_id!r}")
    row = books[0]

    authors = [r[0] for r in db.try_rows(
        "SELECT a.name FROM books_authors_link l JOIN authors a ON a.id = l.author "
        "WHERE l.book = ? ORDER BY l.id", (row["id"],), gaps, "authors")]

    def linked(sql, what):
        return [r[0] for r in db.try_rows(sql, (row["id"],), gaps, what)]

    identifiers = {r[0]: r[1] for r in db.try_rows(
        "SELECT type, val FROM identifiers WHERE book = ?", (row["id"],), gaps, "identifiers")}
    comments = db.rows("SELECT text FROM comments WHERE book = ?", (row["id"],))

    formats = []
    for r in db.dicts("SELECT format, uncompressed_size, name FROM data WHERE book = ?",
                      (row["id"],), gaps, "formats"):
        path = cdir / row["path"] / f"{r['name']}.{r['format'].lower()}"
        formats.append({"format": r["format"].upper(), "name": r["name"],
                        "declared_size": r["uncompressed_size"], "exists": path.is_file(),
                        "size_bytes": path.stat().st_size if path.is_file() else None,
                        "_real_path": str(path)})

    custom = db.rows("SELECT COUNT(*) FROM custom_columns")
    if custom and custom[0][0]:
        gaps.append(f"{custom[0][0]} Calibre custom column(s) present and not read")

    return {
        "source": {"app": "calibre", "book_id": row["id"], "uuid": row.get("uuid"),
                   "library_path": row.get("path")},
        "fields": {k: v for k, v in row.items() if k not in ("path",)},
        "authors": authors,
        "publishers": linked("SELECT p.name FROM books_publishers_link l "
                             "JOIN publishers p ON p.id = l.publisher WHERE l.book = ?",
                             "publishers"),
        "tags": linked("SELECT t.name FROM books_tags_link l JOIN tags t ON t.id = l.tag "
                       "WHERE l.book = ?", "tags"),
        "series": linked("SELECT s.name FROM books_series_link l JOIN series s ON s.id = l.series "
                         "WHERE l.book = ?", "series"),
        "languages": linked("SELECT g.lang_code FROM books_languages_link l "
                            "JOIN languages g ON g.id = l.lang_code WHERE l.book = ?", "languages"),
        "identifiers": identifiers,
        "comments": comments[0][0] if comments else None,
        "formats": formats, "schema_gaps": gaps,
    }


# --------------------------------------------------------------------------- identifiers

_ARXIV_NEW = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(v\d+)?(?![\d])")
_ARXIV_OLD = re.compile(r"\b([a-z-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?\b")


def find_arxiv(*texts):
    """An arXiv identifier mentioned in any text (an `extra` line, a URL, an `arXiv.<id>` DOI)."""
    for text in texts:
        if not text:
            continue
        text = str(text)
        for pattern in (r"arxiv[.:/ ]+(?:abs/|pdf/)?(\S+)", r"arxiv\.org/(?:abs|pdf)/(\S+)"):
            m = re.search(pattern, text, re.I)
            if m:
                tail = m.group(1).rstrip(".,;)")
                tail = re.sub(r"\.pdf$", "", tail)
                n, o = _ARXIV_NEW.search(tail), _ARXIV_OLD.search(tail)
                if n:
                    return n.group(1) + (n.group(2) or ""), None
                if o:
                    return o.group(1) + (o.group(2) or ""), o.group(1).split("/")[0]
    return None, None


def parse_extra(extra):
    """Zotero's free-text `extra` field: `Key: value` lines (Citation Key, arXiv, PMID, ...)."""
    out = {}
    for line in (extra or "").splitlines():
        m = re.match(r"^\s*([A-Za-z][A-Za-z .-]{1,30}):\s*(.+?)\s*$", line)
        if m:
            out.setdefault(m.group(1).strip().lower(), m.group(2))
    return out


def clean_doi(doi):
    doi = (doi or "").strip()
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi, flags=re.I) or None


# --------------------------------------------------------------------------- normalise -> BibTeX

ZOTERO_BIBTYPE = {
    "journalArticle": "article", "magazineArticle": "article", "newspaperArticle": "article",
    "book": "book", "bookSection": "incollection", "conferencePaper": "inproceedings",
    "thesis": "phdthesis", "report": "techreport", "preprint": "misc",
}


def _year(text):
    m = re.search(r"(1[5-9]\d\d|20\d\d)", str(text or ""))
    return m.group(1) if m else None


def normalise(record):
    """Reduce either library's record to the neutral fields a BibTeX entry is made from."""
    src = record["source"]
    if src["app"] == "zotero":
        f = record["fields"]
        extra = parse_extra(f.get("extra"))
        itype = src["item_type"]
        ref = {"type": ZOTERO_BIBTYPE.get(itype, "misc"), "title": f.get("title"),
               "year": _year(f.get("date")), "volume": f.get("volume"), "number": f.get("issue"),
               "pages": f.get("pages"), "publisher": f.get("publisher"),
               "address": f.get("place"), "edition": f.get("edition"), "series": f.get("series"),
               "isbn": f.get("ISBN"), "issn": f.get("ISSN"), "doi": clean_doi(f.get("DOI")),
               "url": f.get("url"), "cite_key": extra.get("citation key")}
        ref["container"] = (f.get("publicationTitle") if itype in ("journalArticle", "magazineArticle",
                            "newspaperArticle") else f.get("bookTitle") if itype == "bookSection"
                            else (f.get("proceedingsTitle") or f.get("conferenceName"))
                            if itype == "conferencePaper" else None)
        ref["school"] = f.get("university")
        ref["institution"] = f.get("institution")
        ref["report_number"] = f.get("reportNumber")
        if itype == "thesis" and "master" in (f.get("thesisType") or "").lower():
            ref["type"] = "mastersthesis"
        ref["authors"] = [c for c in record["creators"] if c["type"] == "author"]
        ref["editors"] = [c for c in record["creators"] if c["type"] == "editor"]
        archive_id = (f"arXiv:{f['archiveID']}" if f.get("archiveID")
                      and (f.get("repository") or "").lower().startswith("arxiv") else None)
        arxiv, pclass = find_arxiv(extra.get("arxiv"), archive_id, f.get("url"), f.get("DOI"))
    else:
        f, ids = record["fields"], record["identifiers"]
        ref = {"type": "book", "title": f.get("title"), "year": _year(f.get("pubdate")),
               "publisher": (record["publishers"] or [None])[0],
               "isbn": ids.get("isbn") or f.get("isbn") or None, "doi": clean_doi(ids.get("doi")),
               "series": (record["series"] or [None])[0], "cite_key": None,
               "authors": [], "editors": [], "container": None}
        for name in record["authors"]:
            ref["authors"].append({"type": "author", "first": "", "last": name, "single_field": True})
        arxiv, pclass = find_arxiv(ids.get("arxiv"), ids.get("url"), ids.get("doi"))
    ref["eprint"], ref["primary_class"] = arxiv, pclass
    return ref


def _fold(text):
    return unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()


def cite_key(ref, taken):
    if ref.get("cite_key") and re.fullmatch(r"[A-Za-z0-9:_.+-]+", ref["cite_key"]):
        base = ref["cite_key"]
    else:
        first = (ref["authors"] or ref["editors"] or [{"last": "Anon"}])[0]["last"]
        last = re.sub(r"[^A-Za-z0-9]", "", _fold(first.split(",")[0].split()[-1] if first else "Anon"))
        base = (last or "Anon") + (ref.get("year") or "")
    key, n = base, 0
    while key in taken:
        key = base + "abcdefghijklmnopqrstuvwxyz"[n % 26] * (n // 26 + 1)
        n += 1
    return key


def _esc(value):
    """Escape & % # that are not already escaped. `_` and `$` are left alone: titles carry math."""
    value = re.sub(r"(?<!\\)([&%#])", r"\\\1", str(value))
    if value.count("{") != value.count("}"):
        value = value.replace("{", "").replace("}", "")
    return " ".join(value.split())


def _names(people):
    out = []
    for p in people:
        if p["single_field"]:
            out.append("{" + _esc(p["last"]) + "}")
        elif p["first"]:
            out.append(f"{_esc(p['last'])}, {_esc(p['first'])}")
        else:
            out.append(_esc(p["last"]))
    return " and ".join(out)


def to_bibtex(ref, key):
    """A BibTeX entry. Identifiers are copied as catalogued, never completed or guessed."""
    pages = re.sub(r"(?<=\d)\s*[-–—]+\s*(?=\d)", "--", ref.get("pages") or "") or None
    rows = [
        ("author", _names(ref["authors"]) if ref["authors"] else None),
        ("editor", _names(ref["editors"]) if ref["editors"] else None),
        ("title", ref.get("title")),
    ]
    container = {"article": "journal", "incollection": "booktitle",
                 "inproceedings": "booktitle"}.get(ref["type"])
    if container:
        rows.append((container, ref.get("container")))
    rows += [("school", ref.get("school") if ref["type"] in ("phdthesis", "mastersthesis") else None),
             ("institution", ref.get("institution") if ref["type"] == "techreport" else None),
             ("year", ref.get("year")), ("volume", ref.get("volume")),
             ("number", ref.get("number") or ref.get("report_number")), ("pages", pages),
             ("publisher", ref.get("publisher")), ("address", ref.get("address")),
             ("edition", ref.get("edition")), ("series", ref.get("series")),
             ("isbn", ref.get("isbn")), ("issn", ref.get("issn")), ("doi", ref.get("doi"))]
    if ref.get("eprint"):
        rows += [("eprint", ref["eprint"]), ("archivePrefix", "arXiv"),
                 ("primaryClass", ref.get("primary_class"))]
    rows.append(("url", ref.get("url")))
    body = []
    for name, value in rows:
        if value in (None, ""):
            continue
        text = str(value) if name in ("url", "doi", "eprint", "archivePrefix", "primaryClass") \
            else _esc(value)
        body.append(f"  {name:<13} = {{{text}}},")
    notes = []
    if ref.get("eprint") and not ref.get("primary_class"):
        notes.append("% primaryClass not in the catalogue: verify on arxiv.org before adding it")
    return "\n".join(notes + [f"@{ref['type']}{{{key},", *body, "}"])


# --------------------------------------------------------------------------- import

def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_name(name):
    stem, dot, ext = name.rpartition(".")
    stem, ext = (stem, ext) if dot else (name, "")
    clean = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip("._") or "file"
    return clean[:80] + (("." + re.sub(r"[^A-Za-z0-9]", "", ext)[:8].lower()) if ext else "")


def plan_files(record, max_mb, no_file=False, formats=("pdf", "epub")):
    """Decide, per candidate file, whether it will be copied -- and say why not if not."""
    limit = int(max_mb * 1024 * 1024)
    plan = []
    if record["source"]["app"] == "zotero":
        for a in record["attachments"]:
            entry = {"name": a["filename"] or "(no file)", "size_bytes": a["size_bytes"],
                     "real": a["_real_path"], "action": "copy", "reason": None,
                     "content_type": a["content_type"]}
            ctype = (a["content_type"] or "").lower()
            if no_file:
                entry.update(action="skip", reason="--no-file")
            elif a["path_kind"] == "none":
                entry.update(action="skip", reason="attachment has no file path")
            elif a["path_kind"] == "relative-to-base-dir":
                entry.update(action="skip", reason="stored relative to Zotero's base attachment "
                             "directory, which is a preference outside the database")
            elif ctype in ("text/html", "application/xhtml+xml"):
                entry.update(action="skip", reason="a saved web page (snapshot), not the paper")
            elif ctype != "application/pdf":
                entry.update(action="skip", reason=f"content type {a['content_type'] or 'unknown'}, "
                             "not a PDF")
            elif not a["exists"]:
                entry.update(action="skip", reason="file is missing on this machine")
            elif a["size_bytes"] > limit:
                entry.update(action="skip", reason=f"{a['size_bytes'] / 1048576:.1f} MB is over "
                             f"the {max_mb:g} MB limit")
            plan.append(entry)
    else:
        preferred = [f.lower() for f in formats]
        chosen = False
        for fmt in sorted(record["formats"], key=lambda x: preferred.index(x["format"].lower())
                          if x["format"].lower() in preferred else 99):
            entry = {"name": f"{fmt['name']}.{fmt['format'].lower()}", "size_bytes": fmt["size_bytes"],
                     "real": fmt["_real_path"], "action": "copy", "reason": None,
                     "content_type": fmt["format"]}
            if no_file:
                entry.update(action="skip", reason="--no-file")
            elif fmt["format"].lower() not in preferred:
                entry.update(action="skip", reason=f"format {fmt['format']} not requested "
                             f"(--formats {','.join(preferred)})")
            elif not fmt["exists"]:
                entry.update(action="skip", reason="file is missing on this machine")
            elif fmt["size_bytes"] > limit:
                entry.update(action="skip", reason=f"{fmt['size_bytes'] / 1048576:.1f} MB is over "
                             f"the {max_mb:g} MB limit")
            elif chosen:
                entry.update(action="skip", reason="a preferred format was already chosen")
            else:
                chosen = True
            plan.append(entry)
    copies = 0
    for entry in plan:                                  # cap how much one item can add
        if entry["action"] == "copy":
            copies += 1
            if copies > MAX_FILES_PER_ITEM:
                entry.update(action="skip", reason=f"more than {MAX_FILES_PER_ITEM} files per item")
    return plan


def _looks_like(entry):
    """Cheap content check: is a file that claims to be a PDF actually a PDF?"""
    if (entry.get("content_type") or "").lower() not in ("application/pdf", "pdf"):
        return True
    with open(entry["real"], "rb") as fh:
        return fh.read(5).startswith(b"%PDF")


def build_import(record, *, label=None, role=None, max_mb=DEFAULT_MAX_MB, no_file=False,
                 formats=("pdf", "epub"), papers_dir=None, registry_path=None, refs_path=None):
    """Everything an import would do, as data. Raises LibraryError for a refusal. Writes nothing."""
    papers_dir = Path(papers_dir or registry.ROOT / "papers")
    registry_path = Path(registry_path or papers_dir / "sources.yaml")
    refs_path = Path(refs_path or papers_dir / "refs.bib")

    ref = normalise(record)
    if not ref.get("title"):
        raise LibraryError("the catalogue entry has no title; refusing to import something "
                           "that cannot be identified")
    key = cite_key(ref, registry.existing_bib_keys(refs_path))
    label = label or key
    if not registry.valid_label(label):
        raise LibraryError(f"invalid label {label!r}: use letters, digits, . _ - (max 64)")
    if label in registry.existing_labels(registry_path):
        raise LibraryError(f"label {label!r} is already in papers/sources.yaml; pass --label")
    if (papers_dir / "imported" / label).exists():
        raise LibraryError(f"papers/imported/{label}/ already exists; pass --label")
    if ref.get("doi") and ref["doi"].lower() in registry.existing_dois(registry_path, refs_path):
        raise LibraryError(f"DOI {ref['doi']} is already in the bibliography; not importing a "
                           "second copy of the same work")

    files = plan_files(record, max_mb, no_file, formats)
    for entry in files:
        if entry["action"] == "copy" and not _looks_like(entry):
            entry.update(action="skip", reason="catalogued as a PDF but the file is not one "
                         "(a mislabelled attachment)")
    return {"record": record, "ref": ref, "key": key, "label": label, "role": role,
            "files": files, "bibtex": to_bibtex(ref, key), "papers_dir": papers_dir,
            "registry_path": registry_path, "refs_path": refs_path, "max_mb": max_mb}


def public_record(record):
    """The record as it may be written to disk: no machine paths, nothing excluded by design."""
    def clean(item):
        return {k: v for k, v in item.items() if not k.startswith("_")}
    out = json.loads(json.dumps(record))
    for group in ("attachments", "formats"):
        if group in out:
            out[group] = [clean(i) for i in out[group]]
    return out


def execute_import(plan, library_db_mtime=None):
    """Perform an import. Either everything is written, or nothing is."""
    papers_dir, label = plan["papers_dir"], plan["label"]
    dest = papers_dir / "imported" / label
    reg_path, refs_path = plan["registry_path"], plan["refs_path"]
    saved = {p: (p.read_text(encoding="utf-8") if p.exists() else None) for p in (reg_path, refs_path)}
    created_dir = False
    copied = []
    try:
        dest.mkdir(parents=True)
        created_dir = True
        for n, entry in enumerate(f for f in plan["files"] if f["action"] == "copy"):
            name = _safe_name(entry["name"])
            target = dest / (name if n == 0 else f"{n + 1}_{name}")
            shutil.copyfile(entry["real"], target)
            entry["copied_as"] = f"imported/{label}/{target.name}"
            entry["sha256"] = _sha256(target)
            entry["size_bytes"] = target.stat().st_size
            copied.append(entry)

        record = public_record(plan["record"])
        record["import"] = {
            "label": label, "bibtex_key": plan["key"], "imported": _now(),
            "max_mb": plan["max_mb"], "verified": False,
            "excluded_by_design": EXCLUDED_BY_DESIGN,
            "library_db_mtime": _iso(library_db_mtime) if library_db_mtime else None,
            "files": [{k: v for k, v in e.items() if k != "real"} for e in plan["files"]]}
        (dest / "metadata.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n",
                                            encoding="utf-8")

        ref, src = plan["ref"], plan["record"]["source"]
        where = (f"PI Zotero library, item key {src['item_key']} (itemID {src['item_id']})"
                 if src["app"] == "zotero" else f"PI Calibre library, book id {src['book_id']}")
        first = copied[0] if copied else None
        fields = [("doi", ref.get("doi")) if ref.get("doi") else None,
                  ("eprint", f"arXiv:{ref['eprint']}") if ref.get("eprint") else None,
                  ("isbn", ref.get("isbn")) if ref.get("isbn") else None,
                  ("title", ref.get("title")),
                  ("year", ref.get("year")) if ref.get("year") else None,
                  ("version", "FILL IN", "the exact version consulted"),
                  ("file", first["copied_as"] if first else None),
                  ("size_bytes", first["size_bytes"]) if first else None,
                  ("sha256", first["sha256"]) if first else None,
                  ("role", plan["role"] or "FILL IN", "primary | benchmark | method-reference | background"),
                  ("notes", "FILL IN", "what THIS project needs from it, specifically"),
                  ("provenance", f"{where}, imported {_now()[:10]}"),
                  ("metadata", f"imported/{label}/metadata.json (local, gitignored)"),
                  ("bibtex_key", plan["key"]),
                  ("verified", False, "true only after checking the identifiers and the file "
                                      "against the document's own first page")]
        registry.append_source(label, [f for f in fields if f], reg_path)
        registry.append_bib(plan["key"], plan["bibtex"],
                            f"imported from {where}, {_now()[:10]} -- UNVERIFIED: check against "
                            "the document itself", refs_path)
    except Exception:
        for path, text in saved.items():                 # restore exactly what was there
            if text is None:
                if path.exists():
                    path.unlink()
            else:
                path.write_text(text, encoding="utf-8")
        if created_dir:
            shutil.rmtree(dest, ignore_errors=True)
        raise
    return {"label": label, "key": plan["key"], "dest": dest, "copied": copied}
