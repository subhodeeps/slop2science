---
name: checkpoint
description: Mid-session safe save - account for every changed file, run the tool-free checks, refresh the handoff, and propose a commit of work that is in a coherent state. The middle ground between nothing committed and a full session close.
disable-model-invocation: true
allowed-tools: Bash(make check) Bash(make test) Bash(git status) Bash(git status *) Bash(git diff *) Bash(git log *) Read Edit Write
---

# Checkpoint

For the middle of a session, when a piece of work has reached a coherent state and should be
saved without closing. `/session-close` is the end of a session; this is a landing.

Use it when: a derivation stage passes its checks, a solver change is green, an audit is
written up, or a long session is about to cross a usage limit. **It is also the right answer
when uncommitted work has been accumulating** — a working tree that has been dirty for hours
is a session whose orphan check is already going to be hard.

## Steps

1. **`git status` and `git diff --stat`.** List what changed.

2. **Account for every file**, as at `/session-close`: which step produced it and why it is
   expected. Anything you cannot account for is reported by name now, not carried forward —
   an unexplained file gets harder to explain with every hour that passes
   (`docs/failure_modes.md` entry 5).

3. **Is this a coherent state?** A checkpoint commits work that stands on its own:
   - a stage script **and** its write-up, together — never one without the other;
   - code **and** its test;
   - a record **and** whatever produced it.

   If the work is genuinely mid-edit, say so and **do not propose a commit.** Refresh the
   handoff (step 5) and stop. A half-stage in the history is worse than an uncommitted one.

4. **Run the checks that apply.** `make check` always — it needs no toolchain. `make test` if
   code changed. `make codegen-check TOPIC=…` if an export changed. Report actual output.
   **A failing check means no commit is proposed**, only a report of what failed.

5. **Refresh `handoff.md`.** Overwrite it with where the work actually stands right now
   (`docs/handoff_guide.md` — the four headings, and what not to put in it). This is the step
   that makes a checkpoint worth doing even when nothing gets committed: the next session's
   opening context comes from this file, with its age
   (`.claude/hooks/session_context.sh`). If the work is mid-edit, say so here — that is the
   single most useful line a returning session can read.

6. **Propose a commit**: conventional, scoped, listing the checks actually run and their
   results. **Do not commit or push** unless the PI says so (CLAUDE.md §1).

## What a checkpoint does *not* do

It does not update `docs/STATUS.md`, `docs/reproduction_and_extension.md`, the decision log
or the checklist. Those are `/session-close`'s job, and doing them piecemeal mid-session is
how a status file comes to describe a state the repository was never in. The handoff is the
mid-session record; STATUS is the session record.

## Report

Under 12 lines: files changed, checks run with results, anything unaccounted for, whether a
commit is proposed (and if not, why), and the one next action.
