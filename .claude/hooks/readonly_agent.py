#!/usr/bin/env python3
"""PreToolUse guard registered in the `verification` subagent's own frontmatter.

The audit layer must not be able to fix what it is auditing, and an instruction saying so is
not enough: an agent that finds a one-line bug is strongly tempted to fix it, and a fixed bug
is an unrecorded finding. This hook makes the independence structural for the Edit and Write
tools. It does not cover Bash: the agent needs Bash to run checks, and a guard for shell writes
would not be complete. The session that dispatches the audit runs `git status` afterwards.

Two kinds of write are allowed. First, anything under .claude/agent-memory/ (recurring
pitfalls, not results). Second, a NEW audit report: `Write` of a file docs/audits/<date>*.md that
does not exist yet. The findings of an audit must be recorded somewhere, and the verifier is the
only party that must not be able to change or hide them afterwards: it cannot overwrite or edit
an audit, and guard_paths.json blocks a `Write` over an existing audit for every other agent.
Everything else is blocked with exit code 2.
"""
import json
import os
import re
import sys

ALLOWED_PREFIX = ".claude/agent-memory/"

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

path = (data.get("tool_input") or {}).get("file_path") or ""
root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
rel = ""
if path:
    try:
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(root)).replace(os.sep, "/")
    except ValueError:
        rel = path

if rel.startswith(ALLOWED_PREFIX):
    sys.exit(0)

tool = data.get("tool_name") or ""
is_new_audit = (
    tool == "Write"
    and re.fullmatch(r"docs/audits/20\d{6}[^/]*\.md", rel) is not None
    and not os.path.exists(os.path.abspath(path))
)
if is_new_audit:
    sys.exit(0)

print(
    f"The verification agent is read-only; blocked write to {rel or path}. "
    "Report the finding with its class, evidence and suggested check instead of fixing it. "
    "Write the report to a new file docs/audits/<YYYYMMDD>_<topic>.md "
    "(.claude/skills/verification/SKILL.md).",
    file=sys.stderr,
)
sys.exit(2)
