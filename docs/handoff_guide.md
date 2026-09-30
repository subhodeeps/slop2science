# Writing a handoff

How to write `handoff.md`: the prose note one session leaves for the next. Read this when you
are writing one — it costs nothing until then, which is why it lives here rather than as
comments inside the file itself.

Mechanism (who reads it, when, and how the age is stamped): `docs/GUIDE.md` §2 and
`.claude/hooks/session_context.sh`. Where it sits among the other continuity artifacts:
`TEMPLATE_GUIDE.md` §4a.

## 1. What it is for

`docs/STATUS.md` records the project's **state**. `docs/status_history.md` records what
**happened**. Neither can hold what was in your head when you stopped:

- the stage that is half-written and whether it currently runs;
- the number that looked wrong, before you knew why;
- the thing you suspect and have not shown;
- the approach you already tried that does not work, so nobody tries it again;
- the question you would ask the PI if they were here.

All of that is provisional, and some of it will turn out to be wrong. That is exactly why it
does not belong in a record — and exactly why losing it is expensive. Reconstructing a
suspicion takes as long as having it did.

## 2. The one rule that matters

**A handoff is never evidence.**

It is unverified by construction. If something in it turns out to be worth relying on, it
gets established properly — a script, a printed check, a labelled result — moved into a
record, and then **the handoff line is deleted**. A handoff entry that has been promoted and
left behind is a claim with two homes and one of them unversioned.

Precedence, when they disagree: `docs/decision_log.md`, `docs/STATUS.md`,
`docs/reproduction_and_extension.md` and the validation records are right; the handoff is
stale. Never resolve a conflict in the handoff's favour, and never quietly pick one — record
the inconsistency (`docs/failure_modes.md` entry 9 is what happens otherwise: a report writer
copied a claim from a working note that the decision log contradicted, and it shipped).

## 3. Write it for a stranger arriving in three months

You do not know who reads it or when. It might be you tomorrow; it might be a collaborator
after a term away; it might be you in March having forgotten the whole thing. So:

- **No pronouns without referents.** "It stopped converging" — what did?
- **No session-local shorthand.** "the second one", "that weird factor", "the thing from
  yesterday" all evaporate overnight.
- **Name files and identifiers.** `symbolic/topic1/stage_04_reduce.wls`, `D-007`, `N=80`,
  not "the reduction script".
- **Say whether things currently run.** "Stage 04 is written and passes; stage 05 exists and
  does not run yet" is worth ten lines of narrative.

The hook stamps the file's age into context precisely because prose reads as current. At
three days old a handoff is context; at three months it describes a project that has moved
on. Write so that a reader who is *told* it is 90 days old can still use it.

## 4. The shape

Four headings. Use them; they are in this order because that is the order a returning session
needs them.

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

**"What I believe but have not established" is the heading that earns the file.** It has
nowhere else to live: too uncertain for STATUS, too specific for the decision log, and the
single most expensive thing to reconstruct. Every entry under it names what would settle it,
so it is a lead rather than a rumour.

**"Next" must agree with `docs/STATUS.md`'s immediate next task.** If it does not, one of the
two is wrong — fix it now, at the close, not at the next session's start.

## 5. A good handoff

```markdown
# Handoff

## Where I stopped
Stage 04 (`symbolic/topic1/stage_04_reduce.wls`) is written and passing — 18 checks, and its
write-up `derivation/topic1/04_reduce.md` is committed with it. Stage 05 exists as a file but
is a sketch: it runs to the substitution and then stops. It is NOT in `stages.txt` yet, on
purpose, so `make stages` stays clean.

## What I believe but have not established
- The source's Eq. (12) looks like it is missing a factor of 2 in the second term. Derived by
  hand only, not scripted. What would settle it: redo the reduction from Eq. (9) in stage 05
  and compare coefficient by coefficient — and if it holds up, it is a five-point discrepancy
  record, not a fix.
- The residual at N=80 is ~1e-7 where N=40 gave ~1e-9. That is the wrong direction. It might
  be conditioning rather than a bug, but I have not looked. What would settle it: run the
  same case in extended precision; if the residual improves, it is conditioning.

## Watch out for
`make stages TOPIC=topic1` is clean, but only because stage 05 is out of the manifest. Do not
add it until it actually terminates, or every subsequent run fails and the failure looks like
stage 04's.

I lost about an hour reading Eq. (12) from the PDF text layer before realising the tarball
has the LaTeX. Use `papers/source/2504.01234v2/ms.tex` — the macros are in `macros.sty` and
`\calJ` expands with a factor I nearly missed.

## Next
Finish stage 05: complete the substitution, add the coefficient-by-coefficient comparison
against source Eq. (12), and only then add it to `stages.txt`. This is STATUS's immediate
next task.
```

Why it works: every claim is either marked as unestablished with a test attached, or names a
file and a check count. It says what does not run. It warns about a trap that is invisible
from the repository. And "Next" is one action, not a wish list.

## 6. A bad handoff, annotated

```markdown
# Handoff
Made good progress on the reduction today. The master equation works now and matches the
paper. Fixed the issue with the residual. Should be able to finish the solver next time —
just need to tidy a few things up. Also see my note about the factor.
```

Every line fails:

| Written | Problem |
|---|---|
| "Made good progress" | Unfalsifiable. Progress on what, to what state? |
| "The master equation works now and matches the paper" | A **result claimed in a handoff**. If it is verified it belongs in STATUS with its script and check label; if it is not, saying "matches" is exactly the false confidence the project guards against. |
| "Fixed the issue with the residual" | Which issue, in which file, verified how? The next session cannot tell whether to trust it. |
| "just need to tidy a few things up" | Unbounded. Which things? |
| "see my note about the factor" | Which note? A dangling reference to something only you can find. |
| no mention of what is broken | The most valuable line is the missing one. |

## 7. Length and mechanics

- **Overwrite; never append.** A handoff that has become a log is a handoff nobody reads, and
  the log already exists in `docs/status_history.md`. If a line is still true next session,
  the next session rewrites it.
- **Aim for 10–30 lines.** Long enough for the four headings, short enough to read in the
  first ten seconds of a session. It is injected into the opening context, so length is a
  real cost paid on every session start.
- **Delete a heading with nothing under it** rather than writing "N/A". An empty "Watch out
  for" is information: nothing bit you. (This is why the seeded `handoff.md` ships with no
  headings at all — a file that opens with four empty ones would break this rule on its own
  first line.)
- **HTML comments are stripped when it is injected**, so a comment is a safe place for a note
  to yourself that the next session does not need.
- Written at `/session-close` (step 6a) and at `/checkpoint` (step 5) — the checkpoint case
  matters, because refreshing the handoff is worth doing even when no commit is proposed.

## 8. It is committed and shareable — the transcript is not

`handoff.md` is tracked and shared with anyone the repository is shared with. The condensed
session transcript is deliberately **outside** the repository
(`.claude/hooks/capture_session.py`, `docs/failure_modes.md` C2), because sharing permissions
inherit downward and cannot be subtracted from a subfolder.

So: **write nothing in the handoff you would not want a collaborator, a reviewer or a
supervisor to read.** Frustration with a source paper, a guess about why someone's published
number is off, an aside about a colleague's code — that is transcript material, not handoff
material. Keep the handoff technical.

## 9. Special cases

**The session was interrupted, or hit a usage limit.** This is when the handoff matters most
and gets written worst. Say explicitly what was *completed* versus *started and left
incomplete* (CLAUDE.md §8a), and name any file an interrupted step left behind. Scope shrinks
under interruption — the handoff is where you record that it did, so the next session does not
resume from a false picture.

**Nothing much happened.** Say so, briefly, and say why: blocked on a PI decision, waiting on
a source, spent the session reading. "Nothing to report" with no reason reads as an
abandoned session.

**The work is in a broken state.** Say that first, in the first line, before anything else.
A returning session that runs `make test` and sees failures it did not cause will spend real
time deciding whether the repository is broken or the tests are. One sentence prevents it.

**Handing off to a person rather than a session.** Same file, same discipline — it is already
written for a stranger. Add the one thing a session does not need and a person does: where the
open questions for the PI are (`docs/STATUS.md` open questions, tagged).

## 10. Checklist

- [ ] Overwrote the file; did not append
- [ ] Every file, identifier and number named explicitly — no "it", no "the thing"
- [ ] Said what is in a working state and what is not
- [ ] No result claimed as established; anything verified has been moved to a record and the
      handoff line deleted
- [ ] Each suspicion has what-would-settle-it attached
- [ ] "Next" matches `docs/STATUS.md`'s immediate next task
- [ ] Interruptions recorded as completed-versus-incomplete
- [ ] Nothing here you would not want a collaborator to read
- [ ] Under ~30 lines
