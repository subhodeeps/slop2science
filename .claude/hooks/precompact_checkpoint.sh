#!/usr/bin/env bash
# PreCompact hook: fires just before the context window is compacted.
#
# Compaction is the moment this project is most likely to lose something: a summary keeps the
# thread of the conversation but not the half-formed judgement, the number that looked wrong,
# or the fact that a stage was left mid-edit. Everything this template does to preserve
# context across *sessions* is worthless if it is lost silently inside one.
#
# Two things, both cheap:
#   1. write a snapshot of the working tree and the project's own state to a file OUTSIDE the
#      repository, so it survives compaction and cannot pollute the project's history;
#   2. print a short instruction, so the post-compaction context carries the one obligation
#      that cannot be reconstructed from files -- writing down what is only in the model's
#      head right now.
set -u
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

slug=$(basename "$(pwd)" | tr -c 'A-Za-z0-9._-' '_')
dir="${RESEARCH_RECORDS_DIR:-$HOME/.claude-research-records}/$slug"
mkdir -p "$dir" 2>/dev/null || exit 0
out="$dir/precompact-$(date +%Y%m%dT%H%M%S).md"

{
  echo "# Pre-compaction snapshot — $(date -Iseconds)"
  echo
  echo "Project: $(pwd)"
  echo
  echo "## git"
  echo '```'
  git status --short 2>/dev/null | head -40
  echo "--- branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
  echo "--- HEAD:   $(git log -1 --format='%h %s' 2>/dev/null)"
  echo '```'
  echo
  echo "## docs/STATUS.md — immediate next task"
  awk '/^## Immediate next task/{f=1; next} /^## /{f=0} f' docs/STATUS.md 2>/dev/null | head -20
  echo
  echo "## handoff.md (as it stands)"
  sed 's/^/    /' handoff.md 2>/dev/null | head -30
} > "$out" 2>/dev/null

echo "[precompact] Context is about to be compacted. A snapshot of git state, the next task and the current handoff is at $out."
echo "[precompact] Before continuing: if anything important is only in this conversation and not yet in a file — a judgement you have not written down, a result you have not recorded, a stage left mid-edit, a suspicion worth keeping — put it in handoff.md or docs/STATUS.md NOW. Compaction keeps the thread, not the detail."
exit 0
