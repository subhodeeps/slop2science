#!/usr/bin/env bash
# Render reports/<topic>_report.md to PDF. The Markdown is the source; the PDF is generated
# and gitignored, so a report is never "fixed" by editing its output.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
topic="${1:?usage: report_pdf.sh <topic>}"
src="reports/${topic}_report.md"
[ -f "$src" ] || { echo "no $src" >&2; exit 66; }

command -v pandoc >/dev/null 2>&1 || { echo "pandoc not found (make check-env)" >&2; exit 127; }
engine=""
for e in xelatex lualatex pdflatex; do
  command -v "$e" >/dev/null 2>&1 && { engine="$e"; break; }
done
[ -n "$engine" ] || { echo "no LaTeX engine found (make check-env)" >&2; exit 127; }
# xelatex/lualatex first: prose in these reports routinely contains Unicode mathematics and
# named symbols that pdflatex's default fonts cannot set.

pandoc "$src" \
  --from=markdown+tex_math_dollars+pipe_tables+footnotes \
  --pdf-engine="$engine" \
  --toc --number-sections \
  -V geometry:margin=1in -V fontsize=11pt -V colorlinks=true \
  -o "reports/${topic}_report.pdf"
echo "wrote reports/${topic}_report.pdf (engine: $engine)"
