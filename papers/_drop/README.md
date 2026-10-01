# papers/_drop — the drop folder of the PI

Put a PDF here. The next session finds it, because the session-start hook reports a drop folder
that is not empty. Then the `literature` agent completes the intake:

1. Identify the paper.
2. Verify the identifiers.
3. Register the paper in `../sources.yaml` with a role.
4. Move the file onward.
5. Leave this folder empty.

Git ignores this folder, except this README. Therefore nobody commits a file from here by
accident.

**Never leave a source here "for now".** An unregistered source that someone cites later has no
provenance. The registry exists to prevent the work to rebuild that provenance afterwards.
