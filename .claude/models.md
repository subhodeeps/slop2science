# Model routing

This is the single place where model identifiers appear in this repository. The frontmatter of
each agent cites this file. If a vendor retires a model or a tier changes, change this one file.

## The choice that this template makes, and its cost

A bare tier alias (`opus`, `sonnet`, `haiku`, `fable`) resolves to the latest model in that tier
for the account. The alias can change without a commit here. Then the provenance record of a
result can name a model that is not the model that ran. An exact ID makes the record honest. It
also **guarantees** that the setup breaks one day. A retired ID gives an explicit
model-not-found error. It does not give a silent substitution.

This template uses **aliases by default**. A template that breaks on first use is worse than a
template whose provenance is a tier and not a build. If your project reports results that
depend on the model, switch the table to exact IDs. Log the decision. Expect to revisit it. This
is the trade, and the project makes it deliberately.

## Table

| Agent / session | Model | Why |
|---|---|---|
| `derivation` | `opus` | The hard algebra. A wrong answer here is the most expensive and the least visible. |
| `paper-writer` | `opus` | The main deliverable for human readers. It must reconstruct and explain what the source omits. It does not assemble bounded text. It runs rarely. |
| `implementation` | `sonnet` | Tests, generated coefficients and the validation protocol bound the work. |
| `literature` | `sonnet` | Primary sources bound the work. Its typical failures are procedural (a misread PDF, an unverified identifier). They are not gaps in reasoning. |
| `verification` | `sonnet` | The work follows a checklist with a fixed failure taxonomy. Use `opus` for an audit that must derive again and not only check again. |
| `status-reporter` | `sonnet` | The work summarises authoritative files. It has no mathematics. |
| `explore` | `haiku` | Lookup that locates and quotes. It does not synthesize. |
| `session-close` | `haiku` | The work follows a template over read-only git and make commands. |
| Main session | project default | It orchestrates, prompts and reviews. It does not do the hard algebra or the independent audits. |

To raise the model of one session, use `/model` when a task needs it. This does not change the
table.

## Cost shape

The agent that does the derivations dominates the spend. The largest spike in the project that
this template came from was not a strong model on a hard problem. It was **fan-out**: ten
parallel writer subagents used about 1.5M subagent tokens in about 17 minutes. They produced ten
voices, and one author had to rewrite them (`docs/failure_modes.md`). Watch `/usage` when a
session dispatches several subagents at the same time. See the rule in `docs/WORKFLOW.md` §8
about what parallelism is good for and what it is not good for.
