# Structured proofs — the write-up format for a non-trivial argument

This format comes from the structured proof style of Lamport. *How to Train Your Slop Cannon*
recommends it
([Open-Science-Ledger](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)).

Prose hides gaps. A paragraph that says "and therefore, after some algebra, it follows that" is
not falsifiable at the level of a single step. The step that it hides is exactly the step that
is wrong. A numbered hierarchy makes each step small. A reader can check each step
independently. The hierarchy links each step explicitly to what it depends on. It makes a gap
**visible in the structure**. The reader does not have to notice the gap.

## The form

Each step has a hierarchical ID and a statement. Exactly one of three justifications supports
each step:

```
1. <statement>
   PROOF: obvious from <cited result / stated assumption>.

2. ASSUME: <hypothesis>
   2.1. <statement>
        PROOF: by 1 and <cited result>.
   2.2. <statement>
        PROOF:
        2.2.1. <sub-statement>
               PROOF: [E: `symbolic/<topic>/stage_04.wls`, "residual vanishes"]
        2.2.2. <sub-statement>
               PROOF: by 2.2.1 and the assumption.
        Q.E.D. by 2.2.1, 2.2.2.
   Q.E.D. by 2.1, 2.2.

3. CASE: <condition A>
   ...
4. CASE: <condition B>          (the cases must be exhaustive — say why)
   ...

Q.E.D. by 2, 3, 4.
```

- **`ASSUME`** opens the scope of a hypothesis. The matching `Q.E.D.` closes it.
- **`CASE`** introduces branches. The write-up must state why the branches are exhaustive.
- **A step with no children and no justification is an exposed gap.** The format works as
  intended here. Name the gap. Do not bury it. Mark it `GAP:` with what would close it.
- If a script establishes a step, the justification is the evidence tag. Then the hierarchy and
  the chain of provenance of the project are the same object.

## When to use it

Use it for an argument that is not a mechanical computation. Examples: a claim of uniqueness or
exhaustiveness, a limiting argument, a gauge or regularity argument, and anything where a
reviewer asks "why does that follow?".

Do not use it for algebra that a script verifies coefficient by coefficient. In that case the
script *is* the proof. The write-up cites its check label. A proof hierarchy around it adds
ceremony and no rigour.

## Why it pays off

- **Verification targets a step. It does not target a document.** The adversarial protocol
  (`.claude/skills/verification/reference/adversarial_protocol.md`) gives a verifier the
  numbered artifact and receives a verdict for each step. This is possible only if the steps
  exist.
- **A failure is local.** If a step fails, expand it into children and check the children
  again. Decompose until each block is small enough to check reliably. Then the error rate of
  the whole argument falls. This is the same reason why one derivation stage for each script is
  the rule.
- **The structure of the dependencies is explicit.** "By 2.1 and 3" states what a later change
  breaks. Prose does not state it.
