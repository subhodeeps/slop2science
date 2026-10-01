---
name: external-code
description: Any code that this project did not write: public implementations that give technique or independent benchmark values, and code that the PI drops into code/_drop/. Record provenance, licence and attribution for it. Use it before you consult or adapt an external implementation.
when_to_use: 'Trigger phrases: existing implementation, reference code, how do others do this, independent benchmark values, use this package, I dropped a script in, use this code, adapt this, _drop'
---

# External and PI-supplied code

This skill is the one canonical statement of the attribution and licence rules for code that
this project did not write. Papers and published numbers belong to `literature-audit`. They do
not belong to this skill.

## Attribution — required, not optional

Some modules use the technique, the algorithm structure or the numerical detail of an external
implementation. The docstring or header of each such module must have these items:

- the URL of the repository or package, and the **specific commit or release** that you
  consulted
- the authors, as that project credits them
- the licence
- what exactly you took: an idea, the structure of an algorithm, a specific formula or a test
  case. "Informed by" and "ported from" are different. Do not blur them.

If you consult an implementation and then write your own, you still consulted it. Copying is not
the line to avoid. The line to avoid is failing to say what you looked at.

## Licence

- Check the licence **before** you read the code in detail. Record it.
- If the licence is not compatible with the intended use of this project, do not consult the
  code for implementation detail. You can still cite its *published results* as a benchmark.
  That is a literature matter. It is not a code matter.
- Never copy code that has no licence. No licence means no permission. It does not mean
  permission by default.
- Record the licence check itself. Then a later reader does not repeat it.

## What external code can be, and what it cannot be

| Use | Allowed? |
|---|---|
| A source of technique or algorithm structure, with attribution | yes |
| A source of independent benchmark **values** | yes. Record how the values were produced. |
| A cross-check of the own implementation of this project | yes, labelled `cross-check` |
| A dependency of the production pipeline | only by PI decision, logged, with the licence recorded |
| A source of physics equations to shorten a derivation | **no.** Equations enter through `symbolic/generated/`, from the derivation of this project (CLAUDE.md §5) |

The last row is the important row. The coefficient function of an external solver is as
untrusted as a coefficient that someone types from a paper. It can be right. There is no record
of why, and no check that it matches the conventions of this project.

## Where it lives

- `code/reference/<topic>/` — third-party code kept for reference. Committed. Project code never
  imports it. The pipeline never runs it.
- `code/pi/<topic>/` — the own code of the PI, kept as supplied and unchanged.
- `code/unused/` — supplied code that was not useful, kept with a note that states why. Keep it.
  Do not delete it. "We tried this and it did not fit" is information.
- `code/_drop/` — the transient drop folder of the PI. Git ignores it, except its README. Empty
  it by moving each file onward. Never empty it by deletion.

Adapted code goes to its normal place (`src/`, `validation/`, `symbolic/common/`). Rewrite it to
the interfaces of this project. Add the attribution block above. **Also** move the original to
`code/reference/` or `code/pi/`. Then the source of the adaptation stays available for
comparison.

## Intake of a dropped file

The session-start hook reports a `code/_drop/` that is not empty. For each file:

1. Identify what it is and where it came from. If the file does not state the provenance, ask
   the PI. Do not infer it from the style or the contents of the code.
2. Record the licence and the author.
3. State plainly what it is useful for here and what it is not useful for.
4. Move it to `code/reference/`, `code/pi/` or `code/unused/`, with an entry in the README.
5. Leave the drop folder empty.

Never run a dropped script before you read it. Never let one write into `src/`,
`symbolic/generated/`, `validation/**/records/` or `papers/`.
