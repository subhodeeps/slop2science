#!/usr/bin/env python3
"""Scaffold a validation result record with every required provenance field present.

    scripts/py scripts/new_record.py --topic <topic> --id <run-id> [--kind reproduction|extension]

Records are normally written by the validation driver itself -- that is the point: a number
and its provenance are produced by the same run. This helper exists for the first record of a
topic, so the schema is taken from one authoritative place rather than from whichever earlier
record someone happened to open, which is how a mislabelled field propagates.

It refuses to overwrite an existing record: a changed number is a new run, not an edited file.
"""
import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def head():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True)
    ap.add_argument("--id", required=True, help="run id, e.g. baseline_case1_n0")
    ap.add_argument("--kind", default="reproduction", choices=["reproduction", "extension"])
    args = ap.parse_args()

    out = ROOT / "validation" / args.topic / "records" / f"{args.id}.json"
    if out.exists():
        print(f"refusing to overwrite {out.relative_to(ROOT)}: a changed number is a new run, "
              f"not an edited record", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "topic": args.topic,
        "run_id": args.id,
        "kind": args.kind,
        "judged_against": "FILL IN: the paper's Eq./Table N, or the named benchmark/physics",
        "params": {},
        "resolution": [],
        "eltype": [],
        "result": {"value": None, "units": "FILL IN"},
        "residual": None,
        "delta_resolution": None,
        "delta_precision": None,
        "status": "candidate",
        "reject_reason": None,
        "benchmark": {"file": None, "method": None, "converted": False,
                      "conversion": "FILL IN: the explicit convention conversion, or null"},
        "generated_code": {"file": None, "source_sha256": None},
        "tools": {"mathematica": None, "julia": None, "python": platform.python_version()},
        "script": "FILL IN: the script that produced this record",
        "prompt_record": "FILL IN: docs/prompts/<ID>_<topic>.md, or null",
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git": head(),
    }
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    print("Fill every FILL IN field from the run that produced the number, then have the")
    print("driver write records itself from then on (docs/validation_protocol.md §12).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
