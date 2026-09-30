# Status history

The session-by-session record, appended at each `/session-close`. **Not auto-loaded**: it
exists so that `docs/STATUS.md` can hold current state only and stay small.

Newest last. Never rewrite an entry — a record that was true when written stays as written,
even after it is superseded. Corrections are a new entry saying what changed.

## Entry format

    ## <date> — session <id> — <one-line summary>

    Prompt record: docs/prompts/<ID>_<topic>.md
    Commits:       <hashes with subjects>

    Done:
      - <what was completed, with the evidence: script, command, result>

    Started and left incomplete:
      - <what was begun and not finished, and what state it is in>

    Checks run:
      - <command> -> <actual result>

    Decisions:
      - D-NNN <title>

    Orphaned artefacts:
      - <file> -> <disposition>

    Open after this session:
      - <what remains, and who it waits on>

---

(no sessions yet)
