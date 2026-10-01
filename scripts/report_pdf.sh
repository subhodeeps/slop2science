#!/usr/bin/env bash
# Render Markdown to LaTeX and PDF with pandoc. The Markdown is the source. The .tex and .pdf
# are generated and git-ignored (reports/*.pdf, reports/*.tex), so nobody "fixes" a document by
# editing its output.
#
#   scripts/report_pdf.sh <topic>          reports/<topic>_report.md -> reports/<topic>_report.pdf
#   scripts/report_pdf.sh <path/to/file.md> any Markdown file       -> reports/<file>.pdf
#
# Settings (environment):
#   REPORT_OUT=dir     output directory (default: reports)
#   NUMBER=1           number the sections (default: off, because many documents number by hand)
#   TOC=0              no table of contents (default: on)
#   PDF_ENGINE=name    xelatex or lualatex (default: xelatex, then lualatex)
#   REPORT_AUTHOR=text the default author. It overrides docs/author.txt. An empty value means
#                      that there is no default author.
#   META=auto|0|refresh  title and abstract that the document lacks (default: auto).
#                      auto: ask a model once, and keep the answer in <out>/<name>.meta.json.
#                      0: never ask, and ignore the saved answer. refresh: ask again.
#   METADATA_MODEL=sonnet   the model for that request (.claude/models.md). CLAUDE_BIN=claude
#
# Title, author and abstract come from a YAML header in the Markdown, and the first level-1
# heading is the title. A document without an author gets the default author of the project:
# REPORT_AUTHOR, else the first line of docs/author.txt that is not blank or a comment
# (/init-paper writes that file). For each of the title, the abstract (and the author, when
# the project has no default author) that is missing, the script asks a model, with the
# `claude` command. The text of the document goes to that model. A YAML header always wins
# over the default author and over the saved answer. The build never fails because of this step.
#
# The reader is CommonMark (commonmark_x), as on GitHub, not pandoc's own Markdown. Pandoc's
# Markdown reads a line that starts with "ML." or "CIV." inside a paragraph as a Roman-numeral
# list item and splits the paragraph. Only "1." and "-" start a list here, as on GitHub.
#
# A document with one level-1 heading, at its start, gets that heading as its title and each
# other heading moves up one level. Math uses $...$ and $$...$$ (CLAUDE.md: KaTeX style).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
arg="${1:?usage: report_pdf.sh <topic | path/to/file.md>}"
if [[ "$arg" == *.md || "$arg" == */* ]]; then
  src="$arg"; base="$(basename "${src%.md}")"
else
  src="reports/${arg}_report.md"; base="${arg}_report"
fi
out="${REPORT_OUT:-reports}"
tex="$out/$base.tex"; pdf="$out/$base.pdf"; log="$out/$base.latexmk.log"
[ -f "$src" ] || { echo "no $src" >&2; exit 66; }

command -v pandoc >/dev/null 2>&1 || { echo "pandoc not found (make check-env)" >&2; exit 127; }
engine="${PDF_ENGINE:-}"
if [ -z "$engine" ]; then
  for e in xelatex lualatex; do command -v "$e" >/dev/null 2>&1 && { engine="$e"; break; }; done
fi
[ -n "$engine" ] && command -v "$engine" >/dev/null 2>&1 \
  || { echo "no xelatex or lualatex found (make check-env). pdflatex cannot set Unicode text." >&2; exit 127; }
mkdir -p "$out"; out_abs="$(cd "$out" && pwd)"

# One level-1 heading, on the first non-blank line, outside code fences: it is the title.
h1_count="$(awk '/^```/{f=!f} !f && /^# /{n++} END{print n+0}' "$src")"
first="$(awk 'NF{print; exit}' "$src")"
shift_args=()
if [ "$h1_count" -eq 1 ] && [[ "$first" == "# "* ]]; then shift_args=(--shift-heading-level-by=-1); fi
# --- metadata: ask a model only for what the document lacks ------------------------------------
yaml_has() {                      # does a YAML header at the top of $src have the key $1?
  awk -v k="$1" 'NR==1{if ($0!="---") exit 1; next} /^(---|\.\.\.)[[:space:]]*$/{exit}
                 $0 ~ "^"k"[[:space:]]*:"{f=1} END{exit f?0:1}' "$src"
}
meta_json="$out/$base.meta.json"; meta_args=(); author_args=()
if [ -n "${REPORT_AUTHOR+x}" ]; then default_author="$REPORT_AUTHOR"
elif [ -f docs/author.txt ]; then default_author="$(grep -v '^[[:space:]]*\(#\|$\)' docs/author.txt | head -1 || true)"
else default_author=""; fi
default_author="$(printf '%s' "$default_author" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
missing=()
[ "${#shift_args[@]}" -gt 0 ] || yaml_has title || missing+=(title)
if ! yaml_has author; then
  if [ -n "$default_author" ]; then
    author_args=(--metadata="author:$default_author")
    echo "[report] author: $default_author (the default author; a YAML header in the Markdown overrides it)"
  else
    missing+=(author)
  fi
fi
yaml_has abstract || missing+=(abstract)
mode="${META:-auto}"
if [ "$mode" != 0 ] && [ "${#missing[@]}" -gt 0 ] && { [ "$mode" = refresh ] || [ ! -f "$meta_json" ]; }; then
  want="$(IFS=,; echo "${missing[*]}")"; model="${METADATA_MODEL:-sonnet}"; claude_bin="${CLAUDE_BIN:-claude}"
  if ! command -v "$claude_bin" >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1; then
    echo "[report] metadata: missing $want. No title page entry: the model step needs claude and jq."
  else
    echo "[report] metadata: missing $want. Asking $model. The text of $src goes to the model; META=0 stops this."
    system="You read one Markdown document and give the entries for its title page. Reply with one JSON object and nothing else. Use only these keys: $want. title: the title of the document, in its own words. author: a person or group that the document itself names as its author. Use null if it names none. Never guess an author. abstract: a summary of 3 to 5 sentences of what the document says, in ASD-STE100 Simplified Technical English (short active sentences, one idea in each), with no claim that the document does not make, as plain text with no Markdown headings. Use null if the document is too short to summarise."
    # The call runs in an empty folder with the project settings off. Then no project hook (the
    # prompt log, for one) records the text of the document, and no CLAUDE.md or skill loads.
    scratch="$(mktemp -d)"
    if reply="$(head -c 40000 "$src" | { cd "$scratch" && timeout 180 "$claude_bin" -p --model "$model" \
          --tools "" --setting-sources user --disable-slash-commands --no-session-persistence \
          --output-format text --max-budget-usd 0.50 --system-prompt "$system" \
          "Give the JSON object for this document." 2>"$out_abs/$base.meta.err"; })" \
       && json="$(printf '%s\n' "$reply" | sed '/^```/d' | jq -ce --arg want "$want" --arg model "$model" \
          '($want|split(",")) as $k | with_entries(select((.key|IN($k[])) and (.value|type=="string") and (.value|length>0))) | select(length>0) + {_generated_by: $model}' 2>/dev/null)" \
       && [ -n "$json" ]; then
      printf '%s\n' "$json" > "$meta_json"
      echo "[report] metadata: wrote $meta_json. A YAML header in the Markdown overrides it. Read it:"
      jq -r 'to_entries[] | select(.key|startswith("_")|not) | "[report]   \(.key): \(.value)"' "$meta_json"
    else
      echo "[report] metadata: the model gave no usable answer (see $out/$base.meta.err). The build goes on without it."
    fi
    rmdir "$scratch" 2>/dev/null || true
  fi
fi
[ "$mode" = 0 ] || [ ! -f "$meta_json" ] || meta_args=(--metadata-file="$meta_json")

opts=(--standalone --from=commonmark_x+tex_math_dollars-fancy_lists
      --pdf-engine="$engine" -V geometry:margin=1in -V colorlinks=true -V fontsize=11pt
      --resource-path=".:$(dirname "$src")" -H scripts/pandoc/report_header.tex
      --lua-filter=scripts/pandoc/html_images.lua
      --lua-filter=scripts/pandoc/prefer_vector_images.lua
      --lua-filter=scripts/pandoc/break_table_code.lua
      --lua-filter=scripts/pandoc/fit_display_math.lua
      --lua-filter=scripts/pandoc/fit_code_blocks.lua)
[ "${TOC:-1}" = "0" ] || opts+=(--toc)
[ "${NUMBER:-0}" = "1" ] && opts+=(--number-sections)

echo "[report] pandoc: $src -> $tex"
pandoc "$src" ${shift_args[@]+"${shift_args[@]}"} ${meta_args[@]+"${meta_args[@]}"} \
  ${author_args[@]+"${author_args[@]}"} "${opts[@]}" -o "$tex"

echo "[report] $engine: $tex -> $pdf"
if command -v latexmk >/dev/null 2>&1; then
  flag=-pdfxe; [ "$engine" = lualatex ] && flag=-pdflua
  latexmk -g "$flag" -interaction=nonstopmode -halt-on-error -output-directory="$out" "$tex" >"$log" 2>&1 \
    || { echo "latexmk FAILED - see $log" >&2; tail -30 "$log" >&2; exit 1; }
else                                   # no latexmk: two passes settle the table of contents
  for _ in 1 2; do
    "$engine" -interaction=nonstopmode -halt-on-error -output-directory="$out" "$tex" >"$log" 2>&1 \
      || { echo "$engine FAILED - see $log" >&2; tail -30 "$log" >&2; exit 1; }
  done
fi
[ -f "$pdf" ] || { echo "[report] FAILED: $pdf was not produced" >&2; exit 1; }
pages=""; command -v pdfinfo >/dev/null 2>&1 && pages="$(pdfinfo "$pdf" | awk '/^Pages/{print $2}')"
echo "[report] wrote $pdf${pages:+ ($pages pages)} (engine: $engine)"
