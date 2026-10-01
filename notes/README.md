# notes — working notes, probes and open leads

Notes are real and worth keeping. They are **not the record.**

    probes/<session>/      exploratory scripts that are not stages: quick numerical probes,
                           dead ends, "what if" calculations. Each probe has a README that
                           states the question and the result.
    open_leads.md          items to return to, with enough context to resume.
    <topic>_notes.md       working notes on a topic.

## Precedence

A note **never** outranks the settled record. `docs/decision_log.md` and the discrepancy rows
of the source audit outrank the notes that they came from. If a note and the record disagree,
**record the inconsistency** as an open question. Do not pick one silently. A report writer once
copied a claim from a working note that the decision log contradicted. The claim shipped
(`docs/failure_modes.md` entry 9).

Keep probes. Do not delete them. A probe that ruled something out is evidence. To run it again
costs less than to derive again why the project abandoned the idea. Give each probe a README. A
probe with no README is a small orphaned artefact.
