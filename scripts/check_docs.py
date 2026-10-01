#!/usr/bin/env python3
"""Repository documentation and evidence checks. One file, three checks, one allow list.

    scripts/check_docs.py refs       every path cited in prose still resolves
    scripts/check_docs.py evidence   every [E: file, "label"] tag cites a label that exists
    scripts/check_docs.py stale      ownership declared, records self-consistent, the
                                     every-session context budget, and write-ups not older
                                     than the scripts they cite (the last as a warning)
    scripts/check_docs.py init       fail while {{PLACEHOLDERS}} remain (uninitialized)
    scripts/check_docs.py all        all three

Why this exists. A write-up whose cited script was renamed, or a claim whose check label was
re-worded, breaks the evidence chain silently: nothing fails at run time, and the citation
still *looks* authoritative. These checks make that failure visible on every push.

What they CANNOT do. Every check here verifies that a reference *resolves* -- to a file, a
label, a column, a commit -- never that the statement built on it is *true*. A citation that
resolves cleanly to a real script whose check does not establish what the entry claims passes
every check here in full. That still needs a human reading the script, and the project this
template came from found that exact failure shape by hand (docs/failure_modes.md).

Allow list: scripts/check_docs.allow, lines of the form

    <citing file>: <target>      # why this is intentionally unresolved

for deliberate references to files that do not exist yet (planned work, user-local paths,
illustrative examples).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # for registry.py

ROOT = Path(__file__).resolve().parent.parent
ALLOWFILE = ROOT / "scripts" / "check_docs.allow"

# Historical documents describe the repository as it was when they were written, and are not
# expected to track renames. Prompt records in particular are a verbatim record.
EXCLUDE_PREFIX = ("docs/prompts/", "docs/status_history.md")
# Skills' reference and template files use generic example names on purpose.
GENERIC_PREFIX = (".claude/skills/",)

TOPLEVEL = ("docs", "scripts", "symbolic", "derivation", "src", "tests", "validation",
            "papers", "reports", "code", "notes", "data", "figures", "logs", ".claude",
            ".github")

PATH_TOKEN = re.compile(
    r"`((?:" + "|".join(re.escape(d) for d in TOPLEVEL) + r")/[A-Za-z0-9_./*-]*)`")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)")
BARE_FILE = re.compile(r"`((?:stage|export|check|selftest)_[A-Za-z0-9_]+\.(?:wls|wl|jl|py))`")
EVIDENCE = re.compile(r"\[E:\s*(.+?)\]", re.S)


def git(*args):
    try:
        out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                             text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
    return out


def tracked(*globs):
    files = git("ls-files", *globs).splitlines()
    return [f for f in files if f and not f.startswith(EXCLUDE_PREFIX)]


def load_allow():
    allow = set()
    if ALLOWFILE.exists():
        for line in ALLOWFILE.read_text(encoding="utf-8").splitlines():
            line = re.sub(r"\s*#.*$", "", line).strip()
            if line:
                allow.add(line)
    return allow


def skill_root(rel):
    parts = rel.split("/")
    if len(parts) >= 3 and parts[0] == ".claude" and parts[1] == "skills":
        return "/".join(parts[:3])
    return None


_CLONE_VIEW = None


def clone_view():
    """(files, dirs): what a fresh clone would contain if everything not ignored were committed.

    `git ls-files --cached --others --exclude-standard` is tracked files plus untracked files
    that are NOT gitignored. That is deliberately not "what exists on disk": a working tree
    accumulates ignored files (logs/, a fetched source tree, a local settings file) that a
    clone never has. Asking the filesystem is how a reference can resolve on the author's
    machine and fail in CI -- which happened (logs/), after the same shape had already been
    patched twice by hand-adding allow-list entries (data/raw/, papers/source/).
    """
    global _CLONE_VIEW
    if _CLONE_VIEW is None:
        files = {f for f in git("ls-files", "--cached", "--others",
                                "--exclude-standard").splitlines() if f}
        dirs = set()
        for f in files:
            parts = f.split("/")
            for i in range(1, len(parts)):
                dirs.add("/".join(parts[:i]))
        _CLONE_VIEW = (files, dirs)
    return _CLONE_VIEW


def declared_runtime_path(path):
    """True if .gitignore itself says this path is created at runtime, not committed.

    The answer depends only on the ignore patterns, never on whether the path exists, so it is
    identical on a laptop and in CI.

    Every ancestor is tested as an explicit directory (`papers/`, `papers/source/`, ...). That
    matters: for a path that does not exist, git cannot tell a directory from a file, and a
    directory-only pattern such as `papers/source/` or `logs/` matches only when given a
    trailing slash. Without this, `papers/source/<id>/ms.tex` resolved only on a machine where
    `papers/source/` had already been created -- the same local/CI split this function exists
    to remove, one level down.
    """
    parts = path.rstrip("/").split("/")
    candidates = ["/".join(parts[:i]) + "/" for i in range(1, len(parts))]
    candidates.append(path)
    # No -q: git rejects --quiet with more than one path (fatal, exit 128), which reads as
    # "not ignored" and silently turned every nested case into a false negative. Exit 0 means
    # at least one path is ignored, 1 none, anything else is an error and is not an answer.
    result = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "--", *candidates],
                            capture_output=True)
    return result.returncode == 0


def resolves(rel, target):
    """Does `target`, as cited from `rel`, resolve in a fresh clone?

    Tries repo-root, then citing-file-relative, then skill-root-relative.
    """
    files, dirs = clone_view()
    wants_dir = target.endswith("/")
    bases = ["", os.path.dirname(rel)]
    sr = skill_root(rel)
    if sr:
        bases.append(sr)
    for base in bases:
        path = os.path.normpath(os.path.join(base, target.rstrip("/"))).replace(os.sep, "/")
        if path.startswith(".."):
            continue
        if path in files and not wants_dir:
            return True
        if path in dirs:
            return True
        if declared_runtime_path(path + "/" if wants_dir else path):
            return True
    return False


# --- check: refs -------------------------------------------------------------------

def check_refs():
    allow, problems, checked = load_allow(), [], 0
    for rel in tracked("*.md", "*.csv"):
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        targets = set()
        for m in PATH_TOKEN.finditer(text):
            targets.add(m.group(1))
        for m in MD_LINK.finditer(text):
            t = m.group(1)
            if not re.match(r"^[a-z]+:", t) and not t.startswith("#"):
                targets.add(t)
        if not rel.startswith(GENERIC_PREFIX):
            for m in BARE_FILE.finditer(text):
                targets.add(m.group(1))
        for target in sorted(targets):
            target = target.rstrip(".,;:")
            if any(ch in target for ch in "*<>{}…") or not target:
                continue
            checked += 1
            if resolves(rel, target):
                continue
            if f"{rel}: {target}" in allow:
                continue
            problems.append(f"unresolved: {rel} -> {target}")
    for p in problems:
        print(p)
    print(f"check-refs: {checked} references checked, {len(problems)} unresolved")
    return len(problems)


# --- check: evidence ---------------------------------------------------------------

FENCED = re.compile(r"^```.*?^```", re.M | re.S)
INDENTED = re.compile(r"^(?: {4}|\t).*$", re.M)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


def strip_examples(text):
    """Remove code blocks and HTML comments.

    An [E: ...] tag inside a fenced block, an indented block or an HTML comment is showing
    the tag *syntax*, not making a claim -- every instructional file in this repository
    contains one. Scanning them would make the check cry wolf on its own documentation, and a
    check that cries wolf gets ignored.
    """
    text = FENCED.sub("", text)
    text = HTML_COMMENT.sub("", text)
    return INDENTED.sub("", text)


def check_evidence():
    """[E: `path`, "label", "label"] / [E: records `glob.json`, field `name`]

    Every quoted label must appear verbatim in one of the files named earlier in the same
    tag; every backticked bare word after a JSON glob must appear as a "word": key in a file
    the glob matches. Label presence only -- not that the check proves the claim.

    Skipped: `.claude/**` and `.github/**` (instructions and forms, which show the tag
    syntax by necessity), and any tag inside a code block or HTML comment anywhere (an
    example, not a claim).
    """
    allow, problems, checked = load_allow(), [], 0
    for rel in tracked("*.md"):
        if rel.startswith((".claude/", ".github/")):
            continue
        text = strip_examples((ROOT / rel).read_text(encoding="utf-8", errors="replace"))
        for m in EVIDENCE.finditer(text):
            body = re.sub(r"\s+", " ", m.group(1)).strip()
            files = re.findall(r"`([A-Za-z0-9_./*-]+\.(?:wls|wl|jl|py|m))`", body)
            globs = re.findall(r"`([A-Za-z0-9_./*-]+\.json)`", body)
            labels = re.findall(r'"([^"]+)"', body)
            fields = [w for w in re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", body)]

            haystack = ""
            for f in files:
                hits = sorted(ROOT.glob(f)) or sorted(ROOT.glob(f"**/{f}"))
                for h in hits[:8]:
                    haystack += h.read_text(encoding="utf-8", errors="replace")
            if files and not haystack:
                checked += 1
                if f"{rel}: {files[0]}" not in allow:
                    problems.append(f"evidence tag cites a file that does not exist: {rel} -> {files[0]}")
                continue
            for label in labels:
                checked += 1
                if label in haystack:
                    continue
                if f"{rel}: {label}" in allow:
                    continue
                problems.append(f'evidence label not found in the cited file(s): {rel} -> "{label}"')

            for g in globs:
                matches = sorted(ROOT.glob(g)) or sorted(ROOT.glob(f"**/{g}"))
                keys = set()
                for path in matches[:20]:
                    try:
                        obj = json.loads(path.read_text(encoding="utf-8"))
                    except Exception:
                        continue
                    if isinstance(obj, dict):
                        keys |= set(obj.keys())
                for field in fields:
                    checked += 1
                    if field in keys:
                        continue
                    if f"{rel}: {field}" in allow:
                        continue
                    problems.append(f"evidence tag cites JSON field `{field}` absent from {g}: {rel}")
    for p in problems:
        print(p)
    print(f"check-evidence: {checked} evidence items checked, {len(problems)} unresolved")
    return len(problems)


# --- check: stale ------------------------------------------------------------------

STARTUP_BUDGET = 400


def startup_load():
    """Files that load into every session, with their line counts.

    The charter, each `@path` import in it, and each rule file without a `paths:` limit in its
    frontmatter. Skills, agents and path-scoped rules load on demand and are not counted.
    """
    files = {}

    def count(rel):
        path = ROOT / rel
        if path.exists():
            files[rel] = len(path.read_text(encoding="utf-8", errors="replace").splitlines())

    count("CLAUDE.md")
    charter = ROOT / "CLAUDE.md"
    if charter.exists():
        for m in re.finditer(r"^@(\S+)\s*$", charter.read_text(encoding="utf-8", errors="replace"), re.M):
            count(m.group(1))
    for rule in sorted((ROOT / ".claude" / "rules").glob("*.md")):
        text = rule.read_text(encoding="utf-8", errors="replace")
        front = text.split("---", 2)[1] if text.startswith("---") else ""
        if "paths:" not in front:
            count(rule.relative_to(ROOT).as_posix())
    return {"files": files, "total": sum(files.values())}


def check_stale():
    errors, warnings = [], []

    # 1. Tool ownership must be declared for every topic that has stage scripts.
    registry = ""
    tc = ROOT / "docs" / "toolchain.md"
    if tc.exists():
        registry = tc.read_text(encoding="utf-8", errors="replace")
    for topic_dir in sorted((ROOT / "symbolic").glob("*")):
        if not topic_dir.is_dir() or topic_dir.name in ("common", "generated"):
            continue
        topic = topic_dir.name
        stages = list(topic_dir.glob("stage_*")) + list(topic_dir.glob("export_*"))
        if not stages:
            continue
        if not (topic_dir / "stages.txt").exists():
            errors.append(f"symbolic/{topic}/ has stage scripts but no stages.txt manifest "
                          f"(order would fall back to glob order; see docs/failure_modes.md)")
        if topic not in registry:
            errors.append(f"symbolic/{topic}/ has stage scripts but topic '{topic}' is not in "
                          f"the ownership registry in docs/toolchain.md (CLAUDE.md §5)")

    # 2. Result records must not claim acceptance while flagging themselves.
    for path in sorted(ROOT.glob("validation/**/records/*.json")):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: not valid JSON ({exc})")
            continue
        if not isinstance(obj, dict):
            continue
        rel = path.relative_to(ROOT)
        if obj.get("status") == "accepted":
            for key, val in obj.items():
                if key.lower().endswith("flag") and val is True:
                    errors.append(f'{rel}: status "accepted" while {key} is true')
        missing = [k for k in ("status", "kind", "judged_against", "git") if k not in obj]
        if missing:
            errors.append(f"{rel}: record is missing required provenance field(s): "
                          f"{', '.join(missing)} (docs/validation_protocol.md §12)")

    # 3. Benchmark CSV provenance headers must cite their own columns.
    for path in sorted(ROOT.glob("validation/benchmarks/*.csv")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        header = next((l for l in lines if l and not l.lstrip().startswith("#")), "")
        columns = {c.strip().strip('"') for c in header.split(",")}
        prose = "\n".join(l for l in lines if l.lstrip().startswith("#"))
        for m in re.finditer(r"(?:column|field)s?\s+`([A-Za-z0-9_]+)`", prose):
            if m.group(1) not in columns:
                errors.append(f"{path.relative_to(ROOT)}: provenance header cites column "
                              f"`{m.group(1)}`, which is not one of its own columns")

    # 4. Context budget: the files that load into EVERY session.
    #    These have a stated size discipline because their cost is paid on every prompt, and
    #    they grow by accretion -- the project this template came from let its status file
    #    reach 504 lines of history before anyone measured it (docs/failure_modes.md entry 10).
    #    An ERROR, not a warning: a budget that only warns is a budget that is ignored until
    #    the file is 500 lines of history (docs/failure_modes.md entry 10). Going over means
    #    move detail into a skill, a rule or a referenced doc -- not trim wording.
    BUDGETS = {"CLAUDE.md": 199, "docs/STATUS.md": 100, "docs/conventions.md": 60,
               ".claude/rules/communication.md": 70}
    for rel, budget in BUDGETS.items():
        path = ROOT / rel
        if not path.exists():
            continue
        lines = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if lines > budget:
            errors.append(
                f"{rel}: {lines} lines, over its {budget}-line context budget. This file "
                f"loads into every session. Move detail into a skill, a rule, or a "
                f"referenced doc; do not compress the wording.")

    # 4b. What loads at startup, in total: the charter, the files that it imports with @, and
    #     each rule that has no paths: limit. An import moves text out of the charter into the
    #     same context, so the budget counts the sum and not only the charter.
    startup = startup_load()
    if startup["total"] > STARTUP_BUDGET:
        detail = ", ".join(f"{k}: {v}" for k, v in startup["files"].items())
        errors.append(
            f"startup load is {startup['total']} lines, over the {STARTUP_BUDGET}-line budget "
            f"({detail}). Move detail into an on-demand skill or a path-scoped rule. Do not "
            f"move it into an @ import.")

    # 5. Sources imported from a catalogue are written `verified: false`. Catalogue metadata
    #    can be wrong (a mislabelled entry, a snapshot standing in for the paper), and the
    #    bibliography rule is that identifiers are never taken on trust. A warning, not an
    #    error: the aim is that the count is visible, not that an import blocks the build.
    try:
        import registry
        unverified = [e.get("label") for e in registry.parse_sources(ROOT / "papers" / "sources.yaml")
                      if e.get("verified") == "false"]
    except Exception as exc:                     # a malformed registry is its own finding
        unverified = []
        errors.append(f"papers/sources.yaml cannot be parsed: {exc}")
    if unverified:
        shown = ", ".join(unverified[:5]) + (" ..." if len(unverified) > 5 else "")
        warnings.append(f"WARNING unverified: {len(unverified)} source(s) in papers/sources.yaml "
                        f"still `verified: false` ({shown}). Check each one's identifiers and file "
                        "against the document's own first page, then set `verified: true`.")

    # 6. Warnings: a write-up older than a script it cites.
    def last_commit(rel):
        out = git("log", "-1", "--format=%ct", "--", rel).strip()
        return int(out) if out.isdigit() else 0

    for rel in tracked("derivation/**/*.md", "reports/*.md"):
        doc_time = last_commit(rel)
        if not doc_time:
            continue
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        for m in PATH_TOKEN.finditer(text):
            target = m.group(1)
            if not target.startswith("symbolic/") or not (ROOT / target).exists():
                continue
            if last_commit(target) > doc_time:
                warnings.append(f"WARNING stale: {rel} was last committed before "
                                f"{target}, which it cites")
                break

    for e in errors:
        print(e)
    for w in sorted(set(warnings)):
        print(w)
    print(f"check-docs: {len(errors)} error(s), {len(set(warnings))} staleness warning(s) "
          f"(warnings do not fail the build)")
    return len(errors)


def check_init():
    """Fail while {{PLACEHOLDERS}} remain outside the template's own documentation.

    Expected to FAIL in the template repository itself, and to pass in any project that has
    been through /init-paper. Excluded: the template's own docs, the init skill, and the three
    files whose job is to detect or mention placeholders (including this checker).
    """
    out = git("grep", "-l", "-E", r"\{\{[A-Z_]+\}\}", "--",
              ":!TEMPLATE_GUIDE.md", ":!README.md", ":!.claude/skills/init-paper/**",
              ":!.claude/hooks/session_context.sh", ":!.github/workflows/checks.yml",
              ":!scripts/check_docs.py", ":!Makefile")
    hits = [line for line in out.splitlines() if line.strip()]
    for hit in hits:
        print(f"uninitialized placeholders: {hit}")
    if hits:
        print("check-init: run /init-paper in a Claude Code session "
              "(expected to fail in the template repository itself)")
    else:
        print("check-init: no placeholders outside the template's own documentation")
    return len(hits)


CHECKS = {"refs": check_refs, "evidence": check_evidence, "stale": check_stale,
          "init": check_init}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    names = list(CHECKS) if which == "all" else [which]
    if any(n not in CHECKS for n in names):
        print(f"usage: check_docs.py [{'|'.join(CHECKS)}|all]", file=sys.stderr)
        return 64
    return 1 if sum(CHECKS[n]() for n in names) else 0


if __name__ == "__main__":
    sys.exit(main())
