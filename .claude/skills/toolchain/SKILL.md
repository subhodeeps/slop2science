---
name: toolchain
description: Run this project's tools - Mathematica, Julia and Python - through the common wrapper, with the environment, timeouts, logging, serialisation, precision tiers and codegen hand-off conventions they share. Use for any command that executes scientific code.
when_to_use: 'Trigger phrases: run the script; wolframscript; Mathematica; julia; python; make test; make stages; codegen; export coefficients; which tool owns this; environment; precision; BigFloat; mpmath'
allowed-tools: Bash(scripts/run *) Bash(scripts/run_stages.sh *) Bash(scripts/run_tests.sh *) Bash(make *) Bash(scripts/check_env.sh *)
---

# Toolchain

Mathematica, Julia and Python are **co-equal** here. Which one is the record for a given topic
or solver is **the PI's decision** (CLAUDE.md §1), recorded in `docs/toolchain.md`'s ownership
registry — not implied by the language, and not yours to choose.

If the registry does not cover the work in front of you, **stop and ask the PI.** Do not pick
the obvious option, do not follow what another topic did, and do not move work into a
different language because it would be easier there. The same applies to hand-offs: if you
need a quantity in a tool the registry does not deliver it to, that is a question, not a
converter to write.

## One invocation path

    scripts/run <file.wls|.jl|.py> [args...]

Everything goes through it, in every language, so that a mixed-language stage manifest is
reproducible. It exports `PROJECT_ROOT`, runs from the repository root, serialises execution
with `flock` (CAS licences commonly cap concurrent kernels, and parallel subagents would
otherwise fail with licence errors), applies `SYMBOLIC_TIMEOUT` (default 1800 s), and tees
output to `logs/`.

    make stages TOPIC=<topic>          run the topic's stages.txt in declared order
    make codegen TOPIC=<topic>         run its export_* stages
    make codegen-check TOPIC=<topic>   regenerate and fail on any diff
    make test                          every present language's tests
    make check-env                     what is installed here, and the ownership registry

Never call an interpreter directly for anything whose result matters. A bare
`wolframscript -code` or `python -c` is fine for a throwaway probe and never for a result:
it is unlogged, unserialised, and leaves no record of what ran.

## Per-tool notes

**Mathematica.** Plain-text `.wls`, never notebooks — notebooks cannot be executed here and
are for the PI's own exploration. Shared helpers in `symbolic/common/*.wl`, loaded by path
from `PROJECT_ROOT`. Avoid version-specific binary formats; persist with text output. Each
kernel launch is slow, so batch a stage's work into one script rather than many calls.

**Julia.** Environment is `src/julia` (`Project.toml` + `Manifest.toml`, **both committed** —
the manifest pins the exact environment behind every result). `make setup` instantiates.
Write numerics generic in `T<:AbstractFloat` so the same code runs in working, double-double
and arbitrary precision. Each call pays start-up and compilation: batch into one script.

**Python.** Environment is `src/python` (`pyproject.toml` + a committed lock file, same
reason). Generic precision via `mpmath`/`gmpy2` where extended precision is needed; be
explicit about where a computation silently drops to machine precision — a NumPy call in the
middle of an `mpmath` chain is the usual culprit, and it is invisible in the output.

## Hand-off between tools

Whichever tool derives, whichever consumes:

1. the deriving tool's `export_NN_*` script writes to `symbolic/generated/<lang>/`;
2. the generated file carries a banner naming the generating script and its SHA-256;
3. `make codegen-check TOPIC=<topic>` regenerates and fails on any diff;
4. `symbolic/generated/**` is hook-blocked against editing.

**Never hand-transcribe an expression between tools**, in any direction, however short, however
temporary. This is the rule that a rushed session breaks first and that costs the most.

## When a tool is absent

`make check` and every repository check run with no scientific toolchain at all — in CI, on a
laptop, in a cloud container. `make test` skips a language that is not installed, loudly.
`make check-env` reports what is missing and never fails for absence alone. A session in a
container without the owning tool can still audit, write up, plan and check references; it
cannot produce a new verified result, and should say so rather than reasoning one out.
