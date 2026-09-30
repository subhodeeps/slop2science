# Failure modes

Things that actually went wrong in an AI-assisted paper-reproduction project, what each one
cost, and which mechanism in this repository exists because of it.

Read this before an audit, before writing a report, and whenever a session is under time
pressure. It is not a list of hypotheticals: every entry below happened, most of them to
people who knew better in the abstract.

**Part 1 is inherited** — from the project this template was extracted from. Keep it: these
are general to the work, not to that paper. **Part 2 is yours** — add to it at every
`/session-close` where something went wrong, with the same three fields.

---

## Part 1 — inherited

### 1. A claim asserted before it was checked

A derivation script asserted an expected invariant and passed. The printed value, read by
hand afterwards, said the opposite: the assertion had been written to match the expectation,
and the check had never compared it to anything.

**Cost**: caught, but only by someone re-reading raw output that had already "passed".
**Mechanism**: *print before assert* — every non-trivial step prints its value and then checks
it (`.claude/rules/derivation.md`). Ordering matters; the discipline is worthless in reverse.

### 2. The same equation misread from a PDF, three times

The three most consequential documentation errors in that project — a dropped term in an
asymptotic expression, a misattributed sign convention, and a mislabelled benchmark column —
all traced to reading a PDF's extracted text layer for a nested expression or a table,
instead of the rendered page.

**Cost**: one error survived three sessions and a write-up; a convention was recorded
backwards; a benchmark was labelled with the wrong method.
**Mechanism**: read equations, tables and numbers **as a rendered page image**
(`.claude/skills/literature-audit/SKILL.md`), and require a second independent source before
one paper's stated equation changes a project convention.

### 3. Audits spawning audits

One discrepancy with the source was independently re-derived four times before being
considered closed. The first two were justified — it contradicted a published paper. The
third and fourth were ritual.

**Cost**: several sessions spent re-confirming something three independent routes already
agreed on.
**Mechanism**: a stopping rule. Once an independent re-derivation confirms a result by a
genuinely different route — not the same script rerun, not the same route retyped — and either
the literature agrees or there is a stated reason it cannot be consulted: **stop**.

### 4. Convergence that proved nothing

A recurrence with a deliberately flipped sign converged cleanly and gave confidently wrong
answers, missing the benchmark by an amount no convergence diagnostic could see.

**Cost**: nothing, because it was tested deliberately — but it established that convergence
alone cannot detect a wrong formulation, which had been assumed until then.
**Mechanism**: an independent-method benchmark or an exact known answer is the only check on
*which problem* was solved. Residuals, resolution refinement and precision refinement all
test how well the problem was solved (`.claude/skills/solver-workflow/SKILL.md`).

### 5. An orphaned script nobody could account for

A subagent, dispatched under one scope, kept working after a later prompt had narrowed that
scope, then hit a rate limit mid-task. It left behind a script in a validation directory that
had never been requested, never been run, and was not a validation. Nothing recorded where it
came from.

**Cost**: weeks of a file sitting in a results directory looking authoritative.
**Mechanism**: **scope shrinks under interruption, never expands** (CLAUDE.md §8a); and the
session-close orphaned-artefact check, which accounts for every changed and untracked file by
name and disposition. The second is the real backstop, because the first depends on the rule
being followed under exactly the pressure that makes rules get skipped.

### 6. A long write stalling silently

A subagent tried to write a whole report in one call, hit the output-token limit, and produced
nothing for several minutes while appearing to work.

**Cost**: a restart that discarded real work, on a second occasion when the agent was in fact
still running.
**Mechanism**: write in chunks of roughly 250 lines per call. Before declaring an agent stuck,
check whether the target file's line count and the transcript are still growing.

### 7. Ten parallel authors, one document

A report was split across ten parallel writer subagents. It finished fast, used about 1.5M
subagent tokens in 17 minutes, and produced ten voices, drifting notation and the same framing
repeated four times.

**Cost**: the whole document had to be rewritten by one author.
**Mechanism**: split *reading* and *checking*; never split a narrative a reader must follow in
order. Fan-out is also where cost spikes, not where hard problems are
(`.claude/models.md`).

### 8. A brief followed faithfully, producing the wrong thing

A report brief demanded a provenance tag on every result and a classification line on every
section. The writer complied exactly. The result was a ledger nobody could read, and it was
rejected outright.

**Cost**: an entire report, rewritten from scratch.
**Mechanism**: a brief **starts** with who the reader is and what they must be able to do.
Mechanical requirements go where they serve that reader — an appendix — not everywhere
(`.claude/skills/report-writing/SKILL.md`).

### 9. A working note outranking the settled record

A report writer copied a claim from an exploratory note. The settled decision log and the
numerics both contradicted it. It shipped.

**Cost**: a wrong statement in a delivered document, found later.
**Mechanism**: an explicit precedence order — the decision log and the audit's discrepancy
rows outrank the per-leg notes they were synthesized from — and, where they disagree, **record
the inconsistency** rather than quietly picking one.

### 10. The status file drifting

`STATUS.md` still described a file as uncommitted after it had been committed, and had grown
to 504 lines of accumulated history, all of it loading into every session.

**Cost**: context spent every session on history, and a next-session picture that was wrong
in a way nobody checked because it was the authoritative file.
**Mechanism**: STATUS holds **current state only**, under ~100 lines; history goes to
`status_history.md`, which is not auto-loaded. When a session changes a fact STATUS states, it
updates that line.

### 11. Documentation restating documentation

The same facts were stated in a README, a guide, a structure document, a start-here file and
several directory READMEs. They drifted apart. A 379-line staleness checker was then written
to police drift that restatement had created.

**Cost**: a maintenance burden that existed only because of duplication, plus one document
that had to be marked "superseded" in place.
**Mechanism**: **one owner per fact**; every other mention is a link. The checker survives in
this template (`scripts/check_docs.py`) because it also catches renames — but it is a net, not
a substitute for not duplicating.

### 12. Machine captures buried the real prompts

A prompt-capture hook wrote every long prompt to one directory. Harness traffic — subagent
hand-backs, task notifications, stop-hook feedback — arrived through the same hook: at least
54 of 110 captured "prompts" were not prompts, sitting beside the curated records.

**Cost**: the prompt record became unusable for its purpose, and a README had to explain how
to tell the two apart.
**Mechanism**: machine captures go to `docs/prompts/auto/` and the raw per-session log; curated
records live in `docs/prompts/` and are written by hand. Separate directories, so no filtering
rule has to be trusted.

---

## Part 2 — this project's own

Add an entry at `/session-close` whenever something went wrong: **what happened**, **what it
cost**, **what changed as a result**. If nothing changed, the entry is still worth having —
"we decided to accept this risk" is a finding.

(none yet)
