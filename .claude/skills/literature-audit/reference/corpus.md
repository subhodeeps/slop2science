# Building a corpus for a source — source formats first

## The reading order, stated once

Read from the best form that exists, in this order, and say which one you used:

1. the **`.tex` source** — equations, table bodies, the authors' macros;
2. a **data file** shipped with the source — a table's real numbers;
3. a **figure file** from the source — a curve;
4. the **rendered PDF, as page images** — when there is no source, and for the jobs a `.tex`
   cannot do (below);
5. the **PDF text layer or OCR** — last resort, and never for an equation.

**This file is the one place that order is stated.** Every other file that tells you how to
read a paper points here rather than restating it, and `make test-checks` fails if one
mentions reading a rendered page without doing so. Restating it is how nine files came to say
"read the rendered page" with no mention of the source.

## The hierarchy, best to worst

| Form | Why |
|---|---|
| **LaTeX source** (arXiv tarball) | what the authors actually wrote — the equation, not a rendering of it. Macros, labels, and a `.bbl` with identifiers already resolved |
| **Author-supplied data** (`.dat`, `.csv` in the tarball) | a table's real numbers, with provenance. Beats any digit read off a plot |
| **Figure source** (`.pdf`, `.eps`, `.pgf` in the tarball) | vector figures; `.eps` and PGF are text, so a curve's numbers are sometimes literally in the file |
| **Rendered PDF, read as page images** | correct but slow. The only form for a PDF-only or pre-arXiv paper, and still the way to see printed equation numbers and what a reader sees |
| **PDF text layer / OCR** | **a reconstruction, and for older documents a lossy one.** Last resort, and never for an equation |

    make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>

fetches the e-print tarball **and** the PDF, extracts the source to `papers/source/<id>/`, and
reports what it found by category — flagging it when the submission ships data files.

## Why not just read the PDF

PDF extraction reorders nested structure silently and confidently. Ligatures vanish, a
fraction becomes two adjacent tokens, a stacked sub/superscript loses which is which, table
columns interleave — and the result reads as perfectly plausible prose. The three most
expensive documentation errors in the project this template came from all traced to exactly
this (`docs/failure_modes.md` entry 2), and the LaTeX source would have made two of them
impossible.

So:

- **equations** — read the `.tex`. With no source, read the **rendered page image**; never
  the text layer.
- **tables and numbers** — prefer a shipped data file, then the `.tex` table body, then the
  rendered page. Transcribe to the printed precision; never round, extend or recompute.
- **figures** — use the figure file from the tarball. If a number must come off a plot, say
  so and state the read precision: a digitized value is a much weaker benchmark than a
  tabulated one and must never be reported as tabulated.

## What the rendered page is still for, when a source exists

Narrowly, and never as the origin of an equation's content:

- **Printed equation numbers.** A `.tex` has `\label`s; the numbers are assigned when it
  compiles, and the audit records printed numbers because "Eq. (9)" is what anyone citing the
  paper means. Read the label from the `.tex`, the number from the page.
- **Is this the version being audited?** The source is one arXiv version's, the PDF another's,
  and the journal's a third. Fetch with an explicit version (`make fetch-source ID=<id>v2`)
  and check the page agrees.
- **What the reader sees**: layout, what a figure plots, what a table's columns are called.

**If the `.tex` and the page disagree about an equation, that is a discrepancy.** Record it in
the five-point form (CLAUDE.md §3). Do not pick whichever reads better: the `.tex` can carry
commented-out text, conditional blocks or an earlier draft's equation, and the page is what
was published.

## Pin the version

An undated corpus becomes untrustworthy. Record in `papers/sources.yaml`, every time:

- the exact version consulted (`v2`, or the journal version) — they differ, sometimes in the
  equation this project depends on;
- the date fetched;
- for the source tree, which file an equation came from
  (`papers/source/<id>/ms.tex`, at `\label{eq:master}`).

Cite the file and the label, not "the paper's Eq. (9)" alone, wherever a write-up leans on
something read out of the source tree.

## Author macros

A paper's own macros (`\newcommand{\calJ}{\mathcal{J}}`) are in the tarball — in the preamble
or a `.sty`. **Resolve them before transcribing an equation.** A macro that hides a sign or a
factor is an easy and invisible way to transcribe an equation wrongly. Record the expansion
next to the transcription.

## What not to do

- Do not build a corpus speculatively. Fetch against a stated need; a citation in the
  source's bibliography is not by itself a reason to fetch it.
- Do not read a `.tex` and report the rendered meaning without checking the macros.
- Do not treat the source tree as a substitute for the audit. `papers/source/` is input;
  `docs/<topic>_source_audit.md` is the record.
