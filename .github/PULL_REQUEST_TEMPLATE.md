<!-- For a scientific change, the diff does not explain itself. Fill in what a reviewer cannot
     reconstruct from the code. Delete a section only if it does not apply. -->

## What this establishes

<!-- State the scientific claim in one or two sentences. Do not write "added stage 04". Write
     what stage 04 establishes. -->

## Kind

- [ ] **REPRODUCTION** — judged against the source: <which equation / table / figure>
- [ ] **EXTENSION** — judged against: <independent benchmark / exact limit / physical requirement>
- [ ] **CROSS-CHECK** of an existing result, by: <the different route>
- [ ] Harness only — no scientific content

## Evidence

<!-- Give the script and the check label for each displayed equation. Give a record for each
     number. A claim with no citable evidence does not belong in the diff
     (docs/WORKFLOW.md §3). -->

| Claim | Evidence |
|---|---|
| | `[E: \`path\`, "check label"]` |

## Checks run

```
make check      ->
make test       ->
make stages TOPIC=        ->
make codegen-check TOPIC= ->
```

<!-- Paste the real output. Do not write "all green". -->

## Not checked, and why

<!-- This section is mandatory, and it is rarely empty. State what the reviewer must not
     assume that you verified. -->

## Records and docs updated

- [ ] `docs/STATUS.md` — the line that this change makes untrue
- [ ] `docs/reproduction_and_extension.md` — the affected rows, in both tables if relevant
- [ ] `docs/decision_log.md` — each PI decision that this change encodes
- [ ] `handoff.md` — where the work stands now
- [ ] Commit the write-up together with its script

## Open after this

<!-- State what remains and who it waits for: [PI] / [tool] / [lit]. -->
