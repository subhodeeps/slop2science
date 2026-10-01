# Build a corpus for a source — source formats first

## The reading order, stated once

Read the best form that exists, in this order. State which form you used:

1. the **`.tex` source**: the equations, the table bodies and the macros of the authors
2. a **data file** that ships with the source: the real numbers of a table
3. a **figure file** from the source: a curve
4. the **rendered PDF, as page images**: use it when there is no source, and for the jobs that a
   `.tex` file cannot do (below)
5. the **PDF text layer or OCR**: the last resort. Never use it for an equation.

**This file is the only place that states this order.** Each other file that tells you how to
read a paper points here. It does not restate the order. `make test-checks` fails if a file
mentions the reading of a rendered page without a pointer here. A restated order is the reason
why nine files said "read the rendered page" with no mention of the source.

## The hierarchy, from best to worst

| Form | Why |
|---|---|
| **LaTeX source** (arXiv tarball) | It is what the authors wrote: the equation, not a rendering of it. It has the macros, the labels, and a `.bbl` with resolved identifiers. |
| **Data from the author** (`.dat`, `.csv` in the tarball) | The real numbers of a table, with provenance. It is better than any digit that you read from a plot. |
| **Figure source** (`.pdf`, `.eps`, `.pgf` in the tarball) | Vector figures. `.eps` and PGF are text, so the numbers of a curve are sometimes in the file. |
| **Rendered PDF, read as page images** | It is correct but slow. It is the only form for a paper that only exists as a PDF, or for a paper from before arXiv. It is also the way to see printed equation numbers and what a reader sees. |
| **PDF text layer / OCR** | **A reconstruction. For older documents it loses information.** It is the last resort. Never use it for an equation. |

    make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>

This command fetches the e-print tarball **and** the PDF. It extracts the source to
`papers/source/<id>/`. It reports what it found, by category. It flags a submission that ships
data files.

## Why not only read the PDF

PDF extraction reorders nested structure silently and with confidence. Ligatures disappear. A
fraction becomes two adjacent tokens. A stacked subscript and superscript lose their order.
Table columns interleave. The result reads as plausible prose. The three most expensive
documentation errors in the project that this template came from all had this cause
(`docs/failure_modes.md` entry 2). The LaTeX source would have made two of them impossible.

Therefore:

- **Equations.** Read the `.tex` file. If there is no source, read the **rendered page image**.
  Never read the text layer.
- **Tables and numbers.** Prefer a shipped data file. Then use the `.tex` table body. Then use
  the rendered page. Transcribe to the printed precision. Never round, extend or recompute.
- **Figures.** Use the figure file from the tarball. If you must take a number from a plot, say
  so and state the precision of your reading. A digitized value is a much weaker benchmark than a
  tabulated value. Never report it as tabulated.

## What the rendered page is still for, when a source exists

The page has a narrow job. It is never the origin of the content of an equation:

- **Printed equation numbers.** A `.tex` file has `\label` commands. The numbers appear when the
  file compiles. The audit records printed numbers, because "Eq. (9)" is what anyone who cites
  the paper means. Read the label from the `.tex` file and the number from the page.
- **The version.** Is this the version that you audit? The source belongs to one arXiv version.
  The PDF can belong to another version. The journal has a third version. Fetch with an explicit
  version (`make fetch-source ID=<id>v2`). Check that the page agrees.
- **What the reader sees.** This includes the layout, what a figure plots and the names of the
  columns of a table.

**If the `.tex` and the page disagree about an equation, that is a discrepancy.** Record it in
the five-item form (CLAUDE.md §3). Do not pick the version that reads better. The `.tex` can
contain commented-out text, conditional blocks or an equation from an earlier draft. The page is
what the publisher published.

## Pin the version

A corpus without dates becomes untrustworthy. Each time, record these items in
`papers/sources.yaml`:

- the exact version that you consulted (`v2`, or the journal version). They differ, sometimes in
  the equation that this project depends on
- the date of the fetch
- for the source tree, the file that an equation came from (`papers/source/<id>/ms.tex`, at
  `\label{eq:master}`)

Cite the file and the label. Do not cite only "Eq. (9) of the paper" where a write-up depends
on something that you read out of the source tree.

## Macros of the authors

The paper has its own macros (`\newcommand{\calJ}{\mathcal{J}}`). They are in the tarball, in the
preamble or in a `.sty` file. **Resolve them before you transcribe an equation.** A macro that
hides a sign or a factor is an easy and invisible way to transcribe an equation wrongly. Record
the expansion next to the transcription.

## What to not do

- Do not build a corpus speculatively. Fetch against a stated need. A citation in the
  bibliography of the source is not a reason to fetch it.
- Do not read a `.tex` file and report the rendered meaning without a check of the macros.
- Do not use the source tree in place of the audit. `papers/source/` is input.
  `docs/<topic>_source_audit.md` is the record.
