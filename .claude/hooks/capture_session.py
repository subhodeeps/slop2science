#!/usr/bin/env python3
"""Stop hook: keep a condensed copy of this session's transcript, OUTSIDE the repository.

Where: ${RESEARCH_RECORDS_DIR:-~/.claude-research-records}/<project>/last-session.md

**Why outside the repository.** A transcript is near-verbatim. It holds half-formed
reasoning, the dead ends, and whatever was said about a result before anyone was sure of it.
A repository gets shared — with a collaborator, a supervisor, a journal, eventually the
world — and sharing permissions inherit downward and cannot be subtracted from a subfolder.
A leading dot does not help: `.claude/` is hidden in a file browser and an ordinary visible
folder in a web UI. The property being relied on is *never shared*, not *not in the repo*.

`handoff.md` is the artifact meant to be read by other people, and it is committed.
This is not.

Fires after every assistant turn; the transcript on disk is always current, so each fire
re-condenses the whole thing and the last turn leaves a complete record. The write is atomic
and the heavy work is backgrounded, so a turn is never blocked.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    transcript = data.get("transcript_path") or ""
    if not transcript or not Path(transcript).is_file():
        return 0

    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".").resolve()
    slug = re.sub(r"[^A-Za-z0-9._-]", "_", root.name) or "project"
    records = Path(os.environ.get("RESEARCH_RECORDS_DIR")
                   or Path.home() / ".claude-research-records") / slug
    condenser = HERE / "condense_transcript.py"
    if not condenser.is_file():
        return 0

    try:
        records.mkdir(parents=True, exist_ok=True)
        (records / ".project-path").write_text(str(root) + "\n", encoding="utf-8")
        # Backgrounded and detached: a Stop hook that blocks is a turn that hangs.
        subprocess.Popen(
            [sys.executable, str(HERE / "_write_record.py"), str(condenser),
             transcript, str(records / "last-session.md")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True)
    except Exception:
        pass                              # capture must never break a session
    return 0


if __name__ == "__main__":
    sys.exit(main())
