# src — production code

    julia/      Julia package  (Project.toml + Manifest.toml, both committed)
    python/     Python package (pyproject.toml + uv.lock, both committed; uv builds the venv)

Delete the directory of each language that this project does not use. `/init-paper` does this.
The libraries of each environment are the list of the PI in `packages.txt`, in the directory of
that language.

## The rules that matter here

- **Physics enters only through `symbolic/generated/`.** Never write a coefficient or an
  equation by hand, not even temporarily. If something is missing, stop. Derive it and export
  it.
- Do not guess results. Do not put known answers or tables of expected values anywhere in this
  tree. A documented automated rule must give each shift, target or bracket.
- Write code that is generic in the element type. Then the same code path runs at working
  precision and at extended precision. A precision study that runs different code at each
  precision compares two implementations.
- Evaluate residuals in the **original** problem.
- Each module has a test in `tests/<lang>/`. At least one test for each topic is a
  known-answer test of the **full chain**.

Full rules: `.claude/rules/implementation.md`. Workflow and order of work:
`.claude/skills/solver-workflow/SKILL.md`.
