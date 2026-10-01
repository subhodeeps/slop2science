# The conversion pipeline

The script is `scripts/report_pdf.sh`. The filters and the LaTeX header are in `scripts/pandoc/`.

## What the pipeline fixes

| Problem in the conversion | Filter or file | Effect |
|---|---|---|
| Pandoc drops raw HTML, so `<img>` figures vanish | `html_images.lua` | each `<img>` becomes an image, and `<p align="center">` centres it |
| A PNG where a PDF exists | `prefer_vector_images.lua` | the PDF is used |
| Long paths in tables and code spans overflow | `break_table_code.lua` | break points, and column widths from the content |
| Long display equations overflow | `fit_display_math.lua` | a list of results becomes a stack, and a wide display shrinks |
| Code lines wrap with an arrow | `fit_code_blocks.lua` | the block gets the largest font that fits |
| A missing glyph vanishes in silence | `report_header.tex` | a missing character stops the build |

The reader is CommonMark (`commonmark_x`), as on GitHub. Pandoc's own Markdown reads a line that
starts with `ML.` as a Roman-numeral list item and splits the paragraph.


## Tools and test

Needed: `pandoc`, and `xelatex` or `lualatex`. Optional: `latexmk`, `pdfinfo` and, for the
title page step, `claude` and `jq`. `make check-env` shows what is present. On Debian or Ubuntu:

    apt-get install pandoc texlive-xetex texlive-latex-extra texlive-fonts-recommended \
        lmodern latexmk fonts-dejavu-core poppler-utils jq

For lualatex also install `texlive-luatex`. A build that stops with `File '<name>.sty' not found`
needs the package that owns that file. `make test-report` tests the pipeline with `README.md`,
a fixture and a fake model. It prints a loud SKIP without pandoc or LaTeX, and it is not part of
`make check`. When you change a filter, add a case to `scripts/test_report.sh` in the same commit.
