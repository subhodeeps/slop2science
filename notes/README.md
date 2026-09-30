# notes — working notes, probes and open leads

Real, worth keeping, and **not the record.**

    probes/<session>/      exploratory scripts that were not stages: quick numerical probes,
                           dead ends, "what if" calculations. Kept with a README saying what
                           was being asked and what came of it.
    open_leads.md          things worth returning to, with enough context to resume.
    <topic>_notes.md       working notes on a topic.

## Precedence

A note **never** outranks the settled record. `docs/decision_log.md` and the source audit's
discrepancy rows outrank the notes they were synthesized from. Where a note and the record
disagree, **record the inconsistency** as an open question — do not quietly pick one. A report
writer once copied a claim from a working note that the decision log contradicted, and it
shipped (`docs/failure_modes.md` entry 9).

Keep probes rather than deleting them: a probe that ruled something out is evidence, and
re-running it later is cheaper than re-deriving why it was abandoned. Give each one a README —
a probe with no README is the orphaned artefact problem in miniature.
