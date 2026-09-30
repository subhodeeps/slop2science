#!/usr/bin/env python3
"""Fetch a source paper, preferring its LaTeX source over the rendered PDF, and register it.

    scripts/py scripts/fetch_source.py <arxiv-id> [label]          # source tarball + PDF
    scripts/py scripts/fetch_source.py <arxiv-id> [label] --pdf-only
    scripts/py scripts/fetch_source.py <doi|url> [label]           # registers only

**Why source first.** Extracting text from a PDF is a reconstruction, and for anything with
fractions, stacked indices or matrices it is a lossy one: ligatures vanish, nested structure
is reordered, and the result reads as perfectly plausible. The LaTeX source is what the
authors actually wrote — the equation, not a rendering of it. The three most expensive
documentation errors in the project this template came from all traced to reading a PDF's
text layer instead of the page (docs/failure_modes.md entry 2), and the source would have
made two of them impossible.

The tarball also carries what the PDF cannot give back:

  * `.tex`      — the equations verbatim, with the authors' own macros
  * figures     — `.pdf`/`.eps`/`.png` plot files, far better than a screenshot of a figure,
                  and occasionally with the numbers still in them (`.eps`/PGF are text)
  * `.bbl`/`.bib` — the bibliography with identifiers already resolved
  * data files  — some authors ship the `.dat`/`.csv` behind a table or figure. When they do,
                  that is a benchmark with real provenance rather than digits read off a plot

Layout:
    papers/<id>.pdf              the rendered paper (gitignored by default)
    papers/source/<id>/          the extracted source tree (gitignored by default)
    papers/sources.yaml          the registry entry (committed — this is the record)

A DOI or publisher URL is deliberately *not* fetched: paywalls and terms differ, and a script
that appears to fetch anything ends up storing an HTML error page named like a paper. Those
are registered, and the PI puts the file in `papers/_drop/`.
"""
import gzip
import io
import re
import shutil
import sys
import tarfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "papers" / "sources.yaml"
UA = "claude-code-research-template (paper reproduction; one fetch per paper)"

ARXIV = re.compile(r"^(?:arxiv:)?(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+/\d{7}(?:v\d+)?)$", re.I)

TEX_LIKE = {".tex", ".bbl", ".bib", ".sty", ".cls", ".clo", ".bst"}
FIGURE_LIKE = {".pdf", ".eps", ".ps", ".png", ".jpg", ".jpeg", ".svg", ".pgf", ".tikz"}
DATA_LIKE = {".dat", ".csv", ".txt", ".tsv", ".json"}


def get(url, timeout=180):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def register(label, identifier, kind, files):
    entry = (f"\n  - label: {label}\n"
             f"    {kind}: {identifier}\n"
             f"    version: FILL IN     # the exact version consulted (vN / journal)\n")
    for key, value in files.items():
        entry += f"    {key}: {value}\n"
    entry += ("    role: FILL IN        # primary | benchmark | method-reference | background\n"
              "    notes: FILL IN       # what THIS project needs from it, specifically\n")
    with REGISTRY.open("a", encoding="utf-8") as handle:
        handle.write(entry)
    print(f"\nregistered '{label}' in papers/sources.yaml — fill in version, role and notes")


def summarize(tree):
    """Report what the extracted source actually contains, by category."""
    buckets = {"tex": [], "figures": [], "data": [], "other": []}
    for path in sorted(tree.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(tree)
        suffix = path.suffix.lower()
        if suffix in TEX_LIKE:
            buckets["tex"].append(rel)
        elif suffix in FIGURE_LIKE:
            buckets["figures"].append(rel)
        elif suffix in DATA_LIKE:
            buckets["data"].append(rel)
        else:
            buckets["other"].append(rel)

    try:
        shown_path = tree.relative_to(ROOT)
    except ValueError:                    # a tree outside the repo (tests, a custom dest)
        shown_path = tree
    print(f"\nextracted {shown_path}:")
    for name, label in (("tex", "LaTeX/bib"), ("figures", "figures"),
                        ("data", "data files"), ("other", "other")):
        items = buckets[name]
        if not items:
            continue
        shown = ", ".join(str(p) for p in items[:6])
        more = f" … +{len(items) - 6} more" if len(items) > 6 else ""
        print(f"  {label:<10} {len(items):>3}  {shown}{more}")

    if buckets["data"]:
        print("\n  NOTE: this source ships data files. If any of them is the table or figure\n"
              "  you need, that is a benchmark with real provenance — far better than digits\n"
              "  read off a plot. Record which file, in the benchmark's provenance header.")
    if not buckets["tex"]:
        print("\n  NOTE: no .tex found. This submission may be PDF-only, or the tarball may\n"
              "  hold a single flattened file. Read the PDF as page images instead\n"
              "  (.claude/skills/literature-audit/SKILL.md).")
    return buckets


def extract_source(blob, dest):
    """Extract an arXiv e-print payload: tar.gz, bare gzip of one .tex, or raw."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:*") as tar:
            members = [m for m in tar.getmembers()
                       if m.isfile() and not m.name.startswith(("/", ".."))
                       and ".." not in Path(m.name).parts]
            for member in members:
                tar.extract(member, dest, filter="data")
        return "tar"
    except tarfile.TarError:
        pass

    try:
        text = gzip.decompress(blob)
        (dest / "main.tex").write_bytes(text)
        return "gzip-single"
    except OSError:
        pass

    (dest / "e-print.bin").write_bytes(blob)
    return "unknown"


def fetch_arxiv(arxiv_id, label, pdf_only):
    files = {}
    name = arxiv_id.replace("/", "_")

    if not pdf_only:
        url = f"https://arxiv.org/e-print/{arxiv_id}"
        print(f"fetching source  {url}")
        try:
            blob = get(url)
        except (urllib.error.URLError, OSError) as exc:
            print(f"  source fetch failed: {exc}", file=sys.stderr)
            print("  continuing with the PDF; re-run later for the source.", file=sys.stderr)
        else:
            if blob[:4] == b"%PDF":
                print("  arXiv returned a PDF: this submission has no LaTeX source.")
            else:
                tree = ROOT / "papers" / "source" / name
                how = extract_source(blob, tree)
                print(f"  {len(blob) // 1024} KiB, extracted as {how}")
                summarize(tree)
                files["source"] = f"papers/source/{name}/"

    url = f"https://arxiv.org/pdf/{arxiv_id}"
    print(f"\nfetching pdf     {url}")
    dest = ROOT / "papers" / f"{name}.pdf"
    try:
        blob = get(url)
    except (urllib.error.URLError, OSError) as exc:
        print(f"  pdf fetch failed: {exc}", file=sys.stderr)
    else:
        if blob.startswith(b"%PDF"):
            dest.write_bytes(blob)
            print(f"  wrote papers/{name}.pdf ({len(blob) // 1024} KiB; gitignored by default)")
            files["file"] = f"{name}.pdf"
        else:
            print("  downloaded content is not a PDF; nothing written", file=sys.stderr)

    if not files:
        return 1
    register(label, f"arXiv:{arxiv_id}", "eprint", files)
    print("\nNext: verify from the document itself that this is the paper you wanted,")
    print("then run the source audit (/source-audit) before writing any code.")
    return 0


def main():
    args = [a for a in sys.argv[1:] if a]
    pdf_only = "--pdf-only" in args
    args = [a for a in args if not a.startswith("--")]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        return 64

    identifier = args[0].strip()
    label = args[1].strip() if len(args) > 1 else None

    match = ARXIV.match(identifier)
    if not match:
        kind = "doi" if identifier.lower().startswith("10.") or "doi.org" in identifier else "url"
        register(label or "UNLABELLED", identifier, kind, {"file": "null"})
        print("\nNot an arXiv ID, so nothing was downloaded — deliberately.")
        print("Place the file in papers/_drop/; the next session's start hook reports it and")
        print("the literature skill completes the intake.")
        print("If the work IS on arXiv, prefer the arXiv ID: it gets you the LaTeX source,")
        print("the figures and sometimes the data behind the tables.")
        return 0

    arxiv_id = match.group(1)
    return fetch_arxiv(arxiv_id, label or arxiv_id.replace("/", "_"), pdf_only)


if __name__ == "__main__":
    sys.exit(main())
