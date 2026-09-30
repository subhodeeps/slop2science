#!/usr/bin/env python3
"""Fetch a source into papers/ and register it, or say plainly why it must be done by hand.

    scripts/py scripts/fetch_source.py <arxiv-id|doi|url> [label]

arXiv IDs are fetched directly. A DOI or publisher URL is deliberately NOT fetched: paywalls
and terms differ, and a script that appears to fetch anything invites a half-downloaded HTML
error page sitting in papers/ named like a paper. For those, the identifier is registered and
the PI places the PDF in papers/_drop/ themselves.

PDFs are gitignored by default (TEMPLATE_GUIDE.md section 4); the registry entry is what gets
committed, so a source stays identifiable even where its file is not redistributable.
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "papers" / "sources.yaml"
ARXIV = re.compile(r"^(?:arxiv:)?(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+/\d{7}(?:v\d+)?)$", re.I)


def register(label, identifier, filename, kind):
    entry = (f"\n  - label: {label}\n"
             f"    {kind}: {identifier}\n"
             f"    file: {filename or 'null'}\n"
             f"    role: FILL IN      # primary | benchmark | method-reference | background\n"
             f"    notes: FILL IN\n")
    with REGISTRY.open("a", encoding="utf-8") as fh:
        fh.write(entry)
    print(f"registered '{label}' in papers/sources.yaml -- fill in role and notes")


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print(__doc__.strip(), file=sys.stderr)
        return 64
    ident = sys.argv[1].strip()
    label = sys.argv[2].strip() if len(sys.argv) > 2 and sys.argv[2].strip() else None

    match = ARXIV.match(ident)
    if not match:
        kind = "doi" if ident.lower().startswith("10.") or "doi.org" in ident else "url"
        register(label or "UNLABELLED", ident, None, kind)
        print("\nNot an arXiv ID, so nothing was downloaded.")
        print("Place the PDF in papers/_drop/ yourself; the next session's start hook will")
        print("notice it, and the literature skill completes the intake.")
        return 0

    arxiv_id = match.group(1)
    label = label or arxiv_id.replace("/", "_")
    dest = ROOT / "papers" / f"{arxiv_id.replace('/', '_')}.pdf"
    if dest.exists():
        print(f"{dest.relative_to(ROOT)} already present; registering only")
        register(label, f"arXiv:{arxiv_id}", dest.name, "eprint")
        return 0

    url = f"https://arxiv.org/pdf/{arxiv_id}"
    print(f"fetching {url}")
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "claude-code-research-scholar-template"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
    except Exception as exc:
        print(f"download failed: {exc}", file=sys.stderr)
        print("Register the identifier and drop the PDF in papers/_drop/ by hand.",
              file=sys.stderr)
        return 1
    if not data.startswith(b"%PDF"):
        print("downloaded content is not a PDF (paywall or error page); nothing written",
              file=sys.stderr)
        return 1
    dest.write_bytes(data)
    print(f"wrote {dest.relative_to(ROOT)} ({len(data) // 1024} KiB; gitignored by default)")
    register(label, f"arXiv:{arxiv_id}", dest.name, "eprint")
    print("\nNow run the source audit (/source-audit) before writing any code.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
