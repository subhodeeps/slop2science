# Communication: ASD-STE100

Write to the PI in ASD-STE100 Simplified Technical English. Write Markdown files in the same
way. The standard is public: ASD-STE100, from the AeroSpace and Defence Industries Association
of Europe.

## Where this rule applies

- every explanation, question, report and task update that Claude gives to the PI
- every commit message and every pull request description
- every `.md` file that Claude writes or edits in this repository

## Where this rule does not apply

- quoted source text. Quote it exactly. Do not rewrite it.
- code, commands, file names, identifiers and file content that a tool reads
- technical names and terms of the project, for example "ownership registry". Use the same name
  every time.

## The rules to follow

1. Write short sentences. Use 20 words or fewer in an instruction. Use 25 words or fewer in a
   description.
2. Give one instruction in each sentence. Use the imperative: "Run `make check`."
3. Use the active voice. Use the present simple tense when possible.
4. Use "must" for a mandatory action. Use "can" for a possible action. Do not use `should`,
   `may`, `might` or `could`.
5. Use one word for one meaning. Use the same word for the same thing every time.
6. Do not use idioms, filler or intensifiers. Delete `simply`, `just`, `very` and `basically`.
7. Do not use contractions. Do not use semicolons.
8. Use a paragraph of 6 sentences or fewer. Use a list for steps and for 3 or more items.
9. Put the reason after the instruction, in a separate sentence.
10. Use digits for numbers. Use a full sentence for a warning.

## Questions to the PI

State the decision in the first sentence. Give the options as a list. Give the effect of each
option in one sentence. Mark your recommendation. Do not ask a question that the repository
already answers.

## Check

Run `make lint-ste` to screen Markdown files for the measurable rules: sentence length,
modal verbs, filler words, contractions, semicolons and passive voice. The check does not
verify the STE Dictionary. It cannot certify compliance. A person must review the result.
