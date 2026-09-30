# Structured proofs — the write-up format for a non-trivial argument

From Lamport's structured proof style, as recommended by *How to Train Your Slop Cannon*
([Open-Science-Ledger](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)).

Prose hides gaps. A paragraph that says "and therefore, after some algebra, it follows that"
is unfalsifiable at the level of the individual step, and the step it is hiding is exactly
the one that is wrong. A numbered hierarchy makes each step small, independently checkable,
and explicitly linked to what it depends on — and makes a gap **structurally visible** rather
than something a reader has to notice.

## The form

Every step has a hierarchical ID and a statement, and is justified in exactly one of three
ways:

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

- **`ASSUME`** opens a hypothesis scope; the matching `Q.E.D.` closes it.
- **`CASE`** introduces branches, and the write-up must state why they are exhaustive.
- **A step with no children and no justification is an exposed gap.** That is the format
  working as intended: name it, do not bury it. Mark it `GAP:` with what would close it.
- Where a step is established by a script, its justification is the evidence tag — so the
  hierarchy and the project's provenance chain are the same object.

## When to use it

Use it for an argument that is not a mechanical computation: a uniqueness or exhaustiveness
claim, a limiting argument, a gauge or regularity argument, anything where a reviewer would
ask "why does that follow?".

Do not use it for algebra a script verifies coefficient by coefficient. There, the script
*is* the proof and the write-up cites its check label — wrapping that in a proof hierarchy
adds ceremony and no rigour.

## Why it pays off

- **Verification targets a step, not a document.** The adversarial protocol
  (`.claude/skills/verification/reference/adversarial_protocol.md`) hands a verifier the
  numbered artifact and gets back per-step verdicts. That is only possible if the steps exist.
- **A failure is localized.** When a step fails, expand it into children and re-check the
  children. Decompose until each block is small enough to check reliably, and the error rate
  of the whole argument falls with it — the same reason one derivation stage per script is
  the rule.
- **The dependency structure is explicit.** "By 2.1 and 3" says what a later change would
  break. Prose does not.
