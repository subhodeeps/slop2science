---
name: session-close
description: End-of-session procedure. Account for each changed file, run the checks, update STATUS and the reproduction matrix, and record decisions and open issues. Propose a commit. Never make the commit.
disable-model-invocation: true
model: haiku
allowed-tools: Bash(make check) Bash(make test) Bash(make codegen-check *) Bash(git status) Bash(git status *) Bash(git diff *) Bash(git log *) Read Edit Write
---

# Session close

Run this at the end of every session. Run it **instead of** the remaining work when a usage limit
is near or when an interruption stopped the session (CLAUDE.md §8a).

1. **What changed.** Run `git status` and `git diff --stat`.

2. **Orphaned-artefact check.** List each untracked and modified file. Account for each file:
   which step produced it, and why you expect it. Report each
   file that an interrupted step left behind, or that a step created beyond the stated scope of
   its prompt. Report it **by name, with a disposition.** The dispositions are: kept and flagged, reviewed and fine, or needs a PI decision.
   Never commit such a file silently. Never delete it silently. This check exists because an
   unrequested script once stayed in a validation directory for weeks. Nothing recorded where
   it came from (`docs/failure_modes.md`).

3. **Checks.** Always run `make check`. It needs no toolchain. Run `make test` if code changed.
   If stage or export scripts changed, run `make stages TOPIC=<topic>` and
   `make codegen-check TOPIC=<topic>`.

   Report **each** unresolved reference and each staleness warning that `make check` prints. A
   session does not close silently over a broken reference that it can see. Fix a real finding at
   its source before you propose the commit. If it is a false positive, correct the checker.
   Never leave it unmentioned.

4. **History, then state.** Append the full record of this session to the end of
   `docs/status_history.md`: what you did, the evidence and the commits. *Then* update
   `docs/STATUS.md`. It holds the current state only, it loads in every session, and it has a
   budget that `make check-docs` checks. If it warns, move detail to the history. Do not
   compress the wording.

   - Update the current phase and give one concrete immediate next task.
   - Move an item between *Derived*, *Validated* and *Open* **only with the evidence** (script
     path, command and result). Nothing is "validated" without a re-runnable check.
   - **If an interruption or a usage limit stopped the session**, state explicitly what the
     session completed and what it started and left incomplete. Then the next session does not
     resume from a false picture.
   - Update the last validation: date, command, outcome and commit.

5. **Reproduction and extension.** Update `docs/reproduction_and_extension.md` for anything that
   the session reproduced, established, attempted, found discrepant, or found not to work. Update
   **both** tables and the new-work deliverables. The PI reads this file. If a session advanced
   the extension and updated only the reproduction table, the session recorded itself wrongly.
   Record a negative extension result. Do not drop it.

6. **Decisions and prompts.** Append each PI decision to `docs/decision_log.md` in the `D-NNN`
   form. Fill in the `## Outcome` section of the prompt record of this session in
   `docs/prompts/`. If something went wrong in the session, add an entry to
   `docs/failure_modes/project.md`.

6a. **Write `handoff.md`.** Overwrite it. Do not append. Write what the records cannot hold. Write
   what was in progress. Write what you believe and have not established. Write what cost time
   in this session. Write the one next action. **`docs/handoff_guide.md` explains how to write one, with a good and
   a bad example and a checklist.** Read it if you have not written a handoff before. The usual
   failure is a cheerful paragraph that claims results. That is worse than an empty file.

7. **Checklist.** Tick the completed boxes in `docs/implementation_checklist.md`, only with
   evidence.

8. **Propose a commit message.** Use a conventional, scoped message. List the checks that you ran
   and their results. **Do not commit or push** unless the PI says so.

9. **Report**, in fewer than 20 lines: the changed files, the checks that you ran with their
   results, the orphaned artefacts that you found with their dispositions, the open issues, and
   the next task.
