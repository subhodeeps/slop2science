# Failure modes — index

This repository records what went wrong in AI-assisted paper reproduction, what each failure cost,
and which mechanism exists because of it. The records are in four files. Each failure has an id.
Other files cite an id, for example "entry 9" or "0c". Use this table to find the file.

Read the files before an audit, before you write a report, and whenever a session is under time
pressure. The entries are not hypothetical. Each entry in `inherited.md` happened.

| File | Ids | Content | Lifecycle |
|---|---|---|---|
| [`failure_modes/model.md`](failure_modes/model.md) | 0a, 0b, 0c | How the model fails: context rot, hyperfixation, sycophancy. No project discipline prevents them. | stable, from the template |
| [`failure_modes/inherited.md`](failure_modes/inherited.md) | 1–12 | Failures from the project that this template came from. | stable, from the template |
| [`failure_modes/anticipated.md`](failure_modes/anticipated.md) | A–E, C2 | Failures that nobody has seen yet, which the structure of the project guards against. | stable. Move an entry to `project.md` if it happens. |
| [`failure_modes/project.md`](failure_modes/project.md) | P1, P2, … | The failure log of this project. | **grows.** Add an entry at each `/session-close` where something went wrong. |

Each entry states three things: **what happened**, **what it cost** and **which mechanism exists
because of it**.

## Which entry answers which question

| Question | Entry |
|---|---|
| Why does the context budget exist? | 0a, 10 |
| Why must a check print before it asserts? | 0b, 1 |
| Why must a verifier not know what you hope it finds? | 0c |
| Why read the `.tex` and not the PDF text layer? (`corpus.md` gives the order) | 2 |
| Why does the project have a stopping rule for audits? | 3 |
| Why can convergence not validate a formulation? | 4 |
| Why does `/session-close` check for orphaned files? | 5 |
| Why does a writer write in chunks, and why one author? | 6, 7 |
| Why does a brief start with the reader? | 8 |
| Why does the decision log outrank a working note? | 9 |
| Why does each fact have one owner? | 11 |
| Why are machine captures and curated prompts separate? | 12 |
| Why does each topic have one declared owner tool? | A |
| Why does the project track the extension as an equal part? | B, C |
| Why is the transcript outside the repository? | C2 |
| Why does Claude ask the PI before it supplies a default? | D |
| Why does an imported reference stay unverified? | E |
