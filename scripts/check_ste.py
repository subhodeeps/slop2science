#!/usr/bin/env python3
"""Screen text for the measurable ASD-STE100 writing rules.

Checks sentence length (over 25 words), modal verbs (should, may, might, could), filler words,
contractions, semicolons and passive voice. It does NOT check the STE Dictionary and it cannot
certify compliance: a person must review the result.

Skipped, because the rule does not apply to them: fenced and inline code, tables, headings,
block quotes, text inside double quotes, HTML comments, indented blocks, and the `when_to_use`
trigger phrases of a skill.

  scripts/py scripts/check_ste.py [--strict] [FILE...]        Markdown (default: every tracked *.md)
  scripts/py scripts/check_ste.py --code [--strict] [FILE...] comments and docstrings in code
                                                              (default: every tracked *.py *.sh *.jl *.wl *.wls)
  SHOW=10 scripts/py scripts/check_ste.py FILE                print the first 10 hits per file
  --quiet                                                     print only files that have hits, and the total

Exit 0 unless --strict is given and a hit exists.
"""
import ast
import io
import os
import re
import subprocess
import sys
import tokenize

FLUFF = r"\b(simply|just|very|really|basically|essentially|quite|rather|perhaps|maybe|actually|obviously|clearly|etc|e\.g\.|i\.e\.|thus|hence|whilst|utilis\w+|utiliz\w+|leverag\w+)\b"
MODAL = r"\b(should|may|might|could|ought)\b"
CONTR = r"\b\w+n't\b|\b(it|that|there|here|let|we|you|they)'(s|ll|re|ve|d)\b"
PASSIVE = r"\b(is|are|was|were|be|been|being)\s+(\w+ed|written|made|done|run|given|taken|shown|kept|held|built|known|seen)\b"
RULES = (("fluff", FLUFF), ("modal", MODAL), ("contraction", CONTR), ("passive", PASSIVE))
MAX_WORDS = 25


def clean(text):
    """Remove what the rule does not cover: links, inline code, quoted text, emphasis marks."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`[^`]*`", "X", text)
    text = re.sub(r'"[^"]*"|“[^”]*”', "Q", text)
    return re.sub(r"\*+", "", text)


def md_blocks(text):
    """Markdown prose as (line number, paragraph text) pairs. List items are separate blocks."""
    lines, fence, comment = [], False, False
    front = text.startswith("---\n")
    for n, line in enumerate(text.splitlines(), 1):
        st = line.strip()
        if front:
            if n > 1 and st == "---":
                front = False
            elif st.startswith("description:"):
                lines += [(n, st.split(":", 1)[1].strip().strip("'\"")), (n, "")]
            continue
        if st.startswith("```"):
            fence = not fence
            lines.append((n, ""))
            continue
        if "<!--" in st and "-->" not in st:
            comment = True
            continue
        if comment:
            comment = "-->" not in st
            continue
        if fence or not st or st.startswith(("<!--", "---", "|", "#", ">")) or line.startswith("    "):
            if not fence:
                lines.append((n, ""))
            continue
        lines.append((n, line))
    blocks, para, start = [], [], 0
    for n, line in lines + [(10**9, "")]:
        item = bool(re.match(r"^\s*([-*]|\d+[.)])\s", line))
        if line.strip() and not item:
            if not para:
                start = n
            para.append(line.strip())
            continue
        if para:
            blocks.append((start, " ".join(para)))
            para = []
        if item:
            blocks.append((n, line.strip()))
    return blocks


def judge(blocks):
    """Hits for a list of (line number, text) blocks."""
    hits = []
    for n, text in blocks:
        c = clean(text)
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“`(])", c.strip()):
            w = len(s.split())
            if w > MAX_WORDS:
                hits.append((n, f"{w} words: {s[:70]}..."))
        for name, pat in RULES:
            for m in re.finditer(pat, c, re.I):
                hits.append((n, f"{name}: {m.group(0)}"))
        if ";" in c:
            hits.append((n, "semicolon"))
    return hits


def hash_blocks(text):
    """Line comments (`#`) of shell, Julia and Wolfram scripts, joined into paragraphs."""
    blocks, last, para, start = [], -5, [], 0
    for n, line in enumerate(text.splitlines(), 1):
        st = line.strip()
        if not st.startswith("#") or st.startswith("#!"):
            continue
        body = st.lstrip("#").strip()
        if n != last + 1 and para:
            blocks.append((start, " ".join(para)))
            para = []
        if not para:
            start = n
        if body:
            para.append(body)
        last = n
    if para:
        blocks.append((start, " ".join(para)))
    return blocks


def py_blocks(text):
    """Comments and docstrings of Python source, as (line number, paragraph text) pairs."""
    blocks, last, para, start = [], -5, [], 0
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError):
        toks = []
    for t in toks:
        if t.type != tokenize.COMMENT or t.string.startswith("#!"):
            continue
        body = t.string.lstrip("#").strip()
        if t.start[0] != last + 1 and para:
            blocks.append((start, " ".join(para)))
            para = []
        if not para:
            start = t.start[0]
        if body:
            para.append(body)
        last = t.start[0]
    if para:
        blocks.append((start, " ".join(para)))
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return blocks
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node, clean=True)
            if doc and node.body:
                for k, para_text in enumerate(re.split(r"\n\s*\n", doc)):
                    flat = " ".join(x.strip() for x in para_text.splitlines() if not x.startswith("    "))
                    if flat.strip():
                        blocks.append((node.body[0].lineno + k, flat))
    return blocks


def candidate_files(pats):
    """Tracked files, and new files that git does not ignore, that match the patterns.

    A new file must count: if the lint read only tracked files, a new file would pass
    `make check` before its commit and fail it after the commit.
    """
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", *pats],
                         capture_output=True, text=True, check=True).stdout.split()
    return sorted(f for f in set(out) if os.path.exists(f))


def main(argv):
    strict = "--strict" in argv
    code = "--code" in argv
    quiet = "--quiet" in argv
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        pats = ["*.py", "*.sh", "*.jl", "*.wl", "*.wls"] if code else ["*.md"]
        args = candidate_files(pats)
    show = int(os.environ.get("SHOW", "0"))
    total = 0
    for f in args:
        text = open(f, encoding="utf-8", errors="replace").read()
        if code:
            blocks = py_blocks(text) if f.endswith(".py") else hash_blocks(text)
        else:
            blocks = md_blocks(text)
        hits = sorted(judge(blocks))
        if hits or not quiet:
            print(f"{f}: {len(hits)}")
        for n, h in hits[:show or (5 if quiet and hits else 0)]:
            print(f"   {n}: {h}")
        total += len(hits)
    print("total", total)
    return 1 if strict and total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
