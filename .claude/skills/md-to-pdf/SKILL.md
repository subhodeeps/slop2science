---
name: md-to-pdf
description: Convert a Markdown document to LaTeX and PDF with pandoc. The Markdown is the source. The output goes to reports/. Use it when the person wants a document in LaTeX or PDF, for a report, a README, notes or an appendix. It converts. It does not write the document.
when_to_use: 'Trigger phrases: make a PDF, convert to PDF, convert to LaTeX, give me the .tex, render the report, pdf of the readme, LaTeX version, pandoc, make report, title page, abstract'
allowed-tools: Bash(scripts/report_pdf.sh *) Bash(make report *) Bash(make test-report) Bash(make check-env) Bash(pdftoppm *) Bash(pdfinfo *)
---

# Markdown to LaTeX and PDF

`scripts/report_pdf.sh` reads one Markdown file. It writes `reports/<name>.tex` and
`reports/<name>.pdf`. Git ignores both. The Markdown is the source of the document.

This skill converts a document that exists. To write a report, use `report-writing` first.

## Run it

    make report TOPIC=<topic>                 reports/<topic>_report.md
    make report FILE=README.md                any Markdown file, output in reports/README.pdf
    make report FILE=docs/notes.md NUMBER=1   number the sections

`scripts/report_pdf.sh <topic | path.md>` does the same without `make`. Set these as
environment variables:

- `REPORT_OUT=dir`: the output folder.
- `NUMBER=1`: number the sections. The default is off, because many documents number by hand.
- `TOC=0`: no table of contents.
- `PDF_ENGINE=lualatex`: the default is xelatex, then lualatex.
- `META`: see the next section.

## Rules

- **Never edit the `.tex` or the `.pdf`.** Fix the Markdown, then run the script again. A fix
  for the layout belongs in the pipeline (`scripts/pandoc/`), not in the Markdown.
- Commit the PDF only if the person asks. Use `git add -f`. Tell the person that a tool
  generates the file.
- Never change the words of a document to make it convert. If a sentence breaks the build,
  tell the person which sentence and why.
- The pipeline is pandoc, its Lua filters and one LaTeX engine. Add no other tool without the
  approval of the person.

## Title, author and abstract

The title page takes them from a YAML header in the Markdown. The first level-1 heading is the
title.

- **Author.** A document with no `author:` gets the default author of the project. That is
  `REPORT_AUTHOR`, or else the first line of `docs/author.txt` that is not a comment. The PI
  chooses the wording, and `/init-paper` writes the file. An empty `REPORT_AUTHOR` means no
  default author. Without one, the model reads the document for an author that it names.
- **Title and abstract.** For each one that the document lacks, the script asks a model
  (`sonnet`, set in `.claude/models.md`) with the `claude` command. The model reads the text of
  the document, so the text leaves the machine. `META=0` stops the request. The rules for the
  model: use only what the document states, and write the abstract in ASD-STE100. The call runs
  in an empty folder with the project settings off. Then no project hook (the prompt log, for
  one) records the text of the document.

- The answer is in `reports/<name>.meta.json`. Later builds read it and do not ask again.
  `META=refresh` asks again.
- A YAML header in the Markdown always wins, also over the default author. To fix an entry,
  put it in the header.
- The build never fails because of this step. Without `claude` or `jq` it skips the step.
- **Show the person the generated entries.** The abstract is text that a model wrote. The
  person must read it before the PDF goes to anyone.

## Images

Prefer PDF over PNG over JPG. The Markdown keeps the PNG, because GitHub and the VS Code preview
cannot show a PDF in an image tag. For LaTeX, `prefer_vector_images.lua` looks at each image. If a
PDF with the same name is beside it, the filter uses the PDF. The PNG is the fallback. A JPG
gives way to a PNG in the same way. Web addresses stay as they are.

So make each figure as PDF and PNG (`amore.save` writes both). `make plot-examples` makes the
PDFs of the example figures, and git ignores them.

## Look at the result

A build that succeeds can still give a bad page. After each build:

1. Read the last line of the script output. It gives the page count.
2. Make images of the pages: `pdftoppm -r 60 -png reports/<name>.pdf <scratch>/page`. Look at the
   first page, a page with a figure, a page with a table and a page with code.
3. Search the log, `reports/<name>.latexmk.log`, for `Overfull`. Each hit is a line that goes
   into the margin. Report the count.

Tell the person what you saw. Do not say "it works" because the build exited with code 0.

## Write Markdown that converts well

- Math: `$ ... $` and `$$ ... $$` only (CLAUDE.md §10a). Never `\( \)` or `\[ \]`.
- One level-1 heading, on the first line. Then the other headings move up one level. With more
  than one level-1 heading, the levels stay, and the script asks for a title.
- Images: a path from the repository root or from the folder of the file. The alt text of a
  single image becomes its caption.
- Keep code lines under 100 characters. No emoji and no symbol that the fonts lack: a missing
  character stops the build. Replace the symbol, or ask the person.

## More

`reference/pipeline.md` lists each filter and the problem that it fixes. It also has the tools to
install and the test. Read it when a build fails, when a page looks wrong or when you change a
filter.
