# papers/_drop — the drop folder of the PI

Put a PDF here, with its BibTeX entry in a `.bib` file if you have one. You can also give an
arXiv link to Claude instead. The next session finds the files, because the session-start hook
reports a drop folder that is not empty. Then the `literature` agent completes the intake:

1. Identify the paper.
2. Verify the identifiers and the BibTeX entry against the first page of the PDF.
3. Register the paper in `../sources.yaml` with a role, and add the BibTeX entry to
   `../refs.bib`.
4. Move the file onward.
5. Leave this folder empty.

Git ignores this folder, except this README. Therefore nobody commits a file from here by
accident.

**Never leave a source here "for now".** An unregistered source that someone cites later has no
provenance. The registry exists to prevent the work to rebuild that provenance afterwards.
