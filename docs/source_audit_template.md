# Source audit template

Copy this file to `docs/<topic>_source_audit.md` and fill it in. The template is
domain-agnostic. Rename or drop a section that does not apply. **Do not drop §N.** The record of
open issues is the purpose of the audit.

For the procedure and the rules to read a PDF, see `.claude/skills/source-audit/SKILL.md`.

---

## Source

State the path or the registry label. State the **exact version** that you consulted (preprint
vN or journal). The versions differ, sometimes in the equation that this project needs.

## A. Bibliographic record

- title, authors, venue
- version, identifiers (DOI, preprint ID), date
- related versions, and what is different between them

## B. Conventions and notation

Record the items below as the source states them. **Transcribe them. Do not paraphrase them into
the vocabulary of this project.**

- units, normalizations, signature or sign conventions
- coordinates or independent variables, and their ranges
- dependent variables, and the definition of each
- orientation conventions, and conventions for time and direction
- the definition of each reported quantity
- labelling and ordering of results
- angular, basis or harmonic conventions, where they apply

Send each ambiguous item to §N. Put `OPEN` in `docs/conventions.md`. Do not choose a reading
here.

## C. Setup

State the background, the system, the state or configuration that the source perturbs or
studies, and each function or parameter that the source defines.

## D. The perturbation, expansion or approximation scheme

- the ansatz, with its dependence on time or on a parameter
- the basis and its normalization
- the amplitudes or unknowns, and their meaning
- the order to which the source carries the expansion, and what it drops

## E. Displayed equations

**Use one row for each displayed equation in scope.** This section is the substance of the
audit.

| Eq. | Section/page | Variables | Order | Role | Depends on | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

`Role` states why the equation exists: definition, constraint, evolution, gauge condition,
reduction step or result. `Notes` records what the source states about the equation that its
form does not show.

## F. Reduction

- which equations the source uses, and which it differentiates
- which variables the source eliminates, and in what order
- the intermediate and final reduced forms
- each variable transformation, and its inverse
- **each item that the source calls "standard" or omits.** This list is the derivation plan.

## G. Singular structure and limits

For each singular point, boundary or limit, fill in a row:

| Location | Type | Indicial/limiting relation | Exponents/behaviours | Physical reading |
|---|---|---|---|---|

## H. Boundary or initial conditions

Record exactly what the source imposes, where it imposes it, and the physical interpretation
that the source gives. Record the exact words of the source for the interpretation. A prose and
equation mismatch often occurs here. A paraphrase hides the mismatch.

## I. Method

- the numerical or analytic method, step by step as the source gives it
- its parameters, truncations, resolutions and precision
- initial guesses, brackets and the continuation strategy
- the convergence criteria, and whether the source states them

## J. Results

- what the source tabulates or plots, with table and figure numbers
- parameter values, resolutions, precision and printed digits
- the benchmark comparisons of the source, and what it compares against
- internal consistency: do the tables agree with the figures and the text?

## K. Special cases and exact results

Record each closed-form, exact or degenerate case that the source gives. These cases give the
cheapest and strongest checks later. Record them also if they look incidental.

## L. Claimed extensions and future work

Record exactly what the source claims. Distinguish done, sketched and asserted. A later project
inherits these claims. Record which is which.

## M. What the source does not give

List the steps that the source calls standard. List the constants that it states without
derivation, the numerical detail that it omits and the assumptions that it does not state.
**The derivation plan is this list, in the order of dependency.**

## N. Open issues

Use the five-item form (CLAUDE.md §3). Use one row for each issue. Do not resolve anything here
silently.

| # | Source states | Its equations imply | Independent derivation gives | Adopted (D-NNN) | Deciding validation |
|---|---|---|---|---|---|
| | | | | | |

A deciding validation can be non-computational, for example a statement from the authors, or an
equivalent external source. Record that. Do not leave the cell blank.

## O. Reproduction targets

List the rows that this audit adds to `docs/reproduction_and_extension.md`. Include each
equation, table and figure that the project intends to reproduce. Set all rows to
`not attempted`.
