# Model routing

The single place model identifiers appear in this repository. Agent frontmatter cites this
file; when a model is retired or a tier changes, one file changes.

## The choice this template makes, and its cost

Bare tier aliases (`opus` / `sonnet` / `haiku` / `fable`) resolve to "whatever is latest in
that tier for this account" and can change without any commit here — which means a result's
provenance record can name a model that is no longer what ran. Exact IDs make the record
honest but **guarantee** eventual breakage: a retired ID surfaces as an explicit
model-not-found error rather than a silent substitution.

This template ships **aliases by default**, because a template that breaks on first use is
worse than one whose provenance is a tier rather than a build. If your project reports
model-sensitive results, switch the table to exact IDs, log the decision, and expect to
revisit it — that is the trade, made deliberately.

## Table

| Agent / session | Model | Why |
|---|---|---|
| `derivation` | `opus` | The hard algebra, where a wrong answer is most expensive and least visible. |
| `paper-writer` | `opus` | The main human-facing deliverable; it must reconstruct and explain what the source omits, not assemble bounded text. Runs rarely. |
| `implementation` | `sonnet` | Bounded by tests, generated coefficients and the validation protocol. |
| `literature` | `sonnet` | Bounded by primary sources; its characteristic failures are procedural (misread PDF, unverified identifier), not reasoning gaps. |
| `verification` | `sonnet` | Checklist-driven with a fixed failure taxonomy. Raise to `opus` for an audit that must re-derive rather than re-check. |
| `status-reporter` | `sonnet` | Summarising authoritative files; no mathematics. |
| `explore` | `haiku` | Locate-and-quote lookup, no synthesis. |
| `session-close` | `haiku` | Template-following over read-only git/make commands. |
| Main session | project default | Orchestrates, prompts and reviews; does not itself do the hard algebra or the independent audits. |

Raise a single session with `/model` when a task warrants it; that does not change this table.

## Cost shape

Spend is dominated by whichever agent does the derivations. The largest spike observed in the
project this template came from was not a strong model on a hard problem but **fan-out**: ten
parallel writer subagents, ~1.5M subagent tokens in ~17 minutes, producing ten voices that
had to be rewritten by one author anyway (`docs/failure_modes.md`). Watch `/usage` whenever a
session dispatches several subagents at once, and see the rule in `docs/WORKFLOW.md` §8 about
what parallelism is and is not good for.
