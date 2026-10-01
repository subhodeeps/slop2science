#!/usr/bin/env python3
"""Self-test for scripts/check_docs.py's reference resolution.

    scripts/py scripts/test_checks.py        (also: make test-checks, part of make check)

The point of this file is one regression. `check-refs` once asked the filesystem whether a
cited path existed. A working tree holds ignored files a clone never has -- logs/, a fetched
source tree, a local settings file -- so a reference could resolve on the author's machine and
fail in CI. It did (`logs/`), after the same shape had been patched twice by hand-adding
allow-list entries. The resolver now answers for a *clone*, and these cases pin that down.

Each case states the answer a clean clone would give, so the suite means the same thing on a
laptop that has accumulated runtime files and in CI that has none.
"""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_docs", ROOT / "scripts" / "check_docs.py")
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)

passed = failed = 0


def expect(description, got, want):
    global passed, failed
    ok = got == want
    passed += ok
    failed += not ok
    print(f"  {'ok  ' if ok else 'FAIL'} {description}"
          + ("" if ok else f"  (got {got}, wanted {want})"))


def fresh():
    cd._CLONE_VIEW = None          # forget the cached view of the tree


print("check_docs.py — reference resolution answers for a clone")

fresh()
expect("a tracked file resolves", cd.resolves("README.md", "docs/GUIDE.md"), True)
expect("a tracked directory resolves", cd.resolves("README.md", "docs/"), True)
expect("a directory cited without a slash resolves", cd.resolves("README.md", "docs"), True)
expect("a file that is not there does not resolve",
       cd.resolves("README.md", "docs/does_not_exist.md"), False)
expect("a file under a directory that is not there does not resolve",
       cd.resolves("README.md", "docs/_no_such_dir/x.md"), False)
expect("a typo in a real directory does not resolve",
       cd.resolves("README.md", "docs/GUDE.md"), False)

print("check_docs.py — gitignored runtime paths (the logs/ regression)")
expect("logs/ resolves: .gitignore declares it runtime-created",
       cd.resolves(".claude/skills/toolchain/SKILL.md", "logs/"), True)
expect("a path under an ignored directory resolves",
       cd.resolves("README.md", "papers/source/2504.01234v2/ms.tex"), True)
expect("a gitignored settings file resolves",
       cd.resolves("README.md", ".claude/settings.local.json"), True)

# The decisive case: the answer must not depend on what happens to exist on this machine.
logs = ROOT / "logs"
probe = logs / "_probe.txt"
logs.mkdir(exist_ok=True)
probe.write_text("x")
fresh()
with_logs = cd.resolves("README.md", "logs/")
fresh()
expect("answer is the same with an ignored logs/ present...", with_logs, True)
probe.unlink()
fresh()
expect("...as without its contents (what a clone sees)", cd.resolves("README.md", "logs/"), True)

print("check_docs.py — untracked but not ignored counts, as a clone would after `git add`")
untracked = ROOT / "docs" / "_untracked_probe.md"
untracked.write_text("probe")
try:
    fresh()
    expect("a new, not-yet-added file resolves", cd.resolves("README.md",
           "docs/_untracked_probe.md"), True)
finally:
    untracked.unlink()
fresh()
expect("and stops resolving once it is gone",
       cd.resolves("README.md", "docs/_untracked_probe.md"), False)

print("check_docs.py — relative resolution still works")
expect("citing-file-relative resolves",
       cd.resolves("docs/GUIDE.md", "WORKFLOW.md"), True)
expect("skill-root-relative resolves",
       cd.resolves(".claude/skills/literature-audit/SKILL.md", "reference/corpus.md"), True)
expect("a path escaping the repository does not resolve",
       cd.resolves("README.md", "../../etc/passwd"), False)

print(f"\nchecks: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
