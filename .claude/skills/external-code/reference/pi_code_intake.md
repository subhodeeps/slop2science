# PI code intake — the conversation to have

The PI drops a file in `code/_drop/` and says something like "use this" or "here's a script
that does the thing". The temptation is to read it and start adapting. That loses the two
things only the PI knows, and they are gone once the session ends.

## Ask, before reading it closely

1. **Where is it from?** The PI's own work, a collaborator, a supervisor's old code, a
   package, a paper's supplement, a forum post? This determines both the licence and how much
   its correctness can be assumed.
2. **What is it believed to do, and was that ever checked?** "This reproduces Table 2" and
   "this is what I was experimenting with" are completely different inputs.
3. **What is it for here?** Technique reference, benchmark values, a cross-check, or is it
   meant to become part of the pipeline? The answer decides where it lands and what rules
   apply.
4. **Is it correct as far as they know?** Record the answer, including "unknown". An
   unvalidated script treated as a reference implementation is a very expensive mistake,
   because its outputs look like independent confirmation.

## Then

- Record the answers in the destination folder's README, next to the file. Not in chat, not
  in a commit message — in a file, where the next session finds it.
- Check and record the licence, even for the PI's own code (they may intend to publish it).
- **Do not run it before reading it.** Not for a quick look at the output.
- Do not import it into `src/`. If it is to become part of the pipeline, that is a PI
  decision, logged in `docs/decision_log.md`, and the code is rewritten to this project's
  interfaces with attribution — not vendored.
- If its numbers are to be used as a benchmark, they need provenance exactly like a published
  table: the method that produced them, the conventions, the conversion. An in-house script's
  output is not independent evidence unless it was independently validated, and say so
  either way.

## If it contradicts the project

A dropped script whose result disagrees with the project's own is **not** automatically
authoritative, and it is not automatically wrong either. It is a discrepancy: record it in
the five-point form (CLAUDE.md §3), with the script as one of the parties. Do not change the
project to match it, and do not dismiss it, without the PI deciding.

## If it is not useful

Say so, once, plainly, with the reason — and move it to `code/unused/` with that reason in the
README. Do not quietly leave it in the drop folder, and do not find a use for it to avoid
saying it was not useful. An orphaned script nobody can account for is the specific failure
the session-close orphan check exists to catch.
