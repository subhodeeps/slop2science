#!/usr/bin/env bash
# SessionStart hook (matchers: startup|resume|clear|compact). stdout is added to Claude's
# context, so keep it short and fast -- never launch a CAS kernel here.
#
# Registered for resume/clear/compact as well as startup: after /clear or a compaction the
# session has no project context at all, which is exactly when a wrong assumption is cheapest
# to make and most expensive to catch.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

present=()
for t in wolframscript julia python3; do
  if command -v "${t}" >/dev/null 2>&1; then present+=("${t}"); fi
done
[ ${#present[@]} -eq 0 ] && present=("none")

phase=$(awk '/^## Current phase/{getline; while ($0 ~ /^[[:space:]]*$/) getline; print; exit}' \
        docs/STATUS.md 2>/dev/null)
task=$(awk '/^## Immediate next task/{getline; while ($0 ~ /^[[:space:]]*$/) getline; print; exit}' \
        docs/STATUS.md 2>/dev/null)

echo "[project] tools present: ${present[*]}"
echo "[project] phase: ${phase:-unknown}"
[ -n "$task" ] && echo "[project] next task: $task"
echo "[project] toolchain ownership: docs/toolchain.md | commands: make help | close with /session-close"

if grep -rlq '{{[A-Z_]*}}' CLAUDE.md 2>/dev/null; then
  echo "[project] NOTE: CLAUDE.md still contains {{PLACEHOLDERS}} -- this project has not been initialized. Run /init-paper before any scientific work."
fi

if [ -n "$(ls -A papers/_drop 2>/dev/null | grep -v '^README.md$')" ]; then
  echo "[project] NOTE: papers/_drop/ is not empty -- the PI has supplied sources awaiting intake (.claude/skills/literature-audit/SKILL.md)."
fi
if [ -n "$(ls -A code/_drop 2>/dev/null | grep -v '^README.md$')" ]; then
  echo "[project] NOTE: code/_drop/ is not empty -- the PI has supplied code awaiting intake (.claude/skills/external-code/SKILL.md)."
fi
exit 0
