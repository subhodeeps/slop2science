#!/usr/bin/env python3
"""Self-test for the local-library tools: scripts/library.py, library_meta.py, registry.py.

    scripts/py scripts/test_library.py        (also: make test-library, part of make check)

Built on synthetic Zotero and Calibre databases that follow those applications' table layouts.
That is a real limitation, said plainly: no real library exists in CI, so what is verified
here is the tool's logic against the schema as understood, not against every Zotero version.
The first run on a real library should be `import --dry-run`.

Names and titles are invented on purpose. Each case states what must hold -- and the cases
that matter most are the refusals: read-only, nothing personal copied, nothing guessed, and an
import that either completes or leaves no trace.
"""
import contextlib
import hashlib
import io
import json
import os
import re
import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import registry                      # noqa: E402
import library_meta as lm            # noqa: E402
import library as lib                # noqa: E402
import fetch_source                  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None

passed = failed = skipped = 0


def expect(description, got, want=True):
    global passed, failed
    ok = got == want
    passed += ok
    failed += not ok
    print(f"  {'ok  ' if ok else 'FAIL'} {description}" + ("" if ok else f"  (got {got!r}, wanted {want!r})"))


def skip(description, why):
    global skipped
    skipped += 1
    print(f"  skip {description}  ({why})")


def refused(fn, *a, **kw):
    try:
        fn(*a, **kw)
    except (lm.LibraryError, registry.RegistryError) as exc:
        return str(exc)
    return None


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree(root):
    return sorted(str(p.relative_to(root)) for p in Path(root).rglob("*"))


SECRET = "PRIVATE-NOTE-DO-NOT-LEAK"
PDF = b"%PDF-1.4\n% a small stand-in for a paper\n" + b"x" * 400

# --------------------------------------------------------------------------- fixtures

ZOTERO_SCHEMA = """
CREATE TABLE libraries (libraryID INTEGER PRIMARY KEY, type TEXT);
CREATE TABLE groups (groupID INTEGER PRIMARY KEY, libraryID INT, name TEXT);
CREATE TABLE itemTypes (itemTypeID INTEGER PRIMARY KEY, typeName TEXT);
CREATE TABLE items (itemID INTEGER PRIMARY KEY, itemTypeID INT, dateAdded TEXT, dateModified TEXT,
                    libraryID INT, key TEXT);
CREATE TABLE fields (fieldID INTEGER PRIMARY KEY, fieldName TEXT);
CREATE TABLE itemDataValues (valueID INTEGER PRIMARY KEY, value TEXT);
CREATE TABLE itemData (itemID INT, fieldID INT, valueID INT);
CREATE TABLE creators (creatorID INTEGER PRIMARY KEY, firstName TEXT, lastName TEXT, fieldMode INT);
CREATE TABLE creatorTypes (creatorTypeID INTEGER PRIMARY KEY, creatorType TEXT);
CREATE TABLE itemCreators (itemID INT, creatorID INT, creatorTypeID INT, orderIndex INT);
CREATE TABLE itemAttachments (itemID INTEGER PRIMARY KEY, parentItemID INT, linkMode INT,
                              contentType TEXT, path TEXT);
CREATE TABLE itemNotes (itemID INTEGER PRIMARY KEY, parentItemID INT, note TEXT, title TEXT);
CREATE TABLE tags (tagID INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE itemTags (itemID INT, tagID INT, type INT);
CREATE TABLE collections (collectionID INTEGER PRIMARY KEY, collectionName TEXT, parentCollectionID INT);
CREATE TABLE collectionItems (collectionID INT, itemID INT, orderIndex INT);
CREATE TABLE deletedItems (itemID INTEGER PRIMARY KEY, dateDeleted TEXT);
"""


def build_zotero(base):
    zdir = Path(base) / "Zotero"
    storage = zdir / "storage"
    for key in ("PDFGOOD1", "SNAPSHT1", "BIGPDF01", "FAKEPDF1"):
        (storage / key).mkdir(parents=True)
    (storage / "PDFGOOD1" / "marlowe1985.pdf").write_bytes(PDF)
    (storage / "SNAPSHT1" / "page.html").write_bytes(b"<html><body>abstract only</body></html>")
    (storage / "BIGPDF01" / "huge.pdf").write_bytes(PDF + b"y" * (1536 * 1024))
    (storage / "FAKEPDF1" / "notapdf.pdf").write_bytes(b"<html>login required</html>")

    db = sqlite3.connect(zdir / "zotero.sqlite")
    db.executescript(ZOTERO_SCHEMA)
    db.executemany("INSERT INTO libraries VALUES (?,?)", [(1, "user"), (2, "group")])
    db.execute("INSERT INTO groups VALUES (1, 2, 'Toy Lab Group')")
    db.executemany("INSERT INTO itemTypes VALUES (?,?)", [
        (1, "journalArticle"), (2, "preprint"), (3, "report"), (4, "attachment"), (5, "note"),
        (6, "book"), (7, "bookSection")])
    db.executemany("INSERT INTO fields VALUES (?,?)", [
        (1, "title"), (2, "date"), (3, "publicationTitle"), (4, "DOI"), (5, "volume"),
        (6, "pages"), (7, "extra"), (8, "abstractNote"), (9, "ISSN"), (10, "repository"),
        (11, "archiveID"), (12, "url"), (13, "institution"), (14, "reportNumber")])
    db.executemany("INSERT INTO creatorTypes VALUES (?,?)", [(1, "author"), (2, "editor")])

    values, fid = {}, {"title": 1, "date": 2, "publicationTitle": 3, "DOI": 4, "volume": 5,
                       "pages": 6, "extra": 7, "abstractNote": 8, "ISSN": 9, "repository": 10,
                       "archiveID": 11, "url": 12, "institution": 13, "reportNumber": 14}

    def put(item, **kw):
        for name, value in kw.items():
            vid = values.setdefault(value, len(values) + 1)
            db.execute("INSERT INTO itemData VALUES (?,?,?)", (item, fid[name], vid))

    def item(item_id, type_id, key, lib_id=1):
        db.execute("INSERT INTO items VALUES (?,?,?,?,?,?)",
                   (item_id, type_id, "2026-01-02 03:04:05", "2026-02-03 04:05:06", lib_id, key))

    # 101: a journal article with every kind of attachment
    item(101, 1, "ITEM0101")
    put(101, title="A toy model of resonant spectra", date="1985-06-01 June 1985",
        publicationTitle="J. Toy Phys. A", DOI="10.1234/toy.1985.0119", volume="402",
        pages="285-298", ISSN="0000-0001",
        extra="Citation Key: Marlowe1985\nPMID: 123456",
        abstractNote="We study a toy operator and its spectrum.")
    db.execute("INSERT INTO creators VALUES (1, 'Alice B.', 'Marlowe', 0)")
    db.execute("INSERT INTO itemCreators VALUES (101, 1, 1, 0)")
    db.executemany("INSERT INTO tags VALUES (?,?)", [(1, "spectra"), (2, "benchmark")])
    db.executemany("INSERT INTO itemTags VALUES (101, ?, 0)", [(1,), (2,)])
    db.executemany("INSERT INTO collections VALUES (?,?,?)", [(1, "Physics", None), (2, "Toy models", 1)])
    db.execute("INSERT INTO collectionItems VALUES (2, 101, 0)")
    for att, key, ctype, path in [(103, "PDFGOOD1", "application/pdf", "storage:marlowe1985.pdf"),
                                  (104, "SNAPSHT1", "text/html", "storage:page.html"),
                                  (105, "BIGPDF01", "application/pdf", "storage:huge.pdf"),
                                  (106, "FAKEPDF1", "application/pdf", "storage:notapdf.pdf"),
                                  (107, "TRASHED1", "application/pdf", "storage:gone.pdf")]:
        item(att, 4, key)
        db.execute("INSERT INTO itemAttachments VALUES (?,101,1,?,?)", (att, ctype, path))
    db.execute("INSERT INTO deletedItems VALUES (107, '2026-03-01')")
    item(111, 5, "NOTE0111")                                    # a child note: must never leak
    db.execute("INSERT INTO itemNotes VALUES (111, 101, ?, 'my note')", (f"<p>{SECRET}</p>",))

    # 102: a preprint, arXiv recorded only in the repository / archiveID fields
    item(102, 2, "ITEM0102")
    put(102, title="Spectra of toy operators", date="2025-04-02", repository="arXiv",
        archiveID="2504.01234v2")
    db.execute("INSERT INTO creators VALUES (2, 'Bo', 'Tester', 0)")
    db.execute("INSERT INTO itemCreators VALUES (102, 2, 1, 0)")

    # 112: single-field author (an organisation) and an editor
    item(112, 3, "ITEM0112")
    put(112, title="Annual toy report & review", date="2020", institution="Toy Institute",
        reportNumber="TR-7")
    db.execute("INSERT INTO creators VALUES (3, '', 'Toy Standards Organisation', 1)")
    db.execute("INSERT INTO creators VALUES (4, 'Cy', 'Editor', 0)")
    db.execute("INSERT INTO itemCreators VALUES (112, 3, 1, 0)")
    db.execute("INSERT INTO itemCreators VALUES (112, 4, 2, 1)")

    # 109: in the trash.  110: a standalone note.  113: in a group library, same author-year.
    item(109, 1, "ITEM0109")
    put(109, title="A trashed toy article", date="1999")
    db.execute("INSERT INTO deletedItems VALUES (109, '2026-03-01')")
    item(110, 5, "NOTE0110")
    db.execute("INSERT INTO itemNotes VALUES (110, NULL, ?, 'standalone')", (SECRET,))
    item(113, 1, "ITEM0113", lib_id=2)
    put(113, title="Another toy model of resonant spectra", date="1985",
        publicationTitle="Group Journal", DOI="10.1234/toy.other.1985")
    db.execute("INSERT INTO itemCreators VALUES (113, 1, 1, 0)")

    db.executemany("INSERT INTO itemDataValues VALUES (?,?)", [(v, k) for k, v in values.items()])
    db.commit()
    db.close()
    return zdir


def build_calibre(base):
    cdir = Path(base) / "Calibre Library"
    book = cdir / "Marlowe, Alice" / "A Textbook of Toy Operators (7)"
    book.mkdir(parents=True)
    (book / "A Textbook of Toy Operators - Alice Marlowe.pdf").write_bytes(PDF)
    (book / "A Textbook of Toy Operators - Alice Marlowe.epub").write_bytes(b"PK\x03\x04epub")
    big = cdir / "Marlowe, Alice" / "A Very Large Book (8)"
    big.mkdir(parents=True)
    (big / "Large.pdf").write_bytes(PDF + b"z" * (1536 * 1024))
    (big / "Large.epub").write_bytes(b"PK\x03\x04small epub")

    db = sqlite3.connect(cdir / "metadata.db")
    db.executescript("""
    CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, sort TEXT, timestamp TEXT, pubdate TEXT,
        series_index REAL, author_sort TEXT, isbn TEXT, lccn TEXT, path TEXT, uuid TEXT,
        last_modified TEXT);
    CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE books_authors_link (id INTEGER PRIMARY KEY, book INT, author INT);
    CREATE TABLE publishers (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE books_publishers_link (id INTEGER PRIMARY KEY, book INT, publisher INT);
    CREATE TABLE tags (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE books_tags_link (id INTEGER PRIMARY KEY, book INT, tag INT);
    CREATE TABLE series (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE books_series_link (id INTEGER PRIMARY KEY, book INT, series INT);
    CREATE TABLE languages (id INTEGER PRIMARY KEY, lang_code TEXT);
    CREATE TABLE books_languages_link (id INTEGER PRIMARY KEY, book INT, lang_code INT);
    CREATE TABLE identifiers (id INTEGER PRIMARY KEY, book INT, type TEXT, val TEXT);
    CREATE TABLE comments (id INTEGER PRIMARY KEY, book INT, text TEXT);
    CREATE TABLE data (id INTEGER PRIMARY KEY, book INT, format TEXT, uncompressed_size INT, name TEXT);
    CREATE TABLE custom_columns (id INTEGER PRIMARY KEY, label TEXT);
    INSERT INTO authors VALUES (1, 'Alice B. Marlowe');
    INSERT INTO publishers VALUES (1, 'Toy Press');
    INSERT INTO tags VALUES (1, 'textbook');
    INSERT INTO languages VALUES (1, 'eng');
    INSERT INTO custom_columns VALUES (1, 'read_status');
    INSERT INTO books VALUES (7, 'A Textbook of Toy Operators', 'Textbook of Toy Operators, A',
        '2026-01-01', '1983-01-01 00:00:00+00:00', 1.0, 'Marlowe, Alice', '9780000000002', '',
        'Marlowe, Alice/A Textbook of Toy Operators (7)', 'uuid-7', '2026-01-01');
    INSERT INTO books VALUES (8, 'A Very Large Book', 'Very Large Book, A', '2026-01-01',
        '2001-01-01 00:00:00+00:00', 1.0, 'Marlowe, Alice', '', '', 'Marlowe, Alice/A Very Large Book (8)',
        'uuid-8', '2026-01-01');
    INSERT INTO books_authors_link VALUES (1, 7, 1), (2, 8, 1);
    INSERT INTO books_publishers_link VALUES (1, 7, 1);
    INSERT INTO books_tags_link VALUES (1, 7, 1);
    INSERT INTO books_languages_link VALUES (1, 7, 1);
    INSERT INTO identifiers VALUES (1, 7, 'isbn', '9780000000002');
    INSERT INTO comments VALUES (1, 7, 'A textbook on toy operators.');
    INSERT INTO data VALUES (1, 7, 'PDF', 440, 'A Textbook of Toy Operators - Alice Marlowe');
    INSERT INTO data VALUES (2, 7, 'EPUB', 10, 'A Textbook of Toy Operators - Alice Marlowe');
    INSERT INTO data VALUES (3, 8, 'PDF', 1500000, 'Large');
    INSERT INTO data VALUES (4, 8, 'EPUB', 20, 'Large');
    """)
    db.commit()
    db.close()
    return cdir


def new_papers(base, name="papers"):
    papers = Path(base) / name
    papers.mkdir(parents=True)
    return papers


def open_z(zdir):
    path = zdir / "zotero.sqlite"
    return path, lm.ReadOnly(path)


def read_z(zdir, ref):
    path, ro = open_z(zdir)
    with ro as db:
        return lm.read_zotero(db, zdir, ref)


def read_c(cdir, book):
    with lm.ReadOnly(cdir / "metadata.db") as db:
        return lm.read_calibre(db, cdir, book)


def bib_norm(text):
    return re.sub(r"[ \t]+", " ", text).strip()


# --------------------------------------------------------------------------- tests

root = Path(tempfile.mkdtemp(prefix="libtest."))
zdir, cdir = build_zotero(root), build_calibre(root)
zdb_before = sha(zdir / "zotero.sqlite")

print("registry.py — one writer for papers/sources.yaml")
reg = root / "reg" / "sources.yaml"
reg.parent.mkdir()
reg.write_text("# old seed\nsources: []\n")
registry.ensure_registry(reg)
expect("the old `sources: []` seed is migrated to a block list", "sources:\n" in reg.read_text()
       and "[]" not in reg.read_text())
tricky = 'Pre-1991: "quoted" & a # hash, with unicode — é'
registry.append_source("Tricky_1", [("title", tricky), ("doi", "10.1000/a:b"), ("file", None),
                                    ("verified", False, "a trailing comment")], reg)
registry.append_source("Second-2", [("role", "FILL IN", "primary | benchmark")], reg)
mine = registry.parse_sources(reg)
expect("two entries round-trip through the project's own parser", len(mine), 2)
expect("a tricky title survives the round trip", mine[0]["title"], tricky)
expect("a colon inside a DOI survives", mine[0]["doi"], "10.1000/a:b")
expect("null stays null", mine[0]["file"], None)
if yaml:
    theirs = yaml.safe_load(reg.read_text())["sources"]
    expect("PyYAML reads the same file as valid YAML", len(theirs), 2)
    expect("PyYAML agrees on the tricky title", theirs[0]["title"], tricky)
    expect("PyYAML reads `verified: false` as a boolean", theirs[0]["verified"], False)
else:
    skip("PyYAML cross-check", "PyYAML not installed")
expect("a duplicate label is refused", bool(refused(registry.append_source, "Second-2", [], reg)))
expect("a path-traversal label is refused",
       bool(refused(registry.append_source, "../escape", [], reg)))
expect("an unknown file shape is refused rather than guessed at", bool(refused(
    registry.ensure_registry, (lambda p: (p.write_text("not: a registry\n"), p)[1])(root / "reg" / "x.yaml"))))

print("fetch_source.py — now writes through the shared writer")
saved_reg = registry.REGISTRY
registry.REGISTRY = root / "fetch" / "sources.yaml"
registry.REGISTRY.parent.mkdir()
registry.REGISTRY.write_text("sources: []\n")
with contextlib.redirect_stdout(io.StringIO()):
    fetch_source.register("Doi_One", "10.1000/one", "doi", {"file": None})
    fetch_source.register(fetch_source.default_label("10.1000/two"), "10.1000/two", "doi",
                          {"file": None})
if yaml:
    got = yaml.safe_load(registry.REGISTRY.read_text())["sources"]
    expect("two fetches leave a registry PyYAML can read (it used to become invalid)", len(got), 2)
    expect("default labels for unlabelled DOIs do not collide", got[0]["label"] != got[1]["label"])
else:
    expect("two fetches parse", len(registry.parse_sources(registry.REGISTRY)), 2)
expect("a derived label is valid", registry.valid_label(fetch_source.default_label("10.1000/two")))
registry.REGISTRY = saved_reg

print("library_meta.py — reading ALL metadata, read-only (Zotero)")
rec = read_z(zdir, 101)
expect("every field is read, including ones nobody asked for",
       {"abstractNote", "extra", "ISSN", "title"} <= set(rec["fields"]))
expect("creators keep first names and types", rec["creators"][0],
       {"type": "author", "first": "Alice B.", "last": "Marlowe", "single_field": False})
expect("tags are read", sorted(rec["tags"]), ["benchmark", "spectra"])
expect("collections are read as a path", rec["collections"], ["Physics / Toy models"])
expect("item type and key are recorded", (rec["source"]["item_type"], rec["source"]["item_key"]),
       ("journalArticle", "ITEM0101"))
expect("a trashed attachment is not listed", len(rec["attachments"]), 4)
expect("by key works as well as by itemID", read_z(zdir, "ITEM0101")["source"]["item_id"], 101)
expect("the child note's text is not in the record", SECRET not in json.dumps(rec, default=str))
expect("a group-library item records its library", read_z(zdir, 113)["source"]["library_type"], "group")
expect("...and the group's name", read_z(zdir, 113)["source"]["group_name"], "Toy Lab Group")

print("library_meta.py — refusals")
expect("a trashed item is refused, and says why", "trash" in (refused(read_z, zdir, 109) or ""))
expect("an attachment is refused and the parent is named",
       "parent, item 101" in (refused(read_z, zdir, 103) or ""))
expect("a standalone note is refused", "note" in (refused(read_z, zdir, 110) or ""))
expect("a missing item is refused", "no Zotero item" in (refused(read_z, zdir, 99999) or ""))

print("library_meta.py — BibTeX is built from catalogue metadata, known answers")
ref = lm.normalise(rec)
entry = lm.to_bibtex(ref, lm.cite_key(ref, set()))
expect("an article, in full", bib_norm(entry), bib_norm("""@article{Marlowe1985,
  author = {Marlowe, Alice B.},
  title = {A toy model of resonant spectra},
  journal = {J. Toy Phys. A},
  year = {1985},
  volume = {402},
  pages = {285--298},
  issn = {0000-0001},
  doi = {10.1234/toy.1985.0119},
}"""))
expect("the key comes from Zotero's `Citation Key:` line", lm.cite_key(ref, set()), "Marlowe1985")
expect("a key falls back to Author+Year when there is none",
       lm.cite_key(dict(ref, cite_key=None), set()), "Marlowe1985")
expect("a colliding key gets a suffix", lm.cite_key(dict(ref, cite_key=None), {"Marlowe1985"}),
       "Marlowe1985a")
org = lm.normalise(read_z(zdir, 112))
org_entry = lm.to_bibtex(org, "Toy2020")
expect("a single-field author is braced so BibTeX does not split it",
       "author = {{Toy Standards Organisation}}" in bib_norm(org_entry))
expect("an editor is kept", "editor = {Editor, Cy}" in bib_norm(org_entry))
expect("& in a title is escaped", "Annual toy report \\& review" in org_entry)
expect("a report becomes @techreport", org_entry.startswith("@techreport{Toy2020,"))
expect("math is left alone: _ and $ are not escaped",
       "$x_1$" in lm.to_bibtex(dict(ref, title="On $x_1$ and 50% of cases"), "K"))
expect("...but % is", "50\\% of cases" in lm.to_bibtex(dict(ref, title="On $x_1$ and 50% of cases"), "K"))
expect("an unbalanced brace is dropped rather than breaking the file",
       "{" not in lm.to_bibtex(dict(ref, title="Broken {title"), "K").split("title")[1].split("\n")[0].replace("= {", ""))
expect("pages with a hyphen or en dash become --", "pages = {10--20}" in bib_norm(
    lm.to_bibtex(dict(ref, pages="10–20"), "K")))

print("library_meta.py — arXiv identifiers are found, never invented")
pre = lm.normalise(read_z(zdir, 102))
expect("from repository + archiveID", (pre["eprint"], pre["primary_class"]), ("2504.01234v2", None))
pre_entry = lm.to_bibtex(pre, "Tester2025")
expect("eprint and archivePrefix are written together",
       "eprint = {2504.01234v2}" in bib_norm(pre_entry) and "archivePrefix = {arXiv}" in bib_norm(pre_entry))
expect("a missing primaryClass is flagged, not made up",
       "primaryClass not in the catalogue" in pre_entry and "primaryClass =" not in pre_entry)
expect("from a URL", lm.find_arxiv("https://arxiv.org/abs/2504.01234v3")[0], "2504.01234v3")
expect("from an arXiv DOI", lm.find_arxiv("10.48550/arXiv.2504.01234")[0], "2504.01234")
expect("an old-style ID carries its primary class", lm.find_arxiv("arXiv:hep-th/9901001"),
       ("hep-th/9901001", "hep-th"))
expect("a journal DOI is not mistaken for an arXiv ID", lm.find_arxiv("10.1103/PhysRevD.111.044002"),
       (None, None))

print("library_meta.py — Calibre")
book = read_c(cdir, 7)
cref = lm.normalise(book)
centry = lm.to_bibtex(cref, lm.cite_key(cref, set()))
expect("a book becomes @book with publisher, year, ISBN", bib_norm(centry), bib_norm("""@book{Marlowe1983,
  author = {{Alice B. Marlowe}},
  title = {A Textbook of Toy Operators},
  year = {1983},
  publisher = {Toy Press},
  isbn = {9780000000002},
}"""))
expect("formats and sizes are listed", sorted(f["format"] for f in book["formats"]), ["EPUB", "PDF"])
expect("custom columns are reported as NOT read, not silently skipped",
       any("custom column" in g for g in book["schema_gaps"]))
expect("a missing book is refused", "no Calibre book" in (refused(read_c, cdir, 999) or ""))

print("library_meta.py — planning an import: small files only, and say why not")
papers = new_papers(root)
plan = lm.build_import(rec, papers_dir=papers, max_mb=1)
actions = {f["name"]: (f["action"], f["reason"]) for f in plan["files"]}
expect("the small real PDF is copied", actions["marlowe1985.pdf"][0], "copy")
expect("a saved web page is not", "snapshot" in (actions["page.html"][1] or ""))
expect("an oversize PDF is not, and the size limit is named", "limit" in (actions["huge.pdf"][1] or ""))
expect("a file catalogued as PDF that is not a PDF is not", "not one" in (actions["notapdf.pdf"][1] or ""))
expect("exactly one file would be copied", sum(f["action"] == "copy" for f in plan["files"]), 1)
expect("--no-file copies nothing", sum(f["action"] == "copy" for f in
       lm.build_import(rec, papers_dir=papers, no_file=True)["files"]), 0)
cplan = lm.build_import(book, papers_dir=papers, max_mb=1)
expect("Calibre: the preferred format (PDF) is chosen", [f["name"].rsplit(".", 1)[1] for f in cplan["files"]
       if f["action"] == "copy"], ["pdf"])
cbig = lm.build_import(read_c(cdir, 8), papers_dir=papers, max_mb=1)
expect("Calibre: an oversize PDF falls back to the EPUB",
       [f["name"].rsplit(".", 1)[1] for f in cbig["files"] if f["action"] == "copy"], ["epub"])

print("import — a dry run writes nothing")
before = tree(root / "papers")
with contextlib.redirect_stdout(io.StringIO()):
    lm.build_import(rec, papers_dir=papers)
expect("building a plan leaves papers/ untouched", tree(root / "papers"), before)

print("import — the full thing")
plan = lm.build_import(rec, papers_dir=papers, max_mb=1, role="benchmark")
result = lm.execute_import(plan, library_db_mtime=(zdir / "zotero.sqlite").stat().st_mtime)
dest = papers / "imported" / "Marlowe1985"
expect("the PDF is copied", (dest / "marlowe1985.pdf").read_bytes(), PDF)
expect("and nothing else is", sorted(p.name for p in dest.iterdir()), ["marlowe1985.pdf", "metadata.json"])
meta = json.loads((dest / "metadata.json").read_text())
expect("metadata.json holds every field read", {"abstractNote", "extra", "ISSN"} <= set(meta["fields"]))
expect("...with first names, tags and collections",
       (meta["creators"][0]["first"], sorted(meta["tags"]), meta["collections"]),
       ("Alice B.", ["benchmark", "spectra"], ["Physics / Toy models"]))
expect("the import is recorded as unverified", meta["import"]["verified"], False)
expect("what was left out by design is listed", "Zotero notes" in meta["import"]["excluded_by_design"])
expect("every skipped file records its reason", all(f["reason"] for f in meta["import"]["files"]
       if f["action"] == "skip"))
entries = registry.parse_sources(papers / "sources.yaml")
expect("sources.yaml gains one entry", len(entries), 1)
e = entries[0]
expect("with the DOI, role and provenance", (e["doi"], e["role"], "item key ITEM0101" in e["provenance"]),
       ("10.1234/toy.1985.0119", "benchmark", True))
expect("the recorded sha256 matches the copied file", e["sha256"], sha(dest / "marlowe1985.pdf"))
expect("verified is false", e["verified"], "false")
expect("the file path is relative to papers/", e["file"], "imported/Marlowe1985/marlowe1985.pdf")
if yaml:
    expect("and the registry is valid YAML", yaml.safe_load((papers / "sources.yaml").read_text())
           ["sources"][0]["verified"], False)
bib = (papers / "refs.bib").read_text()
expect("refs.bib gains the entry", "@article{Marlowe1985," in bib)
expect("...marked UNVERIFIED", "UNVERIFIED" in bib)
expect("the library database is byte-identical afterwards (read-only held)",
       sha(zdir / "zotero.sqlite"), zdb_before)
leak = [str(p.relative_to(papers)) for p in papers.rglob("*") if p.is_file()
        and (SECRET.encode() in p.read_bytes() or str(root).encode() in p.read_bytes()
             or str(zdir).encode() in p.read_bytes())]
expect("no private note text and no machine path in anything written", leak, [])

print("import — refusals and rollback")
expect("importing the same item again is refused", bool(refused(lm.build_import, rec, papers_dir=papers)))
second = lm.build_import(read_z(zdir, 113), papers_dir=papers, label="GroupCopy")
expect("a different item with the same author and year gets a distinct key",
       second["key"], "Marlowe1985a")
dupe_doi = read_z(zdir, 113)
dupe_doi["fields"]["DOI"] = "https://doi.org/10.1234/TOY.1985.0119"
expect("the same DOI under another label is refused", "already in the bibliography" in
       (refused(lm.build_import, dupe_doi, papers_dir=papers, label="Elsewhere") or ""))
expect("a path-traversal label is refused", bool(refused(lm.build_import, read_z(zdir, 102),
       papers_dir=papers, label="../../escape")))
expect("...and nothing was created outside papers/", not (root / "escape").exists())

reg_text, bib_text = (papers / "sources.yaml").read_text(), (papers / "refs.bib").read_text()
real_append = registry.append_bib
registry.append_bib = lambda *a, **k: (_ for _ in ()).throw(OSError("disk full"))
try:
    rb_plan = lm.build_import(read_z(zdir, 102), papers_dir=papers, label="WillFail", max_mb=1)
    try:
        lm.execute_import(rb_plan)
        expect("a failure part-way raises", False)
    except OSError:
        expect("a failure part-way raises", True)
finally:
    registry.append_bib = real_append
expect("...and rolls back: no directory left behind", (papers / "imported" / "WillFail").exists(), False)
expect("...sources.yaml is exactly as it was", (papers / "sources.yaml").read_text(), reg_text)
expect("...refs.bib is exactly as it was", (papers / "refs.bib").read_text(), bib_text)

print("registry.py — the shipped, header-only refs.bib accepts an append")
seeded = root / "seeded" / "refs.bib"
seeded.parent.mkdir()
seeded.write_text((HERE.parent / "papers" / "refs.bib").read_text())
registry.append_bib("Marlowe1985", "@article{Marlowe1985,\n  title = {T},\n}", "imported, UNVERIFIED", seeded)
body = seeded.read_text()
expect("the header is kept", body.startswith("% Bibliography."))
expect("the entry follows it", "@article{Marlowe1985," in body)
expect("a duplicate key is refused", bool(refused(registry.append_bib, "Marlowe1985", "@misc{Marlowe1985,\n}", None, seeded)))
expect("the shipped file has no entries of its own", registry.existing_bib_keys(HERE.parent / "papers" / "refs.bib"), set())

print("import — a size limit still records the work")
p2 = new_papers(root, "papers2")
plan = lm.build_import(read_z(zdir, 102), papers_dir=p2, no_file=True)
lm.execute_import(plan)
e2 = registry.parse_sources(p2 / "sources.yaml")[0]
expect("metadata-only import records no file", e2["file"], None)
expect("...but still records the identifiers", e2["eprint"], "arXiv:2504.01234v2")

print("import — Calibre end to end")
p3 = new_papers(root, "papers3")
lm.execute_import(lm.build_import(book, papers_dir=p3, max_mb=1))
cd3 = p3 / "imported" / "Marlowe1983"
expect("the PDF is copied under a safe name", [p.name for p in cd3.iterdir() if p.suffix == ".pdf"],
       ["A_Textbook_of_Toy_Operators_-_Alice_Marlowe.pdf"])
expect("provenance names the Calibre book id",
       "book id 7" in registry.parse_sources(p3 / "sources.yaml")[0]["provenance"])
expect("no ratings, no machine path in the Calibre import", not any(
    str(root).encode() in p.read_bytes() for p in p3.rglob("*") if p.is_file()))

print("library.py — the command line, end to end")
saved = (registry.ROOT, registry.REGISTRY, registry.REFS)
cli_root = root / "cli"
(cli_root / "papers").mkdir(parents=True)
registry.ROOT, registry.REGISTRY, registry.REFS = (cli_root, cli_root / "papers" / "sources.yaml",
                                                   cli_root / "papers" / "refs.bib")
os.environ["ZOTERO_DIR"], os.environ["CALIBRE_DIR"] = str(zdir), str(cdir)


def cli(*argv):
    out, err = io.StringIO(), io.StringIO()
    old = sys.argv
    sys.argv = ["library.py", *argv]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = lib.main()
            except SystemExit as exc:          # argparse reports a usage error this way
                code = exc.code
    finally:
        sys.argv = old
    return code, out.getvalue(), err.getvalue()


try:
    code, out, _ = cli("show", "--zotero", "101")
    expect("show prints metadata and exits 0", code, 0)
    expect("show lists the fields, tags and what it deliberately did not read",
           all(s in out for s in ("abstractNote", "benchmark", "deliberately not read")))
    expect("show never prints the private note", SECRET not in out)
    code, out, _ = cli("bibtex", "--zotero", "101")
    expect("bibtex prints an UNVERIFIED entry", (code, "@article{Marlowe1985," in out, "UNVERIFIED" in out),
           (0, True, True))
    code, out, _ = cli("import", "--zotero", "101", "--dry-run", "--max-mb", "1")
    expect("import --dry-run says so and writes nothing", (code, "DRY RUN" in out,
           (cli_root / "papers" / "imported").exists()), (0, True, False))
    expect("the dry run explains each skipped file", "because:" in out and "snapshot" in out)
    code, out, _ = cli("import", "--zotero", "101", "--max-mb", "1", "--role", "benchmark")
    expect("import exits 0", code, 0)
    expect("...and tells the PI what is still theirs to do", "still to do" in out.lower())
    code, _, err = cli("import", "--zotero", "101")
    expect("importing it again is refused with exit 1", (code, "refused" in err), (1, True))
    code, _, err = cli("import", "--zotero", "109")
    expect("a trashed item is refused through the CLI", (code, "trash" in err), (1, True))
    code, out, _ = cli("import", "--calibre", "8", "--max-mb", "1", "--formats", "pdf,epub", "--dry-run")
    expect("the CLI plumbs --formats and --max-mb: oversize PDF skipped, EPUB copied",
           "COPY  Large.epub" in out and "skip  Large.pdf" in out)
    code, _, err = cli("import", "--zotero", "101", "--calibre", "7", "--dry-run")
    expect("naming two libraries at once is a usage error", code != 0)
    code, out, _ = cli("search", "--author", "Nobody", "--title", "toy model")
    expect("search is an AND: a missing author means no match, not the title's hits",
           "no match" in out.lower() and "A toy model" not in out)
    code, out, _ = cli("search", "--title", "toy")
    expect("search hides the trashed item", "trashed" not in out)
    expect("search hides attachments and notes", "page.html" not in out and SECRET not in out)
    expect("search points at show and import", "show --zotero" in out and "import --zotero" in out)
finally:
    registry.ROOT, registry.REGISTRY, registry.REFS = saved
    for var in ("ZOTERO_DIR", "CALIBRE_DIR"):
        os.environ.pop(var, None)

print("library_meta.py — a locked live database falls back to a scratch copy")
locker = sqlite3.connect(zdir / "zotero.sqlite", isolation_level=None)
locker.execute("BEGIN EXCLUSIVE")
try:
    with lm.ReadOnly(zdir / "zotero.sqlite") as db:
        n = db.rows("SELECT COUNT(*) FROM items")[0][0]
        expect("a locked database is read from a copy, and says so", (db.copied, n > 0), (True, True))
finally:
    locker.execute("ROLLBACK")
    locker.close()
expect("...and the live file is still untouched", sha(zdir / "zotero.sqlite"), zdb_before)

print(f"\nchecks: {passed} passed, {failed} failed" + (f", {skipped} skipped" if skipped else ""))
import shutil  # noqa: E402
shutil.rmtree(root, ignore_errors=True)
sys.exit(1 if failed else 0)
