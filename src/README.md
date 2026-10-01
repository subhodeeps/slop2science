# src — production code

    julia/      Julia package  (Project.toml + Manifest.toml, both committed)
    python/     Python package (pyproject.toml + uv.lock, committed; the venv is built by uv)

Delete the directory for any language this project does not use; `/init-paper` does this. The
libraries each environment carries are the PI's list in `packages.txt` in that directory.

## The rules that matter here

- **Physics enters only through `symbolic/generated/`.** Never hand-write a coefficient or an
  equation, not even temporarily. If something is missing, stop and derive and export it.
- No result guesses, no known answers, no tables of expected values anywhere in this tree. A
  shift, target or bracket comes from a documented automated rule.
- Generic in the element type, so the same code path runs at working and extended precision. A
  precision study that runs different code at each precision compares two implementations.
- Residuals are evaluated in the **original** problem.
- Every module has a test in `tests/<lang>/`; at least one test per topic is a known-answer
  test of the **full chain**.

Full rules: `.claude/rules/implementation.md`. Workflow and order of work:
`.claude/skills/solver-workflow/SKILL.md`.
