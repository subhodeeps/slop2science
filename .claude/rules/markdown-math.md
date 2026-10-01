---
paths:
  - "**/*.md"
---

# Mathematics in Markdown

A KaTeX-based previewer (VS Code, GitHub) displays each `.md` file in this repository. Write
mathematics for that previewer:

- Inline: `$ ... $`. Display: `$$ ... $$` on their own lines, with a blank line before and
  after.
- **Never use `\( ... \)` or `\[ ... \]`.** KaTeX does not render them. The reader sees literal
  backslashes and brackets.
- Escape a literal dollar sign as `\$`.
- KaTeX supports a subset of LaTeX. It has no `\label`, `\ref`, `\eqref` or `\newcommand`. For a
  multi-line display, use `aligned` inside `$$ ... $$`. Do not use `align` or `equation`.
- Put the equation numbers of the source paper in prose ("Eq. (23)"). Never use LaTeX
  numbering. The numbering would belong to this document, and the reference is to the source.
- Define each symbol at its first use. Use one notation in a whole document, also if the
  sources that it uses differ. State the conversions where they matter.

In `.tex` files (a manuscript, an appendix), use normal LaTeX delimiters. This rule applies to
the Markdown that a previewer displays.
