# PI code intake — the conversation to have

The PI drops a file in `code/_drop/` and says something like "use this" or "here is a script
that does the thing". You want to read the file and start to adapt it. That loses two items that
only the PI knows. They are gone when the session ends.

## Ask before you read the file closely

1. **Where does it come from?** Is it the own work of the PI, a collaborator, old code of a
   supervisor, a package, the supplement of a paper, or a forum post? The answer decides the
   licence. It also decides how far you can assume that the code is correct.
2. **What does the PI believe that it does? Did anyone ever check it?** "This reproduces Table 2"
   and "this is what I was trying out" are completely different inputs.
3. **What is it for here?** Is it a technique reference, benchmark values or a cross-check? Is it
   meant to become part of the pipeline? The answer decides where the file goes and which rules
   apply.
4. **Does the PI believe that it is correct?** Record the answer, including "unknown". If you
   treat an unvalidated script as a reference implementation, the mistake is costly. Its
   outputs look like independent confirmation.

## Then do these steps

- Record the answers in the README of the destination folder, next to the file. Do not record
  them in chat or in a commit message. Record them in a file, where the next session finds them.
- Check and record the licence, also for the own code of the PI. The PI can plan to publish it.
- **Do not run the file before you read it.** Do not run it for a quick look at the output.
- Do not import the file into `src/`. If it must become part of the pipeline, the PI decides
  and logs the decision in `docs/decision_log.md`. Rewrite the code to the interfaces of
  this project, with attribution. Do not vendor it.
- If the project uses its numbers as a benchmark, the numbers need provenance, like a published
  table: the method that produced them, the conventions and the conversion. The output of an
  in-house script is not independent evidence unless someone validated it independently. State
  which case applies.

## If it contradicts the project

A dropped script can give a result that disagrees with the result of the project. The script is
**not** automatically authoritative. It is also not automatically wrong. It is a discrepancy.
Record it in the five-item form (CLAUDE.md §3), with the script as one of the parties. Do not
change the project to match the script. Do not dismiss the script. The PI decides.

## If it is not useful

Say so one time, plainly, with the reason. Move the file to `code/unused/` with that reason in
the README. Do not leave it in the drop folder. Do not find a use for it to avoid saying that it
is not useful. An orphaned script that nobody can account for is the specific failure that the
orphan check of the session close finds.
