# slop2science

> *"Staying afloat in this torrent of slop requires scrutinising everything the model
> produces."*
> — [How to Train Your Slop Cannon](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)

A Claude Code template for reproducing a scientific paper and then building new work on top
of it. It holds the reusable parts: instructions, subagents, skills, hooks, prompt records,
validation protocol and audit workflow. No paper-specific content.

Reproducing the source shows that the machinery is sound. The new work built
on it is the point, and it should end in a paper of your own. Both are tracked side by side
and judged differently: a reproduction is judged against the source, an extension cannot be,
because the source does not contain the answer.

You decide the question, the conventions, the scope, what gets claimed, which language
implements what, and how the tools exchange results. Claude advises, asks when something has
not been decided, and implements. It may disagree once, with reasons. If you say no, that is
settled. This is in the charter, not left to etiquette.

This kind of work fails in repeatable ways. The assistant "fixes" an inconsistency in the
source instead of recording it. Something gets called verified that was never checked. The
reasoning is lost between sessions. An expression is hand-copied between tools and picks up a
sign error. A number appears that nobody can trace to a script. An agent that cannot make a
test pass deletes the test. You mention a suspicion and it finds evidence for it.

Every mechanism below answers one of those. The full list, with what each one cost, is
`docs/failure_modes.md`.

## Features

| Mechanism | Failure |
|---|---|
| `CLAUDE.md` + `docs/STATUS.md` + `docs/conventions.md` | losing the thread between sessions |
| Prompts captured automatically, curated records kept apart | a result whose prompt nobody can find |
| Five-point discrepancy form | silently correcting the source |
| `Kind:` and `Judged against:` markers | reproduction evidence read as extension evidence |
| Evidence tags, and checkers that resolve them | a broken citation chain nobody noticed |
| Ladder of rigour, prose to machine-checked | "verified" meaning six different things |
| Prover/verifier split, verifier sees only the artifact | an auditor inheriting the author's blind spots |
| `PreToolUse` guards | edits to sources, generated code, accepted results |
| Read-only `verification` agent, enforced by a hook | the auditor fixing what it audits |
| Tool-ownership registry, codegen not transcription | two tools holding different versions of one equation |
| Result records with provenance, acceptance protocol | numbers nobody can reproduce |
| `docs/reproduction_and_extension.md` | not knowing how far along you are |
| Authority and tool choices written into the charter | Claude quietly deciding something that was yours |
| `make check` and CI | checks that run only when someone remembers |
| `handoff.md`, read in at session start with its age | starting cold; trusting a stale note |
| Snapshot before compaction | losing a judgement that was never written down |
| Transcripts kept outside the repository | half-formed reasoning shipping with the repo |
| Git guard on every subagent | an agent rewriting history it cannot see |
| arXiv LaTeX source preferred over the PDF | equations mis-transcribed from a PDF; figures and data lost |
| Zotero and Calibre searched, never browsed | a session spent enumerating a large library |

## Quick start

```bash
git clone <this repo> my-paper-project
cd my-paper-project && rm -rf .git && git init
$EDITOR papers/sources.yaml        # register the paper; committing the PDF is your call
```

Then, in Claude Code, run `/init-paper`. It asks for the project name, the paper, what you
are trying to establish, what counts as the new work, and which tool owns what. Then it fills
in the placeholders, writes the ownership registry, seeds the first prompt record, and says
what is left. It refuses to run twice.

```bash
make check       # repository checks; needs no scientific toolchain
make check-env   # what is installed here
```

Then run `/source-audit`. No code before the audit.

## Layout

    CLAUDE.md          the charter, loaded every session   docs/         state, protocol, records
    handoff.md         note to the next session            papers/       sources (read-only)
    .claude/           agents, skills, rules, hooks        symbolic/     stage scripts, generated code
    derivation/        the write-ups                       src/          production code, per language
    validation/        runs, records, benchmarks           tests/        unit and regression
    reports/           the paper                           notes/        probes, open leads
    code/              other people's code, filed          scripts/      wrappers and checks

`docs/GUIDE.md` for how the pieces fit; `docs/WORKFLOW.md` for how to do a piece of work.

## Tools

Mathematica, Python and Julia. The template comes configured for all three: an environment
for each, one runner that handles any of them, and separate test and codegen paths per
language. Any of them can own any topic.

If you don't choose, the default profile applies: Mathematica for algebra, as plain `.wls`
scripts; Julia for numerics; Python for plotting, ML and anything else with a better Python
ecosystem. `/init-paper` shows you that and lets you change it. Say "ask me each time" and it
will.

What it does require is that the choice is written down. Three capable tools make it easy to
derive something twice and end up with two versions of one equation, both passing their own
checks. The registry in `docs/toolchain.md` records the owner of each topic and each solver,
and Claude does not move work between languages on its own.

Everything runs through `scripts/run`, whatever the language. A missing tool is a loud skip,
not a failure.

## Libraries

Zotero and Calibre, if you have them. Useful for stuff you already have.

```bash
make libraries
scripts/py scripts/library.py search --author Chandrasekhar
scripts/py scripts/library.py import --zotero 101 --dry-run
```

Read-only, and search only. There is no browse mode: a large library would eat a session's
context, and it is not this project's bibliography.

`show` prints everything a library knows about one item. `import` takes one item: it copies
the file into `papers/imported/` if it is small (25 MB by default), saves the full metadata,
and adds entries to `papers/sources.yaml` and `papers/refs.bib`, marked unverified until
someone checks them against the paper. Your Zotero notes and annotations are never read.

For arXiv papers it fetches the LaTeX source as well as the PDF. The `.tex` is what the
authors wrote; PDF text extraction is a reconstruction. The tarball also has the figures, and
sometimes the data behind a table.

## How to use it

You bring the paper. There is no example project and no sample derivation, so there is
nothing to copy by accident and nothing that can later be mistaken for a result of your own.

`/init-paper` is where the choices get made. It asks what you are reproducing, what the new
work is, which tool owns what, and which conventions to pin, and writes your answers into the
charter and the registry. Anything you leave open stays open, and it asks again when the work
reaches it.

After that the process runs itself: audit the source, derive a stage, check it, write it up,
commit, close the session. What counts as a result, and what gets claimed, stays with you.

## Credit

The authors of [How to Train Your Slop Cannon](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)
got me to set this up in the first place, and the name comes from their paper. I used Claude
to implement some of their ideas here: the prover/verifier split, Lamport-structured
derivations, the ladder of rigour, and the three model failure modes that open
`docs/failure_modes.md`.

The rest of the engineering came out of a real paper-reproduction project.

Also taken from:

- [benning-lab/agentic-starter](https://github.com/benning-lab/agentic-starter) — the handoff
  with its age, transcripts outside the repo, source formats over PDFs.
- [mitevpi/claude-project-scaffold](https://github.com/mitevpi/claude-project-scaffold) — the
  subagent git guard, the parallel-work partition rules, checking the instruction file's size.
- [josipjelic/orchestrated-project-template](https://github.com/josipjelic/orchestrated-project-template)
  — `/checkpoint` and `/sync-template`.
- [scotthavird/claude-code-template](https://github.com/scotthavird/claude-code-template) —
  saving state before compaction.
- [shinpr/ai-coding-project-boilerplate](https://github.com/shinpr/ai-coding-project-boilerplate)
  — framing the instruction file as what Claude can decide and when it should ask.
- Lorena Barba, *Reproducibility in the Age of Agentic AI*
  ([barbagroup/agentic-reproducibility](https://github.com/barbagroup/agentic-reproducibility))
  — reproducible-research practice as context engineering, and the caveat this is built
  around: the researcher stays responsible for the judgements these artifacts encode.
