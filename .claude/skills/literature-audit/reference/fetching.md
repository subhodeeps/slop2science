# Fetch sources

## The rule

Fetch only what a specific, stated need requires. If you download everything that a paper cites,
`papers/` fills with unregistered PDFs. Nobody can reconstruct the role of each PDF. The folder
then looks as if someone consulted all of it.

Register each fetched source in `papers/sources.yaml` **in the same session**, with these
fields:

    label, identifier(s), file (or null), role, notes

`role` is one of: `primary`, `benchmark`, `method-reference`, `background`. `notes` states what
this project needs from the source, in one specific line: "Table 3 is the independent-method
benchmark for topic X". Do not write "background on the method".

## How

    make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>

The command fetches and registers arXiv IDs. It **registers a DOI or a publisher URL and does
not fetch it.** Paywalls and terms differ. A script that appears to fetch anything ends up with
an HTML error page that has the name of a paper. For a DOI or a publisher URL, the PI puts the
file in `papers/_drop/` and the intake finishes the job.

## PDFs are not committed by default

Git ignores `papers/**/*.pdf`. Commit the registry. Then each source stays identifiable and
possible to fetch again, also where nobody can redistribute the file. The PI decides whether to
commit a given PDF. The assistant does not decide this. If the PI wants to commit one, the PI
can remove it from the ignore rules deliberately.

## Read what you fetched

`reference/corpus.md` states the order in one place. Read the `.tex` first. Then read a shipped
data file or figure file. Then read the rendered page image. Never read the text layer. The
expensive mistakes come from the text layer.

## What to never do

- Cite a source that you did not open, however sure you are about what it says.
- Record an identifier that you did not resolve.
- Leave a fetched file unregistered "until we know if we need it".
- Paraphrase the equation of a source into the notation of this project *in the audit record*.
  Record it in the notation of the source. Convert it separately and explicitly.
