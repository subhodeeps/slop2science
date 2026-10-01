# Communication: ASD-STE100

**This rule is permanent and applies to the whole project.** Write all natural-language text in
ASD-STE100 Simplified Technical English. The AeroSpace and Defence Industries Association of
Europe (ASD) publishes the standard. `CLAUDE.md` §11 states the requirement. This file holds the
details.

This file has no `paths:` limit, so it loads in each session. Each agent in `.claude/agents/`
names it. Each skill runs inside a session or an agent and inherits it. `docs/GUIDE.md` §6 lists
the enforcement.

## Where this rule applies

- all CLI communication: explanations, questions, progress updates and answers
- all reports, summaries, audits and research documents
- each new file and each edit that contains natural-language text
- all Markdown files, status records, handoffs and session notes
- all code comments and docstrings
- all commit messages, pull request descriptions and other generated prose

## Where this rule does not apply

- **Executable code.** Do not change code only to enforce this rule. This includes identifiers,
  APIs, file names, command lines and configuration keys.
- **Mathematical notation** and required technical terms. Use the same term every time (for
  example "ownership registry").
- **Quoted text.** Quote papers, error messages, tool output and the prompts of the PI exactly.
- **Text that a tool reads as data.** Examples: the trigger phrases in `when_to_use`, template
  placeholders and the fixed lines of a hook protocol.

## The rules to follow

1. Write short sentences. Use 20 words or fewer in an instruction. Use 25 words or fewer in a
   description.
2. Give one instruction in each sentence. Use the imperative: "Run `make check`."
3. Use the active voice. Use the present simple tense when possible.
4. Use "must" for a mandatory action. Use "can" for a possible action. Do not use `should`,
   `may`, `might` or `could`.
5. Use one word for one meaning, and the same word for the same thing every time. Use simple
   words. Do not use idioms.
6. Remove each word that adds nothing, but keep the detail that the reader needs. Delete
   `simply`, `just`, `very` and `basically`.
7. Do not use contractions. Do not use semicolons.
8. Use a paragraph of 6 sentences or fewer. Use a list for steps and for 3 or more items.
9. Put the reason after the instruction, in a separate sentence.
10. Use digits for numbers. Use a full sentence for a warning.

Technical accuracy comes first. If a rule makes a statement less exact, keep the exact statement
in the simplest form that stays exact.

## Edit existing text

Write new and changed text in STE. If you change a sentence, rewrite the whole sentence. Do not
restructure a file because you edited one line, unless the PI asks for a full pass. In a full
pass, change only natural-language text. Comments and docstrings follow the same rules. A
comment states what the code does and why, in few words.

## Questions to the PI

State the decision in the first sentence. Give the options as a list. Give the effect of each
option in one sentence. Mark your recommendation. Do not ask a question that the repository
already answers.
