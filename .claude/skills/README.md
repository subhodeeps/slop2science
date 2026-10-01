# Project skills

Each skill is a folder with `SKILL.md`. A skill can also have `reference/` files and
`templates/`. Claude loads a `reference/` file only when the skill needs it. Copy a template
into the repository. Never edit a template in place.

| Skill | Invoked by | Purpose |
|---|---|---|
| `init-paper` | **you only**: `/init-paper` | One-time initialization of this template for a new paper. The skill deletes itself when it is done. |
| `source-audit` | Claude (auto) or `/source-audit` | Reconstruct what the source states, what its equations imply and where it is inconsistent. Do this before any code. |
| `derivation-workflow` | Claude (auto) | The cycle derive, check, write up, commit, export. It has the print-before-assert discipline and the checklist for each stage. |
| `solver-workflow` | Claude (auto) | Build and audit a production solver from generated coefficients, in the order that makes each step cheap. |
| `toolchain` | Claude (auto) or `/toolchain` | Run Mathematica, Julia and Python through the common wrapper. It covers environments, precision tiers and the codegen hand-off. |
| `literature-audit` | Claude (auto) | Audit primary sources and conventions. It covers benchmark provenance and how to read equations from a source correctly. |
| `verification` | Claude (auto) | Checklists for independent audit, and the failure taxonomy. The read-only `verification` agent uses it. |
| `external-code` | Claude (auto) | All code that this project did not write: provenance, licence, attribution and intake from the drop folder of the PI. |
| `report-writing` | `paper-writer` (auto) | Write a report as a paper that a researcher can follow by hand. Put provenance in an appendix, not after each equation. |
| `checkpoint` | **you only**: `/checkpoint` | Safe save during a session: account for the changes, run the checks, refresh the handoff and propose a commit of coherent work. |
| `session-close` | **you only**: `/session-close` | Account for each changed file, run the checks, update the state, write the handoff and propose a commit. |
| `sync-template` | **you only**: `/sync-template` | Pull harness improvements from the upstream template. Do not touch scientific content. |
| `plotting` | Claude (auto), and preloaded by `implementation` | Make each matplotlib figure in `amore`, the plot style: LaTeX labels, muted palettes, shaded bands, insets, contour maps. Look at the rendered figure before you call it done. `make check-plots` enforces the style in code. |
| `parallel-safety` | Claude (auto) | What is safe to run in parallel and what is not. The partition rules to apply before you dispatch concurrent agents. |

## Conventions

- Keep a skill under about 100 lines. Put detail that you need only sometimes in `reference/`.
  It costs nothing until someone reads it.
- Put trigger phrases in `when_to_use`. After `/init-paper`, these phrases carry the
  vocabulary of **this project**. A skill that never starts usually has generic trigger
  phrases.
- Each skill inherits the language rule. It runs inside a session or an agent. Both must write in
  ASD-STE100 (`.claude/rules/communication.md`). Write each new skill in STE.
- Put shared executable code in `symbolic/common/` and `src/`. Never put it inside a skill.
  Then scripts can load it directly.
- A skill describes *how to do a category of work*. A rule (`.claude/rules/`) states a
  constraint on a path. A hook enforces a requirement whatever the model decides. If people
  keep missing an instruction, it is in the wrong one of these three (`docs/GUIDE.md` §6).
