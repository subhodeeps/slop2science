---
name: checkpoint
description: Safe save in the middle of a session. Account for each changed file, run the tool-free checks, refresh the handoff, and propose a commit of work that is in a coherent state. It is the middle option between nothing committed and a full session close.
disable-model-invocation: true
allowed-tools: Bash(make check) Bash(make test) Bash(git status) Bash(git status *) Bash(git diff *) Bash(git log *) Read Edit Write
---

# Checkpoint

Use this skill in the middle of a session. Use it when a piece of work reaches a coherent state
and you want to save it without a close. `/session-close` is the end of a session. A checkpoint is a
landing.

Use it in these cases:

- a derivation stage passes its checks
- a solver change is green
- an audit has a write-up
- a long session is about to cross a usage limit
 **It is also the right action
when uncommitted work has accumulated.** A working tree that has had changes for hours makes the
orphan check hard.

## Steps

1. **Run `git status` and `git diff --stat`.** List what changed.

2. **Account for each file**, as at `/session-close`. State which step produced the file and why
   you expect it. Report by name now each file that you cannot account for. Do not carry it
   forward. An unexplained file gets harder to explain with each hour that passes
   (`docs/failure_modes/inherited.md` entry 5).

3. **Decide if the state is coherent.** A checkpoint commits work that stands on its own:
   - a stage script **and** its write-up, together. Never commit one without the other.
   - code **and** its test
   - a record **and** what produced it

   If the work is in the middle of an edit, say so and **do not propose a commit.** Refresh the
   handoff (step 5) and stop. A half-finished stage in the history is worse than an uncommitted
   stage.

4. **Run the checks that apply.** Always run `make check`. It needs no toolchain. Run `make test`
   if code changed. Run `make codegen-check TOPIC=…` if an export changed. Report the actual
   output. **If a check fails, do not propose a commit.** Report only what failed.

5. **Refresh `handoff.md`.** Overwrite it with the real state of the work now
   (`docs/handoff_guide.md`: the four headings, and what to keep out). This step makes a
   checkpoint worth doing even when you commit nothing. The next session gets its opening
   context from this file, with its age (`.claude/hooks/session_context.sh`). If the work is in
   the middle of an edit, say so here. That is the most useful line that a returning session can
   read.

6. **Propose a commit.** Use a conventional, scoped message. List the checks that you ran and
   their results. **Do not commit or push** unless the PI says so (CLAUDE.md §1).

## What a checkpoint does *not* do

A checkpoint does not update `docs/STATUS.md`, `docs/reproduction_and_extension.md`, the
decision log or the checklist. Those updates belong to `/session-close`. If you do them in
pieces during a session, the status file describes a state that the repository never had. The
handoff is the record of the middle of a session. STATUS is the record of a session.

## Report

Write fewer than 12 lines. Include these items:

- the changed files
- the checks that you ran, with their results
- each file that you cannot account for
- whether you propose a commit (and if not, why)
- the one next action
