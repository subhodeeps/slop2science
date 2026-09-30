# claude_code_ai_research_scholar

A **Claude Code template for reproducing and extending a scientific paper.** It is the
reusable engineering harness — instructions, subagents, skills, hooks, prompt records,
validation protocol and audit workflow — with no paper-specific content in it.

It exists because reproducing a paper with an AI assistant fails in specific, repeatable
ways: the assistant silently "fixes" the source, calls something verified that was never
checked, loses the reasoning between sessions, hand-transcribes an expression and introduces
a sign error, or produces a result nobody can trace back to a script. Every mechanism here
answers one of those failures. The ones that were learned the hard way are recorded in
`docs/failure_modes.md`.

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
| `docs/reproduction_matrix.md` | "how much of the paper have we actually reproduced?" being unanswerable |
| Two-tier `Makefile` and CI | checks that only run when someone remembers |

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

## Making this a GitHub template

Creating the repository from the API cannot set the template flag, so do it once by hand:
**Settings → General → check "Template repository"**. After that, "Use this template"
appears on the repository page and every new paper project starts from a clean history.

## What is deliberately *not* here

- No scientific content, no example project, no sample derivation. The template ships empty
  so nothing paper-specific can be copied by accident into the next project.
- No opinion about your physics, your CAS, or your numerics. Tool ownership is declared per
  topic (`docs/toolchain.md`), and `/init-paper` asks.
- No dependency on any tool being installed: the entire `make check` tier runs in CI, on a
  laptop, or in a cloud container with none of Mathematica, Julia or Python's scientific
  stack present.

## Provenance

The pattern is extracted from a working physics paper-reproduction project.
Every rule in `docs/failure_modes.md` corresponds to something that actually went wrong
there. The physics is gone; the scar tissue is the valuable part.
