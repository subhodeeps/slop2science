#!/usr/bin/env python3
"""Screen Markdown files for the measurable ASD-STE100 writing rules.

Checks sentence length (over 25 words), modal verbs (should, may, might, could), filler
words, contractions, semicolons and passive voice. It does NOT check the STE Dictionary and it
cannot certify compliance: a person must review the result. Quoted text and code are skipped
where the tool can see them (fenced blocks, inline code, tables, headings).

  scripts/py scripts/check_ste.py [--strict] [FILE...]     # default: every tracked *.md
  SHOW=10 scripts/py scripts/check_ste.py FILE             # print the first 10 hits per file

Exit 0 unless --strict is given and a hit exists.
"""
import os, re, subprocess, sys

FLUFF = r"\b(simply|just|very|really|basically|essentially|quite|rather|perhaps|maybe|actually|obviously|clearly|etc|e\.g\.|i\.e\.|thus|hence|whilst|utilis\w+|utiliz\w+|leverag\w+)\b"
MODAL = r"\b(should|may|might|could|ought)\b"
CONTR = r"\b\w+n't\b|\b(it|that|there|here|let|we|you|they)'(s|ll|re|ve|d)\b"
PASSIVE = r"\b(is|are|was|were|be|been|being)\s+(\w+ed|written|made|done|run|given|taken|shown|kept|held|built|known|seen)\b"
def prose(text):
    """Lines of running prose: not code, tables, headings, quotes, comments or indented blocks."""
    out, fence, comment = [], False, False
    front = text.startswith("---\n")  # YAML frontmatter: check only description and when_to_use
    for n, line in enumerate(text.splitlines(), 1):
        st = line.strip()
        if front:
            if n > 1 and st == "---":
                front = False
            elif st.startswith(("description:", "when_to_use:")):
                out.append((n, st.split(":", 1)[1].strip().strip("'\"")))
                out.append((n, ""))
            continue
        if st.startswith("```"):
            fence = not fence
            out.append((n, ""))  # a code block ends the paragraph before it
            continue
        if "<!--" in st and "-->" not in st:
            comment = True
            continue
        if comment:
            comment = "-->" not in st
            continue
        if fence or not st or st.startswith(("<!--", "---", "|", "#", ">")) or line.startswith("    "):
            if not fence:
                out.append((n, ""))
            continue
        out.append((n, line))
    return out


args = [a for a in sys.argv[1:] if a != "--strict"]
strict = "--strict" in sys.argv[1:]
if not args:
    args = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split()
tot = 0
for f in args:
    text = open(f, encoding="utf-8").read()
    hits = []
    # join wrapped lines into paragraphs for sentence length
    para, start = "", 0
    for n, line in prose(text) + [(10**9, "")]:
        if line.strip() and not re.match(r"^\s*([-*]|\d+[.)])\s", line) and n != 10**9:
            if not para: start = n
            para += " " + line.strip()
            continue
        if para:
            clean = re.sub(r"\*+", "", re.sub(r"`[^`]*`", "X", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", para)))
            for s in re.split(r"(?<=[.!?])\s+(?=[A-Z*\"“`(])", clean.strip()):
                w = len(s.split())
                if w > 25: hits.append((start, f"{w} words: {s[:70]}..."))
            para = ""
        if n != 10**9 and line.strip():  # list item: check as a sentence
            clean = re.sub(r"\*+", "", re.sub(r"`[^`]*`", "X", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)))
            w = len(clean.split())
            if w > 25: hits.append((n, f"list item {w} words: {clean.strip()[:60]}..."))
    for n, line in prose(text):
        c = re.sub(r"`[^`]*`", "", line)
        for name, pat in (("fluff", FLUFF), ("modal", MODAL), ("contraction", CONTR), ("passive", PASSIVE)):
            for m in re.finditer(pat, c, re.I): hits.append((n, f"{name}: {m.group(0)}"))
        if ";" in c: hits.append((n, "semicolon"))
    hits.sort()
    print(f"{f}: {len(hits)}")
    for n, h in hits[:int(os.environ.get('SHOW', '0'))]: print(f"   {n}: {h}")
    tot += len(hits)
print("total", tot)
sys.exit(1 if strict and tot else 0)
