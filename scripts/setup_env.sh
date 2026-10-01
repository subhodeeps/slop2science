#!/usr/bin/env bash
# Create or instantiate whichever language environments are present. Idempotent.
#   Julia   : src/julia/Project.toml + Manifest.toml          (Pkg.instantiate)
#   Python  : src/python/pyproject.toml + uv.lock, a venv at src/python/.venv  (uv sync)
# The libraries each environment carries are the PI's list in src/<lang>/packages.txt, applied
# here; the environment files are the record afterwards.
# A language this project does not use has no src/<lang>/ directory and is skipped.
set -uo pipefail
libs() { # file -> package names, comments and blanks removed
  [ -f "$1" ] && sed 's/#.*//' "$1" | awk 'NF {print $1}'
}
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ -f src/julia/Project.toml ] && grep -q '{{' src/julia/Project.toml; then
  echo "=== julia: skipped (src/julia/Project.toml still has placeholders: run /init-paper)"
elif command -v "${JULIA:-julia}" >/dev/null 2>&1 && [ -f src/julia/Project.toml ]; then
  echo "=== julia: instantiate src/julia (writes Manifest.toml -- commit it)"
  jl=$(libs src/julia/packages.txt | tr '\n' ' ')
  if [ -n "$jl" ]; then
    echo "    adding from src/julia/packages.txt: $jl"
    # shellcheck disable=SC2086
    "${JULIA:-julia}" --project=src/julia -e 'using Pkg; Pkg.add(ARGS)' $jl
  fi
  "${JULIA:-julia}" --project=src/julia -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'
else
  echo "=== julia: skipped (not installed, or src/julia/Project.toml absent)"
fi

if [ -f src/python/pyproject.toml ] && grep -q '{{' src/python/pyproject.toml; then
  echo "=== python: skipped (src/python/pyproject.toml still has placeholders: run /init-paper)"
elif [ -f src/python/pyproject.toml ]; then
  if command -v uv >/dev/null 2>&1; then
    echo "=== python: uv sync src/python (creates src/python/.venv, writes uv.lock -- commit it)"
    uv sync --project src/python || echo "    (uv sync failed -- see the message above)"
    py=$(libs src/python/packages.txt | tr '\n' ' ')
    if [ -n "$py" ]; then
      echo "    adding from src/python/packages.txt: $py"
      # shellcheck disable=SC2086
      uv add --project src/python $py || echo "    (uv add failed -- see the message above)"
    fi
  else
    echo "=== python: skipped -- uv not found. Install it (https://docs.astral.sh/uv/) and re-run"
    echo "    make setup. The project environment is deliberately not built with bare pip: that"
    echo "    would install into whichever interpreter happens to be first on PATH."
  fi
else
  echo "=== python: skipped (src/python/pyproject.toml absent)"
fi

echo "=== mathematica: nothing to instantiate; shared code lives in symbolic/common/"
echo
echo "Now run: make check-env && make check && make test"
