# symbolic/generated — machine-written. Do not edit.

The `export_NN_*` scripts under `symbolic/<topic>/` write this folder. It has one subdirectory
for each consuming language. **A hook blocks edits here** (`.claude/hooks/guard_paths.py`).

To change a file here, change the exporting stage script and run:

    make codegen TOPIC=<topic>
    make codegen-check TOPIC=<topic>      # regenerates and fails on any diff from git

Each generated file has a banner. The banner names the generating script and its SHA-256. Then
you can identify a stale file without a rerun.

## Why the project enforces this rule

To transcribe an expression by hand from one tool to another looks cheap. It is the most
expensive shortcut in a project like this. It causes a sign error that no test catches. The
error is in a file that looks authoritative, and nothing records where the expression came
from. The check `make codegen-check` in CI and this hook together prevent this by accident.

Never write a coefficient by hand here. Never write one by hand in `src/`. If a solver needs
something that is missing, stop. Derive it and export it.
