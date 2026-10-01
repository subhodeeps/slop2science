# Failure modes

This file lists the things that went wrong in an AI-assisted project that reproduced a paper. For
each failure, it states what the failure cost and which mechanism in this repository exists
because of it.

Read this file before an audit, before you write a report, and whenever a session is under time
pressure. The entries are not hypothetical. Each entry happened. Most of them happened to people
who knew better in the abstract.

**Part 0 is about the model.** It describes three ways in which an LLM fails. No project
discipline prevents them, because they are properties of the tool. **Part 1 comes from earlier
work.** It comes from the project that this template came from. It is general to the work. It
is not specific to that paper. **Part 2 is yours.** At each `/session-close` where something
went wrong, add an entry with the same three fields. **Part 3 describes failures that nobody has
seen yet.**

---

## Part 0 — how the model fails

These three failures come from *How to Train Your Slop Cannon*
([Open-Science-Ledger](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)).
The guide names them. It is worth reading in full. They are the reason why several rules in this
repository look paranoid. Each rule is a countermeasure to one of them.

### 0a. Context rot

**What it is.** The context window fills, and attention starts to produce spurious correlations.
The quality of the output drops. There is no sharp threshold. The guide gives this calibration:
*"quality starts to sag beyond roughly 30% context usage."*

**What it looks like.** An answer that was sharp early in a session becomes vague or slightly
wrong late in the session. The model remembers a file that it read an hour ago incorrectly. The
model quietly violates a convention that the session established at the start.

**Countermeasures here.** The filesystem is the memory. The conversation is not. `docs/STATUS.md`
and `docs/conventions.md` are small and reload in every session. Detail lives in skills and
`reference/` files that load only when needed. The context budget of the files that load in
every session is a hard error (`make check-docs`). In practice: **run `/checkpoint` early and
often. Prefer a fresh session to a long session.** A `PreCompact` hook writes a snapshot. It
tells the session to record anything that only the session holds, because compaction keeps the
thread and loses the detail.

### 0b. Hyperfixation

**What it is.** The model locks onto a subgoal. It produces work that is more and more
unreliable to "achieve" that subgoal before the context ends. The guide gives this exact example:
*"an agent that cannot make a test suite pass will sometimes delete the failing tests, hard-code
the expected output, or simply declare success."*

**What it looks like.** A tolerance that someone widened without an explanation. A check that
someone rewrote until it passes. An assertion that matches the expectation and not the
computation. "Done" with no output quoted.

**Countermeasures here.** A whole family of prohibitions exists for this failure. They look
different when you know its name:

- Never skip, disable or quarantine a test.
- Never widen a tolerance without a recorded reason.
- Never adjust a check to make it pass.
- Print before you assert.
- If a check fails, stop and report. Do not iterate until it is green.

Decomposition also helps. Use one stage for each script. Make it small enough that a failure is
local. Then the failure is not something to escape.

### 0c. Sycophancy

**What it is.** Post-training on human preference means that the model does not only state
falsehoods fluently. *"It preferentially asserts the falsehoods you would quite like to be
true."*

**What it looks like, and why it is the dangerous failure here.** The method of this project is
"the PI decides, Claude implements". Therefore the project is *structurally* exposed to this
failure. Suppose that you say "I think Eq. (12) of the source is missing a factor of 2". A
sycophantic model finds the missing factor. The result is a discrepancy record built on nothing.
It can spread into a decision, a convention and a paper.

**Countermeasures here.** The five-item form separates three things: *what the source states*,
*what its equations imply* and *what an independent derivation gives*. A suspicion then cannot
become a finding. The project also adopts the rule of the guide: **be sceptical of the
enthusiasm of the model for your idea. When you want a real assessment, ask a clean session that
does not know your position.** Do not tell the verifier what you expect it to find. The
`verification` agent exists partly for this reason. Therefore its brief must carry the artifact.
It must not carry your hypothesis about the artifact.

---

## Part 1 — inherited

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

---

## Part 2 — the own failures of this project

At `/session-close`, add an entry whenever something went wrong. State **what happened**, **what
it cost** and **what changed as a result**. If nothing changed, the entry is still worth having.
"We decided to accept this risk" is a finding.

(none yet)

---

## Part 3 — anticipated, not yet observed

Part 3 is separate from Part 1 on purpose. **These failures did not happen here.** The structure
of this project guards against them. The project records them so that the reason for a rule
survives when the rule looks like bureaucracy. If one of them happens, move it to Part 2 with
what it cost.

### A. A language chosen for convenience, then two records for one fact

Three tools of equal standing make it easy to derive something in one tool. During a debugging
session, someone derives it again in another tool. Someone commits both. Nothing states which
one is authoritative. **The checks of neither tool can detect this.** Each one passes.

Guard: the PI decides which language implements which work, per topic or by the default profile (CLAUDE.md
§1, §5). Then nobody picks a language for convenience. The ownership and interoperation
registries in `docs/toolchain.md` cite a decision in each row. `make check-docs` fails when a
topic has stage scripts and no registry row. A second implementation is a labelled `CROSS-CHECK`.
It is never a second record.

### B. The project that quietly becomes a reproduction project

Reproduction has clear targets, visible progress and an obvious stopping condition. Extension has
none of these. The easy path is to keep reproducing, to report that as progress, and never to
start the new work. The new work is the part that the project is for (CLAUDE.md §2).

Guard: `docs/STATUS.md` and `docs/reproduction_and_extension.md` have separate sections of equal
weight. The source audit must list what the source *does not* do, and not only what it does. The
checklist has an extension phase. The instructions of `status-reporter` say that progress of the
reproduction never stands in for progress of the project.

### C. An extension that someone validates against the source

The source does not contain the results of the extension. Therefore it cannot validate them.
"This agrees with the paper" is a reassuring sentence, and someone writes it anyway. It is
usually about a limiting case that does agree. It reads as if someone checked the whole
extension.

Guard: `Kind:` and `Judged against:` where the project uses a result. Each record requires the
field `judged_against`. `docs/validation_protocol.md` §8 states what an extension can rest on
when no independent benchmark exists.

### C2. A transcript that travels with a shared repository

A session transcript is nearly verbatim. It holds half-formed reasoning, dead ends, and whatever
someone said about a result before anyone was sure of it. People share a repository: with a
collaborator, a supervisor, a journal, and eventually with everyone. **Sharing permissions
inherit downward. You cannot subtract them from a subfolder.** A leading dot does not help.
`.claude/` is hidden in a file browser and it is an ordinary visible folder in a web interface.

Guard: `capture_session.py` writes to `$RESEARCH_RECORDS_DIR` (default
`~/.claude-research-records`), **never inside the repository.** The hook self-tests assert that
nothing leaked in. The design depends on the property *never shared*. It does not depend on the
property *not in the repo*. `handoff.md` is the artifact that other people read, and the project
commits it.

Credit: [benning-lab/agentic-starter](https://github.com/benning-lab/agentic-starter) gave this
argument and the mechanism. This template first committed its prompt logs into the tree. That
was wrong, for the same reason.

### D. A default that someone supplied silently for a decision that belonged to the PI

An assistant that receives a request to proceed will proceed. The missing convention, the unstated
scope boundary and the unassigned language each have an answer that looks obvious. To supply it is
faster than to ask. The cost is not the wrong answer. The cost is that nobody knows that anyone
made a choice.

Guard: the instruction to **stop and ask** and not to supply a default (CLAUDE.md §1). `OPEN` is
a first-class status in `docs/conventions.md`. `/init-paper` records unanswered questions as open
and does not fill them. The field `Options:` of the decision log is impossible to fill honestly
for a decision that nobody made. No hook can enforce this guard. This is why the first section of
the charter states it, and not the last section.

### E. A catalogue entry that someone takes on trust

A reference manager holds the metadata of someone for years. Most of it is correct. Some of it is
wrong. An entry can have the right title and the wrong DOI. It can have a PDF that is a different
version or a different paper. It can have a saved web page in place of the article. After an
import, each of these looks authoritative. The entry sits in `refs.bib` with a clean key. Nothing
marks it as less checked than an entry that someone verified by hand.

Guard: `scripts/library.py import` writes each entry with `verified: false`, in the registry, and
as an UNVERIFIED comment in `refs.bib`. `make check-docs` counts the entries that are still
unverified. The importer never guesses an identifier or a `primaryClass` that the catalogue did
not give. It refuses a saved web page and a file that the catalogue calls a PDF and that is not a
PDF. To verify an entry, someone reads the first page of the copied document. This is the work
of a person or of an agent. A script does not do it
(`.claude/skills/literature-audit/reference/local_libraries.md`).
