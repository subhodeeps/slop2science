# slop2science

> *"Staying afloat in this torrent of slop requires scrutinising everything the model
> produces."*
> — Loader, Oppenheim & Osborne, [How to Train Your Slop Cannon](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)

This is a Claude Code template. Use it to reproduce a scientific paper and then build new work
on that paper. It contains the reusable parts: instructions, subagents, skills, hooks, a
validation protocol and an audit workflow. It contains no content from any one paper.

The reproduction shows that the setup is sound. The new work is the goal. The new work ends in
a set of new calculations. You can include these calculations in a future publication.

The project tracks the two parts side by side and judges them against different things. It
judges a reproduction against the source. It cannot judge an extension against the source,
because the source does not contain the answer.

You decide the question, the conventions, the scope, what you claim and which language does
what. Claude advises and implements. Claude can disagree one time and gives its reasons. If you
say no, the decision is final. The charter states this rule.

## Features

- Source audit before any code. The audit reconstructs the paper first. It records each
  inconsistency in a five-point form. It never corrects an inconsistency silently.
- Reproduction and extension, tracked side by side. Each has its own standard of evidence. The
  extension ends in a set of new calculations for a possible publication.
- Mathematica, Python and Julia each own named topics. An ownership registry records the
  owners. The project generates code from the algebra. It never retypes code.
- Independent verification. The verifier sees only the artifact and cannot change files. Each
  result has a record of how the project produced it.
- Continuity between sessions. The project keeps the current status, a handoff note and the
  captured prompts. Guards protect the sources and the accepted results.

`docs/failure_modes.md` lists the failure that each feature prevents and the cost of each fix.

## Quick start

```bash
git clone <this repo> my-paper-project
cd my-paper-project && rm -rf .git && git init
$EDITOR papers/sources.yaml        # register the paper
```

Then run `/init-paper` in Claude Code. It asks you for these items:

- the project name
- the paper
- what you want to establish
- what counts as the new work
- which tool owns which topic
- which libraries you need

It then fills in the placeholders, writes the ownership registry and creates the first prompt
record. It tells you what remains. It refuses to run a second time. Then run `/source-audit`.
Do not write code before the audit.

```bash
make check       # repository checks; needs no scientific toolchain
make check-env   # what is installed here
```

## Tools and libraries

I use Mathematica, Python and Julia. The template has a configuration for all three. It has
one runner (`scripts/run`) for any of them. It has separate test and codegen paths.

Julia and Python each get their own environment if you use them. Julia uses `Project.toml` and
`Manifest.toml`. Python uses a virtual environment that [uv](https://docs.astral.sh/uv/)
creates from `pyproject.toml` and `uv.lock`. A language that you do not use has no environment.

`/init-paper` asks which libraries you need. It starts from a short default list. For Python
the list is numpy, scipy, mpmath, sympy and matplotlib. For Julia it is the linear algebra,
extended-precision and JSON packages. The project installs only the libraries that you choose.

Any of the three tools can own any topic. If you do not choose, the default profile applies.
Mathematica does algebra, in plain `.wls` scripts. Julia does numerics. Python does plotting
and ML. `/init-paper` lets you change this.

The project writes down each choice. With three capable tools, it is easy to derive one
equation twice. The result is two versions of one equation. Each version can pass its own
checks. The registry in `docs/toolchain.md` records the owner of each topic. Claude does not
move work between languages by itself.

For sources, the project prefers the arXiv LaTeX source to the PDF. The `.tex` file is what the
authors wrote. Text extraction from a PDF is a reconstruction. The tarball also contains the
figures and sometimes the data.

If you keep a Zotero or Calibre library, the project can search it. It can import one item,
with full metadata and BibTeX, into `papers/imported/`:

```bash
scripts/py scripts/library.py search --author Chandrasekhar
scripts/py scripts/library.py import --zotero 101 --dry-run
```

The tool is read-only. It only searches. It has no browse mode, because a large library fills
the context of a session. The tool marks each import unverified until a person compares it with
the paper. The tool never reads your notes and annotations.

## Layout

    CLAUDE.md          the charter, loaded every session   docs/         state, protocol, records
    handoff.md         note to the next session            papers/       sources (read-only)
    .claude/           agents, skills, rules, hooks        symbolic/     stage scripts, generated code
    derivation/        the write-ups                       src/          production code, per language
    validation/        runs, records, benchmarks           tests/        unit and regression
    reports/           the paper                           notes/        probes, open leads
    code/              other people's code, filed          scripts/      wrappers and checks

`docs/GUIDE.md` explains how the parts fit together. `docs/WORKFLOW.md` explains how to do a
piece of work.

## How to use it

You bring the paper. The template has no example project. Therefore you cannot copy an example
by accident, and nothing can look like a result of your own.

`/init-paper` is where you make the choices. A choice that you leave open stays open. Claude
asks again when the work reaches it. After that, the loop is:

1. Audit the source.
2. Derive a stage.
3. Check the stage.
4. Write it up.
5. Commit.
6. Close the session.

## Credit

> *"This is tedious and total overkill for most use cases."*
> — Loader, Oppenheim & Osborne, How to Train Your Slop Cannon

I read [How to Train Your Slop Cannon](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)
(Loader, Oppenheim & Osborne) and then started this project. The first version was the setup
from a project that reproduced a published paper. I removed the parts that were specific to
that paper. Then I used Claude to add ideas from the slop cannon paper:

- the prover/verifier split
- Lamport-structured derivations
- the ladder of rigour
- the model failure modes at the start of `docs/failure_modes.md`

Other repositories contributed parts:

- [benning-lab/agentic-starter](https://github.com/benning-lab/agentic-starter) — the handoff
  with its age, transcripts outside the repo, source formats over PDFs.
- [mitevpi/claude-project-scaffold](https://github.com/mitevpi/claude-project-scaffold) — the
  subagent git guard, the rules that divide parallel work, a size check on the instruction
  file.
- [josipjelic/orchestrated-project-template](https://github.com/josipjelic/orchestrated-project-template)
  — `/checkpoint` and `/sync-template`.
- [scotthavird/claude-code-template](https://github.com/scotthavird/claude-code-template) —
  saving state before compaction.
- [shinpr/ai-coding-project-boilerplate](https://github.com/shinpr/ai-coding-project-boilerplate)
  — the instruction file that states what Claude can decide and when Claude must ask.
- Lorena Barba, *Reproducibility in the Age of Agentic AI*
  ([barbagroup/agentic-reproducibility](https://github.com/barbagroup/agentic-reproducibility))
  — reproducible-research practice as context engineering. The template follows her
  caveat: the researcher stays responsible for the judgements that these artifacts contain.
