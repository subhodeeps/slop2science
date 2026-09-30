# code/_drop — the PI's code drop folder

Put a script here and the next session will notice it: the session-start hook reports a
non-empty drop folder.

Intake, before the file is read closely
(`.claude/skills/external-code/reference/pi_code_intake.md`): where it came from, what it is
believed to do and whether that was ever checked, what it is for here, and whether it is
believed correct — including "unknown", which is a valid and important answer.

Then: record licence and author, move it to `code/reference/`, `code/pi/` or `code/unused/`
with a README entry, and leave this folder empty.

Gitignored except this README. **Never run a dropped script before reading it**, and never let
one write into `src/`, `symbolic/generated/`, `validation/**/records/` or `papers/`.
