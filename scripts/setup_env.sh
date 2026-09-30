#!/usr/bin/env bash
# Create or instantiate whichever language environments are present. Idempotent.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if command -v "${JULIA:-julia}" >/dev/null 2>&1 && [ -f src/julia/Project.toml ]; then
  echo "=== julia: instantiate src/julia (writes Manifest.toml -- commit it)"
  "${JULIA:-julia}" --project=src/julia -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'
else
  echo "=== julia: skipped (not installed, or src/julia/Project.toml absent)"
fi

if scripts/py -c '' >/dev/null 2>&1 && [ -f src/python/pyproject.toml ]; then
  echo "=== python: install src/python in editable mode with dev extras"
  scripts/py -m pip install -e 'src/python[dev]' || \
    echo "    (pip install failed -- if you use uv/conda, install src/python[dev] your own way)"
else
  echo "=== python: skipped (no interpreter, or src/python/pyproject.toml absent)"
fi

echo "=== mathematica: nothing to instantiate; shared code lives in symbolic/common/"
echo
echo "Now run: make check-env && make check && make test"
