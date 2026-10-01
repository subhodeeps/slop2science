# Formulation checklist — before any solver code exists

Answer each question here, in the derivation, verified by a stage script, before you write the
first line of the solver. Each question that you leave open becomes a bug later. You cannot
distinguish that bug from a discretization problem.

## The problem

- [ ] What exactly is the unknown? What is the parameter that you solve for?
- [ ] Which equation, in which variable, on which domain? Cite the derivation stage.
- [ ] Which equation of the source is this, or which extension of it? (`Kind:`)

## Singular points and endpoints

- [ ] You located and classified each singular point of the domain.
- [ ] You **derived** the exponents or behaviours at each singular point. You did not assume
      them. You did not generalize them from another case by substitution of a symbol.
- [ ] You know which behaviour at each endpoint is the physical one, and you have the argument.
- [ ] You know the factors that you pull out to regularize the problem, and what remains after
      you do.
- [ ] A check shows that the remaining function is regular there.

## Domain and discretization

- [ ] You have the map from the physical domain to the computational domain, and the reason for
      this map.
- [ ] You know where the map concentrates resolution, and if the solution varies there.
- [ ] You have the discretization, and the convergence rate that you expect for this
      smoothness.
- [ ] You know how the discretization imposes the boundary conditions: by construction (factored
      out) or by row replacement. If it replaces rows, you know which rows and what this does to
      the spectrum.

## Structure in the unknown parameter

- [ ] How does the parameter enter? Linearly, polynomially of degree p, or transcendentally?
- [ ] If it enters polynomially: you read p from the generated coefficients. You did not assume
      it.
- [ ] You know how to solve the problem in that structure. You know what the solution method
      adds to the solution set that the original problem does not contain.
- [ ] You estimated the sizes of the matrices or systems before you assembled anything.

## Acceptance

- [ ] You have the problem with an exact answer that tests the full chain.
- [ ] You defined the residual in the **original** problem, and its norm.
- [ ] You chose the resolutions and precisions at which you confirm each result.
- [ ] You have the independent benchmark, its method, and the full convention conversion.
- [ ] You have the diagnostics that distinguish a real result from a solver artefact.
- [ ] You know what the record contains (`docs/validation_protocol.md` §12).

## Warning signs in a formulation

- You obtained an endpoint exponent by pattern-matching another case. You did not derive it.
- You chose a boundary condition because it makes the solver converge.
- A factorization removes a singularity, and no check shows that it did.
- "We will filter the spurious ones by eye."
- You assumed a degree in the unknown parameter. You did not read it from the coefficients.
