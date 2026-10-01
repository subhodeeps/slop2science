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
import re
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

print("check_docs.py — sources imported from a catalogue stay visible until verified")
import contextlib, io, tempfile      # noqa: E402
import registry                       # noqa: E402


def stale_output(root):
    saved = cd.ROOT
    cd.ROOT = root
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            errors = cd.check_stale()
    finally:
        cd.ROOT = saved
    return errors, buf.getvalue()


tmp = Path(tempfile.mkdtemp(prefix="stale."))
(tmp / "papers").mkdir()
reg = tmp / "papers" / "sources.yaml"
reg.write_text("sources:\n")
registry.append_source("Imported_1", [("verified", False)], reg)
registry.append_source("Imported_2", [("verified", False)], reg)
registry.append_source("Checked_3", [("verified", True)], reg)
errors, out = stale_output(tmp)
expect("two unverified sources produce a warning naming the count", "2 source(s)" in out
       and "verified: false" in out, True)
expect("the verified one is not counted", "Checked_3" not in out, True)
expect("a warning does not fail the build", errors, 0)

reg.write_text("sources:\n  - label: Broken\n  this line is not valid\n")
errors, out = stale_output(tmp)
expect("a registry the tools cannot parse is an ERROR, not a silent skip", errors >= 1
       and "cannot be parsed" in out, True)
import shutil                          # noqa: E402
shutil.rmtree(tmp, ignore_errors=True)

print("reading order — stated once, pointed at everywhere else")

READING_RE = re.compile(r"rendered page|page image|text layer|text-layer|\bOCR\b", re.I)
OWNER = ".claude/skills/literature-audit/reference/corpus.md"
# Narrative mentions, not instructions: a worked example that happens to say "text layer".
NARRATIVE = {"docs/handoff_guide.md"}


def reading_order_violations(files):
    """Files that tell the reader how to read a PDF but never point at the one owner of the order.

    Seven files once said "read the rendered page" with no mention of the LaTeX source, because
    the order had been restated instead of pointed at. The order lives in corpus.md; anything
    else that mentions reading a rendered page must say where the order is stated.
    """
    return sorted(path for path, text in files.items()
                  if path != OWNER and path not in NARRATIVE
                  and READING_RE.search(text) and "corpus.md" not in text)


expect("a file that says 'read the rendered page' and never points at corpus.md is flagged",
       reading_order_violations({"x.md": "Read the rendered page, not the text layer."}), ["x.md"])
expect("the same sentence with a pointer is fine",
       reading_order_violations({"x.md": "Read the rendered page (see reference/corpus.md)."}), [])
expect("a file that never mentions reading a PDF is not flagged",
       reading_order_violations({"x.md": "Nothing to see here."}), [])
expect("the owner itself is exempt", reading_order_violations({OWNER: "rendered page"}), [])
expect("a narrative mention is exempt", reading_order_violations(
       {"docs/handoff_guide.md": "I lost an hour on the PDF text layer."}), [])
real = {f: (cd.ROOT / f).read_text(encoding="utf-8", errors="replace") for f in cd.tracked("*.md")}
expect("every real file that mentions it points at corpus.md",
       reading_order_violations(real), [])
expect("corpus.md leads with the .tex, and puts the text layer last",
       (lambda s: s.index(".tex") < s.index("rendered PDF") < s.index("text layer"))(
           real[OWNER].split("## The reading order, stated once", 1)[1]), True)

print(f"\nchecks: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
