---
name: sync-template
description: Pull harness improvements from the upstream template into this project without touching any scientific content. It diffs only the reusable layer and reports what changed. It applies only what the PI approves.
disable-model-invocation: true
argument-hint: "[optional: path or URL of the upstream template]"
allowed-tools: Bash(git status) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git fetch *) Bash(make check) Read Edit Write
---

# Sync the harness from upstream

This project started from a template. The template keeps improving. Someone fixes a bug in a
hook, a checker gets a new case, or someone writes down a failure mode. This skill pulls those
changes in **without touching one line of science.**

## The layer that syncs, and the layer that never syncs

| Syncs | Never syncs |
|---|---|
| `.claude/hooks/`, `.claude/rules/`, `.claude/agents/` | `docs/STATUS.md`, `docs/conventions.md` |
| `.claude/skills/` **except** the trigger phrases of the project | `docs/decision_log.md`, `docs/status_history.md` |
| `scripts/` (checkers, wrappers, helpers) | `docs/reproduction_and_extension.md`, `handoff.md` |
| `Makefile`, `.github/workflows/` | the registries in `docs/toolchain.md` |
| `docs/GUIDE.md`, `docs/WORKFLOW.md`, `docs/validation_protocol.md`, `docs/source_audit_template.md` | `derivation/`, `symbolic/`, `src/`, `tests/`, `validation/`, `reports/`, `papers/`, `notes/`, `code/` |
| `docs/failure_modes.md` (index), `docs/failure_modes/model.md`, `docs/failure_modes/inherited.md` | `docs/failure_modes/project.md` and `docs/failure_modes/anticipated.md` (the own parts of the project) |
| `CLAUDE.md` §§1, 3, 4, 6, 8–11 (the discipline) | `CLAUDE.md` §2, §5 and each value that comes from a `{{PLACEHOLDER}}` |

The split works because the reusable layer never imports project content. One file is split
down the middle: `CLAUDE.md`. For this file, **show the PI the diff and let the PI decide
section by section.** Never merge it automatically.

## Steps

1. **Locate upstream.** Use `$ARGUMENTS` if the PI gives it. Otherwise look for a `template` remote,
   or ask the PI for the path or URL. Do not guess.
2. **Diff the syncing paths only.** Report the changes in groups: fixes, new capabilities, and
   changes that touch a split file. For each change, write one line about what it does and why
   it changed. Read the upstream commit messages. Do not infer this from the diff.
3. **Flag divergence.** Report separately each syncing file that this project modified locally.
   **Never overwrite such a file silently.** A local change to a hook is usually a deliberate
   adaptation. To overwrite it is the one way that this command can do real damage.
4. **Apply only what the PI approves**, item by item. Do not apply "all of it" unless the PI
   says so.
5. **Run `make check` and `make test`** afterwards, and report. If a sync breaks the checks,
   revert it. Do not debug it into place.
6. **Log it** in `docs/decision_log.md`. State which upstream commit you synced, what you took
   and what you declined on purpose. The declines matter most. Without them, the next sync
   proposes again everything that the PI already rejected.

## Refusals

- Never sync while the working tree has uncommitted changes. Checkpoint or commit first.
- Never sync a file in the right-hand column, even if the upstream version looks better. The
  `STATUS.md` of the template is blank. If you overwrite the `STATUS.md` of this project with
  it, you destroy the record.
- Never take a change to `CLAUDE.md` §2 or §5 as a whole. Those sections carry the objective of
  this project and its tool ownership. These are PI decisions.
