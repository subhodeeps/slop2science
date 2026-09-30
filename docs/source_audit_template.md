# Source audit template

Copy to `docs/<topic>_source_audit.md` and fill in. Domain-agnostic: rename or drop sections
that do not apply, but **do not drop §N** — the open-issues record is the point of the audit.

Procedure and the rules for reading a PDF: `.claude/skills/source-audit/SKILL.md`.

---

## Source

Path or registry label, and the **exact version** consulted (preprint vN / journal). They
differ, sometimes in the equation this project depends on.

## A. Bibliographic record

- Title, authors, venue
- Version, identifiers (DOI, preprint ID), date
- Related versions and what differs between them

## B. Conventions and notation

Record, as the source states them — **transcribed, not paraphrased into this project's
vocabulary**:

- units, normalizations, signature or sign conventions
- coordinates / independent variables, and their ranges
- dependent variables and the definition of each
- orientation and time/direction conventions
- the definition of every reported quantity
- labelling and ordering of results
- angular, basis or harmonic conventions, where applicable

Anything ambiguous goes to §N, and `OPEN` in `docs/conventions.md`. Do not choose a reading
here.

## C. Setup

The background, the system, the state or configuration being perturbed or studied, and every
function or parameter the source defines.

## D. The perturbation / expansion / approximation scheme

- the ansatz, with its time or parameter dependence
- the basis and its normalization
- the amplitudes or unknowns, and their meaning
- what order the expansion is carried to, and what is dropped

## E. Displayed equations

**One row per displayed equation in scope.** This section is the audit's substance.

| Eq. | Section/page | Variables | Order | Role | Depends on | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

`Role` is why it exists: definition, constraint, evolution, gauge condition, reduction step,
result. `Notes` records anything the source states about it that its form does not show.

## F. Reduction

- which equations are used, and which are differentiated
- which variables are eliminated, in what order
- the intermediate and final reduced forms
- any variable transformation, and its inverse
- **anything the source calls "standard" or omits** — this list is the derivation plan

## G. Singular structure and limits

For each singular point, boundary or limit:

| Location | Type | Indicial/limiting relation | Exponents/behaviours | Physical reading |
|---|---|---|---|---|

## H. Boundary or initial conditions

Exactly what the source imposes, where, and what physical interpretation it gives. Record its
own words for the interpretation — this is a frequent source of a prose/equation mismatch, and
the paraphrase is where the mismatch disappears.

## I. Method

- the numerical or analytic method, step by step as the source gives it
- its parameters, truncations, resolutions, precision
- initial guesses, brackets, continuation strategy
- convergence criteria, and whether the source states them

## J. Results

- what is tabulated or plotted, with table and figure numbers
- parameter values, resolutions, precision, printed digits
- the source's own benchmark comparisons, and against what
- internal consistency: do its tables agree with its figures and its text?

## K. Special cases and exact results

Any closed-form, exact or degenerate case the source gives. These are the cheapest and
strongest checks available later — record them even where they look incidental.

## L. Claimed extensions and future work

Exactly what the source claims, distinguishing done / sketched / asserted. A later project
inherits these claims; record which is which.

## M. What the source does not give

Steps called standard, constants stated without derivation, omitted numerical detail,
unstated assumptions. **The derivation plan is this list in dependency order.**

## N. Open issues

Five-point form (CLAUDE.md §3), one row each. Do not silently resolve anything here.

| # | Source states | Its equations imply | Independent derivation gives | Adopted (D-NNN) | Deciding validation |
|---|---|---|---|---|---|
| | | | | | |

A deciding validation may legitimately be non-computational — a statement from the authors, or
an equivalent external source. Record that rather than leaving the cell blank.

## O. Reproduction targets

The rows this audit contributes to `docs/reproduction_matrix.md`: every equation, table and
figure the project intends to reproduce, all `not attempted`.
