"""Write a result record from the run that produced the number. Copy into validation/<topic>/.

The number and its provenance are produced by the same run: that is the whole point. A record
written afterwards, by hand, from memory or from another record, is how a mislabelled field
propagates (docs/validation_protocol.md §12).

Records are hook-protected against hand editing. A changed number is a new run.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("PROJECT_ROOT", ".")).resolve()


def _git_head() -> str:
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def write_record(topic: str, run_id: str, *, kind: str, judged_against: str,
                 params: dict, resolution: list, eltype: list, result: dict,
                 residual, delta_resolution, delta_precision,
                 status: str, benchmark: dict, generated_code: dict,
                 script: str, prompt_record: str | None = None,
                 reject_reason: str | None = None, **extra) -> Path:
    """Write one record. Every provenance field is required, on purpose.

    `status` is 'candidate' until the validation protocol has been passed. Do not pass
    'accepted' from a run that has not run every applicable check — and never pass 'accepted'
    alongside a flag that is true, which `make check-docs` rejects.
    """
    if status == "accepted" and any(
            k.lower().endswith("flag") and v is True for k, v in extra.items()):
        raise ValueError("a record cannot be 'accepted' while one of its own flags is true")

    record = {
        "topic": topic, "run_id": run_id, "kind": kind,
        "judged_against": judged_against,
        "params": params, "resolution": resolution, "eltype": eltype,
        "result": result,
        "residual": residual,
        "delta_resolution": delta_resolution,
        "delta_precision": delta_precision,
        "status": status, "reject_reason": reject_reason,
        "benchmark": benchmark, "generated_code": generated_code,
        "tools": {"mathematica": None, "julia": None, "python": platform.python_version()},
        "script": script, "prompt_record": prompt_record,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git": _git_head(),
        **extra,
    }
    out = ROOT / "validation" / topic / "records" / f"{run_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return out
