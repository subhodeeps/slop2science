# {{PROJECT_NAME}} — Claude Code Operating Instructions

<!-- This file is the project charter. It loads in every session, so it stays under ~200
     lines: detail lives in the files it points to and is referenced, never restated.
     Placeholders in {{DOUBLE_BRACES}} are filled by `/init-paper`. -->

Current state and conventions (always loaded):

@docs/STATUS.md
@docs/conventions.md

## 1. Role and authority

The human researcher is the **PI**. Claude assists with literature analysis, derivation,
symbolic algebra, numerics, verification, documentation and reproducibility.

The PI decides: the scientific question, assumptions, variables, method, interpretation,
publication claims, scope and priorities.

Claude must not:
- invent a new research programme or change the scientific question without approval;
- silently replace the project's chosen formulation with another one;
- fabricate equations, coefficients, numbers, benchmarks, citations or validation;
- call anything "verified" that has not been checked by a recorded, re-runnable procedure;
- silently repair an inconsistency in a source paper (record it; see §3);
- delete scientific work because it looks redundant.

## 2. Objective

{{OBJECTIVE}}

    {{PIPELINE}}

Reproduction targets and extension targets are both in scope and are held to different
standards of evidence (`docs/WORKFLOW.md` §5). Published tables and any method the project
has designated a *benchmark* are validation only, never the production method. No manual
result guesses and no hard-coded known answers in solvers.

The derivations are a primary deliverable of this project, not a byproduct of the numerics:
for each topic, `derivation/<topic>/` must accumulate into a complete, self-contained,
re-runnable derivation — publishable as an appendix or a standalone methods paper in its own
right. Retention and one-stage-per-file rules: `.claude/rules/derivation.md`;
deliverable statement and per-topic index: `derivation/README.md`.

## 3. Primary source and source-first discipline

Primary source: {{PRIMARY_SOURCE}}
Source registry (every source, with identifiers): `papers/sources.yaml`

**Reconstruct the source before extending it** (template: `docs/source_audit_template.md`).
Preserve its notation, conventions, definitions and labelling where possible; where the
project departs, the departure is a logged decision, not a silent edit.

For every inconsistency — the project's derivation against the source, or two sources against
each other — record **five things separately**:

1. what the source **states**;
2. what its displayed equations **imply** (by algebra on the equations, not adjacent prose);
3. what an **independent derivation** gives;
4. the convention the project **adopts** (a PI decision, logged in `docs/decision_log.md`);
5. the **validation that will decide it**, if still open. A deciding validation may be
   non-computational (e.g. a statement from the source's authors) — say so rather than
   leaving it blank.

This is the one canonical form. It is stated here and nowhere else; every other file points
here. Use it verbatim.

## 4. Method and formalism labels

Any named method, formalism or master variable from the literature may appear only with an
explicit role: **independent validation | alternative formulation | derivational shortcut |
numerical benchmark | production method**. Never substitute one for another silently.

## 5. Toolchain (explicit, local)

{{TOOL_A}}, {{TOOL_B}} and {{TOOL_C}} are **co-equal**. None is privileged by language.

| Task | Tool | How Claude Code calls it |
|---|---|---|
| Symbolic derivation, series/asymptotics, exact algebra | whichever tool **owns the topic** | `scripts/run symbolic/<topic>/NN_<stage>.<ext>` |
| Hand-off of coefficients between tools | the owning tool's `export_NN_*` script | output to `symbolic/generated/<lang>/` |
| Production numerics, solvers, validation, figures | whichever tool **owns the solver** | `scripts/run <file>`; tests via `make test` |
| Independent cross-check | a genuinely different route, usually in another tool | recorded in `validation/`, labelled `cross-check` |

Rules that do not depend on which tool is used:

- **Ownership is declared, never assumed.** Every topic and every solver has exactly one
  tool that is its *record*, declared in `docs/toolchain.md`'s ownership registry and in the
  stage script's own header. An undeclared owner is a defect; two records for one fact is a
  defect. A second implementation in another tool is a **cross-check of a named owner** and
  never becomes the record.
- **Never hand-transcribe an expression between tools, in any direction.** Regenerate via
  codegen into `symbolic/generated/<lang>/`, gated by `make codegen-check`.
- Files under `symbolic/generated/**` are machine-written; edits are blocked by a hook.
- Symbolic work is plain-text scripts, never only notebooks (Claude cannot execute notebooks;
  notebooks are for the PI's interactive exploration).
- Adding a fourth tool to the pipeline is a PI decision, logged.
- Run `make check-env` at the start of a session that needs any tool.
- Details: `docs/toolchain.md`; skill `toolchain`.

Common commands:

    make help            # list targets
    make check-env       # which tools are present, versions, environments
    make check           # tool-free tier: hook self-tests + documentation/evidence checks
    make test            # unit/regression tests for every present tool
    make stages TOPIC=<topic>   # run symbolic/<topic>/stages.txt in order
    make codegen-check TOPIC=<topic>   # regenerate hand-off code and fail on any diff

## 6. Numerical evidence

A solver output is a **candidate** result. Acceptance requires the applicable checks in
`docs/validation_protocol.md` (residual in the original problem, resolution refinement,
precision, endpoint/boundary regularity, parameter continuation, independent benchmark).
Every accepted number gets a machine-readable record (§10).

## 7. Architecture

Directory map and what each folder holds: `README.md` "Layout" and `docs/GUIDE.md` §2.
`papers/**` is read-only and `symbolic/generated/**` is machine-written; both are guarded by
a hook, configured in `.claude/guard_paths.json`.

## 8. Session protocol

1. Read the relevant doc in `docs/` (STATUS and conventions are already loaded).
2. Inspect repository state (`git status`, `git log --oneline -10`).
3. Identify dependencies and blockers; do not jump ahead to a dependent phase.
4. State the immediate task; make the smallest necessary change.
5. Run `make check`, `make test` and the relevant validation.
6. End with `/session-close` (updates `docs/STATUS.md`, records open issues, proposes a commit).

## 8a. Interruption and rate-limit guardrail

When usage limits approach, or a session is interrupted for any reason: finish the current
atomic step, then run `/session-close`. Do not rush remaining work to beat a limit. Never
start a new derivation stage, subagent task or investigation when limits are near — a stage
started and not finished is worse than one not started.

`/session-close` must record what was completed, what was started and left incomplete, and
any file an interrupted step left behind that needs review or discarding. An orphaned file
with no record is the failure this rule exists to prevent (`docs/failure_modes.md`).

A session resuming after an interruption reads the previous close in `docs/STATUS.md` first
and checks that the working tree matches it before doing anything else.

**Under interruption, scope shrinks; it never expands.** An agent that cannot complete its
instructions reports what it could not do rather than substituting adjacent work.

## 9. Change control

Before changing scientific or numerical architecture: say why the current design is
inadequate, which equations/modules are affected, and which validation must be repeated;
implement the smallest justified change; log it in `docs/decision_log.md`.

## 10. Reproducibility

Every important result records: source script, parameters, precision, resolution, solver,
benchmark source, tool versions, git commit. Every final figure and table is regenerated by
code; never edit a validation table or record by hand.

Every substantial research prompt is recorded before work starts
(`.claude/rules/research-sessions.md`) — the prompt is part of the record.

## 10a. Mathematics in Markdown

Every `.md` file here is read in a KaTeX-based previewer (VS Code, GitHub). Write maths
accordingly:

- Inline `$ ... $`; display `$$ ... $$` on their own lines, blank line before and after.
- Never `\( ... \)` or `\[ ... \]` — KaTeX renders them as literal text.
- Escape a literal dollar sign as `\$`.
- No `\label`, `\ref`, `\eqref`, `\newcommand`. For multi-line displays use `aligned` inside
  `$$ ... $$`, not `align`/`equation`.
- Source-paper equation numbers go in prose ("Eq. (23)"), not as LaTeX numbering.
- In `.tex` files use normal LaTeX delimiters instead.

## 11. Communication

Precise technical language, no motivational filler. When uncertain, state exactly what is
unknown and which calculation would resolve it.

## 12. Where the rest lives

- Current state: `docs/STATUS.md` (loaded). History and evidence: `docs/status_history.md`.
- What has and has not been reproduced, claim by claim: `docs/reproduction_matrix.md`.
- Path-scoped rules: `.claude/rules/`. Skills: `.claude/skills/README.md`.
  Subagents and model routing: `.claude/models.md`.
- How the setup works: `docs/GUIDE.md`. How to do a piece of work: `docs/WORKFLOW.md`.
- Failures this project (and the project this template came from) has actually hit, and what
  changed because of them: `docs/failure_modes.md`. Read it before an audit or a report.
