#!/usr/bin/env python3
"""Detect a project file that a Bash command of the `verification` agent changed.

readonly_agent.py blocks the Edit and Write tools of the verifier. It cannot block a shell
write such as `sed -i` or `cat > file`, because no parser of shell commands is complete. This
hook does not try to parse the command. It compares the state of the working tree before and
after each Bash call:

  pre   (PreToolUse on Bash)   record each changed or untracked file and a hash of its content
  post  (PostToolUse on Bash)  record the state again and report each difference

A change under docs/audits/ or .claude/agent-memory/ is expected and is not reported. Any other
change exits with code 2, so the agent sees the message and must report the write as a finding.
The hook detects. It does not prevent and it does not undo. It does not see files that
.gitignore excludes. Malformed input never blocks.

Usage (from the agent frontmatter): bash_write_check.py pre | bash_write_check.py post
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

EXPECTED_PREFIXES = ("docs/audits/", ".claude/agent-memory/")
STATE_DIR = os.path.join(tempfile.gettempdir(), "claude-bash-write-check")


def tree_state(root):
    """{path: content hash} for each file that git reports as changed, deleted or untracked."""
    try:
        out = subprocess.run(["git", "-C", root, "status", "--porcelain", "-z", "-uall"],
                             capture_output=True, text=True, check=True).stdout
    except Exception:
        return None
    state = {}
    entries = out.split("\0")
    i = 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        if "R" in code or "C" in code:
            i += 1                      # a rename has the old path in the next entry
        full = os.path.join(root, path)
        try:
            with open(full, "rb") as fh:
                state[path] = hashlib.sha256(fh.read()).hexdigest()
        except OSError:
            state[path] = "missing"
    return state


def state_file(data):
    key = data.get("tool_use_id") or data.get("session_id") or "default"
    key = "".join(c for c in key if c.isalnum() or c in "-_")[:100] or "default"
    return os.path.join(STATE_DIR, key + ".json")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                     # never block on malformed input
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    path = state_file(data)

    if mode == "pre":
        state = tree_state(root)
        if state is not None:
            os.makedirs(STATE_DIR, exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(state, fh)
        sys.exit(0)

    if mode != "post":
        sys.exit(0)
    try:
        with open(path, encoding="utf-8") as fh:
            before = json.load(fh)
        os.remove(path)
    except Exception:
        sys.exit(0)                     # no snapshot: nothing to compare
    after = tree_state(root)
    if after is None:
        sys.exit(0)

    changed = sorted(p for p in set(before) | set(after)
                     if before.get(p) != after.get(p) and not p.startswith(EXPECTED_PREFIXES))
    if not changed:
        sys.exit(0)
    print(
        "This Bash command changed project files: " + ", ".join(changed) + ".\n"
        "The verification agent must not change project files. Do not undo the change yourself. "
        "Report each file as a finding in your audit report, with the command that changed it, "
        "so that the main session can review it.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
