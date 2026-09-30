<!-- For a scientific change, the diff is not self-explanatory. Fill in what a reviewer
     cannot reconstruct from the code. Delete any section that genuinely does not apply. -->

## What this establishes

<!-- The scientific claim, in one or two sentences. Not "added stage 04" — what stage 04
     establishes. -->

## Kind

- [ ] **REPRODUCTION** — judged against the source: <which equation / table / figure>
- [ ] **EXTENSION** — judged against: <independent benchmark / exact limit / physical requirement>
- [ ] **CROSS-CHECK** of an existing result, by: <the different route taken>
- [ ] Harness only — no scientific content

## Evidence

<!-- Script and check label per displayed equation; record per number. A claim with no
     citable evidence does not belong in the diff (docs/WORKFLOW.md §3). -->

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

<!-- Paste actual output, not "all green". -->

## Not checked, and why

<!-- Mandatory and rarely empty. What a reviewer should not assume was verified. -->

## Records and docs updated

- [ ] `docs/STATUS.md` — the line this change makes untrue
- [ ] `docs/reproduction_and_extension.md` — the affected row(s), both tables if relevant
- [ ] `docs/decision_log.md` — any PI decision this encodes
- [ ] `handoff.md` — where the work stands now
- [ ] Write-up committed together with its script

## Open after this

<!-- What remains, and who it waits on: [PI] / [tool] / [lit]. -->
