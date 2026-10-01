# Audit report template

    # Audit — <what you audited> — <date>

    Auditor:   verification subagent (read-only; a hook enforces this)
    Scope:     <the exact files, stages, records or claims in scope>
    Out of scope: <what you deliberately did not examine>
    Commands run:
      <each command, word for word>

    ## Verdict

    <One of: no findings | findings below, none blocking | blocking findings below.>
    <One sentence: what the audit established, and at which resolution and precision.>

    ## Findings

    ### F1 | <class> | <severity: blocking|high|medium|low>

    Claim audited:   <the claim, quoted from where it is made, with a file:line>
    Cited evidence:  <what the claim cites>
    What I found:    <what the cited evidence establishes>
    Evidence:
      $ <command>
      <the actual output, quoted, not paraphrased>
    Why it matters:  <the consequence, not your confidence>
    Suggested check: <the specific check that settles it>

    ### F2 | ...

    ## Checks run and passed

    | Check | Command | Result |
    |---|---|---|

    List only checks that you ran.

    ## Checks NOT run, and why

    | Check | Why not | What it would establish |
    |---|---|---|

    This section is mandatory. In a real audit it is never empty. An audit that lists no gaps
    claims a completeness that it cannot have.

    ## Audit completeness

    <State if the stopping rule is met. Did an independent route confirm the result? Does the
    literature agree, or is there a stated reason why you cannot check the result against it? If
    the rule is met, say that the audit is complete. If it is not met, state exactly what
    remains.>
