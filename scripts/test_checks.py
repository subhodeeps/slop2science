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

print("toolchain — the default profile is mentioned wherever the language rule is stated")

ASK_RE = re.compile(r"stop\s+and\s+ask|never\s+(?:pick|choose|invent)|not\s+yours\s+to\s+choose|"
                    r"question\s+for\s+the\s+PI|not\s+(?:pick|choose)\s|never\s+a\s+choice", re.I)
LANG_RE = re.compile(r"\blanguage\b|\bowner\b|\bownership\b", re.I)


def default_profile_violations(files):
    """Files with a paragraph that says to ask about / never choose a language or tool owner,
    in a file that never mentions the default profile.

    Eleven files once said Claude must stop and ask which language to use. Adding a default
    profile made every one of them a contradiction. The profile is defined once, in
    docs/toolchain.md; any file that states the language rule has to acknowledge it.
    """
    bad = []
    for path, text in files.items():
        if "default profile" in text.lower():
            continue
        if any(ASK_RE.search(par) and LANG_RE.search(par) for par in re.split(r"\n\s*\n", text)):
            bad.append(path)
    return sorted(bad)


expect("'stop and ask which language' with no mention of the default profile is flagged",
       default_profile_violations({"x.md": "Which language owns this? Stop and ask the PI."}), ["x.md"])
expect("the same paragraph in a file that names the default profile is fine",
       default_profile_violations({"x.md": "Stop and ask the PI which language.\n\nSee the default profile."}), [])
expect("a paragraph about asking that is not about a language or owner is not flagged",
       default_profile_violations({"x.md": "If two sources disagree, never pick one: stop and ask."}), [])
real = {f: (cd.ROOT / f).read_text(encoding="utf-8", errors="replace") for f in cd.tracked("*.md")}
expect("every real file that states the language rule acknowledges the default profile",
       default_profile_violations(real), [])
expect("docs/toolchain.md defines the profile by kind of work",
       all(s in real["docs/toolchain.md"] for s in ("## Default profile", "**Algebra**", "**Numerics**",
                                                    "Python ecosystem")), True)

print("language rule (ASD-STE100) — the requirement reaches every session, agent and skill")

R = ROOT
ste_spec = importlib.util.spec_from_file_location("check_ste", R / "scripts" / "check_ste.py")
ste = importlib.util.module_from_spec(ste_spec)
ste_spec.loader.exec_module(ste)


def ste_hits(markdown):
    return [h for _, h in ste.judge(ste.md_blocks(markdown))]


expect("the screen flags a modal verb, a semicolon and a long sentence",
       len(ste_hits("Do not do this; you should stop. " + "word " * 30 + ".\n")) >= 3, True)
expect("the screen skips code blocks, quoted text, tables and headings",
       ste_hits("# You should\n\n```\nyou should; may\n```\n\n| a may |\n|---|\n\nSee \"it may be\" here.\n"), [])
expect("the screen skips the when_to_use trigger phrases of a skill",
       ste_hits("---\nname: x\nwhen_to_use: 'could; should; may'\n---\n\nBody text.\n"), [])

charter = (R / "CLAUDE.md").read_text(encoding="utf-8")
rule_text = (R / ".claude/rules/communication.md").read_text(encoding="utf-8")
expect("CLAUDE.md states the requirement and points to the rule",
       "ASD-STE100" in charter and ".claude/rules/communication.md" in charter, True)
expect("the rule file exists and has no paths: limit, so it loads in every session",
       "paths:" not in rule_text.split("# Communication", 1)[0], True)
expect("the rule covers code comments, docstrings, commit messages and handoffs",
       all(w in rule_text for w in ("code comments and docstrings", "commit messages", "handoffs")), True)
expect("the rule excludes executable code, notation and quoted text",
       all(w in rule_text for w in ("Executable code", "Mathematical notation", "Quoted text")), True)
agents = sorted((R / ".claude/agents").glob("*.md"))
expect("every agent names the rule in its own instructions",
       [a.name for a in agents if "communication.md" not in a.read_text(encoding="utf-8")], [])
expect("at least one agent exists (the check above is not vacuous)", len(agents) >= 7, True)
expect("the SessionStart hook repeats the requirement",
       "ASD-STE100" in (R / ".claude/hooks/session_context.sh").read_text(encoding="utf-8"), True)
expect("the skills README states that every skill inherits the rule",
       "inherits the language rule" in (R / ".claude/skills/README.md").read_text(encoding="utf-8"), True)

print("instruction loading — what loads at startup is small and listed")

load = cd.startup_load()
expect("the startup load is the charter, its two imports and the one rule without a paths: limit",
       sorted(load["files"]), sorted(["CLAUDE.md", "docs/STATUS.md", "docs/conventions.md",
                                      ".claude/rules/communication.md"]))
expect("the charter is under 200 lines", load["files"]["CLAUDE.md"] < 200, True)
expect("the startup total is within its budget", load["total"] <= cd.STARTUP_BUDGET, True)

print("toolchain — the default-profile assignment has one owner")

PROFILE_OWNERS = {"docs/toolchain.md", "README.md"}   # the owner, and the human overview
PROFILE_RE = re.compile(r"algebra[^.\n]{0,80}mathematica|mathematica\s+(?:does|for)\s+algebra|"
                        r"numerics[^.\n]{0,40}julia", re.I)


def profile_restated(files):
    """Files, other than the owner and the overview, that restate which tool the default profile
    gives to algebra and to numerics. About eight files did, and one copy can drift."""
    return sorted(p for p, t in files.items()
                  if p not in PROFILE_OWNERS and not p.startswith("docs/prompts/")
                  and PROFILE_RE.search(" ".join(t.split())))


expect("a file that restates the assignment is flagged",
       profile_restated({"x.md": "Algebra goes to Mathematica and numerics goes to Julia."}), ["x.md"])
expect("the owner and the overview may state it",
       profile_restated({"docs/toolchain.md": "Algebra: Mathematica.", "README.md": "Mathematica does algebra."}), [])
expect("a pointer to the registry is fine",
       profile_restated({"x.md": "The registry in docs/toolchain.md names the owner tool."}), [])
expect("no other real file restates the assignment", profile_restated(real), [])

print("derivation write-ups — every statement of the 'no citable check' rule has the same exception")


def rule_without_exception(files):
    """Files that say an equation with no citable check stays out, without the exception for
    algebra by hand between two checked expressions. The agent and the skill once disagreed."""
    return sorted(p for p, t in files.items()
                  if re.search(r"no\s+citable\s+check|has\s+no\s+check", t, re.I)
                  and not re.search(r"algebra\s+by\s+hand|by\s+hand\s+between", t, re.I))


expect("a statement of the rule without the exception is flagged",
       rule_without_exception({"x.md": "If an equation has no citable check, leave it out."}), ["x.md"])
expect("the same statement with the exception is fine",
       rule_without_exception({"x.md": "No citable check: leave it out, except algebra by hand."}), [])
expect("'by hand' in an unrelated sentence does not count as the exception",
       rule_without_exception({"x.md": "No citable check: leave it out. Never copy by hand."}), ["x.md"])
expect("every real file that states the rule also states the exception",
       rule_without_exception(real), [])

print("models — the model in each file matches the table in .claude/models.md")


def table_models():
    """{name: model} from the rows of the table in .claude/models.md that name a backticked model."""
    out = {}
    for m in re.finditer(r"^\|\s*`([\w-]+)`\s*\|\s*`(\w+)`\s*\|", (R / ".claude/models.md").read_text(encoding="utf-8"), re.M):
        out[m.group(1)] = m.group(2)
    return out


def frontmatter_model(path):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^model:\s*(\S+)", text.split("---", 2)[1], re.M) if text.startswith("---") else None
    return m.group(1) if m else None


table = table_models()
declared = {a.stem: frontmatter_model(a) for a in agents}
declared["session-close"] = frontmatter_model(R / ".claude/skills/session-close/SKILL.md")
expect("every agent and the session-close skill has the model that the table gives",
       {k: v for k, v in declared.items() if table.get(k) != v}, {})
expect("the table covers every agent (the check above is not vacuous)",
       sorted(set(declared) - set(table)), [])

print("tools — the tools and hooks table in .claude/models.md matches the frontmatter")


def table_tools():
    """{agent: (tools, hooks)} from the tools table in .claude/models.md."""
    text = (R / ".claude/models.md").read_text(encoding="utf-8")
    section = text.split("## Tools and hooks of each agent", 1)[-1]
    out = {}
    for m in re.finditer(r"^\|\s*`([\w-]+)`\s*\|([^|]*)\|([^|]*)\|", section, re.M):
        tools = frozenset(t.strip() for t in m.group(2).split(",") if t.strip())
        hooks = frozenset(re.findall(r"[\w]+\.py", m.group(3)))
        out[m.group(1)] = (tools, hooks)
    return out


def frontmatter_tools(path):
    front = path.read_text(encoding="utf-8").split("---", 2)[1]
    m = re.search(r"^tools:\s*(.+)$", front, re.M)
    tools = frozenset(t.strip() for t in m.group(1).split(",")) if m else frozenset()
    return tools, frozenset(re.findall(r"hooks/([\w]+\.py)", front))


ttable = table_tools()
expect("the tools table has one row for each agent", sorted(ttable), sorted(a.stem for a in agents))
expect("the tools and hooks of each agent match its frontmatter",
       sorted(a.stem for a in agents if ttable.get(a.stem) != frontmatter_tools(a)), [])
expect("the verification agent has Write (it must write its audit report)",
       "Write" in frontmatter_tools(R / ".claude/agents/verification.md")[0], True)

print("charter — the numbered sections have no gap")

nums = [int(m.group(1)) for m in re.finditer(r"^## (\d+)[a-z]?\.", charter, re.M)]
expect("CLAUDE.md section numbers run 1, 2, 3 ... with no gap",
       sorted(set(nums)), list(range(1, max(nums) + 1)))

print("guard config — every entry is well formed and every entry blocks something")

sys.path.insert(0, str(R / ".claude/hooks"))
import json
import guard_paths as gp

guard_cfg = gp.load_config(str(R))
expect("guard_paths.json loads (a broken file would make the guard allow everything)",
       guard_cfg is not None, True)
entries = [(k, e) for k in ("readonly", "append_only") for e in (guard_cfg or {}).get(k, [])]
expect("every entry has a non-empty glob and a reason",
       [e.get("glob") for k, e in entries if not e.get("glob") or not e.get("reason")], [])


def sample(glob):
    """A path that the glob must match."""
    return glob.replace("**", "x/y").replace("*", "x").replace("?", "x")


expect("every glob matches its own sample path (a typo in a glob matches nothing)",
       [e["glob"] for k, e in entries if not e["_re"].match(sample(e["glob"]))], [])
readonly_res = [e["_re"] for e in (guard_cfg or {}).get("readonly", [])]
expect("every readonly_exempt path falls under a readonly glob (an exemption of nothing is a typo)",
       [x for x in (guard_cfg or {}).get("readonly_exempt", [])
        if not any(r.match(x) for r in readonly_res)], [])

print("verifier claim — no file says that the verifier cannot change project files without the limit")

UNQUALIFIED = re.compile(
    r"cannot\s+(?:edit|change|write|modify)\s+(?:any\s+|the\s+)?project\s+files", re.I)


def unqualified_verifier_claims(files):
    """Files that claim the verifier cannot change project files. The hook covers Edit and Write
    only, so the true claim names those tools."""
    return sorted(n for n, t in files.items() if UNQUALIFIED.search(" ".join(t.split())))


expect("the claim without the tool names is flagged",
       unqualified_verifier_claims({"x.md": "The verifier cannot edit project files."}), ["x.md"])
expect("the claim that names Edit and Write is fine",
       unqualified_verifier_claims({"x.md": "It cannot use `Edit` or `Write` on project files."}), [])
old_text = {"README.md": "The verifier sees only the artifact. It cannot change project files. It"}
expect("the old README text is flagged",
       unqualified_verifier_claims(old_text), ["README.md"])
expect("no real file makes the unqualified claim",
       unqualified_verifier_claims({str(p.relative_to(R)): p.read_text(encoding="utf-8")
                                    for p in R.rglob("*.md") if ".git" not in p.parts
                                    and "docs/failure_modes" not in str(p)}), [])

print("guard files — a change to the guards needs approval")

settings = json.loads((R / ".claude/settings.json").read_text(encoding="utf-8"))
ask = settings.get("permissions", {}).get("ask", [])
for guarded in (".claude/guard_paths.json", ".claude/settings.json", ".claude/hooks/guard_paths.py",
                ".claude/hooks/subagent_git_guard.py", ".claude/hooks/readonly_agent.py",
                ".claude/agents/verification.md"):
    covered = any(a.startswith("Edit(/") and
                  gp.glob_to_regex(a[len("Edit(/"):-1]).match(guarded) for a in ask)
    expect(f"an ask rule covers {guarded}", covered, True)

print(f"\nchecks: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
