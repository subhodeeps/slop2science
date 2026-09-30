"""Package entry point. Renamed by /init-paper.

Physics coefficient functions enter ONLY through code generated into
``symbolic/generated/python/`` (CLAUDE.md §5). Never hand-transcribe a coefficient here — if
something a solver needs is missing, stop and derive and export it.

Where extended precision matters, be explicit about every point at which a computation could
silently drop to machine precision: a NumPy call inside an ``mpmath`` chain is the usual
culprit and is invisible in the output.
"""

__version__ = "0.1.0"
