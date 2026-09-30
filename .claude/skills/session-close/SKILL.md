---
name: session-close
description: End-of-session procedure - account for every changed file, run the checks, update STATUS and the reproduction matrix, record decisions and open issues, and propose (never perform) a commit.
disable-model-invocation: true
model: haiku
allowed-tools: Bash(make check) Bash(make test) Bash(make codegen-check *) Bash(git status) Bash(git status *) Bash(git diff *) Bash(git log *) Read Edit Write
---

# Session close

Run at the end of every session, and **instead of** finishing remaining work when a usage
limit is near or the session was interrupted (CLAUDE.md §8a).

1. **What changed.** `git status` and `git diff --stat`.

2. **Orphaned-artefact check.** List every untracked and modified file and account for each
   one: which step produced it, and why it is expected. Any file left over from an
   interrupted step, or from a step that ran past its prompt's stated scope, is reported **by
   name with a disposition** — kept-and-flagged / reviewed-and-fine / needs PI decision. Never
   silently committed, never silently deleted. This check exists because an unrequested
   script once sat in a validation directory for weeks with nothing recording where it came
   from (`docs/failure_modes.md`).

3. **Checks.** Run `make check` (always — it needs no toolchain). Run `make test` if code
   changed. If stage or export scripts changed, run `make stages TOPIC=<topic>` and
   `make codegen-check TOPIC=<topic>`.

   Report **every** unresolved reference and every staleness warning `make check` prints. A
   session does not close silently over a broken reference it can see. A genuine finding is
   fixed at its source before the commit is proposed — or, if it is a false positive, the
   checker is corrected. It is never left unmentioned.

4. **History, then state.** Append this session's full record — what was done, the evidence,
   the commits — to the end of `docs/status_history.md`. *Then* update `docs/STATUS.md`,
   which holds current state only, loads every session, and stays under ~100 lines:

   - current phase; one concrete immediate next task;
   - move an item between *Derived*, *Validated* and *Open* **only with the evidence**
     (script path + command + result). Nothing is "validated" without a re-runnable check;
   - **if the session was interrupted or hit a usage limit**: say explicitly what was
     completed versus started-and-left-incomplete, so the next session does not resume from a
     false picture;
   - last validation: date, command, outcome, commit.

5. **Reproduction matrix.** Update `docs/reproduction_matrix.md` for anything reproduced,
   attempted, or found discrepant this session. This is the row the PI actually looks at.

6. **Decisions and prompts.** Append any PI decisions to `docs/decision_log.md` in the
   `D-NNN` form. Fill in the `## Outcome` section of this session's prompt record in
   `docs/prompts/`.

7. **Checklist.** Tick completed boxes in `docs/implementation_checklist.md` — only with
   evidence.

8. **Propose a commit** message: conventional, scoped, listing the checks actually run and
   their results. **Do not commit or push** unless the PI says so.

9. **Report**, under 20 lines: changed files, checks run with results, orphaned artefacts
   found and their disposition, open issues, and the next task.
