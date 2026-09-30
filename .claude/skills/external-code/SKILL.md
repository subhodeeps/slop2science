---
name: external-code
description: Any code this project did not write - public implementations used for technique or independent benchmark values, and code the PI drops into code/_drop/ - with mandatory provenance, licence and attribution recording. Use before consulting or adapting any external implementation.
when_to_use: 'Trigger phrases: existing implementation; reference code; how do others do this; independent benchmark values; use this package; I dropped a script in; use this code; adapt this; _drop'
---

# External and PI-supplied code

The one canonical statement of the attribution and licence rules for code this project did not
write. Papers and published numbers are `literature-audit`'s remit, not this skill's.

## Attribution — required, not optional

Any module whose technique, algorithm structure or numerical detail was informed by an
external implementation carries, in its own docstring or header:

- the repository or package URL, and the **specific commit or release** consulted;
- the author(s), as that project credits them;
- the licence;
- what exactly was taken: an idea, an algorithm's structure, a specific formula, a test case?
  "Informed by" and "ported from" are different things and must not be blurred.

Consulting an implementation and then writing your own is still consulting it. The line to
avoid crossing is not copying; it is failing to say what you looked at.

## Licence

- Check the licence **before** reading the code in any detail, and record it.
- A licence incompatible with this project's intended use means: do not consult it for
  implementation detail. You may still cite its *published results* as a benchmark, which is
  a literature matter, not a code matter.
- Never copy code with no licence at all. No licence means no permission, not permission by
  default.
- Record the licence check itself, so a later reader does not have to redo it.

## What external code may and may not be

| Use | Allowed? |
|---|---|
| A source of technique or algorithm structure, with attribution | yes |
| A source of independent benchmark **values** | yes — record how the values were produced |
| A cross-check of this project's own implementation | yes, labelled `cross-check` |
| A dependency of the production pipeline | only by PI decision, logged, with the licence recorded |
| A source of physics equations to shortcut a derivation | **no.** Equations enter through `symbolic/generated/` from this project's own derivation (CLAUDE.md §5) |

That last row is the important one. An external solver's coefficient function is exactly as
untrusted as a coefficient typed out of a paper: it may be right, and there is no record of
why, and no check that it matches this project's conventions.

## Where it lives

- `code/reference/<topic>/` — third-party code kept for reference. Committed. Not imported by
  project code, never run by the pipeline.
- `code/pi/<topic>/` — the PI's own code, kept as supplied, unmodified.
- `code/unused/` — supplied code that turned out not to be useful, kept with a note saying
  why. Kept, not deleted: "we tried this and it did not fit" is information.
- `code/_drop/` — the PI's transient drop folder. Gitignored except its README. Emptied by
  moving each file onward, never by deleting.

Code adapted for actual use goes to its normal home (`src/`, `validation/`,
`symbolic/common/`), rewritten to this project's interfaces, carrying the attribution block
above — **and** the original still moves to `code/reference/` or `code/pi/`, so the thing the
adaptation came from stays available for comparison.

## Intake of a dropped file

The session-start hook reports a non-empty `code/_drop/`. For each file:

1. Identify what it is and where it came from. Ask the PI if the provenance is not in the
   file — do not infer it from the code's style or contents.
2. Record licence and author.
3. Say plainly what it is useful for here, and what it is not.
4. Move it to `code/reference/`, `code/pi/` or `code/unused/` with a README entry.
5. Leave the drop folder empty.

Never run a dropped script before reading it, and never let one write into `src/`,
`symbolic/generated/`, `validation/**/records/` or `papers/`.
