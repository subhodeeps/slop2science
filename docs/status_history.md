# Status history

This file is the record of each session. `/session-close` appends an entry. The file **does not
load automatically**. Because of this, `docs/STATUS.md` holds the current state only and stays
small.

Put the newest entry last. Never rewrite an entry. A record that was true when written stays as
written, also after something supersedes it. A correction is a new entry that states what
changed.

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
