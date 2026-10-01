---
paths:
  - "docs/prompts/**"
  - "symbolic/**"
  - "derivation/**"
---

# Research sessions — prompt recording

Each substantial research session records its own prompt. The prompt is part of the
reproducibility record (CLAUDE.md §10). It is not incidental chat. You cannot derive a result
again without the prompt that produced it. You also cannot check how much the model chose and
how much the prompt told it.

A session is "substantial" if it touches `symbolic/**` or `derivation/**`, audits a source, or
settles a convention.

## Before you start work

Write the prompt word for word to `docs/prompts/<ID>_<topic>.md`:

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

`<ID>` is a short, stable handle (`A1` source audit, `D2` second derivation stage, `V1` first
validation run). Use the same handle in commit messages and in `docs/STATUS.md`. Then you can
find a result, its prompt and its commit from each other.

State these items in the prompt. State what is in scope and **what is out of scope**. State
which files to read first and which subagent or skill the prompt expects. A prompt that is vague about scope causes
an agent to produce an artefact that nobody requested and nobody can explain later.

## At the end of the session

Fill in `## Outcome`. Include these items: stages completed, checks passed with their labels,
discrepancies raised, decisions forced (logged in `docs/decision_log.md`), files written and
commits. If an interruption stopped the session, state what the session completed and what it
left half-done.

## Automatic captures are not the curated record

`.claude/hooks/log_prompt.py` writes `docs/prompts/log/<session>.md` (every prompt, raw) and
`docs/prompts/auto/` (long prompts, one file each). These files are a safety net. A machine
writes them, and they include false starts and harness traffic. The curated record above is the
citable record. Promote an auto-capture by hand. Never cite `auto/` as a curated record.
