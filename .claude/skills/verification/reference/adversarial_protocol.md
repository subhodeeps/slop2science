# Adversarial verification — prover and verifier

Adapted from *How to Train Your Slop Cannon*
([Open-Science-Ledger](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)).

One agent proves; a second attacks the proof and **never sees the first agent's reasoning.**
That asymmetry is the whole mechanism. A verifier that has read the derivation inherits its
blind spots and its confidence; a verifier handed only the numbered artifact has to check
each step on its own terms.

## Protocol

1. **Prover.** Dispatch `derivation` with: *produce a structured proof of this claim, in the
   numbered form of `reference/structured_proofs.md`. Every step is either obvious from a
   cited result, justified by earlier steps, or expanded into child steps.*

2. **Verifier, with the artifact alone.** Dispatch `verification` with **only the numbered
   proof** — not the prover's transcript, not its commentary, not your own expectation of
   the answer. The brief is: *you are the verifier. Attack every step. Accept nothing you
   cannot check. For each step, state: accepted, challenged (and why), or unjustified.*

   **Do not tell the verifier what you hope it concludes.** A model asked "check that this is
   right" and a model asked "attack this" behave differently, and the first is sycophancy
   waiting to happen (`docs/failure_modes.md` 0c).

3. **Iterate until the challenges dry up.** Each surviving challenge either gets a new child
   step that closes it, or becomes a recorded gap. A challenge answered by rewording rather
   than by argument has not been answered.

4. **Push independence further where a claim carries real weight.** A verifier from a
   different model family, or a different capability class, shares fewer failure modes than
   two runs of the same model. Two runs of the same model on the same input are not
   independent evidence; do not report them as such.

## When to use it

- A claim that would change a project convention or close a discrepancy.
- A result the project's own numerics cannot check (a limit, a scaling argument, a uniqueness
  claim).
- Any step a reviewer would reasonably not take on trust.
- Before a claim of this kind enters a report.

Not for routine algebra a script already checks coefficient by coefficient. The script is a
better verifier there, and it is re-runnable.

## Recording it

The prover's artifact and the verifier's findings both go in the record — the challenges
especially, including the ones that were answered. *"Step 2.3 was challenged as assuming
regularity at the boundary; closed by 2.3.1"* is far more useful to a later reader than a
clean proof with no history, because it says where the argument is load-bearing.

A claim that survived adversarial verification is recorded as such, naming the agents and
models used. That is not the same status as machine-checked, and must not be reported as
though it were (`docs/WORKFLOW.md` §3a).
