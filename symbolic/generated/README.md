# symbolic/generated — machine-written. Do not edit.

Written by the `export_NN_*` scripts under `symbolic/<topic>/`, one subdirectory per consuming
language. **Edits here are blocked by a hook** (`.claude/hooks/guard_paths.py`).

To change something here, change the exporting stage script and run:

    make codegen TOPIC=<topic>
    make codegen-check TOPIC=<topic>      # regenerates and fails on any diff from git

Every generated file carries a banner naming the generating script and its SHA-256, so a stale
file is identifiable without rerunning anything.

## Why this is enforced rather than requested

Hand-transcribing an expression from one tool to another is the cheapest-looking and most
expensive shortcut available in a project like this: it introduces a sign error that no test
catches, in a file that looks authoritative, with no record of where the expression came from.
`make codegen-check` in CI and this hook together make it impossible to do accidentally.

Never hand-write a coefficient here, and never hand-write one in `src/` either. If something a
solver needs is missing, the correct response is to stop and derive and export it.
