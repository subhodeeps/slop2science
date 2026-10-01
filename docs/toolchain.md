# Toolchain and tool ownership

Mathematica, Julia and Python are **equal in capability**: any of them can own any topic.
Which one does, when nobody chose, is the **default profile** below.

**The PI decides what is implemented in which language, and how the tools interoperate**
(CLAUDE.md §1, §5): per topic, or by adopting the default profile. Claude applies that
assignment and does not invent one, does not move work between languages, and does not add or
change a hand-off between tools. Every assignment is a PI decision with a
`docs/decision_log.md` entry; where neither a registry row nor the default profile covers the
work at hand, **stop and ask the PI** rather than picking the obvious option.

Execution details (the common wrapper, environments, precision, hand-off): the `toolchain`
skill. Rules a checker enforces: `.claude/rules/derivation.md`,
`.claude/rules/implementation.md`.

## Default profile

A standing PI decision, so that a project never stops to ask "which language?" about work whose
answer is not in doubt. It assigns by **kind of work**, not by a preference for a language:

| Kind of work | Default owner | Why |
|---|---|---|
| **Algebra**: tensor calculus, series and asymptotics, symbolic reduction, exact identities, limits, and exporting coefficients | **Mathematica**, as plain-text `.wls` scripts run through `scripts/run` | a mature symbolic engine; scripts, never notebooks, are the record |
| **Numerics**: solvers, eigenproblems, ODE/PDE, root finding, precision and convergence studies, validation drivers | **Julia** (`src/julia`) | speed and arbitrary precision together; written generic in the element type |
| **Anything with a better Python ecosystem**: plotting, machine learning, statistics and fitting, data wrangling and file formats, fetching, repository tooling | **Python** (`src/python`) | the libraries decide this one, not the language |

Default routes between them (the PI may change any of them):

| From | To | What crosses | Mechanism |
|---|---|---|---|
| Mathematica | Julia | coefficient functions | `export_NN_*.wls` → `symbolic/generated/julia/` |
| Mathematica | Python | an expression Python needs (rare) | `export_NN_*.wls` → `symbolic/generated/python/` |
| Julia | Python | results to plot or analyse | JSON records in `validation/<topic>/records/`, data files in `data/` |
| Python | Julia, Mathematica | **nothing, as physics** | a quantity Python computes for another tool needs its own registry row |

**When it applies.** When the PI chose "defaults" at `/init-paper`, and also when the PI did not
choose. That is deliberate: the alternative is a project that stops to ask about work whose
answer is not in doubt. It does not apply if the PI declined it ("ask me each time"), and it
never applies silently:

1. **Applying it means writing it down.** Before the work starts, the topic gets a row in the
   registry below, citing the decision that adopted the profile. `make check-docs` fails if a
   topic has stage scripts and no row.
2. **A task that straddles kinds splits at the hand-off.** A derivation whose result is then
   evaluated numerically is two pieces of work: Mathematica derives and exports, Julia consumes.
3. **Work that fits no kind, or whose kind is unclear, is a question for the PI.** The profile
   covers three kinds; it is not a licence to extend itself.
4. **Python never becomes a second record of physics.** A figure or a fit is a view of a
   record. A Python re-implementation of an algebra or numerics result is a cross-check of a
   named owner, labelled as one.
5. **The PI can override at any time**, per topic or per kind. That is a new logged decision,
   and the profile still applies to everything it did not override.
6. **A machine without the default owner does not reassign the work.** A session there can
   audit, plan and write up, and says so. Moving the work to another tool is the PI's call.

**How it is adopted.** `/init-paper` shows this table and asks. The PI can accept it, override
parts of it, or decline it. Accepting it, or skipping the question, records decision `D-002`
("adopted the default profile", saying which of the two it was), and the init report says so
in its first lines, so a default is never one nobody knew had been chosen.

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

Filled by `/init-paper` from the PI's answers, or from the default profile where the PI did
not choose, and changed only by a PI decision. Every row
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
- **Claude does not invent a route.** Needing a quantity in a tool that neither the registry
  nor the default routes deliver it to is a question for the PI, not an opportunity to add a
  converter.

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
