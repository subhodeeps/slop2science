#!/usr/bin/env python3
"""Run the condenser and write its output atomically. Invoked detached by capture_session.py.

    _write_record.py <condenser.py> <transcript.jsonl> <destination.md>

Atomic because a Stop hook fires after every turn: a reader (the next session, or the PI)
must never catch a half-written record. Writes to a temporary file beside the destination and
renames, which is atomic on the same filesystem; on any failure the destination is left as it
was rather than truncated.
"""
import os
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 4:
        return 64
    condenser, transcript, dest = (Path(p) for p in sys.argv[1:4])
    tmp = dest.with_suffix(f".tmp.{os.getpid()}")
    try:
        result = subprocess.run([sys.executable, str(condenser), str(transcript)],
                                capture_output=True, text=True, timeout=120)
        if result.returncode != 0 or not result.stdout.strip():
            return 1
        tmp.write_text(result.stdout, encoding="utf-8")
        os.replace(tmp, dest)
    except Exception:
        return 1
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
