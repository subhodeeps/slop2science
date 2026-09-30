#!/usr/bin/env python3
"""PreToolUse guard for Edit|Write. Registered in .claude/settings.json.

Enforcement that does not depend on the model following an instruction. Two protections,
both configured as data in .claude/guard_paths.json (nothing is hardcoded here):

  readonly     paths that Claude must never edit directly (sources, machine-generated
               hand-off code, result records, accepted tables), minus `readonly_exempt`
               entries (curated logs a subagent does maintain by hand).
  append_only  paths where `Write` to an *existing* file is blocked but `Edit` is allowed:
               derivation stage and export scripts are a permanent, citable record, so a
               new stage is a new numbered file, never an overwrite of an old one.

Exit code 2 blocks the tool call and shows stderr to Claude as the reason. Malformed input
or a missing/broken config never blocks: a guard that fails closed on its own bug would make
the repository unusable, and `make test-hooks` is what catches a broken guard.
"""
import json
import os
import re
import sys

CONFIG = ".claude/guard_paths.json"


def glob_to_regex(pattern):
    """Repository-relative POSIX glob -> anchored regex.

    '**' crosses path separators, '*' and '?' do not. Everything else is literal.
    """
    out, i = [], 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def load_config(root):
    try:
        with open(os.path.join(root, CONFIG), encoding="utf-8") as fh:
            cfg = json.load(fh)
    except Exception:
        return None
    for key in ("readonly", "append_only"):
        for entry in cfg.get(key, []):
            entry["_re"] = glob_to_regex(entry.get("glob", ""))
    return cfg


def block(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                     # never block on malformed input

    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not path:
        sys.exit(0)

    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    try:
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(root))
    except ValueError:                  # different drive on Windows
        sys.exit(0)
    rel = rel.replace(os.sep, "/")
    if rel.startswith("../"):
        sys.exit(0)                     # outside the repository; not ours to police

    cfg = load_config(root)
    if cfg is None:
        sys.exit(0)                     # config missing or unreadable: `make test-hooks` catches this

    if rel not in set(cfg.get("readonly_exempt", [])):
        for entry in cfg.get("readonly", []):
            if entry["_re"].match(rel):
                block(f"Blocked edit to {rel}: {entry.get('reason', 'path is read-only.')}")

    if (data.get("tool_name") or "") == "Write":
        for entry in cfg.get("append_only", []):
            if entry["_re"].match(rel) and os.path.exists(os.path.abspath(path)):
                block(f"Blocked overwrite of {rel}: {entry.get('reason', 'file is append-only.')}")

    sys.exit(0)


if __name__ == "__main__":
    main()
