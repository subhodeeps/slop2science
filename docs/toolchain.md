# Toolchain and tool ownership

Mathematica, Julia and Python have **equal capability**. Any of them can own any topic. If
nobody chose, the **default profile** below decides which one owns the topic.

**The PI decides which language implements which work, and how the tools interoperate**
(CLAUDE.md §1, §5). The PI decides per topic, or adopts the default profile. Claude applies that
assignment. Claude does not invent an assignment. Claude does not move work between languages.
Claude does not add or change a hand-off between tools. Each assignment is a PI decision with an
entry in `docs/decision_log.md`. If neither a registry row nor the default profile covers the
work, **stop and ask the PI.** Do not pick the obvious option.

For execution details (the common wrapper, environments, precision, hand-off), see the
`toolchain` skill. For the rules that a checker enforces, see `.claude/rules/derivation.md` and
`.claude/rules/implementation.md`.

## Default profile

This is a standing PI decision. A project then does not stop to ask "which language?" about work
whose answer is not in doubt. It assigns by **kind of work**. It does not assign by a preference
for a language:

| Kind of work | Default owner | Why |
|---|---|---|
| **Algebra**: tensor calculus, series and asymptotics, symbolic reduction, exact identities, limits, and export of coefficients | **Mathematica**, as plain-text `.wls` scripts that run through `scripts/run` | It is a mature symbolic engine. Scripts are the record. Notebooks are never the record. |
| **Numerics**: solvers, eigenproblems, ODE and PDE, root finding, studies of precision and convergence, validation drivers | **Julia** (`src/julia`) | It combines speed and arbitrary precision. Write the code generic in the element type. |
| **Work that depends on the Python ecosystem**: plotting, machine learning, statistics and fitting, data handling and file formats, fetching, repository tooling | **Python** (`src/python`) | The libraries decide this one. The language does not decide it. |

Default routes between the tools (the PI can change any route):

| From | To | What crosses | Mechanism |
|---|---|---|---|
| Mathematica | Julia | coefficient functions | `export_NN_*.wls` → `symbolic/generated/julia/` |
| Mathematica | Python | an expression that Python needs (rare) | `export_NN_*.wls` → `symbolic/generated/python/` |
| Julia | Python | results to plot or analyse | JSON records in `validation/<topic>/records/`, data files in `data/` |
| Python | Julia, Mathematica | **nothing, as physics** | A quantity that Python computes for another tool needs its own registry row. |

**When the profile applies.** It applies when the PI chose "defaults" at `/init-paper`. It also
applies when the PI did not choose. This is deliberate. The alternative is a project that stops
to ask about work whose answer is not in doubt. It does not apply if the PI declined it ("ask me
each time"). It never applies silently:

1. **To apply it, write it down.** Before the work starts, the topic gets a row in the registry
   below. The row cites the decision that adopted the profile. `make check-docs` fails if a topic
   has stage scripts and no row.
2. **A task that crosses kinds splits at the hand-off.** A derivation whose result is then
   evaluated numerically is two pieces of work. Mathematica derives and exports. Julia consumes.
3. **Work that fits no kind, or whose kind is not clear, is a question for the PI.** The profile
   covers three kinds. It does not extend itself.
4. **Python never becomes a second record of physics.** A figure or a fit is a view of a record.
   A Python implementation of an algebra result or a numerics result is a cross-check of a named
   owner. Label it as a cross-check.
5. **The PI can override the profile at any time**, per topic or per kind. An override is a new
   logged decision. The profile still applies to everything that the override did not change.
6. **A machine without the default owner does not reassign the work.** A session on that machine
   can audit, plan and write up, and it says so. The PI decides if another tool takes the work.

**How the PI adopts it.** `/init-paper` shows this table and asks. The PI can accept it,
override parts of it, or decline it. If the PI accepts it, or skips the question, the project
records decision `D-002`. The record says "adopted the default profile" and gives the route:
chosen, or applied because the PI did not choose. The init report says this in its first lines. Then nobody
overlooks a default that someone chose.

## Why the project declares ownership and does not infer it

Three capable tools make it easy to get two slightly different versions of one equation. One
tool derives it. Another tool derives it again during a debugging session. Someone commits both.
Nothing marks either one as authoritative. Nothing catches this. Both pass their own checks.

Therefore the project keeps one record for each fact. A derivation or solver in a second tool is
a **cross-check** of a named owner. Label it as a cross-check in its header and in `validation/`.
It never becomes the record. If an owner and its cross-check disagree, that is a discrepancy.
Record it in the five-item form. Do not choose silently.

`make check-docs` fails if a topic has stage scripts but no row in the registry below.

## Ownership registry

`/init-paper` fills this registry from the answers of the PI, or from the default profile where
the PI did not choose. Only a PI decision changes it. Each row cites the decision that put it
there. Then "why is this in Julia?" always has an answer.

<!-- REGISTRY-START -->

| Topic / solver | Owner tool | Kind | Cross-checked by | Decision | Notes |
|---|---|---|---|---|---|
| {{TOPIC_1}} | {{TOOL_A}} | derivation | — | D-002 | |
| {{TOPIC_1}} solver | {{TOOL_B}} | implementation | — | D-002 | consumes `symbolic/generated/` only |

<!-- REGISTRY-END -->

## Interoperation

This section states how results pass between the tools. **This is also a PI decision.** It is
part of the registry. A session does not settle it for itself.

| From | To | What crosses | Mechanism | Decision |
|---|---|---|---|---|
| {{TOOL_A}} | {{TOOL_B}} | coefficient functions | `export_NN_*` → `symbolic/generated/{{LANG_B}}/` | D-002 |

These rules hold for every route, whatever the PI chooses:

- **A machine generates the hand-off. Nobody transcribes it by hand**, in any direction, however
  short and however temporary. A rushed session breaks this rule first, and the cost is the
  highest.
- **Each fact has one direction.** If two tools both write the same quantity, one of them is the
  record and the other is a cross-check. The registry states which.
- **Use text. Do not use a binary format that belongs to one tool.** Then anything can read and
  compare a hand-off, and `make codegen-check` can compare it.
- **Claude does not invent a route.** If Claude needs a quantity in a tool that neither the
  registry nor the default routes serve, that is a question for the PI. It is not an opportunity
  to add a converter.

## Division of labour

| Layer | Location | Record |
|---|---|---|
| Derivation: equations, reduction, series and asymptotics, limits | `symbolic/<topic>/stage_NN_*.<ext>` | the scripts, their `out/` files and the logs |
| Hand-off between tools | `symbolic/<topic>/export_NN_*.<ext>` → `symbolic/generated/<lang>/` | a banner that names the generating script and its SHA-256 |
| Production numerics, validation, figures | `src/<lang>/`, `validation/<topic>/` | JSON result records |
| Tests | `tests/<lang>/` | `make test` |
| Independent cross-checks | a different route, usually another tool | labelled `cross-check` in `validation/` |

To add a fourth tool to the pipeline is a PI decision. Log it in `docs/decision_log.md`.

## Mathematica

- Invocation: always use `scripts/run <script.wls>`. It exports `PROJECT_ROOT`, runs from the
  repository root, and serialises kernels with `flock`. Licences commonly limit concurrent
  kernels. This matters as soon as two subagents run at the same time. The wrapper applies
  `SYMBOLIC_TIMEOUT` and writes a log.
- If `wolframscript` is not on `PATH`, set `WOLFRAMSCRIPT=/path/to/wolframscript` in the shell or
  in the `env` of `.claude/settings.local.json`.
- Shared code: `symbolic/common/*.wl`, loaded by path from `PROJECT_ROOT`. Run its self-tests
  before you rely on it.
- **Scripts are the record. Notebooks are not the record.** Notebooks cannot run here. They are
  for the own exploration of the PI, and they live in `notes/`.
- Avoid binary formats that depend on a version. Persist results as text.

## Julia

- Environment: `src/julia` (`Project.toml` **and** `Manifest.toml`, both committed). The manifest
  pins the exact environment behind each result. `make setup` instantiates it.
- Write numerics generic in `T<:AbstractFloat`. Then the same code runs in working precision,
  double-double precision and arbitrary precision.
- Each call pays the cost of start-up and compilation. Batch a task into one script. Do not use
  many invocations.

## Python

- Environment: `src/python`, managed with [uv](https://docs.astral.sh/uv/). Commit
  `pyproject.toml` and `uv.lock`. Do not commit the venv at `src/python/.venv/`. `make setup`
  runs `uv sync`. To add a dependency, run `uv add --project src/python <pkg>`. This updates both
  files. Record the reason in `docs/decision_log.md`.
- `scripts/run <script>.py` runs inside that environment (`uv run --project src/python`). Then a
  result does not depend on which interpreter is first on `PATH`. `PYTHON=...` overrides it
  explicitly. Without uv, a project script fails loudly. It does not run in the wrong place.
- As for Julia, the environment exists only if the project uses Python. If it does not, delete
  `src/python`.
- Libraries: see **Libraries** below.
- Use `mpmath` or `gmpy2` for extended precision. **State where a chain silently drops to machine
  precision.** A NumPy call in the middle of an `mpmath` computation is the usual cause. Nothing
  in the output shows it.
- Python also carries the own checkers and hooks of this repository (`scripts/check_docs.py`,
  `.claude/hooks/*.py`). Those are infrastructure. They are outside the ownership registry.

## Libraries

The PI decides which libraries each environment carries. They are in `src/python/packages.txt`
and `src/julia/packages.txt`, one name on each line, with a reason. `/init-paper` shows the
default and asks what to add or remove. It records the answer as decision `D-003`. If the PI does
not answer, the default applies, and the record says so.

- **Default (the minimum).** Python: numpy, scipy, mpmath, sympy, matplotlib. Julia:
  LinearAlgebra, SparseArrays, Printf, JSON, DoubleFloats, GenericLinearAlgebra, GenericSchur.
  The file gives the reason for each package. The Julia list has no plotting package, because
  figures are Python's by default.
- **`make setup` applies the list**: `uv add` for Python and `Pkg.add` for Julia. Afterwards,
  `pyproject.toml` and `uv.lock`, and `Project.toml` and `Manifest.toml`, are the record of what
  the environment contains. Commit them.
- **To add a library later** is a PI decision. Add a new line with its reason to `packages.txt`.
  Add an entry in `docs/decision_log.md`. Then run `make setup`. Claude proposes a library when
  the work needs one and says why. Claude does not install one by itself. **To remove one**, run
  `uv remove` or `Pkg.rm` and delete the line.
- Mathematica has no package list here. Shared code lives in `symbolic/common/`.

## When a tool is missing

`make check` and each repository check run with no scientific toolchain at all: in CI, on a
borrowed laptop and in a cloud container. `make test` skips an absent language and says so
loudly. `make check-env` reports what is present. It does not fail only because a tool is absent
(use `--strict` where a missing tool must fail).

A session on a machine without the tool that owns the topic can audit, write up, plan and check
references. It **cannot** produce a new verified result. It must say so. It must not reason a
result out.
