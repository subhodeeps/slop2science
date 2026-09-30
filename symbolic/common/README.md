# symbolic/common — shared helper code

Loaded by path from `PROJECT_ROOT`, never copy-pasted into a stage script. Lives here rather
than inside a skill so that scripts can load it directly.

    checks.wl / checks.py / checks.jl     the print-before-assert check helpers
    selftest_checks.*                     self-tests for the above

One set of check helpers per language the project derives in, with the **same semantics**: a
check prints what it found and then asserts it, records a labelled pass/fail, and the run exits
non-zero if any check failed. Identical semantics matter because a stage's check count is
compared across reruns, and a topic may be cross-checked in another tool.

Run the self-tests before relying on any of this:

    scripts/run symbolic/common/selftest_checks.wls
    scripts/run symbolic/common/selftest_checks.py
