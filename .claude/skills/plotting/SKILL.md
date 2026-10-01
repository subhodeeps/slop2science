---
name: plotting
description: Make each matplotlib figure in amore, the plot style of this project. The style has LaTeX labels, muted blue, green and red palettes, a heavy frame, shaded bands with monospace labels, insets and contour colour maps. Use it each time you make or change a figure.
when_to_use: 'Trigger phrases: plot, figure, matplotlib, make a figure, graph, inset, contour, colour map, shaded region, colour, color, palette, regenerate the figure'
paths:
  - "src/**"
  - "validation/**"
  - "reports/**"
---

# Plotting

The plot style `amore` is in `src/python/amore/`:

- `amore.mplstyle` sets the fonts, the colour cycle, the frame, the ticks and the grid.
- `__init__.py` adds the named palettes and the helpers `use`, `palette`, `cmap`,
  `diverging`, `shade`, `inset`, `tag` and `save`.
- `examples.py` makes the three example figures in `README.md` (`make plot-examples`). Read it
  before you make your first figure.

## Rules

1. Import `amore` and call `amore.use()` before you make a figure. Do not set the fonts, the
   frame width, the tick direction or the grid by hand. The style owns them.
2. Take each colour from `amore.palette("blue")`, `amore.palette("green")` or
   `amore.palette("red")`. Each palette has four tones:
   - `ink` for a reference or an exact curve
   - `main` for the computed result
   - `light` for a fill
   - `shade` for a background band
3. For a contour plot or an image, use `amore.cmap(name)`. For a signed field, use
   `amore.diverging("red", "green")` with `vmin = -vmax`, so that zero is at the centre.
4. Draw a line on top of a colour map (flow lines, guides) in `amore.OVERLAY` at
   `amore.OVERLAY_ALPHA`. This is a dark neutral grey. White vanishes on the light centre of a
   map. Black competes with the contour lines. A coloured line looks like a quantity.
5. Use one palette for one family of figures. Then one quantity has one colour in the whole
   document.
6. Write each axis label, legend entry and mathematical symbol in LaTeX. Write a text note
   inside the axes in monospace. `amore.shade(ax, x0, x1, "label")` does this, or use
   `\texttt{...}`.
7. Mark a region with `amore.shade()`. Show a detail with `amore.inset()`. Put a status line,
   for example the figure that you reproduce, with `amore.tag()`.
8. Save with `amore.save(fig, path)`. It writes a PDF for the paper and a PNG for review, side
   by side.
9. A script makes each figure from the records (CLAUDE.md §10). Never edit a figure by hand.

## Look at the figure before you call it done

Read the PNG. Look for these faults:

- a label or an annotation that touches a curve
- an inset that hides data, a label or the legend
- tick labels that overlap
- a legend on top of data
- a marker that is not at the point that it marks
- a colour that is not in a palette

Fix each fault and render again. A figure that you did not look at is not finished.

## How the project enforces this

- `make check` runs `scripts/check_plots.py`. It fails if a Python file imports matplotlib and
  does not call `amore.use()`, or if it hard-codes a hex colour. CI runs it on each push.
- The `implementation` agent loads this skill in its frontmatter. A main session loads it when
  the task matches its description or when the work touches `src/`, `validation/` or
  `reports/`.
- The check reads source text only. It cannot see a figure that looks wrong. That is why you
  must read the PNG.

## Requirement

The style uses LaTeX for all text, so it needs `latex` and `dvipng` (and the `type1cm`,
`cm-super` and `amsmath` TeX packages). `make check-env` reports them. If they are missing,
stop and tell the PI. Do not switch off LaTeX to get a figure, because then the figure does not
match the document.

## Credit

The Physical Review style sheet of
[hosilva/physrev_mplstyle](https://github.com/hosilva/physrev_mplstyle) inspired this style. That repository has no
licence file, so this template does not copy its file. `amore.mplstyle` is an independent file.
