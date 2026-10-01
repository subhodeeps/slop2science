# Fetching sources

## The rule

Fetch only what a specific, stated need requires. Speculative downloading of everything a
paper cites fills `papers/` with unregistered PDFs whose role nobody can reconstruct, and the
folder then reads as though all of it has been consulted.

Every fetched source is registered in `papers/sources.yaml` **in the same session**, with:

    label, identifier(s), file (or null), role, notes

`role` is one of: `primary`, `benchmark`, `method-reference`, `background`. The `notes` say
what this project actually needs from it — one line, specific: "Table 3 is the
independent-method benchmark for topic X", not "background on the method".

## How

    make fetch-source ID=<arxiv-id> LABEL=<firstauthor><year>

arXiv IDs are fetched and registered. A DOI or publisher URL is **registered but not
fetched**: paywalls and terms differ, and a script that appears to fetch anything ends up
storing an HTML error page named like a paper. For those, the PI puts the file in
`papers/_drop/` and the intake completes it.

## PDFs are not committed by default

`papers/**/*.pdf` is gitignored. The registry is committed, so every source stays identifiable
and re-fetchable even where the file itself cannot be redistributed. Whether to commit a given
PDF is the PI's decision, not the assistant's — if the PI wants one committed, they can
un-ignore it deliberately.

## Reading what you fetched

`reference/corpus.md` is the one place the order is stated: the `.tex` first, then a shipped
data or figure file, then the rendered page image, and never the text layer. Where the
expensive mistakes come from is the last of those.

## What never to do

- Cite a source you have not opened, however confident you are about what it says.
- Record an identifier you have not resolved.
- Leave a fetched file unregistered "until we know if we need it".
- Paraphrase a source's equation into this project's notation *in the audit record*. Record
  it in the source's own notation, and convert separately and explicitly.
