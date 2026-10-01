# Template guide — what to change, and what to leave alone

Read this guide one time, before `/init-paper`. It states which parts of this repository you
rewrite for your paper and which parts must stay unchanged. It also gives the reasons.

## 1. The three layers

| Layer | Files | Change it? |
|---|---|---|
| **Charter and discipline** | `CLAUDE.md` §1, §3–§4, §6–§11; `.claude/rules/`; `docs/WORKFLOW.md`; `docs/failure_modes.md`; the hooks | **No.** These files encode failure modes. They do not encode preferences. §1 matters most: the authority of the PI, and asking in place of choosing a default. The rest depends on it. Change these files only after your project meets a failure that they do not cover. Then log the change in `docs/decision_log.md`. |
| **Project parameters** | the `{{PLACEHOLDERS}}` in `CLAUDE.md`; `docs/conventions.md`; the ownership registry in `docs/toolchain.md`; `papers/sources.yaml`; the trigger phrases of agents and skills | **Yes, one time**, through `/init-paper`. Then change them as the project evolves. |
| **Scientific content** | `derivation/`, `symbolic/`, `src/`, `tests/`, `validation/`, `reports/`, `docs/reproduction_and_extension.md`, `docs/STATUS.md` | **Yes, continuously.** This is the work. It ships empty. |

If you edit layer 1 in the first week, the template is probably wrong for your problem. The rule
is not only inconvenient. Say which rule and why in `docs/decision_log.md`. Then the next project
inherits the reasoning.

## 2. What `/init-paper` does

It interviews you. Then it writes these items:

- `CLAUDE.md`: the project name, the objective, the pipeline, the primary source and the names of
  the three tools.
- `docs/conventions.md`: the first rows of the conventions register (units, notation, sign and
  orientation conventions, labelling). Each row has the tag SOURCE, ADOPTED, OPEN or DERIVED.
- `docs/toolchain.md`: the **ownership registry**. It states which tool is the record for which
  topic and which solver.
- `docs/STATUS.md`: phase 0, the first immediate task (the source audit) and no blockers.
- `docs/prompts/A1_source_audit.md`: the first curated prompt record, ready to run.
- The `description` and `when_to_use` lines of agents and skills, so that the triggers match your
  vocabulary.
- The package names in `src/julia/Project.toml` and `src/python/pyproject.toml`, and the library
  lists `src/python/packages.txt` and `src/julia/packages.txt` (the choice of the PI, decision
  D-003).

Then it deletes its own placeholder scaffolding. It prints a checklist of what only you can do:
decide open conventions and install tools. You do not fetch or register the paper yourself. You
give `/init-paper` an arXiv link, or you put the BibTeX entry and the PDF in `papers/_drop/`.

If you run it again on an initialized project, it refuses. To change one answer, edit the file.

## 3. The names that you inherit

- **PI**: the human researcher who decides. If you are a solo researcher, you are the PI. The
  word exists so that the question "who decides this?" always has an answer in the text.
- **topic**: one model, system, regime or chapter of the work. It is the unit that gets its own
  `symbolic/<topic>/`, `derivation/<topic>/` and `validation/<topic>/`. Topics are usually a
  progression of increasing difficulty: the simplest case first, then the case that the paper is
  about, then the extension.
- **stage**: one derivation step. It has one script, one write-up and one number. Never two.
- **record**: a machine-readable JSON result with its full provenance.
- **REPRODUCTION and EXTENSION**: see `docs/WORKFLOW.md` §5. The project marks them where it uses
  them. It does not mark them by directory.

## 4. Deliberate design choices that you can undo by accident

**One canonical statement for each fact.** `CLAUDE.md` §3 states the five-item discrepancy form,
and no other file states it. `docs/WORKFLOW.md` §5 states the REPRODUCTION and EXTENSION
convention, and no other file states it. `.claude/models.md` states the model routing, and no
other file states it. If you restate a rule in a second file, the two copies drift apart. The
project that this template came from had to write a staleness checker for the drift that its own
restatements created. If you need to invoke a rule, link to it.

**`docs/STATUS.md` holds the current state only.** It loads into every session. Therefore it
stays under about 100 lines. The history goes to `docs/status_history.md`, which does *not* load
automatically. In the source project, STATUS reached 504 lines of history before this split.

**Tool ownership is a PI decision.** `docs/toolchain.md` owns the rule, the default profile and
the registries. The registry exists to prevent one defect: two tools that each hold a slightly
different version of the same equation. Nothing states which one is the record, and the checks
of neither tool can detect it.

**Reproduction and extension are equal parts, in one tree.** The template does not treat the
extension as a follow-on. `docs/reproduction_and_extension.md` tracks both parts and the new-work
deliverables. `docs/STATUS.md` has a section for each part. The project holds the two parts to
different standards of evidence where it uses them. It does not separate them by directory
(`docs/WORKFLOW.md` §5). If you fill in only the reproduction table, the project quietly becomes
a reproduction project.

**Derivation scripts are append-only.** A hook blocks `Write` to an existing stage script. A new
stage is a new numbered file. Supersede by adding. Never supersede by overwriting. The write-ups
cite these scripts by name. If you rewrite a script silently, you invalidate each citation.

**Git ignores the PDFs in `papers/` by default.** The project commits the registry
(`papers/sources.yaml`) with DOIs and arXiv IDs. It does not commit the PDFs. You decide whether
to redistribute the PDF of a publisher. The template does not decide this.
`make fetch-source ID=<arxiv-id>` retrieves the files locally.

**There is no example project.** If a template has a worked example, people copy it into real
projects. Then they cite it as real evidence. The cost of having no example is this: the pipeline
is not exercised until your first stage. `make check` and the hook self-tests exist for this
reason.

## 4a. Continuity across sessions, and what each piece is for

There are four mechanisms. They are distinct on purpose. If you mix them, a project ends up with
one file that is a record, a note and a log at the same time. Then the file is none of them.

| Artifact | Written by | Read by | Committed? |
|---|---|---|---|
| `docs/STATUS.md` | `/session-close` | every session, automatically | yes. It is the authoritative current state. |
| `handoff.md` | `/checkpoint`, `/session-close` | every session, **with its age** | yes. It is prose for the next session, and you can share it. |
| `docs/status_history.md` | `/session-close` | on demand | yes. It is the log. It does not load automatically. |
| session transcript | a `Stop` hook, condensed | the next session, on demand | **no. It is outside the repository entirely.** |

The last row matters most, and people get it wrong most often. A transcript holds half-formed
reasoning and dead ends. Sharing permissions of a repository inherit downward. You cannot
subtract them from a subfolder. A web interface does not hide a folder with a dot prefix
(`docs/failure_modes/anticipated.md` C2). The design depends on this property: *never shared*.

`handoff.md` carries its **age** into the context on purpose. At three days, it is context. At
three months, it describes a project that moved on. To believe it silently is worse than to have
no handoff.

`docs/handoff_guide.md` explains how to write a handoff. It has the four headings, a good
example, a bad example with an annotation for each line, and a checklist. It is a separate file
and not comments inside `handoff.md`. It matters only while someone writes a handoff. Anything
inside `handoff.md` costs context at each session start.

## 5. Keep the harness healthy

```bash
make check         # every session: hooks self-test, references, evidence tags, staleness
make check-env     # when a tool or a local library seems missing
make check-init    # fail while {{PLACEHOLDERS}} remain (passes once initialized)
make libraries     # what is in the PI's local Zotero/Calibre, if anything
```

`make check` includes the **context budget**. `CLAUDE.md`, `docs/STATUS.md` and
`docs/conventions.md` have line limits. If a file exceeds its limit, that is an error. It is not
a warning. Nobody obeys a budget that only warns. The file grows to 500 lines of history. When the
budget fires, move detail into a skill, a rule or a referenced document. Do not compress the
wording.

`/sync-template` pulls harness improvements from upstream without touching scientific content.
It diffs only the reusable layer. It applies only what the PI approves.

In a Claude Code session, `/doctor prompt-audit` reviews `CLAUDE.md`, the rules, the skills and
the agents. It finds instructions that contradict each other and files that no longer exist.
Run it after each significant restructuring.

If Claude seems to ignore an instruction, check `/context` to confirm that the file loaded. Then
decide where the instruction belongs. Use a rule if it is path-scoped and loads when Claude
touches the path. Use a skill if it loads on a trigger. Use a hook if it must run whatever the
model decides. Prose in `CLAUDE.md` is the weakest of the three. A hook is the strongest.
`docs/GUIDE.md` §6 lists which guarantees of this template the system enforces, and which depend
on the compliance of the model.

## 6. Upgrade the harness later

The reusable layer is in `.claude/`, `scripts/`, `Makefile`, and the process documents in `docs/`
(`GUIDE`, `WORKFLOW`, `failure_modes`, `validation_protocol`, `source_audit_template`). None of
it imports project content. To pull improvements from a newer version of this template into a
running project, diff only those paths. This does not touch your scientific content or your
`STATUS`, `conventions` and `decision_log`.
