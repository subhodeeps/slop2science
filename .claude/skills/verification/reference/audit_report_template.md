# Audit report template

    # Audit — <what was audited> — <date>

    Auditor:   verification subagent (read-only; hook-enforced)
    Scope:     <the exact files, stages, records or claims in scope>
    Out of scope: <what was deliberately not examined>
    Commands run:
      <each command, verbatim>

    ## Verdict

    <One of: no findings | findings below, none blocking | blocking findings below.>
    <One sentence on what was actually established, and at what resolution/precision.>

    ## Findings

    ### F1 | <class> | <severity: blocking|high|medium|low>

    Claim audited:   <the claim, quoted from where it is made, with a file:line>
    Cited evidence:  <what the claim cites>
    What I found:    <what the cited evidence actually establishes>
    Evidence:
      $ <command>
      <actual output, quoted, not paraphrased>
    Why it matters:  <the consequence, not the confidence>
    Suggested check: <the specific check that would settle it>

    ### F2 | ...

    ## Checks run and passed

    | Check | Command | Result |
    |---|---|---|

    Only checks actually executed appear here.

    ## Checks NOT run, and why

    | Check | Why not | What it would establish |
    |---|---|---|

    This section is mandatory and is never empty in a real audit. An audit that lists no gaps
    is claiming completeness it cannot have.

    ## Audit completeness

    <Whether the stopping rule is met: has an independent route confirmed the result, and does
    the literature agree or is there a stated reason it cannot be checked? If met, say the
    audit is complete. If not, say exactly what remains.>
