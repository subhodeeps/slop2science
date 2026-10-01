# symbolic/common — shared helper code

Scripts load this code by path from `PROJECT_ROOT`. Never copy it into a stage script. It lives
here, not inside a skill, so that scripts can load it directly.

    checks.wl / checks.py / checks.jl     the print-before-assert check helpers
    selftest_checks.*                     self-tests for the check helpers

Each language in which the project derives has one set of check helpers. The sets have the
**same semantics**. A check prints what it found and then asserts it. A check records a
labelled pass or fail. The run exits with a non-zero code if any check failed. The semantics
must be identical, because the project compares the check count of a stage across reruns. Also,
another tool can cross-check a topic.

Run the self-tests before you rely on the helpers:

    scripts/run symbolic/common/selftest_checks.wls
    scripts/run symbolic/common/selftest_checks.py
