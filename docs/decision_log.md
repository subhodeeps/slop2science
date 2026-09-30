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
- **Which language implements which piece of work, and how the tools interoperate** — every
  row of `docs/toolchain.md`'s registry cites its entry here (CLAUDE.md §5).
- **What extension work is in scope**, and what is deliberately not: the boundary between
  reproduction and new work, and what the new work is for (CLAUDE.md §2).
- Any change to the scientific or numerical architecture (CLAUDE.md §9).
- Adding a tool or a dependency to the pipeline, or dropping one.
- Declaring a discrepancy closed, and on what evidence.
- Accepting a result whose validation is incomplete, with what is missing stated.
- A disagreement Claude raised that the PI overruled, where the reasoning is worth keeping
  (CLAUDE.md §1).

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

## D-002 — <example: language assignment and interoperation; replace or delete> — YYYY-MM-DD

Context:      Three co-equal tools are available. Without an explicit assignment, the same
              quantity ends up derived in two of them during debugging, both committed, with
              nothing saying which is authoritative — and both pass their own checks.
Options:      (a) leave it to whoever works on a topic; (b) assign per language by kind of
              work; (c) assign per topic and per solver, explicitly, and record each one.
Decision:     (c). {{TOOL_A}} is the record for the {{TOPIC_1}} derivation; {{TOOL_B}} is the
              record for its solver; coefficients cross from the first to the second by
              generated code only. Anything computed in a third tool is a `CROSS-CHECK` and
              never the record. Claude asks before assigning anything not covered here.
Consequences: `docs/toolchain.md`'s ownership and interoperation registries are filled in
              accordingly; every stage header names its owner tool; `make check-docs` fails
              if a topic has stage scripts and no registry row.
Evidence:     None — this is a scope and process decision, not a scientific one. The evidence
              that it was needed is `docs/failure_modes.md` and the fact that two records for
              one fact cannot be detected by either tool's own checks.
