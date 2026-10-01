---
name: parallel-safety
description: How to run more than one agent at the same time without damage to the record. It states what is safe to parallelise, what is not, and the partition rules. Use it before you dispatch concurrent subagents.
when_to_use: 'Trigger phrases: in parallel, at the same time, several agents, fan out, concurrently, split this across, multiple subagents, speed this up with more agents'
---

# Parallel agents — what is safe, and what is not

The rule of the project is not "never parallelise". The rule is this: **parallelism is safe for
independent reading and checking. It is unsafe for anything that produces one coherent
artifact.** This skill is the constructive half of `docs/failure_modes.md` entry 7.

## Safe to run concurrently

- **Reading and locating.** Use several `explore` agents over different directories.
- **Independent checks of the same object.** Use two `verification` agents. They audit the same
  derivation by *different routes* and report separately. Their disagreement is the signal. This
  works only if neither agent saw the work of the other.
- **Independent topics.** Run a derivation in topic A and a solver in topic B, if they share no
  file and no generated code.
- **Literature lookups for different sources.**

## Never run concurrently

- **One narrative.** This includes a report, a write-up, and a document that a reader follows in
  order. Ten parallel writers finished fast. They used about 1.5M subagent tokens in 17 minutes.
  They produced ten voices with drifting notation. One author had to rewrite them.
- **One file.** If two agents edit the same file, you get a lost edit. You do not get a merge.
- **Stage scripts in the same topic.** Stage N+1 uses the output of stage N. If you run them
  together, one stage reads a half-written file.
- **Anything that writes `symbolic/generated/`.** The codegen diff gate compares against git. Two
  concurrent exports make its result meaningless.
- **Anything that touches git.** A hook blocks subagents from git
  (`.claude/hooks/subagent_git_guard.py`), because a concurrent agent cannot see what else
  someone staged.

## If you do parallelise

1. **Partition by writer.** Name, before dispatch, the one agent that can write each file. Do
   not write "roughly separate areas". Give an explicit list.
2. **State the partition in each brief.** Include what the agent must *not* touch. An agent with
   a fresh context cannot infer the boundary.
3. **Limit the concurrency to three agents.** Above that, the cost of reconciliation is more
   than the time that you save. A spike in `/usage` comes from fan-out. It does not come from a
   hard problem (`.claude/models.md`).
4. **Serialise anything that a licence limits.** `scripts/run` already takes a lock, because CAS
   licences limit concurrent kernels, and parallel agents would fail with licence errors. Do not
   work around the lock.
5. **Reconcile in one pass, by one author,** before you commit anything. Parallel work produces
   material. A single pass turns it into the record.
6. **Make one commit, after the reconciliation.** Never make one commit for each agent.
7. **Commit before you dispatch.** If the tree is clean before an agent runs, you can undo any
   mistake with one command. The diff afterwards is a complete, compact record of what the agent
   did. It is usually easier to review than the transcript of the agent. `/checkpoint` exists for
   this.
8. **Use separate worktrees when two agents must touch the same tree.** `git worktree` gives each
   agent its own checkout of its own branch. A concurrent write cannot collide. Land the branches
   in sequence, reconciled by one author. Subagents cannot create worktrees (the git guard blocks
   it). The main session sets them up.

## The honest test

Before you dispatch, ask: *if these two agents disagree, is that a finding or a mess?*

If it is a finding, parallelise. Examples: two independent audits, or two derivations by
different routes. If it is a mess, do not parallelise. Examples: two halves of one document, or
two edits to one file.
