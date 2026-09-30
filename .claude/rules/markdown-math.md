---
paths:
  - "**/*.md"
---

# Mathematics in Markdown

Every `.md` file in this repository is read in a KaTeX-based previewer (VS Code, GitHub).
Write maths accordingly:

- Inline: `$ ... $`. Display: `$$ ... $$` on their own lines, blank line before and after.
- **Never `\( ... \)` or `\[ ... \]`** — KaTeX does not render them, and they appear to the
  reader as literal backslashes and brackets.
- Escape a literal dollar sign as `\$`.
- KaTeX supports a subset of LaTeX: no `\label`, `\ref`, `\eqref` or `\newcommand`. For a
  multi-line display use `aligned` inside `$$ ... $$`, not `align` or `equation`.
- Source-paper equation numbers go in prose ("Eq. (23)"), never as LaTeX numbering — the
  numbering would be this document's, and the reference is to the source's.
- Define every symbol at first use, and use one notation throughout a document even where the
  sources it draws on differ. State the conversions where they matter.

In `.tex` files (a manuscript, an appendix) use normal LaTeX delimiters instead; this rule is
about the Markdown that is read in a previewer.
