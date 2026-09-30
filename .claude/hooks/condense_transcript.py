#!/usr/bin/env python3
"""Condense a session transcript to dialogue plus one-line tool summaries.

    condense_transcript.py <transcript.jsonl>   -> condensed markdown on stdout

Kept: what the PI actually said, what the assistant actually replied, and one line per tool
call saying what it touched. Dropped: thinking blocks, full tool outputs, and file contents —
which are the bulk of a transcript and are already on disk where they matter.

The point is not a complete archive. It is that the *next* session can be grounded in what
happened, including the dead ends, rather than only in the tidied-up handoff — and the tidying
is exactly where a wrong turn stops being visible.
"""
import json
import sys
from pathlib import Path

MAX_TEXT = 1500          # per message; a very long message is truncated, not dropped


def text_of(content):
    """Extract human-readable text from a message's content field."""
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            kind = block.get("type")
            if kind == "text":
                parts.append(block.get("text", ""))
            elif kind == "tool_use":
                name = block.get("name", "tool")
                inp = block.get("input") or {}
                target = (inp.get("file_path") or inp.get("path") or inp.get("pattern")
                          or inp.get("command") or inp.get("url") or "")
                target = str(target).replace("\n", " ")[:120]
                parts.append(f"[{name}] {target}".rstrip())
            # tool_result and thinking are deliberately dropped
    return "\n".join(p for p in parts if p).strip()


def main():
    if len(sys.argv) < 2:
        return 64
    path = Path(sys.argv[1])
    if not path.is_file():
        return 66

    lines = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        message = rec.get("message") or {}
        role = message.get("role") or rec.get("type") or ""
        if role not in ("user", "assistant"):
            continue
        body = text_of(message.get("content"))
        if not body:
            continue
        if body.startswith(("<system-reminder>", "Caveat:")):
            continue
        if len(body) > MAX_TEXT:
            body = body[:MAX_TEXT] + f"\n… [truncated, {len(body)} chars total]"
        lines.append(f"## {role}\n\n{body}\n")

    if not lines:
        return 1
    sys.stdout.write(
        "# Condensed session transcript\n\n"
        "Dialogue and one-line tool summaries. Thinking blocks, tool outputs and file "
        "contents are omitted. Written by `.claude/hooks/capture_session.py`, deliberately "
        "outside the repository.\n\n" + "\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
