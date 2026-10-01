#!/usr/bin/env bash
# Report the local toolchain. Reports only by default and exits 0 even when nothing is
# installed: "no scientific tools here" is the *expected* answer in a cloud container or in
# CI, and a target that fails there trains everyone to ignore it. Use --strict to fail when a
# tool the ownership registry actually depends on is missing.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
strict=0; [ "${1:-}" = "--strict" ] && strict=1
missing=0
say() { printf '%-24s %s\n' "$1" "$2"; }

echo "--- scientific tools ---"
WS="${WOLFRAMSCRIPT:-wolframscript}"
if command -v "$WS" >/dev/null 2>&1; then
  say "wolframscript" "$(command -v "$WS")"
  if out=$(timeout 120 "$WS" -code 'Print[$Version]; Print["LicenseID: ", $LicenseID]; Print["MaxLicenseProcesses: ", $MaxLicenseProcesses]' 2>&1); then
    echo "$out" | sed 's/^/  wl: /'
  else
    say "wolframscript" "FOUND BUT FAILED TO RUN: $out"; missing=$((missing+1))
  fi
else
  say "wolframscript" "not found (set WOLFRAMSCRIPT=/path/to/wolframscript)"; missing=$((missing+1))
fi

if command -v "${JULIA:-julia}" >/dev/null 2>&1; then
  say "julia" "$(command -v "${JULIA:-julia}")"
  say "julia version" "$("${JULIA:-julia}" --startup-file=no -e 'print(VERSION)' 2>&1)"
  [ -f src/julia/Manifest.toml ] && say "julia Manifest.toml" "present" \
    || say "julia Manifest.toml" "missing -> run: make setup"
else
  say "julia" "not found"; missing=$((missing+1))
fi

if scripts/py -c '' >/dev/null 2>&1; then
  say "python (system)" "$(scripts/py -c 'import sys; print(sys.executable)')"
  say "python (system) version" "$(scripts/py -c 'import sys; print(sys.version.split()[0])')"
else
  say "python" "not found"; missing=$((missing+1))
fi

if [ -f src/python/pyproject.toml ]; then
  if command -v uv >/dev/null 2>&1; then
    say "uv" "$(uv --version)"
    [ -d src/python/.venv ] && say "python env" "src/python/.venv present" \
      || say "python env" "not built -> make setup"
    [ -f src/python/uv.lock ] && say "python uv.lock" "present" \
      || say "python uv.lock" "missing -> run: make setup, then commit it"
  else
    say "uv" "not found: the Python project environment is built with uv (docs.astral.sh/uv)"
  fi
fi

echo
echo "--- helper tools ---"
for t in git make timeout flock jq pandoc xelatex latexmk; do
  command -v "$t" >/dev/null 2>&1 && say "$t" "ok" || say "$t" "missing"
done
echo "  (pandoc + xelatex are needed only for: make report)"
for t in latex dvipng; do
  command -v "$t" >/dev/null 2>&1 && say "$t" "ok" || say "$t" "missing"
done
echo "  (latex + dvipng are needed for every figure in the amore plot style: src/python/amore/)"

echo
echo "--- local reference libraries (read-only) ---"
"$ROOT/scripts/py" "$ROOT/scripts/library.py" status 2>/dev/null \
  || echo "  scripts/library.py unavailable"

echo
echo "--- ownership registry ---"
if grep -q '{{' docs/toolchain.md 2>/dev/null; then
  echo "  docs/toolchain.md still has placeholders: run /init-paper"
else
  sed -n '/<!-- REGISTRY-START -->/,/<!-- REGISTRY-END -->/p' docs/toolchain.md 2>/dev/null \
    | grep -E '^\|' | sed 's/^/  /' || echo "  (no registry rows yet)"
fi

echo
if [ "$missing" -eq 0 ]; then
  echo "toolchain: all three present"
else
  echo "toolchain: $missing of 3 not available here (fine unless a topic you are about to work on is owned by one of them)"
fi
[ "$strict" -eq 1 ] && exit "$missing"
exit 0
