"""
Package entry point. Renamed to <PackageName>.jl by /init-paper.

Physics coefficient functions enter ONLY through code generated into
`symbolic/generated/<lang>/` (CLAUDE.md §5). Never hand-transcribe a coefficient here — if
something a solver needs is missing, stop and derive and export it.

Add modules as they are written, one per concern, each with a test in `tests/julia/`.
"""
module Placeholder

const VERSION_STRING = "0.1.0"

# --- generic numerics -------------------------------------------------------------
# include("discretization.jl")
# include("boundary_factors.jl")
# include("assembly.jl")
# include("solve.jl")
# include("filtering.jl")
# include("convergence.jl")
# include("continuation.jl")
# include("records.jl")          # provenance: parameters, versions, git commit -> JSON

# --- topics (only after each topic's derivation gate) -----------------------------
# include("topics/topic1.jl")    # includes ../../../symbolic/generated/julia/topic1_*.jl

end # module
