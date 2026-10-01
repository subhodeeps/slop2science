# Adversarial verification — prover and verifier

This protocol adapts an idea from *How to Train Your Slop Cannon*
([Open-Science-Ledger](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)).

One agent proves. A second agent attacks the proof and **never sees the reasoning of the first
agent.** This asymmetry is the whole mechanism. A verifier that has read the derivation inherits
its blind spots and its confidence. A verifier that receives only the numbered artifact must
check each step on its own terms.

## Protocol

1. **Prover.** Dispatch `derivation` with this instruction: *produce a structured proof of this
   claim, in the numbered form of `reference/structured_proofs.md`. Each step is obvious from a
   cited result, or justified by earlier steps, or expanded into child steps.*

2. **Verifier, with the artifact alone.** Dispatch `verification` with **only the numbered
   proof.** Do not give it the transcript of the prover, its commentary or your own expectation
   of the answer. The brief is: *you are the verifier. Attack each step. Accept nothing that you
   cannot check. For each step, state one of three verdicts: accepted, challenged (and why), or
   unjustified.*

   **Do not tell the verifier what you hope that it concludes.** A model that receives "check
   that this is right" and a model that receives "attack this" behave differently. The first
   case is sycophancy that waits to happen (`docs/failure_modes.md` 0c).

3. **Iterate until the challenges stop.** Each surviving challenge gets a new child step that
   closes it, or becomes a recorded gap. If you answer a challenge by rewording and not by
   argument, you did not answer it.

4. **Increase the independence where a claim carries real weight.** A verifier from a different
   model family, or a different capability class, shares fewer failure modes than two runs of
   the same model. Two runs of the same model on the same input are not independent evidence.
   Do not report them as such.

## When to use it

- A claim that would change a convention of the project or close a discrepancy.
- A result that the numerics of the project cannot check (a limit, a scaling argument, a
  uniqueness claim).
- Any step that a reviewer would reasonably not accept on trust.
- Before a claim of this kind enters a report.

Do not use it for routine algebra that a script already checks coefficient by coefficient. The
script is a better verifier there, and you can run it again.

## Record it

Put the artifact of the prover and the findings of the verifier in the record. Include the
challenges, especially the challenges that someone answered. *"Step 2.3 had a challenge: it
assumes regularity at the boundary. Step 2.3.1 closed it."* helps a later reader more than a clean
proof with no history. It shows where the argument carries load.

Record a claim that survived adversarial verification as such. Name the agents and the models
that you used. This status is not the same as machine-checked. Do not report it as
machine-checked (`docs/WORKFLOW.md` §3a).
