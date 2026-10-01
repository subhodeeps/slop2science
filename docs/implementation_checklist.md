# Implementation checklist

This file tracks progress for each item. It is the companion of `docs/STATUS.md`. **Tick a box
only with evidence**: a script and its check count, or a record. Never tick a box because a
file exists.

A tag shows what an open item needs:

- **[PI]** needs a decision
- **[tool]** needs a computation on a machine that has the owning tool
- **[lit]** needs a source
- **[doc]** needs documentation

`/init-paper` replaces the phase headings below with the pipeline of this project.

## Infrastructure

- [ ] `/init-paper` initialized the repository from the template, and `make check-init`
      passes
- [ ] `make check` passes (hooks self-test, references, evidence tags, staleness)
- [ ] CI runs the tool-free tier on every push
- [ ] `make check-env` ran. STATUS records which tools each machine has.
- [ ] The language environments exist, and the project committed their lock files (`make setup`)
- [ ] `make test` runs (it can only skip absent languages)
- [ ] [PI] The PI decided tool ownership **and interoperation**, logged it (D-002) and
      registered it in `docs/toolchain.md`
- [ ] [PI] The PI chose the Python and Julia libraries, logged them (D-003) and recorded them
      in `src/<lang>/packages.txt`
- [ ] The shared helper code and its self-tests exist (`symbolic/common/`)
- [ ] Prompt recording works (a curated record exists for the first real session)

## Source audit

- [ ] `papers/sources.yaml` registers the primary source with verified identifiers
- [ ] Someone read the source in full for each equation and table in scope. Use the `.tex` file
      where it exists. Otherwise use the rendered pages (`reference/corpus.md`).
- [ ] `docs/<topic>_source_audit.md` exists, written from the template
- [ ] `docs/conventions.md` records the conventions. Ambiguous conventions have `OPEN`.
- [ ] Each displayed equation in scope has a record with its number and role (§E)
- [ ] The audit lists what the source omits, in dependency order (§M). This is the derivation
      plan.
- [ ] The audit records discrepancies in the five-item form (§N). Nobody resolved one silently.
- [ ] `docs/reproduction_and_extension.md` has content: reproduction targets, **and** the
      candidate extensions that the audit found, for the PI to rule in or out

## Derivation — {{TOPIC_1}}

- [ ] [tool] Stage 01 — <setup / background>, with checks
- [ ] [tool] Stage 02 — <...>
- [ ] A write-up exists for each stage. It cites the script and the check label at each
      displayed equation.
- [ ] The `stages.txt` manifest is complete. `make stages TOPIC={{TOPIC_1}}` is clean from a
      fresh checkout.
- [ ] The project reproduced the source equations coefficient by coefficient, where it claims
      this
- [ ] The project derived the singular structure and the limits. It did not assume them.
- [ ] The project exported the coefficients, and `make codegen-check TOPIC={{TOPIC_1}}` is clean

## Implementation — {{TOPIC_1}}

- [ ] `derivation/` records and verifies the formulation **before** the solver code
      (`.claude/skills/solver-workflow/reference/formulation_checklist.md`)
- [ ] A known-answer test of the **full chain** exists, in each precision tier
- [ ] The solver uses generated coefficients only
- [ ] The residuals are in the original problem
- [ ] The project recorded the resolution study (N, 2N)
- [ ] The project recorded the precision study
- [ ] Artefact filtering uses a diagnostic, with the reasons recorded
- [ ] Parameter continuation matches by overlap, not by ordering
- [ ] An independent-method benchmark exists, with the conversion written out
- [ ] The driver writes the records. They are complete according to
      `docs/validation_protocol.md` §12.
- [ ] The results are in `Validated` in STATUS, with evidence

## Extension — new work beyond the source

The extension is the second part of the project. It is not a follow-on (CLAUDE.md §2). The PI
decides the scope. Each item names its standard of judgement, because the source cannot
validate any of it.

- [ ] [PI] The PI decided the extension scope and logged it. The rows are in
      `docs/reproduction_and_extension.md` §2.
- [ ] [PI] The PI decided language ownership and interoperation for the new work, and
      registered them (`docs/toolchain.md`)
- [ ] The reproduction gate passed for what the extension builds on. The extension does not
      start on unverified foundations.
- [ ] [tool] The derivation stages for the new work exist, with checks, one stage for each
      script
- [ ] The extension recovers the already-verified case as a **limiting case**. A check runs
      this.
- [ ] [tool] The project extends or writes the solver. The known-answer test of the full chain still
      passes.
- [ ] An independent-method benchmark exists where one exists. Where none exists, the record
      states what the result rests on.
- [ ] The project recorded negative results. It did not drop them
      (`docs/reproduction_and_extension.md`, `negative`).
- [ ] The results are in `Extension / new work` in STATUS, with evidence and the standard that
      judges each result

## Write-up

- [ ] [PI] The PI decided which document the project writes, a methods report or a
      manuscript, and what it claims
- [ ] One author wrote `reports/{{TOPIC_1}}_report.md` as a paper, in chunks
- [ ] Each result equation cites a check. Each number cites a record.
- [ ] The text states the discrepancies. An appendix gives them in full.
- [ ] `make report TOPIC={{TOPIC_1}}` renders
- [ ] The PI reviewed the report

## Per session

- [ ] Someone recorded the prompt before the work started
- [ ] `make check` and `make test` ran
- [ ] `/session-close` ran: orphan check, STATUS, reproduction matrix, decisions, prompt outcome
