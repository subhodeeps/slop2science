# Decision log

PI decisions, newest last. Append only; never rewrite an entry. A superseded decision gets a
**new** entry that says what it supersedes and why — the history of why a convention changed
is often more useful than the convention.

## Format

    ## D-NNN — <title> — <date>
    Context:      why a decision was needed
    Options:      the alternatives actually considered
    Decision:     what the PI decided
    Consequences: which equations, modules and documents are affected; which validation
                  must be repeated
    Evidence:     the scripts, records or sources supporting it (or: none, and why)

Every field is filled. `Options:` matters most in a year's time: a decision with no recorded
alternatives cannot be revisited, only reversed.

## What belongs here

- Any convention the project adopts where the source is ambiguous or the project departs
  from it.
- Any change to the scientific or numerical architecture (CLAUDE.md §9).
- Adding a tool or a dependency to the pipeline.
- Declaring a discrepancy closed, and on what evidence.
- Accepting a result whose validation is incomplete, with what is missing stated.

## What does not

Task ordering, session planning, and anything reversible without consequence. Those go in
`docs/STATUS.md`.

---

## D-001 — <example: the worked shape of an entry; replace or delete> — YYYY-MM-DD

Context:      The source states X in its text, while its Eq. (N) implies Y. Everything
              downstream depends on which is used, and the two differ by a sign.
Options:      (a) follow the text; (b) follow the displayed equations; (c) treat it as an
              error in this project's reading and re-derive.
Decision:     Follow the displayed equations (b). The project's own derivation independently
              gives Y, and (c) is ruled out by that derivation.
Consequences: Affects stages 04–09 and every result downstream. The comparison against the
              source's own Table 1 must be recomputed in the adopted convention.
              `docs/conventions.md` row "sign convention" becomes ADOPTED.
Evidence:     `symbolic/<topic>/stage_04_reduce.wls` check "reduced system matches Eq. (N)";
              the five-point record in `docs/<topic>_source_audit.md` §N.
              Whether the source *intended* X remains open and is not decidable numerically —
              it needs a statement from its authors.
