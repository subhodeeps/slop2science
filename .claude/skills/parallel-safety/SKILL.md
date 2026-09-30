---
name: parallel-safety
description: How to run more than one agent at once without corrupting the record - what parallelises safely, what must not, and the partition rules. Use before dispatching concurrent subagents.
when_to_use: 'Trigger phrases: in parallel; at the same time; several agents; fan out; concurrently; split this across; multiple subagents; speed this up with more agents'
---

# Parallel agents — what is safe, and what is not

The project's rule is not "never parallelise". It is that **parallelism is safe for
independent reading and checking, and unsafe for anything that produces one coherent
artifact.** This skill is the constructive half of `docs/failure_modes.md` entry 7.

## Safe to run concurrently

- **Reading and locating** — several `explore` agents over different directories.
- **Independent checks of the same object** — two `verification` agents auditing the same
  derivation by *different routes*, reporting separately. Their disagreement is the signal;
  that only works if neither saw the other's work.
- **Independent topics** — a derivation in topic A and a solver in topic B, provided they
  share no file and no generated code.
- **Literature lookups for different sources.**

## Never run concurrently

- **One narrative.** A report, a write-up, a document a reader follows in order. Ten parallel
  writers finished fast, used about 1.5M subagent tokens in 17 minutes, and produced ten
  voices with drifting notation that had to be rewritten by one author anyway.
- **One file.** Two agents editing the same file is a lost edit, not a merge.
- **Stage scripts in the same topic.** Stage N+1 consumes stage N's output; running them
  together means one reads a half-written file.
- **Anything writing `symbolic/generated/`.** The codegen diff gate compares against git; two
  concurrent exports make its result meaningless.
- **Anything touching git.** Subagents are blocked from it by a hook
  (`.claude/hooks/subagent_git_guard.py`) precisely because a concurrent agent cannot see
  what else is staged.

## If you do parallelise

1. **Partition by writer.** Every file has exactly one agent that may write it, named before
   dispatch. Not "roughly separate areas" — an explicit list.
2. **State the partition in each brief**, including what the agent must *not* touch. An agent
   with a fresh context cannot infer the boundary.
3. **Cap concurrency at three.** Beyond that, the cost of reconciling exceeds the time saved,
   and `/usage` spikes are fan-out, not hard problems (`.claude/models.md`).
4. **Serialise anything licence-limited.** `scripts/run` already takes a lock, because CAS
   licences cap concurrent kernels and parallel agents would otherwise fail with licence
   errors. Do not work around it.
5. **Reconcile in one pass, by one author**, before anything is committed. Parallel work
   produces material; a single pass turns it into the record.
6. **One commit, after reconciliation.** Never a commit per agent.
7. **Commit before dispatching.** A clean tree before an agent runs makes any mistake a
   one-command undo, and the diff afterwards is a complete, compact record of what the agent
   actually did — which is usually easier to review than its transcript. `/checkpoint` exists
   for this.
8. **Separate worktrees when two agents must touch the same tree.** `git worktree` gives each
   one its own checkout of its own branch, so a concurrent write cannot collide; land the
   branches in sequence, reconciled by one author. Subagents cannot create worktrees
   themselves (the git guard blocks it) — the main session sets them up.

## The honest test

Before dispatching, ask: *if these two agents disagree, is that a finding or a mess?*

A finding — two independent audits, two derivations by different routes — parallelise. A mess
— two halves of one document, two edits to one file — do not.
