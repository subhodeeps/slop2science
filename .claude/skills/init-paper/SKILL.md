---
name: init-paper
description: Initialize this template for a new paper-reproduction project. Interview the PI, fill each placeholder, write the conventions register and the tool-ownership registry, create the first prompt record, and print what remains to do.
disable-model-invocation: true
argument-hint: "[optional: paper arXiv ID or DOI]"
allowed-tools: Read Grep Glob Edit Write Agent Bash(git status) Bash(git ls-files *) Bash(scripts/py *) Bash(make check) Bash(make check-env) Bash(make fetch-source *)
---

# Initialize this project

Run this skill one time, at the start of a new project. **Refuse and stop** if `CLAUDE.md` has no
`{{` placeholders. In that case the project is already initialized, and a second run overwrites
real state. Tell the PI to edit the specific file.

## 1. Interview

Ask these questions as one batch. Use `AskUserQuestion` where the answer is a choice. Do not
guess any answer from the repository. Do not continue with a placeholder that has no answer. A
placeholder with no answer silently becomes a permanent wrong default.

0. Confirm the framing before you ask anything else. Use one line for each item. Then the PI
   corrects a wrong assumption now, and not after you write ten files. **The PI is the final
   authority here.** Claude asks, and does not choose a default, when a decision belongs to the
   PI. This project is a reproduction *and* an extension. It is not a reproduction alone
   (CLAUDE.md §1, §2).
1. **Project name.** Keep it short. The project uses it in headings and in the banner of the
   Makefile.
1a. **Author line.** Ask for the author line of the documents that the project converts to PDF
   (the reports and the README). Offer the wording as a choice: a name alone, or a name with an
   acknowledgement such as "(with help from Claude)". The PI decides the wording. Never take the
   name from `git config` or from the repository.
1b. **Licence.** The section Copying of `README.md` states the present policy of the template.
   The MIT licence covers all files. The CC BY 4.0 licence is an option for the documentation,
   the reports, and the images (plots and figures). Offer three choices:
   - **Adopt the policy** for the files of the project.
   - **Choose another licence.** The PI supplies the licence text.
   - **No licence yet.**

   Also ask for the copyright holder (the legal name) and the year. Never take them from
   `git config` or from the repository. Tell the PI to check if the institute or a funder has a
   say in the licence. Claude does not decide this. **If the PI skips the question, apply "No
   licence yet"**, and say so in the first lines of the init report. A licence is a grant in the
   name of the PI. Claude never grants one that nobody chose.
2. **Primary source.** This is the paper that the project reproduces. Ask the PI for one of
   these two:
   - an arXiv link or identifier (`$ARGUMENTS` can give it)
   - a BibTeX entry and the PDF, which the PI puts in `papers/_drop/`
   Do not ask for the authors or the title, and never ask the PI to edit `papers/sources.yaml`.
   The `literature` agent reads the details from the source and registers it (section 2,
   step 0).
3. **Objective.** Ask for two or three sentences. State what the project produces
   at its end. State what the *production* method is, as opposed to what is only a benchmark.
3a. **The new work.** Ask what the project intends to establish **beyond** the source. This is
   the new system, regime, method or open question. Ask what the eventual publication can claim.
   The reproduction is the foundation. The new work is what the foundation supports (CLAUDE.md
   §2). If the PI does not know yet, record that explicitly as an open scope question. Do not
   imply that the project is only a reproduction project.
4. **Pipeline.** Ask for the sequence of stages from the source equations to the final results,
   as an arrow chain. This becomes the indented block in `CLAUDE.md` §2 and the phase structure
   in `docs/implementation_checklist.md`.
5. **Topics.** A topic is a unit of work. Each topic gets its own `symbolic/<topic>/`,
   `derivation/<topic>/` and `validation/<topic>/`. Topics are usually a progression of
   increasing difficulty. The first topic is where the work starts.
6. **Tools.** Show the **default profile** and its default routes from `docs/toolchain.md`. Ask
   which of these the PI wants:
   - **Accept it**, "defaults".
   - **Override parts of it.** State which topic or kind goes to which tool, and which routes
     change.
   - **Decline it**, "ask me each time". The registry then starts empty. Claude asks when the
     work reaches each topic.

   **If the PI skips the question or does not answer it, treat that as "accept it".** The default
   profile is the fallback. Record which of the two cases applies. Write decision `D-002` in
   `docs/decision_log.md` as "adopted the default profile (chosen)" or as "(applied: the PI did
   not choose)". Write the rows into the two registries of `docs/toolchain.md`, and cite the
   decision. The init report must say, in its first lines, that the default profile applied and
   by which route. Then nobody overlooks a default that someone chose.
6a. **Libraries.** For each language that the project uses (Python, Julia), show the default list
   in `src/<lang>/packages.txt` with the one-line reason for each package. Ask this question: "which libraries do you expect to need?" The PI
   can add or remove entries. Name what the stated pipeline
   typically needs (an eigensolver package, a sparse-matrix package, a plotting library). Present
   these names as suggestions that the PI accepts or refuses. Never add one yourself. Write the
   final list of the PI into `packages.txt`. Write decision `D-003` in `docs/decision_log.md`:
   "default stack (chosen)", "default stack, amended (chosen)" or "(applied: the PI did not
   choose)". Do not add a library that nobody asked for. In the init report, say that `make setup`
   installs the list. Say which languages have no environment because the PI does not use them.
7. **Conventions to pin now.** Ask for units, notation, sign and orientation conventions, and how
   the project labels results. Anything that the PI does not know yet goes in as `OPEN`. Do not
   guess.
8. **Reproduction targets.** Ask which equations, tables and figures of the source the project
   intends to reproduce. This answer seeds `docs/reproduction_and_extension.md`. It is the most
   useful answer in this interview. It turns "reproduce the paper" into a finite list. Together
   with 3a, it also fixes the boundary between the two parts. That boundary is a scope decision,
   and therefore the PI decides it.

## 2. Write

Write in this order. If a step fails part-way, the project is visibly incomplete. It is not
subtly wrong.

0. The primary source. Dispatch the `literature` agent with the answer to question 2:
   - For an arXiv link, it runs `make fetch-source ID=<id> LABEL=<firstauthor><year>`. Then it
     reads the authors, the title, the version, and any journal reference and DOI from the
     arXiv record, and adds the BibTeX entry to `papers/refs.bib`.
   - For files in `papers/_drop/`, it does the intake of the `literature-audit` skill. It
     checks the BibTeX entry against the first page of the PDF.
   In both cases it registers the paper in `papers/sources.yaml` with the role `primary`, and
   returns the authors, title and identifier for `{{PRIMARY_SOURCE}}`. If it cannot reach arXiv
   (a network policy can block it), stop. Ask the PI to put the BibTeX and the PDF in
   `papers/_drop/`.
1. `CLAUDE.md`. Replace `{{PROJECT_NAME}}`, `{{OBJECTIVE}}`, `{{PIPELINE}}`,
   `{{PRIMARY_SOURCE}}` and `{{TOOL_A}}`, `{{TOOL_B}}`, `{{TOOL_C}}`. Change nothing else. §1, §3,
   §4, §6 and §7–§11 are the discipline. They are not project parameters (`TEMPLATE_GUIDE.md`
   §1).
1a. `docs/author.txt`. Replace the author line with the answer to question 1a. Keep the comment
   lines. `scripts/report_pdf.sh` reads this line for each document that has no author.
1b. The licence. **Keep `LICENSE-MIT.txt`, `LICENSE-CC-BY.txt` and the copyright line of the
   template author.** The files of the template are in the project, and the MIT licence requires
   its notice with each substantial part of them. Then follow the answer to question 1b:
   - *Adopt the policy.* Add the line `Copyright (c) <year> <holder>` under the existing line in
     `LICENSE-MIT.txt`, and the same line in the section Copying of `README.md`. Do not add a
     line that is already there.
   - *Another licence.* Put the text that the PI supplied in `LICENSE-<name>.txt`. Never write a
     licence text from memory, because an exact text matters. Change the section Copying to say
     which files each licence covers.
   - *No licence yet.* Change the section Copying to say that the files from the template keep
     the licences of the template, and that the licence of the other files is not decided. Put
     the open question in `handoff.md` and in `docs/STATUS.md`.

   Write decision `D-004` in `docs/decision_log.md`: "policy adopted (chosen)", "another licence
   (chosen)" or "no licence yet (applied: the PI did not choose)".
2. `docs/toolchain.md`. Fill the ownership registry between the `REGISTRY-START/END` markers. Use
   one row for each topic and each solver. Name the owning tool. Take it from the answers of the
   PI or from the default profile. Remove the notes for a tool that this project does not use.
   **Keep the Default profile section.** It is the standing fallback.
3. `docs/conventions.md`. Add one row for each convention from answer 7. Tag each row SOURCE,
   ADOPTED, OPEN or DERIVED, with the place where the project fixes it.
4. `docs/reproduction_and_extension.md`. Add one row for each reproduction target from answer 8,
   all `not attempted`. Add the extension rows from answer 3a, with what judges each one. Add the
   new-work deliverables that the paper needs. Fill all three tables, not only the first.
5. `docs/STATUS.md`. Set phase 0. Set the immediate next task to the source audit. The project has
   derived nothing and validated nothing. There are no blockers.
6. `docs/implementation_checklist.md`. Add the phase headings from answer 4, all unticked.
7. `papers/sources.yaml`. Check that step 0 registered the primary source with the role
   `primary`. Do not write the entry yourself.
8. `docs/prompts/A1_source_audit.md`. This is the first curated prompt record. Write it out so
   that the PI can run it. Leave the Outcome empty.
9. `src/julia/Project.toml` and `src/python/pyproject.toml`. Set the package name. Delete the
   directory of each language that this project does not use. Write the library list of the PI
   (6a) into `packages.txt` of that language. `make setup` builds the Python environment later
   with uv (the project commits `uv.lock` and does not commit `.venv`).
10. `Makefile`. Set `{{DEFAULT_TOPIC}}` to the first topic.
10a. `handoff.md`. Write the first real handoff. It replaces the "not initialized" placeholder.
    State where the project stands (initialized, nothing derived). State what the PI must still
    supply (the paper, missing tools, each convention that is `OPEN`). Set `Next` to the source
    audit, to match `docs/STATUS.md`. Follow `docs/handoff_guide.md`. The next session opens with
    this note. This is the first chance to build the habit.
11. The `description` and `when_to_use` lines of the agents and skills. Add the vocabulary of this
    project: its domain terms, method names and the terminology of the source. Then the automatic
    selection of skills and agents works. People skip this step easily. It is the reason why a
    well-written skill never starts.

## 3. Clean up and verify

- Delete `.claude/skills/init-paper/`. It did its job. If you keep it, someone can run it again
  and destroy state. (Keep `TEMPLATE_GUIDE.md`. It explains the design that the project
  inherits.)
- Run `make check` and `make check-init`. Both must pass.
- Run `make check-env`. Report which of the tools that the project chose are missing here.

## 4. Report

Print the items below in this order. **Start with the toolchain line.** State which profile or
override the project adopted. State if the PI chose it or if it applied because the PI did not
choose.

1. Each file that you wrote, with a one-line summary of what it now says.
2. **What only the PI can do.** The PI must install missing tools, and decide each convention that is `OPEN`. The PI must decide the licence of the project, if the answer
   to question 1b was "no licence yet". The PI must settle each question of
   language ownership that the default profile does not cover. If the profile applied because the
   PI did not choose, the PI must confirm it or change it.
3. The first session to run: the source audit, with `docs/prompts/A1_source_audit.md`.
4. A reminder that nobody writes code before the audit. This order is the purpose of this
   template. Each later gate assumes that the audit exists.
