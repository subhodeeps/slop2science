# slop2science

> *"Staying afloat in this torrent of slop requires scrutinising everything the model
> produces."*
> — [How to Train Your Slop Cannon](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)

A Claude Code template for reproducing a scientific paper and then building new work on top
of it. It holds the reusable parts: instructions, subagents, skills, hooks, a validation
protocol and an audit workflow. No paper-specific content.

Reproducing the paper shows the setup is sound. The new work is the point, and it ends in a
new set of calculations that may go into a future publication. The two are tracked side by
side and judged differently: a reproduction is judged against the source, an extension cannot
be, because the source does not contain the answer.

You decide the question, the conventions, the scope, what gets claimed, which language does
what. Claude advises, implements, may disagree once with reasons, and asks when something has
not been decided. If you say no, that is settled, and the charter says so.

## Features

- Source audit before any code. The paper is reconstructed first, and every inconsistency is
  recorded in a five-point form instead of being quietly fixed.
- Reproduction and extension tracked side by side, judged against different things. The
  extension ends in a new set of calculations that may go into a future publication.
- Mathematica, Python and Julia each own named topics, written in an ownership registry. Code
  is generated from the algebra, never retyped.
- Independent verification: the verifier sees only the artifact, is read-only, and results
  carry records of how they were produced.
- Continuity between sessions: current status, a handoff note, captured prompts, and guards
  on sources and accepted results.

`docs/failure_modes.md` has the failure each of these answers, and what it cost.

## Quick start

```bash
git clone <this repo> my-paper-project
cd my-paper-project && rm -rf .git && git init
$EDITOR papers/sources.yaml        # register the paper
```

Then, in Claude Code, run `/init-paper`. It asks for the project name, the paper, what you are
trying to establish, what counts as the new work, and which tool owns what. It fills in the
placeholders, writes the ownership registry, seeds the first prompt record, and says what is
left. It refuses to run twice. Then run `/source-audit`. No code before the audit.

```bash
make check       # repository checks; needs no scientific toolchain
make check-env   # what is installed here
```

## Tools and libraries

I use Mathematica, Python and Julia, so the template comes configured for all three: an
environment for each, one runner (`scripts/run`) for any of them, and separate test and
codegen paths. Any of them can own any topic. If you don't choose, the default profile applies:
Mathematica for algebra, as plain `.wls` scripts; Julia for numerics; Python for plotting and
ML. `/init-paper` lets you change it.

Whatever the choice, it gets written down. Three capable tools make it easy to derive
something twice and end up with two versions of one equation, both passing their own checks.
The registry in `docs/toolchain.md` records who owns what, and Claude does not move work
between languages on its own.

For sources, it prefers the arXiv LaTeX source to the PDF. The `.tex` is what the authors
wrote; PDF text extraction is a reconstruction, and the tarball also has the figures and
sometimes the data. If you keep a Zotero or Calibre library, it can search it and import one
item, with full metadata and BibTeX, into `papers/imported/`:

```bash
scripts/py scripts/library.py search --author Chandrasekhar
scripts/py scripts/library.py import --zotero 101 --dry-run
```

Read-only, search only, no browse mode: a large library would eat a session's context. Imports
are marked unverified until someone checks them against the paper, and your notes and
annotations are never read.

## Layout

    CLAUDE.md          the charter, loaded every session   docs/         state, protocol, records
    handoff.md         note to the next session            papers/       sources (read-only)
    .claude/           agents, skills, rules, hooks        symbolic/     stage scripts, generated code
    derivation/        the write-ups                       src/          production code, per language
    validation/        runs, records, benchmarks           tests/        unit and regression
    reports/           the paper                           notes/        probes, open leads
    code/              other people's code, filed          scripts/      wrappers and checks

`docs/GUIDE.md` for how the pieces fit; `docs/WORKFLOW.md` for how to do a piece of work.

## How to use it

You bring the paper. There is no example project, so there is nothing to copy by accident and
nothing that can be mistaken for a result of your own. `/init-paper` is where the choices get
made; anything you leave open stays open, and Claude asks again when the work reaches it.
After that the loop is: audit the source, derive a stage, check it, write it up, commit, close
the session.

## Credit

> *"This is tedious and total overkill for most use cases."*
> — How to Train Your Slop Cannon

I started this after reading [How to Train Your Slop Cannon](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon).
The first version was the setup from a project that reproduced a published paper, with the
paper-specific parts taken out. Then I used Claude to add ideas from the slop cannon paper:
the prover/verifier split, Lamport-structured derivations, the ladder of rigour, and the model
failure modes that open `docs/failure_modes.md`.

Other repositories contributed pieces:

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
