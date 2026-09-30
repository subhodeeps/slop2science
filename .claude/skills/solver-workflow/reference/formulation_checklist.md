# Formulation checklist — before any solver code exists

Answer every question here, in the derivation and verified by a stage script, before writing
the first line of the solver. Each unanswered question becomes a bug that is indistinguishable
from a discretization problem later.

## The problem

- [ ] What exactly is the unknown, and what is the parameter being solved for?
- [ ] What equation, in what variable, on what domain? Cite the derivation stage.
- [ ] Which of the source's equations is this, or what extension of it? (`Kind:`)

## Singular points and endpoints

- [ ] Every singular point of the domain, located and classified.
- [ ] The exponents/behaviours at each one, **derived**, not assumed and not generalized from
      another case by substituting a symbol.
- [ ] Which behaviour at each endpoint is the physical one, and by what argument.
- [ ] The factors pulled out to regularize the problem, and what remains after they are.
- [ ] A check that the remaining function really is regular there.

## Domain and discretization

- [ ] The map from the physical domain to the computational one, and why this map.
- [ ] Where the map concentrates resolution, and whether that is where the solution varies.
- [ ] The discretization, and what its convergence rate should be for this smoothness.
- [ ] How boundary conditions are imposed: by construction (factored out) or by row
      replacement. If rows are replaced, which rows and what that does to the spectrum.

## Structure in the unknown parameter

- [ ] How the parameter enters: linearly, polynomially of degree p, transcendentally?
- [ ] If polynomially: p, read from the generated coefficients rather than assumed.
- [ ] How the problem is solved in that structure, and what the solution method adds to the
      solution set that the original problem does not contain.
- [ ] Expected matrix or system sizes, estimated before assembling anything.

## Acceptance

- [ ] The exact-answer problem that will test the full chain.
- [ ] The residual definition, in the **original** problem, and its norm.
- [ ] The resolutions and precisions each result will be confirmed at.
- [ ] The independent benchmark, its method, and the convention conversion in full.
- [ ] The diagnostics that distinguish a real result from a solver artefact.
- [ ] What the record will contain (`docs/validation_protocol.md` §12).

## Red flags in a formulation

- An endpoint exponent obtained by pattern-matching another case rather than derived.
- A boundary condition chosen because it makes the solver converge.
- A factorization that removes a singularity without a check that it did.
- "We will filter the spurious ones by eye."
- A degree in the unknown parameter assumed rather than read off the coefficients.
