#!/usr/bin/env bash
# Run one language's tests, or report clearly that its toolchain is absent.
#
#   scripts/run_tests.sh julia|python
#
# Absent toolchain is a skip, not a failure: `make test` must be runnable on a machine that
# has only one of the project's languages, and in a cloud container that has none. A skip is
# printed loudly so it is never mistaken for a pass.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
lang="${1:?usage: run_tests.sh julia|python}"

case "$lang" in
  julia)
    if ! command -v "${JULIA:-julia}" >/dev/null 2>&1; then
      echo "[test] SKIP julia: not installed (docs/toolchain.md)"; exit 0; fi
    [ -f tests/julia/runtests.jl ] || { echo "[test] SKIP julia: no tests/julia/runtests.jl"; exit 0; }
    "${JULIA:-julia}" --project=src/julia --threads=auto tests/julia/runtests.jl ;;
  python)
    if [ -f src/python/pyproject.toml ] && [ -z "${PYTHON:-}" ]; then
      command -v uv >/dev/null 2>&1 || { echo "[test] SKIP python: uv not installed (make setup)"; exit 0; }
      [ -d src/python/.venv ] || { echo "[test] SKIP python: no environment yet (make setup)"; exit 0; }
      uv run --project src/python pytest -q tests/python
    else
      scripts/py -c '' >/dev/null 2>&1 || { echo "[test] SKIP python: no interpreter (docs/toolchain.md)"; exit 0; }
      scripts/py -c 'import pytest' >/dev/null 2>&1 || { echo "[test] SKIP python: pytest not installed"; exit 0; }
      scripts/py -m pytest -q tests/python
    fi ;;
  *) echo "unknown language: $lang" >&2; exit 64 ;;
esac
