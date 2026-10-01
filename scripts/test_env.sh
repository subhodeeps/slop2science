#!/usr/bin/env bash
# Self-test how the scripts choose the Python environment, with a fake `uv` that records its
# arguments, so it needs neither network nor a real uv. What it pins:
#   - a project script runs through `uv run --project src/python`, not whichever python3 is
#     first on PATH (otherwise a result depends on an interpreter nobody recorded);
#   - PYTHON=... is an explicit override, and a project without src/python is left alone;
#   - with no uv a project script fails loudly, and setup/tests say why they skipped;
#   - setup refuses to build an environment from a pyproject that still has placeholders;
#   - the libraries installed are exactly the PI's list in src/<lang>/packages.txt: comments
#     and blanks ignored, nothing added that is not listed, nothing run when the list is empty.
set -uo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
pass=0; fail=0
ok()  { pass=$((pass+1)); printf '  ok   %s\n' "$1"; }
bad() { fail=$((fail+1)); printf '  FAIL %s\n' "$1"; }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }

W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
mk() { # tree dir: scripts copied, a fake uv in $W/bin
  local t="$1"; mkdir -p "$t/scripts" "$t/src/python" "$t/validation"
  cp "$SRC"/scripts/{run,py,setup_env.sh,run_tests.sh} "$t/scripts/"
  echo 'print("hi")' > "$t/validation/p.py"
  printf '[project]\nname = "demo"\n' > "$t/src/python/pyproject.toml"
}
mkdir -p "$W/bin"
cat > "$W/bin/uv" <<'F'
#!/usr/bin/env bash
echo "$*" >> "$UV_LOG"; exit 0
F
chmod +x "$W/bin/uv"
cat > "$W/bin/julia" <<'F'
#!/usr/bin/env bash
echo "julia $*" >> "$UV_LOG"; exit 0
F
chmod +x "$W/bin/julia"
export UV_LOG="$W/uv.log"
BASE="/usr/bin:/bin:/usr/local/bin"

echo "env-test: scripts/run"
T="$W/a"; mk "$T"; : > "$UV_LOG"
( cd "$T" && PATH="$W/bin:$BASE" RUN_SERIAL=0 scripts/run validation/p.py >/dev/null 2>&1 )
check "a project script goes through uv run --project src/python" \
  'grep -q "^run --project src/python python validation/p.py$" "$UV_LOG"'

: > "$UV_LOG"
( cd "$T" && PATH="$W/bin:$BASE" PYTHON=python3 RUN_SERIAL=0 scripts/run validation/p.py >/dev/null 2>&1 )
check "PYTHON=... is an explicit override: uv is not used" '[ ! -s "$UV_LOG" ]'

T2="$W/b"; mk "$T2"; rm -f "$T2/src/python/pyproject.toml"; : > "$UV_LOG"
( cd "$T2" && PATH="$W/bin:$BASE" RUN_SERIAL=0 scripts/run validation/p.py >/dev/null 2>&1 )
check "a project with no src/python is left alone: uv is not used" '[ ! -s "$UV_LOG" ]'

out="$(cd "$T" && PATH="$BASE" RUN_SERIAL=0 scripts/run validation/p.py 2>&1)"; rc=$?
check "no uv: a project script fails loudly (exit 127)" '[ "$rc" -eq 127 ]'
check "...and says what to do" 'echo "$out" | grep -q "make setup"'

echo "env-test: scripts/setup_env.sh"
T3="$W/c"; mk "$T3"; : > "$UV_LOG"
printf '[project]\nname = "{{PROJECT_PACKAGE}}"\n' > "$T3/src/python/pyproject.toml"
out="$(cd "$T3" && PATH="$W/bin:$BASE" scripts/setup_env.sh 2>&1)"
check "placeholders in pyproject: nothing is built, and it says run /init-paper" \
  '[ ! -s "$UV_LOG" ] && echo "$out" | grep -q "run /init-paper"'

: > "$UV_LOG"
out="$(cd "$T" && PATH="$W/bin:$BASE" scripts/setup_env.sh 2>&1)"
check "setup builds the environment with uv sync --project src/python" \
  'grep -q "^sync --project src/python$" "$UV_LOG"'

out="$(cd "$T" && PATH="$BASE" scripts/setup_env.sh 2>&1)"
check "no uv: setup skips Python and says to install uv, not to use pip" \
  'echo "$out" | grep -q "uv not found" && ! echo "$out" | grep -q "pip install"'

echo "env-test: the PI's library lists"
mkdir -p "$T/src/julia"; printf '[deps]\n' > "$T/src/julia/Project.toml"
printf '# header\nnumpy   # arrays\n\n   scipy\n' > "$T/src/python/packages.txt"
printf '# header\nLinearAlgebra  # std\nDoubleFloats\n' > "$T/src/julia/packages.txt"
: > "$UV_LOG"; ( cd "$T" && PATH="$W/bin:$BASE" scripts/setup_env.sh >/dev/null 2>&1 )
check "Python: uv add receives exactly the listed names, comments stripped" \
  'grep -qx "add --project src/python numpy scipy" "$UV_LOG"'
check "Julia: Pkg.add receives exactly the listed names" \
  'grep -q "using Pkg; Pkg.add(ARGS) LinearAlgebra DoubleFloats$" "$UV_LOG"'

printf '# nothing chosen\n\n' > "$T/src/python/packages.txt"; printf '# nothing\n' > "$T/src/julia/packages.txt"
: > "$UV_LOG"; ( cd "$T" && PATH="$W/bin:$BASE" scripts/setup_env.sh >/dev/null 2>&1 )
check "an empty list installs nothing in either language" \
  '! grep -q "^add " "$UV_LOG" && ! grep -q "Pkg.add" "$UV_LOG"'

echo "env-test: scripts/run_tests.sh"
mkdir -p "$T/tests/python"; : > "$UV_LOG"; mkdir -p "$T/src/python/.venv"
( cd "$T" && PATH="$W/bin:$BASE" scripts/run_tests.sh python >/dev/null 2>&1 )
check "tests run in the project environment: uv run --project src/python pytest" \
  'grep -q "^run --project src/python pytest -q -rs tests/python$" "$UV_LOG"'

out="$(cd "$T" && PATH="$BASE" scripts/run_tests.sh python 2>&1)"
check "no uv: tests are a loud SKIP, not a pass" 'echo "$out" | grep -q "SKIP python: uv not installed"'

echo
echo "env-test: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
