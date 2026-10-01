# reports — generated write-ups

`<topic>_report.md` is the source. A tool generates the PDF, and Git ignores it.

    make report TOPIC=<topic>        renders <topic>_report.md -> .pdf

**Never fix a report by editing its PDF or its intermediate LaTeX.** Fix the Markdown and render
it again.

## What a report is

A report is a paper that a researcher in the field can read from start to end. The reader can
use it to **follow, redo and reproduce** the calculation. It supplies the algebra that the
source omits. It is not a repository report, an activity log or a provenance ledger.

Put provenance in a verification appendix. For each equation that the report presents as a
result, give the script, the check label and the result. For each number, give a record. Do not
put provenance after every equation. That makes a document that nobody can read. This happened.
The project rejected the report and rewrote it from the start (`docs/failure_modes.md` entry 8).

One author writes the report, in order, in chunks (`.claude/skills/report-writing/SKILL.md`).
Ten parallel writers finish faster. They also produce ten voices, and one person must rewrite
them.
