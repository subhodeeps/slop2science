# Toolchain and tool ownership

Mathematica, Julia and Python are **co-equal** in this project. Neither symbolic work nor
numerics belongs to a language by default. What matters is that for every topic and every
solver, exactly one tool is the **record**, and that this is written down.

Execution details (the common wrapper, environments, precision, hand-off): the `toolchain`
skill. Rules a checker enforces: `.claude/rules/derivation.md`,
`.claude/rules/implementation.md`.

## Why ownership is declared rather than inferred

Three capable tools make it easy to end up with two slightly different versions of the same
equation — derived in one tool, re-derived in another during a debugging session, both
committed, neither marked as authoritative. Nothing catches that: both pass their own checks.

So: one record per fact. A derivation or solver in a second tool is a **cross-check** of a
named owner, labelled as such in its header and in `validation/`, and it never becomes the
record. Disagreement between an owner and its cross-check is a discrepancy to record in the
five-point form, not a choice to make silently.

`make check-docs` fails if a topic has stage scripts but no row in the registry below.

## Ownership registry

<!-- REGISTRY-START -->

| Topic / solver | Owner tool | Kind | Cross-checked by | Notes |
|---|---|---|---|---|
| {{TOPIC_1}} | {{TOOL_A}} | derivation | — | |
| {{TOPIC_1}} solver | {{TOOL_B}} | implementation | — | consumes `symbolic/generated/` only |

<!-- REGISTRY-END -->

## Division of labour

| Layer | Location | Record |
|---|---|---|
| Derivation: equations, reduction, series and asymptotics, limits | `symbolic/<topic>/stage_NN_*.<ext>` | the scripts, their `out/` files, and the logs |
| Hand-off between tools | `symbolic/<topic>/export_NN_*.<ext>` → `symbolic/generated/<lang>/` | a banner naming the generating script and its SHA-256 |
| Production numerics, validation, figures | `src/<lang>/`, `validation/<topic>/` | JSON result records |
| Tests | `tests/<lang>/` | `make test` |
| Independent cross-checks | a genuinely different route, usually another tool | labelled `cross-check` in `validation/` |

Adding a fourth tool to the pipeline is a PI decision, logged in `docs/decision_log.md`.

## Mathematica

- Invocation: always `scripts/run <script.wls>`. It exports `PROJECT_ROOT`, runs from the
  repository root, serialises kernels with `flock` (licences commonly cap concurrent kernels —
  relevant as soon as two subagents run at once), applies `SYMBOLIC_TIMEOUT`, and logs.
- If `wolframscript` is not on `PATH`, set `WOLFRAMSCRIPT=/path/to/wolframscript` in the shell
  or in `.claude/settings.local.json`'s `env`.
- Shared code: `symbolic/common/*.wl`, loaded by path from `PROJECT_ROOT`. Run its self-tests
  before relying on it.
- **Scripts, not notebooks**, are the record. Notebooks cannot be executed here; they are for
  the PI's own exploration and live in `notes/`.
- Avoid version-specific binary formats; persist results as text.

## Julia

- Environment: `src/julia` (`Project.toml` **and** `Manifest.toml`, both committed — the
  manifest pins the exact environment behind every result). `make setup` instantiates.
- Write numerics generic in `T<:AbstractFloat` so the same code runs in working, double-double
  and arbitrary precision.
- Each call pays start-up and compilation: batch a task into one script rather than many
  invocations.

## Python

- Environment: `src/python` (`pyproject.toml` and a committed lock file, same reason).
  `make setup` installs it with dev extras.
- Extended precision via `mpmath`/`gmpy2`. **Be explicit about where a chain silently drops to
  machine precision** — a NumPy call in the middle of an `mpmath` computation is the usual
  culprit, and nothing in the output reveals it.
- Python also carries this repository's own checkers and hooks
  (`scripts/check_docs.py`, `.claude/hooks/*.py`); those are infrastructure, outside the
  ownership registry.

## When a tool is missing

`make check` and every repository check run with no scientific toolchain at all — in CI, on a
borrowed laptop, in a cloud container. `make test` skips an absent language loudly.
`make check-env` reports what is present and does not fail for absence alone (use `--strict`
where a missing tool should fail).

A session on a machine without the tool that owns the topic can audit, write up, plan and
check references. It **cannot** produce a new verified result, and should say so rather than
reasoning one out.
