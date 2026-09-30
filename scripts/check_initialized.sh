#!/usr/bin/env bash
# Fail if the repository still carries {{PLACEHOLDERS}} outside the template's own docs.
# In the template repository itself this is expected to fail; in a real project it means
# /init-paper has not been run (or was interrupted part-way).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
# Excluded: files that legitimately CONTAIN the placeholder pattern rather than being
# templated by it -- the template's own documentation, the init skill, and the three files
# whose job is to detect or mention placeholders (including this script).
hits=$(git grep -l -E '\{\{[A-Z_]+\}\}' -- \
         ':!TEMPLATE_GUIDE.md' ':!README.md' ':!.claude/skills/init-paper/**' \
         ':!.claude/hooks/session_context.sh' ':!.github/workflows/checks.yml' \
         ':!scripts/check_initialized.sh' 2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "uninitialized placeholders remain in:"
  echo "$hits" | sed 's/^/  /'
  echo "run /init-paper in a Claude Code session"
  exit 1
fi
echo "initialized: no placeholders outside the template's own documentation"
