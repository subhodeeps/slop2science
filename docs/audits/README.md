# docs/audits — audit reports

The `verification` agent writes each audit report here. It cannot edit any other project file,
so this folder is the one place where it records its findings.

- Name each report `<YYYYMMDD>_<topic>.md`. The agent creates a new file and never overwrites one.
  A hook blocks the agent from editing or replacing a report. Another hook blocks a `Write` over an
  existing report for every agent.
- Use the layout in `.claude/skills/verification/reference/audit_report_template.md`.
- The agent also returns the same report to the session that dispatched it. The session cites the
  path in the prompt record and in `docs/STATUS.md`.
- Never delete a report. If a finding changes, add a new report, or use `Edit` to append a
  correction that names the finding.
