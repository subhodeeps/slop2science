# Implementation checklist

Item-by-item progress, the companion to `docs/STATUS.md`. **A box is ticked only with
evidence** — a script and its check count, or a record. Never from a file's existence.

Open items are tagged by what they need: **[PI]** a decision, **[tool]** a computation on a
machine that has the owning tool, **[lit]** a source, **[doc]** documentation only.

`/init-paper` replaces the phase headings below with this project's pipeline.

## Infrastructure

- [ ] Repository initialized from the template (`/init-paper`, `scripts/check_initialized.sh` passes)
- [ ] `make check` passes (hooks self-test, references, evidence tags, staleness)
- [ ] CI running the tool-free tier on every push
- [ ] `make check-env` run; which tools are present on which machine recorded in STATUS
- [ ] Language environments created and their lock files committed (`make setup`)
- [ ] `make test` runs (even if it only skips absent languages)
- [ ] Tool-ownership registry filled in `docs/toolchain.md`
- [ ] Shared helper code and its self-tests in place (`symbolic/common/`)
- [ ] Prompt recording working (a curated record exists for the first real session)

## Source audit

- [ ] Primary source registered in `papers/sources.yaml` with verified identifiers
- [ ] Source read in full, as rendered pages, for every equation and table in scope
- [ ] `docs/<topic>_source_audit.md` written from the template
- [ ] Conventions recorded in `docs/conventions.md`, ambiguous ones marked `OPEN`
- [ ] Every displayed equation in scope recorded with its number and role (§E)
- [ ] What the source omits, listed in dependency order (§M) — this is the derivation plan
- [ ] Discrepancies recorded in five-point form (§N); none silently resolved
- [ ] `docs/reproduction_matrix.md` populated with every reproduction target

## Derivation — {{TOPIC_1}}

- [ ] [tool] Stage 01 — <setup / background>, with checks
- [ ] [tool] Stage 02 — <...>
- [ ] Write-up per stage, citing script and check label at every displayed equation
- [ ] `stages.txt` manifest complete; `make stages TOPIC={{TOPIC_1}}` clean from a fresh checkout
- [ ] Source equations reproduced coefficient by coefficient where claimed
- [ ] Singular structure / limits derived, not assumed
- [ ] Coefficients exported; `make codegen-check TOPIC={{TOPIC_1}}` clean

## Implementation — {{TOPIC_1}}

- [ ] Formulation recorded and verified in `derivation/` **before** solver code
      (`.claude/skills/solver-workflow/reference/formulation_checklist.md`)
- [ ] Known-answer test of the **full chain**, in every precision tier
- [ ] Solver implemented from generated coefficients only
- [ ] Residuals in the original problem
- [ ] Resolution study (N, 2N) recorded
- [ ] Precision study recorded
- [ ] Artefact filtering by diagnostic, with reasons recorded
- [ ] Parameter continuation, matched by overlap not ordering
- [ ] Independent-method benchmark, conversion written out
- [ ] Records written by the driver, complete per `docs/validation_protocol.md` §12
- [ ] Results moved to `Validated` in STATUS with evidence

## Write-up

- [ ] `reports/{{TOPIC_1}}_report.md` written as a paper, one author, in chunks
- [ ] Every result equation cites a check; every number cites a record
- [ ] Discrepancies in the text and in full in an appendix
- [ ] `make report TOPIC={{TOPIC_1}}` renders
- [ ] PI review

## Per session

- [ ] Prompt recorded before work started
- [ ] `make check` and `make test` run
- [ ] `/session-close`: orphan check, STATUS, reproduction matrix, decisions, prompt outcome
