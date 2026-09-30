# Template guide — what to change, and what to leave alone

Read this once, before `/init-paper`. It says which parts of this repository are meant to be
rewritten for your paper, which are meant to survive unchanged, and why.

## 1. The three layers

| Layer | Files | Change it? |
|---|---|---|
| **Charter and discipline** | `CLAUDE.md` §1, §3–§4, §6, §8–§11; `.claude/rules/`; `docs/WORKFLOW.md`; `docs/failure_modes.md`; the hooks | **No.** These encode failure modes, not preferences — §1 in particular (PI authority, and asking rather than defaulting) is the one the rest rests on. Change them only after your project hits a failure they don't cover — and then log it in `docs/decision_log.md`. |
| **Project parameters** | `CLAUDE.md` `{{PLACEHOLDERS}}`; `docs/conventions.md`; `docs/toolchain.md` ownership registry; `papers/sources.yaml`; agent/skill trigger phrases | **Yes, once**, via `/init-paper`, then as the project evolves. |
| **Scientific content** | `derivation/`, `symbolic/`, `src/`, `tests/`, `validation/`, `reports/`, `docs/reproduction_and_extension.md`, `docs/STATUS.md` | **Yes, continuously.** This is the work. Ships empty. |

If you find yourself editing layer 1 in the first week, that is a signal the template is
wrong for your problem — not that the rule is inconvenient. Say which rule and why in
`docs/decision_log.md` so the next project inherits the reasoning.

## 2. What `/init-paper` does

It interviews you, then writes:

- `CLAUDE.md` — project name, objective, pipeline, primary source, the three tool names.
- `docs/conventions.md` — the first rows of the conventions register (units, notation,
  sign/orientation conventions, labelling), each tagged SOURCE / ADOPTED / OPEN / DERIVED.
- `docs/toolchain.md` — the **ownership registry**: which tool is the record for which topic
  and which solver.
- `docs/STATUS.md` — phase 0, the first immediate task (the source audit), no blockers.
- `docs/prompts/A1_source_audit.md` — the first curated prompt record, ready to run.
- Agent and skill `description` / `when_to_use` lines, so triggering matches your vocabulary.
- `src/julia/Project.toml` and `src/python/pyproject.toml` package names.

It then deletes its own placeholder scaffolding and prints a checklist of what only you can
do (fetch the paper, decide open conventions, install tools).

Re-running it on an initialized project is refused; to change one answer, edit the file.

## 3. The naming you inherit

- **PI** — the human researcher who decides. If you are a solo researcher, you are the PI;
  the word exists so that "who decides this?" always has an answer in the text.
- **topic** — one model, system, regime or chapter of the work: the unit that gets its own
  `symbolic/<topic>/`, `derivation/<topic>/`, `validation/<topic>/`. Usually a progression of
  increasing difficulty — the simplest case first, then the one the paper is actually about,
  then the extension.
- **stage** — one derivation step: one script, one write-up, one number. Never two.
- **record** — a machine-readable JSON result with its full provenance.
- **REPRODUCTION vs EXTENSION** — see `docs/WORKFLOW.md` §5. Marked at the point of use, not
  by directory.

## 4. Deliberate design choices you might otherwise undo

**One canonical statement per fact.** The five-point discrepancy form is stated in
`CLAUDE.md` §3 and nowhere else. The REPRODUCTION/EXTENSION convention is in
`docs/WORKFLOW.md` §5 and nowhere else. Model routing is in `.claude/models.md` and nowhere
else. Restating a rule in a second file is how the two copies drift apart; the project this
came from had to write a staleness checker to police drift it had created by restating.
If you need to invoke a rule, link to it.

**`docs/STATUS.md` holds current state only.** It loads into every session, so it stays
under ~100 lines. History goes to `docs/status_history.md`, which is *not* auto-loaded. In
the source project STATUS reached 504 lines of history before this split.

**Tool ownership is a PI decision, declared per topic, not per language.** All three tools are
co-equal, and Claude never picks one: not for new work, not to move existing work, not to add
a hand-off between tools. The defect the registry prevents is not "using the wrong tool" — it
is two tools each holding a slightly different version of the same equation, with nothing
saying which is the record, and neither tool's own checks able to detect it. `docs/toolchain.md`
carries both an ownership registry and an interoperation registry for that reason.

**Reproduction and extension are equal halves, in one tree.** The template does not treat the
extension as a follow-on: `docs/reproduction_and_extension.md` tracks both plus the
new-work deliverables, `docs/STATUS.md` has a section for each, and the two are held to
different standards of evidence at the point of use rather than separated by directory
(`docs/WORKFLOW.md` §5). If you only ever fill in the reproduction table, the project will
have quietly become a reproduction project.

**Derivation scripts are append-only.** A hook blocks `Write` to an existing stage script; a
new stage is a new numbered file. Supersede by adding, never by overwriting — the write-ups
cite these scripts by name, and rewriting one silently invalidates every citation.

**`papers/` PDFs are gitignored by default.** The registry (`papers/sources.yaml`) with DOIs
and arXiv IDs is committed; the PDFs are not, because redistributing a publisher's PDF is
your call, not the template's. `make fetch-source ID=<arxiv-id>` retrieves them locally.

**No example project.** A worked example in a template gets copied into real projects and
then cited as if it were real evidence. The cost is that the pipeline is unexercised until
your first stage — which is what `make check` and the hook self-tests are for.

## 4a. Continuity across sessions, and what each piece is for

Four mechanisms, deliberately distinct — conflating them is how a project ends up with one
file that is simultaneously a record, a note and a log, and therefore none of them:

| Artifact | Written by | Read by | Committed? |
|---|---|---|---|
| `docs/STATUS.md` | `/session-close` | every session, automatically | yes — the authoritative current state |
| `handoff.md` | `/checkpoint`, `/session-close` | every session, **with its age** | yes — prose for the next session, shareable |
| `docs/status_history.md` | `/session-close` | on demand | yes — the log, not auto-loaded |
| session transcript | a `Stop` hook, condensed | the next session, on demand | **no — outside the repository entirely** |

The last row matters most and is the one people get wrong. A transcript holds half-formed
reasoning and dead ends; repository sharing permissions inherit downward and cannot be
subtracted from a subfolder, and a dot-prefixed folder is not hidden in a web UI
(`docs/failure_modes.md` C2). The property relied on is *never shared*.

`handoff.md` carries its **age** into context on purpose: at three days old it is context, at
three months it describes a project that has moved on, and silently believing it is worse than
having none.

How to write one — the four headings, a worked good example, a bad one annotated line by
line, and a checklist — is `docs/handoff_guide.md`. It is a separate file rather than comments
inside `handoff.md` because it only matters while a handoff is being written, and anything
left inside that file is paid for in context at every session start.

## 5. Keeping the harness healthy

```bash
make check         # every session: hooks self-test, references, evidence tags, staleness
make check-env     # when a tool or a local library seems missing
make check-init    # fail while {{PLACEHOLDERS}} remain (passes once initialized)
make libraries     # what is in the PI's local Zotero/Calibre, if anything
```

`make check` includes the **context budget**: `CLAUDE.md`, `docs/STATUS.md` and
`docs/conventions.md` have line limits and exceeding one is an error, not a warning. A budget
that only warns is a budget ignored until the file is 500 lines of history. When it fires,
move detail into a skill, a rule or a referenced doc — do not compress the wording.

`/sync-template` pulls harness improvements from upstream without touching any scientific
content; it diffs only the reusable layer and applies nothing unapproved.

In a Claude Code session, `/doctor prompt-audit` reviews `CLAUDE.md`, the rules, skills and
agents for instructions that contradict each other or cite files that no longer exist. Run it
after any significant restructuring.

If Claude seems not to follow an instruction: check `/context` to confirm the file loaded,
then ask whether the instruction belongs in a rule (path-scoped, loads on touch), a skill
(loads on trigger), or a hook (runs regardless of what the model decides). Prose in
`CLAUDE.md` is the weakest of the three; a hook is the strongest. `docs/GUIDE.md` §6 lists
which of this template's guarantees are enforced and which depend on the model complying.

## 6. Upgrading the harness later

The reusable layer is confined to `.claude/`, `scripts/`, `Makefile`, and the process docs in
`docs/` (`GUIDE`, `WORKFLOW`, `failure_modes`, `validation_protocol`,
`source_audit_template`). None of it imports project content. To pull improvements from a
newer version of this template into a running project, diff those paths only — your
scientific content and your `STATUS`/`conventions`/`decision_log` are untouched by it.
