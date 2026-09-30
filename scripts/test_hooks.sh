#!/usr/bin/env bash
# Self-test the Claude Code hooks by feeding them synthetic payloads.
#
# A guard hook that has silently stopped working looks exactly like a guard hook that is
# working: nothing gets blocked either way. These tests are the only thing that tells the
# difference, so they run in `make check` and in CI on every push.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export CLAUDE_PROJECT_DIR="$ROOT"
PY="$ROOT/scripts/py"
pass=0; fail=0

payload() { # tool_name file_path
  printf '{"tool_name":"%s","tool_input":{"file_path":"%s"},"cwd":"%s"}' "$1" "$ROOT/$2" "$ROOT"
}

expect() { # description expected_rc hook payload
  local desc="$1" want="$2" hook="$3" data="$4"
  echo "$data" | "$PY" "$hook" >/dev/null 2>&1
  local got=$?
  if [ "$got" -eq "$want" ]; then
    pass=$((pass+1)); printf '  ok   %s\n' "$desc"
  else
    fail=$((fail+1)); printf '  FAIL %s (expected exit %s, got %s)\n' "$desc" "$want" "$got"
  fi
}

G=".claude/hooks/guard_paths.py"
R=".claude/hooks/readonly_agent.py"

echo "guard_paths.py — read-only paths"
expect "blocks Write under papers/"            2 "$G" "$(payload Write papers/some_source.pdf)"
expect "blocks Edit under papers/"             2 "$G" "$(payload Edit  papers/some_source.pdf)"
expect "blocks symbolic/generated/"            2 "$G" "$(payload Write symbolic/generated/julia/coeffs.jl)"
expect "blocks a result record"                2 "$G" "$(payload Edit  validation/topic/records/r1.json)"
expect "blocks an accepted table"              2 "$G" "$(payload Write validation/topic/accepted/table.csv)"
expect "allows the curated source registry"    0 "$G" "$(payload Edit  papers/sources.yaml)"
expect "allows an ordinary doc"                0 "$G" "$(payload Edit  docs/STATUS.md)"
expect "allows a derivation write-up"          0 "$G" "$(payload Write derivation/topic/01_setup.md)"

echo "guard_paths.py — append-only stage scripts"
mkdir -p symbolic/_hooktest
printf '(* fixture *)\n' > symbolic/_hooktest/stage_01_fixture.wls
printf '# fixture\n'      > symbolic/_hooktest/export_01_fixture.py
expect "blocks Write over an existing stage"   2 "$G" "$(payload Write symbolic/_hooktest/stage_01_fixture.wls)"
expect "blocks Write over an existing export"  2 "$G" "$(payload Write symbolic/_hooktest/export_01_fixture.py)"
expect "allows Edit of an existing stage"      0 "$G" "$(payload Edit  symbolic/_hooktest/stage_01_fixture.wls)"
expect "allows Write of a NEW stage"           0 "$G" "$(payload Write symbolic/_hooktest/stage_02_new.jl)"
rm -f symbolic/_hooktest/stage_01_fixture.wls symbolic/_hooktest/export_01_fixture.py
rmdir symbolic/_hooktest 2>/dev/null || true

echo "guard_paths.py — robustness"
expect "does not block on malformed input"     0 "$G" 'not json at all'
expect "does not block with no file_path"      0 "$G" '{"tool_name":"Write","tool_input":{}}'

echo "readonly_agent.py — verification agent"
expect "blocks a write to a project file"      2 "$R" "$(payload Write src/julia/src/solver.jl)"
expect "blocks a write to docs/"               2 "$R" "$(payload Edit  docs/STATUS.md)"
expect "allows a write to its agent memory"    0 "$R" "$(payload Write .claude/agent-memory/verification/MEMORY.md)"

echo "log_prompt.py — prompt capture"
tmp_session="hooktest"
printf '{"prompt":"%s","session_id":"%s","cwd":"%s"}' \
  "synthetic hook self-test prompt" "$tmp_session" "$ROOT" \
  | "$PY" .claude/hooks/log_prompt.py >/dev/null 2>&1
if grep -q "synthetic hook self-test prompt" "docs/prompts/log/${tmp_session:0:8}.md" 2>/dev/null; then
  pass=$((pass+1)); echo "  ok   appends a prompt to the raw session log"
else
  fail=$((fail+1)); echo "  FAIL did not append a prompt to docs/prompts/log/"
fi
long=$(printf 'x%.0s' $(seq 1 700))
printf '{"prompt":"%s","session_id":"%s","cwd":"%s"}' "$long" "$tmp_session" "$ROOT" \
  | "$PY" .claude/hooks/log_prompt.py >/dev/null 2>&1
if ls docs/prompts/auto/*_${tmp_session:0:8}_*.md >/dev/null 2>&1; then
  pass=$((pass+1)); echo "  ok   captures a >=600-char prompt to docs/prompts/auto/"
else
  fail=$((fail+1)); echo "  FAIL did not capture a long prompt to docs/prompts/auto/"
fi
printf '{"prompt":"<task-notification>%s","session_id":"%s","cwd":"%s"}' "$long" "$tmp_session" "$ROOT" \
  | "$PY" .claude/hooks/log_prompt.py >/dev/null 2>&1
if [ "$(ls docs/prompts/auto/*_${tmp_session:0:8}_*.md 2>/dev/null | wc -l)" -eq 1 ]; then
  pass=$((pass+1)); echo "  ok   does not capture harness traffic as a prompt"
else
  fail=$((fail+1)); echo "  FAIL captured harness traffic into docs/prompts/auto/"
fi
rm -f "docs/prompts/log/${tmp_session:0:8}.md" docs/prompts/auto/*_${tmp_session:0:8}_*.md

echo "session_context.sh"
if out=$(CLAUDE_PROJECT_DIR="$ROOT" ./.claude/hooks/session_context.sh 2>/dev/null) \
   && echo "$out" | grep -q '^\[project\]'; then
  pass=$((pass+1)); echo "  ok   prints project context"
else
  fail=$((fail+1)); echo "  FAIL produced no project context"
fi

echo
echo "hooks: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
