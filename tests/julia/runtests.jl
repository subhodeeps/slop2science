# Run with:  make test   (or: julia --project=src/julia tests/julia/runtests.jl)
using Test

@testset "{{PROJECT_PACKAGE}}" begin
    @testset "harness" begin
        # Placeholder so `make test` is meaningful before any module exists.
        @test true
    end

    # One include per module as it is written:
    # include("test_discretization.jl")
    # include("test_assembly.jl")
    # include("test_codegen_roundtrip.jl")   # generated code loads and matches reference points

    # And, per topic, the test that matters most (.claude/rules/implementation.md):
    # a KNOWN-ANSWER test of the FULL chain — assembly, solve, refinement, acceptance —
    # against a problem with an exact closed-form solution, in every precision tier.
    # A chain can be correct piece by piece and wrong end to end; only this test catches that.
    # include("test_known_answer_chain.jl")
end
