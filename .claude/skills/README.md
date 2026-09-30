# Project skills

Each skill is a folder with `SKILL.md`, plus optional `reference/` files (loaded only when
the skill actually needs them) and `templates/` (copied into the repository, never edited in
place).

| Skill | Invoked by | Purpose |
|---|---|---|
| `init-paper` | **you only**: `/init-paper` | One-time initialization of this template for a new paper. Deletes itself when done. |
| `source-audit` | Claude (auto) or `/source-audit` | Reconstruct what the source states, what its equations imply, and where it is inconsistent — before any code. |
| `derivation-workflow` | Claude (auto) | The derive → check → write up → commit → export cycle, with the print-before-assert discipline and the per-stage checklist. |
| `solver-workflow` | Claude (auto) | Building and auditing a production solver from generated coefficients, in the order that makes each step cheap. |
| `toolchain` | Claude (auto) or `/toolchain` | Running Mathematica, Julia and Python through the common wrapper; environments, precision tiers, codegen hand-off. |
| `literature-audit` | Claude (auto) | Primary-source and convention auditing; benchmark provenance; reading equations from a PDF correctly. |
| `verification` | Claude (auto) | Independent audit checklists and the failure taxonomy. Used by the read-only `verification` agent. |
| `external-code` | Claude (auto) | Every piece of code this project did not write: provenance, licence, attribution, and PI drop-folder intake. |
| `report-writing` | `paper-writer` (auto) | Writing a report as a paper a researcher can follow by hand; provenance in an appendix, not after every equation. |
| `session-close` | **you only**: `/session-close` | Account for every changed file, run the checks, update state, propose a commit. |

## Conventions

- A skill stays under about 100 lines. Detail that is only sometimes needed goes in
  `reference/`, which costs nothing until it is read.
- Trigger phrases live in `when_to_use`. After `/init-paper`, these carry **this project's**
  vocabulary — a skill that never fires is usually a skill whose trigger phrases were left
  generic.
- Shared executable code lives in `symbolic/common/` and `src/`, never inside a skill, so
  that scripts can load it directly.
- A skill describes *how to do a category of work*. A rule (`.claude/rules/`) states a
  constraint on a path. A hook enforces something regardless of what the model decides.
  If an instruction keeps being missed, it is in the wrong one of those three
  (`docs/GUIDE.md` §6).
