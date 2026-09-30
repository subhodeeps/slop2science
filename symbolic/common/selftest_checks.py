#!/usr/bin/env python3
"""Self-test for symbolic/common/checks.py.

Run:  scripts/run symbolic/common/selftest_checks.py

Checks that the helpers do what stages rely on: pass when they should, fail when they should,
print in every case, and report a correct tally. A check helper that silently always passes
would make every stage in the project vacuous, so this runs before anything relies on it.
"""
import io
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks  # noqa: E402

failures = []


def expect(description, condition):
    print(f"  [{'PASS' if condition else 'FAIL'}] {description}")
    if not condition:
        failures.append(description)


print("=== selftest: symbolic/common/checks.py ===")

buf = io.StringIO()
with redirect_stdout(buf):
    ok_zero = checks.check_zero("zero passes", 0)
    bad_zero = checks.check_zero("nonzero fails", 3)
    ok_eq = checks.check_equal("equal passes", 7, 7)
    bad_eq = checks.check_equal("unequal fails", 7, 8)
    ok_true = checks.check_true("true passes", True)
    bad_true = checks.check_true("false fails", False)
    ok_num = checks.check_numeric("within tolerance passes", 1.0, 1.0 + 1e-14)
    bad_num = checks.check_numeric("outside tolerance fails", 1.0, 1.5)
out = buf.getvalue()

expect("check_zero(0) passes", ok_zero is True)
expect("check_zero(3) fails", bad_zero is False)
expect("check_equal(7,7) passes", ok_eq is True)
expect("check_equal(7,8) fails", bad_eq is False)
expect("check_true(True) passes", ok_true is True)
expect("check_true(False) fails", bad_true is False)
expect("check_numeric within tol passes", ok_num is True)
expect("check_numeric outside tol fails", bad_num is False)

expect("every check printed its value", out.count("->") == 8)
expect("a failing check prints the value it found", "3" in out and "[FAIL]" in out)
expect("tally counted 4 passes", checks._passed == 4)
expect("tally counted 4 failures", checks._failed == 4)

buf2 = io.StringIO()
with redirect_stdout(buf2):
    checks.report_checks(exit_on_failure=False)
expect("report_checks prints the tally", "4 passed, 4 failed" in buf2.getvalue())
expect("report_checks names the failed labels", "nonzero fails" in buf2.getvalue())

print(f"--- selftest: {8 + 6 - len(failures)} passed, {len(failures)} failed")
if failures:
    print(f"--- failed: {failures}")
    sys.exit(1)
