# slop2science

*From plausible output to established result.*

A **Claude Code template for reproducing a scientific paper and then building new work on
top of it.** It is the reusable engineering harness — instructions, subagents, skills, hooks,
prompt records, validation protocol and audit workflow — with no paper-specific content in it.

**Two halves of equal standing.** Reproducing the source establishes that the machinery is
sound; the extension built on that foundation is the point, and it ends in a paper of the
project's own. The template tracks both side by side and holds them to different standards of
evidence, because the source can validate a reproduction and cannot validate an extension.

**The PI is the final authority.** The researcher decides the question, the conventions, the
scope, what is claimed — and, specifically, *what is implemented in which language and how the
tools interoperate*. Claude advises, asks when a decision has not been made, and implements.
That is written into the charter rather than left to etiquette.

It exists because this kind of work with an AI assistant fails in specific, repeatable ways:
the assistant silently "fixes" the source, calls something verified that was never checked,
loses the reasoning between sessions, hand-transcribes an expression and introduces a sign
error, quietly picks a language or a default nobody chose, or produces a result nobody can
trace back to a script. Every mechanism here answers one of those failures. The ones learned
the hard way are recorded in `docs/failure_modes.md`.

## What you get

| Mechanism | What it prevents |
|---|---|
| Three-tier context (`CLAUDE.md` charter + `docs/STATUS.md` state + `docs/conventions.md` register) | losing the thread between sessions, and burning context on history |
| Automatic prompt capture + curated prompt records | a result whose originating prompt nobody can find |
| The **five-point discrepancy form** (`CLAUDE.md` §3) | silently "correcting" the source paper |
| `Kind:` / `Judged against:` markers at the point of use | reproduction evidence being mistaken for extension evidence |
| Verified-vs-not vocabulary + `[E: …]` evidence tags + machine checkers | claims whose evidence chain has quietly broken |
| `PreToolUse` guard hooks | edits to source PDFs, machine-generated code, or accepted results |
| A `verification` subagent made read-only **by a hook** | the auditor fixing what it is supposed to be auditing |
| Declared tool ownership + codegen-not-transcription | two divergent records of the same equation |
| Machine-readable result records + validation protocol | numbers nobody can reproduce |
| `docs/reproduction_and_extension.md` | "how much of the paper have we reproduced, and what have we actually added?" being unanswerable |
| PI authority written into the charter, including language and interoperation choices | Claude quietly deciding something that was the researcher's to decide |
| Two-tier `Makefile` and CI | checks that only run when someone remembers |
| `handoff.md` injected at session start **with its age** | a new session starting cold, or trusting a three-month-old note |
| A snapshot before every compaction | losing a judgement mid-session that was never written down |
| Condensed transcripts kept **outside** the repository | half-formed reasoning travelling with a shared repo |
| A git guard on every subagent | an agent with a fresh context rewriting history it cannot see |
| arXiv **LaTeX source** preferred over the PDF | equations mis-transcribed from a PDF text layer; figures and data lost |
| Local Zotero/Calibre searched, never browsed | a session spending its context enumerating a 10,000-item library |

## Quick start

```bash
# 1. Use this template on GitHub ("Use this template" -> "Create a new repository"),
#    or: git clone <this repo> my-paper-project && rm -rf my-paper-project/.git && git init
cd my-paper-project

# 2. Put the paper where the project can see it
#    (registry entry is required; committing the PDF is optional and off by default)
$EDITOR papers/sources.yaml

# 3. Start Claude Code and initialize
claude
> /init-paper
```

`/init-paper` interviews you for the project name, the source paper, the scientific
objective, and which tools own which part of the work; then it fills every `{{PLACEHOLDER}}`,
writes the ownership registry, seeds the first prompt record, and prints what is left to do.

```bash
# 4. Confirm the harness works before any physics
make check          # needs no scientific toolchain at all
make check-env      # reports which of your tools are present
```

Then run your first real session: the **source audit** (`/source-audit`). No code before the
audit — that ordering is the point of the template.

## Layout

    CLAUDE.md          the charter, loaded every session      docs/            state, protocol, records
    .claude/           agents, skills, rules, hooks           papers/          sources (read-only)
    derivation/        human-readable derivations             symbolic/        stage scripts + generated code
    src/               production code, per language          tests/           unit/regression
    validation/        validation runs, records, benchmarks   reports/         generated write-ups
    code/              external and PI-supplied code          notes/           probes, open leads
    scripts/           wrappers and repository checks         data/ figures/ logs/

Full account: `docs/GUIDE.md` §2. How to do a piece of work: `docs/WORKFLOW.md`.

## What it leaves to you

This is process, not content. It supplies the part that is the same in every project of this
kind — the discipline, the provenance, and the machinery that ties a claim to the command
that established it — and it deliberately decides nothing that is yours to decide:

- **The science.** It ships with no example project and no sample derivation. You start from
  your paper, not from a specimen of someone else's, so there is nothing to copy by accident
  and nothing that can later be mistaken for evidence of your own.
- **The tools.** Mathematica, Python and Julia are equal here. Which one owns which piece of
  work, and how results pass between them, is your call — `/init-paper` asks, records each
  answer as a decision, and a registry keeps the standing answer where anyone can read it.
- **The claims.** Claude derives, checks, records and drafts. What counts as a result, what
  goes in a paper, and what is claimed for it stay with you.

## Provenance and prior art

The starting point was [Open-Science-Ledger/how-to-train-your-slop-cannon](https://github.com/Open-Science-Ledger/how-to-train-your-slop-cannon)
— the guide that makes the case for doing research this way at all, and the reason this
repository exists. Its framing is the one this template is built on: a model produces
plausible output at scale, so *"staying afloat in this torrent of slop requires scrutinising
everything the model produces."* Hence the name. Several of its ideas are implemented here
directly — the adversarial prover/verifier split, Lamport-structured derivations, the ladder
of rigour, and the three model failure modes in `docs/failure_modes.md` Part 0.

The engineering pattern itself was extracted from a working physics paper-reproduction
project. Every entry in `docs/failure_modes.md` Part 1 is something that actually went wrong
there. The science is gone; the scar tissue is the valuable part.

Other mechanisms were taken or adapted from other people's work, and are better for it:

- [benning-lab/agentic-starter](https://github.com/benning-lab/agentic-starter) — the
  handoff-with-age idea, the argument for keeping transcripts outside the project folder, and
  the "prefer source formats; PDF extraction is a reconstruction" rule.
- [mitevpi/claude-project-scaffold](https://github.com/mitevpi/claude-project-scaffold) — the
  subagent git guard, the partition rules behind `parallel-safety`, and checking the
  instruction file's own size budget.
- [josipjelic/orchestrated-project-template](https://github.com/josipjelic/orchestrated-project-template)
  — `/checkpoint` and `/sync-template`.
- [scotthavird/claude-code-template](https://github.com/scotthavird/claude-code-template) —
  the `PreCompact` checkpoint.
- [shinpr/ai-coding-project-boilerplate](https://github.com/shinpr/ai-coding-project-boilerplate)
  — independently frames its instruction file as "what Claude can decide and when it should
  ask you", which is this template's §1 reached from the other direction.
- Barba, *Reproducibility in the Age of Agentic AI*
  ([barbagroup/agentic-reproducibility](https://github.com/barbagroup/agentic-reproducibility))
  — the argument that reproducible-research practice *is* context engineering for coding
  agents, with the caveat this template is built around: researchers remain responsible for
  verifying these artifacts and the scientific judgements they encode.
