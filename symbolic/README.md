# symbolic — derivation scripts and generated hand-off code

    common/           shared helper code, loaded by path from PROJECT_ROOT, with self-tests
    <topic>/          stage and export scripts for one topic, plus stages.txt and out/
    generated/        machine-written hand-off code; a hook blocks edits

## Per topic

    symbolic/<topic>/
      stages.txt                  the ORDER. Not a glob.
      stage_NN_<what>.<ext>       one derivation stage, with printed labelled checks
      export_NN_<what>.<ext>      codegen into ../generated/<lang>/
      out/                        the persisted result of each stage, as text

`stages.txt` has one path on each line, relative to the topic directory. The tools ignore `#`
comments and blank lines. An export stage is a line whose basename starts with `export_`. The
file exists because glob order is lexical. Lexical order reorders stages silently when someone
renames a stage or adds a tenth stage. This happened (`docs/failure_modes.md`).

    make stages TOPIC=<topic>          run the stages in declared order
    make codegen TOPIC=<topic>         run the exports
    make codegen-check TOPIC=<topic>   regenerate and fail on any diff

The extension can change from line to line. A topic can use more than one tool if two
conditions hold. The header of each stage names the tool that **owns** the topic. A label
`CROSS-CHECK` marks each part in another tool (`docs/toolchain.md`).

Rules: `.claude/rules/derivation.md`. Template:
`.claude/skills/derivation-workflow/templates/stage_template.wls`.
