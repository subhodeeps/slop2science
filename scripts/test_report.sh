#!/usr/bin/env bash
# Test the Markdown -> LaTeX -> PDF pipeline (scripts/report_pdf.sh) on this repository's own
# README.md and on a small fixture. It needs pandoc and xelatex (or lualatex). Without them the
# test prints a loud SKIP and exits 0: it is not part of `make check`, which needs no toolchain.
# What it pins:
#   - the README renders to a PDF with pages in it;
#   - each <img> of the README is in the LaTeX (pandoc drops raw HTML unless html_images.lua runs);
#   - a line that starts with "ML." stays inside its paragraph (no Roman-numeral list);
#   - a code block with a long line gets a smaller font, and one with short lines does not;
#   - a document with one level-1 heading gets that heading as its title;
#   - a glyph that no font has fails the build, not the PDF (tracinglostchars);
#   - an image uses its PDF when one is beside it (PDF over PNG over JPG), else the named file;
#   - a missing title, author or abstract is asked of a model once (a fake one here), the answer
#     is saved, a YAML header wins over it, and a failing or absent model never fails the build;
#   - that model call runs in an empty folder with the project settings off, so no project hook
#     (the prompt log, for one) records the text of the document.
set -uo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SRC"
command -v pandoc >/dev/null 2>&1 && { command -v xelatex >/dev/null 2>&1 || command -v lualatex >/dev/null 2>&1; } \
  || { echo "report-test: SKIP (needs pandoc and xelatex or lualatex; run make check-env)"; exit 0; }
pass=0; fail=0
ok()  { pass=$((pass+1)); printf '  ok   %s\n' "$1"; }
bad() { fail=$((fail+1)); printf '  FAIL %s\n' "$1"; }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
export REPORT_OUT="$W"
export META=0                     # no test calls a real model; the metadata tests use a fake one

echo "report-test: README.md"
check "README renders to a PDF" 'scripts/report_pdf.sh README.md >"$W/readme.out" 2>&1 && [ -s "$W/README.pdf" ]'
check "the PDF has pages" '[ "$(pdfinfo "$W/README.pdf" 2>/dev/null | awk "/^Pages/{print \$2}")" -ge 1 ] 2>/dev/null \
  || [ -s "$W/README.pdf" ]'
want="$(grep -c '<img ' README.md)"; got="$(grep -c '^\\includegraphics' "$W/README.tex" 2>/dev/null)"
check "every README image is in the LaTeX ($got of $want)" '[ "$want" -ge 1 ] && [ "$got" -eq "$want" ]'
check "the README title is the document title" 'grep -q "\\\\title{" "$W/README.tex"'

echo "report-test: fixture"
cat > "$W/fix.md" <<'F'
# Fixture title

- one two plotting and
  ML. then more text

Inline math $a+b$ and a display:

$$
\int_0^1 x\,dx = \tfrac12
$$

```text
short line
```

```text
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
```
F
check "the fixture renders" 'scripts/report_pdf.sh "$W/fix.md" >"$W/fix.out" 2>&1 && [ -s "$W/fix.pdf" ]'
check "a line that starts with ML. stays in its paragraph" '! grep -q "begin{enumerate}" "$W/fix.tex"'
check "a long code line gets a smaller font" 'grep -q "begingroup.footnotesize\|begingroup.scriptsize" "$W/fix.tex"'
check "a short code block keeps the body size" '[ "$(grep -c "begingroup" "$W/fix.tex")" -eq 1 ]'
check "one level-1 heading becomes the title" 'grep -q "title{Fixture title}" "$W/fix.tex"'

printf '# T\n\nA glyph that no font has: \xf0\x9f\xa7\xbf\n' > "$W/lost.md"
check "a glyph with no font fails the build" '! scripts/report_pdf.sh "$W/lost.md" >"$W/lost.out" 2>&1'

echo "report-test: images"
mkdir -p "$W/img" && : > "$W/img/a.png" && : > "$W/img/a.pdf" && : > "$W/img/b.png" \
  && : > "$W/img/c.jpg" && : > "$W/img/c.png"
printf '![a](img/a.png) ![b](img/b.png) ![c](img/c.jpg) ![web](https://example.org/w.png)\n' > "$W/img.md"
pandoc "$W/img.md" -f commonmark_x -t latex --resource-path="$W" \
  --lua-filter=scripts/pandoc/prefer_vector_images.lua > "$W/img.tex" 2>/dev/null
check "a PNG with a PDF beside it becomes the PDF"        'grep -q "img/a.pdf" "$W/img.tex"'
check "a PNG with no PDF stays a PNG"                     'grep -q "img/b.png" "$W/img.tex"'
check "a JPG with a PNG beside it becomes the PNG"        'grep -q "img/c.png" "$W/img.tex" && ! grep -q "img/c.jpg" "$W/img.tex"'
check "a web address is not changed"                      'grep -q "https://example.org/w.png" "$W/img.tex"'
check "the README names PNG files, which GitHub can show" '! grep -q "figures/[a-z_]*\.pdf" README.md'

echo "report-test: metadata (a fake model)"
mkdir -p "$W/bin"
cat > "$W/bin/claude" <<'F'
#!/usr/bin/env bash
cat >/dev/null; echo x >> "$CALLS"; pwd > "$CALLS.cwd"; echo "$*" > "$CALLS.args"
if [ -n "${FAKE_FAIL:-}" ]; then exit 1; fi
printf '```json\n{"title":"Fake Title","author":null,"abstract":"Fake abstract sentence."}\n```\n'
F
chmod +x "$W/bin/claude"; export CALLS="$W/calls"
printf '## First part\n\nText.\n\n## Second part\n\nMore text.\n' > "$W/bare.md"
meta() { META="${META_MODE:-auto}" CLAUDE_BIN="$W/bin/claude" scripts/report_pdf.sh "$@" >"$W/meta.out" 2>&1; }
check "a bare document gets the title and the abstract"  'meta "$W/bare.md" && grep -q "title{Fake Title}" "$W/bare.tex" && grep -q "Fake abstract sentence" "$W/bare.tex"'
check "the model call runs outside the repository"        '[ "$(cat "$CALLS.cwd")" != "$SRC" ] && [ "$(cat "$CALLS.cwd")" != "$W" ]'
check "the model call has the project settings off"       'grep -q -- "--setting-sources user" "$CALLS.args" && grep -q -- "--tools" "$CALLS.args"'
check "the model call leaves no prompt capture in the repo" '[ -z "$(git status --short docs/prompts 2>/dev/null)" ]'
check "a null author stays empty"                        '! grep -q "author{.\+}" "$W/bare.tex"'
check "the answer is saved with the model that wrote it" 'jq -e "._generated_by == \"sonnet\"" "$W/bare.meta.json" >/dev/null'
check "a second build does not ask again"                'n1="$(wc -l < "$CALLS")"; meta "$W/bare.md"; [ "$(wc -l < "$CALLS")" -eq "$n1" ]'
check "META=refresh asks again"                          'n1="$(wc -l < "$CALLS")"; META_MODE=refresh meta "$W/bare.md"; [ "$(wc -l < "$CALLS")" -gt "$n1" ]'
printf -- '---\ntitle: Own Title\nauthor: Own Author\nabstract: Own abstract.\n---\n\n## Part\n\nText.\n' > "$W/own.md"
check "a document with all three entries asks no model"  'n1="$(wc -l < "$CALLS")"; meta "$W/own.md"; [ "$(wc -l < "$CALLS")" -eq "$n1" ] && grep -q "title{Own Title}" "$W/own.tex"'
printf -- '---\ntitle: Own Title\n---\n\n## Part\n\nText.\n' > "$W/part.md"
check "a YAML title wins over the saved answer"          'cp "$W/bare.meta.json" "$W/part.meta.json"; meta "$W/part.md" && grep -q "title{Own Title}" "$W/part.tex" && ! grep -q "Fake Title" "$W/part.tex"'
check "a failing model does not fail the build"          'rm -f "$W/bare.meta.json"; FAKE_FAIL=1 meta "$W/bare.md" && [ -s "$W/bare.pdf" ] && grep -q "no usable answer" "$W/meta.out"'
check "no claude command: the build goes on, with a note" 'rm -f "$W/bare.meta.json"; META=auto CLAUDE_BIN=/nonexistent scripts/report_pdf.sh "$W/bare.md" >"$W/meta.out" 2>&1 && grep -q "needs claude and jq" "$W/meta.out"'
check "META=0 never asks"                                'n1="$(wc -l < "$CALLS")"; META=0 CLAUDE_BIN="$W/bin/claude" scripts/report_pdf.sh "$W/bare.md" >/dev/null 2>&1; [ "$(wc -l < "$CALLS")" -eq "$n1" ]'

echo "report-test: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
