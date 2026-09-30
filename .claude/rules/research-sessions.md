---
paths:
  - "docs/prompts/**"
  - "symbolic/**"
  - "derivation/**"
---

# Research sessions — prompt recording

Every substantial research session records its own prompt. The prompt is part of the
reproducibility record (CLAUDE.md §10), not incidental chat: a result without the prompt that
produced it cannot be re-derived, and cannot be checked for how much the model chose versus
was told.

A session is "substantial" if it touches `symbolic/**` or `derivation/**`, audits a source,
or settles a convention.

## Before starting work

Write the prompt verbatim to `docs/prompts/<ID>_<topic>.md`:

    <!-- session <id> | <date> -->

    # <ID> — <topic>

    ## Prompt

    ```text
    <the prompt, verbatim, never paraphrased or tidied>
    ```

    ## Outcome

    (filled in at session close)

    ## Revisions for reuse

    (what to change when adapting this prompt for another topic or another source)

`<ID>` is a short stable handle (`A1` source audit, `D2` second derivation stage, `V1` first
validation run). Use the same handle in commit messages and in `docs/STATUS.md` so a result,
its prompt and its commit are findable from each other.

State explicitly in the prompt: what is in scope, **what is out of scope**, which files to
read first, and which subagent or skill it expects. A prompt vague about scope is how an
agent ends up producing an unrequested artefact that nobody can account for later.

## At the end of the session

Fill in `## Outcome`: stages completed, checks passed with their labels, discrepancies
raised, decisions forced (and logged in `docs/decision_log.md`), files written, commits. If
the session was interrupted, say what was completed and what was left half-done.

## Automatic captures are not this

`.claude/hooks/log_prompt.py` writes `docs/prompts/log/<session>.md` (every prompt, raw) and
`docs/prompts/auto/` (long prompts, one file each). Those are a safety net, machine-written
and including false starts and harness traffic. The curated record above is the citable one.
Promote an auto-capture by hand; never cite `auto/` as if it were curated.
