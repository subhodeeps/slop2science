#!/usr/bin/env python3
"""Fail if a Python plotting script does not use the amore plot style.

    scripts/check_plots.py          check each tracked or new .py file (make check-plots)

A file that imports matplotlib must import `amore` and call `<name>.use()`, and it must not
contain a hard-coded hex colour: colours come from `amore.palette()` and `amore.cmap()`.
The amore package itself, tests/ and scripts/ are exempt.

What it cannot do: it reads source text. It does not run the script, so it cannot see a
figure that looks wrong. It does not check notebooks, Julia or Mathematica plots. The
`plotting` skill asks Claude to read each rendered figure for that reason.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXEMPT = ("src/python/amore/", "tests/", "scripts/", ".claude/")
USES_MPL = re.compile(r"^\s*(?:import|from)\s+matplotlib\b", re.M)
IMPORTS_AMORE = re.compile(r"^\s*import\s+amore(?:\s+as\s+(\w+))?\s*$", re.M)
HEX = re.compile(r"""["']#[0-9a-fA-F]{6}["']""")


def violations(text):
    """The reasons why one source file breaks the rule (an empty list if it does not)."""
    if not USES_MPL.search(text):
        return []
    out = []
    m = IMPORTS_AMORE.search(text)
    name = (m.group(1) or "amore") if m else None
    if name is None or not re.search(rf"\b{name}\.use\(\)", text):
        out.append("imports matplotlib but does not import amore and call amore.use()")
    if HEX.search(text):
        out.append("hard-codes a hex colour; take colours from amore.palette() or amore.cmap()")
    return out


def files():
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached", "--others",
                          "--exclude-standard", "*.py"], capture_output=True, text=True).stdout
    return [f for f in out.split() if not f.startswith(EXEMPT)]


def main():
    bad = 0
    checked = files()
    for f in checked:
        for reason in violations((ROOT / f).read_text(encoding="utf-8", errors="replace")):
            print(f"{f}: {reason}")
            bad += 1
    print(f"check-plots: {len(checked)} Python files checked, {bad} violation(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
