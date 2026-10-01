# Inherited failure modes

These twelve failures happened in the project that this template came from. They are general to
the work. They are not specific to that paper. Each entry states what happened, what it cost and
which mechanism exists because of it. `docs/failure_modes.md` is the index of all failure modes.

### 1. A claim that someone asserted before checking it

A derivation script asserted an expected invariant, and the assertion passed. Later, someone read
the printed value by hand. The value said the opposite. The author had written the assertion to
match the expectation. The check never compared it to anything.

**Cost**: someone caught it, but only by a re-read of raw output that had already "passed".
**Mechanism**: *print before assert*. Each non-trivial step prints its value and then checks it
(`.claude/rules/derivation.md`). The order matters. The discipline is worthless in the reverse
order.

### 2. The same equation misread from a PDF, three times

Three documentation errors had the most consequence in that project. They were a dropped term in
an asymptotic expression, a sign convention with the wrong attribution, and a benchmark column
with the wrong label. All three came from the extracted text layer of a PDF, for a nested
expression or a table. The rendered page would have avoided them.

**Cost**: one error survived three sessions and a write-up. Someone recorded a convention
backwards. Someone labelled a benchmark with the wrong method.
**Mechanism**: read equations from the **`.tex` source** where one exists. Where none exists,
read them from the **rendered page image**. Never read them from the text layer
(`.claude/skills/literature-audit/reference/corpus.md`). Require a second independent source
before the stated equation of one paper changes a convention of the project.

### 3. Audits that start audits

One discrepancy with the source was re-derived independently four times before the project
considered it closed. The first two derivations had a reason, because the discrepancy contradicted a
published paper. The third and the fourth were ritual.

**Cost**: several sessions went to the confirmation of something that three independent routes
already agreed on.
**Mechanism**: a stopping rule. An independent derivation confirms a result by a different route.
The same script run again does not count. The same route typed again does not count. Also, the
literature agrees, or there is a stated reason why nobody can consult it. Then **stop**.

### 4. Convergence that proved nothing

A recurrence with a deliberately flipped sign converged cleanly. It gave answers that were
confidently wrong. It missed the benchmark by an amount that no convergence diagnostic showed.

**Cost**: nothing, because the test was deliberate. It did establish that convergence alone
cannot detect a wrong formulation. People had assumed the opposite until then.
**Mechanism**: only an independent-method benchmark or an exact known answer checks *which
problem* the work solved. Residuals, resolution refinement and precision refinement all test how
well the work solved the problem (`.claude/skills/solver-workflow/SKILL.md`).

### 5. An orphaned script that nobody could account for

A subagent had one scope. A later prompt narrowed that scope. The subagent kept working, and then
hit a rate limit in the middle of a task. It left a script in a validation directory. Nobody had
requested the script. Nobody had run it. It was not a validation. Nothing recorded where it came
from.

**Cost**: a file stayed for weeks in a results directory and looked authoritative.
**Mechanism**: **scope gets smaller under interruption. It never gets larger** (CLAUDE.md §8a).
The second mechanism is the orphaned-artefact check of the session close. It accounts for each
changed and untracked file by name and disposition. The second mechanism is the real backstop.
The first mechanism depends on people who follow the rule under the same pressure that makes
people skip rules.

### 6. A long write that stalled silently

A subagent tried to write a whole report in one call. It hit the output-token limit. It produced
nothing for several minutes while it appeared to work.

**Cost**: a restart that discarded real work. On a second occasion, the agent was still running.
**Mechanism**: write in chunks of about 250 lines for each call. Before you declare that an agent
is stuck, check if the line count of the target file and the transcript still grow.

### 7. Ten parallel authors, one document

The project split a report across ten parallel writer subagents. The report finished fast. It
used about 1.5M subagent tokens in 17 minutes. It had ten voices, drifting notation and the same
framing repeated four times.

**Cost**: one author had to rewrite the whole document.
**Mechanism**: split the *reading* and the *checking*. Never split a narrative that a reader must
follow in order. Fan-out is also where cost spikes. It is not where the hard problems are
(`.claude/models.md`).

### 8. A brief that an agent followed faithfully and that produced the wrong thing

A report brief required a provenance tag on each result and a classification line on each
section. The writer complied exactly. The result was a ledger that nobody can read. The project
rejected it completely.

**Cost**: a whole report, rewritten from the start.
**Mechanism**: a brief **starts** with the reader and with what the reader must be able to do.
Mechanical requirements go where they serve that reader: in an appendix. They do not go
everywhere (`.claude/skills/report-writing/SKILL.md`).

### 9. A working note that outranked the settled record

A report writer copied a claim from an exploratory note. The settled decision log and the
numerics both contradicted the claim. The claim shipped.

**Cost**: a wrong statement in a delivered document, which someone found later.
**Mechanism**: an explicit order of precedence. The decision log and the discrepancy rows of the
audit outrank the per-leg notes that they came from. If they disagree, **record the
inconsistency**. Do not pick one quietly.

### 10. The status file that drifted

`STATUS.md` still described a file as uncommitted after someone committed it. It had grown to
504 lines of accumulated history. All of it loaded into every session.

**Cost**: every session spent context on history. The picture for the next session was wrong,
and nobody checked it, because the file was the authoritative file.
**Mechanism**: STATUS holds the **current state only**, in about 100 lines or fewer. The history
goes to `status_history.md`, which does not load automatically. If a session changes a fact that
STATUS states, the session updates that line.

### 11. Documentation that restated documentation

The same facts were in a README, a guide, a structure document, a start-here file and several
READMEs of directories. They drifted apart. Then someone wrote a staleness checker of 379 lines.
It policed the drift that the restatements created.

**Cost**: a burden of maintenance that existed only because of duplication. One document also
needed the mark "superseded" in place.
**Mechanism**: **one owner for each fact.** Every other mention is a link. The checker survives
in this template (`scripts/check_docs.py`), because it also catches renames. It is a net. It does
not replace the discipline of no duplication.

### 12. Machine captures buried the real prompts

A prompt-capture hook wrote each long prompt to one directory. Harness traffic arrived through
the same hook: hand-backs of subagents, task notifications and feedback of stop hooks. At least
54 of 110 captured "prompts" were not prompts. They sat next to the curated records.

**Cost**: the prompt record became unusable for its purpose. A README had to explain how to tell
the two apart.
**Mechanism**: machine captures go to `docs/prompts/auto/` and to the raw log of each session.
Curated records are in `docs/prompts/`, and a person writes them by hand. The directories are
separate. Then no filtering rule needs trust.
