# Guide — how Claude Code drives this repository

This guide is for a researcher who has never used Claude Code. It explains the **mechanism**.
`docs/WORKFLOW.md` explains how to do a piece of work with it.

## 1. What Claude Code is, here

Claude Code is an agentic command-line tool. You give it a prompt in a terminal. It reads
files, runs shell commands, edits and writes files, and reports back. It works inside the
permissions that this repository grants. Each claim that it makes about the science of this
project must have a command behind it. Claude must have run the command, and you must be able to
run it again.

Files under version control shape everything that Claude does here. Nothing private to an
account or a model shapes it. **The configuration is part of the reproducibility record**, like
a derivation script.

## 2. The configuration, and when each piece acts

| Piece | When it acts | Purpose |
|---|---|---|
| `CLAUDE.md` | every session, always | The charter. It states **the authority of the PI and the decisions that belong to the PI**. These include which language implements which work, and how the tools interoperate (by choice or by the default profile). It states the two parts of the project, reproduction and new work. It states source-first discipline, the five-item discrepancy form, the toolchain rules, the session protocol and the interruption guardrail. It is short on purpose. It references detail and never restates it. `make check-docs` checks its size budget, because a file that loads in every session grows by accretion. |
| `docs/STATUS.md`, `docs/conventions.md` | every session (`CLAUDE.md` imports them with `@`) | The current state only (reproduction **and** extension), and the conventions register. They have a budget and a check, because they load every time. The history is in `docs/status_history.md`, which does not load. |
| `.claude/rules/*.md` | automatically, when Claude reads a file that matches the `paths:` of the rule | Narrow constraints for specific paths. You never invoke them. If Claude touches a matching file, the rule loads. |
| `.claude/skills/*/SKILL.md` | when its `description` or `when_to_use` matches the task, or by name (`/skill-name`) | Procedures: how to do a category of work. Each skill has about 100 lines or fewer. Occasional detail is in the `reference/` of the skill. It loads only when needed. |
| `.claude/agents/*.md` | you dispatch it, or the session decides that a subtask fits | Subagents. Each has a separate context window with its own tools, skills and model. |
| `.claude/hooks/*` | on the tool-use or session event that `.claude/settings.json` names, or in the frontmatter of a subagent | Enforcement that does **not** depend on the model that follows an instruction. Hooks also run the continuity machinery: the handoff that the session start injects with its age, a snapshot before compaction, and a condensed transcript outside the repository. |
| `handoff.md` | the opening context of each session, **with its age** | Prose from the last session to the next session: what was in progress, what someone suspects but did not show, and what to watch for. Write it at `/checkpoint` and `/session-close`. `docs/handoff_guide.md` explains how to write one. It is committed and shareable, unlike the transcript. It is never evidence. If something in it is worth relying on, establish it and move it to a record. |
| `.claude/settings.json` | every session | Permissions, environment and hook registration. |
| `.claude/models.md` | read by you and by the frontmatter of agents | The one place that records model choices. |
| `Makefile` | on demand | The canonical commands. Skills and the session protocol call these commands. They do not use raw tool calls. |

Nothing is hidden. If you want to know why Claude Code did something here, one of these files
has the answer. A model that you cannot inspect does not have it.

## 3. A session, from start to close

1. Claude Code loads `CLAUDE.md`, `docs/STATUS.md` and `docs/conventions.md`.
   `session_context.sh` prints which tools are present, the current phase and the next task.
2. You give a prompt. Record a substantial research prompt word for word in
   `docs/prompts/<ID>_<topic>.md` **before** the work starts
   (`.claude/rules/research-sessions.md`).
3. The work happens: derivation, implementation, literature and verification. Claude does it
   directly or through subagents (§4).
4. `make check`, `make test` and the relevant validation run before anyone calls anything done.
5. The session ends with `/session-close`. Claude accounts for each changed file, updates STATUS
   and the reproduction matrix, records decisions, and proposes a commit. Claude never makes
   the commit by itself.
6. The next session reads that close before it does anything else.

## 4. Subagents: why, and which one

A subagent is a separate context window with its own tools and model. There are two reasons to
use one. First, a large or noisy task fills the context of the session with material that the
session does not need to keep. Examples: a full derivation or a literature sweep. Second, a role
that must be independent can have a structure that stops it from seeing or touching what it
checks.

| Subagent | For | Notes |
|---|---|---|
| `derivation` | symbolic derivation, source reconstruction, asymptotics, limits | It writes `symbolic/**` and `derivation/**`. It has project memory for confirmed conventions and pitfalls. It has no memory of results. |
| `implementation` | solvers, discretization, convergence, precision | It takes physics only from `symbolic/generated/`. It never invents an equation. |
| `literature` | sources, benchmarks, reconciliation of conventions | It is the only agent with web access. It is the only agent that writes under `papers/`. |
| `verification` | independent audit after each derivation, export, solver change or result | **It cannot edit project files, even if it wants to.** A hook blocks it. It reports findings. It does not fix them. |
| `paper-writer` | the report or paper of a topic | It uses only script-verified equations as results and only recorded numbers. It writes in chunks. One author writes the document. |
| `status-reporter` | factual status and progress reports | It never derives or verifies. Each claim traces to a named file. |
| `explore` | fast read-only lookup before substantive work | It returns file:line and an excerpt. It does not synthesize. The caller does that. |

`.claude/models.md` has the model routing and the reasoning behind it.

## 5. How the tools connect

The project derives physics one time, in the tool that owns the topic. Nobody ever transcribes
it by hand:

    symbolic/<topic>/stage_NN_*.<ext>        the derivation, with labelled printed checks
            |  scripts/run  (serialises kernels, applies a timeout, logs to logs/)
            v
    symbolic/<topic>/out/*                   the record of the owning tool for the run
            |
    symbolic/<topic>/export_NN_*.<ext>       codegen
            v
    symbolic/generated/<lang>/               machine-written; a hook blocks Edit and Write
            |  make codegen-check            regenerates and fails on any diff from git
            v
    src/<lang>/                              production code; uses generated code only
            |  scripts/run
            v
    validation/<topic>/                      results, residuals, convergence, JSON records

If a solver needs a coefficient that is not in `symbolic/generated/`, stop. Derive it and
export it. Never write it by hand "for now".

## 6. What the system enforces, and what depends on the prompt

**The system enforces these rules whatever a prompt says** (hooks, not instructions):

- Nobody can edit `papers/**`, `symbolic/generated/**`, `validation/**/records/**`,
  `validation/**/accepted/**` and `data/accepted/**` directly. `guard_paths.py` enforces this,
  with the configuration in `.claude/guard_paths.json`.
- `Write` cannot overwrite an existing derivation stage or export script. The same hook
  enforces this.
- The `verification` subagent cannot write project files. `readonly_agent.py` enforces this.
- **No subagent can push, commit, rebase, reset, branch or stage everything.**
  `subagent_git_guard.py` enforces this. The frontmatter of each subagent that can use Bash
  registers it. A subagent can read git. It cannot change the history or the remote. A
  subagent has a fresh context and cannot see what else is in progress. Therefore the main
  session proposes the commit.
- `log_prompt.py` captures each prompt.
- `precompact_checkpoint.sh` writes a state snapshot before each compaction.
- `capture_session.py` keeps a condensed transcript **outside the repository**.

**You can run these checks on demand, with no scientific toolchain.** `make check` runs these
checks:

- the hook self-tests (synthetic payloads through each hook, so that you notice a broken guard)
- reference resolution
- evidence-tag resolution
- the staleness guard
- the language rule: `make lint-ste-md` fails if a Markdown file breaks a measurable ASD-STE100
  rule, and `make test-checks` fails if the charter, the rule, an agent or the session hook loses
  the requirement

The same tier runs in CI on each push.

**These items depend on the prompt and on the model that follows it:**

- correct use of the five-item form
- the claim "verified" only for what a re-runnable procedure checked
- print-before-assert in a new script
- a session that stops at a usage limit and does not hurry
- **asking the PI, not choosing a default,** when a decision belongs to the PI. No hook can
  enforce this. The other items depend on it.

These items are process. They are not code. `docs/WORKFLOW.md` §8 and `docs/failure_modes.md`
explain what to watch for. If an instruction here keeps failing, move it from prose into a rule,
then into a skill, then into a hook. This is the order of increasing strength.
