---
name: toolchain
description: Run the tools of this project (Mathematica, Julia and Python) through the common wrapper. It covers the environment, timeouts, logging, serialisation, precision tiers and the codegen hand-off that the tools share. Use it for any command that runs scientific code.
when_to_use: 'Trigger phrases: run the script, wolframscript, Mathematica, julia, python, make test, make stages, codegen, export coefficients, which tool owns this, environment, precision, BigFloat, mpmath'
allowed-tools: Bash(scripts/run *) Bash(scripts/run_stages.sh *) Bash(scripts/run_tests.sh *) Bash(make *) Bash(scripts/check_env.sh *)
---

# Toolchain

The registry in `docs/toolchain.md` names the tool that owns each topic and solver. It also
defines the default profile (CLAUDE.md §5). If the registry has no row for your work, apply the
default profile by kind of work. Write the row first and cite the decision. If the work fits no
kind, or the kind is not clear, **stop and ask the PI.** Use the default routes for hand-offs.
Do not write a converter.

## One path of invocation

    scripts/run <file.wls|.jl|.py> [args...]

Everything goes through this wrapper, in each language. Then a stage manifest with more than one
language is reproducible. The wrapper exports `PROJECT_ROOT`, runs from the repository root and
serialises execution with `flock`. CAS licences commonly limit concurrent kernels, and parallel
subagents would fail with licence errors without the lock. The wrapper applies
`SYMBOLIC_TIMEOUT` (default 1800 s) and copies the output to `logs/`.

    make stages TOPIC=<topic>          run the stages.txt of the topic in declared order
    make codegen TOPIC=<topic>         run its export_* stages
    make codegen-check TOPIC=<topic>   regenerate and fail on any diff
    make test                          the tests of each language that is present
    make check-env                     what is installed here, and the ownership registry

Never call an interpreter directly for anything whose result matters. A bare
`wolframscript -code` or `python -c` is acceptable for a throwaway probe. It is never acceptable
for a result. Nothing logs it, nothing serialises it, and it leaves no record of what ran.

## Notes for each tool

**Mathematica.**

- Use plain-text `.wls`. Never use notebooks as the record. Notebooks cannot run here. They are
  for the own exploration of the PI, and they live in `notes/`.
- Run each script with `scripts/run`. If `wolframscript` is not on `PATH`, set
  `WOLFRAMSCRIPT=/path/to/wolframscript` in the shell or in the `env` of
  `.claude/settings.local.json`.
- Put shared helpers in `symbolic/common/*.wl`. Load them by path from `PROJECT_ROOT`. Run their
  self-tests before you rely on them.
- Avoid binary formats that depend on a version. Persist results as text.
- Each kernel launch is slow. Batch the work of a stage into one script.

**Julia.**

- The environment is `src/julia` (`Project.toml` and `Manifest.toml`, **both committed**). The
  manifest pins the exact environment behind each result. `make setup` instantiates it.
- Write numerics generic in `T<:AbstractFloat`. Then the same code runs in working precision,
  double-double precision and arbitrary precision.
- Each call pays the cost of start-up and compilation. Batch the work into one script.

**Python.**

- The environment is `src/python`, managed with [uv](https://docs.astral.sh/uv/). Commit
  `pyproject.toml` and `uv.lock`. Do not commit `src/python/.venv/`. `make setup` runs
  `uv sync`. To add a dependency, run `uv add --project src/python <pkg>`, and record the reason
  in `docs/decision_log.md`.
- `scripts/run x.py` runs inside the environment (`uv run --project src/python`). Then a result
  does not depend on which interpreter is first on `PATH`. `PYTHON=...` overrides this
  explicitly. Without uv, a project script fails loudly.
- Use `mpmath` or `gmpy2` for extended precision. State where a computation silently drops to
  machine precision. A NumPy call in the middle of an `mpmath` chain is the usual cause, and the
  output does not show it.
- Python also runs the checkers and hooks of this repository (`scripts/check_docs.py`,
  `.claude/hooks/*.py`). They are infrastructure and are outside the ownership registry.

Julia and Python each have an environment only if the project uses the language. If it does not,
delete `src/julia` or `src/python`. `docs/toolchain.md` states which libraries each environment
carries.

## Hand-off between tools

This applies to each tool that derives and each tool that consumes:

1. The `export_NN_*` script of the deriving tool writes to `symbolic/generated/<lang>/`.
2. The generated file has a banner that names the generating script and its SHA-256.
3. `make codegen-check TOPIC=<topic>` regenerates the file and fails on any diff.
4. A hook blocks edits to `symbolic/generated/**`.

**Never transcribe an expression by hand between tools**, in any direction, however short and
however temporary. A rushed session breaks this rule first, and the cost is the highest.

## When a tool is absent

`make check` and each repository check run with no scientific toolchain at all: in CI, on a
laptop and in a cloud container. `make test` skips a language that is not installed, and it says
so loudly. `make check-env` reports what is missing. It never fails only because a tool is
absent. A session in a container without the owning tool can still audit, write up, plan and
check references. It cannot produce a new verified result. It must say so. It must not reason a
result out.
