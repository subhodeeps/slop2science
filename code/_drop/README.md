# code/_drop — the code drop folder of the PI

Put a script here. The next session finds it, because the session-start hook reports a drop
folder that is not empty.

Do the intake before you read the file closely
(`.claude/skills/external-code/reference/pi_code_intake.md`). Ask these questions:

- Where did the file come from?
- What does it do, according to the PI? Did anyone ever check this?
- What is it for in this project?
- Does the PI believe that it is correct? "Unknown" is a valid and important answer.

Then do these steps:

1. Record the licence and the author.
2. Move the file to `code/reference/`, `code/pi/` or `code/unused/`, with an entry in the README.
3. Leave this folder empty.

Git ignores this folder, except this README. **Never run a dropped script before you read it.**
Never let a dropped script write into `src/`, `symbolic/generated/`,
`validation/**/records/` or `papers/`.
