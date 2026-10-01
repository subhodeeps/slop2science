# Decision log

This file records the decisions of the PI. Put the newest entry last. Append only. Never
rewrite an entry. A new entry supersedes an old decision. State what it supersedes and why.
The history of why a convention changed is often more useful than the convention.

## Format

    ## D-NNN — <title> — <date>
    Context:      why a decision was needed
    Options:      the alternatives actually considered
    Decision:     what the PI decided
    Consequences: which equations, modules and documents are affected; which validation
                  must be repeated
    Evidence:     the scripts, records or sources supporting it (or: none, and why)

Fill in each field. `Options:` matters most in one year. If a decision has no recorded
alternatives, nobody can revisit it. Someone can only reverse it.

## What belongs here

- Each convention that the project adopts where the source is ambiguous, or where the project
  departs from the source.
- **Which language implements which piece of work, and how the tools interoperate.** Each row of
  the registry in `docs/toolchain.md` cites its entry here (CLAUDE.md §5). This includes the
  adoption of the default profile. State if the PI chose it, or if it applied because the PI did
  not choose.
- **Which extension work is in scope, and which is not.** This is the boundary between
  reproduction and new work, and the purpose of the new work (CLAUDE.md §2).
- Each change to the scientific or numerical architecture (CLAUDE.md §9).
- The addition or removal of a tool or a dependency of the pipeline.
- The closure of a discrepancy, and the evidence for it.
- The acceptance of a result with incomplete validation. State what is missing.
- A disagreement that Claude raised and the PI overruled, if the reasoning has value
  (CLAUDE.md §1).

## What does not belong here

Task order, session planning, and anything that you can reverse without consequence. Put these
in `docs/STATUS.md`.

---

## D-001 — <example: the worked shape of an entry; replace or delete> — YYYY-MM-DD

Context:      The source states X in its text. Its Eq. (N) implies Y. All later work depends on
              the choice, and the two differ by a sign.
Options:      (a) follow the text. (b) Follow the displayed equations. (c) Treat it as an
              error in the reading of this project and derive again.
Decision:     Follow the displayed equations (b). The derivation of this project gives Y
              independently, and that derivation rules out (c).
Consequences: This affects stages 04–09 and all later results. Compute the comparison with
              Table 1 of the source again, in the adopted convention.
              The row "sign convention" in `docs/conventions.md` becomes ADOPTED.
Evidence:     `symbolic/<topic>/stage_04_reduce.wls` check "reduced system matches Eq. (N)",
              and the five-item record in `docs/<topic>_source_audit.md` §N.
              The question of whether the source *intended* X stays open. Numerics cannot
              decide it. It needs a statement from the authors.

## D-002 — <example: language assignment and interoperation; replace or delete> — YYYY-MM-DD

Context:      Three tools of equal capability are available. Without an explicit assignment,
              debugging derives the same quantity in two of them. Both results are committed,
              nothing states which result is authoritative, and both pass their own checks.
Options:      (a) leave it to the person who works on a topic. (b) Assign each topic and solver
              explicitly. (c) Adopt the default profile (`docs/toolchain.md`) and
              override it where necessary.
Decision:     (c), chosen. {{TOOL_A}} is the record for the {{TOPIC_1}} derivation. {{TOOL_B}}
              is the record for its solver. Coefficients pass from the first to the second by
              generated code only. A computation in a third tool is a `CROSS-CHECK`. It never
              becomes the record. (If the PI had not chosen, this entry would say "applied: the
              PI did not choose", and the init report would state it.) Claude asks about
              anything that the profile does not cover.
Consequences: Fill in the ownership and interoperation registries of `docs/toolchain.md`
              accordingly. The header of each stage names its owner tool. `make check-docs`
              fails if a topic has stage scripts and no registry row.
Evidence:     None. This is a scope and process decision. It is not a scientific decision.
              The evidence that it was necessary is `docs/failure_modes.md`, and the fact that
              the checks of one tool cannot detect two records for one fact.

## D-003 — <example: library stack for the Python and Julia environments; replace or delete> — YYYY-MM-DD

Context:      Each language that the project uses gets its own environment (`src/python` with
              uv, `src/julia` with `Project.toml`). The contents of the environments decide
              what a result can depend on. A library that nobody chose is a dependency that
              nobody checked.
Options:      (a) install what turns out to be necessary, when it is necessary. (b) Install
              the default minimum stack in `src/<lang>/packages.txt`, plus what the PI names.
Decision:     (b), chosen. Python: numpy, scipy, mpmath, sympy, matplotlib, plus {{PI_PYTHON}}.
              Julia: the default seven, plus {{PI_JULIA}}. (If the PI had not answered, this
              entry would say "applied: the PI did not choose".)
Consequences: `make setup` installs the lists and writes `uv.lock` and `Manifest.toml`. Commit
              both files. A later addition is a PI decision. It needs a new line in
              `packages.txt` and an entry here.
Evidence:     None. This is a scope decision. It is not a scientific decision.
