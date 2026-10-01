# Failure modes of the model

These three failures are properties of the tool. No project discipline prevents them. They come
from *How to Train Your Slop Cannon*
([Open-Science-Ledger](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)).
The guide names them. It is worth reading in full. They are the reason why several rules in this
repository look paranoid. Each rule is a countermeasure to one of them. `docs/failure_modes.md`
is the index of all failure modes.

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
