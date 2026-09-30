---
name: init-paper
description: Initialize this template for a new paper-reproduction project - interview the PI, fill every placeholder, write the conventions register and the tool-ownership registry, seed the first prompt record, and print what is left to do.
disable-model-invocation: true
argument-hint: "[optional: paper arXiv ID or DOI]"
allowed-tools: Read Grep Glob Edit Write Bash(git status) Bash(git ls-files *) Bash(scripts/py *) Bash(make check) Bash(make check-env)
---

# Initialize this project

Run once, at the start of a new project. **Refuse and stop** if `CLAUDE.md` no longer
contains `{{` placeholders: the project is already initialized, and re-running would
overwrite real state. Tell the PI to edit the specific file instead.

## 1. Interview

Ask these as one batch (use `AskUserQuestion` where the answer is a choice). Do not guess
any of them from the repository, and do not proceed with a placeholder still unanswered —
an unanswered placeholder silently becomes a permanent wrong default.

0. Confirm the framing before asking anything else, in one line each, so a wrong assumption
   is corrected now rather than after ten files are written: **the PI is the final authority
   here**, Claude asks rather than defaulting when a decision is the PI's, and this project is
   a reproduction *and* an extension, not a reproduction alone (CLAUDE.md §1, §2).
1. **Project name** — short, used in headings and the Makefile banner.
2. **Primary source** — the paper being reproduced: authors, title, journal/preprint,
   identifier. If `$ARGUMENTS` gave an arXiv ID or DOI, offer it as the default.
3. **Objective** — two or three sentences: what the project will have produced when it is
   done, and what the *production* method is (as opposed to what is only a benchmark).
3a. **The new work** — what the project intends to establish **beyond** the source: the new
   system, regime, method or open question, and what the eventual paper would claim. The
   reproduction is the foundation; this is what it is a foundation for (CLAUDE.md §2). If the
   PI does not yet know, record that explicitly as an open scope question rather than
   implying the project is a reproduction project.
4. **Pipeline** — the sequence of stages from source equations to final results, as an
   arrow chain. This becomes `CLAUDE.md` §2's indented block and the phase structure in
   `docs/implementation_checklist.md`.
5. **Topics** — the units of work that each get their own `symbolic/<topic>/`,
   `derivation/<topic>/`, `validation/<topic>/`. Usually a progression of increasing
   difficulty. The first one is where work starts.
6. **Tools — the PI's decision, in two parts.** All three are co-equal and Claude never
   chooses (CLAUDE.md §1, §5), so ask both parts explicitly and do not offer a default split
   as though it were obvious:
   - **Ownership**: which of Mathematica, Python and Julia this project will use, and for
     each topic and each solver, **which tool is the record**.
   - **Interoperation**: which tool hands what to which, in which direction, by what
     mechanism. Include the cases the PI expects to need later, not only the first one.

   Record both as decision `D-002` in `docs/decision_log.md`, and write them into
   `docs/toolchain.md`'s two registries with that reference. Anything the PI leaves open stays
   open, and Claude asks again when the work reaches it.
7. **Conventions to pin now** — units, notation, sign/orientation conventions, how results
   are labelled. Anything the PI does not yet know goes in as `OPEN`, not as a guess.
8. **Reproduction targets** — which equations, tables and figures of the source the project
   intends to reproduce. This seeds `docs/reproduction_and_extension.md`, and it is the single
   most useful answer in this interview: it turns "reproduce the paper" into a finite list.
   Together with 3a it also fixes the boundary between the two halves, which is a scope
   decision and therefore the PI's.

## 2. Write

In this order, so a failure part-way leaves an obviously-incomplete project rather than a
subtly-wrong one:

1. `CLAUDE.md` — replace `{{PROJECT_NAME}}`, `{{OBJECTIVE}}`, `{{PIPELINE}}`,
   `{{PRIMARY_SOURCE}}`, `{{TOOL_A}}`/`{{TOOL_B}}`/`{{TOOL_C}}`. Change nothing else:
   §1, §3, §4, §6, §8–§11 are the discipline and are not project parameters
   (`TEMPLATE_GUIDE.md` §1).
2. `docs/toolchain.md` — fill the ownership registry between the `REGISTRY-START/END`
   markers: one row per topic and per solver, naming its owning tool. Remove profiles for
   tools this project will not use.
3. `docs/conventions.md` — one row per convention from answer 7, each tagged SOURCE /
   ADOPTED / OPEN / DERIVED, with where it is fixed.
4. `docs/reproduction_and_extension.md` — one row per reproduction target from answer 8, all
   `not attempted`; the extension rows from answer 3a with what each will be judged against;
   and the new-work deliverables the paper would need. All three tables, not only the first.
5. `docs/STATUS.md` — phase 0; immediate next task = the source audit; nothing derived,
   nothing validated, no blockers.
6. `docs/implementation_checklist.md` — the phase headings from answer 4, all unticked.
7. `papers/sources.yaml` — the primary source, with role `primary`.
8. `docs/prompts/A1_source_audit.md` — the first curated prompt record, written out and
   ready for the PI to run, with an empty Outcome.
9. `src/julia/Project.toml` and/or `src/python/pyproject.toml` — the package name. Delete the
   directory for any language this project will not use.
10. `Makefile` — `{{DEFAULT_TOPIC}}` = the first topic.
10a. `handoff.md` — the first real handoff, replacing the "not initialized" placeholder: where
    the project stands (initialized, nothing derived), what the PI still has to supply (the
    paper, missing tools, any convention left `OPEN`), and `Next` = the source audit, matching
    `docs/STATUS.md`. Follow `docs/handoff_guide.md`; this is the note the next session opens
    with, so it is the first chance to get the habit right.
11. Agent and skill `description` / `when_to_use` lines — add this project's vocabulary
    (its domain terms, method names, and the source's own terminology) so that automatic
    skill and agent selection actually triggers. This step is easy to skip and it is the
    reason a well-written skill never fires.

## 3. Clean up and verify

- Delete `.claude/skills/init-paper/` — it has done its job, and leaving it invites a
  destructive re-run. (Keep `TEMPLATE_GUIDE.md`: it explains the design you are inheriting.)
- Run `make check` and `make check-init`; both must pass.
- Run `make check-env` and report which of the project's chosen tools are missing here.

## 4. Report

Print, in this order:

1. Every file written, with a one-line summary of what it now says.
2. **What only the PI can do**: fetch the paper (`make fetch-source ID=…`), install missing
   tools, decide each convention left `OPEN`, and settle any language-ownership or
   interoperation question left unanswered in 6.
3. The first session to run: the source audit, via `docs/prompts/A1_source_audit.md`.
4. A reminder that no code is written before the audit — that ordering is the point of this
   template, and every later gate assumes the audit exists.
