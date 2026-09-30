---
name: sync-template
description: Pull harness improvements from the upstream template into this project without touching any scientific content. Diffs only the reusable layer, reports what changed, and applies nothing the PI has not approved.
disable-model-invocation: true
argument-hint: "[optional: path or URL of the upstream template]"
allowed-tools: Bash(git status) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git fetch *) Bash(make check) Read Edit Write
---

# Sync the harness from upstream

This project was started from a template. The template keeps improving — a hook gets a bug
fixed, a checker gets a new case, a failure mode gets written down. This pulls those in
**without touching a single line of science.**

## The layer that syncs, and the layer that never does

| Syncs | Never syncs |
|---|---|
| `.claude/hooks/`, `.claude/rules/`, `.claude/agents/` | `docs/STATUS.md`, `docs/conventions.md` |
| `.claude/skills/` **except** project-specific trigger phrases | `docs/decision_log.md`, `docs/status_history.md` |
| `scripts/` (checkers, wrappers, helpers) | `docs/reproduction_and_extension.md`, `handoff.md` |
| `Makefile`, `.github/workflows/` | `docs/toolchain.md`'s registries |
| `docs/GUIDE.md`, `docs/WORKFLOW.md`, `docs/validation_protocol.md`, `docs/source_audit_template.md` | `derivation/`, `symbolic/`, `src/`, `tests/`, `validation/`, `reports/`, `papers/`, `notes/`, `code/` |
| `docs/failure_modes.md` **Part 1 only** | `docs/failure_modes.md` Parts 2–3 (this project's own) |
| `CLAUDE.md` §§1, 3, 4, 6, 8–11 (the discipline) | `CLAUDE.md` §2, §5 and every `{{PLACEHOLDER}}`-derived value |

The split works because the reusable layer never imports project content. Where a file is
split down the middle — `CLAUDE.md`, `failure_modes.md` — **show the PI the diff and let them
decide section by section.** Never merge those automatically.

## Steps

1. **Locate upstream.** Use `$ARGUMENTS` if given; otherwise look for a `template` remote, or
   ask the PI for the path or URL. Do not guess.
2. **Diff the syncing paths only.** Report, grouped: fixes, new capabilities, and changes that
   touch a split file. For each, one line on what it does and why it changed — read the
   upstream commit messages rather than inferring from the diff.
3. **Flag divergence.** Any syncing file this project has modified locally is reported
   separately and **never overwritten silently**: a local change to a hook is usually a
   deliberate adaptation, and clobbering it is the one way this command can do real damage.
4. **Apply only what the PI approves**, item by item. Not "all of it" unless they say so.
5. **Run `make check` and `make test`** afterwards, and report. A sync that breaks the checks
   is reverted, not debugged into place.
6. **Log it** in `docs/decision_log.md` — which upstream commit was synced, what was taken,
   and what was deliberately declined. The declines matter most: without them the next sync
   re-proposes everything the PI already rejected.

## Refusals

- Never sync while the working tree is dirty. Checkpoint or commit first.
- Never sync a file in the right-hand column, even when upstream's version looks better. The
  template's `STATUS.md` is a blank; overwriting this project's with it destroys the record.
- Never take a `CLAUDE.md` §2 or §5 change wholesale: those carry this project's objective
  and its tool ownership, which are PI decisions.
