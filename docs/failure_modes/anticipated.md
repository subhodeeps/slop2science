# Anticipated failure modes

These failures did not happen in this project. The structure of the project guards against them.
The project records them so that the reason for a rule survives when the rule looks like
bureaucracy. If one of them happens, move it to `docs/failure_modes/project.md` with what it
cost. `docs/failure_modes.md` is the index of all failure modes.

### A. A language chosen for convenience, then two records for one fact

Three tools of equal standing make it easy to derive something in one tool. During a debugging
session, someone derives it again in another tool. Someone commits both. Nothing states which
one is authoritative. **The checks of neither tool can detect this.** Each one passes.

Guard: the PI decides which language implements which work, per topic or by the default profile (CLAUDE.md
§1, §5). Then nobody picks a language for convenience. The ownership and interoperation
registries in `docs/toolchain.md` cite a decision in each row. `make check-docs` fails when a
topic has stage scripts and no registry row. A second implementation is a labelled `CROSS-CHECK`.
It is never a second record.

### B. The project that quietly becomes a reproduction project

Reproduction has clear targets, visible progress and an obvious stopping condition. Extension has
none of these. The easy path is to keep reproducing, to report that as progress, and never to
start the new work. The new work is the part that the project is for (CLAUDE.md §2).

Guard: `docs/STATUS.md` and `docs/reproduction_and_extension.md` have separate sections of equal
weight. The source audit must list what the source *does not* do, and not only what it does. The
checklist has an extension phase. The instructions of `status-reporter` say that progress of the
reproduction never stands in for progress of the project.

### C. An extension that someone validates against the source

The source does not contain the results of the extension. Therefore it cannot validate them.
"This agrees with the paper" is a reassuring sentence, and someone writes it anyway. It is
usually about a limiting case that does agree. It reads as if someone checked the whole
extension.

Guard: `Kind:` and `Judged against:` where the project uses a result. Each record requires the
field `judged_against`. `docs/validation_protocol.md` §8 states what an extension can rest on
when no independent benchmark exists.

### C2. A transcript that travels with a shared repository

A session transcript is nearly verbatim. It holds half-formed reasoning, dead ends, and whatever
someone said about a result before anyone was sure of it. People share a repository: with a
collaborator, a supervisor, a journal, and eventually with everyone. **Sharing permissions
inherit downward. You cannot subtract them from a subfolder.** A leading dot does not help.
`.claude/` is hidden in a file browser and it is an ordinary visible folder in a web interface.

Guard: `capture_session.py` writes to `$RESEARCH_RECORDS_DIR` (default
`~/.claude-research-records`), **never inside the repository.** The hook self-tests assert that
nothing leaked in. The design depends on the property *never shared*. It does not depend on the
property *not in the repo*. `handoff.md` is the artifact that other people read, and the project
commits it.

Credit: [benning-lab/agentic-starter](https://github.com/benning-lab/agentic-starter) gave this
argument and the mechanism. This template first committed its prompt logs into the tree. That
was wrong, for the same reason.

### D. A default that someone supplied silently for a decision that belonged to the PI

An assistant that receives a request to proceed will proceed. The missing convention, the unstated
scope boundary and the unassigned language each have an answer that looks obvious. To supply it is
faster than to ask. The cost is not the wrong answer. The cost is that nobody knows that anyone
made a choice.

Guard: the instruction to **stop and ask** and not to supply a default (CLAUDE.md §1). `OPEN` is
a first-class status in `docs/conventions.md`. `/init-paper` records unanswered questions as open
and does not fill them. The field `Options:` of the decision log is impossible to fill honestly
for a decision that nobody made. No hook can enforce this guard. This is why the first section of
the charter states it, and not the last section.

### E. A catalogue entry that someone takes on trust

A reference manager holds the metadata of someone for years. Most of it is correct. Some of it is
wrong. An entry can have the right title and the wrong DOI. It can have a PDF that is a different
version or a different paper. It can have a saved web page in place of the article. After an
import, each of these looks authoritative. The entry sits in `refs.bib` with a clean key. Nothing
marks it as less checked than an entry that someone verified by hand.

Guard: `scripts/library.py import` writes each entry with `verified: false`, in the registry, and
as an UNVERIFIED comment in `refs.bib`. `make check-docs` counts the entries that are still
unverified. The importer never guesses an identifier or a `primaryClass` that the catalogue did
not give. It refuses a saved web page and a file that the catalogue calls a PDF and that is not a
PDF. To verify an entry, someone reads the first page of the copied document. This is the work
of a person or of an agent. A script does not do it
(`.claude/skills/literature-audit/reference/local_libraries.md`).
