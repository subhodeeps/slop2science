# Guide — how this repository is driven by Claude Code

For a researcher who has never used Claude Code. It explains the **mechanism**;
`docs/WORKFLOW.md` explains how to actually do a piece of work with it.

## 1. What Claude Code is, here

An agentic CLI: you give it a prompt in a terminal, and it reads files, runs shell commands,
edits and writes files, and reports back — within the permissions this repository grants it.
Every claim it makes about this project's science is expected to be backed by a command it
actually ran and that you can rerun.

Everything it does here is shaped by files under version control, not by anything private to
an account or a model. That is the point: **the configuration is part of the reproducibility
record**, like a derivation script.

## 2. The configuration surface, and when each piece fires

| Piece | Fires | Purpose |
|---|---|---|
| `CLAUDE.md` | every session, always | The charter: **the PI's authority and what is the PI's to decide** (including which language implements what, and how the tools interoperate), the project's two halves — reproduction and new work — source-first discipline, the five-point discrepancy form, toolchain rules, session protocol, the interruption guardrail. Kept deliberately short — detail is referenced, never restated — and its size budget is checked by `make check-docs`, because a file that loads every session grows by accretion. |
| `docs/STATUS.md`, `docs/conventions.md` | every session (`@`-imported by `CLAUDE.md`) | Current state only (reproduction **and** extension), and the conventions register. Budgeted and checked, because they load every time; history lives in `docs/status_history.md`, which does not. |
| `.claude/rules/*.md` | automatically, when Claude reads a file matching the rule's `paths:` | Narrow, path-scoped constraints. You never invoke these; touching a matching file loads them. |
| `.claude/skills/*/SKILL.md` | when its `description`/`when_to_use` matches the task, or by name (`/skill-name`) | Procedures: how to do a category of work. Each under ~100 lines; occasional detail sits in the skill's `reference/`, loaded only if needed. |
| `.claude/agents/*.md` | dispatched by you, or by the session judging a subtask fits | Subagents: separate context windows with their own tools, skills and model. |
| `.claude/hooks/*` | on the tool-use or session event named in `.claude/settings.json`, or in a subagent's own frontmatter | Enforcement that does **not** depend on the model following an instruction. Also the continuity machinery: the handoff injected at session start with its age, a snapshot written before compaction, and a condensed transcript kept outside the repository. |
| `handoff.md` | read into the opening context at every session start, **with its age** | Prose from the last session to the next: what was in progress, what is suspected but unshown, what to watch out for. Written at `/checkpoint` and `/session-close`; how to write one is `docs/handoff_guide.md`. Committed and shareable — unlike the transcript. Never evidence: anything in it worth relying on gets established and moved to a record. |
| `.claude/settings.json` | every session | Permissions, environment, hook registration. |
| `.claude/models.md` | read by you and by agent frontmatter | The one place model choices are recorded. |
| `Makefile` | on demand | The canonical commands. Skills and the session protocol invoke these rather than raw tool calls. |

Nothing is hidden. If you want to know why Claude Code did something here, the answer is in
one of those files, not in a model you cannot inspect.

## 3. A session, start to close

1. Claude Code loads `CLAUDE.md` + `docs/STATUS.md` + `docs/conventions.md`;
   `session_context.sh` prints which tools are present, the current phase and the next task.
2. You give a prompt. A substantial research prompt is recorded verbatim in
   `docs/prompts/<ID>_<topic>.md` **before** work starts
   (`.claude/rules/research-sessions.md`).
3. Work happens — derivation, implementation, literature, verification — directly or via
   subagents (§4).
4. `make check`, `make test` and the relevant validation run before anything is called done.
5. The session ends with `/session-close`: account for every changed file, update STATUS and
   the reproduction matrix, record decisions, propose (never perform) a commit.
6. The next session reads that close before doing anything else.

## 4. Subagents: why, and which one

A subagent is a separate context window with its own tools and model. Two reasons to use one:
a large or noisy task (a full derivation, a literature sweep) would otherwise fill the
session's context with material it does not need to keep; and a role with a genuine
independence requirement can be structurally prevented from seeing or touching what it is
checking.

| Subagent | For | Notably |
|---|---|---|
| `derivation` | Symbolic derivation, source reconstruction, asymptotics, limits | Writes `symbolic/**` and `derivation/**`. Has project memory for confirmed conventions and pitfalls — not results. |
| `implementation` | Solvers, discretization, convergence, precision | Consumes physics only from `symbolic/generated/`; never invents an equation. |
| `literature` | Sources, benchmarks, convention reconciliation | The only agent with web access, and the only one that writes under `papers/`. |
| `verification` | Independent audit after any derivation, export, solver change or result | **Cannot edit project files even if it wants to** — a hook blocks it. Reports findings; does not fix them. |
| `paper-writer` | A topic's report or paper | Only script-verified equations as results; only recorded numbers; writes in chunks; one author. |
| `status-reporter` | Factual status and progress reports | Never derives or verifies; every claim traces to a named file. |
| `explore` | Fast read-only lookup before substantive work | Returns file:line and excerpt. No synthesis — the caller does that. |

Model routing, and the reasoning behind it: `.claude/models.md`.

## 5. How the tools connect

Physics is derived once, in whichever tool owns the topic, and **never hand-transcribed**:

    symbolic/<topic>/stage_NN_*.<ext>        the derivation, with labelled printed checks
            |  scripts/run  (serialises kernels, applies a timeout, logs to logs/)
            v
    symbolic/<topic>/out/*                   the owning tool's own record of the run
            |
    symbolic/<topic>/export_NN_*.<ext>       codegen
            v
    symbolic/generated/<lang>/               machine-written; Edit/Write blocked by a hook
            |  make codegen-check            regenerates and fails on any diff from git
            v
    src/<lang>/                              production code; consumes generated code only
            |  scripts/run
            v
    validation/<topic>/                      results, residuals, convergence, JSON records

If a coefficient a solver needs is not in `symbolic/generated/`, the correct response is to
stop and derive and export it — never to write it by hand "for now".

## 6. Enforced automatically vs. depends on the prompt

**Enforced regardless of what any prompt says** (hooks, not instructions):

- `papers/**`, `symbolic/generated/**`, `validation/**/records/**`, `validation/**/accepted/**`
  and `data/accepted/**` cannot be edited directly — `guard_paths.py`, configured in
  `.claude/guard_paths.json`.
- An existing derivation stage or export script cannot be overwritten by `Write` — same hook.
- The `verification` subagent cannot write project files — `readonly_agent.py`.
- **No subagent can push, commit, rebase, reset, branch or stage-everything** —
  `subagent_git_guard.py`, registered in each Bash-capable subagent's frontmatter. Reading git
  is allowed; changing history or the remote is not. A subagent has a fresh context and cannot
  see what else is in flight, so the commit is the main session's to propose.
- Every prompt is captured — `log_prompt.py`.
- A state snapshot is written before every compaction — `precompact_checkpoint.sh`.
- A condensed transcript is kept **outside the repository** — `capture_session.py`.

**Checked on demand, with no scientific toolchain needed**: `make check` runs the hook
self-tests (synthetic payloads through each hook, so a broken guard is noticed), reference
resolution, evidence-tag resolution, and the staleness guard. The same tier runs in CI on
every push.

**Depends on the prompt, and on the model actually following it**: the five-point form being
used correctly; "verified" being claimed only for what a re-runnable procedure checked;
print-before-assert in a new script; a session actually stopping at a usage limit rather than
rushing; and **asking the PI rather than defaulting** when a decision is the PI's — the one
guarantee here that no hook can enforce, and the one the rest depends on. These are process, not code. `docs/WORKFLOW.md` §8 and `docs/failure_modes.md` cover
what to watch for — and if an instruction here keeps being missed, the fix is usually to move
it from prose into a rule, a skill, or a hook, in that order of strength.
