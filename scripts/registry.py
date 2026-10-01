#!/usr/bin/env python3
"""Writers for papers/sources.yaml and papers/refs.bib, shared by fetch_source.py and library.py.

Why this exists as one module. `fetch_source.py` used to append block-style list items
(`  - label: ...`) to a registry seeded as `sources: []`. A flow-style empty list cannot be
followed by block items, so the first fetch turned the file into invalid YAML -- nothing
noticed, because nothing parsed it. Two tools now write this file, so there is exactly one
writer, one parser, and a test that round-trips what the writer produces.

Standard library only; the parser understands exactly the shape the writer emits (a `sources:`
key, `  - key: value` list items, `    key: value` continuation lines), not YAML in general.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "papers" / "sources.yaml"
REFS = ROOT / "papers" / "refs.bib"

LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_PLAIN = re.compile(r"^[A-Za-z0-9_./~+()-][A-Za-z0-9_./~+() -]*$")
_ITEM = re.compile(r"^  - (\w+):\s*(.*)$")
_CONT = re.compile(r"^    (\w+):\s*(.*)$")

HEADER = (
    "# Source registry. Every source this project uses, whether or not its file is committed.\n"
    "#\n"
    "# Rules: .claude/rules/sources.md and .claude/rules/bibliography.md\n"
    "#   - every identifier that exists for the work, verified against the work itself;\n"
    "#   - the exact version consulted (preprint vN vs. journal -- they differ);\n"
    "#   - role: primary | benchmark | method-reference | background;\n"
    "#   - verified: false until the identifiers and the file have been checked against the\n"
    "#     document's own first page, then true.\n"
    "#\n"
    "# `make fetch-source` and `scripts/library.py import` append entries here. Fill in role\n"
    "# and notes by hand.\n\n"
    "sources:\n"
)


class RegistryError(Exception):
    pass


def valid_label(label):
    return bool(LABEL_RE.match(label or ""))


def _quote(value):
    """A YAML scalar: plain when that is unambiguous, otherwise a JSON (= YAML) string."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    if text in ("null", "true", "false", "~") or re.fullmatch(r"[0-9.+-]+", text):
        return json.dumps(text)
    if _PLAIN.match(text) and not text.endswith(" "):
        return text
    return json.dumps(text, ensure_ascii=False)


def _unquote(raw):
    raw = raw.strip()
    if "  #" in raw and not raw.startswith('"'):
        raw = raw.split("  #", 1)[0].strip()
    if raw.startswith('"'):
        end = raw.rfind('"')
        try:
            return json.loads(raw[: end + 1])
        except ValueError:
            return raw
    return None if raw in ("null", "~") else raw


def ensure_registry(path=None):
    """Create the registry if absent; migrate the old `sources: []` seed in place."""
    path = Path(path or REGISTRY)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(HEADER, encoding="utf-8")
        return path
    text = path.read_text(encoding="utf-8")
    # [ \t]* and not \s*: \s* also matches newlines, so on a file ending in `sources: []\n` it
    # swallowed the final newline and left `sources:` with no line ending.
    if re.search(r"^sources:[ \t]*\[[ \t]*\][ \t]*$", text, re.M):
        text = re.sub(r"^sources:[ \t]*\[[ \t]*\][ \t]*$", "sources:", text, flags=re.M)
        path.write_text(text, encoding="utf-8")
    elif not re.search(r"^sources:[ \t]*$", text, re.M):
        raise RegistryError(f"{path} has no top-level `sources:` key; refusing to guess")
    return path


def parse_sources(path=None):
    """Return the registry's entries as a list of dicts (values as strings or None)."""
    path = Path(path or REGISTRY)
    if not path.exists():
        return []
    entries, current = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith("sources:"):
            continue
        item, cont = _ITEM.match(line), _CONT.match(line)
        if item:
            current = {item.group(1): _unquote(item.group(2))}
            entries.append(current)
        elif cont and current is not None:
            current[cont.group(1)] = _unquote(cont.group(2))
        else:
            raise RegistryError(f"unexpected line in {path}: {line!r}")
    return entries


def existing_labels(path=None):
    return {e.get("label") for e in parse_sources(path) if e.get("label")}


def _norm_doi(doi):
    doi = (doi or "").strip().lower()
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi)


def existing_dois(registry_path=None, refs_path=None):
    dois = {_norm_doi(e.get("doi")) for e in parse_sources(registry_path) if e.get("doi")}
    refs = Path(refs_path or REFS)
    if refs.exists():
        for m in re.finditer(r"^\s*doi\s*=\s*[{\"]([^}\"]+)[}\"]", refs.read_text(encoding="utf-8"),
                             re.M | re.I):
            dois.add(_norm_doi(m.group(1)))
    return {d for d in dois if d}


def existing_bib_keys(refs_path=None):
    refs = Path(refs_path or REFS)
    if not refs.exists():
        return set()
    return set(re.findall(r"^\s*@\w+\s*\{\s*([^,\s]+)\s*,", refs.read_text(encoding="utf-8"), re.M))


def append_source(label, fields, path=None):
    """Append one entry. `fields` is an ordered list of (key, value[, trailing comment])."""
    if not valid_label(label):
        raise RegistryError(f"invalid label {label!r}: use letters, digits, . _ - (max 64)")
    path = ensure_registry(path)
    if label in existing_labels(path):
        raise RegistryError(f"label {label!r} is already in {path.name}")
    lines = [f"  - label: {_quote(label)}"]
    for field in fields:
        key, value = field[0], field[1]
        comment = f"      # {field[2]}" if len(field) > 2 and field[2] else ""
        lines.append(f"    {key}: {_quote(value)}{comment}")
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + "\n".join(lines) + "\n", encoding="utf-8")


def append_bib(key, entry_text, comment=None, path=None):
    """Append one BibTeX entry, refusing a duplicate key. Never rewrites existing entries."""
    path = Path(path or REFS)
    if key in existing_bib_keys(path):
        raise RegistryError(f"BibTeX key {key!r} is already in {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.exists() else (
        "% Bibliography. Rules: .claude/rules/bibliography.md\n"
        "% Entries marked UNVERIFIED were imported from a catalogue and have not been checked\n"
        "% against the document itself. Check, then delete the marker.\n\n")
    if text and not text.endswith("\n"):
        text += "\n"
    block = (f"% {comment}\n" if comment else "") + entry_text.rstrip("\n") + "\n"
    path.write_text(text + ("\n" if text.strip() else "") + block, encoding="utf-8")
