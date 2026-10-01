# Failure modes

Things that actually went wrong in an AI-assisted paper-reproduction project, what each one
cost, and which mechanism in this repository exists because of it.

Read this before an audit, before writing a report, and whenever a session is under time
pressure. It is not a list of hypotheticals: every entry below happened, most of them to
people who knew better in the abstract.

**Part 0 is about the model**, not the process: three ways an LLM fails that no amount of
project discipline prevents, because they are properties of the tool. **Part 1 is inherited**
from the project this template was extracted from — general to the work, not to that paper.
**Part 2 is yours**: add to it at every `/session-close` where something went wrong, with the
same three fields. **Part 3** is anticipated and not yet observed.

---

## Part 0 — how the model fails

From *How to Train Your Slop Cannon*
([Open-Science-Ledger](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)),
which names these three and is worth reading in full. They are the reason several rules in
this repository look paranoid: each one is a countermeasure to one of them.

### 0a. Context rot

**What it is.** As the context window fills, attention starts producing spurious
correlations and output quality sags. There is no sharp threshold — the guide's calibration
is that *"quality starts to sag beyond roughly 30% context usage."*

**What it looks like.** Answers that were sharp early in a session become vague or subtly
wrong late in it. A file read an hour ago gets mis-remembered. A convention established at
the start gets quietly violated.

**Countermeasures here.** The filesystem is the memory, not the conversation: `docs/STATUS.md`
and `docs/conventions.md` are small and reloaded every session; detail lives in skills and
`reference/` files loaded only when needed; the context budget on the every-session files is
a hard error (`make check-docs`). Practically: **`/checkpoint` early and often, and prefer a
fresh session over a long one.** A `PreCompact` hook writes a snapshot and tells the session
to record anything held only in its head, because compaction keeps the thread and loses the
detail.

### 0b. Hyperfixation

**What it is.** The model locks onto a subgoal and produces increasingly unreliable work to
"achieve" it before the context runs out. The guide's example is exact: *"an agent that
cannot make a test suite pass will sometimes delete the failing tests, hard-code the expected
output, or simply declare success."*

**What it looks like.** A tolerance widened without explanation. A check rewritten until it
passes. An assertion that matches the expectation rather than the computation. "Done" with no
output quoted.

**Countermeasures here.** This is what a whole family of prohibitions is actually for, and
they read very differently once it has a name: never skip, disable or quarantine a test;
never widen a tolerance without recording why; never adjust a check to pass; print before
asserting; a failing check means stop and report, not iterate until green. Plus decomposition
— one stage per script, small enough that a failure is localized rather than something to be
escaped.

### 0c. Sycophancy

**What it is.** Post-training on human preference means the model does not merely assert
falsehoods fluently — *"it preferentially asserts the falsehoods you would quite like to be
true."*

**What it looks like, and why it is the dangerous one here.** A project whose whole method is
"the PI decides, Claude implements" is *structurally* exposed to this. Say "I think the
source's Eq. (12) is missing a factor of 2" and a sycophantic model will find the missing
factor. That is a discrepancy record built on nothing, and it can propagate into a decision,
a convention and a paper.

**Countermeasures here.** The five-point form separates *what the source states* from *what
its equations imply* from *what an independent derivation gives* — precisely so that a
suspicion cannot be laundered into a finding. Beyond that, the guide's own rule, adopted:
**treat the model's enthusiasm for your idea with scepticism, and when you want a genuine
assessment, ask a clean session that does not know your position.** Do not tell the verifier
what you expect it to find. The `verification` agent exists partly for this, which is why its
brief should carry the artifact and not your hypothesis about it.

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

---

## Part 3 — anticipated, not yet observed

Distinguished from Part 1 on purpose: **these have not happened here.** They are the failure
modes this project's structure is shaped against, written down so that the reason for a rule
survives even when the rule looks like bureaucracy. If one of them does happen, move it to
Part 2 with what it actually cost.

### A. A language chosen by convenience, then two records for one fact

Three co-equal tools make it easy to derive something in one, re-derive it in another during a
debugging session, commit both, and have nothing say which is authoritative. **Neither tool's
own checks can detect this** — each passes.

Guarded by: the PI decides what is implemented where (CLAUDE.md §1, §5); the ownership and
interoperation registries in `docs/toolchain.md`, each row citing its decision;
`make check-docs` failing when a topic has stage scripts and no registry row; and the rule
that a second implementation is a labelled `CROSS-CHECK`, never a co-record.

### B. The project quietly becoming a reproduction project

Reproduction has clear targets, visible progress and an obvious stopping condition. Extension
has none of those. The path of least resistance is to keep reproducing, report that as
progress, and never start the new work — which is the half the project is actually for
(CLAUDE.md §2).

Guarded by: separate, equally weighted sections in `docs/STATUS.md` and
`docs/reproduction_and_extension.md`; the source audit being required to list what the source
*does not* do, not only what it does; an extension phase in the checklist; and
`status-reporter` being told never to let reproduction progress stand in for the project's.

### C. An extension validated against the source

The source does not contain the extension's results, so it cannot validate them — but "this
agrees with the paper" is such a reassuring sentence that it gets written anyway, usually
about a limiting case that genuinely does agree, in a way that reads as though the whole
extension were checked.

Guarded by: `Kind:` / `Judged against:` at the point of use; the `judged_against` field being
required in every record; and `docs/validation_protocol.md` §8 stating what an extension may
rest on when no independent benchmark exists.

### C2. A transcript travelling with a shared repository

A session transcript is near-verbatim: it holds half-formed reasoning, dead ends, and whatever
was said about a result before anyone was sure of it. A repository gets shared — with a
collaborator, a supervisor, a journal, eventually the world — and **sharing permissions
inherit downward and cannot be subtracted from a subfolder.** A leading dot does not help:
`.claude/` is hidden in a file browser and an ordinary visible folder in a web UI.

Guarded by: `capture_session.py` writing to `$RESEARCH_RECORDS_DIR` (default
`~/.claude-research-records`), **never inside the repository**, with the hook self-tests
asserting that nothing leaked in. The property relied on is *never shared*, not *not in the
repo*. `handoff.md` is the artifact meant to be read by other people, and it is committed.

Credit: this argument, and the mechanism, are from
[benning-lab/agentic-starter](https://github.com/benning-lab/agentic-starter). This template
originally committed its prompt logs into the tree, which was wrong for the same reason.

### D. A default silently supplied for a decision that was the PI's

An assistant asked to proceed will proceed. The missing convention, the unstated scope
boundary, the unassigned language: each has an obvious-looking answer, and supplying it is
faster than asking. The cost is not the wrong answer — it is that nobody knows a choice was
made.

Guarded by: the instruction to **stop and ask** rather than default (CLAUDE.md §1); `OPEN` as
a first-class status in `docs/conventions.md`; `/init-paper` recording unanswered questions as
open rather than filling them; and the decision log's `Options:` field, which is impossible to
fill honestly for a decision nobody made. No hook can enforce this one, which is why it is
written in the charter's first section rather than its last.

### E. A catalogue entry taken on trust

A reference manager is somebody's years of accumulated, mostly correct, occasionally wrong
metadata. An entry can carry the right title and the wrong DOI, a PDF that is a different
version or a different paper, or a saved web page standing in for the article. Importing it
makes every one of those look authoritative: it now sits in `refs.bib` with a clean key, and
nothing marks it as less checked than an entry someone verified by hand.

Guarded by: `scripts/library.py import` writes every entry `verified: false`, in the registry
and as an UNVERIFIED comment in `refs.bib`; `make check-docs` counts the ones still unverified;
it never guesses an identifier or a `primaryClass` the catalogue did not give; it refuses a
saved web page and a file catalogued as a PDF that is not one; and verifying means reading
the copied document's own first page, which is a person's or an agent's job and not a script's
(`.claude/skills/literature-audit/reference/local_libraries.md`).
