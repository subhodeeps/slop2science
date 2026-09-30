# reports — generated write-ups

`<topic>_report.md` is the source; the PDF is generated and gitignored.

    make report TOPIC=<topic>        renders <topic>_report.md -> .pdf

**Never fix a report by editing its PDF or its intermediate LaTeX.** Fix the Markdown and
re-render.

## What a report is

A paper a researcher in the field can read start to finish and use to **follow, redo and
reproduce** the calculation. It supplies the algebra the source omits. It is not a repository
report, an activity log, or a provenance ledger.

Provenance belongs in a verification appendix: script, check label and result for every
equation presented as a result, and a record for every number. Putting it after every equation
instead produces a document nobody can read — that happened, and the report was rejected and
rewritten from scratch (`docs/failure_modes.md` entry 8).

Written by one author, in order, in chunks (`.claude/skills/report-writing/SKILL.md`). Ten
parallel writers finish faster and produce ten voices that then have to be rewritten by one
person anyway.
