#!/usr/bin/env python3
"""PreToolUse Bash guard, registered in each write-capable subagent's own frontmatter.

A subagent has one job and a fresh context. It does not know what else is in flight, which
branch the PI is on, or what an interrupted session left half-staged -- so it must not be
able to reshape history or publish anything. Reading git is fine and often necessary.

Allowed:   status, log, diff, show, blame, ls-files, rev-parse, describe, cat-file,
           config --get, and staging an explicit path (`git add <path>`).
Blocked:   push, pull, fetch, merge, rebase, reset, revert, cherry-pick, stash, checkout,
           switch, branch, tag, worktree, filter-branch, gc, reflog, remote, submodule,
           clean, restore, commit, commit --amend, and `git add -A/-u/.`.

`git commit` is blocked deliberately: a commit is the project's record, and it is proposed at
`/session-close` or `/checkpoint` by the main session, which can see the whole working tree
(CLAUDE.md §8).

Detection is deliberately blunt. The command string is scanned for a `git` invocation
anywhere in it -- after a path, after `env VAR=x`, inside `bash -c "..."`, inside a heredoc,
after `&&`, `;` or a pipe -- because a guard that only matches a command starting with `git`
is a guard that anything slightly unusual walks straight past. False positives here cost a
subagent one refusal and a message to the PI; a false negative costs rewritten history.
"""
import json
import re
import shlex
import sys

READ_ONLY = {
    "status", "log", "diff", "show", "blame", "ls-files", "ls-tree", "rev-parse",
    "rev-list", "describe", "cat-file", "shortlog", "grep", "count-objects", "var",
    "check-ignore", "diff-tree", "diff-index", "symbolic-ref", "name-rev", "whatchanged",
}
BLOCKED = {
    "push", "pull", "fetch", "clone", "merge", "rebase", "reset", "revert", "cherry-pick",
    "stash", "checkout", "switch", "branch", "tag", "worktree", "filter-branch",
    "filter-repo", "gc", "prune", "reflog", "remote", "submodule", "clean", "restore",
    "commit", "am", "apply", "mv", "rm", "update-ref", "notes", "replace", "bisect",
    "format-patch", "send-email", "archive", "daemon", "init",
}

# Detection is by token scan, not by a clever regex: every shell punctuation character
# that can precede a command -- whitespace, quotes, operators, backticks, braces, heredoc
# boundaries -- is normalized to a space, and the resulting token stream is scanned for a
# `git` invocation anywhere in it. A guard that only matched a command *starting* with `git`
# would be walked past by `bash -c 'git push'`, `env X=1 git reset`, `make x && git push`,
# or a heredoc body. False positives cost one refusal; a false negative costs history.
PUNCT = re.compile(r"""[;&|()<>{}`'"\\\n\t]|\$\(|\|\|""")
GIT_WORD = re.compile(r"^(?:[\w./\\-]*[/\\])?git(?:\.exe)?$", re.IGNORECASE)

GLOBAL_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                          "--exec-path", "--config-env"}


def git_invocations(command):
    """Yield the argument list of every `git ...` call found anywhere in `command`."""
    flat = PUNCT.sub(" ", command)
    try:
        words = shlex.split(flat, comments=True)
    except ValueError:
        words = flat.split()
    for index, word in enumerate(words):
        if GIT_WORD.match(word):
            yield words[index + 1:]


def verdict(command):
    """Return (blocked_subcommand, reason) for the first offending call, else (None, None)."""
    for args in git_invocations(command):
        i = 0
        while i < len(args):                       # skip git's own global options
            if args[i] in GLOBAL_OPTS_WITH_VALUE:
                i += 2
                continue
            if args[i].startswith("-"):
                i += 1
                continue
            break
        if i >= len(args):
            continue
        sub = args[i].lower()
        rest = args[i + 1:]

        if sub == "add":
            if any(a in ("-A", "--all", "-u", "--update", ".", "*", ":/") for a in rest):
                return ("add -A", "stage everything")
            if not rest:
                return ("add", "stage with no explicit path")
            continue                               # `git add <explicit path>` is allowed
        if sub == "config" and any(a in ("--get", "--get-all", "--list", "-l") for a in rest):
            continue
        if sub in READ_ONLY:
            continue
        if sub in BLOCKED:
            return (sub, "change history, the working tree, or the remote")
    return (None, None)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                        # never block on malformed input

    command = (data.get("tool_input") or {}).get("command") or ""
    if not command:
        sys.exit(0)

    sub, reason = verdict(command)
    if sub is None:
        sys.exit(0)

    print(
        f"Blocked `git {sub}`: subagents may read git but not {reason}.\n"
        f"You have a fresh context and cannot see what else is in flight, which branch the "
        f"PI is on, or what an interrupted step left staged.\n"
        f"Report what you changed and why it should be committed; the main session proposes "
        f"the commit at /checkpoint or /session-close (CLAUDE.md §8).",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
