#!/usr/bin/env python3
"""UserPromptSubmit hook: preserve every prompt, because a result whose originating prompt
nobody can find cannot be re-derived or checked for how much the model chose versus was told
(CLAUDE.md §10).

Two destinations, deliberately separated (the project this template came from mixed them and
then needed a README to explain how to tell them apart):

  docs/prompts/log/<session>.md   every prompt of a session, appended, false starts included.
                                  The raw record.
  docs/prompts/auto/<ts>_<session>_<hash>.md
                                  prompts at or above THRESHOLD characters, each in its own
                                  file with an Outcome placeholder. Machine-written.

Curated, citable prompt records live in docs/prompts/<ID>_<topic>.md and are written by hand
(.claude/rules/research-sessions.md). Nothing in this hook writes there.

Harness traffic arrives through this same hook (subagent hand-backs, task notifications, stop
hook feedback) and is not a prompt. It goes to the raw log only. The prefix list below is
best-effort and will go stale as the harness changes; that is acceptable because the failure
mode is a junk file in auto/, not a lost prompt.

Exit 0 with no stdout: nothing is injected into Claude's context.
"""
import datetime
import hashlib
import json
import os
import sys

THRESHOLD = 600

NOT_A_PROMPT_PREFIXES = (
    "<task-notification>",
    "<agent-message",
    "<wake ",
    "<webhook-payload>",
    "<system-reminder>",
    "[SYSTEM NOTIFICATION",
    "[Artifact comment sent to Claude]",
    "Stop hook feedback",
    "Another Claude session sent a message",
    "Caveat: The messages below were generated",
)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        sys.exit(0)

    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    session = (payload.get("session_id") or "unknown")[:8]
    stamp = datetime.datetime.now().astimezone()
    iso = stamp.isoformat(timespec="seconds")

    try:
        logdir = os.path.join(root, "docs", "prompts", "log")
        os.makedirs(logdir, exist_ok=True)
        with open(os.path.join(logdir, f"{session}.md"), "a", encoding="utf-8") as fh:
            fh.write(f"\n## {iso}\n\n```text\n{prompt}\n```\n")

        if len(prompt) >= THRESHOLD and not prompt.startswith(NOT_A_PROMPT_PREFIXES):
            autodir = os.path.join(root, "docs", "prompts", "auto")
            os.makedirs(autodir, exist_ok=True)
            digest = hashlib.sha256(prompt.encode()).hexdigest()[:6]
            name = f"{stamp.strftime('%Y%m%dT%H%M%S')}_{session}_{digest}.md"
            path = os.path.join(autodir, name)
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(
                        f"<!-- session {session} | {iso} | auto-captured by "
                        f".claude/hooks/log_prompt.py -->\n\n"
                        f"# Prompt\n\n```text\n{prompt}\n```\n\n"
                        f"## Outcome\n\n"
                        f"(fill in at session close: what this produced, which commits, "
                        f"and whether the prompt needs revising before reuse. "
                        f"If this turns out to be a substantial research prompt, promote it "
                        f"to a curated record at docs/prompts/<ID>_<topic>.md.)\n"
                    )
    except Exception:
        pass                            # logging must never block a prompt

    sys.exit(0)


if __name__ == "__main__":
    main()
