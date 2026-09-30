# symbolic — derivation scripts and generated hand-off code

    common/           shared helper code, loaded by path from PROJECT_ROOT, with self-tests
    <topic>/          stage and export scripts for one topic, plus stages.txt and out/
    generated/        machine-written hand-off code; hook-blocked against editing

## Per topic

    symbolic/<topic>/
      stages.txt                  the ORDER. Not a glob.
      stage_NN_<what>.<ext>       one derivation stage, with printed labelled checks
      export_NN_<what>.<ext>      codegen into ../generated/<lang>/
      out/                        each stage's persisted result, as text

`stages.txt` is one path per line, relative to the topic directory; `#` comments and blank
lines are ignored; export stages are the lines whose basename starts with `export_`. It exists
because glob order is lexical, and lexical order silently reorders stages when one is renamed
or a tenth is added — which happened (`docs/failure_modes.md`).

    make stages TOPIC=<topic>          run the stages in declared order
    make codegen TOPIC=<topic>         run the exports
    make codegen-check TOPIC=<topic>   regenerate and fail on any diff

The extension can differ line to line: a topic may mix tools, as long as each stage's header
names the tool that **owns** the topic and anything in another tool is labelled
`CROSS-CHECK` (`docs/toolchain.md`).

Rules: `.claude/rules/derivation.md`. Template:
`.claude/skills/derivation-workflow/templates/stage_template.wls`.
