# Toolchain and tool ownership

Mathematica, Julia and Python are **co-equal** in this project. Neither symbolic work nor
numerics belongs to a language by default.

**The PI decides what is implemented in which language, and how the tools interoperate**
(CLAUDE.md §1, §5). Claude does not choose a language for a new piece of work, does not move
work between languages, and does not add or change a hand-off between tools. Every assignment
below is a PI decision with a `docs/decision_log.md` entry; where this file does not cover the
work at hand, **stop and ask the PI** rather than picking the obvious option.

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

Filled by `/init-paper` from the PI's answers, and changed only by a PI decision. Every row
cites the decision that put it there, so "why is this in Julia?" always has an answer.

<!-- REGISTRY-START -->

| Topic / solver | Owner tool | Kind | Cross-checked by | Decision | Notes |
|---|---|---|---|---|---|
| {{TOPIC_1}} | {{TOOL_A}} | derivation | — | D-002 | |
| {{TOPIC_1}} solver | {{TOOL_B}} | implementation | — | D-002 | consumes `symbolic/generated/` only |

<!-- REGISTRY-END -->

## Interoperation

How results pass between the tools — **also the PI's decision**, and part of the registry
rather than something each session settles for itself.

| From | To | What crosses | Mechanism | Decision |
|---|---|---|---|---|
| {{TOOL_A}} | {{TOOL_B}} | coefficient functions | `export_NN_*` → `symbolic/generated/{{LANG_B}}/` | D-002 |

Rules that hold for every route, whatever the PI chooses:

- **Machine-generated, never hand-transcribed**, in any direction, however short, however
  temporary. This is the rule a rushed session breaks first and that costs the most.
- **One direction per fact.** If two tools both write the same quantity, one of them is the
  record and the other is a cross-check — the registry says which.
- **Text, not a tool-specific binary format**, so a hand-off is readable and diffable by
  anything, and `make codegen-check` can compare it.
- **Claude does not invent a route.** Needing a quantity in a tool the registry does not
  deliver it to is a question for the PI, not an opportunity to add a converter.

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
