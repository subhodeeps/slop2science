#!/usr/bin/env bash
# SessionStart hook (matchers: startup|resume|clear|compact). stdout is added to Claude's
# context, so keep it short and fast -- never launch a CAS kernel or query a large library
# here.
#
# Registered for resume/clear/compact as well as startup: after /clear or a compaction the
# session has no project context at all, which is exactly when a wrong assumption is cheapest
# to make and most expensive to catch.
#
# Four things, in the order a session needs them:
#   1. the handoff note from the last session, WITH ITS AGE
#   2. where the project is (phase, next task) and which tools are here
#   3. what the working tree looks like right now
#   4. anything waiting for intake
#
# Silent about anything that has nothing to say. A hook that prints noise on every session
# start is a hook that gets turned off, and then none of it is there when it matters.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# --- 1. handoff from the previous session ------------------------------------------
# Age is printed because a handoff is prose, not a record: at three days old it is context,
# at three months old it is a description of a project that has moved on. Silently believing
# a stale handoff is worse than having none (docs/GUIDE.md §3).
if [ -f handoff.md ] && [ -s handoff.md ]; then
  age_days=$(scripts/py -c "
import os, time
try:
    print(int((time.time() - os.path.getmtime('handoff.md')) // 86400))
except Exception:
    print('?')
" 2>/dev/null || echo '?')
  case "$age_days" in
    0)  age_note="today" ;;
    1)  age_note="1 day old" ;;
    ''|'?') age_note="age unknown" ;;
    *)  age_note="${age_days} days old" ;;
  esac
  # HTML comments are stripped. The guidance for whoever writes a handoff lives in
  # docs/handoff_guide.md, where it costs nothing until it is read; what is left in the file
  # itself is a pointer, and paying even that in context on every session start is the
  # accretion this hook exists to prevent. (Claude Code strips comments from CLAUDE.md
  # itself; a hook that cats a file has to do it by hand.) Silent if only comments remain.
  body=$(scripts/py -c "
import re, sys
text = open('handoff.md', encoding='utf-8').read()
text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
sys.stdout.write('\n'.join(l for l in text.splitlines() if l.strip()))
" 2>/dev/null)
  if [ -n "$body" ]; then
    echo "=== handoff from the previous session (${age_note}) ==="
    printf '%s\n' "$body"
    echo "=== end handoff ==="
  fi
  if [ "$age_days" != "?" ] && [ -n "$age_days" ] && [ "$age_days" -gt 14 ] 2>/dev/null; then
    echo "[project] NOTE: that handoff is over two weeks old. Treat it as history, and check docs/STATUS.md and the working tree against it before acting on it."
  fi
fi

# --- 2. where the project is, and what is installed --------------------------------
present=()
for t in wolframscript julia python3; do
  command -v "${t}" >/dev/null 2>&1 && present+=("${t}")
done
[ ${#present[@]} -eq 0 ] && present=("none")

phase=$(awk '/^## Current phase/{getline; while ($0 ~ /^[[:space:]]*$/) getline; print; exit}' \
        docs/STATUS.md 2>/dev/null)
task=$(awk '/^## Immediate next task/{getline; while ($0 ~ /^[[:space:]]*$/) getline; print; exit}' \
        docs/STATUS.md 2>/dev/null)

echo "[project] tools present: ${present[*]}"
echo "[project] phase: ${phase:-unknown}"
[ -n "$task" ] && echo "[project] next task: $task"
echo "[project] ownership: docs/toolchain.md | commands: make help | close with /session-close"
echo "[project] language: write all natural-language text in ASD-STE100 (CLI messages, files, comments, commit messages). Not code, notation or quoted text. See .claude/rules/communication.md"

# --- 3. the working tree, right now ------------------------------------------------
# An interrupted session's leftovers are visible at the START, not only at close: that is
# where the orphaned-artefact check is cheap (docs/failure_modes.md entry 5).
if git rev-parse --git-dir >/dev/null 2>&1; then
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  ahead=$(git rev-list --count '@{u}..HEAD' 2>/dev/null || echo 0)
  line="[project] git: branch ${branch:-?}"
  [ "$dirty" != "0" ] && line="$line | ${dirty} uncommitted file(s)"
  [ "$ahead" != "0" ] && [ -n "$ahead" ] && line="$line | ${ahead} commit(s) not pushed"
  echo "$line"
  if [ "$dirty" != "0" ]; then
    git status --porcelain 2>/dev/null | head -8 | sed 's/^/           /'
    [ "$dirty" -gt 8 ] 2>/dev/null && echo "           ... and $((dirty - 8)) more"
    echo "           ^ account for each of these before starting new work (CLAUDE.md §8a)"
  fi
fi

# --- 4. anything waiting ------------------------------------------------------------
if grep -q '{{[A-Z_]*}}' CLAUDE.md 2>/dev/null; then
  echo "[project] NOTE: CLAUDE.md still has {{PLACEHOLDERS}} -- not initialized. Run /init-paper before any scientific work."
fi
for d in papers/_drop code/_drop; do
  if [ -n "$(ls -A "$d" 2>/dev/null | grep -v '^README.md$')" ]; then
    echo "[project] NOTE: $d/ is not empty -- the PI has supplied material awaiting intake."
  fi
done

# Local reference libraries, cached and fast; silent when neither is present.
if [ -x scripts/check_libraries.sh ]; then
  timeout 5 scripts/check_libraries.sh --fast 2>/dev/null \
    || echo "[libraries] check timed out (a library may be on an unreachable volume) -- not blocking"
fi
exit 0
