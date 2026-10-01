# Write a handoff

This guide explains how to write `handoff.md`: the note that one session leaves for the next
session. Read it when you write a handoff. It costs nothing until then. This is why it is here
and not in comments inside the file.

For the mechanism (who reads the handoff, when, and how the hook stamps its age), see
`docs/GUIDE.md` §2 and `.claude/hooks/session_context.sh`. For the place of the handoff among
the other continuity artifacts, see `TEMPLATE_GUIDE.md` §4a.

## 1. What a handoff is for

`docs/STATUS.md` records the **state** of the project. `docs/status_history.md` records what
**happened**. Neither can hold what you knew when you stopped:

- the stage that is half-written, and whether it runs now
- the number that looked wrong, before you knew why
- the thing that you suspect and did not show
- the approach that you tried and that does not work, so that nobody tries it again
- the question that you would ask the PI if the PI were here

All of this is provisional. Some of it will be wrong. For this reason it does not belong in a
record. For the same reason, losing it is expensive. To rebuild a suspicion takes as long as it
took to form it.

## 2. The one rule that matters

**A handoff is never evidence.**

Nobody verified it. If something in it is worth relying on, establish it properly with a
script, a printed check or a labelled result. Move it into a record. Then **delete the line in
the handoff**. A handoff line that someone promoted and left behind is a claim with two homes,
and one home has no version control.

If files disagree, this is the order of precedence. `docs/decision_log.md`, `docs/STATUS.md`,
`docs/reproduction_and_extension.md` and the validation records are right. The handoff is old.
Never resolve a conflict in favour of the handoff. Never pick one silently. Record the
inconsistency. `docs/failure_modes/inherited.md` entry 9 shows what happens otherwise. A report writer
copied a claim from a working note that the decision log contradicted. The claim shipped.

## 3. Write for a stranger who arrives in three months

You do not know who reads the handoff or when. The reader can be you tomorrow. It can be a
collaborator after a term away. It can be you in March, when you have forgotten everything. So
follow these rules:

- **Do not use a pronoun without a referent.** "It stopped converging": what stopped?
- **Do not use shorthand from the session.** "The second one", "that odd factor" and "the thing
  from yesterday" are gone by the next day.
- **Name files and identifiers.** Write `symbolic/topic1/stage_04_reduce.wls`, `D-007` and
  `N=80`. Do not write "the reduction script".
- **State if each item runs now.** "Stage 04 passes. Stage 05 exists and does
  not run yet" is worth ten lines of narrative.

The hook stamps the age of the file into the context, because prose looks current. At 3 days a
handoff is context. At 3 months it describes a project that moved on. Write so that a reader
who knows that the file is 90 days old can still use it.

## 4. The shape

Use four headings, in this order. A returning session needs them in this order.

```markdown
# Handoff

## Where I stopped
<the specific thing in progress, and whether it is in a working state>

## What I believe but have not established
<suspicions, each with what would settle it — explicitly NOT results>

## Watch out for
<what cost time this session, so the next session does not repeat it>

## Next
<the one concrete next action, matching STATUS's immediate next task>
```

**The heading "What I believe but have not established" is the reason for the file.** It has no
other place to live. It is too uncertain for STATUS. It is too specific for the decision log.
It is the most expensive item to rebuild. Each entry under it names what would settle it. Then
the entry is a lead and not a rumour.

**"Next" must agree with the immediate next task in `docs/STATUS.md`.** If it does not agree,
one of the two is wrong. Fix it now, at the close. Do not wait for the start of the next
session.

## 5. A good handoff

```markdown
# Handoff

## Where I stopped
Stage 04 (`symbolic/topic1/stage_04_reduce.wls`) is written and passes. It has 18 checks. Its
write-up `derivation/topic1/04_reduce.md` is committed with it. Stage 05 is a file, but it is
a sketch. It runs to the substitution and then stops. It is NOT in `stages.txt` yet, on
purpose. Then `make stages` stays clean.

## What I believe but have not established
- Eq. (12) of the source seems to miss a factor of 2 in the second term. I derived this by hand
  only. No script checks it. What would settle it: redo the reduction from Eq. (9) in stage 05
  and compare it coefficient by coefficient. If the result holds, record a five-item
  discrepancy. Do not fix the source.
- The residual at N=80 is about 1e-7. At N=40 it was about 1e-9. This is the wrong direction. It
  can be conditioning and not a bug, but I did not look. What would settle it: run the same case
  in extended precision. If the residual improves, the cause is conditioning.

## Watch out for
`make stages TOPIC=topic1` is clean, but only because stage 05 is not in the manifest. Do not
add stage 05 until it terminates. If you add it too early, all later runs fail, and the
failure looks like a failure of stage 04.

I lost about one hour when I read Eq. (12) from the PDF text layer. The tarball has the LaTeX.
Use `papers/source/2504.01234v2/ms.tex`. The macros are in `macros.sty`. `\calJ` expands with a
factor that I almost missed.

## Next
Finish stage 05. Complete the substitution. Add the coefficient-by-coefficient comparison with
Eq. (12) of the source. Then add the stage to `stages.txt`. This is the immediate next task in
STATUS.
```

Why this works: each claim is either marked as not established, with a test, or it names a file
and a check count. It states what does not run. It warns about a trap that the repository does
not show. "Next" is one action. It is not a wish list.

## 6. A bad handoff, annotated

```markdown
# Handoff
Made good progress on the reduction today. The master equation works now and matches the
paper. Fixed the issue with the residual. Should be able to finish the solver next time —
just need to tidy a few things up. Also see my note about the factor.
```

Each line fails:

| Written | Problem |
|---|---|
| "Made good progress" | Nobody can falsify it. Progress on what, and to which state? |
| "The master equation works now and matches the paper" | This is a **result claimed in a handoff**. If someone verified it, it belongs in STATUS with its script and check label. If nobody verified it, "matches" is the false confidence that the project guards against. |
| "Fixed the issue with the residual" | Which issue, in which file, verified how? The next session cannot decide if it can trust the statement. |
| "just need to tidy a few things up" | It has no limit. Which things? |
| "see my note about the factor" | Which note? The reference points to something that only you can find. |
| no mention of what is broken | The most valuable line is the one that is missing. |

## 7. Length and mechanics

- **Overwrite the file. Never append.** Nobody reads a handoff that becomes a log.
  `docs/status_history.md` already has the log. If a line is still true in the next session,
  the next session writes it again.
- **Aim for 10 to 30 lines.** Use enough room for the four headings. Keep it short enough to
  read in the first ten seconds of a session. The hook injects it into the opening context.
  Therefore its length is a real cost at each session start.
- **Delete a heading that has nothing under it.** Do not write "N/A". An empty "Watch out for"
  is information: nothing caused a problem. This is why the seeded `handoff.md` has no headings.
  A file that starts with four empty headings would break this rule on its first line.
- **The hook strips HTML comments** when it injects the file. A comment is a safe place for a
  note to yourself that the next session does not need.
- Write the handoff at `/session-close` (step 6a) and at `/checkpoint` (step 5). The checkpoint
  case matters. A refreshed handoff has value also when nobody proposes a commit.

## 8. The handoff is committed and shareable. The transcript is not.

Git tracks `handoff.md`. Anyone who has the repository can read it. The condensed session
transcript is **outside** the repository on purpose (`.claude/hooks/capture_session.py`,
`docs/failure_modes/anticipated.md` C2). Sharing permissions inherit downward, and you cannot subtract them
from a subfolder.

Therefore **write nothing that you would not want a collaborator, a reviewer or a supervisor
to read.** Keep these items out of the handoff:

- frustration with a source paper
- a guess about why the published number of someone is wrong
- an aside about the code of a colleague

That is transcript material. It is not handoff material. Keep the handoff technical.

## 9. Special cases

**An interruption or a usage limit stopped the session.** In this case the handoff matters most,
and people write it worst. State what the session *completed* and what it *started and left
incomplete* (CLAUDE.md §8a). Name each file that an interrupted step left behind. Under an
interruption the scope gets smaller. Record in the handoff that it did. Then the next session
does not resume from a false picture.

**Nothing much happened.** Say so briefly, and say why. The reasons can be: blocked on a PI
decision, waiting for a source, or the session was spent on reading. "Nothing to report" with no
reason looks like an abandoned session.

**The work is in a broken state.** Say that first, in the first line, before anything else. A
returning session runs `make test` and sees failures that it did not cause. It then spends real
time to decide if the repository is broken or the tests are broken. One sentence prevents this.

**You hand off to a person and not to a session.** Use the same file and the same discipline.
The file is already written for a stranger. Add one item that a person needs and a session
does not need. State where the open questions for the PI are (`docs/STATUS.md`, open
questions, tagged).

## 10. Checklist

- [ ] I overwrote the file. I did not append.
- [ ] I named each file, identifier and number explicitly. There is no "it" and no "the thing".
- [ ] I stated what works and what does not.
- [ ] The handoff claims no established result. I moved each verified item to a record and
      deleted its line in the handoff.
- [ ] Each suspicion has what would settle it.
- [ ] "Next" agrees with the immediate next task in `docs/STATUS.md`.
- [ ] I recorded interruptions as completed or incomplete.
- [ ] The file has nothing that I would not want a collaborator to read.
- [ ] The file has about 30 lines or fewer.
